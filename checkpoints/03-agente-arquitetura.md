# Checkpoint: Agente B — Arquitetura & Infraestrutura
Status: concluído
Última atualização: 2026-07-10

## O que foi feito

Criados/reescritos os arquivos de infraestrutura (nada em `src/` foi tocado):

1. **`.github/workflows/deploy.yml`** — reescrito (era Hugo). Build e deploy no GitHub Pages a cada
   push na `main` (e `workflow_dispatch`). Caminho explícito, sem `withastro/action`:
   `actions/checkout@v4` → `actions/setup-node@v4` (`node-version: 22`, `cache: npm`) →
   `npm ci` → `npm run build` → `actions/configure-pages@v5` →
   `actions/upload-pages-artifact@v3` (`path: ./dist`) → job `deploy` com `actions/deploy-pages@v4`.
   `permissions: contents:read, pages:write, id-token:write`; `concurrency: group "pages"`,
   `cancel-in-progress: false`.

2. **`.github/workflows/pr.yml`** — novo. Roda em `pull_request`: `npm ci` → `npm run build`
   (valida os schemas Zod — é aqui que um YAML inválido reprova o PR) →
   `actions/upload-artifact@v4` publicando `dist/` (`if-no-files-found: error`) →
   `astro check`.

3. **`.gitignore`** — acrescentadas as entradas do Astro/Node (`node_modules/`, `dist/`, `.astro/`,
   `.DS_Store`) e **removido `public/` da lista de ignorados** (ver "Decisões", item 1). O bloco
   grande do Python foi preservado.

4. **`README.md`** — reescrito para Astro: o que é, como rodar (`npm ci && npm run dev`), onde fica o
   conteúdo editável (tabela `src/data/` e `src/content/` + assets em `public/`), como publicar
   (push na `main`), fluxo de PR, e links para `docs/GUIA_DE_MANUTENCAO.md` e
   `docs/DECISAO_ARQUITETURA.md`. Mantido o que ainda era verdade (identidade do lab, URL, nota do
   domínio próprio).

## Verificação

- `python3 -c "import yaml; yaml.safe_load(open(...))"` nos dois workflows → **OK**.
- `npm run build` → **passa** (2 páginas hoje: `/` e `/institucional/`; as demais são do Agente C,
  em paralelo). `legacy-hugo/` e `extracao/` **não** são processados pelo Astro (já excluídos em
  `tsconfig.json`); o build não os toca. Nada a ajustar em `.gitignore`/`tsconfig.json` por causa
  deles (tarefa 5 satisfeita sem mudança).

## Decisões tomadas

1. **`public/` deixou de ser ignorado — correção de bug de infra que quebraria o deploy.**
   O `.gitignore` herdado do Hugo ignorava `public/` porque lá era a *saída* de build. No Astro,
   `public/` é a pasta de **assets de origem** (imagens da equipe, fontes, PDFs). Constatei que
   **0 arquivos de `public/` estavam versionados** (`git ls-files public/` = vazio; `git check-ignore
   public/` casava com `.gitignore:2`). Se isso fosse para produção, o CI publicaria o site **sem
   nenhuma imagem/fonte**. Removi `public/` do ignore e deixei um comentário explicando. Mantive
   `resources/` e `.hugo_build.lock` ignorados (cache do Hugo, inofensivo). Isso respeita "não apagar
   o que já existe" no sentido do bloco Python; a linha do Hugo era um defeito ativo.

2. **`astro check` no PR precisou instalar `@astrojs/check` + `typescript` no próprio step.**
   Esses dois pacotes **não estão em `package.json`** (que não posso alterar nesta fase). Sem eles,
   `astro check` imprime um aviso e **sai com código 0** — verifiquei: `astro check exit code (deps
   missing) = 0`. Ou seja, o step passaria sempre, sem checar nada, tornando a verificação de tipos
   pura encenação. Para o step ser real, o `pr.yml` roda `npm install --no-save @astrojs/check
   typescript` antes do `npx astro check`. O `--no-save` não altera `package.json` nem o
   `package-lock.json` versionado; é instalação efêmera só no runner do CI.

3. **`node-version: 22`** conforme pedido (satisfaz `engines.node >=20` do `package.json`).

4. **PR: `astro check` roda depois do upload do artefato.** Assim, se o build passar mas o
   type-check falhar, o revisor ainda consegue baixar o `dist/` gerado, e o PR fica vermelho pelo
   `astro check`. YAML inválido em coleção já reprova antes, no `npm run build`.

## Pendências / bloqueios

- **AÇÃO NECESSÁRIA ANTES DO PRÓXIMO PUSH:** `public/` agora está desbloqueado, mas os arquivos ainda
  não foram commitados. Rodar `git add public/ && git commit` (junto do restante). Sem isso, o
  primeiro deploy sai sem imagens. Não commitei porque a tarefa não pediu commit.
- **Recomendação ao desenvolvedor:** mover `@astrojs/check` e `typescript` para `devDependencies` em
  `package.json` e simplificar o step de `astro check` no `pr.yml` (remover o `npm install
  --no-save`). Deixei um `TODO` no arquivo. Não fiz porque `package.json` é intocável nesta fase.
- `CNAME` na raiz do repo é resquício do Hugo e **não** é publicado pelo Astro (só `public/` entra).
  O deploy atual usa `base: '/DOXA'` em `felipelamarca.com`, então nenhum CNAME é necessário agora.
  Ao migrar para o domínio próprio, criar `public/CNAME` (ver `astro.config.mjs` e
  `DECISAO_ARQUITETURA.md`). Não removi o `CNAME` da raiz para não sair do meu escopo.

## Próximo passo sugerido

- Ativar o GitHub Pages do repositório em **Settings → Pages → Source: GitHub Actions** (o
  `deploy.yml` só publica depois disso).
- Commitar `public/` (ver pendência) e abrir um PR de teste para confirmar que o `pr.yml` fica verde
  no caminho feliz e vermelho ao introduzir um valor inválido num YAML de `src/data/`.
