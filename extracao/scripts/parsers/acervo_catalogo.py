#!/usr/bin/env python3
"""Normalise the DOXA master audiovisual catalogue (Google Sheets export).

The 'Catálogo DOXA' tab is the master; the per-year tabs (1988..2018) are subsets.
~70 PARTIDO_XXX columns holding SIM/NÃO are collapsed into one ';'-separated column.
"""
import os, sys
import pandas as pd

S = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = f"{S}/sheets/acervo-catalog.xlsx"
MASTER = "Catálogo DOXA"

RENAME = {
    "Carimbo de data/hora": "carimbo",
    "ANO": "ano",
    "DATA": "data",
    "CÓDIGO": "codigo",
    "PROGRAMA": "programa",
    "CARGO": "cargo",
    "OBSERVAÇÃO:": "observacao",
    "ESTADO": "estado",
    "SÃO ELEIÇÕES MUNICIPAIS?": "eleicao_municipal",
    "QUAL MUNICÍPIO?": "municipio",
    "TEM DVD FÍSICO": "tem_dvd_fisico",
    "DVD FUNCIONA": "dvd_funciona",
    "DVD ESTÁ NO DRIVE": "dvd_no_drive",
    "DVD ESTÁ NO HD EXTERNO": "dvd_no_hd",
    "BACK UP FUNCIONANDO": "backup_ok",
}
KEEP = list(RENAME.values())


def norm(v):
    return str(v).strip() if pd.notna(v) else ""


def main():
    x = pd.ExcelFile(SRC)
    df = x.parse(MASTER, header=0, dtype=str)
    df = df.loc[:, ~df.columns.astype(str).str.startswith("Unnamed")]

    party_cols = [c for c in df.columns if str(c).startswith("PARTIDO_")]
    print(f"master rows={len(df)}  party columns={len(party_cols)}")

    def parties(row):
        out = []
        for c in party_cols:
            if norm(row[c]).upper() == "SIM":
                out.append(str(c).replace("PARTIDO_", ""))
        return ";".join(sorted(set(out)))

    out = pd.DataFrame({new: df[old].map(norm) if old in df.columns else ""
                        for old, new in RENAME.items()})
    out["partidos"] = df.apply(parties, axis=1)
    out = out[[c for c in KEEP if c != "carimbo"] + ["partidos"]]
    out = out[out["codigo"].str.strip() != ""]  # drop blank rows

    dst = f"{S}/extracted/acervo-catalogo-mestre.csv"
    out.to_csv(dst, index=False, encoding="utf-8")
    print(f"wrote {dst}: {len(out)} data rows")

    # Is the master a superset of every per-year tab?
    master_codes = set(out["codigo"])
    missing_total = 0
    for name in x.sheet_names:
        if not name.isdigit():
            continue
        d = x.parse(name, header=0, dtype=str)
        col = [c for c in d.columns if str(c).strip() == "CÓDIGO"]
        if not col:
            continue
        codes = {norm(c) for c in d[col[0]] if norm(c)}
        missing = codes - master_codes
        missing_total += len(missing)
        if missing:
            print(f"  tab {name}: {len(missing)} codigos NOT in master, e.g. {sorted(missing)[:4]}")
    print(f"per-year codes missing from master: {missing_total}")

    # summary
    summary = {
        "total": len(out),
        "por_ano": out["ano"].value_counts().sort_index().to_dict(),
        "por_programa": out["programa"].value_counts().head(12).to_dict(),
        "com_dvd_fisico": int((out["tem_dvd_fisico"].str.upper() == "SIM").sum()),
        "backup_ok": int((out["backup_ok"].str.upper() == "SIM").sum()),
        "no_drive": int((out["dvd_no_drive"].str.upper() == "SIM").sum()),
    }
    import json
    print(json.dumps(summary, ensure_ascii=False, indent=1)[:1200])
    json.dump(summary, open(f"{S}/extracted/_acervo_catalogo_summary.json", "w"),
              ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
