#!/usr/bin/env python3
"""Dump the full WordPress REST API of lab-doxa.org.br into raw/*.json"""
import json, os, ssl, sys, time, urllib.request, urllib.error
import certifi

SSL_CTX = ssl.create_default_context(cafile=certifi.where())

BASE = "https://www.lab-doxa.org.br/wp-json/wp/v2"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw")
os.makedirs(OUT, exist_ok=True)

ENDPOINTS = [
    "posts", "pages", "acervo-doxa", "textos-discussao", "lista-pesquisas",
    "media", "categories", "tags", "ano", "estado", "regiao", "partidos",
    "cargo-eletivo", "tipo-de-video", "tipo-pesquisa",
    "candidatos-presidente", "candidatos-governador", "users",
]

def get(url, tries=4):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "doxa-migration/1.0"})
            with urllib.request.urlopen(req, timeout=60, context=SSL_CTX) as r:
                return json.loads(r.read().decode("utf-8")), dict(r.headers)
        except urllib.error.HTTPError as e:
            if e.code in (400, 404):  # past last page / no such endpoint
                return None, {}
            last = f"HTTP {e.code}"
            time.sleep(1.5 * (i + 1))
        except Exception as e:
            last = f"{type(e).__name__}: {e}"
            time.sleep(1.5 * (i + 1))
    print(f"  !! giving up on {url} ({last})", file=sys.stderr)
    return None, {}

summary = {}
for ep in ENDPOINTS:
    items, page = [], 1
    while True:
        data, hdrs = get(f"{BASE}/{ep}?per_page=100&page={page}&context=view")
        if not data:
            break
        items.extend(data)
        total_pages = int(hdrs.get("X-WP-TotalPages", 1) or 1)
        if page >= total_pages:
            break
        page += 1
        time.sleep(0.25)
    path = os.path.join(OUT, f"{ep}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=1)
    summary[ep] = len(items)
    print(f"{ep:26s} {len(items):5d} items -> raw/{ep}.json", flush=True)

with open(os.path.join(OUT, "_summary.json"), "w") as f:
    json.dump(summary, f, indent=1)
print("\nTOTAL objects:", sum(summary.values()))
