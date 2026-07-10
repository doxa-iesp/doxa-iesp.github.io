# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Sobre o projeto

Site do DOXA (Laboratório de Estudos Eleitorais, IESP-UERJ), reconstruído do WordPress para um
site estático em **Astro 7**. Mantido por estagiários do grupo de pesquisa, não por
desenvolvedores — essa é a restrição que governa as decisões de arquitetura.

**Idioma:** conteúdo, comentários, nomes de campo e commits em pt-BR. Mantenha.

## Comandos

```bash
npm ci            # instalação determinística (use isto, não `npm install`)
npm run dev       # http://localhost:4321/DOXA/
npm run validar   # valida os YAML de conteúdo (roda sozinho antes do build)
npm run build     # validar + astro build -> dist/
npm run check     # validar + astro check (tipos)
npm run preview   # serve dist/
```

`npm run build` = `node scripts/validar-dados.mjs && astro build`. **Não remova o validador**
(veja "Armadilhas" abaixo).

Deploy: push em `main` → `.github/workflows/deploy.yml` → GitHub Pages.
PRs rodam `.github/workflows/pr.yml` (build + `astro check` + artefato `site-dist`).

## Arquitetura

Separação dura entre **o que o estagiário edita** e **o que o desenvolvedor edita**.

```
src/
  content.config.ts   ← schemas Zod. O contrato. Mudança aqui quebra conteúdo.
  data/*.yaml         ← EDITÁVEL: listas (publicações, mídia, seminários, acervo, mapas…)
  content/
    equipe/*.yaml     ← EDITÁVEL: um arquivo por pessoa
    eventos/*.md      ← EDITÁVEL: um arquivo por evento
    paginas/*.md      ← EDITÁVEL: a prosa de cada página
  components/ layouts/ pages/ styles/ lib/   ← código
public/               ← imagens, fontes, PDFs (PRECISA estar versionado)
extracao/             ← extração completa do WordPress antigo. Fonte de verdade dos dados.
scripts/              ← conversor de conteúdo e validador de dados
```

### Coleções

Duas formas de carregar, escolhidas por ergonomia de edição:

- `glob()` — **um arquivo por entrada** (`equipe`, `eventos`, `paginas`). Adicionar = criar
  arquivo. Sem indentação de lista para errar, sem conflito de merge.
- `file()` + `listaYaml()` — **um YAML com uma lista** (publicações, mídia, …). O helper
  `listaYaml` em `content.config.ts` gera o `id` de cada item a partir do título, para que ninguém
  precise escrever `id:` à mão. O `id` só aparece em mensagens de erro; não vira URL.

### Base path

O site é publicado em `https://felipelamarca.com/DOXA/`. **Todo link interno passa por `url()`**
de [src/lib/url.ts](src/lib/url.ts). `href="/acervo/"` cru dá 404 em produção.

Para migrar a `www.lab-doxa.org.br`: trocar `site`, remover `base` em
[astro.config.mjs](astro.config.mjs) e criar `public/CNAME`. O `CNAME` da raiz do repo **não** é
publicado — só `public/` entra no build.

## Armadilhas conhecidas

**1. O loader `file()` do Astro engole erros de YAML.** Se um `src/data/*.yaml` estiver
mal-indentado, o Astro imprime `[ERROR] [file-loader] Error reading data`, **sai com código 0** e
publica a coleção **vazia**. Localmente isso se esconde atrás de `node_modules/.astro/data-store.json`;
num build frio (o do CI) a página vai ao ar sem nenhum item.

É por isso que existe [scripts/validar-dados.mjs](scripts/validar-dados.mjs), que roda antes do
build e falha com código 1. E por isso o `deploy.yml` tem uma trava que reprova se
`[file-loader] Error` aparecer no log — com `set -o pipefail`, sem o qual o `tee` devolveria 0.
Para reproduzir o bug original: `rm -rf dist .astro node_modules/.astro && npx astro build`.

**2. `public/` não é saída de build.** No Hugo era; no Astro é a pasta de assets de origem e
**precisa estar versionada**. O `.gitignore` tem um comentário avisando.

**2b. O `.gitignore` já foi um template de Python.** A regra `lib/` (sem âncora) casava com
`src/lib/`, então `url.ts` e `navegacao.ts` nunca chegaram ao repositório: o build passava no
disco e quebrava no CI com `[UNRESOLVED_IMPORT] Could not resolve '../lib/url'`. As regras agora
são ancoradas na raiz (`/node_modules/`, `/dist/`). Antes de confiar num build, teste **o que está
no commit**, não o que está no disco:

```bash
git archive --format=tar HEAD | tar -x -C /tmp/t && cd /tmp/t && npm ci && npm run build
```

**3. Defeito na fonte: `programas-eleitorais-capitais.csv`.** A coluna `municipio` está
rotacionada em relação aos candidatos (Eduardo Paes aparece como Florianópolis). Documentado em
[extracao/README.md](extracao/README.md); a página `/bancos-de-dados/` renderiza um aviso.
Não "conserte" por adivinhação.

**4. Campos opcionais são opcionais de verdade.** 17 das 61 pesquisas não têm link; 8 dos 70 itens
de mídia não têm URL; 1 publicação não tem ano ("no prelo"); 12 dos 16 membros não têm Lattes nem
e-mail; seminários não têm descrição nem link. Nada disso existe no site antigo. Não invente, e não
crie botões mortos.

## Regenerar o conteúdo

[scripts/converter-conteudo.py](scripts/converter-conteudo.py) reconstrói `src/content/` e
`src/data/` a partir de `extracao/dados/`. É idempotente e **sobrescreve edições manuais** —
se alguém corrigir um dado à mão, corrija também em `extracao/`, que é a fonte de verdade.

## Documentos

- [docs/DECISAO_ARQUITETURA.md](docs/DECISAO_ARQUITETURA.md) — por que Astro e não Hugo, com a
  ressalva do `file()` e como foi fechada.
- [docs/GUIA_DE_MANUTENCAO.md](docs/GUIA_DE_MANUTENCAO.md) — guia para estagiários, sem jargão.
- [docs/MUDANCAS_DE_LAYOUT.md](docs/MUDANCAS_DE_LAYOUT.md) — todo desvio do site antigo, com motivo.
- [checkpoints/](checkpoints/) — o histórico de decisões de cada etapa da reconstrução.
