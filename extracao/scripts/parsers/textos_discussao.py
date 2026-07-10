#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parser: Textos para Discussão (working papers) do DOXA.

Fontes:
  raw/textos-discussao.json                             -> CPT (WP REST API), usado só para
                                                           conferência de contagem/IDs/datas.
  rendered/page__textos-para-discussao-2.html           -> listagem renderizada (DOM final).
  rendered/post__novo-texto-para-discussao-as-...html   -> post que anuncia o TD nº 2 (armas),
                                                           de onde vem o abstract.

Saída: extracted/textos_discussao.yaml
Schema (igual ao data/discussions.yaml do site Hugo): title, authors, year, url
       + abstract (apenas quando existe na fonte).
"""
import json
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup

WS = Path("/private/tmp/claude-501/-Users-felipelmc-Desktop-DOXA/"
          "7878c6cf-422b-4c52-a764-25acbf2904f3/scratchpad")

LISTING = WS / "rendered" / "page__textos-para-discussao-2.html"
POST_ARMAS = (WS / "rendered" /
              "post__novo-texto-para-discussao-as-politicas-de-controle-de-a.html")
CPT_JSON = WS / "raw" / "textos-discussao.json"
OUT = WS / "extracted" / "textos_discussao.yaml"


def parse_listing(path: Path):
    """Extrai os itens da listagem renderizada.

    Cada item aparece como um bloco cujo texto, em ordem, é:
      ['Textos para discussão:', '<n>', '<título>', '<autor>', '<ano>']
    (dois <a> apontam para o mesmo PDF: um com o número, outro com título+autor).
    """
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    items = {}
    for a in soup.find_all("a", href=re.compile(r"\.pdf$", re.I)):
        pdf = a.get("href")
        block = a
        for _ in range(4):  # sobe até o container que agrega número/título/autor/ano
            if block.parent:
                block = block.parent
        strings = [s.strip() for s in block.stripped_strings if s.strip()]
        # remove o rótulo fixo
        strings = [s for s in strings if s.lower() != "textos para discussão:"]
        year = next((s for s in strings if re.fullmatch(r"\d{4}", s)), "")
        number = next((s for s in strings
                       if re.fullmatch(r"\d{1,3}", s) and s != year), "")
        rest = [s for s in strings if s not in (year, number)]
        if len(rest) < 2:
            continue
        title, authors = rest[0], rest[1]
        items[pdf] = {
            "number": int(number) if number else None,
            "title": title,
            "authors": authors,
            "year": int(year) if year else None,
            "url": pdf,
        }
    # ordena pelo número do TD (desc: mais recente primeiro, como no site)
    return sorted(items.values(),
                  key=lambda d: (d["number"] is None, -(d["number"] or 0)))


def parse_abstract(path: Path):
    """Extrai o resumo do post que anuncia o TD sobre armas.

    O corpo tem parágrafos descritivos + um link 'Acesse o texto na íntegra' +
    parágrafo de crédito + rodapé. O abstract são os parágrafos analíticos.
    """
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    paras = [p.get_text(" ", strip=True) for p in soup.find_all("p")]
    paras = [p for p in paras if len(p) > 40]
    skip_prefixes = (
        "Acesse o texto na íntegra",
        "Confira todos",
        "Instituto de Estudos",
        "A pesquisa foi realizada",
    )
    keep = [p for p in paras if not any(p.startswith(pre) for pre in skip_prefixes)]
    return "\n\n".join(keep).strip()


def yaml_dump(items):
    """Serializa à mão para controlar ordem de campos e blocos literais do abstract."""
    def q(s):
        return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'

    lines = ["# Textos para Discussão (Working Papers)",
             "# Campos: title, authors, year, url, abstract (quando existe)",
             "# Fonte: rendered/page__textos-para-discussao-2.html (listagem)",
             "#        rendered/post__novo-texto-para-discussao-...html (abstract do TD 2)",
             ""]
    for it in items:
        lines.append(f"- title: {q(it['title'])}")
        lines.append(f"  authors: {q(it['authors'])}")
        lines.append(f"  year: {it['year']}")
        lines.append(f"  url: {q(it['url'])}")
        if it.get("abstract"):
            lines.append("  abstract: |-")
            for para in it["abstract"].split("\n\n"):
                for i, sub in enumerate(para.split("\n")):
                    lines.append("    " + sub)
                lines.append("")  # linha em branco entre parágrafos
            # remove última linha em branco extra
            while lines and lines[-1] == "":
                lines.pop()
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main():
    cpt = json.loads(CPT_JSON.read_text(encoding="utf-8"))
    cpt_titles = {c["title"]["rendered"] for c in cpt}
    print(f"[cpt] {len(cpt)} itens no CPT (REST API): {sorted(cpt_titles)}",
          file=sys.stderr)

    items = parse_listing(LISTING)
    print(f"[dom] {len(items)} itens na listagem renderizada", file=sys.stderr)

    abstract = parse_abstract(POST_ARMAS)
    # anexa o abstract ao item cujo PDF é o do post sobre armas
    for it in items:
        if "Politicas-de-controle-de-armas" in it["url"]:
            it["abstract"] = abstract

    # remove o campo auxiliar 'number' da saída
    for it in items:
        it.pop("number", None)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(yaml_dump(items), encoding="utf-8")
    print(f"[out] escrito {OUT} ({len(items)} itens)", file=sys.stderr)


if __name__ == "__main__":
    main()
