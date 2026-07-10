#!/usr/bin/env python3
"""
Extrai os MAPAS DE VOTACAO do DOXA (pagina "Mapas de votacao").

Fonte:
  rendered/page__mapas-de-votacao.links.json  -> [{href,text}] de todos os links (273 PDFs)
  rendered/page__mapas-de-votacao.html        -> DOM final (usado para confirmar rotulos)

Estrutura da pagina (confirmada no DOM):
  Regiao: "Municipio do Rio de Janeiro" (IESP-UERJ)
  Abas de categoria:
    - "Deputado Federal"  (proporcional)  -> arquivos  <PARTIDO>-DF<ANO>.pdf
    - "Deputado Estadual" (proporcional)  -> arquivos  <PARTIDO>-DE<ANO>.pdf
    - "Majoritarias":
        - "Presidentes"  -> p_<ANO>.pdf
        - "Governadores" -> g_<ANO>.pdf
        - "Senadores"    -> s_<ANO>.pdf
  Texto introdutorio da pagina:
    "Mapas da distribuicao da votacao para os cargos majoritario - Presidente,
     Governador e Senador - e proporcionais - Deputado ..."

Mapeamento (codigo no nome do arquivo -> cargo/eleicao), todos rastreaveis aos
rotulos das abas e ao texto introdutorio:
  DF -> cargo "Deputado Federal",  eleicao "Proporcional"
  DE -> cargo "Deputado Estadual", eleicao "Proporcional"
  p  -> cargo "Presidente",        eleicao "Majoritaria"
  g  -> cargo "Governador",        eleicao "Majoritaria"
  s  -> cargo "Senador",           eleicao "Majoritaria"

Campos:
  ano     -> ano no nome do arquivo (== texto-ancora nas majoritarias)
  eleicao -> "Majoritaria" | "Proporcional"
  cargo   -> ver mapeamento
  turno   -> "" (a fonte NAO informa turno em nenhum lugar)
  titulo  -> partido (texto-ancora) nos mapas proporcionais; "" nas majoritarias
             (nas majoritarias o texto-ancora e apenas o ano, ja capturado por 'ano')
  url     -> href absoluto do PDF
"""
import json
import re
import csv
import os
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
LINKS = os.path.join(BASE, "rendered", "page__mapas-de-votacao.links.json")
OUT_CSV = os.path.join(BASE, "extracted", "mapas-votacao.csv")
OUT_YAML = os.path.join(BASE, "extracted", "mapas_votacao.yaml")

PROP = re.compile(r"^(?P<party>.+?)-(?P<code>DF|DE)(?P<year>\d{4})(?:-\d+)?\.pdf$")
MAJ = re.compile(r"^(?P<code>[gps])_(?P<year>\d{4})\.pdf$")

CARGO = {
    "DF": ("Deputado Federal", "Proporcional"),
    "DE": ("Deputado Estadual", "Proporcional"),
    "p": ("Presidente", "Majoritaria"),
    "g": ("Governador", "Majoritaria"),
    "s": ("Senador", "Majoritaria"),
}


def main():
    links = json.load(open(LINKS, encoding="utf-8"))
    pdfs = [x for x in links if x["href"].lower().endswith(".pdf")]

    # dedup por URL preservando ordem
    seen = set()
    rows = []
    unmatched = []
    for x in pdfs:
        url = x["href"]
        if url in seen:
            continue
        seen.add(url)
        fn = url.rsplit("/", 1)[-1]
        anchor = (x.get("text") or "").strip()
        m = PROP.match(fn)
        if m:
            cargo, eleicao = CARGO[m.group("code")]
            rows.append({
                "ano": m.group("year"),
                "eleicao": eleicao,
                "cargo": cargo,
                "turno": "",
                "titulo": anchor,  # partido
                "url": url,
            })
            continue
        m = MAJ.match(fn)
        if m:
            cargo, eleicao = CARGO[m.group("code")]
            rows.append({
                "ano": m.group("year"),
                "eleicao": eleicao,
                "cargo": cargo,
                "turno": "",
                "titulo": "",  # ancora e apenas o ano (== 'ano')
                "url": url,
            })
            continue
        unmatched.append(fn)

    if unmatched:
        raise SystemExit("Arquivos nao reconhecidos: %r" % unmatched)

    # ordena: ano, cargo, titulo para saida estavel
    rows.sort(key=lambda r: (r["ano"], r["cargo"], r["titulo"]))

    os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True)
    with open(OUT_CSV, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["ano", "eleicao", "cargo", "turno", "titulo", "url"])
        w.writeheader()
        w.writerows(rows)

    # sumario
    total = len(rows)
    by_year = Counter(r["ano"] for r in rows)
    by_cargo = Counter(r["cargo"] for r in rows)
    by_eleicao = Counter(r["eleicao"] for r in rows)

    def yq(s):
        return '"' + str(s).replace("\\", "\\\\").replace('"', '\\"') + '"'

    lines = []
    lines.append("# Mapas de votacao - sumario da extracao")
    lines.append("dominio: mapas_votacao")
    lines.append("fonte_pagina: " + yq("https://www.lab-doxa.org.br/mapas-de-votacao/"))
    lines.append("fonte_local: " + yq("rendered/page__mapas-de-votacao.html"))
    lines.append("fonte_links: " + yq("rendered/page__mapas-de-votacao.links.json"))
    lines.append("csv: " + yq(os.path.relpath(OUT_CSV, BASE)))
    lines.append("csv_abs: " + yq(OUT_CSV))
    lines.append("regiao: " + yq("Municipio do Rio de Janeiro"))
    lines.append("total_pdfs: %d" % total)
    lines.append("colunas: [ano, eleicao, cargo, turno, titulo, url]")
    lines.append("nota_turno: " + yq("A fonte nao informa turno em nenhum ponto; campo 'turno' fica vazio."))
    lines.append("nota_eleicao: " + yq("'eleicao' = sistema eleitoral (Majoritaria/Proporcional), conforme abas e texto introdutorio da pagina."))
    lines.append("nota_titulo: " + yq("Nos mapas proporcionais 'titulo' = sigla do partido (texto-ancora); nas majoritarias fica vazio pois a ancora e apenas o ano."))
    lines.append("por_ano:")
    for k in sorted(by_year):
        lines.append("  '%s': %d" % (k, by_year[k]))
    lines.append("por_cargo:")
    for k in sorted(by_cargo, key=lambda x: -by_cargo[x]):
        lines.append("  %s: %d" % (yq(k), by_cargo[k]))
    lines.append("por_eleicao:")
    for k in sorted(by_eleicao, key=lambda x: -by_eleicao[x]):
        lines.append("  %s: %d" % (yq(k), by_eleicao[k]))
    # combinacao cargo x ano (auditoria)
    combo = defaultdict(int)
    for r in rows:
        combo[(r["cargo"], r["ano"])] += 1
    lines.append("por_cargo_ano:")
    for (cargo, ano) in sorted(combo):
        lines.append("  %s: %d" % (yq(cargo + " " + ano), combo[(cargo, ano)]))

    with open(OUT_YAML, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print("total pdfs:", total)
    print("por eleicao:", dict(by_eleicao))
    print("por cargo:", dict(by_cargo))
    print("por ano:", dict(sorted(by_year.items())))
    print("CSV:", OUT_CSV)
    print("YAML:", OUT_YAML)


if __name__ == "__main__":
    main()
