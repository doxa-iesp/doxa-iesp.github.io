#!/usr/bin/env python3
"""Inventory of the whole WordPress media library (431 items).

The binaries total ~0.94 GB, so we archive the *index* (URL + title + date + type),
not the files. This is also the only record of documents whose linking page is gone.
"""
import csv, html as H, json, os, re

S = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def clean(s):
    return re.sub(r"\s+", " ", H.unescape(s or "")).strip()


def main():
    media = json.load(open(f"{S}/raw/media.json"))
    rows = []
    for m in media:
        rows.append({
            "id": m["id"],
            "date": m["date"][:10],
            "mime": m.get("mime_type", ""),
            "title": clean(m.get("title", {}).get("rendered", "")),
            "filename": os.path.basename(m["source_url"]),
            "url": m["source_url"],
        })
    rows.sort(key=lambda r: (r["mime"], r["date"]))
    dst = f"{S}/extracted/biblioteca-midia.csv"
    with open(dst, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    from collections import Counter
    print(f"wrote {dst}: {len(rows)} items")
    for k, v in Counter(r["mime"] for r in rows).most_common():
        print(f"  {v:4d}  {k}")


if __name__ == "__main__":
    main()
