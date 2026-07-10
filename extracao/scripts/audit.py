#!/usr/bin/env python3
"""Completeness audit: is every 'data link' on the live site captured somewhere?"""
import glob, json, os, re, sys, collections
from urllib.parse import unquote

S = os.path.dirname(os.path.abspath(__file__))


def norm(u):
    """The DOM percent-encodes '–' and '°'; the YAML stores them decoded. Same URL."""
    return unquote(u).strip()

DATA_HOSTS = ("drive.google.com", "docs.google.com", "divulgacandcontas.tse.jus.br",
              "bdtd.uerj.br", "app.powerbi.com", "lattes.cnpq.br")


def is_data_link(u):
    ul = u.lower()
    if ul.endswith(".pdf") or ".pdf?" in ul or ".pdf#" in ul:
        return True
    if ul.endswith((".xlsx", ".csv", ".docx", ".zip")):
        return True
    return any(h in ul for h in DATA_HOSTS)


def main():
    # 1. every link seen while crawling
    site = collections.defaultdict(set)  # url -> pages it appeared on
    for f in glob.glob(f"{S}/rendered/*.links.json"):
        page = os.path.basename(f).replace(".links.json", "")
        for l in json.load(open(f)):
            if is_data_link(l["href"]):
                site[l["href"]].add(page)

    # 2. every string present in any extracted DATA artifact.
    # '_*' files are audit/meta reports — a URL merely mentioned there is NOT captured data.
    blob = []
    for f in glob.glob(f"{S}/extracted/*"):
        if os.path.basename(f).startswith("_"):
            continue
        if os.path.isfile(f):
            try:
                blob.append(open(f, encoding="utf-8", errors="replace").read())
            except Exception:
                pass
    blob = norm("\n".join(blob))

    orphans = {u: p for u, p in site.items() if norm(u) not in blob}
    print(f"data links on site : {len(site)}")
    print(f"captured           : {len(site) - len(orphans)}")
    print(f"ORPHANS            : {len(orphans)}\n")

    by_page = collections.Counter()
    for u, pages in orphans.items():
        for p in pages:
            by_page[p] += 1
    for p, n in by_page.most_common():
        print(f"  {n:4d}  {p}")

    # 3. WordPress media library: PDFs never referenced anywhere
    media = json.load(open(f"{S}/raw/media.json"))
    pdfs = [m["source_url"] for m in media if m.get("mime_type") == "application/pdf"]
    site_urls = norm("\n".join(site.keys()))
    unref = [u for u in pdfs if norm(u) not in blob and norm(u) not in site_urls]
    print(f"\nmedia-library PDFs : {len(pdfs)}")
    print(f"never referenced   : {len(unref)}  (published files whose linking page is gone)")

    json.dump({"orphans": {u: sorted(p) for u, p in orphans.items()},
               "unreferenced_media_pdfs": unref},
              open(f"{S}/extracted/_orphans.json", "w"), ensure_ascii=False, indent=1)

    if orphans:
        print("\nsample orphans:")
        for u in list(orphans)[:8]:
            print("   ", u[:118])


if __name__ == "__main__":
    main()
