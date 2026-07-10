#!/usr/bin/env python3
"""Render every lab-doxa page with JS, fully expanding JetEngine listings.

Saves, per target:
  rendered/<key>.html   final DOM (all pages/tabs of a listing merged into one file)
  rendered/<key>.links.json   every <a href> with its anchor text
"""
import json, os, re, sys, time
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

S = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(S, "rendered")
os.makedirs(OUT, exist_ok=True)
BASE = "https://www.lab-doxa.org.br"

PAGES = [
    "inicio", "nova-pagina-inicial", "institucional", "acervo", "publicacoes",
    "na-midia", "pagina-pesquisas", "pesquisas-realizadas", "teses-e-dissertacoes",
    "bancos-de-dados", "mapas-de-votacao", "seminarios", "pesquisa-covid",
    "analise", "eventos", "publicacoes-academicas",
    "analises-de-conjuntura-eleitoral", "textos-para-discussao-2",
]
POSTS = [
    "textos-para-discussao",
    "novo-texto-para-discussao-as-politicas-de-controle-de-armas-de-fogo-e-municoes-no-brasil",
    "edicao-digital-gratuita-do-livro-a-decisao-do-voto-de-marcus-figueiredo",
    "programas-eleitorais-dos-candidatos-a-prefeito-das-capitais",
    "programas-eleitorais-dos-candidatos-a-prefeito-do-estado-do-rio-de-janeiro",
    "seminario-comemora-25-anos-do-doxa",
    "coordenadora-do-doxa-recebe-premio-de-excelencia-academica-da-abcp",
    "covid-no-estado-do-rio-monitoramento-e-efeitos",
    "doxa-20-anos-o-legado-de-marcus-figueiredo",
    "seminario-marcus-figueiredo-eleicoes-opiniao-publica-e-comunicacao-politica",
    "nota-editorial-sobre-falecimento-de-marcus-figueiredo-na-revista-dados",
]

ITEM = ".jet-listing-grid__item"


def harvest_links(pg):
    return pg.eval_on_selector_all(
        "a[href]",
        "els=>els.map(e=>({href:e.href, text:(e.innerText||'').trim().slice(0,200)}))",
    )


def click_all_tabs(pg):
    """Reveal content hidden behind tab widgets."""
    for sel in (".elementor-tab-title", ".e-n-tab-title", ".jet-tabs__control"):
        n = pg.locator(sel).count()
        for i in range(n):
            try:
                pg.locator(sel).nth(i).click(timeout=4000)
                pg.wait_for_timeout(1200)
            except Exception:
                pass


def exhaust_scroll(pg, rounds=60):
    """Trigger JetEngine scroll/load-more until the item count stops growing."""
    stable, last = 0, -1
    for _ in range(rounds):
        n = pg.locator(ITEM).count()
        if n == last:
            stable += 1
            if stable >= 3:
                break
        else:
            stable, last = 0, n
        # walk down the page so every grid's #load-more sentinel enters the viewport
        pg.mouse.wheel(0, 4000)
        pg.wait_for_timeout(500)
        pg.keyboard.press("End")
        pg.wait_for_timeout(900)
        for i in range(pg.locator("#load-more").count()):
            try:
                el = pg.locator("#load-more").nth(i)
                if el.is_visible():
                    el.click(timeout=2500)
                    pg.wait_for_timeout(1200)
            except Exception:
                pass
    return pg.locator(ITEM).count()


def exhaust_pagination(pg):
    """Click through jet-filters pagination, snapshotting DOM + links per page."""
    doms, links = [], []
    vals = pg.eval_on_selector_all(
        ".jet-filters-pagination__item",
        "els=>els.map(e=>e.dataset.value).filter(Boolean)",
    )
    vals = sorted({int(v) for v in vals if str(v).isdigit()})  # skip prev/next
    if len(vals) < 2:
        return doms, links
    for v in vals:
        try:
            sel = f'.jet-filters-pagination__item[data-value="{v}"]'
            if pg.locator(sel).count():
                pg.locator(sel).first.scroll_into_view_if_needed(timeout=5000)
                pg.locator(sel).first.click(timeout=8000)
                pg.wait_for_timeout(2600)
            doms.append(pg.content())
            links.extend(harvest_links(pg))
            print(f"      pag {v}: {pg.locator(ITEM).count()} items in DOM", flush=True)
        except Exception as e:
            print(f"      pag {v} FAILED: {type(e).__name__}", flush=True)
    return doms, links


def crawl(pg, url, key):
    pg.goto(url, wait_until="networkidle", timeout=90000)
    pg.wait_for_timeout(2500)
    click_all_tabs(pg)
    n = exhaust_scroll(pg)
    doms, pag_links = exhaust_pagination(pg)

    links = harvest_links(pg) + pag_links
    seen, uniq = set(), []
    for l in links:
        k = (l["href"], l["text"])
        if k not in seen:
            seen.add(k)
            uniq.append(l)

    html = "\n<!-- ===== PAGE BREAK ===== -->\n".join(doms) if doms else pg.content()

    with open(f"{OUT}/{key}.html", "w", encoding="utf-8") as f:
        f.write(html)
    with open(f"{OUT}/{key}.links.json", "w", encoding="utf-8") as f:
        json.dump(uniq, f, ensure_ascii=False, indent=1)
    ext = {l["href"] for l in uniq if "lab-doxa.org.br" not in l["href"]}
    print(f"  {key:38s} items={n:4d} pags={len(doms) or 1} bytes={len(html):8d} ext={len(ext)}", flush=True)
    return n


def main():
    targets = [(f"{BASE}/{s}/", f"page__{s}") for s in PAGES]
    targets += [(f"{BASE}/{s}/", f"post__{s[:55]}") for s in POSTS]
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", headless=True)
        ctx = b.new_context(viewport={"width": 1440, "height": 1000})
        pg = ctx.new_page()
        pg.set_default_timeout(30000)
        for url, key in targets:
            try:
                crawl(pg, url, key)
            except Exception as e:
                print(f"  !! {key} FAILED {type(e).__name__}: {str(e)[:120]}", flush=True)
        b.close()


if __name__ == "__main__":
    main()
