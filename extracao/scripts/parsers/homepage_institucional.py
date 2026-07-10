#!/usr/bin/env python3
"""Extract the homepage + institucional page from the rendered DOM.

Recovers the three values the Hugo repo still carries as placeholders:
  * featured_video.youtube_id  (jet-video widget, data-lazy-load attribute)
  * dashboards[].url           (the real Power BI ?view=r=... embed URL)
  * the institutional prose
"""
import html as H
import json, os, re, sys
from bs4 import BeautifulSoup

S = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def clean(s):
    return re.sub(r"\s+", " ", H.unescape(s).replace("\xa0", " ")).strip()


def soup_of(name):
    s = BeautifulSoup(open(f"{S}/rendered/{name}", encoding="utf-8").read(), "html.parser")
    for t in s(["script", "style", "noscript"]):
        t.decompose()
    return s


def homepage():
    raw = open(f"{S}/rendered/page__inicio.html", encoding="utf-8").read()
    s = soup_of("page__inicio.html")

    # 1. featured video: the jet-video widget lazy-loads the real embed URL
    fv = re.search(r'data-lazy-load="https://www\.youtube\.com/embed/([A-Za-z0-9_-]+)', raw)
    featured_id = fv.group(1) if fv else ""

    # 2. every youtube reference on the page, with its card label
    videos = []
    if featured_id:
        videos.append({"youtube_id": featured_id,
                       "title": "Melhores momentos do horário eleitoral",
                       "kind": "embed"})
    for a in s.select('a[href*="youtu"]'):
        href = a["href"]
        if "channel" in href:
            continue
        m = re.search(r"(?:youtu\.be/|v=)([A-Za-z0-9_-]{6,})", href)
        if not m:
            continue
        label = card_label(a.find_parent(class_="elementor-widget-container"))
        if not any(v["youtube_id"] == m.group(1) for v in videos):
            videos.append({"youtube_id": m.group(1), "title": label or "", "kind": "link", "url": href})

    # 3. dashboards: collect DISTINCT power bi urls with their card labels
    dash = {}
    for a in s.select('a[href*="powerbi"]'):
        label = card_label(a.find_parent(class_="elementor-widget-container"))
        if label:
            dash.setdefault(a["href"], []).append(label)

    # 4. Vota Aí block
    votaai_url = ""
    for a in s.select('a[href*="votaai"]'):
        votaai_url = a["href"]
        break
    strings = [clean(x) for x in s.stripped_strings]
    votaai_title, votaai_desc = "", []
    for i, x in enumerate(strings):
        if x.startswith("Vota aí"):
            votaai_title = x
            for y in strings[i + 1:i + 5]:
                if len(y) > 60:
                    votaai_desc.append(y)
            break
    return featured_id, videos, dash, votaai_title, " ".join(votaai_desc), votaai_url


def institucional_md():
    """Read whole <p> blocks: inline <strong>/<a> would otherwise split a sentence
    into several 'strings' and the names (Marcus Figueiredo…) would be lost."""
    s = soup_of("page__institucional.html")
    body, seen = [], set()
    for p in s.find_all("p"):
        if p.find_parent(["nav", "header", "footer"]):
            continue
        t = clean(p.get_text(" ", strip=True))
        t = re.sub(r"\s+([,.])", r"\1", t)  # 'Figueiredo ,' -> 'Figueiredo,'
        if len(t) < 60 or t in seen:
            continue
        if t.startswith("Instituto de Estudos Sociais e Políticos"):  # footer
            continue
        seen.add(t)
        body.append(t)
    md = ["# Sobre o DOXA", "",
          "<!-- Fonte: https://www.lab-doxa.org.br/institucional/ (DOM renderizado, 2026-07-09) -->",
          ""]
    md += [p + "\n" for p in body]
    open(f"{S}/extracted/institucional.md", "w", encoding="utf-8").write("\n".join(md))
    return len(body)


def q(s):
    return '"' + str(s).replace("\\", "\\\\").replace('"', '\\"') + '"'


def card_label(box):
    """Elementor image-box cards render <h?>title</h?> + <p>subtitle</p>; we want the title."""
    if not box:
        return ""
    h = box.find(["h1", "h2", "h3", "h4", "h5", "h6"])
    return clean(h.get_text(" ", strip=True)) if h else clean(box.get_text(" ", strip=True))


def main():
    fid, videos, dash, vt, vd, vurl = homepage()
    nparas = institucional_md()

    L = [
        "# Homepage + Institucional — dados reais extraídos do WordPress",
        "# Fonte: DOM renderizado de /inicio/ e /institucional/ (2026-07-09)",
        "# Substitui os placeholders de data/homepage.yaml:",
        "#   featured_video.youtube_id: 'SUBSTITUA_PELO_ID_DO_VIDEO'  -> valor real abaixo",
        "#   dashboards[].url: 'https://app.powerbi.com/' (nu)        -> URL de embed real abaixo",
        "",
        "votaai:",
        f"  title: {q(vt)}",
        f"  description: {q(vd)}",
        f"  url: {q(vurl)}",
        "",
        "featured_video:",
        f"  title: {q('Melhores momentos do horário eleitoral')}",
        f"  youtube_id: {q(fid)}",
        "",
        "videos:",
    ]
    for v in videos:
        L.append(f"  - youtube_id: {q(v['youtube_id'])}")
        L.append(f"    title: {q(v['title'])}")
        L.append(f"    kind: {q(v['kind'])}")
        if v.get("url"):
            L.append(f"    url: {q(v['url'])}")
        L.append("")
    L += ["dashboards:",
          '  title: "Eleições Rio e São Paulo 2024"',
          "  items:"]
    for url, labels in dash.items():
        primary = next((l for l in labels if "Eleições" in l), labels[0])
        L.append(f"    - label: {q(primary)}")
        L.append(f"      url: {q(url)}")
        if len(set(labels)) > 1:
            others = sorted(set(labels) - {primary})
            L.append(f"      # ATENÇÃO: a mesma URL também é usada pelo card {others!r} na home")
            L.append("      # do site original — muito provavelmente um link errado na fonte.")
    L.append("")
    open(f"{S}/extracted/homepage_institucional.yaml", "w", encoding="utf-8").write("\n".join(L))

    print("featured youtube_id:", fid)
    print("videos:", len(videos))
    for v in videos:
        print("   ", v["youtube_id"], "|", v["title"][:55])
    print("distinct powerbi urls:", len(dash))
    for u, l in dash.items():
        print("   labels:", sorted(set(l)))
        print("   url:", u[:100] + "...")
    print("votaai:", repr(vt), "|", vurl)
    print("votaai desc chars:", len(vd))
    print("institucional.md paragraphs:", nparas)


if __name__ == "__main__":
    main()
