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

Rodei o teste equivalente em Astro antes de decidir. Com o mesmo erro de digitação, o build falha:

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
2. **Uma trava no `deploy.yml`** que reprova o deploy se a palavra `[file-loader] Error` aparecer no
   log, mesmo que o Astro insista em sair com 0. (O passo usa `set -o pipefail`; sem isso o `tee`
   devolveria 0 e a trava seria inútil.)

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
- Versão do Node fixada no workflow (`node-version: 22`).
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
    parceiros.yaml
    site.yaml             ← contato, redes, menu
  content/                ← CONTEÚDO EDITÁVEL (textos e fichas)
    equipe/*.yaml         ← um arquivo por pessoa
    eventos/*.md          ← um arquivo por evento
    paginas/*.md          ← prosa de cada página
  components/             ← código. Estagiário não mexe.
  layouts/
  pages/                  ← rotas
  styles/tokens.css       ← paleta e tipografia
public/                   ← imagens, PDFs, CNAME
  img/equipe/, img/parceiros/
```

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
GitHub Actions: npm ci → astro build (valida schemas) → dist/
        ↓
falhou? → PR fica vermelho, nada é publicado
        ↓
passou? → deploy para GitHub Pages
```

Em **pull requests**, roda um job separado que só faz `astro build` e publica o `dist/` como
artefato de download. O revisor vê se o build passou antes de aprovar. (Preview com URL pública
exigiria um serviço externo — Netlify/Cloudflare —, deliberadamente evitado para não introduzir
outra conta a manter.)

**URL de deploy.** Hoje o site é publicado em `https://felipelamarca.com/DOXA/`, portanto
`base: '/DOXA'`. Para migrar a `www.lab-doxa.org.br`: remover o `base`, criar `public/CNAME` com o
domínio e apontar o DNS. Atenção: o `CNAME` na raiz do repositório **não** é publicado — só o
conteúdo de `public/` entra no build.

---

## 5. Identidade visual

Extraída do site antigo e consolidada em `src/styles/tokens.css`:

| Token | Valor | Uso |
|---|---|---|
| `--cor-primaria` | `#305371` | azul institucional (header, títulos) |
| `--cor-primaria-clara` | `#3d6b8c` | gradiente do header |
| `--cor-primaria-escura` | `#1e3a50` | hover, rodapé |
| `--cor-destaque` | `#CE673E` | terracota — borda do header, links de ação |
| `--cor-acento` | `#086D60` | verde — usos pontuais |
| `--cor-texto` | `#26231E` | corpo |
| `--cor-fundo-alt` | `#EDEDED` | faixas alternadas |
| `--fonte` | Montserrat | títulos e corpo |

A fonte Montserrat é **auto-hospedada** (`public/fonts/`), não carregada do Google Fonts: o site
antigo dependia de uma requisição externa que falha em redes restritas e vaza dados de visitantes.

Logo: `public/img/logo-doxa.svg` (extraído do site antigo).

---

## 6. Decisão de conteúdo já fechada (Seção 4.1 do prompt)

A **home deixa de ser um feed de destaques** e passa a ser a apresentação institucional do grupo:
quem é o DOXA, missão, linha de pesquisa, vínculo com o IESP-UERJ, parceiros. Destaques de projetos
aparecem como seção secundária, com link para `/pesquisas/`.

`/institucional/` continua existindo, **focada na equipe**. O texto institucional integral não é
duplicado nas duas páginas: a home apresenta o grupo, `/institucional/` mostra quem o compõe.

Isso está refletido no schema: a coleção `paginas` tem uma entrada `home.md` (apresentação) e uma
`institucional.md` (texto curto de contexto + a equipe vem da coleção `equipe`).
