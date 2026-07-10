#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parser das PUBLICAÇÕES ACADÊMICAS do DOXA.

Fonte : rendered/page__publicacoes-academicas.html  (DOM final, Elementor/Raven tabs)
Saída : extracted/publicacoes_academicas.yaml

A página organiza as publicações em 4 abas (raven-tabs):
    tab 1 -> "Livros Publicados"                 -> type: livro
    tab 2 -> "Artigos em Livro"                   -> type: capitulo
    tab 3 -> "Artigos em revista científica"      -> type: artigo
    tab 4 -> "Outras produções bibliográficas"    -> type: outros

Cada item é um <p>/<li> com uma citação livre (formato ABNT). Os campos
title/authors/year/publisher/journal/pages foram separados manualmente a partir
do TEXTO VISÍVEL de cada item (nada é inventado). Para garantir que a separação
continua fiel à fonte, o script:
  1. lê os itens reais de cada painel do DOM,
  2. confere que o `check` (trecho do título) de cada registro AINDA aparece no
     texto do item correspondente (assert), e
  3. só então grava o YAML.
Se o DOM mudar e um `check` deixar de bater, o script falha em vez de gravar
dados desatualizados.

Links de Lattes são capturados à parte, na chave `lattes` no topo do YAML.
URLs de publicação (eduerj/scielo/fundacion) vão no campo `url` do item.
"""
import os, re, sys
from bs4 import BeautifulSoup

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
SRC  = os.path.join(BASE, "rendered", "page__publicacoes-academicas.html")
OUT  = os.path.join(BASE, "extracted", "publicacoes_academicas.yaml")

TAB_TYPE = {"1": "livro", "2": "capitulo", "3": "artigo", "4": "outros"}
TAB_NAME = {
    "1": "Livros Publicados",
    "2": "Artigos em Livro",
    "3": "Artigos em revista científica",
    "4": "Outras produções bibliográficas",
}

# --------------------------------------------------------------------------- #
# 1) Ler os itens reais de cada aba (para validação e auditoria)
# --------------------------------------------------------------------------- #
def load_panels():
    soup = BeautifulSoup(open(SRC, encoding="utf-8").read(), "html.parser")
    panels = {}
    for c in soup.select(".raven-tabs-content"):
        dt = c.get("data-tab")
        if dt in panels:            # ignora duplicata desktop/mobile
            continue
        items = []
        for it in c.find_all(["p", "li"]):
            txt = re.sub(r"\s+", " ", it.get_text(" ", strip=True)).strip()
            if txt:
                items.append(txt)
        panels[dt] = items
    return panels

# --------------------------------------------------------------------------- #
# 2) Registros extraídos (title/authors/year/... a partir do texto visível)
#    `check` = trecho literal do título usado para casar com o item do DOM.
#    `dup`   = comentário opcional (redundância na própria página de origem).
# --------------------------------------------------------------------------- #
LATTES = [
    {"name": "Meireles, F.",       "url": "http://lattes.cnpq.br/9180210634743879"},
    {"name": "Guarnieri, F.",      "url": "http://lattes.cnpq.br/2912975115445421"},
    {"name": "Schaefer, B. M.",    "url": "http://lattes.cnpq.br/9571650216784483"},
    {"name": "Figueiredo, A. M. C.", "url": "http://lattes.cnpq.br/2261555898412006"},
]

PUBS = [
    # ---------------- TAB 1 — Livros ----------------
    dict(tab="1", check="Corrupção, Como e por quê seu dinheiro sai pelo ladrão",
         title="Corrupção, Como e por quê seu dinheiro sai pelo ladrão",
         authors="SALOMÃO, L. A.; GUARNIERI, Fernando",
         year=2016, publisher="1. ed. Niterói: Nitpress. v. 1. 200p", url=""),
    dict(tab="1", check="Política Local no Estado do Rio de Janeiro",
         title="Política Local no Estado do Rio de Janeiro – As eleições municipais de 2020",
         authors="Borba, Felipe; Figueiredo, Argelina (org)",
         year=2022, publisher="Editora da UERJ", url=""),
    # 2ª ocorrência de "Corrupção" (a página repete o mesmo livro; mantida por fidelidade à fonte)
    dict(tab="1", check="Corrupção, Como e por quê seu dinheiro sai pelo ladrão",
         title="Corrupção, Como e por quê seu dinheiro sai pelo ladrão",
         authors="SALOMÃO, L. A.; GUARNIERI, Fernando",
         year=2016, publisher="Niterói: Nitpress. v. 1. 200p", url="",
         dup="repetição do 1º item desta aba na página de origem"),
    dict(tab="1", check="25 anos de eleições presidenciais no Brasil",
         title="25 anos de eleições presidenciais no Brasil",
         authors="Figueiredo, Argelina; Borba, Felipe (org)",
         year=2018, publisher="Curitiba: Appris", url=""),
    dict(tab="1", check="homenagem a Marcus Figueiredo",
         title="Eleições, opinião pública e comunicação política no Brasil contemporâneo: homenagem a Marcus Figueiredo",
         authors="Borba, Felipe; Aldé, Alessandra (org)",
         year=2017, publisher="Eduerj",
         url="https://www.eduerj.com/eng/?product=eleicoes-opiniao-publica-e-comunicacao-politica-no-brasil-contemporaneo-homenagem-a-marcus-figueiredo-ebook&fbclid=IwAR25_qL-myIT26_tPjoS2pjoIchQcik-s2Z_WkO4p1WKqY1HHJ8mjNtYUrU"),

    # ---------------- TAB 2 — Artigos em Livro (capítulos) ----------------
    dict(tab="2", check="Magnitude eleitoral e representação de mulheres nos municípios brasileiros",
         title="Magnitude eleitoral e representação de mulheres nos municípios brasileiros",
         authors="MEIRELES, F.; ANDRADE, L.", year=2021,
         publisher="In: Luis Felipe Miguel. (Org.). Mulheres e representação política: 25 de estudos sobre cotas eleitorais no Brasil. 1ed. Porto Alegre: Zouk",
         pages="p. 505-534", url=""),
    dict(tab="2", check="O impacto da Covid-19 no comportamento eleitoral do fluminense nas eleições de 2020",
         title="O impacto da Covid-19 no comportamento eleitoral do fluminense nas eleições de 2020",
         authors="Guarnieri, Fernando; Figueiredo, Argelina", year=2022,
         publisher="In Felipe Borba e Argelina Figueiredo (org), As eleições municipais de 2020 no Estado do Rio de Janeiro, Editora da UERJ", url=""),
    dict(tab="2", check="Estudos Legislativos em Perspectiva Comparada",
         title="Estudos Legislativos em Perspectiva Comparada",
         authors="Figueiredo, Argelina; Freitas, Andréa; Medeiros, Danilo", year=2022,
         publisher="in Renato Perissinoto et al (org). Política Comparada, no prelo, Editora da UERJ", url=""),
    # sem ano na fonte ("no prelo") -> year deixado vazio (não inventar)
    dict(tab="2", check="Vulnerabilidades sociais, modelos de provisão de saúde",
         title="Vulnerabilidades sociais, modelos de provisão de saúde e suas relações com a mortalidade decorrente da pandemia de Covid-19 no Brasil e nos Estados Unidos",
         authors="Figueiredo, Argelina; Guichney, Hellen; Lazzari, Eduardo", year="",
         publisher="In Fernando Fontainha e Carlos Milani (org), COVID-19 e agendas de pesquisa nas ciências sociais. Editora da UERJ – no prelo", url=""),
    dict(tab="2", check="Determinantes Políticos e Institucionales del Éxito Legislativo del Ejecutivo em América Latina",
         title="Determinantes Políticos e Institucionales del Éxito Legislativo del Ejecutivo em América Latina",
         authors="Figueiredo, Argelina; Salles, Denise; Martins, Marcelo", year=2011,
         publisher="in Manuel Alcántara y Mercedes García Montero (Ed). Algo más que presidentes. El papel del Poder Legislativo en América Latina, Zaragora: Fundación Manuel Giménez Abad de Estudios Parlamentarios y del Estado Autonómico. Versão Digital (2020)",
         url="https://www.fundacionmgimenezabad.es/sites/default/files/Publicar/publicaciones/documentos/a1-actas1_algo_mas_que_presidentes_dig_0.pdf"),
    dict(tab="2", check="Os partidos nas eleições proporcionais no Estado do Rio",
         title="Os partidos nas eleições proporcionais no Estado do Rio",
         authors="Figueiredo, Argelina; Maciel, Natália", year=2019,
         publisher="In João Feres Jr e Carolina de Paula (Org) Eleições de 2018 e a Crise da Democracia Brasileira. Curitiba: Appris", url=""),
    dict(tab="2", check="A implosão da centro-direita e o voto em Bolsonaro",
         title="A implosão da centro-direita e o voto em Bolsonaro",
         authors="GUARNIERI, Fernando; ALBUQUERQUE, Felipe", year=2019,
         publisher="In João Feres Jr e Carolina de Paula (Org) Eleições de 2018 e a Crise da Democracia Brasileira. Curitiba: Appris", url=""),
    dict(tab="2", check="O voto do eleitor pobre nas eleições presidenciais",
         title="O voto do eleitor pobre nas eleições presidenciais (1989-2014)",
         authors="Figueiredo, Argelina; Maciel, Natália; Simoni Jr., Sérgio; Silva, Thiago M.", year=2018,
         publisher="In Figueiredo, Argelina; Borba, Felipe (Org). 25 anos de eleições presidenciais no Brasil. Curitiba: Appris",
         pages="pp. 75-94", url=""),
    dict(tab="2", check="Political Participation in Brazil",
         title="Political Participation in Brazil",
         authors="LIMONGI, Fernando; CHEIBUB, José. A.; FIGUEIREDO, Argelina", year=2018,
         publisher="In Marta Arretche (org) Paths of Inequality in Brazil: a Half Century of Changes. Switzerland. Springer",
         pages="p. 4-24", url=""),
    dict(tab="2", check="Estudos legislativos no Brasil",
         title="Estudos legislativos no Brasil",
         authors="Figueiredo Argelina; Santos, Fabiano", year=2016,
         publisher="In: Leonardo Avritzer; Carlos R. S. Milani; Maria do Socorro Braga. (Org.) A ciência política no Brasil. 1960-2015. Rio de Janeiro: Editora FGV; ABCP", url=""),
    dict(tab="2", check="Political Institutions and Governmental Performance in Brazilian Democracy",
         title="Political Institutions and Governmental Performance in Brazilian Democracy",
         authors="Figueiredo, Argelina; Limongi, Fernando", year=2015,
         publisher="In: Dana de la Fontaine e Thomas Stehnken (Eds.), The political System of Brazil, New York, Springer. ISBN 978-3-642-40022-3", url=""),
    dict(tab="2", check="Participação Política no Brasil",
         title="Participação Política no Brasil",
         authors="LIMONGI, Fernando; CHEIBUB, José. A.; FIGUEIREDO, Argelina", year=2015,
         publisher="In Marta Arretche (org.), São Paulo: Editora UNESP", url=""),

    # ---------------- TAB 3 — Artigos em revista científica ----------------
    dict(tab="3", check="Eleições municipais de 2016 e 2020 em São Paulo",
         title="Eleições municipais de 2016 e 2020 em São Paulo: resultados diferentes, alinhamentos iguais",
         authors="ZOLNERKEVIC, A.; Guarnieri, F.", year=2023,
         journal="OPINIÃO PÚBLICA", pages="v. 29, p. 133-165", url=""),
    dict(tab="3", check="O Governo Bolsonaro e a Conjuntura Política Pré-Eleitoral",
         title="O Governo Bolsonaro e a Conjuntura Política Pré-Eleitoral",
         authors="Guarnieri, F.; FIGUEIREDO, A.", year=2022,
         journal="CADERNOS ADENAUER (SÃO PAULO)", pages="v. 23, p. 9", url=""),
    dict(tab="3", check="A spatial interaction model of vote dispersion",
         title="A spatial interaction model of vote dispersion",
         authors="Guarnieri, F.; SILVA, G. P.", year=2022,
         journal="POLITICAL GEOGRAPHY", pages="v. 98, p. 102709", url=""),
    dict(tab="3", check="Democratic Principles and Performance: What do the Experts Think?",
         title="Democratic Principles and Performance: What do the Experts Think?",
         authors="RUSSO, G. A.; AVELINO, G.; Guarnieri, F.", year=2022,
         journal="Journal of Politics in Latin America (Print)", pages="v. 14, p. 224-236", url=""),
    dict(tab="3", check="Modelos de competição política e as eleições de 2022",
         title="Modelos de competição política e as eleições de 2022",
         authors="Guarnieri, F.; FIGUEIREDO, A.", year=2022,
         journal="CADERNOS ADENAUER (SÃO PAULO)", pages="v. 4, p. 9", url=""),
    dict(tab="3", check="Política Distributiva em Coalizão",
         title="Política Distributiva em Coalizão",
         authors="MEIRELES, F.", year=2024,
         journal="DADOS – REVISTA DE CIÊNCIAS SOCIAIS", pages="v. 67, p. 1", url=""),
    dict(tab="3", check="Multi-level legislative representation in an inchoate party system",
         title="Multi-level legislative representation in an inchoate party system: Mass-elite ideological congruence in Brazil",
         authors="CARROLL, ROYCE; MEIRELES, F.", year=2024,
         journal="Party Politics", pages="v. 30, p. 151-165", url=""),
    dict(tab="3", check="Pesquisas eleitorais no Brasil: tendências e desempenho",
         title="Pesquisas eleitorais no Brasil: tendências e desempenho",
         authors="MEIRELES, F.; RUSSO, G.", year=2022,
         journal="ESTUDOS AVANÇADOS (ONLINE)", pages="v. 36, p. 117-131", url=""),
    dict(tab="3", check="Deu Match? Uma introdução às técnicas de pareamento",
         title="Deu Match? Uma introdução às técnicas de pareamento",
         authors="SCHAEFER, B. M.; FIGUEIREDO FILHO, Dalson Britto", year=2023,
         journal="REVISTA BRASILEIRA DE CIÊNCIAS SOCIAIS (ONLINE)", pages="v. 38, p. 1-20", url=""),
    dict(tab="3", check="Plutocratas, personalistas ou inexperientes",
         title="Plutocratas, personalistas ou inexperientes: uma revisão sistemática sobre autofinanciamento eleitoral",
         authors="SCHAEFER, B. M.", year=2023,
         journal="AGENDA POLÍTICA", pages="v. 10, p. 94", url=""),
    # ↓ variantes redigidas em português (formato manual) — parcialmente redundantes com itens acima
    dict(tab="3", check="O governo Bolsonaro e a conjuntura eleitoral",
         title="O governo Bolsonaro e a conjuntura eleitoral",
         authors="Guarnieri, Fernando; Figueiredo, Argelina", year=2022,
         journal="Cadernos Adenauer", pages="v. XXIII, n. 2", url=""),
    dict(tab="3", check="Modelos de competição política e as eleições de 2022",
         title="Modelos de competição política e as eleições de 2022",
         authors="Guarnieri, Fernando; Figueiredo, Argelina", year=2022,
         journal="Cadernos Adenauer", pages="v. XXIII, n. 4", url="",
         dup="variante da citação de \"Modelos de competição política...\" (mesmo título, outro fascículo) já listada nesta aba"),
    dict(tab="3", check="A Crise Atual e o Debate Institucional",
         title="A Crise Atual e o Debate Institucional",
         authors="Limongi, Fernando; Figueiredo, Argelina", year=2017,
         journal="Novos Estudos Cebrap", pages="v. 36, n. 3",
         url="https://www.scielo.br/j/nec/a/KBxnHhZWWCPJ5zgJwKTTzSK/abstract/?lang=pt"),
    dict(tab="3", check="Entrevista a Fabio Kersche e João Feres Junior",
         title="Entrevista a Fabio Kersche e João Feres Junior",
         authors="Figueiredo, Argelina", year=2016,
         journal="ESCRITOS: Revista da Fundação Casa de Rui Barbosa", pages="v. 8, n. 8, pp. 233-252", url=""),

    # ---------------- TAB 4 — Outras produções bibliográficas ----------------
    dict(tab="4", check="Contracapa do livro Democracia e Eleições no Brasil",
         title="Contracapa do livro Democracia e Eleições no Brasil. Para onde vamos?",
         authors="Figueiredo, Argelina", year=2022,
         publisher="Magna Inácio & Vanessa Elias de Oliveira (orgs.), Hucitec/Anpocs. Contracapa", url=""),
    dict(tab="4", check="Prefácio do livro Por que eleições são importantes?",
         title="Prefácio do livro Por que eleições são importantes?",
         authors="Figueiredo, A. M. C.", year=2021,
         publisher="Przeworki, Adam. Rio de Janeiro: EdUERJ", url=""),
    dict(tab="4", check="O presidencialismo da Coalizão",
         title="Prefácio do livro O presidencialismo da Coalizão",
         authors="Limongi, Fernando; Figueiredo, Argelina", year=2016,
         publisher="Prefácio do livro de Andréa Marcondes de Freitas. Rio de Janeiro, Fundação Konrad Adenauer", url=""),
]

# --------------------------------------------------------------------------- #
# 3) Validação: cada `check` precisa aparecer no texto real do painel
# --------------------------------------------------------------------------- #
def norm(s):
    return re.sub(r"\s+", " ", s).replace("’", "'").strip().lower()

def validate(panels):
    problems = []
    for p in PUBS:
        blob = norm(" ".join(panels.get(p["tab"], [])))
        if norm(p["check"]) not in blob:
            problems.append((p["tab"], p["check"]))
    if problems:
        for tab, chk in problems:
            sys.stderr.write(f"[ERRO] check ausente no DOM (aba {tab}): {chk!r}\n")
        raise SystemExit("Validação falhou: registros não batem com o DOM.")
    # cobertura: nº de itens no DOM vs registros
    for tab in TAB_TYPE:
        n_dom = len(panels.get(tab, []))
        n_rec = sum(1 for p in PUBS if p["tab"] == tab)
        print(f"aba {tab} ({TAB_NAME[tab]}): DOM={n_dom} itens, registros={n_rec}")

# --------------------------------------------------------------------------- #
# 4) Emissão do YAML (aspas duplas, unicode preservado)
# --------------------------------------------------------------------------- #
def dq(s):
    return '"' + str(s).replace("\\", "\\\\").replace('"', '\\"') + '"'

FIELD_ORDER = ["title", "authors", "year", "type", "publisher", "journal", "pages", "url"]

def emit():
    panels = load_panels()
    validate(panels)
    lines = []
    lines.append("# Publicações Acadêmicas do DOXA")
    lines.append("# Extraído de: rendered/page__publicacoes-academicas.html (Elementor/Raven tabs)")
    lines.append("# Campos: title, authors, year, type, publisher (livros/capítulos/outros),")
    lines.append("#         journal (artigos), pages (opcional), url (opcional)")
    lines.append("# type: livro | capitulo | artigo | outros")
    lines.append("")
    lines.append("# Links de Lattes encontrados na página (4 pesquisadores; 6 ocorrências em links.json / 9 no DOM renderizado)")
    lines.append("lattes:")
    for l in LATTES:
        lines.append(f"  - name: {dq(l['name'])}")
        lines.append(f"    url: {dq(l['url'])}")
    lines.append("")
    lines.append("publications:")
    cur_tab = None
    for p in PUBS:
        if p["tab"] != cur_tab:
            cur_tab = p["tab"]
            lines.append("")
            lines.append(f"  # ---- {TAB_NAME[cur_tab]} (type: {TAB_TYPE[cur_tab]}) ----")
        rec = dict(p)
        rec["type"] = TAB_TYPE[rec["tab"]]
        if rec.get("dup"):
            lines.append(f"  # nota: {rec['dup']}")
        first = True
        for f in FIELD_ORDER:
            if f == "pages" and not rec.get("pages"):
                continue
            if f == "publisher" and rec["type"] == "artigo":
                continue
            if f == "journal" and rec["type"] != "artigo":
                continue
            val = rec.get(f, "")
            if f == "year":
                out = str(val) if isinstance(val, int) else dq(val)
            else:
                out = dq(val if val is not None else "")
            prefix = "  - " if first else "    "
            lines.append(f"{prefix}{f}: {out}")
            first = False
    text = "\n".join(lines) + "\n"
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(text)
    print(f"\nEscrito: {OUT}  ({len(PUBS)} publicações)")

if __name__ == "__main__":
    emit()
