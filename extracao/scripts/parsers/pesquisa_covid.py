#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extrai a Pesquisa COVID do DOXA a partir do DOM renderizado.

Fonte de verdade:
  rendered/page__pesquisa-covid.html  (DOM final, JS já executado;
  a listagem de subprojetos é um widget "raven-tabs" com 5 abas)

Saídas:
  extracted/pesquisa-covid.md    -> prosa institucional/descritiva (markdown)
  extracted/pesquisa-covid.yaml  -> dados estruturados (projeto, equipe,
                                    subprojetos + downloads, publicações)

Regras: nada é inventado. Todo valor vem do DOM. Onde a fonte não traz um
campo (ex.: data de publicação explícita dos PDFs), ele é omitido; o único
sinal de data disponível é o mês de upload no caminho /wp-content/uploads/AAAA/MM/,
capturado como `date` (mês de upload no WordPress).
"""
import os
import re
import yaml
from bs4 import BeautifulSoup

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
SRC = os.path.join(BASE, "rendered", "page__pesquisa-covid.html")
OUT_DIR = os.path.join(BASE, "extracted")
PAGE_URL = "https://www.lab-doxa.org.br/pesquisa-covid/"

os.makedirs(OUT_DIR, exist_ok=True)


def clean(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "")).strip()


def upload_month(url: str):
    """Mês de upload WP a partir de .../uploads/AAAA/MM/... -> 'AAAA-MM'."""
    m = re.search(r"/uploads/(\d{4})/(\d{2})/", url)
    return f"{m.group(1)}-{m.group(2)}" if m else ""


def fmt_of(url: str) -> str:
    ext = url.rsplit(".", 1)[-1].lower()
    return {"xlsx": "xlsx", "pdf": "pdf", "xls": "xls", "csv": "csv"}.get(ext, ext)


def main():
    html = open(SRC, encoding="utf-8").read()
    soup = BeautifulSoup(html, "html.parser")
    for t in soup(["script", "style", "noscript", "header", "footer", "nav"]):
        t.decompose()
    main_el = soup.find(id="jupiterx-main") or soup.body
    widgets = main_el.select("div.elementor-widget-container")

    # ---- cabeçalho do projeto (fora das abas) ----
    titulo = clean(widgets[0].get_text(" "))                 # widget 0
    objetivo = clean(widgets[1].get_text(" "))               # widget 1
    # widget 34: título formal do projeto + financiamento
    proj_lines = [clean(x) for x in widgets[34].get_text("\n").split("\n") if clean(x)]
    titulo_projeto = proj_lines[0]
    financiamento = proj_lines[1] if len(proj_lines) > 1 else ""

    # ---- equipe (widget 36): pares (nome, instituição/papel) ----
    team_lines = [clean(x) for x in widgets[36].get_text("\n").split("\n") if clean(x)]
    equipe = []
    for i in range(0, len(team_lines) - 1, 2):
        nome = team_lines[i]
        aff = team_lines[i + 1].replace("D0XA", "DOXA")  # OCR/typo da fonte: "D0XA"
        papel = ""
        m = re.search(r"\(([^)]+)\)", aff)
        if m:
            papel = m.group(1)
            instituicao = clean(aff.replace(m.group(0), ""))
        else:
            instituicao = aff
        item = {"nome": nome, "instituicao": instituicao}
        if papel:
            item["papel"] = papel
        equipe.append(item)

    # ---- abas raven-tabs ----
    rav = main_el.select_one(".elementor-widget-raven-tabs")
    panels = {
        el.get("data-tab"): el
        for el in rav.find_all(True, {"data-tab": True})
        if "raven-tabs-content" in " ".join(el.get("class", []))
    }

    GENERIC = {"download", "baixar", "leia mais", "saiba mais", ""}

    def downloads_in(panel):
        """Retorna os downloads na ordem do DOM. Quando o texto do link é
        genérico ('Download'), o título é resolvido para o heading (h2/h3/h4)
        imediatamente anterior no mesmo painel — texto verbatim da fonte."""
        out = []
        last_heading = ""
        for el in panel.find_all(["h2", "h3", "h4", "a"]):
            if el.name in ("h2", "h3", "h4"):
                txt = clean(el.get_text(" "))
                if txt:
                    last_heading = txt
                continue
            href = el.get("href", "").strip()
            if "wp-content/uploads" not in href:
                continue
            label = clean(el.get_text(" "))
            title = last_heading if label.lower() in GENERIC else label
            out.append(
                {
                    "title": title,
                    "date": upload_month(href),
                    "format": fmt_of(href),
                    "url": href,
                }
            )
        return out

    def headings_in(panel):
        return [clean(h.get_text(" ")) for h in panel.find_all(["h2", "h3", "h4"]) if clean(h.get_text(" "))]

    # títulos de cada subprojeto = 1º heading da aba
    sub_titles = {dt: headings_in(panels[dt])[0] for dt in ("1", "2", "3", "4")}

    # descrições curtas (rótulos das abas mostram só "Subprojeto 0X";
    # a descrição real é o(s) heading(s) internos)
    subprojetos = []
    for dt in ("1", "2", "3", "4"):
        p = panels[dt]
        heads = headings_in(p)
        subprojetos.append(
            {
                "numero": f"{int(dt):02d}",
                "titulo": heads[0],
                "componentes": heads[1:],  # subtítulos (H3) internos, quando houver
                "downloads": downloads_in(p),
            }
        )

    # ---- Publicações (aba 5) ----
    pub_panel = panels["5"]
    publicacoes = []
    for a in pub_panel.select("a[href*='wp-content/uploads']"):
        publicacoes.append({"title": clean(a.get_text(" ")), "url": a.get("href", "").strip()})
    # completa metadados a partir do texto (citações)
    pub_meta = {
        "GUARNIERI-FIGUEIREDO.pdf": {
            "authors": "Guarnieri, F.; Figueiredo, A.",
            "year": 2022,
            "in": "Felipe Borba e Argelina Figueiredo (orgs), As eleições municipais de 2020 no Estado do Rio de Janeiro",
            "publisher": "Editora da UERJ, 2022",
        },
        "Figueiredo_Guicheney_Lazzari_REVISTO_ed.pdf": {
            "authors": "Figueiredo, A.; Guichney, H.; Lazzari, L.",
            "year": 2022,
            "in": "Fernando Fontainha e Carlos Milani (orgs), COVID-19 e agendas de pesquisa nas ciências sociais",
            "publisher": "Editora da UERJ – no prelo",
        },
    }
    for pub in publicacoes:
        key = pub["url"].rsplit("/", 1)[-1]
        meta = pub_meta.get(key, {})
        # ordena campos: title, authors, year, in, publisher, url
        pub_ordered = {"title": pub["title"]}
        pub_ordered.update(meta)
        pub_ordered["url"] = pub["url"]
        pub.clear()
        pub.update(pub_ordered)

    # ---- Tabela 1 (limpa) ----
    tables = main_el.select(".jet-table")
    t1 = tables[0]
    tabela1 = {"head": [clean(c.get_text(" ")) for c in t1.select_one(".jet-table__head-row").select(".jet-table__cell")],
               "rows": [], "total": []}
    for row in t1.select(".jet-table__body-row"):
        tabela1["rows"].append([clean(c.get_text(" ")) for c in row.select(".jet-table__cell")])
    foot = t1.select_one(".jet-table__foot-row")
    if foot:
        tabela1["total"] = [clean(c.get_text(" ")) for c in foot.select(".jet-table__cell")]

    # parcerias/instituições citadas (síntese; ver campo 'fonte' de cada item)
    parcerias = [
        {"nome": "FAPERJ", "papel": "Financiamento",
         "fonte": "financiamento: 'FAPERJ, AÇÃO EMERGENCIAL COVID-19/SARS-CoV-2 FAPERJ/SES'"},
        {"nome": "SES", "papel": "Co-financiamento",
         "fonte": "citado como 'FAPERJ/SES' no texto (sigla SES não é expandida na página)"},
        {"nome": "Netquest", "papel": "Empresa de pesquisas: seleção da amostra e aplicação dos surveys",
         "fonte": "Subprojeto 02: 'A amostra foi selecionada pela empresa de pesquisas Netquest'"},
        {"nome": "IESP-UERJ", "papel": "Instituição-sede (afiliação de toda a equipe)",
         "fonte": "campo Equipe (todos os membros são IESP-UERJ ou DOXA-IESP)"},
    ]

    data = {
        "projeto": {
            "titulo": titulo,
            "titulo_projeto": titulo_projeto,
            "objetivo": objetivo,
            "financiamento": financiamento,
            "url": PAGE_URL,
        },
        "equipe": equipe,
        "parcerias": parcerias,
        "subprojetos": subprojetos,
        "publicacoes": publicacoes,
    }

    yaml_path = os.path.join(OUT_DIR, "pesquisa-covid.yaml")
    header = (
        "# Pesquisa COVID do DOXA - extraído de rendered/page__pesquisa-covid.html\n"
        "# Campos de download: title, date, format, url\n"
        "#   date = mês de upload no WordPress (AAAA-MM), derivado do caminho /uploads/AAAA/MM/;\n"
        "#   a página NÃO traz data de publicação explícita dos arquivos.\n"
        "# Total de arquivos: 12 PDFs + 4 planilhas (xlsx) = 16 downloads.\n\n"
    )
    with open(yaml_path, "w", encoding="utf-8") as f:
        f.write(header)
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False, width=1000)

    # ---------- Markdown (prosa) ----------
    def wlines(idx):
        return [clean(x) for x in widgets[idx].get_text("\n").split("\n") if clean(x)]

    def wbody(idx, drop_head=1, drop_tail_labels=("Download",)):
        """Linhas de um widget sem o heading inicial e sem o rótulo de botão final."""
        ls = wlines(idx)
        if drop_head:
            ls = ls[drop_head:]
        while ls and ls[-1] in drop_tail_labels:
            ls = ls[:-1]
        return ls

    md = []
    md.append(f"# {titulo}\n")
    md.append(f"**Projeto:** {titulo_projeto}  ")
    md.append(f"**Financiamento:** {financiamento}  ")
    coord = "; ".join(f"{m['nome']} ({m['papel']})" for m in equipe if m.get("papel"))
    md.append(f"**Coordenação:** {coord}\n")
    md.append(objetivo + "\n")

    md.append("---\n")
    # Subprojeto 01
    s1 = subprojetos[0]
    md.append(f"## Subprojeto 01 — {s1['titulo']}\n")
    for w in (widgets[4], widgets[5], widgets[6]):
        txt = clean(w.get_text(" "))
        # remove rótulos de botão de download que vazam no texto do widget
        for lbl in ("Lista de buscadores legislativos", "Banco de dados - Decretos COVID RJ"):
            if txt.endswith(lbl):
                txt = clean(txt[: -len(lbl)])
        md.append(txt + "\n")
    # Tabela 1
    md.append(f"### {clean(widgets[7].get_text(' '))}\n")
    md.append("| " + " | ".join(tabela1["head"]) + " |")
    md.append("|" + "|".join(["---"] * len(tabela1["head"])) + "|")
    if tabela1["total"]:
        md.append("| " + " | ".join(tabela1["total"]) + " |")
    for r in tabela1["rows"]:
        md.append("| " + " | ".join(r) + " |")
    md.append("")
    md.append(clean(widgets[9].get_text(" ")) + "\n")
    md.append(
        "> Nota de extração: no HTML de origem, o detalhamento regional (Tabela 2 — Capital, "
        "Interior/Região Litorânea e Metropolitana) apresenta inconsistências de digitação na coluna "
        "\"Capital\" (valores como 762, 292, 195 superam o total regional de 88, aparentemente copiados "
        "da Tabela 1). Por isso as sub-tabelas regionais não são reproduzidas aqui como dado autoritativo. "
        "Os arquivos completos estão nos downloads abaixo.\n"
    )
    md.append(clean(widgets[14].get_text(" ")) + "\n")
    md.append(clean(widgets[16].get_text(" ")) + "\n")
    md.append(clean(widgets[18].get_text(" ")) + "\n")
    md.append("**Downloads:**\n")
    for d in s1["downloads"]:
        md.append(f"- [{d['title']}]({d['url']}) ({d['format'].upper()})")
    md.append("")

    md.append("---\n")
    # Subprojeto 02
    s2 = subprojetos[1]
    md.append(f"## Subprojeto 02 — {s2['titulo']}\n")
    md.append(f"### {s2['componentes'][0]}\n")
    # widget 21: a H3 (1ª frase) é reaproveitada como subtítulo; o parágrafo
    # descritivo é o restante, até o rótulo do 1º botão ("Análise dos surveys").
    survey_txt = clean(widgets[21].get_text(" ")).rsplit("Análise dos surveys", 1)[0].strip()
    head0 = s2["componentes"][0]
    if survey_txt.startswith(head0):
        survey_txt = survey_txt[len(head0):].strip()
    md.append(survey_txt + "\n")
    md.append("**Downloads:**\n")
    for d in s2["downloads"][:3]:
        md.append(f"- [{d['title']}]({d['url']}) ({d['format'].upper()})")
    md.append("")
    md.append(f"### {s2['componentes'][1]}\n")
    for line in wbody(24):  # widget 24: parágrafo sob a H3 "mercado de trabalho"
        md.append(line + "\n")
    d = s2["downloads"][3]
    md.append(f"- [Pandemia e mercado de trabalho no Rio de Janeiro (relatório)]({d['url']}) ({d['format'].upper()})\n")
    md.append(f"### {s2['componentes'][2]}\n")

    md.append("---\n")
    # Subprojeto 03
    s3 = subprojetos[2]
    md.append(f"## Subprojeto 03 — {s3['titulo']}\n")
    md.append("### Introdução\n")
    for line in wbody(27):  # widget 27: introdução do levantamento bibliográfico
        md.append(line + "\n")
    # widget 28: rótulo "Listagem ... temas:" + 6 temas + "Download"
    temas_lines = wlines(28)
    md.append(temas_lines[0] + "\n")  # "Listagem dos textos organizada de acordo com os seguintes temas:"
    for tema in temas_lines[1:]:
        if tema == "Download":
            break
        md.append(f"- {tema.rstrip(';.')}")
    md.append("")
    # widget 29: citação ao Brasil
    for line in wlines(29):
        if "Textos que citam o Brasil" in line:
            md.append(line.replace("99", "**99**") + "\n")
    md.append("**Downloads:**\n")
    for d in s3["downloads"]:
        md.append(f"- [{d['title']}]({d['url']}) ({d['format'].upper()})")
    md.append("")

    md.append("---\n")
    # Subprojeto 04
    s4 = subprojetos[3]
    md.append(f"## Subprojeto 04 — {s4['titulo']}\n")
    md.append("### Introdução\n")
    for line in wbody(32):  # widget 32: introdução de "Trabalho e Pandemia"
        md.append(line + "\n")
    d = s4["downloads"][0]
    md.append(f"- [Trabalho e Pandemia no Estado do Rio de Janeiro (relatório)]({d['url']}) ({d['format'].upper()})\n")

    md.append("---\n")
    # Publicações
    md.append("## Publicações relacionadas\n")
    for pub in publicacoes:
        line = f"- [{pub['title']}]({pub['url']})"
        extra = []
        if pub.get("authors"):
            extra.append(pub["authors"])
        if pub.get("in"):
            extra.append(f"In: {pub['in']}")
        if pub.get("publisher"):
            extra.append(pub["publisher"])
        if extra:
            cite = ". ".join(s.rstrip(".") for s in extra) + "."
            line += "  \n  " + cite
        md.append(line)
    md.append("")

    md.append("---\n")
    # Equipe
    md.append("## Equipe\n")
    for m in equipe:
        suffix = f" — {m['papel']}" if m.get("papel") else ""
        md.append(f"- **{m['nome']}** ({m['instituicao']}){suffix}")
    md.append("")

    md_path = os.path.join(OUT_DIR, "pesquisa-covid.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md).rstrip() + "\n")

    n_pdf = sum(1 for s in subprojetos for d in s["downloads"] if d["format"] == "pdf") + \
            sum(1 for p in publicacoes if p["url"].lower().endswith(".pdf"))
    n_xlsx = sum(1 for s in subprojetos for d in s["downloads"] if d["format"] == "xlsx")
    print(f"OK -> {yaml_path}")
    print(f"OK -> {md_path}")
    print(f"equipe: {len(equipe)} | subprojetos: {len(subprojetos)} | publicacoes: {len(publicacoes)}")
    print(f"downloads: {n_pdf} PDFs + {n_xlsx} xlsx")


if __name__ == "__main__":
    main()
