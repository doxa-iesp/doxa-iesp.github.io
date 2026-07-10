#!/usr/bin/env python3
"""Parse the 'Na Mídia' page into structured records.

Sections: Mídia Impressa / Mídia Virtual (citation paragraphs with links)
          Mídia Audiovisual (H2 'Ano: YYYY' + H2 title + credit paragraphs)
"""
import os, re, sys
from bs4 import BeautifulSoup

S = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = f"{S}/rendered/page__na-midia.html"
SECTIONS = {"Mídia Impressa": "impressa", "Mídia Virtual": "virtual", "Mídia Audiovisual": "audiovisual"}
FOOTER = "Instituto de Estudos Sociais e Políticos"

MONTHS = {"jan": 1, "fev": 2, "mar": 3, "abr": 4, "mai": 5, "jun": 6,
          "jul": 7, "ago": 8, "set": 9, "out": 10, "nov": 11, "dez": 12}
Q = "“”\"'‘’"


def clean(s):
    return re.sub(r"\s+", " ", s.replace("\xa0", " ")).strip()


def parse_date(tail):
    """'Valor Econômico, São Paulo, 24 abr. 2022.' -> (outlet, 2022-04-24)"""
    t = clean(tail)
    m = re.search(r"(\d{1,2})\s+de\s+([a-zç]+)\w*\.?\s+de\s+(\d{4})", t, re.I)
    if not m:
        m = re.search(r"(\d{1,2})\s+([a-zç]{3})\w*\.?\s*,?\s*(\d{4})", t, re.I)
    day = mon = year = None
    if m:
        day, mon_s, year = int(m.group(1)), m.group(2)[:3].lower(), int(m.group(3))
        mon = MONTHS.get(mon_s)
    if not year:
        y = re.search(r"\b(19|20)\d{2}\b", t)
        year = int(y.group(0)) if y else None
    date = ""
    if year and mon and day:
        date = f"{year:04d}-{mon:02d}-{day:02d}"
    elif year:
        date = str(year)
    t = re.sub(r"^[\s.,;:”“\"']+", "", t)          # drop the punctuation that closed the title
    t = re.sub(r"^(In:|Em:)\s*", "", t).strip()
    # Split on commas only: periods appear inside outlet names ("O Estado de S. Paulo").
    outlet = t.split(",")[0].strip()
    outlet = re.sub(r"\s*\d{1,2}\s+(de\s+)?[a-zç]{3}.*$", "", outlet, flags=re.I).strip(" .")
    return outlet, date


def parse_citation(p):
    """'Meireles, Fernando. “Title”. Valor Econômico, São Paulo, 24 abr. 2022.'"""
    txt = clean(p.get_text(" ", strip=True))

    # Uma citação tem um <a> por aspa tipográfica que virou link por acidente no WordPress
    # (ex.: um <a> cujo texto é só "’"). Descartamos essas âncoras degeneradas.
    anchors = [a for a in p.select("a[href]")
               if len(clean(a.get_text(" ", strip=True))) >= 5]
    links = [a["href"] for a in anchors]

    # O texto-âncora É o título do artigo nesta página. Usá-lo evita dois problemas das aspas:
    # títulos com aspas ANINHADAS (El País: ...fala "e daí") e citações que fecham o título
    # com uma aspa esquerda (“) em vez de direita (”).
    titles = [clean(a.get_text(" ", strip=True)) for a in anchors]
    if not titles:  # item sem link (existem 2): cai para o texto entre aspas
        titles = re.findall(r"[“”\"]\s*(.+?)\s*[”“\"]", txt)
    authors = clean(re.split(r"[“”\"]", txt)[0]).strip(" .,;:")
    authors = re.sub(r"\s*Entrevista:?$", "", authors).strip(" .,;:")
    last_q = max((txt.rfind(c) for c in "”“\""), default=-1)
    tail = txt[last_q + 1:] if last_q >= 0 else ""
    outlet, date = parse_date(tail)

    out = []
    for i, t in enumerate(titles):
        out.append({
            "title": clean(t),
            "authors": authors,
            "outlet": outlet,
            "date": date,
            "url": links[i] if i < len(links) else (links[0] if links else ""),
        })
    return out


def main():
    soup = BeautifulSoup(open(SRC, encoding="utf-8").read(), "html.parser")
    for t in soup(["script", "style", "noscript"]):
        t.decompose()

    records, cur = [], None
    av_year = av_title = None
    av_credits = []

    def flush_av():
        if av_title:
            records.append({
                "title": av_title, "authors": clean(" | ".join(av_credits[:1])),
                "outlet": clean(" | ".join(av_credits[1:])) or "",
                "date": av_year or "", "type": "audiovisual", "url": "",
            })

    for e in soup.find_all(["h1", "h2", "h3", "h4", "h5", "p", "li"]):
        txt = clean(e.get_text(" ", strip=True))
        if not txt:
            continue
        if txt.startswith(FOOTER):
            break
        if txt in SECTIONS:
            if cur == "audiovisual":
                flush_av()
                av_title = None
            cur = SECTIONS[txt]
            continue
        if cur is None:
            continue

        if cur == "audiovisual":
            if e.name.startswith("h"):
                m = re.match(r"Ano:\s*(\d{4})", txt)
                if m:
                    flush_av()
                    av_title, av_credits = None, []
                    av_year = m.group(1)
                else:
                    av_title = txt
            elif e.name in ("p", "li"):
                av_credits.append(txt)
        else:
            if e.name == "p" and e.find_parent("li"):
                continue
            if e.name not in ("p", "li"):
                continue
            # NÃO exigir link: 2 itens da mídia impressa são citações sem URL
            # ("A polarização do vírus", "Desconstruindo Mitos"). Exigir <a> os apagava.
            if not e.select("a[href]") and not re.search(r"[“\"].+[”“\"]", txt):
                continue
            for r in parse_citation(e):
                r["type"] = cur
                records.append(r)

    if cur == "audiovisual":
        flush_av()

    def q(s):
        return '"' + str(s).replace("\\", "\\\\").replace('"', '\\"') + '"'

    lines = [
        "# Na Mídia — cobertura e aparições do DOXA",
        "# Fonte: DOM renderizado de https://www.lab-doxa.org.br/na-midia/ (extraído em 2026-07-09)",
        "# Campos: title, authors, outlet, date, type (impressa|virtual|audiovisual), url",
        "",
    ]
    for r in records:
        lines.append(f"- title: {q(r['title'])}")
        for k in ("authors", "outlet", "date", "type", "url"):
            lines.append(f"  {k}: {q(r[k])}")
        lines.append("")
    open(f"{S}/extracted/na_midia.yaml", "w", encoding="utf-8").write("\n".join(lines))

    from collections import Counter
    print("records:", len(records), dict(Counter(r["type"] for r in records)))
    print("with url:", sum(1 for r in records if r["url"]))
    print("with date:", sum(1 for r in records if r["date"]))
    for r in records[:3]:
        print("  ", r)


if __name__ == "__main__":
    main()
