# Checkpoint: Agente C — Frontend (frente 3 de 3)
Status: concluído
Última atualização: 2026-07-10

## O que foi feito

Criadas 3 páginas e 2 componentes, todos validados por `npx astro build` (passa).

### Páginas
- `src/pages/acervo.astro` → `/acervo/`
  - Prosa de `getEntry('paginas','acervo')`.
  - Bloco de acesso em destaque (`role="note"`) com: catálogo completo (`geral.catalogo_acervo`),
    formulário `.docx` (`url(geral.formulario_acervo)` — recebe o prefixo `/DOXA`), e o e-mail de
    solicitação (`mailto:${geral.email}`).
  - Os 95 itens de `getCollection('acervo')` renderizados como cards (SSG). Filtro multi-faceta
    client-side: candidato (busca em texto), ano, cargo (array), região, partido (array).
    O JS apenas **esconde** os cards que não casam (`card.hidden`), nunca remove — sem JS, todos
    os 95 aparecem. Contador "N de 95 itens" com `aria-live="polite"`; mensagem "nenhum resultado";
    `<noscript>` avisando que os filtros exigem JavaScript.
- `src/pages/mapas-de-votacao.astro` → `/mapas-de-votacao/`
  - Prosa + 273 mapas agrupados em `<details>` por ano (decrescente, o mais recente `open`) e,
    dentro, por cargo (ordem: Presidente, Governador, Senador, Deputado Federal, Deputado Estadual).
    Cada mapa é um link direto para o PDF. Verificado: 5 anos, 273 links de PDF.
- `src/pages/bancos-de-dados.astro` → `/bancos-de-dados/`
  - Prosa + os 3 bancos como cards (nome, descrição, cobertura, registros formatados em pt-BR, link).
  - O campo `aviso` do banco das Capitais é renderizado como alerta visível (`role="note"`, fundo
    terracota claro), conforme pedido.

### Componentes
- `src/components/CardAcervo.astro` — card com código, tipo_video, data/ano/região/cargo,
  candidatos (limite 4 + "e mais N"), chips de partidos, link "Assistir no Google Drive"
  (`target=_blank rel=noopener`). Emite `data-ano`, `data-cargo`, `data-regiao`, `data-partidos`,
  `data-candidatos` (todos normalizados sem acento/caixa) para o filtro.
- `src/components/FiltrosAcervo.astro` — formulário com busca por candidato + 4 selects (ano,
  cargo, região, partido) cujas facetas vêm dos próprios dados. Valores das opções normalizados
  para casar com os `data-*` dos cards.

## Decisões tomadas

1. **Filtro por selects de valor único (multi-faceta), não checkboxes.** "Multi-faceta" = várias
   dimensões combinadas em AND; cada faceta é um select "Todos" + opções. Evita 39 checkboxes de
   partido. A busca por candidato é substring normalizada (sem acento).
2. **Normalização compartilhada** (`NFD` + remoção de diacríticos + minúsculas) em três lugares —
   CardAcervo (data-attrs), FiltrosAcervo (valores das opções) e no `<script>` da página (query e
   comparação). Espelha o `slug()` de `content.config.ts`.
3. **`.card-acervo[hidden]{display:none}`** dentro do próprio componente, para o filtro sobrepor o
   `display:flex` do card (a regra de UA `[hidden]` seria vencida pela classe).
4. **Mapas majoritários (título = cargo)** ganham rótulo "Ver mapa" no link, para não repetir o
   nome do cargo que já está no cabeçalho `<h3>`.
5. **Prosa dos bancos renderizada na íntegra** + cards. Há leve sobreposição (a prosa da fonte
   ecoa os nomes dos bancos), mas a instrução pede a prosa e os cards agregam cobertura/registros/
   aviso/link.

## Pendências / bloqueios

- `npx astro check` **não foi executado**: exige instalar `@astrojs/check`+`typescript`, o que
  mexeria em `package.json` — proibido pelas regras duras. O `astro build` (que valida schemas e
  compila o TS das frontmatters/scripts) passa limpo. Revisão manual de tipos feita nos 5 arquivos.
- Nenhum bloqueio por trabalho de outro agente.

## Próximo passo sugerido

Revisão visual das 3 páginas com `npm run dev` (responsividade a 360px já conferida no código:
grids em `auto-fill/auto-fit` colapsam para 1 coluna; sem rolagem horizontal). Coletar Lattes/
e-mail da equipe segue como pendência de dados, alheia a esta frente.
