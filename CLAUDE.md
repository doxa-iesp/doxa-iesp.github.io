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
npm run verificar-links  # depois do build: todo link/arquivo interno do dist/ existe
npm run preview   # serve dist/

# Scripts Python
python3 scripts/trocar-links-arquivos.py MAPA.csv ARQ...   # troca links origem -> destino por string literal
python3 scripts/converter-conteudo.py --forcar-regeneracao # APOSENTADO: sobrescreve src/; não use (ver "Conteúdo")
```

`npm run build` = `npm run validar && astro build`. **Não remova o validador**
(veja "Armadilhas" abaixo). **Node ≥ 22.12** — o Astro 7 se recusa a rodar em versão mais velha;
o CI lê a versão de `.nvmrc`.

**Não há suíte de testes** — e não é esquecimento: o site não tem lógica de runtime para testar.
O que substitui o teste é o par `validar` + `check`, e é isso que o CI roda. Antes de dizer que uma
mudança funciona, rode `npm run build` (que já inclui o validador) e, se mexeu em tipos ou props de
componente, `npm run check`.

Deploy: push em `main` → `.github/workflows/deploy.yml` → GitHub Pages.
PRs rodam `.github/workflows/pr.yml`. Os dois fazem build, a trava do loader (armadilha 1) e
`npm run verificar-links`; o de PR também roda `astro check` e publica o artefato `site-dist`.

## Arquitetura

Separação dura entre **o que o estagiário edita** e **o que o desenvolvedor edita**.

```
src/
  content.config.ts   ← schemas Zod. O contrato. Mudança aqui quebra conteúdo.
  data/*.yaml         ← EDITÁVEL: listas (publicações, mídia, seminários, acervo, mapas…)
  content/
    equipe/*.yaml     ← EDITÁVEL: um arquivo por pessoa
    projetos/*.md     ← EDITÁVEL: um arquivo por projeto (o nome do arquivo vira a URL)
    eventos/*.md      ← EDITÁVEL: um arquivo por evento (só o frontmatter aparece no site)
    destaques/*.md    ← EDITÁVEL: a vitrine "Em destaque" da home
    paginas/*.md      ← EDITÁVEL: a prosa de cada página
  components/ layouts/ pages/ styles/ lib/   ← código
public/               ← imagens, PDFs (pdfs/), CSV e XLSX (dados/), formulários (docs/). PRECISA
                        estar versionado. A fonte Montserrat vem do pacote @fontsource, não daqui.
extracao/             ← extração do WordPress antigo. Registro histórico, congelado (ver "Conteúdo").
scripts/              ← validador de dados, troca de links e o conversor da migração (aposentado)
```

### Coleções

Duas formas de carregar, escolhidas por ergonomia de edição:

- `glob()` — **um arquivo por entrada** (`equipe`, `eventos`, `paginas`, `projetos`, `destaques`).
  Adicionar = criar arquivo. Sem indentação de lista para errar, sem conflito de merge.
  `destaques` é a vitrine curada da home (receita 4.12 do guia) e a única coleção que nasceu
  depois da migração, sem equivalente em `extracao/`.
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
Para um campo de dado que pode ser link externo **ou** caminho interno, use `linkPara()` (mesmo
arquivo), que só aplica `url()` quando o destino não é externo. O config tem
`trailingSlash: 'always'`: links internos terminam em `/`.

No **corpo em Markdown** de uma coleção não há como chamar `url()`: link para arquivo do site ali é
**relativo** (em `src/content/projetos/pesquisa-covid.md`, `../../pdfs/projetos/…`), que resolve
certo com qualquer `base`. Um `](/pdfs/…)` cru seria o mesmo 404 adormecido.

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
  dentro da [404](src/pages/404.astro); arquivos antigos de `/wp-content/uploads/` são achados pelo
  nome em `/arquivos-antigos.json` ([endpoint](src/pages/arquivos-antigos.json.ts)), que varre
  `public/pdfs/` e `public/dados/` (PDF, XLSX, DOCX), lê `mapas-no-drive.csv` e aplica
  `RENOMEADOS` — cujas **chaves precisam estar em minúsculas** (a 404 procura assim) e cujo destino
  pode ser externo. Arquivo trazido do WordPress mantém o nome original justamente para casar sem
  entrada na tabela. A lista do que existia está em `extracao/dados/enderecos-antigos.txt`: toda
  mudança aqui se confere contra ela (cada endereço precisa cair numa página que existe).
  O `id` do card do acervo sai de `idItemAcervo()` em [src/lib/ancoras.mjs](src/lib/ancoras.mjs),
  que imita o slug do WordPress: é por isso que 93 dos 95 endereços `/acervo-doxa/` casam sem
  tabela. **Mudar essa função quebra os redirecionamentos.** Ela e `rotas-antigas.mjs` são `.mjs`,
  não `.ts`, porque o `astro.config.mjs` as importa.
- **Buscas e filtros** normalizam texto com `normalizar()` e casam com `casaBusca()`, ambos em
  [src/lib/texto.ts](src/lib/texto.ts): todos os termos, cada um como início de palavra. As listas com
  abas usam [AbasFiltro.astro](src/components/AbasFiltro.astro), que aceita busca (`busca`, com
  `?busca=` na URL) e esconde grupos vazios (`[data-filtro-grupo]`). As "abas" são botões de
  alternância (`aria-pressed`), não `role="tab"`: não há painel de aba, é um filtro sobre a mesma
  lista. O acervo aceita `?candidato=`, `?ano=`, `?cargo=`, `?regiao=`, `?partido=` e âncora
  `#item-<código>`; o formulário de filtros não é enviado (Enter só filtra).
- **Links com o mesmo texto** ("Ver mapa", "Baixar os dados (CSV)", "Assistir no Google Drive")
  ganham contexto para leitor de tela: `aria-describedby` apontando para o título do item, ou texto
  na classe global `.visualmente-oculto`. Ao criar lista com botões repetidos, faça o mesmo.

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
build e falha com código 1. E por isso `deploy.yml` e `pr.yml` têm uma trava que reprova se um
rótulo `[file-loader]` ou `[glob-loader]` aparecer no log — com `set -o pipefail`, sem o qual o
`tee` devolveria 0. Para reproduzir o bug original: `rm -rf dist .astro node_modules/.astro && npx astro build`.

**A trava original nunca funcionou no CI.** Ela procurava `[file-loader] Error`, mas no GitHub
Actions a variável `CI` liga as cores do log, e o código de cor cai entre o rótulo e a mensagem:
`[ERROR] [file-loader]^[[39m Error reading data`. O grep não casava nunca (reproduzido em
2026-09-14 com `CI=true npx astro build`). Por isso a busca é só pelo rótulo. Ao mexer nessa trava,
teste com `CI=true` e com `/usr/bin/grep` — o `grep` do terminal pode ser outro programa.

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
`extracao/` e `arquivos-preservados/`, e a **única fonte externa é o Wayback Machine** (de onde vieram
o cartaz do seminário Marcus Figueiredo e os downloads da Pesquisa COVID).

Os PDFs moram em dois lugares: `public/pdfs/` (teses, análises, textos para discussão, livro, cartaz)
e o **Google Drive do DOXA** — conta do acervo, pasta *Acervo Doxa (NEW) / Site DOXA — Mapas de
votação*, compartilhada por link — para os **273 mapas** (835 MB, que não cabem no teto de 1 GB do
GitHub Pages). [extracao/dados/mapas-no-drive.csv](extracao/dados/mapas-no-drive.csv) registra o
endereço antigo, o novo e o SHA-256 de cada mapa. **Mover ou renomear no Drive não quebra link;
apagar e reenviar quebra** (o arquivo ganha outro ID). Links de mapa vivem em três arquivos que
precisam bater: `src/data/mapas-votacao.yaml` (o que a página mostra), `public/dados/mapas-votacao.csv`
(catálogo publicado) e `extracao/dados/mapas-no-drive.csv` (lido pelo build para montar
`/arquivos-antigos.json`, que leva o endereço antigo de cada mapa ao novo) — troque com
[scripts/trocar-links-arquivos.py](scripts/trocar-links-arquivos.py), que preserva as quebras de linha
(os CSVs são CRLF). Não presuma que um PDF referenciado existe sem conferir — `DADOS_PENDENTES.md` é
também a lista do que falta preencher (e que está faltando **de propósito**, não por bug).

**2e. `arquivos-preservados/` existe fora do git: no Mac de quem fez a migração e no Drive.** Ignorada pelo git de
propósito (835 MB). Tem a cópia original dos 273 mapas, 6 PDFs órfãos (nenhuma página os linka) e o
PDF original do livro *A Decisão do Voto* (com o trecho que a coordenação pediu para tirar da versão
publicada). Desde 2026-09-13 há segunda cópia de tudo no Drive do DOXA: os mapas na pasta pública
acima; órfãos, original do livro e `manifesto.csv` em *Acervo Doxa (NEW) / Site DOXA — Arquivos
preservados (não compartilhar)*, **privada** — não compartilhe, o original do livro não deve ir ao
ar. `git clean -fdx` apaga a pasta local sem aviso: rode sempre `git clean -fdx -e
arquivos-preservados`, nunca o comando cru.

**2f. Cópias "nome N" viram itens repetidos.** Em 2026-09-07, ao trazer arquivos para a `main`,
apareceram **142** cópias como `felipe-lamarca 3.yaml` e `pesquisa-covid 4.md` em `src/content/`.
Nenhuma tinha conteúdo único (133 idênticas ao original, 9 versões antigas), mas as coleções usam
`glob('**/*')`, que **não distingue cópia de original**: a página da equipe renderizava **80 cards
em vez de 16** e o build produzia 41 páginas em vez de 25, com rotas fantasmas como
`/projetos/pesquisa-covid-3/`. Build verde, site errado.

`scripts/validar-dados.mjs` falha com código 1 quando encontra uma, em qualquer nível de
`src/content`, `src/data` e `public` — mas só quando o original existe ao lado (`nome 2.yaml` com
`nome.yaml`, pasta `equipe 2` com `equipe`), porque `TD 2.pdf` sozinho é nome legítimo. O
`.gitignore` **não** esconde mais nomes com número: as regras antigas (`* [0-9].*`) faziam um
arquivo legítimo nunca ser commitado — 404 no site com o build verde — e deixavam passar pastas.
Antes de apagar uma cópia, `diff` contra o original.

**2g. Classe de página passada a um componente precisa chegar pelo `...rest`.** O Astro escopa o CSS
de cada arquivo com um atributo `data-astro-cid-*`. Uma regra da página como `.hero__titulo
{ margin: 0 }` compila para `.hero__titulo[data-astro-cid-<página>]` — e só casa se o elemento do
componente filho carregar o cid da página, que o Astro entrega junto com as props. Até 2026-09-13 o
[Titulo](src/components/Titulo.astro) recebia a classe em `classe` e não espalhava o resto: **a
margem e a cor do título do herói nunca valeram**, e ninguém viu porque classes globais
(`.titulo-secao`) funcionavam. Agora ele aceita `class` e faz `{...rest}`. Ao criar componente que
recebe classe de fora, faça o mesmo — e confira no `dist/` que o elemento tem os dois cids.

**2h. Link externo apodrece, e às vezes vira armadilha.** Nenhum build acusa link externo quebrado.
Em 2026-09-13, 13 dos ~450 links de terceiros estavam mortos — e um deles, o do texto de Nara
Salles no Horizontes ao Sul, **redirecionava para um site de APK pirata**; o domínio do blog antigo
do Vota Aí tinha sido tomado por outro site; um item de mídia apontava para um **anexo do Gmail**.
Ao consertar: preferir o endereço novo do próprio veículo; senão, uma captura do Wayback Machine
**anterior à perda do domínio**, conferindo que o título da página bate com o `titulo` do item
(capturas de páginas montadas por JavaScript costumam vir vazias); senão, tirar o `url` — o item
fica sem botão. Nunca link de Gmail ou Drive pessoal. Para baixar um arquivo do Wayback, use
`https://web.archive.org/web/<timestamp>id_/<url>` e confira que não veio cortado: capturas antigas
podem parar em exatamente 1 MiB (1.048.576 bytes), e PDF inteiro termina em `%%EOF`.

**3. Defeito na fonte: `programas-eleitorais-capitais.csv`.** A coluna `municipio` está
rotacionada em relação aos candidatos (Eduardo Paes aparece como Florianópolis). Documentado em
[extracao/README.md](extracao/README.md); a página `/bancos-de-dados/` renderiza um aviso.
Não "conserte" por adivinhação.

**4. Campos opcionais são opcionais de verdade.** 30 das 60 pesquisas não têm link; 9 dos 70 itens
de mídia não têm URL; 9 dos 16 membros não têm Lattes e **nenhum** tem e-mail; seminários não têm
descrição nem link. Nada disso existe no site antigo. Não invente, e não crie botões mortos — o
`CardMembro` reserva a linha vazia justamente para o card não desalinhar quando falta o link.
O que falta e o que está "a conferir" fica em [DADOS_PENDENTES.md](DADOS_PENDENTES.md).

**5. Em evento, só o frontmatter aparece.** Não há página de detalhe de evento: `/eventos/` passa
ao `CardEvento` só `titulo`, `data`, `descricao`, `imagem`, `url` e `anexos`. Texto escrito no corpo
do `.md` não é renderizado em lugar nenhum. E `data` é a data **do evento** — a migração trouxe a
data do post do WordPress, e dois eventos ficaram com a data errada até 2026-09-13.

**6. A coleção vem ordenada pelo id, não pela ordem do arquivo.** O Astro guarda e devolve toda
coleção em ordem alfabética do `id` (`mutable-data-store.js`). Com o id feito só do título, as
análises dentro de um ciclo, as publicações do mesmo ano e matérias de mesma data saíam em ordem
alfabética — diferente do site antigo — e ninguém percebeu por meses (corrigido em 2026-09-14).
Hoje `listaYaml()` põe a **posição do item no id** (`0007-hgpe-eleicoes-1989`), então a ordem do id
é a ordem do arquivo; e **toda página que lista precisa de sort explícito com desempate**
(`|| a.id.localeCompare(b.id)` para as listas; `|| titulo` para as coleções `glob`, cujo id é o nome
do arquivo). Parceiros ordena por `nome` de propósito. Ao criar uma lista nova, não confie na ordem
em que `getCollection` devolve.

## Conteúdo: `src/` é a fonte

**Desde 2026-09-13, a fonte de verdade do conteúdo é `src/`.** Corrija e acrescente direto em
`src/content/` e `src/data/` — é o que o guia manda o estagiário fazer, e é a única regra.

[scripts/converter-conteudo.py](scripts/converter-conteudo.py) foi o que converteu `extracao/dados/`
nas coleções durante a migração. Está **aposentado**: sem `--forcar-regeneracao`, sai com código 1
sem tocar em nada. Rodado com a flag, ele apaga e regenera `src/content/` (menos `destaques/`) e os
YAML de `src/data/` — inclusive `site.yaml`, cujos valores estão fixos no próprio script — e
**desfaz toda correção feita em `src/` depois da migração**. Fica no repositório como documentação de
como cada dado foi convertido (`CARGOS`, `OVERRIDES`, filtros).

`extracao/` é **registro histórico congelado**: não edite para corrigir o site. Duas exceções vivas:

- `extracao/dados/mapas-no-drive.csv` é **entrada do build** (lido por
  [src/pages/arquivos-antigos.json.ts](src/pages/arquivos-antigos.json.ts)); se os mapas mudarem
  de lugar, ele muda junto.
- `extracao/dados/enderecos-antigos.txt` é a lista de endereços do site antigo, referência para
  conferir qualquer mudança em [src/lib/rotas-antigas.mjs](src/lib/rotas-antigas.mjs).

## Documentos

- [docs/DECISAO_ARQUITETURA.md](docs/DECISAO_ARQUITETURA.md) — por que Astro e não Hugo, com a
  ressalva do `file()` e como foi fechada.
- [docs/GUIA_DE_MANUTENCAO.md](docs/GUIA_DE_MANUTENCAO.md) — guia para estagiários, sem jargão, com
  uma receita por tarefa. **Mudou um campo, uma regra do validador ou um rótulo da página? Atualize a
  receita e a Seção 5 (valores permitidos) no mesmo commit.**
- [DADOS_PENDENTES.md](DADOS_PENDENTES.md) — o que falta preencher ou conferir, e o que já foi
  resolvido (com a origem dos arquivos recuperados).
- [docs/MUDANCAS_DE_LAYOUT.md](docs/MUDANCAS_DE_LAYOUT.md) — todo desvio do site antigo, com motivo.
- [docs/RESUMO_EXECUTIVO.md](docs/RESUMO_EXECUTIVO.md) — retrato da reconstrução em 2026-07-10
  (contagens de conteúdo migrado, estado técnico); desatualizado quanto às rotas (é anterior a
  `/producao/` e `/projetos/`), mas útil como referência de escopo.
- [extracao/README.md](extracao/README.md) — o que foi extraído do WordPress e os defeitos da fonte
  (retrato congelado da extração).
- [checkpoints/](checkpoints/) — o histórico de decisões de cada etapa da reconstrução.
