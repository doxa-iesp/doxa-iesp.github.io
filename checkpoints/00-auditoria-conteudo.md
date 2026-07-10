# Checkpoint: Fase 0 — Auditoria de conteúdo
Status: concluído
Última atualização: 2026-07-09

## O que foi feito

Auditei a pasta `extracao/` (produzida numa sessão anterior) contra a tabela de páginas da
Seção 4 do prompt mestre. A extração anterior cobria **todos os itens estruturados** (equipe,
publicações, eventos, seminários, pesquisas, acervo, na mídia, bancos de dados, mapas), mas
faltava a **prosa editorial das páginas** e os **logos de parceiros**. Ambos foram complementados
dentro de `extracao/`, sem criar estrutura paralela.

### Cobertura, página a página

| Página (Seção 4) | Itens estruturados | Prosa da página | Situação |
|---|---|---|---|
| `/` home | `homepage-institucional.yaml` (vídeo, dashboard, Vota Aí) | ✅ `paginas/inicio.md` | completo |
| `/institucional/` | `equipe.yaml` (15 membros, todos com foto) | ✅ `paginas/institucional.md` | completo |
| `/pagina-pesquisas/` | `pesquisas.yaml` (61) | ✅ `paginas/pagina-pesquisas.md` | completo |
| `/pesquisa-covid/` | `pesquisa-covid.yaml` (16) | ✅ `paginas/pesquisa-covid.md` | completo |
| `/acervo/` | `acervo.yaml` (95) + `acervo-catalogo-mestre.csv` (2.034) | ✅ `paginas/acervo.md` | completo |
| `/mapas-de-votacao/` | `mapas-votacao.csv` (273) | ✅ `paginas/mapas-de-votacao.md` | completo |
| `/bancos-de-dados/` | `bancos-de-dados.yaml` (3) + 2 CSVs (821 registros) | ✅ `paginas/bancos-de-dados.md` | completo |
| `/publicacoes-academicas/` | `publicacoes-academicas.yaml` (34 + 4 Lattes) | ✅ via `paginas/publicacoes.md` | completo |
| `/analises-de-conjuntura-eleitoral/` | `analises-conjuntura.yaml` (28) | ✅ via `paginas/publicacoes.md` | completo |
| `/textos-para-discussao-2/` | `textos-discussao.yaml` (2) | ✅ `paginas/textos-para-discussao-2.md` | completo |
| `/eventos/` | `eventos-seminarios.yaml` → `eventos` (5) | ⚠️ página sem prosa na origem | completo |
| `/seminarios/` | `eventos-seminarios.yaml` → `seminarios` (36) | ✅ `paginas/seminarios.md` | ⚠️ ver lacuna 1 |
| `/na-midia/` | `na-midia.yaml` (70) | ✅ `paginas/na-midia.md` | completo |

## O que foi complementado nesta fase

1. **`extracao/dados/paginas/*.md` — 12 arquivos.** Prosa editorial de cada página (títulos de
   seção + parágrafos), extraída do DOM renderizado. O parser (`scripts/parsers/paginas.py`)
   ignora tudo que está dentro de uma listagem JetEngine, para não duplicar o que já está
   estruturado nos YAML/CSV.
2. **`extracao/dados/parceiros.yaml` + `extracao/assets/parceiros/*.png` — 8 logos**
   (CAPES, CNPq, FAPERJ, FINEP, IBOPE, IESP-UERJ, UERJ, VOX). Baixados, todos HTTP 200.

Nenhuma re-raspagem do site foi necessária: o DOM renderizado das 32 páginas e o dump da REST API
já estavam disponíveis da sessão anterior.

## Decisões tomadas

- **`/publicacoes-academicas/` e `/analises-de-conjuntura-eleitoral/` não geram arquivo de prosa
  próprio.** São listagens puras; o texto introdutório das duas vive em `/publicacoes/`. Extrair
  seus parágrafos duplicaria os 34 + 28 registros já estruturados.
- **A prosa institucional foi mantida em `paginas/institucional.md`**, embora a Seção 4.1 mande
  movê-la para a home. Motivo: `extracao/` é o registro fiel do site antigo; o remanejamento é uma
  decisão de arquitetura de conteúdo, aplicada pelo Agente A, não uma reescrita da fonte.

## Lacunas remanescentes (com tratamento sugerido)

1. **Seminários não têm descrição, link nem embed.** A Seção 4 pede esses campos, mas a página
   `/seminarios/` do site antigo só publica *apresentador (instituição) – "título". [data]*.
   Nenhum dos 36 seminários tem link ou vídeo.
   → *Tratamento:* o schema deve tornar `description`, `url` e `embed` opcionais. Não inventar.

2. **Lattes e e-mail dos membros da equipe não existem no site antigo.** Os únicos 4 links de
   Lattes do site estão em `publicacoes-academicas.yaml` (Meireles, Guarnieri, Schaefer,
   Figueiredo).
   → *Tratamento:* campos opcionais no schema; coleta manual pelo time do DOXA.

3. **`programas-eleitorais-capitais.csv` tem a coluna `municipio` corrompida na origem**
   (rotacionada em relação aos candidatos — Eduardo Paes aparece como Florianópolis). Documentado
   em `extracao/README.md`.
   → *Tratamento:* não publicar essa coluna no site novo até revisão manual.

4. **17 das 61 pesquisas não têm link** para o texto completo, e 4 pesquisas concluídas não têm
   autor único (só "Equipe:"). Fiel à origem.
   → *Tratamento:* campos opcionais.

5. **Acesso ao acervo depende de e-mail.** A página `/acervo/` informa que, para ver os vídeos, é
   preciso enviar `acervo-doxa@iesp.uerj.br` com um formulário (`.docx`, já salvo em
   `extracao/bruto/datasets/`).
   → *Tratamento:* o site novo deve manter esse fluxo explícito na página do acervo.

6. **6 PDFs publicados não são linkados por nenhuma página viva** — listados em
   `extracao/dados/fontes-externas.yaml`.
   → *Tratamento:* decisão editorial do DOXA; não migrar por padrão.

## Próximo passo sugerido

Fase 1 — decisão de arquitetura (`docs/DECISAO_ARQUITETURA.md`). O schema de conteúdo precisa
tornar opcionais os campos das lacunas 1, 2 e 4, senão a validação vai reprovar dados verdadeiros.
