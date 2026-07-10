#!/usr/bin/env python3
"""Parse eventos + seminários.

eventos:    authoritative from the WP REST API (posts in category 136 = 'Evento'),
            enriched with the featured image resolved through media.json.
seminarios: parsed from the rendered /seminarios/ page, which groups <li> entries
            under year <h2> headings.
"""
import html as H
import json, os, re, sys
from bs4 import BeautifulSoup

S = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVENT_CAT = 136

MONTHS = {"janeiro": 1, "fevereiro": 2, "março": 3, "abril": 4, "maio": 5, "junho": 6,
          "julho": 7, "agosto": 8, "setembro": 9, "outubro": 10, "novembro": 11, "dezembro": 12}


def clean(s):
    return re.sub(r"\s+", " ", H.unescape(s).replace("\xa0", " ")).strip()


def strip_tags(s):
    return clean(BeautifulSoup(s, "html.parser").get_text(" ", strip=True))


DATA_HOSTS = ("drive.google.com", "docs.google.com")


def attachments_for(slug):
    """Event posts carry downloadable material (the free digital edition of 'A Decisão do
    Voto' is a Google Doc; others are PDFs). These links live only in the post's DOM."""
    import glob
    hits = glob.glob(f"{S}/rendered/post__{slug[:55]}*.html")
    if not hits:
        return []
    soup = BeautifulSoup(open(hits[0], encoding="utf-8").read(), "html.parser")
    out = []
    for a in soup.select("a[href]"):
        h = a["href"]
        if h.lower().endswith(".pdf") or any(d in h for d in DATA_HOSTS):
            if h not in out:
                out.append(h)
    return out


def eventos():
    posts = json.load(open(f"{S}/raw/posts.json"))
    media = {m["id"]: m["source_url"] for m in json.load(open(f"{S}/raw/media.json"))}
    out = []
    for p in posts:
        if EVENT_CAT not in p.get("categories", []):
            continue
        desc = strip_tags(p.get("excerpt", {}).get("rendered", ""))
        desc = re.sub(r"\s*\[…\]$|\s*\[\.\.\.\]$", "", desc)
        out.append({
            "title": clean(p["title"]["rendered"]),
            "date": p["date"][:10],
            "description": desc,
            "image": media.get(p.get("featured_media"), ""),
            "url": p["link"],
            "attachments": attachments_for(p["slug"]),
        })
    out.sort(key=lambda e: e["date"], reverse=True)
    return out


def parse_seminar(txt, year):
    """'Fernando Meireles (IESP-UERJ) – "Título". [25 de setembro]'"""
    txt = clean(txt)
    m = re.search(r"[“\"](.+?)[”“\"]", txt)
    title = clean(m.group(1)) if m else ""
    head = txt[:m.start()] if m else txt

    inst = ""
    mi = re.search(r"\(([^)]*)\)", head)
    if mi:
        inst = clean(mi.group(1))
        head = head[:mi.start()] + head[mi.end():]
    presenter = clean(re.sub(r"[–\-—:]+\s*$", "", head)).strip(" .,–-")

    date = ""
    md = re.search(r"\[(\d{1,2})\s+de\s+([a-zç]+)", txt, re.I)
    if md:
        mon = MONTHS.get(md.group(2).lower())
        if mon:
            date = f"{year}-{mon:02d}-{int(md.group(1)):02d}"
    if not title:  # title outside quotes: take everything after the dash
        parts = re.split(r"\s[–—-]\s", txt, maxsplit=1)
        title = clean(parts[1]) if len(parts) > 1 else txt
    title = re.sub(r"\s*\[.*?\]\s*$", "", title).strip(" .,")
    return {"title": title, "presenter": presenter, "institution": inst,
            "date": date, "year": int(year)}


def seminarios():
    soup = BeautifulSoup(open(f"{S}/rendered/page__seminarios.html", encoding="utf-8").read(), "html.parser")
    for t in soup(["script", "style", "noscript"]):
        t.decompose()
    out, cur = [], None
    for e in soup.find_all(["h2", "li"]):
        txt = clean(e.get_text(" ", strip=True))
        if e.name == "h2":
            if txt.isdigit():
                cur = txt
            continue
        if cur and txt and e.name == "li":
            out.append(parse_seminar(txt, cur))
    # Same talk can be given twice in a year (e.g. Izumi/Medeiros, jun + out 2021),
    # so the date must be part of the identity — dedup only removes exact repeats.
    seen, uniq = set(), []
    for s in out:
        k = (s["title"][:60], s["year"], s["date"], s["presenter"][:40])
        if k not in seen:
            seen.add(k)
            uniq.append(s)
    uniq.sort(key=lambda s: (-s["year"], s["date"]))
    return uniq


def q(s):
    return '"' + str(s).replace("\\", "\\\\").replace('"', '\\"') + '"'


def main():
    ev, sem = eventos(), seminarios()
    lines = [
        "# Eventos e Seminários do DOXA",
        "# eventos:    WP REST API, posts na categoria 'Evento' (term 136) + imagem destacada",
        "# seminarios: DOM renderizado de https://www.lab-doxa.org.br/seminarios/",
        "# Extraído em 2026-07-09",
        "",
        "eventos:",
    ]
    for e in ev:
        lines.append(f"  - title: {q(e['title'])}")
        for k in ("date", "description", "image", "url"):
            lines.append(f"    {k}: {q(e[k])}")
        if e["attachments"]:
            lines.append("    attachments:")
            lines.extend(f"      - {q(a)}" for a in e["attachments"])
        lines.append("")
    lines.append("seminarios:")
    for s in sem:
        lines.append(f"  - title: {q(s['title'])}")
        for k in ("presenter", "institution", "date"):
            lines.append(f"    {k}: {q(s[k])}")
        lines.append(f"    year: {s['year']}")
        lines.append("")
    open(f"{S}/extracted/eventos_seminarios.yaml", "w", encoding="utf-8").write("\n".join(lines))

    print(f"eventos: {len(ev)}")
    for e in ev:
        print(f"   {e['date']}  {e['title'][:58]:<58s} img={'y' if e['image'] else 'n'}")
    print(f"\nseminarios: {len(sem)}")
    from collections import Counter
    print("  by year:", dict(sorted(Counter(s['year'] for s in sem).items(), reverse=True)))
    print("  missing title:", sum(1 for s in sem if not s['title']))
    print("  missing presenter:", sum(1 for s in sem if not s['presenter']))
    print("  with date:", sum(1 for s in sem if s['date']))
    for s in sem[:3]:
        print("  ", s)


if __name__ == "__main__":
    main()
