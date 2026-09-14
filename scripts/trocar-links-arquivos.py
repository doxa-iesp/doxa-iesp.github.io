#!/usr/bin/env python3
"""
Troca links `origem -> novo endereço` em arquivos de conteúdo, por substituição literal de string
(preserva formatação, comentários e indentação — não usa um parser de YAML).

Usado para a migração dos PDFs que o site buscava no WordPress antigo (ver DADOS_PENDENTES.md e
arquivos-preservados/LEIA-ME.md) e, em 2026-09-13, para levar os 273 mapas de votação ao Google Drive
do DOXA. Serve de novo se os mapas mudarem de endereço outra vez (Zenodo, repositório do IESP...).

Uso:
    python3 scripts/trocar-links-arquivos.py MAPA.csv ARQUIVO.yaml [ARQUIVO2.yaml ...]

`MAPA.csv` precisa ter pelo menos as colunas `origem` e `novo` (um CSV no formato de
`arquivos-preservados/manifesto.csv` também serve, desde que se acrescente uma coluna `novo` com o
endereço final de cada arquivo).

Rode em todos os arquivos que guardam o mesmo link. Para os mapas são três (CLAUDE.md, armadilha
2d): `src/data/mapas-votacao.yaml`, `public/dados/mapas-votacao.csv` e
`extracao/dados/mapas-no-drive.csv` — este último é lido pelo build para montar
`/arquivos-antigos.json`. O resto de `extracao/` é registro histórico e não precisa ser tocado.
"""
import csv
import sys


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    caminho_mapa, *alvos = sys.argv[1:]

    with open(caminho_mapa, newline="", encoding="utf-8") as f:
        linhas = list(csv.DictReader(f))
    for campo in ("origem", "novo"):
        if linhas and campo not in linhas[0]:
            sys.exit(f"erro: {caminho_mapa} precisa de uma coluna '{campo}'")

    mapa = {}
    for linha in linhas:
        origem, novo = linha["origem"].strip(), linha["novo"].strip()
        if origem and novo:
            mapa.setdefault(origem, novo)

    usados = set()
    for caminho in alvos:
        # `newline=""` na leitura E na escrita preserva as quebras de linha do arquivo como
        # estão. Sem isso o Python lê CRLF como LF e grava LF: na troca dos mapas, em
        # 2026-09-13, os dois CSVs (que são CRLF) mudavam em TODAS as linhas, cabeçalho
        # incluído, e o diff escondia as 273 trocas de verdade.
        with open(caminho, encoding="utf-8", newline="") as f:
            texto = f.read()
        antes = texto
        for origem, novo in mapa.items():
            if origem in texto:
                texto = texto.replace(origem, novo)
                usados.add(origem)
        if texto != antes:
            with open(caminho, "w", encoding="utf-8", newline="") as f:
                f.write(texto)
            print(f"{caminho}  atualizado")
        else:
            print(f"{caminho}  nenhuma ocorrência")

    faltando = [o for o in mapa if o not in usados]
    print(f"\nlinhas do mapa usadas em algum arquivo: {len(usados)} de {len(mapa)}")
    if faltando:
        print("NÃO encontradas em nenhum dos arquivos passados (confira manualmente):")
        for o in faltando:
            print(" ", o)


if __name__ == "__main__":
    main()
