#!/usr/bin/env python3
"""Definitive acervo parser.

Drive URL + thumbnail + broadcast date come from the rendered DOM (rendered/acervo_pages/*.html);
codigo/slug/permalink and every taxonomy come from the WP REST API (authoritative).
"""
import glob, html, json, os, re, sys
from bs4 import BeautifulSoup

S = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAX = json.load(open(f"{S}/raw/_taxonomy_map.json"))
POSTS = {p["id"]: p for p in json.load(open(f"{S}/raw/acervo-doxa.json"))}

DATE_RE = re.compile(r"^\d{2}/\d{2}/\d{4}$")


def terms(post, taxonomy):
    return [TAX[taxonomy][str(i)] if str(i) in TAX[taxonomy] else TAX[taxonomy].get(i, str(i))
            for i in post.get(taxonomy, [])]


def dom_fields():
    """post_id -> {url, thumb, data}"""
    out = {}
    for f in sorted(glob.glob(f"{S}/rendered/acervo_pages/page-*.html")):
        soup = BeautifulSoup(open(f, encoding="utf-8").read(), "html.parser")
        for it in soup.select(".jet-listing-grid__item"):
            pid = it.get("data-post-id")
            if not pid:
                continue
            pid = int(pid)
            a = it.select_one('a[href*="drive.google.com"]')
            img = it.select_one("img")
            data = ""
            for d in it.select(".jet-listing-dynamic-field"):
                t = d.get_text(" ", strip=True)
                if DATE_RE.match(t):
                    data = t
                    break
            rec = {
                "url": a["href"] if a else "",
                "thumb": (img.get("src") or img.get("data-src") or "") if img else "",
                "data": data,
            }
            # first capture wins, but prefer one that has a drive url
            if pid not in out or (not out[pid]["url"] and rec["url"]):
                out[pid] = rec
    return out


def main():
    dom = dom_fields()
    items = []
    for pid, p in POSTS.items():
        d = dom.get(pid, {"url": "", "thumb": "", "data": ""})
        ano = terms(p, "ano")
        items.append({
            "codigo": html.unescape(p["title"]["rendered"]),
            "slug": p["slug"],
            "wp_id": pid,
            "data": d["data"],
            "year": int(ano[0]) if ano and ano[0].isdigit() else "",
            "tipo_video": (terms(p, "tipo-de-video") or [""])[0],
            "cargo": terms(p, "cargo-eletivo"),
            "region": (terms(p, "regiao") or [""])[0],
            "estado": (terms(p, "estado") or [""])[0],
            "candidatos_presidente": terms(p, "candidatos-presidente"),
            "candidatos_governador": terms(p, "candidatos-governador"),
            "partidos": terms(p, "partidos"),
            "url": d["url"],
            "thumb": d["thumb"],
            "permalink": p["link"],
        })
    items.sort(key=lambda x: (x["year"] or 0, x["codigo"]))

    def q(s):
        return '"' + str(s).replace('\\', '\\\\').replace('"', '\\"') + '"'

    lines = [
        "# Acervo Audiovisual do DOXA — itens publicados no site WordPress",
        "# Fonte: WP REST API (/wp/v2/acervo-doxa) + DOM renderizado de /acervo/ (10 páginas)",
        "# Extraído em 2026-07-09. Campos de taxonomia vêm da API; url/thumb/data vêm do DOM.",
        "",
    ]
    for i in items:
        lines.append(f"- codigo: {q(i['codigo'])}")
        lines.append(f"  slug: {q(i['slug'])}")
        lines.append(f"  wp_id: {i['wp_id']}")
        for k in ("data", "year", "tipo_video", "region", "estado"):
            v = i[k]
            lines.append(f"  {k}: {v if isinstance(v, int) else q(v)}")
        for k in ("cargo", "candidatos_presidente", "candidatos_governador", "partidos"):
            if i[k]:
                lines.append(f"  {k}:")
                lines.extend(f"    - {q(v)}" for v in i[k])
            else:
                lines.append(f"  {k}: []")
        lines.append(f"  url: {q(i['url'])}")
        lines.append(f"  thumb: {q(i['thumb'])}")
        lines.append(f"  permalink: {q(i['permalink'])}")
        lines.append("")

    with open(f"{S}/extracted/acervo.yaml", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    no_url = [i["codigo"] for i in items if not i["url"]]
    print(f"items: {len(items)}")
    print(f"with drive url: {sum(1 for i in items if i['url'])}")
    print(f"without drive url: {len(no_url)} {no_url}")
    print(f"distinct drive urls: {len({i['url'] for i in items if i['url']})}")


if __name__ == "__main__":
    main()
