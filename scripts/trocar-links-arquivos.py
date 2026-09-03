#!/usr/bin/env python3
"""
Troca links `origem -> novo endereço` em arquivos de conteúdo, por substituição literal de string
(preserva formatação, comentários e indentação — não usa um parser de YAML).

Usado para a migração dos PDFs que o site buscava no WordPress antigo (ver DADOS_PENDENTES.md e
arquivos-preservados/LEIA-ME.md) e pensado para ser reaproveitado no dia em que os 273 mapas de
votação ganharem um endereço definitivo (Zenodo, Drive, repositório do IESP...).

Uso:
    python3 scripts/trocar-links-arquivos.py MAPA.csv ARQUIVO.yaml [ARQUIVO2.yaml ...]

`MAPA.csv` precisa ter pelo menos as colunas `origem` e `novo` (um CSV no formato de
`arquivos-preservados/manifesto.csv` também serve, desde que se acrescente uma coluna `novo` com o
endereço final de cada arquivo).

Sempre rode nos dois lugares que precisam bater (regra do CLAUDE.md, seção "Regenerar o
conteúdo"): o(s) arquivo(s) em `src/data/` E o(s) equivalente(s) em `extracao/dados/` — senão o
próximo `scripts/converter-conteudo.py` desfaz a troca.
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
        with open(caminho, encoding="utf-8") as f:
            texto = f.read()
        antes = texto
        for origem, novo in mapa.items():
            if origem in texto:
                texto = texto.replace(origem, novo)
                usados.add(origem)
        if texto != antes:
            with open(caminho, "w", encoding="utf-8") as f:
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
