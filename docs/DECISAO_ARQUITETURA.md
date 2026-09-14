# Decisão de Arquitetura — Site do DOXA

**Data:** 2026-07-09
**Status:** decidido, vinculante para as fases seguintes.

---

## 1. Stack escolhida: **Astro 7 + TypeScript + CSS puro (custom properties)**

Conteúdo em Markdown e YAML, validado por **content collections com schema Zod**.
Deploy estático via GitHub Actions → GitHub Pages.

### O critério que decidiu

O prompt mestre fixa uma restrição de arquitetura: *o site será mantido por estagiários, não por
desenvolvedores*. Disso decorre a pergunta que separa as opções:

> Quando um estagiário digitar algo errado, o site quebra **de forma visível e reversível**
> (build falha, PR não passa), ou **de forma silenciosa** (o site publica sem o conteúdo)?

Essa é a diferença real entre as opções, e não a curva de aprendizado — porque em **todas** elas o
estagiário edita os mesmos arquivos Markdown/YAML. O que muda é o que acontece depois do erro.

### A evidência concreta

O site Hugo que já existe neste repositório tem exatamente a falha silenciosa. Em
`layouts/institucional/list.html`, as categorias da equipe são uma lista literal dentro do template:

```go-html-template
{{ $categories := slice (dict "key" "coordenacao" ...) (dict "key" "pesquisadores" ...) }}
{{ $members := where $team "category" $cat }}
```

Se um estagiário escrever `category: pesquisadorS` em `data/team.yaml`, o Hugo **constrói o site
normalmente** e o membro simplesmente desaparece da página. Sem erro, sem aviso, em produção.
O mesmo vale para `type` em `publications.yaml`.

Rodei o teste equivalente em Astro antes de decidir. Com o mesmo erro de digitação, o build falha
(saída do protótipo de 2026-07, quando a equipe ainda era um `src/data/equipe.yaml` só; hoje é um
arquivo por pessoa em `src/content/equipe/`):

```
[InvalidContentEntryDataError] equipe → bruno data does not match collection schema.
  category: Invalid option: expected one of "coordenacao"|"pesquisadores"|"aluno"
  Location: src/data/equipe.yaml
```

A mensagem nomeia a entrada, o campo e os valores aceitos. O GitHub Actions marca o PR como
falho e o conteúdo errado nunca chega ao ar. É esse comportamento que a Fase 2 (Agente B) exige:
*"um erro de digitação de um estagiário gera um erro de build claro, não uma página quebrada
silenciosa em produção"*.

### A ressalva que descobrimos depois — e como ela foi fechada

A validação do Astro **não é total**. O loader `file()` (usado para as listas em `src/data/*.yaml`)
**engole exceções do parser de YAML**. Se um estagiário errar a indentação de `midia.yaml`, o Astro
imprime `[ERROR] [file-loader] Error reading data`, **sai com código 0** e publica a página de
"Na Mídia" **vazia**. Reproduzido num build frio (o do CI) em 2026-07-10:

```
rm -rf dist .astro node_modules/.astro && npx astro build
→ exit 0, /na-midia/ publicada com 0 das 70 matérias
```

Localmente o erro passava despercebido porque `node_modules/.astro/data-store.json` guardava a
versão boa dos dados. No CI, que começa do zero, o site iria ao ar mutilado.

Ou seja: escolhemos o Astro pela validação, e a validação tinha um furo justamente no formato que
mais gente vai editar. Foram acrescentadas duas travas:

1. **`scripts/validar-dados.mjs`**, executado por `npm run build` *antes* do `astro build`. Ele
   parseia cada arquivo de conteúdo e falha com código 1, apontando arquivo, linha e coluna, em
   português. Também recusa uma lista que ficou pequena demais (item apagado sem querer).
2. **Uma trava no `deploy.yml` e no `pr.yml`** que reprova o build se o rótulo `[file-loader]` ou
   `[glob-loader]` aparecer no log, mesmo que o Astro insista em sair com 0. (O passo usa
   `set -o pipefail`; sem isso o `tee` devolveria 0 e a trava seria inútil.) *Até 2026-09-14 a
   trava procurava `[file-loader] Error` e nunca casou no CI: lá o log sai colorido e o código de
   cor fica entre o rótulo e a mensagem.*

Com as duas, a promessa da seção anterior se sustenta para **todos** os formatos de conteúdo.

---

## 2. Comparação das opções

Avaliadas quatro opções viáveis. As duas primeiras são as candidatas reais: Hugo é o que já está
no repositório, e Astro é o que o MAPE (mesmo departamento, IESP-UERJ) usa.

| | **Astro 7** | **Hugo** | **Eleventy** | **Quarto** |
|---|---|---|---|---|
| **Curva p/ editar conteúdo** | Markdown + YAML | Markdown + YAML | Markdown + YAML | Markdown/`.qmd` |
| **Erro de digitação em campo** | ❌ **build falha, mensagem nomeia entrada e campo** | ⚠️ build passa, conteúdo some em silêncio | ⚠️ igual a Hugo (sem schema nativo) | ⚠️ sem schema de dados |
| **YAML malformado** | build falha, aponta linha | build falha, mensagem razoável | build falha | build falha |
| **Preview antes de publicar** | PR preview via Actions; `npm run dev` com hot reload | `hugo server`; sem preview de PR nativo | `eleventy --serve` | `quarto preview` |
| **Edição pela web do GitHub** | sim (arquivos simples) | sim | sim | sim |
| **Dependências** | ~300 pacotes npm (lockfile) | **binário único, zero deps** | npm | R/Python + pandoc |
| **Velocidade de build** | ~2–5 s | ~40 ms | ~1 s | lento |
| **Conhecimento no IESP** | **MAPE usa Astro** | — | — | comum em stats |

### Por que não Hugo (apesar de já estar pronto)

Hugo é tecnicamente excelente: binário único, build de 40 ms, zero dependências — vantagens reais
para um laboratório sem equipe de TI. **Descartá-lo custa alguma coisa, e vale registrar isso.**

Mas Hugo não tem validação de schema de dados. É possível emular com `errorf` dentro dos templates
Go, e isso resolveria o sintoma; só que a lógica de validação passaria a morar no mesmo código de
template que os estagiários não devem tocar, escrita numa linguagem (Go templates) que ninguém no
grupo lê. Trocaríamos uma falha silenciosa por um código frágil que ninguém mantém.

### Por que não Eleventy

Mesmo problema do Hugo (sem schema nativo), sem a vantagem do binário único.

### Por que não Quarto

Excelente para publicar análises reproduzíveis, e o DOXA faz ciência de dados. Mas exige um runtime
R/Python no CI, é lento, e não tem modelo de dados estruturados para "lista de 34 publicações". Vale
considerar no futuro para publicar *análises*, não para o site institucional.

### O custo aceito do Astro

Astro traz ~300 pacotes npm. Mitigações adotadas:

- `package-lock.json` versionado; CI usa `npm ci` (instalação determinística).
- Versão do Node fixada em `.nvmrc` (22; o Astro 7 exige ≥ 22.12), lida pelo workflow.
- **Nenhum framework de UI** (sem React/Vue/Svelte) e nenhuma biblioteca de CSS. Astro puro,
  CSS com custom properties, JavaScript mínimo no cliente. Isso mantém a árvore de dependências
  pequena e o HTML final leve.

---

## 3. Estrutura de pastas

A regra: **o que o estagiário edita nunca fica junto do que o desenvolvedor edita.**

```
src/
  content.config.ts       ← schemas (Zod). Só desenvolvedor mexe.
  data/                   ← CONTEÚDO EDITÁVEL (listas)
    publicacoes.yaml
    analises.yaml
    textos-discussao.yaml
    midia.yaml
    seminarios.yaml
    pesquisas.yaml
    acervo.yaml
    bancos-de-dados.yaml
    mapas-votacao.yaml    ← links dos 273 mapas (os PDFs ficam no Google Drive)
    parceiros.yaml
    site.yaml             ← contato, redes, vídeos do acervo
  content/                ← CONTEÚDO EDITÁVEL (textos e fichas)
    equipe/*.yaml         ← um arquivo por pessoa
    eventos/*.md          ← um arquivo por evento
    projetos/*.md         ← um arquivo por projeto (o nome vira a URL)
    destaques/*.md        ← a vitrine "Em destaque" da home
    paginas/*.md          ← prosa de cada página
  components/             ← código. Estagiário não mexe.
  layouts/
  lib/                    ← utilitários: url(), menu (navegacao.ts), endereços antigos
  pages/                  ← rotas
  styles/tokens.css       ← paleta e tipografia
public/                   ← imagens, PDFs, CSV/XLSX, CNAME
  img/, pdfs/, dados/, docs/
extracao/                 ← extração do WordPress: registro histórico, não alimenta o site
```

O menu **não** fica em `site.yaml`: é código, em `src/lib/navegacao.ts`.

**Uma pessoa = um arquivo** (`src/content/equipe/nome-sobrenome.yaml`). Adicionar um membro é criar
um arquivo; remover é apagá-lo. Não há indentação de lista para errar, e dois estagiários editando
membros diferentes não geram conflito de merge.

**Listas bibliográficas** (publicações, mídia, seminários…) ficam em um YAML por coleção: são
dezenas de entradas curtas e homogêneas, e um arquivo por publicação criaria 200+ arquivos sem
ganho. O schema Zod valida cada entrada individualmente e a mensagem de erro nomeia a entrada.

---

## 4. Fluxo de publicação

```
push / merge na branch main
        ↓
GitHub Actions: npm ci → npm run build (validador de conteúdo → astro build) → dist/
        ↓
falhou? (ou rótulo de loader no log, ou link interno quebrado) → nada é publicado
        ↓
passou? → deploy para GitHub Pages
```

Em **pull requests**, roda um job separado com o mesmo build (e as mesmas travas: rótulo de loader
no log e `npm run verificar-links`), mais `npm run check` (`astro check`), e publica o `dist/` como
artefato de download. O revisor vê se o build passou antes de aprovar. (Preview com URL pública
exigiria um serviço externo — Netlify/Cloudflare —, deliberadamente evitado para não introduzir
outra conta a manter.)

**URL de deploy.** O site é publicado em `https://lab-doxa.org.br/` (apex, sem `www`), na raiz,
portanto `base: ''`. O caminho até aqui passou por `felipelamarca.com/DOXA/` (com
`base: '/DOXA'`) e por `https://doxa-iesp.github.io/`, que hoje redireciona para o domínio. O
domínio depende de três lugares baterem: o DNS (registro.br), o domínio em *Settings > Pages* e, no
código, `site` + `public/CNAME`. O `CNAME` na raiz do repositório **não** é publicado — só o
conteúdo de `public/` entra no build.

O domínio era do WordPress antigo, que saiu do ar na troca. Os endereços antigos que circulam lá
fora são levados ao conteúdo novo por páginas-stub e pela página 404 (`src/lib/rotas-antigas.mjs`),
já que o GitHub Pages não faz redirecionamento no servidor.

---

## 5. Identidade visual

Extraída do site antigo e consolidada em `src/styles/tokens.css`:

| Token | Valor | Uso |
|---|---|---|
| `--cor-primaria` | `#305371` | azul institucional (header, títulos) |
| `--cor-primaria-clara` | `#3d6b8c` | variação clara do azul (definida, hoje sem uso) |
| `--cor-primaria-escura` | `#1e3a50` | hover, rodapé |
| `--cor-acento` | `#086d60` | verde — a outra ponta do gradiente |
| `--gradiente-marca` | azul → verde | nav, rodapé, capas de seção e **uma** faixa por página |
| `--cor-destaque` | `#ce673e` | terracota — **só superfície** (aba, borda, plaqueta): como texto dá 3,73:1 |
| `--cor-destaque-texto` | `#b3512c` | terracota para texto sobre fundo claro (5,08:1) |
| `--cor-destaque-claro` | `#ffd3be` | terracota para texto sobre o gradiente escuro |
| `--cor-texto` | `#26231e` | corpo |
| `--cor-fundo-alt` | `#f4f4f2` | faixas alternadas |
| `--fonte` | Montserrat | títulos e corpo |

A fonte Montserrat é **auto-hospedada**, pelo pacote `@fontsource-variable/montserrat` (importado em
`src/layouts/Base.astro`), e não carregada do Google Fonts: o site antigo dependia de uma
requisição externa que falha em redes restritas e vaza dados de visitantes.

Logo: `public/img/logo-doxa.svg` (extraído do site antigo).

---

## 6. Decisão de conteúdo já fechada (Seção 4.1 do prompt)

A **home deixa de ser um feed de destaques** e passa a ser a apresentação institucional do grupo:
quem é o DOXA, missão, linha de pesquisa, vínculo com o IESP-UERJ, parceiros. *(Atualização
2026-09: a home ganhou a faixa curada "Em destaque" — coleção `destaques` — e os atalhos levam a
`/producao/` e `/projetos/`, que substituíram `/pesquisas/`.)*

`/institucional/` continua existindo, **focada na equipe**. O texto institucional integral não é
duplicado nas duas páginas: a home apresenta o grupo, `/institucional/` mostra quem o compõe.

Isso está refletido no schema: a coleção `paginas` tem uma entrada `home.md` (apresentação) e uma
`institucional.md` (texto curto de contexto + a equipe vem da coleção `equipe`).
