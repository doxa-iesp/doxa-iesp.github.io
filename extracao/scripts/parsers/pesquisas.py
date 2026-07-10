#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extrai as 61 PESQUISAS do DOXA a partir do DOM renderizado
(rendered/page__pagina-pesquisas.html), cruzando com a REST API
(raw/lista-pesquisas.json) para o tipo-pesquisa autoritativo.

Saida: extracted/pesquisas.yaml

Regras:
- Nunca inventar dados; todo campo rastreavel ao DOM/JSON de origem.
- Campo ausente => omitido.
- Titulos preservados verbatim (aspas curvas, pontuacao).
"""
import json, re, sys
from bs4 import BeautifulSoup

BASE = "/private/tmp/claude-501/-Users-felipelmc-Desktop-DOXA/7878c6cf-422b-4c52-a764-25acbf2904f3/scratchpad"
HTML = BASE + "/rendered/page__pagina-pesquisas.html"
REST = BASE + "/raw/lista-pesquisas.json"
OUT  = BASE + "/extracted/pesquisas.yaml"

TERM_STATUS = {87: "tese", 85: "andamento", 86: "concluida"}
TERM_NAME   = {87: "Teses e Dissertações", 85: "Pesquisa em Andamento", 86: "Pesquisa Concluída"}

def clean(s):
    if s is None:
        return s
    s = s.replace("\xa0", " ")
    s = re.sub(r"[ \t]+", " ", s)
    return s.strip()

def author_from_title(f1):
    """'SOBRENOME, Nome - ANO' -> ('Nome Sobrenome', ano|None)."""
    year = None
    m = re.search(r"\s[–—-]\s*(\d{4})\s*$", f1)
    namepart = f1
    if m:
        year = int(m.group(1))
        namepart = f1[:m.start()].strip()
    if "," in namepart:
        surname, given = namepart.split(",", 1)
        surname = " ".join(w.capitalize() for w in surname.split())
        given = given.strip()
        author = (given + " " + surname).strip()
    else:
        author = namepart.strip()
    return clean(author), year

def parse_advisor_institution(p1):
    """p1 = 'Orientador(a): NOME. Tese/Dissertacao (nivel) - INSTITUICAO'."""
    advisor = None
    institution = None
    ma = re.search(r"Orientador(?:a)?:\s*(.+?)\.\s", p1)
    if ma:
        advisor = clean(ma.group(1))
    mi = re.search(r"(?:Tese|Dissertação)\s*\([^)]*\)\s*[–—-]\s*([^.]+?)\s*(?:\.|$)", p1)
    if mi:
        institution = clean(mi.group(1))
    return advisor, institution

def get_resumo(paras):
    for p in paras:
        t = clean(p)
        if t.lower().startswith("resumo:"):
            return clean(t[len("resumo:"):])
    return None

def get_lead(paras):
    """Responsavel / Coordenador(a) / Coordenacao -> valor (autor lider)."""
    for label in ("Responsável:", "Coordenadora:", "Coordenador:", "Coordenação:"):
        for p in paras:
            t = clean(p)
            if t.startswith(label):
                val = clean(t[len(label):])
                val = val.rstrip(".").strip()
                return val
    return None

def main():
    soup = BeautifulSoup(open(HTML, encoding="utf-8"), "html.parser")
    items = {int(it.get("data-post-id")): it for it in soup.select(".jet-listing-grid__item")}
    rest = json.load(open(REST))
    term_by_id = {it["id"]: (it.get("tipo-pesquisa") or [None])[0] for it in rest}
    slug_by_id = {it["id"]: it.get("slug") for it in rest}

    # sanity: same 61 ids
    assert len(items) == 61, "HTML items != 61: %d" % len(items)
    assert len(rest) == 61, "REST items != 61: %d" % len(rest)
    assert set(items) == set(term_by_id), "id mismatch HTML vs REST"

    records = []
    dom_order = list(items.keys())  # DOM order
    for idx, pid in enumerate(dom_order):
        it = items[pid]
        tid = term_by_id.get(pid)
        status = TERM_STATUS[tid]
        fields = it.select(".jet-listing-dynamic-field__content")
        f1 = clean(fields[0].get_text(" ", strip=True))
        f2 = fields[1]
        a = f2.find("a")
        url = a.get("href") if a else None
        paras = [p.get_text(" ", strip=True) for p in f2.find_all("p")]

        rec = {"_pid": pid, "_idx": idx, "status": status}

        if status == "tese":
            author, year = author_from_title(f1)
            title = clean(paras[0]) if paras else clean(f1)
            rec["title"] = title
            if author:
                rec["author"] = author
            if year is not None:
                rec["year"] = year
            # advisor / institution from p1 (if present)
            if len(paras) >= 2:
                p1 = clean(paras[1])
                n_orient = len(re.findall(r"Orientador(?:a)?:", p1))
                adv, inst = parse_advisor_institution(p1)
                if adv:
                    rec["advisor"] = adv
                if inst:
                    rec["institution"] = inst
                if n_orient > 1:
                    # caso especial [990]: preserva a linha completa
                    rec["description"] = p1
            if url:
                rec["url"] = url
        else:
            # andamento / concluida
            rec["title"] = clean(f1)
            lead = get_lead(paras)
            if lead:
                rec["author"] = lead
            resumo = get_resumo(paras)
            if resumo:
                rec["description"] = resumo
            if url:
                rec["url"] = url

        records.append(rec)

    # ordena: teses (ano desc, None por ultimo, depois ordem DOM),
    #         depois andamento (ordem DOM), depois concluida (ordem DOM)
    order_key = {"tese": 0, "andamento": 1, "concluida": 2}
    def sort_key(r):
        if r["status"] == "tese":
            y = r.get("year")
            return (0, -(y if y is not None else -1), r["_idx"])
        return (order_key[r["status"]], 0, r["_idx"])
    records.sort(key=sort_key)

    # verificacao de contagem
    from collections import Counter
    cnt = Counter(r["status"] for r in records)
    assert cnt["tese"] == 38 and cnt["andamento"] == 13 and cnt["concluida"] == 10, cnt

    # emite YAML (estilo do schema de referencia: strings entre aspas duplas)
    def q(s):
        s = str(s)
        s = s.replace("\\", "\\\\").replace('"', '\\"')
        return '"' + s + '"'

    FIELD_ORDER = ["title", "author", "year", "advisor", "institution", "status", "url", "description"]
    lines = []
    lines.append("# Pesquisas do DOXA — Teses e Dissertacoes, Pesquisas em Andamento e Concluidas")
    lines.append("# Fonte: rendered/page__pagina-pesquisas.html + raw/lista-pesquisas.json (tipo-pesquisa)")
    lines.append("# Campos: title, author, year, advisor, institution, status, url, description")
    lines.append("# Status: tese | andamento | concluida")
    lines.append("# Total: 61 (tese=38, andamento=13, concluida=10)")
    lines.append("")
    for r in records:
        first = True
        for f in FIELD_ORDER:
            if f not in r:
                continue
            v = r[f]
            prefix = "- " if first else "  "
            if f == "year":
                lines.append("%s%s: %d" % (prefix, f, v))
            else:
                lines.append("%s%s: %s" % (prefix, f, q(v)))
            first = False
        lines.append("")

    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines).rstrip() + "\n")

    print("WROTE", OUT)
    print("counts:", dict(cnt), "total", len(records))
    # relatorio de completude
    for f in ["author", "year", "advisor", "institution", "url", "description"]:
        n = sum(1 for r in records if f in r)
        print("  with %-12s: %d" % (f, n))

if __name__ == "__main__":
    main()
