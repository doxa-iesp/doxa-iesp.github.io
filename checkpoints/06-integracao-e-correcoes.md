# Checkpoint: Integração e correções (orquestrador)
Status: concluído
Última atualização: 2026-07-10

## O que foi feito

Integração das quatro frentes (B, C1, C2, C3), verificação independente e correção dos problemas
que a verificação encontrou. **Não confiei nos relatos dos agentes**: refiz as medições.

### Verificação independente do site gerado

- `npm run build` limpo: **14 páginas**.
- `npx astro check`: **0 erros, 0 avisos** (30 arquivos).
- **0** links internos crus (`href="/..."` sem o prefixo `/DOXA`) no HTML gerado.
- **0** imagens sem `alt`; **0** cores hex fora dos tokens.
- Contagens conferidas no HTML de `dist/`, descontando os 17 `<li>` do menu:
  acervo 95 · pesquisas 61 · mídia 70 · publicações 34 · análises 28 · seminários 36 ·
  mapas 273 · eventos 5 · equipe 16. **Todas batem com os dados.**
- Playwright em 4 páginas: **0 erros de JavaScript**, **0 rolagem horizontal** em 360px.

## Correções aplicadas

1. **`astro check` nunca tinha rodado.** Os três agentes de frontend não podiam instalar
   dependências. Adicionei `@astrojs/check` e `typescript` a `devDependencies` e simplifiquei o
   `pr.yml` (o agente B tinha deixado um `npm install --no-save` com um TODO honesto).
   A checagem revelou **2 erros de tipo reais**, corrigidos:
   - `parser` do loader com tipo de retorno errado (`Record<string, unknown>` →
     `Record<string, Record<string, unknown>>`);
   - import de efeito colateral de `@fontsource-variable/montserrat` sem declaração de tipo
     (criado `src/env.d.ts`).
   Migrei também `import { z } from 'astro:content'` (deprecado) para `astro:schema`.

2. **Redundância na home:** o `<h1>` nomeia o laboratório e logo abaixo vinha um
   `## Sobre o DOXA`. O heading é removido pelo conversor.

3. **🔴 FALHA SILENCIOSA — o problema mais grave do projeto.**
   Encontrada pelo Agente D e **confirmada por mim** com um build frio.

   O loader `file()` do Astro engole exceções do parser de YAML. Com `src/data/midia.yaml`
   mal-indentado:

   ```
   rm -rf dist .astro node_modules/.astro && npx astro build
   → [ERROR] [file-loader] Error reading data from src/data/midia.yaml
   → exit 0
   → /na-midia/ publicada com 0 das 70 matérias
   ```

   Localmente isso passava despercebido porque `node_modules/.astro/data-store.json` guardava a
   versão boa dos dados; **no CI, que começa do zero, o site iria ao ar mutilado**. É exatamente a
   falha silenciosa que motivou trocar o Hugo pelo Astro — ou seja, a justificativa da Fase 1
   estava furada no formato que mais gente vai editar.

   Correção em duas travas:
   - **`scripts/validar-dados.mjs`**, rodado por `npm run build` antes do `astro build`. Falha com
     código 1, aponta arquivo/linha/coluna, em português, e recusa lista que encolheu demais
     (item apagado sem querer). Verificado: `exit 1`, `dist/` **não** é gerado.
   - **Trava no `deploy.yml`**: reprova o deploy se `[file-loader] Error` aparecer no log.
     Usa `set -o pipefail` — sem isso o `tee` devolveria 0 e a trava seria decorativa
     (medido: `exit 1` com pipefail, `exit 0` sem).

   `docs/DECISAO_ARQUITETURA.md` e `docs/GUIA_DE_MANUTENCAO.md` foram corrigidos: o guia dizia ao
   estagiário que o PR "pode ficar verde" nesse caso. Não fica mais.

## Decisões tomadas

- **O Hugo foi preservado em `legacy-hugo/`**, não apagado. Pode ser removido quando o time
  aprovar o site novo.
- **`CNAME` na raiz mantido.** Não é publicado pelo Astro (só `public/` entra no build) e o deploy
  atual usa `base: '/DOXA'`. Instruções de migração para o domínio próprio estão no
  `astro.config.mjs` e no resumo executivo.
- A trava do CI é redundante com o validador. Mantida assim de propósito: um bug que publica o
  site sem conteúdo merece cinto e suspensório.

## Pendências / bloqueios

- **`public/` ainda não está versionado** (`git status` mostra `?? public/`). Precisa de
  `git add public/` antes do primeiro push, senão o deploy sai sem imagens e sem fontes.
  Não commitei nada porque commits não foram pedidos.
- O texto do acervo (vindo do site antigo) diz que a busca está "ainda em construção". Ela agora
  existe. É texto editável — decisão do time do DOXA.
- Lattes/e-mail de 12 dos 16 membros continuam vazios: não existem no site antigo.

## Próximo passo sugerido

`docs/RESUMO_EXECUTIVO.md` e a revisão humana. Depois: `git add -A && git commit`, ativar
GitHub Pages em Settings → Pages → Source: GitHub Actions.
