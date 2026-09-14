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

O endereço do site é **https://lab-doxa.org.br/**.
O repositório fica em **https://github.com/doxa-iesp/doxa-iesp.github.io**.

> O site antigo, em WordPress, usava esse mesmo endereço e **não existe mais**. Por isso, nunca
> copie para o site um link que comece com `www.lab-doxa.org.br/...` achado num e-mail ou documento
> antigo: ele não leva ao arquivo, leva a uma página de erro deste site.

**Regra única: todo o conteúdo se edita em `src/`** (`src/content/` e `src/data/`), e as imagens e
PDFs vão em `public/`. A pasta `extracao/` guarda a cópia do site antigo como registro histórico —
não precisa (nem deve) ser tocada para corrigir ou acrescentar nada.

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

### Criar um arquivo novo (membro da equipe, evento, projeto ou destaque)

Alguns conteúdos são **um arquivo por item** (cada pessoa da equipe, cada evento, cada projeto e
cada destaque da página inicial é um arquivo). Para criar um:

1. No repositório, entre na pasta certa (ex.: `src/content/equipe/`).
2. Clique em **"Add file" → "Create new file"** (Adicionar arquivo → Criar novo arquivo).
3. No campo do nome, digite o nome do arquivo (ex.: `maria-souza.yaml`).
4. Cole o conteúdo (veja as Receitas), e siga do passo 5 acima ("Commit changes").

### Enviar uma imagem ou um PDF

1. Entre na pasta certa: `public/img/equipe/` para fotos, `public/img/eventos/` para imagens de
   evento, `public/pdfs/<assunto>/` para PDFs (`analises`, `pesquisas`, `textos-discussao`,
   `livros`, `eventos`, `midia`).
2. Clique em **"Add file" → "Upload files"** (Enviar arquivos).
3. Arraste o arquivo, e siga para "Commit changes" (marcando "Create a new branch...").

Use nomes **sem espaços e sem acentos** (ex.: `relatorio-eleicoes-2026.pdf`). Para linkar o arquivo
num campo `url:`, escreva o caminho **a partir de `public/`, começando com `/`**: o arquivo
`public/pdfs/analises/relatorio-eleicoes-2026.pdf` vira `url: /pdfs/analises/relatorio-eleicoes-2026.pdf`.

### Antes de pôr um link de fora do site

Abra o link numa **janela anônima** do navegador e confira que ele mostra a matéria certa. Links
de jornal e de blog morrem: um domínio abandonado pode ser comprado por outra pessoa e passar a
mostrar propaganda ou golpe. Se a matéria sumiu, procure uma cópia no
[Wayback Machine](https://web.archive.org/) (cole o endereço antigo na busca e escolha uma data
próxima à da publicação). Se nem lá existir, **deixe o item sem `url`** — é melhor do que um link
que leva a outro lugar. E nunca use link de e-mail (Gmail) ou de pasta pessoal do Drive: só abre
para quem tem a senha.

---

## 3. A rede de segurança: o PR fica verde ou vermelho

Depois que você cria um pull request, o GitHub roda uma conferência automática. Você vê o resultado
na própria página do PR e na aba **"Checks"** (Verificações):

- ✅ **Verde** = está tudo certo. A mudança pode ser aprovada e vai para o ar.
- ❌ **Vermelho** = tem algo errado. **O site NÃO é atualizado** enquanto estiver vermelho — ninguém
  vê o erro no site publicado. Você conserta com calma (é só editar o mesmo PR de novo).

### Onde ver o que deu errado

Na página do PR, clique em **"Details"** ao lado da verificação vermelha (ou na aba **"Checks"**).
Abra o passo **"Build do Astro"** e role até a parte vermelha da tela: a mensagem de erro aparece
ali. Abaixo estão as mensagens mais comuns e o que cada uma quer dizer.

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

#### Erro 3 — Você escreveu um nome de campo errado no `site.yaml` ou no `bancos-de-dados.yaml`

Exemplo: escrever `emial:` no lugar de `email:` no arquivo de contato. A mensagem é:

```
[InvalidContentEntryDataError] configuracao → geral data does not match collection schema.

  email: Required
  : Unrecognized key: "emial"
```

**O que significa:** `email: Required` = o campo `email` é obrigatório e sumiu.
`Unrecognized key: "emial"` = você criou uma linha com um nome (`emial`) que o site não reconhece.
Quase sempre é um erro de digitação no começo da linha. Corrija o nome do campo.

O `bancos-de-dados.yaml` confere os nomes de campo do mesmo jeito. Lá, além de erro de digitação,
o aviso aparece se alguém usar um campo que não existe mais — por exemplo `download:`, que foi
trocado pela lista `arquivos:` (receita 4.17): `Unrecognized key: "download"`.

#### Erro 4 — A "arrumação" (indentação) do arquivo ficou torta

Os espaços no começo de cada linha importam. Se você mexer neles sem querer — em qualquer arquivo
de conteúdo: membro, evento, projeto, destaque, página, `site.yaml` ou uma lista como
`publicacoes.yaml` —, o PR fica vermelho com uma mensagem como:

```
✖ Erro no conteúdo do site. O build foi interrompido.

  • src/data/publicacoes.yaml (linha 4, coluna 11)
    All mapping items must start at the same column
    Dica: em YAML, todos os campos de um item precisam começar na mesma coluna.

Nada foi publicado. O site continua no ar com a versão anterior.
```

**O que significa:** espaço a mais ou a menos no começo de alguma linha. A parte `(linha 4,
coluna 11)` diz onde olhar. Volte lá e alinhe as linhas como no exemplo da receita (num arquivo de
membro, cada campo começa colado na margem; dentro de listas, os espaços seguem o padrão do
exemplo). A frase em inglês muda conforme o erro, mas o arquivo e a linha sempre aparecem.

#### Erro 5 — Um item ou arquivo sumiu

```
  • src/content/projetos
    Só 3 arquivos, esperados pelo menos 4. Algum arquivo foi apagado por engano?
    Se a remoção foi de propósito, ajuste o mínimo em scripts/validar-dados.mjs.
```

**O que significa:** a conferência sabe quantos itens cada lista tem, mais ou menos, e desconfia
quando muitos somem de uma vez — o sinal típico de um trecho apagado sem querer. Se você apagou
**de propósito** (um projeto que saiu do site, por exemplo), peça a quem cuida do site para ajustar
o mínimo; não é algo para o estagiário mexer.

#### Erro 6 — Cópias de arquivo (nome 2, nome 3…)

```
  • 1 cópia(s) de arquivo com número no fim do nome, que virariam itens repetidos no site:
      src/content/equipe/felipe-lamarca 2.yaml
    Apague as cópias; o original, sem o número no fim, fica.
```

**O que significa:** existe um arquivo (ou uma pasta) igual a outro, com um número no fim do nome
— `felipe-lamarca 2.yaml` ao lado de `felipe-lamarca.yaml`. Cada cópia viraria uma pessoa, evento
ou projeto repetido na página. Confira que é mesmo uma cópia e apague; o original, sem o número,
fica. Um arquivo com número no nome e **sem** original ao lado (ex.: `TD 2.pdf`) não é acusado.

#### Erro 7 — Link para o site antigo ou para o Gmail

```
  • src/data/midia.yaml (linha 199)
    Este link aponta para o site antigo, que não existe mais.
    Procure o endereço atual do conteúdo; se não existir, apague o link.
```

**O que significa:** o endereço começa com `www.lab-doxa.org.br` (o WordPress antigo, que saiu do
ar — hoje esse endereço mostra uma página de erro deste site) ou com `mail.google.com` (um e-mail,
que só abre para quem tem a senha). Veja "Antes de pôr um link de fora do site", na Seção 2.

#### Erro 8 — Link interno quebrado

No passo **"Links internos"** do PR:

```
✖ 1 link(s) interno(s) quebrado(s) no site montado:

  • producao/analises-de-conjuntura/index.html
      /pdfs/analises/relatorio-eleicoes-2026.pdf
```

**O que significa:** uma página do site aponta para um arquivo ou endereço do próprio site que não
existe. Quase sempre é um PDF que não foi enviado para `public/`, ou um nome digitado diferente do
arquivo (maiúsculas, acentos e espaços contam). Envie o arquivo ou corrija o endereço.

> **Dica que evita 90% dos erros:** para acrescentar um item numa lista, **copie e cole um item
> que já existe** e troque só os valores. Assim a arrumação continua certa.

**Todos os erros deixam o PR vermelho.** Não existe caso em que um erro seu passe despercebido e o
site vá ao ar sem o conteúdo: antes de montar o site, o GitHub roda uma conferência
(`scripts/validar-dados.mjs`) que interrompe tudo se algum arquivo estiver quebrado, e depois de
montar confere que todo link interno leva a algo que existe.

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
no do Bruno Schaefer):

```yaml
nome: Maria Souza
cargo: Professora/Pesquisadora
categoria: pesquisadores
foto: /img/equipe/maria-souza.jpg
lattes: https://lattes.cnpq.br/0000000000000000   # (opcional) apague a linha se não tiver
site: https://mariasouza.com                      # (opcional) página pessoal
ordem: 100
```

- `categoria`: use **exatamente** um dos valores da Tabela (Seção 5). Ela vira a etiqueta do card
  ("Pesquisa", "Pós-graduação"…) e, com a `ordem`, define a posição da pessoa na página.
- `cargo`: o cargo como a pessoa quer que apareça. Se ele só repetir a etiqueta (ex.: "Pesquisadora
  Associada" com a categoria `associado`), o card esconde o cargo sozinho.
- `foto`: escreva o caminho começando com `/img/equipe/` e o **mesmo nome** do arquivo que você
  enviou no Passo 1. Se não houver foto, apague a linha — o site mostra as iniciais no lugar.
- `ordem`: número que define a posição (menor aparece antes; coordenação usa `0`,
  pesquisadores `100`, pós-doutorado `200`, pós-graduação `300`, assistentes `400`, associados
  `500`). *(opcional)*
- `lattes`, `site` e `email` viram links no card. *(todos opcionais)*

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
- `ano`: só o número, sem aspas. *(opcional — use para uma publicação "no prelo" que ainda não
  tem ano; sem `ano`, a página mostra "no prelo".)*
- **Ordem na página:** dentro de cada bloco, do ano mais recente para o mais antigo; entre
  publicações do **mesmo ano**, vale a posição no arquivo (a que está mais acima aparece antes).
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
- **Ordem na página:** dentro de um ciclo, as análises aparecem na ordem do arquivo. Para uma
  análise nova aparecer antes das outras do mesmo ciclo, ponha o bloco acima delas.
- `arquivos`: pode ter um ou vários pares `rotulo` + `url`. Se não houver nenhum arquivo, escreva
  `arquivos: []` na mesma linha.

### 4.6. Adicionar um evento

É **um arquivo por evento**, em `src/content/eventos/`. Crie um arquivo novo com um nome curto,
minúsculo e com hífens, ex.: `seminario-eleicoes-2026.md`. Modelo real:

```markdown
---
titulo: Nome do evento
data: '2026-03-15'
descricao: Quando, onde, quem fala. É o texto que aparece no card.   # (opcional)
imagem: /img/eventos/nome-da-imagem.jpg   # (opcional) envie a imagem para public/img/eventos/
url: https://exemplo.com/evento       # (opcional) vira o botão "Saiba mais"
anexos:                               # (opcional) arquivos para baixar
- /pdfs/eventos/cartaz-do-evento.pdf
---
```

- A parte entre as duas linhas de `---` são os dados. **O que aparece no site é a `descricao`**:
  não há página própria para cada evento, então um texto escrito abaixo do segundo `---` não é
  mostrado em lugar nenhum. Escreva tudo o que importa na `descricao`.
- `data`: a data **em que o evento acontece** (não a de quando você o publicou), sempre no formato
  **`'ano-mês-dia'`** entre aspas (ex.: `'2026-03-15'`). Os eventos aparecem do mais novo para o
  mais antigo.
- `anexos`: cada linha é um arquivo enviado para `public/` (veja "Enviar uma imagem ou um PDF").
  O botão diz "Baixar PDF", "Baixar imagem" etc., conforme o tipo do arquivo.
- `titulo` e `data` são obrigatórios; o resto é opcional.
- Sem `url` e sem anexo, o card aparece só com o texto — sem botão, e está tudo bem.

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

- `tipo`: um dos valores da Tabela (`impressa`, `virtual`, `audiovisual`) — vira a etiqueta da
  matéria e decide em qual aba de filtro ela aparece. É o **único campo obrigatório** além do
  `titulo`.
- A página organiza tudo **por ano**, a partir da `data`: não precisa pôr a matéria em lugar
  nenhum específico do arquivo. Sem `data`, ela vai para um grupo "Sem data" no fim. Duas matérias
  com a mesma data (ou só com o mesmo ano) aparecem na ordem do arquivo.

### 4.9. Mudar o texto de uma página

Os textos das páginas ficam em **`src/content/paginas/`**, um arquivo por página
(ex.: `acervo.md`, `pesquisas.md`, `institucional.md`, `home.md`). Abra o arquivo, clique no lápis
e edite o texto normalmente. A parte de cima, entre as linhas `---`, é o título/descrição; o texto
abaixo é o conteúdo da página. Você pode editar os parágrafos à vontade — só **não apague** as
linhas `---` do topo nem o `titulo:`.

A `descricao` aparece logo abaixo do título da página e é também o resumo que o Google e o WhatsApp
mostram quando alguém compartilha o link: escreva uma frase que diga o que a página tem.

Três páginas têm a introdução escrita **no código**, e não num arquivo de `src/content/paginas/`:
Publicações Acadêmicas, Análises de Conjuntura e Projetos. Se precisar mudar o texto delas, peça a
quem cuida do site.

### 4.10. Trocar o e-mail ou o endereço de contato

Arquivo: **`src/data/site.yaml`**. Abra, clique no lápis e troque só o valor à **direita dos
dois-pontos**. Nunca mude o nome do campo (a palavra à esquerda dos dois-pontos):

```yaml
  email: acervo-doxa@iesp.uerj.br
  endereco: Rua da Matriz, 82, Botafogo, Rio de Janeiro, RJ
  cep: 22260-100
```

Por exemplo, para trocar o e-mail, mude apenas `acervo-doxa@iesp.uerj.br`. Cuidado para **não**
digitar errado o nome do campo (`email`, `endereco`, `cep`): se escrever `emial`, o PR fica vermelho
(veja o Erro 3). O e-mail de contato aparece no rodapé de todas as páginas e na página do Acervo.

No mesmo arquivo ficam:

- `youtube`, `instagram` e `twitter`: os perfis do DOXA, que aparecem no rodapé. Um campo vazio
  (ou sem a linha) simplesmente não aparece. Hoje só o YouTube está preenchido.
- `video_destaque` e `video_documentario`: os dois vídeos da página do Acervo. O valor é só o
  **código** do vídeo no YouTube — o que vem depois de `watch?v=` no endereço (em
  `https://www.youtube.com/watch?v=Ns3jYjf7hx4`, o código é `Ns3jYjf7hx4`).
- `catalogo_acervo` e `formulario_acervo`: o link da planilha do catálogo e o formulário de
  pedido de material, os dois usados na página do Acervo.

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
embed: "https://app.powerbi.com/…"   # opcional: painel (Power BI) ou vídeo mostrado dentro da página
links:                               # opcional: outros links (internos ou externos)
  - rotulo: "Baixar os dados (CSV)"
    url: "/dados/arquivo.csv"
ordem: 5                             # opcional: posição na lista (menor aparece antes)
---

Aqui vai a descrição longa, em parágrafos normais. Pode usar **negrito** e *itálico*.
```

Só o `titulo` e o `resumo` são obrigatórios. **Não invente `status`**: se você não souber se o
projeto está em andamento ou concluído, apague a linha — o projeto vai para o grupo "Outros
projetos" da lista, e está tudo bem.

Para **tirar um projeto do site**, apague o arquivo dele (lixeira, como na receita 4.2). Como hoje
há exatamente quatro projetos, o PR fica vermelho com o Erro 5: peça a quem cuida do site para
ajustar o mínimo.

### 4.12. Trocar os destaques da página inicial

A faixa **"Em destaque"**, logo abaixo da apresentação na página inicial, é a vitrine do
laboratório: é ali que entram um livro novo, um evento que acabou de acontecer, uma plataforma
lançada. Ela é curada — ou seja, alguém escolhe o que aparece.

Cada destaque é um arquivo em **`src/content/destaques/`**. Para publicar um novo, crie um arquivo
com nome em letras minúsculas e hífens (`livro-a-decisao-do-voto.md`):

```markdown
---
titulo: "Nome do que está em destaque"
etiqueta: "Livro"                     # opcional: Livro, Evento, Projeto, Documentário…
resumo: "Uma ou duas frases explicando o que é e por que interessa."
imagem: "/img/destaques/nome.jpg"     # opcional (envie a imagem para public/img/destaques/)
url: "https://..."                    # link externo OU um arquivo do site: /pdfs/livros/x.pdf
rotulo_url: "Baixar o livro (PDF)"    # o texto do botão
ordem: 1                              # 1 aparece antes de 2
ativo: true                           # false = some do site sem apagar o arquivo
---
```

Três coisas que ajudam:

- **Para tirar um destaque do ar, troque `ativo: true` por `ativo: false`.** Não precisa apagar o
  arquivo: no ano que vem, se o assunto voltar, é só religar.
- **Capas e cartazes funcionam melhor.** A imagem aparece inteira, sem corte, então pode ser
  vertical (capa de livro, cartaz de evento).
- Sem `url`, o card aparece sem botão — o que é útil para um aviso curto.

### 4.13. Acrescentar um mapa de votação

Os PDFs dos mapas **não ficam no GitHub** — são grandes demais. Ficam no **Google Drive do DOXA**,
na conta do acervo (`acervo-doxa@iesp.uerj.br`), na pasta **Acervo Doxa (NEW) › Site DOXA — Mapas de
votação**. O site só guarda o link de cada um.

1. **Suba o PDF para essa pasta** do Drive. A pasta já está compartilhada como "qualquer pessoa com
   o link", e o arquivo herda isso — não precisa compartilhar de novo.
2. **Copie o link**: clique com o botão direito no arquivo › Compartilhar › Copiar link. Ele tem a
   cara `https://drive.google.com/file/d/…/view?usp=sharing`.
3. **Confira numa janela anônima** do navegador que o link abre sem pedir login.
4. **Acrescente o mapa em `src/data/mapas-votacao.yaml`** (modelo real):

   ```yaml
   - titulo: PT
     ano: 2022
     cargo: Deputado Federal
     eleicao: Proporcional
     url: https://drive.google.com/file/d/…/view?usp=sharing
   ```

   Nos mapas de eleição majoritária (governador, senador…), o `titulo` é o próprio cargo.
5. **Acrescente a mesma linha no catálogo para download**, `public/dados/mapas-votacao.csv`, na
   ordem das colunas `ano,eleicao,cargo,turno,titulo,url`:
   `2022,Proporcional,Deputado Federal,,PT,https://drive.google.com/file/d/…/view?usp=sharing`

Dois cuidados com o Drive:

- **Mover ou renomear** o arquivo ou a pasta **não quebra** o link.
- **Apagar e subir de novo quebra**: o arquivo ganha outro link, e o antigo passa a dar erro. Para
  trocar um mapa por uma versão corrigida, use no Drive "Gerenciar versões" › "Enviar nova versão",
  que mantém o mesmo link.

### 4.14. Adicionar uma pesquisa (tese, dissertação ou projeto)

Arquivo: **`src/data/pesquisas.yaml`**. Acrescente ao fim (modelo real):

```yaml
- titulo: Título da tese ou do projeto
  autor: Nome de quem fez              # (opcional)
  ano: 2026                            # (opcional) número, sem aspas
  orientador: Nome do orientador       # (opcional)
  instituicao: IESP-UERJ               # (opcional)
  status: tese
  url: /pdfs/pesquisas/nome-do-arquivo.pdf   # (opcional) link externo ou PDF do site
```

- `status`: um dos valores da Tabela (`tese`, `andamento`, `concluida`) — decide a aba da página
  **Pesquisas** onde a pesquisa aparece.
- Uma tese costuma estar na BDTD da UERJ; o link de lá serve como `url`. Se o PDF for do próprio
  laboratório, envie para `public/pdfs/pesquisas/`.
- **Ordem na página:** por tipo, depois do ano mais recente para o mais antigo, depois pelo título.
  A posição no arquivo não importa.

### 4.15. Editar ou remover um evento ou um destaque

**Editar:** abra o arquivo em `src/content/eventos/` ou `src/content/destaques/`, clique no lápis e
troque os valores, como em qualquer outro arquivo.

**Remover um evento:** apague o arquivo (lixeira, como na receita 4.2).

**Tirar um destaque do ar:** troque `ativo: true` por `ativo: false` (receita 4.12). Apague o
arquivo só se tiver certeza de que não vai precisar dele de novo — e mantenha pelo menos um
destaque, senão o PR fica vermelho (Erro 5).

### 4.16. Adicionar um parceiro (faixa "Apoio e parcerias" da página inicial)

1. Envie o logo para `public/img/parceiros/` (PNG com fundo transparente fica melhor).
2. Acrescente ao fim de **`src/data/parceiros.yaml`** (a posição no arquivo não importa: os logos
   aparecem em **ordem alfabética** do `nome`):

```yaml
- nome: Nome da instituição
  arquivo: /img/parceiros/nome-do-logo.png
  url: https://site-da-instituicao.br   # (opcional)
```

### 4.17. Bancos de dados e itens do acervo

Esses arquivos mudam pouco e têm campos mais específicos:

- **Um banco novo** entra ao fim de `src/data/bancos-de-dados.yaml`. Envie os arquivos (CSV ou
  XLSX) para `public/dados/` — um PDF de documentação vai em `public/pdfs/` — e copie um bloco
  existente. Modelo real (o banco de decretos da Pesquisa COVID, com a descrição encurtada):

  ```yaml
  - nome: Decretos municipais de enfrentamento da Covid-19 no Estado do Rio de Janeiro – 2020
    descricao: Decretos do Poder Executivo dos municípios fluminenses sobre a Covid-19.
    cobertura: 87 dos 92 municípios do Estado do Rio de Janeiro; decretos de março a novembro de 2020.
    registros: 2751                        # (opcional) número, sem ponto de milhar
    pagina: /projetos/pesquisa-covid/      # (opcional) página do site sobre a base
    rotulo_pagina: Ver o projeto           # (opcional) texto desse botão; sem ele, "Ver no site"
    arquivos:                              # um par rotulo + url por arquivo para baixar
    - rotulo: Banco de decretos (XLSX)
      url: /dados/pesquisa-covid/DOWNLOAD-2_-BANCO-DE-DADOS_DECRETOS-COVID_RJ_3006.xlsx
    - rotulo: Lista de buscadores legislativos (XLSX)
      url: /dados/pesquisa-covid/DOWNLOAD-1_LISTA-DE-BUSCADORES_DECRETOS.xlsx
    ordem: 4                               # (opcional) posição na página; menor aparece antes
  ```

  - Diga o formato no `rotulo` ("(CSV)", "(XLSX)", "(PDF)"): é o texto do botão.
  - Não escreva dois-pontos seguidos de espaço dentro de `descricao` ou `cobertura` sem pôr o texto
    entre aspas simples — o YAML confunde com um campo novo e o PR fica vermelho (Erro 4).
  - Nomes de campo que o site não conhece, inclusive o antigo `download:`, deixam o PR vermelho
    (Erro 3).
  - Para **tirar um banco do site**, apague o bloco inteiro. Como hoje há exatamente cinco bancos, o
    PR fica vermelho com o Erro 5: peça a quem cuida do site para ajustar o mínimo.
- **Um vídeo novo do acervo** entra em `src/data/acervo.yaml`, copiando um item que já existe: o
  `codigo` da fita, `ano`, `cargo`, `regiao`, `candidatos`, `partidos` e o `url` do vídeo no Google
  Drive (confira numa janela anônima que ele abre sem login). O `codigo` vira a âncora do card,
  então não o troque depois de publicado.

Na dúvida sobre algum campo, peça a quem cuida do site.

### 4.18. O menu do site

O menu (Início, Equipe, Produção, Projetos…) é **código**, em `src/lib/navegacao.ts`. Para
acrescentar, tirar ou renomear um item, peça a quem cuida do site.

---

## 5. Tabela de valores permitidos

Alguns campos só aceitam valores de uma lista fechada. Se digitar qualquer outra coisa (ou com
acento, ou no plural), o PR fica vermelho. Use **exatamente** o que está na coluna "Escreva assim"
(tudo minúsculo, sem acento).

### `categoria` — arquivos de membro (`src/content/equipe/*.yaml`)

| Escreva assim | Etiqueta no card da pessoa |
|---|---|
| `coordenacao` | Coordenação |
| `pesquisadores` | Pesquisa |
| `pos-doutorando` | Pós-doutorado |
| `aluno` | Pós-graduação |
| `assistente` | Assistente |
| `associado` | Pesquisa associada |

### `tipo` — publicações (`src/data/publicacoes.yaml`)

| Escreva assim | Bloco na página |
|---|---|
| `livro` | Livros |
| `capitulo` | Capítulos de livro |
| `artigo` | Artigos em revistas científicas |
| `outros` | Outras produções |

### `tipo` — na mídia (`src/data/midia.yaml`)

| Escreva assim | Etiqueta e aba na página |
|---|---|
| `impressa` | Impressa |
| `virtual` | Virtual |
| `audiovisual` | Audiovisual |

### `status` — pesquisas (`src/data/pesquisas.yaml`)

| Escreva assim | Aba na página |
|---|---|
| `tese` | Teses e dissertações |
| `andamento` | Em andamento |
| `concluida` | Concluídas |

### `status` — projetos (`src/content/projetos/*.md`)

| Escreva assim | Grupo na lista de projetos |
|---|---|
| `ativo` | Em andamento |
| `concluido` | Concluídos |
| *(sem a linha)* | Outros projetos |

> Existem outras listas fechadas em arquivos que raramente mudam (ex.: `eleicao` em
> `mapas-votacao.yaml` aceita só `Majoritaria` ou `Proporcional`). Se for mexer nesses, confira a
> mensagem de erro do PR — ela sempre mostra os valores aceitos entre aspas.

---

## 6. O que você NÃO deve mexer

Estas pastas e arquivos são o "motor" do site. Mexer neles pode quebrar tudo, e não é tarefa de
quem cuida do conteúdo:

- `src/components/`, `src/layouts/`, `src/pages/`, `src/lib/` (onde fica o menu) e `src/styles/`
- `src/content.config.ts`
- `astro.config.mjs`
- `package.json` e `package-lock.json`
- as pastas `scripts/`, `.github/` e `node_modules/`
- a pasta `extracao/`: é a cópia do site antigo, guardada como registro histórico. Nada do que
  está lá aparece no site; corrigir algo ali não muda nada (corrija em `src/`).

Se você achar que precisa mudar algo aí dentro, **não mude** — fale com a pessoa responsável pelo
site (o desenvolvedor/orientador do time). O mesmo vale se um PR ficar vermelho com uma mensagem que
não está neste guia: mande o link do PR para quem cuida do site.

---

## 7. Rodar o site no seu computador (opcional, para quem quiser)

Você **não precisa** disso para editar o conteúdo — tudo funciona pelo navegador (Seção 2). Mas se
quiser ver as mudanças na sua máquina antes de propor, é assim:

1. Instale o [Node.js](https://nodejs.org/) (versão 22.12 ou mais nova — com versão mais velha o
   site não roda) e o
   [Git](https://git-scm.com/).
2. No terminal:

```bash
git clone https://github.com/doxa-iesp/doxa-iesp.github.io.git
cd doxa-iesp.github.io
npm ci        # baixa as dependências (só na primeira vez)
npm run dev   # abre o site em http://localhost:4321/ com recarga automática
```

Enquanto o `npm run dev` estiver rodando, cada arquivo que você salvar aparece na hora no navegador.
Para parar, aperte `Ctrl + C` no terminal.

> **Não existe** um endereço público de "prévia" para cada PR. O que existe é o arquivo `site-dist`
> (o site já montado), que você pode **baixar** na aba "Checks" do PR. Ele não abre com dois
> cliques: os endereços do site começam com `/`, e o navegador não os encontra num arquivo
> solto. Descompacte e sirva a pasta com `npx serve site-dist` (precisa do Node.js, passo 1),
> e abra o endereço que aparecer no terminal.

---

## Quando pedir ajuda

- O PR ficou **vermelho** e a mensagem não está na Seção 3 → mande o link do PR para quem cuida do
  site.
- O PR ficou verde, mas algo não aparece como você esperava no site → mande o link do PR e o
  endereço da página para quem cuida do site.
- Deu vontade de mexer em algo da Seção 6 → não mexa; pergunte antes.

Na dúvida, **não aprove/merge o PR**. Um PR parado não faz mal nenhum; só entra no ar quando for
aprovado.
