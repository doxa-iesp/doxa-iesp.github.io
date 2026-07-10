#!/usr/bin/env python3
"""Extract the editorial prose of each section page.

The listing ITEMS are already structured in the other YAML/CSV files, so we only want the
page's own text: intro paragraphs, section headings and their descriptions.
Anything inside a JetEngine listing grid is skipped, plus a per-page stop marker for the
pages whose items are plain <p> (na-midia) or year headings (seminarios).
"""
import html as H
import os, re

S = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = f"{S}/extracted/paginas"
os.makedirs(OUT, exist_ok=True)

FOOTER = "Instituto de Estudos Sociais e Políticos"

PAGES = {
    # Pages whose ITEMS are already structured elsewhere are excluded or cut short:
    # /publicacoes-academicas/ and /analises-de-conjuntura-eleitoral/ are pure listings,
    # their prose lives on /publicacoes/.
    "inicio":            dict(title="Início",                     stop=None),
    "institucional":     dict(title="Institucional",              stop="Nossa Equipe"),
    "acervo":            dict(title="Acervo Audiovisual",         stop=None),
    "mapas-de-votacao":  dict(title="Mapas de Votação",           stop=None),
    "bancos-de-dados":   dict(title="Bancos de Dados",            stop=None),
    "pagina-pesquisas":  dict(title="Pesquisas do DOXA",          stop=None),
    "publicacoes":       dict(title="Publicações",                stop=None),
    "na-midia":          dict(title="Na Mídia",                   stop="Mídia Impressa"),
    "seminarios":        dict(title="Seminários",                 stop="__YEAR__"),
    "eventos":           dict(title="Eventos",                    stop=None),
    "pesquisa-covid":    dict(title="Pesquisa COVID",             stop=None),
    "textos-para-discussao-2":          dict(title="Textos para Discussão", stop=None),
}


def clean(s):
    s = re.sub(r"\s+", " ", H.unescape(s).replace("\xa0", " ")).strip()
    return re.sub(r"\s+([,.;:])", r"\1", s)


def in_listing(el):
    for p in el.parents:
        cls = p.get("class") or []
        if any("jet-listing-grid" in c for c in cls):
            return True
    return False


def main():
    from bs4 import BeautifulSoup
    index = []
    for slug, cfg in PAGES.items():
        path = f"{S}/rendered/page__{slug}.html"
        if not os.path.exists(path):
            print(f"  !! sem DOM: {slug}")
            continue
        soup = BeautifulSoup(open(path, encoding="utf-8").read(), "html.parser")
        for t in soup(["script", "style", "noscript"]):
            t.decompose()
        for sel in ("nav", "header", "footer"):
            for t in soup.select(sel):
                t.decompose()

        blocks, seen, stopped = [], set(), False
        for el in soup.find_all(["h1", "h2", "h3", "p", "li"]):
            if stopped or in_listing(el):
                continue
            txt = clean(el.get_text(" ", strip=True))
            if not txt or txt.startswith(FOOTER) or txt == "Skip to content":
                continue

            if el.name in ("h1", "h2", "h3"):
                stop = cfg["stop"]
                if stop == "__YEAR__" and txt.isdigit():
                    stopped = True
                    continue
                if stop and stop != "__YEAR__" and txt == stop:
                    stopped = True
                    continue
                if txt in seen:
                    continue
                seen.add(txt)
                blocks.append(("h", txt))
            else:
                if len(txt) < 60 or txt in seen:
                    continue
                seen.add(txt)
                blocks.append(("p", txt))

        if not blocks:
            print(f"  {slug:<34s} 0 blocos (página sem prosa)")
            continue

        md = [f"---", f'titulo: "{cfg["title"]}"',
              f'fonte: "https://www.lab-doxa.org.br/{slug}/"',
              f'extraido_em: "2026-07-09"', "---", ""]
        for kind, txt in blocks:
            md.append(f"## {txt}" if kind == "h" else txt)
            md.append("")
        open(f"{OUT}/{slug}.md", "w", encoding="utf-8").write("\n".join(md))
        nh = sum(1 for k, _ in blocks if k == "h")
        np_ = sum(1 for k, _ in blocks if k == "p")
        chars = sum(len(t) for _, t in blocks)
        index.append((slug, nh, np_, chars))
        print(f"  {slug:<34s} {nh:2d} títulos {np_:3d} parágrafos {chars:6d} chars")

    print(f"\n{len(index)} páginas -> {OUT}/")


if __name__ == "__main__":
    main()
