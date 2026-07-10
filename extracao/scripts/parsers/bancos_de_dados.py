#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extrai os BANCOS DE DADOS do DOXA a partir do DOM renderizado.

Fontes (DOM final renderizado com JS):
  rendered/page__bancos-de-dados.html
  rendered/post__programas-eleitorais-dos-candidatos-a-prefeito-do-estad.html   (RJ)
  rendered/post__programas-eleitorais-dos-candidatos-a-prefeito-das-capi.html   (Capitais)

Saidas:
  extracted/bancos_de_dados.yaml
  extracted/programas-eleitorais-rj.csv
  extracted/programas-eleitorais-capitais.csv

Regra: nada e inventado. Todo campo e rastreavel ao DOM de origem.
"""
import os, re, csv, json
from bs4 import BeautifulSoup

SP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REN = os.path.join(SP, "rendered")
OUT = os.path.join(SP, "extracted")
os.makedirs(OUT, exist_ok=True)

RJ_HTML = os.path.join(REN, "post__programas-eleitorais-dos-candidatos-a-prefeito-do-estad.html")
CAP_HTML = os.path.join(REN, "post__programas-eleitorais-dos-candidatos-a-prefeito-das-capi.html")
BANCOS_HTML = os.path.join(REN, "page__bancos-de-dados.html")

URL_RE = re.compile(r'https?://[^\s<>"\'\)]+')

def soup_of(path):
    html = open(path, encoding="utf-8").read()
    s = BeautifulSoup(html, "html.parser")
    for t in s(["script", "style", "noscript"]):
        t.decompose()
    return s

def clean(t):
    return re.sub(r"\s+", " ", t).strip()

def extract_urls(cell):
    """Extrai TODAS as urls de uma celula 'Link': tags <a> e urls em texto plano."""
    urls = []
    for a in cell.find_all("a"):
        h = a.get("href")
        if h and h.strip():
            h = h.strip()
            if h not in urls:
                urls.append(h)
    txt = cell.get_text(" ", strip=True)
    for m in URL_RE.findall(txt):
        m = m.rstrip(").,;")
        if m not in urls:
            urls.append(m)
    return urls

# ---------------------------------------------------------------------------
# 1) RJ: tabela com Municipio | Candidato | Cargo | Partido | Condicao |
#        Paginas da Proposta | Link
#    Municipio usa rowspan; ha celulas vazias no fim das linhas (ruido).
# ---------------------------------------------------------------------------
def parse_rj():
    s = soup_of(RJ_HTML)
    tbl = s.find("table")
    rows = tbl.find_all("tr")
    header = [clean(c.get_text(" ", strip=True)) for c in rows[0].find_all(["td", "th"])]
    assert header[:7] == ["Município", "Candidato(a)", "Cargo", "Partido",
                          "Condição", "Páginas da Proposta", "Link"], header

    records = []
    # Rowspan afeta APENAS a coluna 0 (Município). Rastreamos quantas linhas
    # ainda estao cobertas pelo rowspan do municipio corrente. Quando a cobertura
    # se esgota, a 1a celula da linha e o proprio municipio (mesmo sem rowspan,
    # caso de municipios com 1 unico candidato, ex.: Macuco).
    active_mun = None  # [linhas_restantes, texto_municipio]
    stats = {"anchors": 0, "text_only": 0, "pdf": 0, "img": 0, "other": 0,
             "rows_com_url": 0, "municipios": set()}
    for r in rows[1:]:
        cells = r.find_all(["td", "th"])
        if not cells:
            continue
        # linha totalmente vazia (sem texto e sem links) -> ignora
        if not any(clean(c.get_text(" ", strip=True)) or c.find("a") for c in cells):
            continue
        # linha "Fonte: ..." no rodape da tabela nao e candidato
        if clean(cells[0].get_text(" ", strip=True)).lower().startswith("fonte"):
            continue
        if active_mun and active_mun[0] > 0:
            cur_mun = active_mun[1]
            active_mun[0] -= 1
            body = cells                # municipio coberto por rowspan acima
        else:
            first = cells[0]
            cur_mun = clean(first.get_text(" ", strip=True))
            rs = int(first.get("rowspan", 1) or 1)
            active_mun = [rs - 1, cur_mun] if rs > 1 else None
            body = cells[1:]            # remove a celula de municipio
        # body = [Candidato, Cargo, Partido, Condicao, Paginas, Link, (vazias...)]
        def g(i):
            return clean(body[i].get_text(" ", strip=True)) if i < len(body) else ""
        candidato = g(0)
        cargo     = g(1)
        partido   = g(2)
        condicao  = g(3)
        paginas   = g(4)
        link_cell = body[5] if len(body) > 5 else None
        urls = extract_urls(link_cell) if link_cell is not None else []

        # contagem/estatistica de urls
        anchors = ([a.get("href").strip() for a in link_cell.find_all("a")
                    if a.get("href") and a.get("href").strip()]
                   if link_cell is not None else [])
        stats["anchors"] += len(anchors)
        stats["text_only"] += max(0, len(urls) - len(anchors))
        for u in urls:
            ul = u.lower()
            if ul.endswith(".pdf"):
                stats["pdf"] += 1
            elif ul.endswith((".jpg", ".jpeg", ".png")):
                stats["img"] += 1
            else:
                stats["other"] += 1
        if urls:
            stats["rows_com_url"] += 1
        stats["municipios"].add(cur_mun)

        # ano: rastreavel a partir do path da url do TSE (/oficial/2020/RJ/...)
        ano = ""
        for u in urls:
            m = re.search(r"/oficial/(\d{4})/", u)
            if m:
                ano = m.group(1)
                break
        if not ano:
            ano = "2020"  # eleicoes municipais de 2020 (mesmo pleito da tabela)

        records.append({
            "municipio": cur_mun,
            "candidato": candidato,
            "cargo": cargo,
            "partido": partido,
            "condicao": condicao,
            "paginas_proposta": paginas,
            "ano": ano,
            "num_arquivos": len(urls),
            "url": " | ".join(urls),
        })

    cols = ["municipio", "candidato", "cargo", "partido", "condicao",
            "paginas_proposta", "ano", "num_arquivos", "url"]
    path = os.path.join(OUT, "programas-eleitorais-rj.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(records)

    stats["municipios"] = len(stats["municipios"])
    stats["total_candidatos"] = len(records)
    stats["total_urls"] = stats["pdf"] + stats["img"] + stats["other"]
    stats["sem_url"] = len(records) - stats["rows_com_url"]
    return records, stats, path

# ---------------------------------------------------------------------------
# 2) Capitais: tabela com Municipio | Candidato | Partido |
#              Proposta 1..5  (texto transcrito, sem links)
# ---------------------------------------------------------------------------
def parse_capitais():
    s = soup_of(CAP_HTML)
    tbl = s.find("table")
    rows = tbl.find_all("tr")
    header = [clean(c.get_text(" ", strip=True)) for c in rows[0].find_all(["td", "th"])]
    assert header[:3] == ["Município", "Candidato", "Partido"], header

    records = []
    municipios = set()
    for r in rows[1:]:
        cells = r.find_all(["td", "th"])
        vals = [clean(c.get_text(" ", strip=True)) for c in cells]
        municipio = vals[0]
        candidato = vals[1]
        partido   = vals[2]
        props = vals[3:8] + ["", "", "", "", ""]
        municipios.add(municipio)
        records.append({
            "municipio": municipio,
            "candidato": candidato,
            "partido": partido,
            "ano": "2020",  # titulo do post: "das Capitais - 2020"
            "proposta_1": props[0],
            "proposta_2": props[1],
            "proposta_3": props[2],
            "proposta_4": props[3],
            "proposta_5": props[4],
        })

    cols = ["municipio", "candidato", "partido", "ano",
            "proposta_1", "proposta_2", "proposta_3", "proposta_4", "proposta_5"]
    path = os.path.join(OUT, "programas-eleitorais-capitais.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(records)

    stats = {"total_candidatos": len(records), "municipios": len(municipios),
             "lista_municipios": sorted(municipios)}
    return records, stats, path

# ---------------------------------------------------------------------------
# 3) Catalogo dos bancos (page__bancos-de-dados)
# ---------------------------------------------------------------------------
def parse_catalogo(rj_stats, cap_stats):
    s = soup_of(BANCOS_HTML)
    main = s.find(id="jupiterx-main") or s.body
    # Coleta blocos: cada H2 (exceto o titulo geral) + o <p> seguinte + botao <a>
    catalogo = []
    for h2 in main.find_all("h2"):
        title = clean(h2.get_text(" ", strip=True))
        if title == "Bancos de Dados":
            continue
        # descricao = primeiro <p> depois do h2; url = primeiro <a> "Veja..."
        desc = ""
        url = ""
        for sib in h2.find_all_next(["p", "a", "h2"]):
            if sib.name == "h2":
                break
            if sib.name == "p" and not desc:
                desc = clean(sib.get_text(" ", strip=True))
            if sib.name == "a" and sib.get("href") and not url:
                url = sib.get("href").strip()
            if desc and url:
                break
        catalogo.append({"nome": title, "descricao": desc, "url": url})
    return catalogo

def write_catalogo_yaml(catalogo, rj_stats, cap_stats):
    """Enriquece o catalogo com cobertura factual (derivada dos dados) e grava YAML."""
    import yaml
    FONTE = "https://www.lab-doxa.org.br/bancos-de-dados/"
    for c in catalogo:
        nome = c["nome"]
        c["fonte"] = FONTE
        if "Rio de Janeiro" in nome:
            c["cobertura"] = (
                f"{rj_stats['municipios']} municipios do Estado do Rio de Janeiro; "
                f"eleicoes municipais de 2020; {rj_stats['total_candidatos']} candidatos a "
                f"prefeito ({rj_stats['rows_com_url']} com programa disponivel, "
                f"{rj_stats['sem_url']} sem programa). "
                f"{rj_stats['total_urls']} arquivos de proposta "
                f"({rj_stats['pdf']} PDF + {rj_stats['img']} imagens) hospedados no TSE "
                f"(divulgacandcontas.tse.jus.br)."
            )
            c["arquivo"] = "programas-eleitorais-rj.csv"
            c["registros"] = rj_stats["total_candidatos"]
        elif "Capitais" in nome:
            c["cobertura"] = (
                f"{cap_stats['municipios']} capitais e grandes cidades; eleicoes municipais "
                f"de 2020; {cap_stats['total_candidatos']} candidatos a prefeito; "
                f"ate 5 propostas transcritas por candidato."
            )
            c["arquivo"] = "programas-eleitorais-capitais.csv"
            c["registros"] = cap_stats["total_candidatos"]
        elif "Mapas" in nome:
            c["cobertura"] = (
                "Distribuicao dos votos dos candidatos por bairro na cidade do Rio de "
                "Janeiro (projeto 'Geografia do voto no Estado do Rio de Janeiro'). "
                "Listagem completa em pagina externa (nao extraida nesta tarefa)."
            )
        # ordem dos campos
    ordered = []
    for c in catalogo:
        o = {}
        for k in ("nome", "descricao", "cobertura", "url", "arquivo", "registros", "fonte"):
            if k in c and c[k] != "":
                o[k] = c[k]
        ordered.append(o)

    header = (
        "# Bancos de Dados do DOXA\n"
        "# Fonte: https://www.lab-doxa.org.br/bancos-de-dados/ "
        "(rendered/page__bancos-de-dados.html)\n"
        "# Campos: nome, descricao, cobertura, url, arquivo (csv), registros, fonte\n"
        "# 'descricao' e 'url' sao exatos da pagina de origem; 'cobertura'/'registros'\n"
        "# sao derivados da contagem real dos dados extraidos (rastreaveis).\n"
        "# Obs.: o menu do site tambem lista 'Cobertura Jornalistica' (#cobjor) e um item\n"
        "# 'Horario Eleitoral Gratuito' (#hpge), mas a pagina original nao possui conteudo\n"
        "# para esses itens; por isso nao constam como bancos aqui.\n\n"
    )
    path = os.path.join(OUT, "bancos_de_dados.yaml")
    with open(path, "w", encoding="utf-8") as f:
        f.write(header)
        yaml.safe_dump(ordered, f, allow_unicode=True, sort_keys=False,
                       default_flow_style=False, width=100)
    return path


def main():
    rj_records, rj_stats, rj_path = parse_rj()
    cap_records, cap_stats, cap_path = parse_capitais()
    catalogo = parse_catalogo(rj_stats, cap_stats)
    yaml_path = write_catalogo_yaml(catalogo, rj_stats, cap_stats)

    print("RJ:", json.dumps({k: v for k, v in rj_stats.items()}, ensure_ascii=False))
    print("CAP:", json.dumps(cap_stats, ensure_ascii=False))
    print("CATALOGO nomes:", [c["nome"] for c in catalogo])
    print("Wrote:", rj_path, cap_path, yaml_path)
    return rj_records, rj_stats, cap_records, cap_stats, catalogo

if __name__ == "__main__":
    main()
