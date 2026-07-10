#!/usr/bin/env python3
"""Data sources that live outside WordPress, plus published files no page links to."""
import json, os, re
from urllib.parse import unquote

S = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def q(s):
    return '"' + str(s).replace("\\", "\\\\").replace('"', '\\"') + '"'


SOURCES = [
    {
        "nome": "Catálogo mestre do acervo audiovisual",
        "tipo": "google_sheets",
        "url": "https://docs.google.com/spreadsheets/d/1b_OFFW0fJS3B0DFvfeoa6y8l9YG6JmFP/edit?usp=sharing&ouid=110351746423153842923&rtpof=true&sd=true",
        "export_csv": "https://docs.google.com/spreadsheets/d/1b_OFFW0fJS3B0DFvfeoa6y8l9YG6JmFP/export?format=csv",
        "export_xlsx": "https://docs.google.com/spreadsheets/d/1b_OFFW0fJS3B0DFvfeoa6y8l9YG6JmFP/export?format=xlsx",
        "acesso": "público (leitura)",
        "registros": 2034,
        "abas": "Catálogo DOXA + 'Respostas ao formulário 1' + uma aba por ano (1988–2018)",
        "arquivo_local": "dados/acervo-catalogo-mestre.csv",
        "nota": "Inventário completo das fitas (1988–2018). É MUITO maior que os 95 itens publicados em /acervo/.",
    },
    {
        "nome": "Vídeos do acervo",
        "tipo": "google_drive",
        "url": "https://drive.google.com/",
        "acesso": "links individuais por item (ver dados/acervo.yaml)",
        "registros": 95,
        "nota": "Cada item publicado do acervo aponta para um arquivo próprio no Google Drive.",
    },
    {
        "nome": "Programas de governo dos candidatos (RJ 2020)",
        "tipo": "tse_divulgacandcontas",
        "url": "https://divulgacandcontas.tse.jus.br/",
        "registros": 577,
        "arquivo_local": "dados/programas-eleitorais-rj.csv",
    },
    {
        "nome": "Dashboard Power BI — Eleições Rio e São Paulo 2024",
        "tipo": "power_bi",
        "url": "https://app.powerbi.com/view?r=eyJrIjoiNDk3MDhjYjktYWNhMC00Y2JhLTgxNDUtZWQzNDM1MGM0N2YwIiwidCI6Ijc0OTMyMDFlLTdhNDUtNDk3OC1iZWZkLTBlZDAwMmIwZjgyMiJ9",
        "acesso": "público",
        "nota": "URL de embed real. Na home do site original DOIS cards apontam para ela: 'Eleições Rio e São Paulo 2024' e 'Textos de discussão do Doxa' — este último é quase certamente um link errado na fonte.",
    },
    {
        "nome": "Canal do DOXA no YouTube",
        "tipo": "youtube",
        "url": "https://www.youtube.com/channel/UCkcuDdIEuQ9YqOjHsp4-EHQ",
    },
]

DATASETS = [
    ("Banco de dados — Decretos COVID RJ", "DOWNLOAD-2_-BANCO-DE-DADOS_DECRETOS-COVID_RJ_3006.xlsx"),
    ("Lista de buscadores — Decretos", "DOWNLOAD-1_LISTA-DE-BUSCADORES_DECRETOS.xlsx"),
    ("Survey IESP-BR — dez/2020 (microdados)", "DADOS_SURVEY_IESPBR_208324-Wed-Dec-16-2020_total.xlsx"),
    ("Survey IESP-BR — dez/2021 (microdados)", "DADOS_SURVEY_IESPBR_227821_20211208.xlsx"),
    ("Formulário de solicitação de material do acervo", "Solicitacao-de-Material-do-Acervo.docx"),
]


def main():
    unlinked = json.load(open(f"{S}/extracted/_pdfs_sem_pagina.json"))

    L = ["# Fontes de dados externas ao WordPress + arquivos publicados sem página que os linke",
         "# Extraído em 2026-07-09 de https://www.lab-doxa.org.br", "",
         "fontes:"]
    for s in SOURCES:
        L.append(f"  - nome: {q(s['nome'])}")
        for k, v in s.items():
            if k == "nome":
                continue
            L.append(f"    {k}: {v if isinstance(v, int) else q(v)}")
        L.append("")

    L.append("datasets_baixados:")
    L.append("  # microdados e planilhas hospedados no WordPress, copiados para bruto/datasets/")
    for nome, fn in DATASETS:
        L.append(f"  - nome: {q(nome)}")
        L.append(f"    arquivo: {q('bruto/datasets/' + fn)}")
        L.append("")

    L.append("pdfs_publicados_sem_pagina:")
    L.append(f"  # {len(unlinked)} PDFs existem na biblioteca de mídia mas NENHUMA página viva os linka.")
    L.append("  # Provavelmente perderam a página que os referenciava. Ver dados/biblioteca-midia.csv.")
    for u in unlinked:
        L.append(f"  - {q(unquote(u))}")
    L.append("")

    open(f"{S}/extracted/fontes_externas.yaml", "w", encoding="utf-8").write("\n".join(L))
    print(f"fontes: {len(SOURCES)} | datasets: {len(DATASETS)} | pdfs sem página: {len(unlinked)}")


if __name__ == "__main__":
    main()
