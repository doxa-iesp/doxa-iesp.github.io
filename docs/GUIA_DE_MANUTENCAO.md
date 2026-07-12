# Guia de Manutenção do Site do DOXA

Este guia é para quem vai **cuidar do conteúdo do site** (equipe, publicações, eventos, notícias
etc.) sem precisar ser programador. Você não vai instalar nada nem escrever código — vai editar
arquivos de texto pelo próprio site do GitHub, do seu navegador.

Se bater qualquer dúvida, **peça ajuda antes de salvar** (veja "Quando pedir ajuda" no fim). É bem
mais fácil tirar uma dúvida do que consertar depois.

---

## 1. Como o site funciona (em 3 frases)

1. Todo o conteúdo do site mora em **arquivos de texto** dentro de um repositório no GitHub — você
   edita esses arquivos como quem edita um documento.
2. Sempre que uma alteração é aprovada, o GitHub **reconstrói o site sozinho** e, em uns 2 minutos,
   a mudança já está no ar.
3. Você **não instala nenhum programa**: tudo é feito pelo navegador, no site do GitHub.

O endereço do site hoje é **https://doxa-iesp.github.io/** (no futuro será www.lab-doxa.org.br).
O repositório fica em **https://github.com/doxa-iesp/doxa-iesp.github.io**.

---

## 2. Editar direto pelo site do GitHub (o jeito recomendado)

Este é o caminho mais seguro e simples. O passo a passo é sempre o mesmo:

1. **Entre no repositório**: https://github.com/doxa-iesp/doxa-iesp.github.io
2. **Navegue até o arquivo** que você quer mudar (as pastas estão explicadas nas "Receitas", na
   Seção 4). Clicar no nome de uma pasta abre ela; clicar no nome de um arquivo abre o conteúdo.
3. **Clique no lápis** (✏️, canto superior direito do arquivo) — é o botão "Edit this file".
4. **Faça a alteração** no texto.
5. Clique no botão verde **"Commit changes..."** (Salvar alterações).
6. Na janelinha que abre:
   - Escreva uma frase curta dizendo o que você fez (ex.: *"Adiciona a pesquisadora Fulana"*).
   - Marque a opção **"Create a new branch for this commit and start a pull request"**
     (Criar um novo branch e abrir um pull request).
   - Clique em **"Propose changes"** e depois em **"Create pull request"**.

> **O que é um *pull request* (PR)?** É um "pedido de alteração": em vez de mudar o site na hora,
> você propõe a mudança, o computador confere se está tudo certo, e só depois ela entra no ar.
> É a sua **rede de segurança**.

Depois de criar o PR, **espere 1 a 2 minutos** e olhe se ele ficou verde ou vermelho (Seção 3).

### Criar um arquivo novo (para membro da equipe ou evento)

Alguns conteúdos são **um arquivo por item** (cada pessoa da equipe é um arquivo; cada evento é um
arquivo). Para criar um:

1. No repositório, entre na pasta certa (ex.: `src/content/equipe/`).
2. Clique em **"Add file" → "Create new file"** (Adicionar arquivo → Criar novo arquivo).
3. No campo do nome, digite o nome do arquivo (ex.: `maria-souza.yaml`).
4. Cole o conteúdo (veja as Receitas), e siga do passo 5 acima ("Commit changes").

### Enviar uma imagem (foto de membro, imagem de evento)

1. Entre na pasta de imagens certa (ex.: `public/img/equipe/`).
2. Clique em **"Add file" → "Upload files"** (Enviar arquivos).
3. Arraste a imagem, e siga para "Commit changes" (marcando "Create a new branch...").

---

## 3. A rede de segurança: o PR fica verde ou vermelho

Depois que você cria um pull request, o GitHub roda uma conferência automática. Você vê o resultado
na própria página do PR e na aba **"Checks"** (Verificações):

- ✅ **Verde** = está tudo certo. A mudança pode ser aprovada e vai para o ar.
- ❌ **Vermelho** = tem algo errado. **O site NÃO é atualizado** enquanto estiver vermelho — ninguém
  vê o erro no site publicado. Você conserta com calma (é só editar o mesmo PR de novo).

### Onde ver o que deu errado

Na página do PR, clique em **"Details"** ao lado da verificação vermelha (ou na aba **"Checks"**).
Role até a parte vermelha da tela: a mensagem de erro aparece ali. Abaixo estão as mensagens mais
comuns e o que cada uma quer dizer.

#### Erro 1 — Você escreveu uma "categoria" (ou "tipo") que não existe

Exemplo: escrever `categoria: assistentes` (com "s" no fim) num arquivo de membro. A mensagem é:

```
[InvalidContentEntryDataError] equipe → teste-erro-categoria data does not match collection schema.

  categoria: Invalid option: expected one of "coordenacao"|"pesquisadores"|"pos-doutorando"|"aluno"|"assistente"|"associado"
```

**O que significa:** o valor que você digitou não está na lista de valores aceitos. A própria
mensagem mostra a lista certa entre aspas (`"coordenacao"|"pesquisadores"|...`). Compare com a
**Tabela de valores permitidos** (Seção 5) e corrija. No exemplo, o certo é `assistente` (singular),
não `assistentes`.

#### Erro 2 — Você esqueceu um campo obrigatório

Exemplo: adicionar uma publicação sem a linha `tipo:`. A mensagem é:

```
[InvalidContentEntryDataError] publicacoes → publicacao-de-teste-sem-tipo data does not match collection schema.

  tipo: Invalid option: expected one of "livro"|"capitulo"|"artigo"|"outros"
```

**O que significa:** faltou um campo que é obrigatório (aqui, o `tipo`). O trecho depois da seta
(`publicacoes → publicacao-de-teste-sem-tipo`) diz **em qual item** está o problema — nesse caso, o
item cujo título vira "publicacao de teste sem tipo". Adicione a linha que faltou.

#### Erro 3 — Você escreveu um nome de campo errado no `site.yaml`

Exemplo: escrever `emial:` no lugar de `email:` no arquivo de contato. A mensagem é:

```
[InvalidContentEntryDataError] configuracao → geral data does not match collection schema.

  email: Required
  : Unrecognized key: "emial"
```

**O que significa:** `email: Required` = o campo `email` é obrigatório e sumiu.
`Unrecognized key: "emial"` = você criou uma linha com um nome (`emial`) que o site não reconhece.
Quase sempre é um erro de digitação no começo da linha. Corrija o nome do campo.

#### Erro 4 — A "arrumação" (indentação) do arquivo ficou torta

Os espaços no começo de cada linha importam. Se você mexer neles sem querer, num arquivo de
**membro, evento, página ou no `site.yaml`**, o PR fica vermelho com uma mensagem como:

```
[DataCollectionEntryParseError] equipe/maria-souza.yaml failed to parse: bad indentation of a mapping entry
  Location:
    src/content/equipe/maria-souza.yaml:2:7
```

**O que significa:** `bad indentation` = espaço a mais ou a menos no começo de alguma linha. A parte
`:2:7` indica a **linha 2, coluna 7** do arquivo. Volte lá e alinhe as linhas como no exemplo da
receita (cada campo começa colado na margem, sem espaços à esquerda; dentro de listas, os espaços
seguem o padrão do exemplo).

Nos arquivos de **lista** (`publicacoes.yaml`, `midia.yaml`, `analises.yaml`, `seminarios.yaml`,
`pesquisas.yaml`, `textos-discussao.yaml`, `acervo.yaml`, `bancos-de-dados.yaml`,
`mapas-votacao.yaml`, `parceiros.yaml`), a mensagem é um pouco diferente, mas o efeito é o mesmo —
o PR fica **vermelho** e nada é publicado:

```
✖ Erro no conteúdo do site. O build foi interrompido.

  • src/data/publicacoes.yaml (linha 4, coluna 11)
    All mapping items must start at the same column
    Dica: em YAML, todos os campos de um item precisam começar na mesma coluna.

Nada foi publicado. O site continua no ar com a versão anterior.
```

> **Dica que evita 90% dos erros:** para acrescentar um item numa lista, **copie e cole um item
> que já existe** e troque só os valores. Assim a arrumação continua certa.

**Todos os erros deixam o PR vermelho.** Não existe caso em que um erro seu passe despercebido e o
site vá ao ar sem o conteúdo: antes de montar o site, o GitHub roda uma conferência
(`scripts/validar-dados.mjs`) que interrompe tudo se algum arquivo estiver quebrado.

---

## 4. Receitas (uma para cada tarefa)

Em todas as receitas, os campos com **`<preencha aqui>`** são para você substituir. Os campos
marcados como *(opcional)* podem ser apagados se você não tiver a informação — **não** deixe a linha
vazia; apague a linha inteira.

### 4.1. Adicionar um membro da equipe

**Passo 1 — a foto.** Envie a foto para a pasta `public/img/equipe/` (veja "Enviar uma imagem" na
Seção 2). Use um nome sem espaços nem acentos, tudo minúsculo, ex.: `maria-souza.jpg`.

**Passo 2 — o arquivo da pessoa.** Crie um arquivo novo em `src/content/equipe/`, com o nome da
pessoa (minúsculo, sem acento, com hífen), ex.: `maria-souza.yaml`. Conteúdo (modelo real, baseado
na Bruno Schaefer):

```yaml
nome: Maria Souza
cargo: Professora/Pesquisadora
categoria: pesquisadores
foto: /img/equipe/maria-souza.jpg
lattes: http://lattes.cnpq.br/0000000000000000   # (opcional) apague a linha se não tiver
ordem: 100
```

- `categoria`: use **exatamente** um dos valores da Tabela (Seção 5). É o que decide em qual bloco
  da página a pessoa aparece.
- `foto`: escreva o caminho começando com `/img/equipe/` e o **mesmo nome** do arquivo que você
  enviou no Passo 1. Se não houver foto, apague a linha — o site mostra as iniciais no lugar.
- `ordem`: número que define a posição dentro do bloco (menor aparece antes). *(opcional)*
- `email`: se tiver, adicione uma linha `email: pessoa@exemplo.com`. *(opcional)*

### 4.2. Remover um membro da equipe

Abra o arquivo da pessoa em `src/content/equipe/` (ex.: `maria-souza.yaml`), clique no ícone de
**lixeira** (🗑️, no topo, "Delete this file") e faça o "Commit changes" abrindo um PR, como sempre.
(A foto em `public/img/equipe/` pode ficar; não atrapalha. Se quiser, apague do mesmo jeito.)

### 4.3. Publicar uma nova publicação acadêmica

Arquivo: **`src/data/publicacoes.yaml`**. É uma lista: cada publicação começa com `- titulo:`.
Vá até o fim do arquivo e **acrescente um bloco** (dica: copie um bloco parecido que já existe e
troque os valores). Modelo real:

```yaml
- titulo: Nome completo da publicação
  autores: Sobrenome, Nome; Outro, Fulano
  ano: 2025
  tipo: artigo
  revista: Nome da revista            # use com tipo "artigo"; apague se não for
  editora: Cidade, Editora            # use com "livro"/"capitulo"; apague se não for
  paginas: p. 10-25                   # (opcional)
  url: https://exemplo.com/artigo.pdf # (opcional) apague se não tiver
```

- `tipo`: um dos valores da Tabela (`livro`, `capitulo`, `artigo`, `outros`) — decide o bloco onde
  a publicação aparece na página **Publicações Acadêmicas**.
- `ano`: só o número, sem aspas. *(opcional — há uma publicação "no prelo" sem ano.)*
- Mantenha os **dois espaços** no começo das linhas `autores:`, `ano:`, etc. (o `- titulo:` é o
  único que começa com `- `).

### 4.4. Publicar um texto para discussão

Arquivo: **`src/data/textos-discussao.yaml`**. Acrescente ao fim (modelo real, baseado no do Matteo
Manes):

```yaml
- titulo: Título do texto para discussão
  autores: Nome do Autor
  ano: 2025
  url: https://exemplo.com/texto.pdf   # (opcional)
  resumo: >
    Resumo do texto, um parágrafo. Pode ser longo — mantenha o recuo
    das linhas seguintes alinhado a este, como neste exemplo.
```

- `ano` aqui é **obrigatório** (número, sem aspas).

### 4.5. Adicionar uma análise de conjuntura eleitoral

Arquivo: **`src/data/analises.yaml`**. Cada análise pode ter vários arquivos para download.
Modelo real:

```yaml
- titulo: Título da análise
  ciclo: '2024'
  periodo: Eleições Municipais 2024     # (opcional)
  descricao: Uma frase descrevendo a análise.   # (opcional)
  arquivos:
  - rotulo: PDF
    url: https://exemplo.com/analise.pdf
  - rotulo: Tabela
    url: https://exemplo.com/tabela.pdf
```

- `ciclo`: escreva entre aspas (ex.: `'2024'`). É o que agrupa as análises na página.
- `arquivos`: pode ter um ou vários pares `rotulo` + `url`. Se não houver nenhum arquivo, escreva
  `arquivos: []` na mesma linha.

### 4.6. Adicionar um evento

É **um arquivo por evento**, em `src/content/eventos/`. Crie um arquivo novo com um nome curto,
minúsculo e com hífens, ex.: `seminario-eleicoes-2026.md`. Modelo real:

```markdown
---
titulo: Nome do evento
data: '2026-03-15'
descricao: Um resumo do evento.       # (opcional)
imagem: /img/eventos/nome-da-imagem.jpg   # (opcional) envie a imagem para public/img/eventos/
url: https://exemplo.com/evento       # (opcional)
---

Texto completo do evento aqui embaixo (pode ter vários parágrafos).
```

- A parte entre as duas linhas de `---` são os dados; o texto que vem **depois** é o corpo.
- `data`: sempre no formato **`'ano-mês-dia'`** entre aspas (ex.: `'2026-03-15'`). Os eventos
  aparecem do mais novo para o mais antigo.
- `titulo` e `data` são obrigatórios; o resto é opcional.

### 4.7. Adicionar um seminário

Arquivo: **`src/data/seminarios.yaml`**. Acrescente ao fim (modelo real):

```yaml
- titulo: Título da apresentação
  apresentador: Nome de quem apresentou
  instituicao: IESP-UERJ        # (opcional)
  data: '2026-05-20'            # (opcional)
  ano: 2026
```

- `titulo`, `apresentador` e `ano` são obrigatórios. Os seminários são agrupados por **ano**.

### 4.8. Adicionar uma aparição na mídia ("Na Mídia")

Arquivo: **`src/data/midia.yaml`**. Acrescente ao fim (modelo real):

```yaml
- titulo: Título da matéria
  autores: Nome do entrevistado/autor   # (opcional)
  veiculo: Nome do jornal/site          # (opcional)
  data: '2026-04-24'                    # (opcional) pode ser só o ano: '2010'
  tipo: virtual
  url: https://exemplo.com/materia      # (opcional)
```

- `tipo`: um dos valores da Tabela (`impressa`, `virtual`, `audiovisual`) — decide o bloco onde a
  matéria aparece. É o **único campo obrigatório** além do `titulo`.

### 4.9. Mudar o texto de uma página

Os textos das páginas ficam em **`src/content/paginas/`**, um arquivo por página
(ex.: `acervo.md`, `pesquisas.md`, `institucional.md`, `home.md`). Abra o arquivo, clique no lápis
e edite o texto normalmente. A parte de cima, entre as linhas `---`, é o título/descrição; o texto
abaixo é o conteúdo da página. Você pode editar os parágrafos à vontade — só **não apague** as
linhas `---` do topo nem o `titulo:`.

### 4.10. Trocar o e-mail ou o endereço de contato

Arquivo: **`src/data/site.yaml`**. Abra, clique no lápis e troque só o valor à **direita dos
dois-pontos**. Nunca mude o nome do campo (a palavra à esquerda dos dois-pontos):

```yaml
  email: acervo-doxa@iesp.uerj.br
  endereco: Rua da Matriz, 82, Botafogo — Rio de Janeiro, RJ
  cep: 22260-100
```

Por exemplo, para trocar o e-mail, mude apenas `acervo-doxa@iesp.uerj.br`. Cuidado para **não**
digitar errado o nome do campo (`email`, `endereco`, `cep`): se escrever `emial`, o PR fica vermelho
(veja o Erro 3). O e-mail de contato aparece no rodapé de todas as páginas e na página do Acervo.

### 4.11. Adicionar um projeto

Um **projeto** é uma iniciativa do laboratório com entrega pública: uma plataforma, um painel, uma
pesquisa aplicada. Exemplos que já estão no site: Vota Aí, Eleições Rio e São Paulo 2024, Pesquisa
COVID, Geografia do Voto.

Crie um arquivo **novo** em **`src/content/projetos/`**. O nome do arquivo vira o endereço da
página: `mapa-da-desinformacao.md` → `.../projetos/mapa-da-desinformacao/`. Use só letras
minúsculas, números e hífens — **sem espaços e sem acentos**.

```markdown
---
titulo: "Nome do Projeto"
resumo: "Uma ou duas frases. É o que aparece no cartão da lista de projetos."
periodo: "2025 — presente"          # opcional
status: "ativo"                      # opcional: ativo | concluido
imagem: "/img/projetos/nome.jpg"     # opcional (envie a imagem para public/img/projetos/)
url: "https://site-do-projeto.br"    # opcional: o site externo do projeto
rotulo_url: "Acessar a plataforma"   # opcional: o texto do botão
links:                               # opcional: outros links (internos ou externos)
  - rotulo: "Baixar os dados (CSV)"
    url: "/dados/arquivo.csv"
destaque: false                      # true = o projeto ganha um cartão grande na lista
---

Aqui vai a descrição longa, em parágrafos normais. Pode usar **negrito** e *itálico*.
```

Só o `titulo` e o `resumo` são obrigatórios. **Não invente `status`**: se você não souber se o
projeto está em andamento ou concluído, apague a linha — a etiqueta simplesmente não aparece.

> ⚠️ **Importante:** crie o arquivo **também** em `extracao/dados/projetos/`, com o mesmo conteúdo.
> Existe um script (`scripts/converter-conteudo.py`) que regenera a pasta `src/content/projetos/` a
> partir de `extracao/` — se alguém rodar esse script, um projeto que só exista em `src/` é apagado.
> Na dúvida, peça ajuda a quem cuida do site.

---

## 5. Tabela de valores permitidos

Alguns campos só aceitam valores de uma lista fechada. Se digitar qualquer outra coisa (ou com
acento, ou no plural), o PR fica vermelho. Use **exatamente** o que está na coluna "Escreva assim"
(tudo minúsculo, sem acento).

### `categoria` — arquivos de membro (`src/content/equipe/*.yaml`)

| Escreva assim | Onde a pessoa aparece na página |
|---|---|
| `coordenacao` | Coordenação |
| `pesquisadores` | Pesquisadores |
| `pos-doutorando` | Pós-doutorandos |
| `aluno` | Alunos de Pós-graduação |
| `assistente` | Assistentes de Pesquisa |
| `associado` | Pesquisadores Associados |

### `tipo` — publicações (`src/data/publicacoes.yaml`)

| Escreva assim | Bloco na página |
|---|---|
| `livro` | Livros |
| `capitulo` | Capítulos de Livro |
| `artigo` | Artigos em Revista Científica |
| `outros` | Outras Produções |

### `tipo` — na mídia (`src/data/midia.yaml`)

| Escreva assim | Bloco na página |
|---|---|
| `impressa` | Mídia Impressa |
| `virtual` | Mídia Virtual |
| `audiovisual` | Mídia Audiovisual |

### `status` — pesquisas (`src/data/pesquisas.yaml`)

| Escreva assim | Etiqueta na página |
|---|---|
| `tese` | Teses e Dissertações |
| `andamento` | Em Andamento |
| `concluida` | Concluídas |

> Existem outras listas fechadas em arquivos que raramente mudam (ex.: `eleicao` em
> `mapas-votacao.yaml` aceita só `Majoritaria` ou `Proporcional`). Se for mexer nesses, confira a
> mensagem de erro do PR — ela sempre mostra os valores aceitos entre aspas.

---

## 6. O que você NÃO deve mexer

Estas pastas e arquivos são o "motor" do site. Mexer neles pode quebrar tudo, e não é tarefa de
quem cuida do conteúdo:

- `src/components/`
- `src/layouts/`
- `src/pages/`
- `src/content.config.ts`
- `astro.config.mjs`
- `package.json` e `package-lock.json`
- as pastas `legacy-hugo/`, `extracao/`, `scripts/` e `node_modules/`

Se você achar que precisa mudar algo aí dentro, **não mude** — fale com a pessoa responsável pelo
site (o desenvolvedor/orientador do time). O mesmo vale se um PR ficar vermelho com uma mensagem que
não está neste guia: mande o link do PR para quem cuida do site.

---

## 7. Rodar o site no seu computador (opcional, para quem quiser)

Você **não precisa** disso para editar o conteúdo — tudo funciona pelo navegador (Seção 2). Mas se
quiser ver as mudanças na sua máquina antes de propor, é assim:

1. Instale o [Node.js](https://nodejs.org/) (versão 20 ou mais nova) e o
   [Git](https://git-scm.com/).
2. No terminal:

```bash
git clone https://github.com/doxa-iesp/doxa-iesp.github.io.git
cd DOXA
npm ci        # baixa as dependências (só na primeira vez)
npm run dev   # abre o site em http://localhost:4321/ com recarga automática
```

Enquanto o `npm run dev` estiver rodando, cada arquivo que você salvar aparece na hora no navegador.
Para parar, aperte `Ctrl + C` no terminal.

> **Não existe** um endereço público de "prévia" para cada PR. O que existe é o arquivo `site-dist`
> (o site já montado) que você pode **baixar** na aba "Checks" do PR — útil para conferir uma
> alteração num arquivo de lista antes de aprovar (veja o aviso da Seção 3).

---

## Quando pedir ajuda

- O PR ficou **vermelho** e a mensagem não está na Seção 3 → mande o link do PR para quem cuida do
  site.
- Você editou um arquivo de **lista** e os itens sumiram da página (mesmo com o PR verde) → veja o
  aviso da Seção 3 e, na dúvida, peça conferência.
- Deu vontade de mexer em algo da Seção 6 → não mexa; pergunte antes.

Na dúvida, **não aprove/merge o PR**. Um PR parado não faz mal nenhum; só entra no ar quando for
aprovado.
