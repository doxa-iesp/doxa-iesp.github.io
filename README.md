# DOXA — Site do Laboratório

Site estático do **DOXA — Laboratório de Estudos Eleitorais, de Comunicação Política e Opinião
Pública** (IESP-UERJ), construído com [Astro](https://astro.build/) e publicado via GitHub Pages.

**URL:** https://doxa-iesp.github.io/ (temporária — a definitiva será www.lab-doxa.org.br)

O site foi migrado de Hugo para Astro. O motivo está em
[`docs/DECISAO_ARQUITETURA.md`](docs/DECISAO_ARQUITETURA.md): em resumo, o conteúdo é validado por
schema, então um erro de digitação num arquivo de dados **faz o build falhar de forma visível** — em
vez de publicar silenciosamente uma página quebrada.

> O site antigo em Hugo foi removido do diretório de trabalho. Ele continua recuperável pelo
> histórico do git: `git checkout 073679b -- layouts/ data/ content/ static/`.

---

## Pré-requisitos

- [Node.js](https://nodejs.org/) 20 ou superior (o CI usa a 22)
- Git

## Rodar localmente

```bash
git clone https://github.com/doxa-iesp/doxa-iesp.github.io.git
cd DOXA
npm ci        # instala as dependências a partir do package-lock.json
npm run dev   # servidor local com recarga automática
```

O site fica em `http://localhost:4321/`. Edite um arquivo de conteúdo e a página recarrega
sozinha.

Outros comandos úteis:

```bash
npm run build     # gera o site final em dist/ (valida todos os schemas)
npm run preview   # serve o que foi gerado em dist/, como ficará em produção
npm run check     # checagem de tipos (astro check)
```

---

## Onde fica o conteúdo editável

Todo o conteúdo que os estagiários editam vive em `src/data/` e `src/content/`. O código
(componentes, layouts, estilos) fica em `src/components/`, `src/layouts/` e `src/styles/` — **não é
preciso mexer nele para atualizar o site.**

| O que | Onde | Formato |
|---|---|---|
| Equipe (uma pessoa = um arquivo) | `src/content/equipe/*.yaml` | um arquivo por membro |
| Eventos | `src/content/eventos/*.md` | um arquivo por evento |
| Texto das páginas (prosa) | `src/content/paginas/*.md` | um arquivo por página |
| Publicações acadêmicas | `src/data/publicacoes.yaml` | lista |
| Análises de conjuntura | `src/data/analises.yaml` | lista |
| Textos para discussão | `src/data/textos-discussao.yaml` | lista |
| Na mídia | `src/data/midia.yaml` | lista |
| Seminários | `src/data/seminarios.yaml` | lista |
| Pesquisas | `src/data/pesquisas.yaml` | lista |
| Acervo | `src/data/acervo.yaml` | lista |
| Bancos de dados | `src/data/bancos-de-dados.yaml` | lista |
| Mapas de votação | `src/data/mapas-votacao.yaml` | lista |
| Parceiros | `src/data/parceiros.yaml` | lista |
| Contato, redes e configurações gerais | `src/data/site.yaml` | objeto |

**Imagens, fontes e PDFs** ficam em `public/` (por exemplo, fotos da equipe em
`public/img/equipe/`). O que está em `public/` é copiado como está para o site final e **precisa ser
versionado no Git.**

Os campos exatos de cada tipo de conteúdo são definidos e validados em `src/content.config.ts`. Se
você preencher um campo com um valor inválido (ou esquecer um obrigatório), o build acusa o erro
nomeando o arquivo e o campo.

Para cada tarefa comum — adicionar um membro, publicar uma publicação, incluir um evento — copie um
item já existente no arquivo correspondente de `src/data/` ou `src/content/` e edite os campos. Os
campos válidos de cada tipo estão definidos em `src/content.config.ts`.

---

## Como publicar

O deploy é automático. Qualquer push (ou merge de PR) na branch `main` dispara o GitHub Actions, que:

1. instala as dependências (`npm ci`);
2. roda `npm run build` — que **valida todos os schemas de conteúdo**;
3. publica o resultado no GitHub Pages.

Se o build falhar (por exemplo, um valor inválido num YAML), **nada é publicado** e a ação aparece
vermelha no GitHub.

### Pull requests

Ao abrir um pull request, um workflow separado roda `npm ci`, `npm run build` e `npx astro check`, e
publica o `dist/` como artefato para o revisor baixar e conferir. Assim, um erro é pego **antes** do
merge.

Os workflows ficam em `.github/workflows/` (`deploy.yml` e `pr.yml`).

---

## Estrutura do repositório

```
├── src/
│   ├── content.config.ts   # schemas (Zod) — só desenvolvedor mexe
│   ├── data/               # CONTEÚDO EDITÁVEL: listas em YAML
│   ├── content/            # CONTEÚDO EDITÁVEL: equipe, eventos e prosa das páginas
│   ├── components/         # componentes (código)
│   ├── layouts/            # layouts (código)
│   ├── pages/              # rotas do site (código)
│   ├── lib/                # utilitários (ex.: url.ts, navegacao.ts)
│   └── styles/             # tokens de cor/tipografia e CSS global
├── public/                 # imagens, fontes, PDFs, robots.txt (versionados)
├── docs/                   # documentação do projeto
├── astro.config.mjs        # configuração do Astro (base path, sitemap)
├── package.json
└── .github/workflows/      # CI/CD (deploy.yml, pr.yml)
```

---

## Documentação

- [`docs/DECISAO_ARQUITETURA.md`](docs/DECISAO_ARQUITETURA.md) — por que Astro, tokens de cor,
  estrutura de pastas e fluxo de publicação.

## Domínio próprio (futuro)

Para migrar de `doxa-iesp.github.io` para `www.lab-doxa.org.br`, siga o comentário no topo de
`astro.config.mjs`: trocar `site`, remover `base`, criar `public/CNAME` com o domínio e apontar o
DNS. O `CNAME` na raiz do repositório **não** é publicado — só o conteúdo de `public/` entra no
build.
