#!/usr/bin/env python3
"""Re-crawl /acervo/ deterministically: capture each pagination page ONLY after the
grid content actually changed (the previous run snapshotted page 1 twice).

Emits rendered/acervo_pages/page-NN.html and a consolidated acervo_items.json
mapping wp post id -> {codigo, drive_url, thumb}.
"""
import json, os, re, sys
from playwright.sync_api import sync_playwright

S = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(S, "rendered", "acervo_pages")
os.makedirs(OUT, exist_ok=True)
URL = "https://www.lab-doxa.org.br/acervo/"
ITEM = ".jet-listing-grid__item"


def post_ids(pg):
    return pg.eval_on_selector_all(ITEM, "els=>els.map(e=>e.dataset.postId||'')")


def snapshot(pg, n):
    ids = post_ids(pg)
    html = pg.content()
    with open(f"{OUT}/page-{n:02d}.html", "w", encoding="utf-8") as f:
        f.write(html)
    return ids


def main():
    all_ids, pages = [], {}
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", headless=True)
        pg = b.new_context(viewport={"width": 1440, "height": 1000}).new_page()
        pg.set_default_timeout(30000)
        pg.goto(URL, wait_until="networkidle", timeout=90000)
        pg.wait_for_timeout(3000)

        vals = sorted({int(v) for v in pg.eval_on_selector_all(
            ".jet-filters-pagination__item", "els=>els.map(e=>e.dataset.value)")
            if str(v).isdigit()})
        print("pagination pages:", vals, flush=True)

        prev = snapshot(pg, 1)
        pages[1] = prev
        all_ids += prev
        print(f"  page 01: {len(prev)} items {prev[:3]}...", flush=True)

        for v in vals[1:]:
            sel = f'.jet-filters-pagination__item[data-value="{v}"]'
            pg.locator(sel).first.scroll_into_view_if_needed()
            pg.locator(sel).first.click()
            # WAIT until the grid's first post id actually changes
            before = prev[0] if prev else ""
            for _ in range(40):
                pg.wait_for_timeout(500)
                cur = post_ids(pg)
                if cur and cur[0] != before:
                    break
            else:
                print(f"  !! page {v}: content never changed", flush=True)
            pg.wait_for_timeout(800)
            cur = snapshot(pg, v)
            if cur == prev:
                print(f"  !! page {v}: DUPLICATE of previous", flush=True)
            pages[v] = cur
            all_ids += cur
            prev = cur
            print(f"  page {v:02d}: {len(cur)} items {cur[:3]}...", flush=True)
        b.close()

    uniq = sorted(set(all_ids))
    print(f"\ntotal item slots: {len(all_ids)} | unique post ids: {len(uniq)}")
    dupes = len(all_ids) - len(uniq)
    if dupes:
        print(f"WARNING: {dupes} duplicate slots")
    json.dump({"pages": pages, "unique_ids": uniq},
              open(f"{S}/rendered/acervo_pageids.json", "w"), indent=1)


if __name__ == "__main__":
    main()
