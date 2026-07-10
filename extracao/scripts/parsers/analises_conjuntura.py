#!/usr/bin/env python3
"""
Auditoria/extração das ANÁLISES DE CONJUNTURA ELEITORAL do site DOXA.

Fontes (DOM renderizado):
  rendered/page__analises-de-conjuntura-eleitoral.html  (página canônica, no menu)
  rendered/page__analise.html                           (página alternativa/antiga "Análises DOXA")

O script:
  1. extrai, em ordem de leitura, os cabeçalhos (h2) e os links .pdf de cada página;
  2. compara os conjuntos de URLs (comum / só-conjuntura / só-analise);
  3. lista os itens presentes SÓ na página /analise/ (candidatos a "novos").

Os títulos/descrições enriquecidos do YAML final vêm do arquivo de referência
data/analyses.yaml (25 itens, já auditados) — este script serve para VERIFICAR
que aquele conjunto casa com o DOM e para IDENTIFICAR o que a página /analise/
acrescenta. Nada é inventado: cada URL é rastreável ao href do DOM.
"""
import os
import re
from bs4 import BeautifulSoup

S = "/private/tmp/claude-501/-Users-felipelmc-Desktop-DOXA/7878c6cf-422b-4c52-a764-25acbf2904f3/scratchpad"
RENDERED = os.path.join(S, "rendered")


def walk(key):
    """Retorna lista ordenada de ('H', texto) e ('PDF', anchor, href)."""
    html = open(os.path.join(RENDERED, f"{key}.html"), encoding="utf-8").read()
    soup = BeautifulSoup(html, "html.parser")
    for sel in ("header", "footer", "nav", "script", "style"):
        for e in soup.select(sel):
            e.decompose()
    main = soup.find(id="jupiterx-main") or soup.body or soup
    out = []
    for el in main.descendants:
        name = getattr(el, "name", None)
        if name == "a" and el.get("href", "").lower().endswith(".pdf"):
            out.append(("PDF", el.get_text(strip=True), el["href"]))
        elif name in ("h1", "h2", "h3", "h4", "h5", "h6"):
            t = el.get_text(strip=True)
            if t:
                out.append(("H", t))
    # dedup consecutivo (Elementor duplica alguns nós)
    dedup, prev = [], None
    for item in out:
        if item != prev:
            dedup.append(item)
        prev = item
    return dedup


def pdf_urls(items):
    return {u for (kind, *rest) in items if kind == "PDF" for u in [rest[1]]}


def basename(u):
    return u.split("/")[-1]


conj = walk("page__analises-de-conjuntura-eleitoral")
anal = walk("page__analise")

cu = {basename(u) for u in pdf_urls(conj)}
au = {basename(u) for u in pdf_urls(anal)}

print(f"conjuntura: {sum(1 for i in conj if i[0]=='PDF')} links pdf ({len(cu)} únicos)")
print(f"analise   : {sum(1 for i in anal if i[0]=='PDF')} links pdf ({len(au)} únicos)")
print(f"comuns    : {len(cu & au)}")
print("\n-- só na conjuntura --")
for b in sorted(cu - au):
    print("  ", b)
print("\n-- só na /analise/ (candidatos a NOVOS) --")
for kind, *rest in anal:
    if kind == "PDF" and basename(rest[1]) in (au - cu):
        print(f'   anchor="{rest[0]}"  ->  {rest[1]}')
