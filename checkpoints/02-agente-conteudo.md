# Checkpoint: Agente A — Conteúdo & Dados
Status: concluído
Última atualização: 2026-07-10

## O que foi feito

Convertido todo o material de `extracao/dados/` para as content collections do Astro, via
**script reproduzível** `scripts/converter-conteudo.py` (idempotente: apaga e regenera
`src/content/` e `src/data/`).

| Coleção | Formato | Registros |
|---|---|---|
| `src/content/equipe/*.yaml` | um arquivo por pessoa | 16 |
| `src/content/paginas/*.md` | um arquivo por página | 12 |
| `src/content/eventos/*.md` | um arquivo por evento | 5 |
| `src/data/publicacoes.yaml` | lista | 34 |
| `src/data/analises.yaml` | lista | 28 |
| `src/data/textos-discussao.yaml` | lista | 2 |
| `src/data/midia.yaml` | lista | 70 |
| `src/data/seminarios.yaml` | lista | 36 |
| `src/data/pesquisas.yaml` | lista | 61 |
| `src/data/acervo.yaml` | lista | 95 |
| `src/data/bancos-de-dados.yaml` | lista | 3 |
| `src/data/mapas-votacao.yaml` | lista | 273 |
| `src/data/parceiros.yaml` | lista | 8 |
| `src/data/site.yaml` | objeto `geral` | — |

**Assets:** 16 fotos de equipe → `public/img/equipe/`; 8 logos → `public/img/parceiros/`;
5 imagens de evento baixadas → `public/img/eventos/`; formulário do acervo → `public/docs/`.

## Decisões tomadas

1. **A home passa a ser a apresentação institucional** (Seção 4.1). `src/content/paginas/home.md`
   recebe o texto "Sobre o DOXA" que antes vivia em `/institucional/`. A página
   `/institucional/` fica com um parágrafo curto de contexto + a equipe. Sem duplicação.
2. **Nomes de campo em português** (`titulo`, `autores`, `ano`), coerentes com quem edita.
3. **Campo ausente é omitido**, nunca preenchido com `""`. O schema decide se é opcional.
4. **Felipe Lamarca preservado.** Não está no site antigo; veio de `legacy-hugo/data/team.yaml`,
   onde foi adicionado deliberadamente. Removê-lo seria uma regressão.
5. **Lattes cruzado automaticamente.** Os 4 links de Lattes que existiam em
   `publicacoes-academicas.yaml` foram associados aos membros correspondentes por sobrenome.

## Três defeitos de dados corrigidos (a validação de schema os encontrou)

A escolha do Astro se pagou já na conversão: o build recusou dados ruins três vezes.

1. **`mapas` — 15 registros sem título.** São os mapas de eleição *majoritária*, que não têm sigla
   partidária. Em vez de afrouxar o schema, o título passou a ser derivado do cargo
   (`Governador`, `Presidente`, `Senador`), e `eleicao`/`turno` viraram campos próprios.
2. **`midia` — 2 registros sem título.** Duas matérias do *El País* têm **aspas aninhadas** no
   título (`...o comandante fala "e daí"`), e o parser da extração as truncava. Corrigido na
   fonte (`extracao/scripts/parsers/na_midia.py`): o título agora vem do texto do link.
3. **`midia` — 2 matérias faltavam por completo.** "A polarização do vírus" (Valor) e
   "Desconstruindo Mitos" (Pesquisa Fapesp) não têm link, e o parser exigia um `<a>` para
   registrar o item. Ambas recuperadas. Um link parasita numa aspa tipográfica, que gerava um
   registro falso de título `’`, foi descartado.

O `extracao/dados/na-midia.yaml` foi regenerado; a extração continua sendo a fonte de verdade.

## Pendências / bloqueios

- Nenhum bloqueio.
- Lattes/e-mail de 12 dos 16 membros continuam vazios: **não existem no site antigo**. Coleta
  manual pelo time do DOXA (ver `docs/RESUMO_EXECUTIVO.md`).

## Próximo passo sugerido

Agentes B (infra) e C (frontend), em paralelo, sobre os schemas já congelados em
`src/content.config.ts`.
