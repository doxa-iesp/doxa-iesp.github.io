# Extração completa do site WordPress lab-doxa.org.br

Extração integral dos dados do site antigo do DOXA (`https://www.lab-doxa.org.br`), feita em
**2026-07-09**, para servir de base à reconstrução do site em Hugo.

**Cobertura:** 999 de 999 links de dados presentes no site foram capturados (0 órfãos).
Nenhum PDF publicado ficou sem registro.

---

## O que tem aqui

| Pasta | Conteúdo |
|---|---|
| `dados/` | Dados limpos e estruturados (YAML e CSV). É isto que você quer usar. |
| `dados/paginas/` | Prosa editorial de cada página do site antigo (12 arquivos Markdown). |
| `assets/` | Imagens baixadas do site antigo (logos de parceiros). |
| `bruto/` | Fontes originais, sem tratamento: dump da REST API, planilhas e microdados. |
| `scripts/` | O crawler e os parsers. Tudo é reproduzível: rode e obtenha `dados/` de novo. |

### `dados/`

| Arquivo | Registros | Origem |
|---|---:|---|
| `equipe.yaml` | 15 | página `/institucional/` |
| `acervo.yaml` | 95 | REST API + DOM de `/acervo/` (10 páginas) |
| `acervo-catalogo-mestre.csv` | **2.034** | planilha Google (catálogo completo das fitas, 1988–2018) |
| `pesquisas.yaml` | 61 | `/pagina-pesquisas/` (38 teses, 13 em andamento, 10 concluídas) |
| `publicacoes-academicas.yaml` | 34 | `/publicacoes-academicas/` (+ 4 links Lattes) |
| `analises-conjuntura.yaml` | 28 | `/analises-de-conjuntura-eleitoral/` + `/analise/` |
| `textos-discussao.yaml` | 2 | CPT `textos-discussao` |
| `na-midia.yaml` | 70 | `/na-midia/` (27 impressa, 37 virtual, 6 audiovisual) |
| `eventos-seminarios.yaml` | 5 + 36 | posts da categoria "Evento" + `/seminarios/` |
| `bancos-de-dados.yaml` | 3 | `/bancos-de-dados/` |
| `programas-eleitorais-rj.csv` | 577 | post dos programas do RJ (links do TSE) |
| `programas-eleitorais-capitais.csv` | 244 | post dos programas das capitais ⚠️ ver *Defeitos* |
| `mapas-votacao.csv` | 273 | `/mapas-de-votacao/` |
| `pesquisa-covid.yaml` + `.md` | 16 | `/pesquisa-covid/` |
| `homepage-institucional.yaml` | — | `/inicio/` e `/institucional/` |
| `institucional.md` | — | prosa "Sobre o DOXA" |
| `biblioteca-midia.csv` | 431 | inventário da biblioteca de mídia do WordPress |
| `fontes-externas.yaml` | — | Google Sheets/Drive, TSE, Power BI, YouTube |
| `paginas/*.md` | 12 | prosa editorial de cada página (títulos + parágrafos) |
| `parceiros.yaml` | 8 | logos de parceiros/financiadores (imagens em `assets/parceiros/`) |

### `bruto/`

- `wp-rest/` — dump completo da WP REST API: 771 objetos (posts, páginas, os 3 custom post types,
  a biblioteca de mídia e todas as 10 taxonomias). `_taxonomy_map.json` resolve IDs → nomes.
- `planilhas/` — o catálogo mestre do acervo (`.xlsx` com 26 abas e o `.csv` da aba principal).
- `datasets/` — microdados hospedados no WordPress: os dois surveys IESP-BR (2020 e 2021),
  o banco de decretos COVID do RJ e o formulário de solicitação de material do acervo.

**Os 348 PDFs do site não foram baixados** (≈ 0,94 GB). Todos os seus URLs estão registrados em
`dados/biblioteca-midia.csv` e nos YAML correspondentes.

---

## Como os dados foram obtidos

O site é WordPress + Elementor + JetEngine. Isso importa por um motivo: **as listagens não
existem no HTML servido** — elas são montadas por JavaScript via AJAX. Raspar o HTML cru
devolve páginas vazias, e a REST API não expõe os campos (`acf` e `meta` vêm vazios).

Por isso a extração combina três fontes:

1. **REST API** (`scripts/dump.py`) — autoritativa para IDs, slugs, datas, títulos e taxonomias.
2. **DOM renderizado** (`scripts/crawl.py`, via Playwright + Chrome) — única fonte dos links de
   Google Drive, dos PDFs e dos campos dinâmicos. O crawler expande abas, dispara o scroll
   infinito do JetEngine e clica em toda a paginação.
3. **Google Sheets** — o catálogo mestre do acervo, exportado como CSV/XLSX.

### Reproduzir

```bash
pip install playwright beautifulsoup4 pandas openpyxl pyyaml certifi
python3 scripts/dump.py          # REST API -> raw/
python3 scripts/crawl.py         # DOM renderizado -> rendered/
python3 scripts/crawl_acervo.py  # paginação do acervo, com detecção de mudança
python3 scripts/parsers/<x>.py   # cada domínio -> extracted/
python3 scripts/audit.py         # confere que nenhum link de dado ficou órfão
```

O HTML renderizado (~7 MB) **não** está versionado; `crawl.py` o regenera.

---

## ⚠️ Defeitos encontrados no site de origem

Estes problemas são **do site original**, não da extração. Os dados foram copiados fielmente;
nada foi "consertado" por adivinhação.

**1. `programas-eleitorais-capitais.csv` — a coluna `municipio` não corresponde ao candidato.**
Na tabela do post original, os municípios estão rotacionados em relação aos candidatos.
Verificado: Eduardo Paes (Rio) aparece como Florianópolis; Rafael Greca (Curitiba) aparece como
Vitória; Elson Manoel Pereira (Florianópolis) aparece como Aracaju. O deslocamento parece ser de
7 blocos, mas como os blocos têm tamanhos diferentes não é seguro corrigi-lo automaticamente.
**Não use a coluna `municipio` desse arquivo sem revisão manual.** Os outros campos (candidato,
partido, propostas) estão corretos.

**2. Homepage: dois cards apontam para o mesmo dashboard do Power BI.**
Existe **uma única** URL de Power BI no site. Ela é usada tanto pelo card
"Eleições Rio e São Paulo 2024" (correto) quanto pelo card "Textos de discussão do Doxa"
(quase certamente um link errado — deveria apontar para `/textos-para-discussao/`).

**3. Páginas mortas.** `/teses-e-dissertacoes/` e `/pesquisas-realizadas/` renderizam vazias,
mesmo com JavaScript: não têm conteúdo nem em `post_content` nem em Elementor. As teses de fato
vivem em `/pagina-pesquisas/`.

**4. Seis PDFs publicados não são linkados por nenhuma página viva** — provavelmente perderam a
página que os referenciava. Listados em `dados/fontes-externas.yaml` → `pdfs_publicados_sem_pagina`.

**5. Link quebrado na origem.** Três teses apontam para
`https://iesp.uerj.br/publicacoes/teses-e-dissertacoes/teses-ciencia-politica/`, que hoje dá 404.
O link foi preservado como está na fonte.

---

## Lacunas (dados que o site simplesmente não tem)

- **Lattes e e-mail dos membros da equipe**: a página `/institucional/` não os publica. Os únicos
  4 links de Lattes do site estão em `publicacoes-academicas.yaml`.
- **Instagram e Twitter/X**: o site só tem YouTube.
- 17 das 61 pesquisas não têm link para o texto completo; 4 pesquisas concluídas não nomeiam um
  autor único (só "Equipe:").
- 81 dos 95 itens do acervo têm `estado` vazio — a taxonomia `estado` do WordPress só tem o
  termo "RJ".

---

## Relação com `data/` (o site Hugo)

Esta pasta **não altera** nada em `data/`. É a matéria-prima; a migração é um passo separado.
Ver `RELATORIO.md` para a comparação item a item e para os três placeholders que já podem ser
substituídos por valores reais.
