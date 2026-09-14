# DOXA — Site do Laboratório

Site estático do **DOXA — Laboratório de Estudos Eleitorais, de Comunicação Política e Opinião
Pública** (IESP-UERJ), construído com [Astro](https://astro.build/) e publicado via GitHub Pages.

**URL:** https://lab-doxa.org.br/

O domínio `lab-doxa.org.br` era do site antigo, em WordPress, que **saiu do ar em 2026-09**. Nada
neste site depende mais dele — ver [Domínio e endereços antigos](#domínio-e-endereços-antigos).

O site foi migrado de Hugo para Astro. O motivo está em
[`docs/DECISAO_ARQUITETURA.md`](docs/DECISAO_ARQUITETURA.md): em resumo, o conteúdo é validado por
schema, então um erro de digitação num arquivo de dados **faz o build falhar de forma visível** — em
vez de publicar silenciosamente uma página quebrada.

> O site antigo em Hugo foi removido do diretório de trabalho. Ele continua recuperável pelo
> histórico do git: `git checkout 073679b -- layouts/ data/ content/ static/`.

---

## Pré-requisitos

- [Node.js](https://nodejs.org/) 22.12 ou superior (o Astro 7 não roda em versão mais velha; o CI
  usa a versão de `.nvmrc`)
- Git

## Rodar localmente

```bash
git clone https://github.com/doxa-iesp/doxa-iesp.github.io.git
cd doxa-iesp.github.io
npm ci        # instala as dependências a partir do package-lock.json
npm run dev   # servidor local com recarga automática
```

O site fica em `http://localhost:4321/`. Edite um arquivo de conteúdo e a página recarrega
sozinha.

Outros comandos úteis:

```bash
npm run validar   # confere só os arquivos de conteúdo (rápido; roda sozinho antes do build)
npm run build     # gera o site final em dist/ (valida o conteúdo e todos os schemas)
npm run preview   # serve o que foi gerado em dist/, como ficará em produção
npm run check     # validar + checagem de tipos (astro check)
npm run verificar-links  # depois do build: confere que todo link e arquivo interno existe
```

---

## Onde fica o conteúdo editável

Todo o conteúdo que os estagiários editam vive em `src/data/` e `src/content/` — **é ali, e só
ali, que se corrige ou acrescenta conteúdo**. A pasta `extracao/` é o registro histórico da
migração do site antigo e não alimenta o site. O código (componentes, layouts, estilos) fica em
`src/components/`, `src/layouts/` e `src/styles/` — **não é preciso mexer nele para atualizar o
site.**

| O que | Onde | Formato |
|---|---|---|
| Equipe (uma pessoa = um arquivo) | `src/content/equipe/*.yaml` | um arquivo por membro |
| Eventos | `src/content/eventos/*.md` | um arquivo por evento |
| Projetos (Vota Aí, Pesquisa COVID…) | `src/content/projetos/*.md` | um arquivo por projeto |
| Destaques da página inicial | `src/content/destaques/*.md` | um arquivo por destaque |
| Texto das páginas (prosa) | `src/content/paginas/*.md` | um arquivo por página |
| Publicações acadêmicas | `src/data/publicacoes.yaml` | lista |
| Análises de conjuntura | `src/data/analises.yaml` | lista |
| Textos para discussão | `src/data/textos-discussao.yaml` | lista |
| Na mídia | `src/data/midia.yaml` | lista |
| Seminários | `src/data/seminarios.yaml` | lista |
| Pesquisas | `src/data/pesquisas.yaml` | lista |
| Acervo | `src/data/acervo.yaml` | lista |
| Bancos de dados | `src/data/bancos-de-dados.yaml` | lista |
| Mapas de votação (os PDFs ficam no Google Drive do DOXA) | `src/data/mapas-votacao.yaml` | lista |
| Parceiros | `src/data/parceiros.yaml` | lista |
| Contato, redes e configurações gerais | `src/data/site.yaml` | objeto |

**Imagens, fontes e PDFs** ficam em `public/` (por exemplo, fotos da equipe em
`public/img/equipe/`). O que está em `public/` é copiado como está para o site final e **precisa ser
versionado no Git.**

Os campos exatos de cada tipo de conteúdo são definidos e validados em `src/content.config.ts`. Se
você preencher um campo com um valor inválido (ou esquecer um obrigatório), o build acusa o erro
nomeando o arquivo e o campo.

Para cada tarefa comum — adicionar um membro, publicar uma publicação, incluir um evento — há uma
receita passo a passo em [`docs/GUIA_DE_MANUTENCAO.md`](docs/GUIA_DE_MANUTENCAO.md). O atalho é
copiar um item já existente no arquivo correspondente e editar os campos. Os campos válidos de cada
tipo estão definidos em `src/content.config.ts`.

---

## Como publicar

O deploy é automático. Qualquer push (ou merge de PR) na branch `main` dispara o GitHub Actions, que:

1. instala as dependências (`npm ci`);
2. roda `npm run build` — que **valida todos os schemas de conteúdo**;
3. roda `npm run verificar-links` — todo link e arquivo interno do site montado precisa existir;
4. publica o resultado no GitHub Pages.

Se o build falhar (por exemplo, um valor inválido num YAML), **nada é publicado** e a ação aparece
vermelha no GitHub.

### Pull requests

Ao abrir um pull request, um workflow separado roda `npm ci`, `npm run build`,
`npm run verificar-links` e `npm run check` (validador + `astro check`), e publica o `dist/` como
artefato (`site-dist`) para o revisor baixar e conferir — servido com `npx serve`, porque os caminhos
do site são absolutos. Assim, um erro é pego **antes** do merge.

### Links externos

No dia 1 de cada mês, `links-externos.yml` confere os links para fora do site (jornais, revistas,
Google Drive) e abre uma issue **"Links quebrados"** quando algum não abre. Não bloqueia o deploy. O
que fazer com a issue está no [guia de manutenção](docs/GUIA_DE_MANUTENCAO.md); os sites deixados
de fora da conferência, com o motivo, em `.github/lychee.toml`. Para rodar agora: aba **Actions** >
**Links externos** > **Run workflow**.

Os workflows ficam em `.github/workflows/` (`deploy.yml`, `pr.yml` e `links-externos.yml`).

---

## Estrutura do repositório

```
├── src/
│   ├── content.config.ts   # schemas (Zod) — só desenvolvedor mexe
│   ├── data/               # CONTEÚDO EDITÁVEL: listas em YAML
│   ├── content/            # CONTEÚDO EDITÁVEL: equipe, eventos, projetos, destaques e prosa das páginas
│   ├── components/         # componentes (código)
│   ├── layouts/            # layouts (código)
│   ├── pages/              # rotas do site (código)
│   ├── lib/                # utilitários (ex.: url.ts, navegacao.ts, rotas-antigas.mjs)
│   └── styles/             # tokens de cor/tipografia e CSS global
├── public/                 # imagens, PDFs (pdfs/), CSV e XLSX (dados/), formulários (docs/), robots.txt, CNAME (versionados)
├── extracao/               # extração do WordPress antigo — registro histórico, não alimenta o site
├── scripts/                # validador de dados, troca de links e o conversor da migração (aposentado)
├── docs/                   # documentação do projeto
├── astro.config.mjs        # configuração do Astro (domínio, base path, sitemap)
├── package.json
└── .github/                # CI/CD (workflows/deploy.yml, pr.yml, links-externos.yml) e config do lychee
```

---

## Documentação

- [`docs/GUIA_DE_MANUTENCAO.md`](docs/GUIA_DE_MANUTENCAO.md) — guia para estagiários, com uma
  receita para cada tarefa.
- [`docs/DECISAO_ARQUITETURA.md`](docs/DECISAO_ARQUITETURA.md) — por que Astro, tokens de cor,
  estrutura de pastas e fluxo de publicação.
- [`DADOS_PENDENTES.md`](DADOS_PENDENTES.md) — o que ainda falta preencher ou conferir, e por quê.
- [`CLAUDE.md`](CLAUDE.md) — arquitetura e armadilhas conhecidas, para quem mexe no código.
- [`docs/MUDANCAS_DE_LAYOUT.md`](docs/MUDANCAS_DE_LAYOUT.md) — todo desvio em relação ao site antigo,
  com o motivo.
- [`docs/RESUMO_EXECUTIVO.md`](docs/RESUMO_EXECUTIVO.md) — retrato da reconstrução em 2026-07
  (desatualizado; útil como referência de escopo).
- [`extracao/README.md`](extracao/README.md) — o que foi extraído do WordPress e os defeitos da fonte.

## Domínio e endereços antigos

**O domínio.** O site responde em `https://lab-doxa.org.br/` (o apex, sem `www`; o `www` só
redireciona). Três lugares precisam bater, e hoje batem:

1. o DNS, no registro.br — quatro registros A do apex para os IPs do GitHub Pages
   (`185.199.108.153` a `185.199.111.153`) e `www` em CNAME para `doxa-iesp.github.io`;
2. o domínio em *Settings > Pages* do repositório, com **Enforce HTTPS** ligado;
3. `site` em `astro.config.mjs` e o arquivo `public/CNAME`. O `CNAME` na raiz do repositório
   **não** seria publicado — só o conteúdo de `public/` entra no build.

**O site antigo não existe mais.** O WordPress saiu do ar e o domínio passou a servir este site.
Não há como baixar nada dele de novo: o que foi preservado está em `extracao/` (versionado) e, fora
do git, em `arquivos-preservados/` — com segunda cópia no Google Drive do DOXA desde 2026-09-13
(os mapas na pasta pública; o resto numa pasta privada). A única fonte externa é o Wayback Machine,
de onde vieram, por exemplo, os downloads da Pesquisa COVID.

**Endereços antigos continuam funcionando.** Links de fora para páginas do WordPress (no Google, em
artigos, em currículos) são levados para onde o conteúdo está agora — um item do acervo cai no card
certo, uma pesquisa chega com a busca preenchida, um PDF antigo abre a cópia nova. A tabela e as
regras ficam em `src/lib/rotas-antigas.mjs`; a lista do que existia no site antigo, em
`extracao/dados/enderecos-antigos.txt`.

**Os mapas de votação ficam no Google Drive do DOXA** (conta do acervo, pasta
*Acervo Doxa (NEW) / Site DOXA — Mapas de votação*, compartilhada por link). São 273 PDFs, grandes
demais para o GitHub Pages. `extracao/dados/mapas-no-drive.csv` registra onde cada um foi parar, com o
SHA-256 (e é lido pelo build para levar o endereço antigo de cada mapa ao novo). Mover ou renomear a
pasta no Drive não quebra os links; **apagar e reenviar um arquivo quebra**, porque ele ganha outro
endereço.
