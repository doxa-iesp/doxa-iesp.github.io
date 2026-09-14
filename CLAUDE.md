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
npm run dev       # http://localhost:4321/
npm run validar   # valida os YAML de conteúdo (roda sozinho antes do build)
npm run build     # validar + astro build -> dist/
npm run check     # validar + astro check (tipos)
npm run preview   # serve dist/
```

`npm run build` = `node scripts/validar-dados.mjs && astro build`. **Não remova o validador**
(veja "Armadilhas" abaixo).

**Não há suíte de testes** — e não é esquecimento: o site não tem lógica de runtime para testar.
O que substitui o teste é o par `validar` + `check`, e é isso que o CI roda. Antes de dizer que uma
mudança funciona, rode `npm run build` (que já inclui o validador) e, se mexeu em tipos ou props de
componente, `npm run check`.

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
    projetos/*.md     ← EDITÁVEL: um arquivo por projeto (o nome do arquivo vira a URL)
    eventos/*.md      ← EDITÁVEL: um arquivo por evento
    paginas/*.md      ← EDITÁVEL: a prosa de cada página
  components/ layouts/ pages/ styles/ lib/   ← código
public/               ← imagens, fontes, PDFs (PRECISA estar versionado)
extracao/             ← extração completa do WordPress antigo. Fonte de verdade dos dados.
scripts/              ← conversor de conteúdo e validador de dados
```

### Coleções

Duas formas de carregar, escolhidas por ergonomia de edição:

- `glob()` — **um arquivo por entrada** (`equipe`, `eventos`, `paginas`, `projetos`, `destaques`).
  Adicionar = criar arquivo. Sem indentação de lista para errar, sem conflito de merge.
  `destaques` é a vitrine curada da home e é a **única** coleção que o
  `converter-conteudo.py` não regenera — o que se escreve nela à mão fica (receita 4.12 do guia).
- `file()` + `listaYaml()` — **um YAML com uma lista** (publicações, mídia, …). O helper
  `listaYaml` em `content.config.ts` gera o `id` de cada item a partir do título, para que ninguém
  precise escrever `id:` à mão. O `id` só aparece em mensagens de erro; não vira URL.

### Base path

O site é publicado em `https://lab-doxa.org.br/` — domínio próprio, **apex sem `www`** (o `www` só
redireciona), servido pelo GitHub Pages na **raiz**. Por isso `base: ''` em
[astro.config.mjs](astro.config.mjs). `doxa-iesp.github.io` redireciona para o domínio.

Mesmo assim, **todo link interno passa por `url()`** de [src/lib/url.ts](src/lib/url.ts). Não é
zelo inútil: o site já viveu em `felipelamarca.com/DOXA/`, e foi só trocar o `base` para migrar.
Um `href="/acervo/"` cru voltaria a dar 404 no dia em que o site for para um subdiretório.

Domínio: três lugares precisam bater — o DNS (registro.br), o domínio em *Settings > Pages* e, no
código, `site` em `astro.config.mjs` + `public/CNAME`. `site` errado não quebra nada visível, mas
manda canonical, `og:url` e sitemap para outro host. O `CNAME` da raiz do repo **não** é publicado —
só `public/` entra no build.

## Estrutura do site

- **`/producao/`** reúne o que o laboratório produz: pesquisas, publicações acadêmicas, análises de
  conjuntura e textos para discussão. Antes eram dois itens de menu separados.
- **`/projetos/`** reúne as iniciativas com entrega pública (Vota Aí, dashboards, Pesquisa COVID,
  Geografia do Voto). Antes viviam espalhadas pela home e dentro de `site.yaml`.
- **Endereços antigos continuam funcionando** — as rotas antigas deste site (`/pesquisas/`,
  `/publicacoes/*`) e as ~650 do WordPress que citam o domínio lá fora. Tudo sai de
  [src/lib/rotas-antigas.mjs](src/lib/rotas-antigas.mjs): `REDIRECIONAMENTOS` (destino exato) vira
  página-stub via [src/pages/[...antiga].astro](src/pages/[...antiga].astro) e
  [Redirecionamento.astro](src/components/Redirecionamento.astro); `destinoAntigo()` resolve os
  padrões (`/acervo-doxa/<item>/` → card do acervo, `/lista-pesquisas/<slug>/` → busca preenchida…)
  dentro da [404](src/pages/404.astro); PDFs antigos de `/wp-content/uploads/` são achados pelo nome
  em `/arquivos-antigos.json` ([endpoint](src/pages/arquivos-antigos.json.ts)). A lista do que
  existia está em `extracao/dados/enderecos-antigos.txt` — use-a para conferir qualquer mudança.
- **Buscas e filtros** normalizam texto com `normalizar()` e casam com `casaBusca()`, ambos em
  [src/lib/texto.ts](src/lib/texto.ts): todos os termos, cada um como início de palavra. As listas com
  abas usam [AbasFiltro.astro](src/components/AbasFiltro.astro), que aceita busca (`busca`, com
  `?busca=` na URL) e esconde grupos vazios (`[data-filtro-grupo]`). O acervo aceita
  `?candidato=`, `?ano=`, `?cargo=`, `?regiao=`, `?partido=` e âncora `#item-<código>`.

## Sistema visual

Tudo em [src/styles/tokens.css](src/styles/tokens.css) e [src/styles/global.css](src/styles/global.css).
Não redefina `.prosa`, `.cartao`, `.grade-cards` numa página: elas são globais **de propósito** —
a `.prosa` já esteve copiada em 12 arquivos, sempre sem `margin-inline: auto`, e por isso o texto
ficava preso à esquerda.

**O terracota tem três tokens, e a distinção importa:**

| Token | Uso | Por quê |
|---|---|---|
| `--cor-destaque` `#ce673e` | **só superfície** (aba, borda, plaqueta) | como texto dá **3,73:1** sobre branco — reprova em AA |
| `--cor-destaque-texto` `#b3512c` | texto sobre fundo claro | 5,08:1 ✓ |
| `--cor-destaque-claro` `#ffd3be` | texto sobre o gradiente escuro | 4,55:1 no pior ponto ✓ |

O `--gradiente-marca` (navy→verde) é a assinatura da marca. Use com parcimônia: nav, rodapé, capas
de seção e **uma** faixa de destaque por página — se toda seção ganhar gradiente, vira um bloco só.

**Títulos são bi-peso, e isso é código, não CSS.** O site antigo escrevia "Textos para
**Discussão**", "Nossa **Equipe**", "Argelina **Cheibub Figueiredo**" — última palavra em destaque.
Quem faz isso é [src/components/Titulo.astro](src/components/Titulo.astro), sobre
`partirUltimaPalavra()` de [src/lib/texto.ts](src/lib/texto.ts) (usado também por `PageHero` e
`CardMembro`). Não escreva `<h2>` cru numa página nova: use `<Titulo>`, e passe `forte` quando a
quebra natural não for a última palavra. Exceções: rótulos pequenos em caixa alta ("O DOXA em
números", "O projeto") e títulos de card/item ficam crus — o bi-peso não se lê neles.

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

**2c. `redirects` do `astro.config.mjs` ignora o `base`.** O Astro monta o destino só a partir dos
segmentos da rota (`dist/core/routing/generator.js`), sem o `base`. Hoje isso é inofensivo, porque
`base` é vazio — mas quando o site vivia em `/DOXA/`, um `redirects: {'/pesquisas':
'/producao/pesquisas'}` mandava o visitante para `felipelamarca.com/producao/pesquisas/` — 404, **e
só em produção**. É uma armadilha adormecida, não morta: ela volta no dia em que o site for para um
subdiretório. Por isso os redirecionamentos continuam sendo páginas-stub que montam o destino com
`url()` ([src/components/Redirecionamento.astro](src/components/Redirecionamento.astro)), geradas da
tabela em [src/lib/rotas-antigas.mjs](src/lib/rotas-antigas.mjs) — e ficam fora do sitemap, via
`ROTAS_ANTIGAS` no [astro.config.mjs](astro.config.mjs), que lê a mesma tabela.

**2d. O site antigo não existe mais — nada pode depender dele.** O WordPress saiu do ar em 2026-09
e o domínio `lab-doxa.org.br` passou a servir este site. Consequência que não é óbvia: **um link
para `www.lab-doxa.org.br/...` não dá erro de conexão, dá 404 deste próprio site**, e nenhum build
acusa (para o Astro é link externo). Foi assim que 273 mapas, 4 "Saiba mais" de eventos, 2 links de
bancos de dados e um anexo quebraram de uma vez. Todos foram resolvidos; um dado novo não pode voltar
a apontar para lá. Não há como baixar nada do site antigo de novo: o que foi preservado está em
`extracao/` e `arquivos-preservados/`, e a **única fonte externa é o Wayback Machine** (de onde veio o
cartaz do seminário Marcus Figueiredo). O conversor tentava baixar imagens de evento de lá; agora usa
`curl -f` e avisa para pôr a imagem à mão.

Os PDFs moram em dois lugares: `public/pdfs/` (teses, análises, textos para discussão, livro, cartaz)
e o **Google Drive do DOXA** — conta do acervo, pasta *Acervo Doxa (NEW) / Site DOXA — Mapas de
votação*, compartilhada por link — para os **273 mapas** (835 MB, que não cabem no teto de 1 GB do
GitHub Pages). [extracao/dados/mapas-no-drive.csv](extracao/dados/mapas-no-drive.csv) registra o
endereço antigo, o novo e o SHA-256 de cada mapa. **Mover ou renomear no Drive não quebra link;
apagar e reenviar quebra** (o arquivo ganha outro ID). Links de mapa vivem em três arquivos que
precisam bater: `extracao/dados/mapas-votacao.csv` (fonte do conversor), `src/data/mapas-votacao.yaml`
e `public/dados/mapas-votacao.csv` (catálogo publicado) — troque com
[scripts/trocar-links-arquivos.py](scripts/trocar-links-arquivos.py), que preserva as quebras de linha
(os CSVs são CRLF). Não presuma que um PDF referenciado existe sem conferir — `DADOS_PENDENTES.md` é
também a lista do que falta preencher (e que está faltando **de propósito**, não por bug).

**2e. `arquivos-preservados/` só existe no Mac de quem fez a migração.** Ignorada pelo git de
propósito (835 MB). Tem a cópia original dos 273 mapas, 6 PDFs órfãos (nenhuma página os linka) e o
PDF original do livro *A Decisão do Voto* (com o trecho que a coordenação pediu para tirar da versão
publicada). Desde 2026-09-13 há segunda cópia de tudo no Drive do DOXA: os mapas na pasta pública
acima; órfãos, original do livro e `manifesto.csv` em *Acervo Doxa (NEW) / Site DOXA — Arquivos
preservados (não compartilhar)*, **privada** — não compartilhe, o original do livro não deve ir ao
ar. `git clean -fdx` apaga a pasta local sem aviso: rode sempre `git clean -fdx -e
arquivos-preservados`, nunca o comando cru.

**2f. O repositório vive no Desktop, e o iCloud fabrica cópias.** Em 2026-09-07 havia **142**
arquivos como `felipe-lamarca 3.yaml` e `pesquisa-covid 4.md` em `src/content/` — cópias de
conflito de sincronização do macOS. Nenhuma tinha conteúdo único (133 idênticas ao original, 9
versões antigas), mas as coleções usam `glob('**/*')`, que **não distingue cópia de original**:
a página da equipe renderizava **80 cards em vez de 16** e o build produzia 41 páginas em vez de
25, com rotas fantasmas como `/projetos/pesquisa-covid-3/`. Build verde, site errado.

O `.gitignore` tinha uma regra para isso, mas só para o sufixo ` 2` — por isso metade das cópias
era invisível no `git status`. A regra agora cobre qualquer número, e `scripts/validar-dados.mjs`
falha com código 1 quando encontra uma (o `.gitignore` protege o commit; só o validador protege o
build local). Antes de apagar, `diff` contra o original — nunca houve conteúdo único, mas é barato
conferir. **O conserto de raiz é tirar o repositório de `~/Desktop`.**

**2g. Classe de página passada a um componente precisa chegar pelo `...rest`.** O Astro escopa o CSS
de cada arquivo com um atributo `data-astro-cid-*`. Uma regra da página como `.hero__titulo
{ margin: 0 }` compila para `.hero__titulo[data-astro-cid-<página>]` — e só casa se o elemento do
componente filho carregar o cid da página, que o Astro entrega junto com as props. Até 2026-09-13 o
[Titulo](src/components/Titulo.astro) recebia a classe em `classe` e não espalhava o resto: **a
margem e a cor do título do herói nunca valeram**, e ninguém viu porque classes globais
(`.titulo-secao`) funcionavam. Agora ele aceita `class` e faz `{...rest}`. Ao criar componente que
recebe classe de fora, faça o mesmo — e confira no `dist/` que o elemento tem os dois cids.

**3. Defeito na fonte: `programas-eleitorais-capitais.csv`.** A coluna `municipio` está
rotacionada em relação aos candidatos (Eduardo Paes aparece como Florianópolis). Documentado em
[extracao/README.md](extracao/README.md); a página `/bancos-de-dados/` renderiza um aviso.
Não "conserte" por adivinhação.

**4. Campos opcionais são opcionais de verdade.** 30 das 61 pesquisas não têm link; 7 dos 70 itens
de mídia não têm URL; 9 dos 16 membros não têm Lattes e **nenhum** tem e-mail; seminários não têm
descrição nem link. Nada disso existe no site antigo. Não invente, e não crie botões mortos — o
`CardMembro` reserva a linha vazia justamente para o card não desalinhar quando falta o link.

## Regenerar o conteúdo

[scripts/converter-conteudo.py](scripts/converter-conteudo.py) reconstrói `src/content/` e
`src/data/` a partir de `extracao/dados/`. É idempotente e **sobrescreve edições manuais** —
se alguém corrigir um dado à mão, corrija também em `extracao/`, que é a fonte de verdade.

Duas formas de corrigir, escolha pela natureza do campo: se o valor em `extracao/` estava **errado ou
mudou** (um anexo que agora é local, um evento novo), edite `extracao/`; se o valor é **proveniência
fiel** que só não deve ir ao ar (o `url` "página original" dos bancos, que apontava para o
WordPress), filtre no conversor e deixe `extracao/` como registro. Depois de qualquer mudança, rode o
conversor e confira com `git diff` que só mudou o que você esperava.

## Documentos

- [docs/DECISAO_ARQUITETURA.md](docs/DECISAO_ARQUITETURA.md) — por que Astro e não Hugo, com a
  ressalva do `file()` e como foi fechada.
- [docs/GUIA_DE_MANUTENCAO.md](docs/GUIA_DE_MANUTENCAO.md) — guia para estagiários, sem jargão.
- [docs/MUDANCAS_DE_LAYOUT.md](docs/MUDANCAS_DE_LAYOUT.md) — todo desvio do site antigo, com motivo.
- [docs/RESUMO_EXECUTIVO.md](docs/RESUMO_EXECUTIVO.md) — retrato da reconstrução em 2026-07-10
  (contagens de conteúdo migrado, estado técnico); desatualizado quanto às rotas (é anterior a
  `/producao/` e `/projetos/`), mas útil como referência de escopo.
- [checkpoints/](checkpoints/) — o histórico de decisões de cada etapa da reconstrução.
