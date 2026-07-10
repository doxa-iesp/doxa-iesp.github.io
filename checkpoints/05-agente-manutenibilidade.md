# Checkpoint: Agente D — Manutenibilidade
Status: concluído
Última atualização: 2026-07-10

## O que foi feito

### Parte 1 — Tarefas de manutenção executadas de verdade (com `npx astro build` após cada uma)

Todas as 6 tarefas do "caminho feliz" **funcionaram** e o item apareceu no `dist/` na seção certa;
depois cada mudança foi desfeita:

| # | Tarefa | Onde conferi | Resultado |
|---|---|---|---|
| 1 | Novo membro (`src/content/equipe/*.yaml`) | `dist/institucional/index.html` | Apareceu no bloco "Alunos de Pós-graduação" (categoria `aluno`). Sem `foto`, o site mostrou as iniciais (placeholder), sem quebrar. |
| 2 | Nova publicação (`src/data/publicacoes.yaml`) | `dist/publicacoes/academicas/index.html` | Apareceu no bloco "Artigos em Revista Científica" (`tipo: artigo`). |
| 3 | Novo evento (`src/content/eventos/*.md`) | `dist/eventos/index.html` | Apareceu com a data formatada "15 de junho de 2025". |
| 4 | Item "Na Mídia" (`src/data/midia.yaml`) | `dist/na-midia/index.html` | Apareceu no bloco "Mídia Virtual" (`tipo: virtual`). |
| 5 | Texto de página (`src/content/paginas/acervo.md`) | `dist/acervo/index.html` | O texto alterado apareceu. |
| 6 | E-mail de contato (`src/data/site.yaml`) | 14 páginas do `dist/` | Trocou no rodapé de todas as páginas e na página do Acervo. |

Os 4 erros de estagiário foram provocados e as mensagens **exatas** foram copiadas para o guia
(`docs/GUIA_DE_MANUTENCAO.md`, Seção 3). Ver "as 4 mensagens" no fim deste checkpoint.

### Parte 2 — `docs/GUIA_DE_MANUTENCAO.md`

Guia completo em pt-BR, linguagem não-técnica: como o site funciona; edição pela web do GitHub
(com o que é um PR); a rede de segurança (verde/vermelho, aba Checks, as 4 mensagens reais e o que
cada uma significa); 10 receitas copiáveis (equipe +foto, publicação, texto para discussão, análise
de conjuntura, evento, seminário, mídia, texto de página, contato, e remover membro); a tabela de
valores permitidos (categoria/tipo publicação/tipo mídia/status pesquisa, copiada do schema); o que
NÃO mexer; e como rodar localmente (opcional). Sem prometer preview público — só o artefato
`site-dist` da aba Checks.

### Verificação final
- `npx astro build` (com cache limpo) → **14 páginas**, sem erros.
- `git status --short src/` → apenas `?? src/` (estado inicial preservado; `src/` é 100% untracked).
- Contagens de volta ao original: equipe 16, eventos 5, páginas 12. Nenhum arquivo `teste-*`/`erro-*`
  deixado para trás; `publicacoes.yaml`, `midia.yaml`, `site.yaml` e `acervo.md` idênticos aos
  backups.

## Decisões tomadas

1. **Testei o build sem o cache do Astro** (`node_modules/.astro/data-store.json`) para simular o CI
   de verdade. Com o cache presente, um YAML de lista quebrado passa "sem efeito visível" porque o
   Astro reaproveita a última versão boa; sem cache (como no CI, que roda `npm ci` do zero) o efeito
   real aparece. Essa distinção é a base do ponto de fricção nº 1 abaixo.
2. **Não mexi em `src/content.config.ts` nem em nenhum arquivo do bloco "não mexer".** Os pontos de
   fricção viram recomendação aos Agentes A/B, não correção minha.
3. **Guia orientado à edição pela web do GitHub** (não ao terminal), porque o público são estagiários
   sem Git. O modo local ficou como apêndice opcional.

## Pendências / bloqueios

- **Nenhum bloqueio para o conteúdo/guia.** Guia e checkpoint entregues; build verde; `src/` limpo.
- **1 pendência de infra herdada de outro agente (não é minha):** o ponto de fricção nº 1 (YAML de
  lista quebrado não reprova o build) precisa de correção do Agente B (guarda no CI) e/ou A (schema).
- **Artefatos de sincronização (iCloud) — ver ponto de fricção nº 5.** Durante a sessão, apareceram
  28 arquivos-cópia com sufixo `" 2"` em `src/content/` (o repositório mora em `~/Desktop`, que é
  sincronizado pelo iCloud). Eles duplicavam **todo membro da equipe** e várias páginas no build.
  Movi os 28 para uma quarentena reversível fora do repositório
  (`.../scratchpad/quarentena-conflict-copies/`), restaurando o build para 16/5/12. **Decisão do
  time:** apagar de vez esses 28 arquivos e, de preferência, tirar o repositório do Desktop/iCloud.

## Pontos de fricção encontrados (com recomendação para cada)

1. **[CRÍTICO — falha silenciosa] Erro de indentação num arquivo de LISTA (`src/data/*.yaml`) NÃO
   reprova o build.** Testado com `publicacoes.yaml`: num build limpo (sem cache, = CI), a saída é
   `[ERROR] [file-loader] Error reading data from src/data/publicacoes.yaml` **mas o build termina
   com código 0 e o site é publicado** — com a coleção inteira **vazia** (as 34 publicações somem;
   a página caiu de ~26 KB para ~9,6 KB). É exatamente a falha silenciosa que a escolha do Astro
   prometia eliminar; o buraco existe só para as coleções carregadas via `listaYaml`/`file()` e
   consumidas por `getCollection()`.
   → **Recomendação (Agente B, mais simples e robusta):** no `pr.yml` e no `deploy.yml`, capturar a
   saída do build e **falhar o job** se aparecer `Error reading data`. Ex.: rodar
   `npm run build 2>&1 | tee build.log` e depois
   `grep -q "\[file-loader\] Error reading data" build.log && exit 1`.
   → **Recomendação alternativa (Agente A, no schema):** trocar o `file()` das listas por um loader
   que **relance como erro fatal** (`AstroError`) quando `YAML.parse` falhar, em vez de deixar o
   `file()` engolir a exceção. Enquanto isso não existir, o guia orienta o estagiário a **conferir o
   `site-dist`** ao editar arquivos de lista (mitigação de processo, não de código).

2. **[médio] `site.yaml` com indentação quebrada reprova o build (bom), mas com mensagem feia.**
   Em vez de um erro de schema legível, sai `[ERROR] [file-loader] Error reading data from
   src/data/site.yaml` seguido de `TypeError: Cannot read properties of undefined (reading 'data')`
   ao renderizar `/acervo`. O PR fica vermelho (a rede de segurança funciona), mas a causa não é
   óbvia. → **Recomendação (Agente A/B):** idealmente o mesmo tratamento do item 1; no mínimo,
   documentar (feito no guia). Prioridade menor porque **falha** de fato.

3. **[baixo] A localização do erro em arquivos de lista aponta `:0:0`.** Ex.:
   `Location: src/data/publicacoes.yaml:0:0` — não indica a linha. O build identifica o item errado
   pelo "slug" derivado do título (ex.: `publicacoes → publicacao-de-teste-sem-tipo`), o que ajuda,
   mas o `:0:0` confunde. → **Recomendação:** aceitável; já expliquei no guia que o estagiário deve
   procurar o item pelo título, não pela linha.

4. **[baixo] Campos `revista` vs `editora` em `publicacoes.yaml` são ambíguos.** Ambos são opcionais
   e nada obriga a usar `revista` com `tipo: artigo` e `editora` com `livro/capitulo`; um estagiário
   pode preencher o campo errado sem que o build reclame. → **Recomendação (Agente A):** opcional —
   um comentário no topo do arquivo, ou renomear para algo mais claro. Já orientei no guia.

5. **[médio — ambiente] Repositório em pasta sincronizada pelo iCloud gera cópias-conflito.** Como o
   projeto está em `~/Desktop` (sincronizado), operações de escrita durante o build/edição criaram
   28 arquivos `"… 2.yaml"`/`"… 2.md"` em `src/content/`. O glob do Astro (`**/*.yaml`) casa esses
   nomes e passa a renderizar **membros e páginas duplicados** — sem nenhum erro de build.
   → **Recomendação (time/desenvolvedor):** mover o repositório para fora do Desktop/iCloud (ou
   excluí-lo da sincronização). Afeta principalmente o desenvolvimento local; quem edita pela web do
   GitHub não sofre com isso. Os 28 arquivos foram postos em quarentena reversível (ver Pendências).

## Próximo passo sugerido

- **Agente B:** adicionar a guarda de CI do ponto nº 1 (uma linha de `grep` que reprova o job em
  `Error reading data`). É a correção de maior retorno e fecha a única falha silenciosa que restou.
- **Time do DOXA:** decidir sobre os 28 arquivos-cópia do iCloud (apagar) e sobre tirar o repo do
  Desktop; depois, abrir 1 PR de teste editando um arquivo de lista para confirmar, na prática, que
  o guia e a rede de segurança funcionam ponta a ponta.
