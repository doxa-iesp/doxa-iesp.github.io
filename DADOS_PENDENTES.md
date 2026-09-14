# Dados que faltam

Tudo o que **não existe no site antigo** (ou se perdeu com ele) e precisa ser preenchido ou
conferido por alguém do DOXA. O site funciona sem nada disto — os campos são opcionais e as
páginas simplesmente omitem o que falta (nenhum botão morto, nenhum "undefined" na tela).

Ordenado por impacto. Marque `[x]` conforme resolver. O que já foi resolvido está no fim, em
"O que **não** está pendente".

Onde corrigir: **sempre em `src/`** (`src/content/` e `src/data/`). A pasta `extracao/` é registro
histórico da migração e não precisa ser tocada.

---

## 🔴 Alto impacto — o visitante percebe

### 1. Lattes de 9 dos 16 membros da equipe
**Onde:** o campo `lattes:` de cada `src/content/equipe/<nome>.yaml`.
**Por que falta:** a página `/institucional/` do site antigo não publicava Lattes. Os 7 que temos
vieram da página de publicações acadêmicas (Argelina Cheibub Figueiredo, Fernando Meireles,
Fernando Guarnieri, Bruno Schaefer), do site do IESP (Flávia Bozza Martins e Thiago Moreira, em
2026-09-03) e do próprio Felipe Lamarca (2026-09-06).

- [ ] Carolina Botelho — buscado, não achado com confiança suficiente
- [ ] Carolini Silva — buscado, não achado com confiança suficiente
- [ ] Hellen Guicheney — buscado, não achado com confiança suficiente
- [ ] Karime Lima — buscado, não achado com confiança suficiente
- [ ] Larissa Mendes — não buscado
- [ ] Maria Dominguez — buscado, não achado (nome comum, resultados ambíguos)
- [ ] Matteo Manes — buscado, não achado
- [ ] Nara Salles — buscado, não achado com confiança suficiente
- [ ] Natalia Maciel — buscado, não achado com confiança suficiente

A pessoa provavelmente tem Lattes (a maioria aparece em plataformas acadêmicas como
Escavador/ResearchGate/Google Acadêmico), mas essas páginas bloqueiam acesso automatizado e a busca
geral não trouxe o número do Lattes com confiança suficiente para publicar sem risco de atribuir o
currículo errado a alguém. Mais rápido: cada pessoa cola o próprio link. Para adicionar, abra o
arquivo da pessoa em `src/content/equipe/` e acrescente a linha (receita 4.1 do guia):

```yaml
lattes: https://lattes.cnpq.br/0000000000000000
```

### 2. E-mail dos membros (nenhum publicado)
**Onde:** o campo `email:` de cada `src/content/equipe/<nome>.yaml`.
**Por que falta:** o site antigo não publicava nenhum e-mail individual, só o do acervo.
Decidam se querem publicar — expor e-mail atrai spam. Se não quiserem, deixem como está.

- [ ] Decidir se publica e-mail individual
- [ ] Se sim, preencher os 16

*(Existe também o campo `site`, para página pessoal — o card mostra "Site" ao lado do "Lattes".
Preencher é opcional, como todo o resto.)*

### 3. Pesquisa COVID: cinco arquivos da página antiga não foram recuperados

Em 2026-09-13 a página do projeto voltou a ter os downloads que tinha no WordPress. Onze dos 16
foram recuperados (tabela abaixo). Os cinco que faltam não existem em lugar nenhum ao nosso alcance:

- **Nunca arquivados no Wayback Machine:** `DOWNLOAD-3_DISTRIBUICAO-DOS-DECRETOS-POR-TEMA-E-MUNICIPIOS.pdf`,
  `3.2.BIBLIO_LISTAGEM-POR-TEMA.pdf` e `3.3.BIBLIO_LISTAGEM-POR-CITACAO-BRASIL.pdf`.
- **Arquivados, mas cortados em 1 MiB** (a única captura está incompleta):
  `3.4.-BIBLIO_LINKS-ABSTRACTS-POR-TEMA.pdf` e `GUARNIERI-FIGUEIREDO.pdf` (o capítulo "O impacto da
  Covid-19 no comportamento eleitoral do fluminense nas eleições de 2020").

A página foi reescrita sem prometer esses arquivos. O banco de decretos publicado
(`DOWNLOAD-2`) traz o município e o tema de cada decreto, então a informação do `DOWNLOAD-3`
pode ser refeita a partir dele. Os bancos (decretos e surveys) também estão listados em
`/bancos-de-dados/`, desde 2026-09-14.

- [ ] Alguém da equipe do projeto (Argelina Figueiredo, Fernando Guarnieri) tem esses cinco
      arquivos? Se sim, enviar para `public/pdfs/projetos/pesquisa-covid/` com o nome original e
      religar em `src/content/projetos/pesquisa-covid.md`.
- [ ] O capítulo de Guarnieri e Figueiredo tem versão aberta (EdUERJ, SciELO Books)? Se sim,
      pôr o link na página e em `src/data/publicacoes.yaml`.

Arquivos publicados, com a origem de cada um:

| Arquivo | Origem | SHA-256 (início) |
|---|---|---|
| `dados/pesquisa-covid/DOWNLOAD-1_LISTA-DE-BUSCADORES_DECRETOS.xlsx` | cópia em `extracao/bruto/datasets/` | `0855d723333f946f` |
| `dados/pesquisa-covid/DOWNLOAD-2_-BANCO-DE-DADOS_DECRETOS-COVID_RJ_3006.xlsx` | cópia em `extracao/bruto/datasets/` | `c5dcce4912fab9a9` |
| `dados/pesquisa-covid/DADOS_SURVEY_IESPBR_208324-Wed-Dec-16-2020_total.xlsx` | cópia em `extracao/bruto/datasets/` | `6fb2254eeb45b5f0` |
| `dados/pesquisa-covid/DADOS_SURVEY_IESPBR_227821_20211208.xlsx` | cópia em `extracao/bruto/datasets/` | `5e97032e50929ece` |
| `pdfs/projetos/pesquisa-covid/3.1.-BIBLIO_-Introducao_v2.pdf` | Wayback, captura 20241203232812 | `e5efecb61b68511a` |
| `pdfs/projetos/pesquisa-covid/DOWNLOAD-4_…POR-MUNICIPIO.pdf` | Wayback, captura 20241203225231 | `16ffe036b752ab1e` |
| `pdfs/projetos/pesquisa-covid/DOWNLOAD-5_…PARTIDO-NO-GOVERNO.pdf` | Wayback, captura 20241204000052 | `825a631db284b448` |
| `pdfs/projetos/pesquisa-covid/SURVEY_OPINIOES-COMPORTAMENTO-1.pdf` | Wayback, captura 20241203235539 | `8e9e64c9b9429f8f` |
| `pdfs/projetos/pesquisa-covid/Pandemia-e-mercado-de-trabalho-no-Rio-de-Janeiro.pdf` | Wayback, captura 20241204002523 | `f2b2a36c594a4bc3` |

O relatório de mercado de trabalho aparecia duas vezes na página antiga (a versão de 2023 é o mesmo
texto com uma nota interna na primeira linha), e o capítulo de Figueiredo, Guicheney e Lazzari
agora é linkado no SciELO Books, onde saiu em acesso aberto. Antes de publicar os dois bancos dos
surveys, as respostas abertas foram lidas: há o código do painelista da Netquest, mas nenhum nome,
e-mail, telefone, CPF ou endereço de quem respondeu.

### 4. Redes sociais
**Onde:** `src/data/site.yaml`, campos `instagram` e `twitter`
O site antigo só tinha YouTube. Se o DOXA tiver perfis, o rodapé já está pronto para mostrá-los.

- [x] **Pesquisado em 2026-09-03: nenhum Instagram ou Twitter/X próprio do DOXA foi encontrado.**
      (O `@iesp.uerj` no Instagram é do instituto todo, não do laboratório — não é o mesmo perfil.)
      Campos deixados vazios, como estavam.
- [ ] **Achado não previsto: existe uma página do DOXA no Facebook**,
      `facebook.com/doxa.iesp.uerj/`. O schema de `site.yaml` não tem campo para Facebook hoje —
      decidam se vale adicionar (mudança de schema) ou se o Facebook não é prioridade.

---

## 🟠 Médio impacto — dado incompleto, mas honesto

### 5. Coluna `municipio` da base das Capitais está errada **na origem**
**Onde:** `public/dados/programas-eleitorais-capitais.csv`
Os municípios estão rotacionados em relação aos candidatos. Verificado: Eduardo Paes (Rio) aparece
como Florianópolis; Rafael Greca (Curitiba) como Vitória; Elson Pereira (Florianópolis) como
Aracaju. Os outros campos (candidato, partido, propostas) estão corretos.

A página `/bancos-de-dados/` já mostra um aviso visível. **Não corrigimos por adivinhação:** o
deslocamento parece ser de 7 blocos, mas os blocos têm tamanhos diferentes.

- [ ] Recuperar o município correto de cada candidato (fonte: TSE) e regravar o CSV
- [ ] Depois, apagar o campo `aviso` em `src/data/bancos-de-dados.yaml`

### 6. Pesquisas sem link para o texto completo — 30 de 60
**Onde:** `src/data/pesquisas.yaml`, campo `url`
Teses e dissertações costumam estar na BDTD da UERJ. Projetos em andamento não têm texto público.

**Pesquisado em 2026-09-03**, com resultado modesto: das teses/dissertações sem nenhum link (9,
todas de 1995–2018, a maioria da época do IUPERJ, antes da UERJ ter repositório digital), nenhuma
foi encontrada num repositório aberto com confiança suficiente para publicar o link — o padrão
sugere que essas teses simplesmente nunca foram digitalizadas. As demais sem link são pesquisas
"em andamento" ou "concluídas" de projeto (sem tese/dissertação individual associada), para as
quais não existe um "texto completo" único a linkar.

- [ ] Conferir quais das 30 já têm PDF publicado e acrescentar o link (baixo retorno esperado nas
      teses pré-2018; se algum membro tiver a cópia da própria tese, vale subir para
      `public/pdfs/pesquisas/` como foi feito com as outras 20)

### 7. Pesquisas sem ano — 24 de 60
São quase todas **pesquisas de projeto** (em andamento e concluídas), que no site antigo nunca
tiveram data. Das 37 teses e dissertações, só uma não tem ano: *"A Trajetória da Ciência Política
Brasileira: Uma Análise da Produção e da Formação Acadêmica (1966-2014)"*, de Lilian Paula da Costa
Oliveira. Se quiserem ordenar por data, precisam do ano.

- [ ] Ano da tese de Lilian Paula da Costa Oliveira
- [ ] Decidir se vale preencher o das pesquisas de projeto

### 8. Quatro pesquisas concluídas sem autor
A fonte não nomeia um responsável, só lista `Equipe:`. São:
*Eleições Gerais 2002*, *Eleições Municipais 2000*, *Ideologia Política, Persuasão…*, *Eleições 1996*.

- [ ] Definir quem assina cada uma (ou manter sem autor)

### 9. Dados a conferir (achados na revisão de 2026-09-13)

A revisão de texto de 2026-09-13 corrigiu o que era erro evidente. O que depende de conferir na
fonte, ou de quem conhece o material, ficou como estava e está listado aqui.

**Títulos de obras publicadas** — podem ter vindo com erro do site antigo, mas só se muda título
de obra conferindo na publicação (DOI, SciELO, página da editora):

- [ ] `publicacoes.yaml`: "Corrupção, Como e por quê seu dinheiro sai pelo ladrão" (provável:
      "Corrupção: como e por que seu dinheiro sai pelo ladrão")
- [ ] `publicacoes.yaml`: "Mulheres e representação política: **25 de** estudos sobre cotas" (falta
      "anos"?)
- [ ] `publicacoes.yaml`: "…del Ejecutivo **em** América Latina" (em espanhol seria "en")
- [ ] `publicacoes.yaml`: "The political System of Brazil"; "Entrevista a Fabio Kersche" (Fábio
      Kerche?); "Prefácio do livro O presidencialismo **da** Coalizão"
- [ ] `publicacoes.yaml`: o livro "Política Local no Estado do Rio de Janeiro – As eleições municipais
      de 2020" aparece com outro título num capítulo ("As eleições municipais de 2020 no Estado do
      Rio de Janeiro"); o título publicado pela EdUERJ parece ser *Política local no estado do Rio de
      Janeiro: disputa partidária e comportamento político nas eleições municipais de 2020*
- [ ] `publicacoes.yaml`: "Estudos Legislativos em Perspectiva Comparada" ainda diz "Política
      Comparada, **no prelo**" (ano 2022). Já saiu?
- [ ] `publicacoes.yaml`: "O Governo Bolsonaro e a Conjuntura Política Pré-Eleitoral" e "O governo
      Bolsonaro e a conjuntura eleitoral" (mesmos autores, Cadernos Adenauer, 2022) — são o mesmo
      artigo?
- [ ] `pesquisas.yaml`: "câmara dos deputados", "A (des) construção", "porque isso interessa",
      "decisão do voto em lula", "Do bolso as urnas" — minúsculas e crase em títulos de teses

**Nomes que podem estar errados:**

- [ ] `acervo.yaml`: "Hermani Fortuna" (candidato a presidente pelo PSC em 1994 — seria
      "Hernani"?), "Lúcia Solto" ("Souto"?), "Alexandre Stoduto", "Armando Corrêa"
- [ ] `pesquisas.yaml`: "Luana Costal" ("Costa"?)

**Dados trocados na fonte:**

- [ ] `pesquisas.yaml`: a descrição da tese de Vladimyr Lombardo Jorge mistura dois registros
      ("Orientador: Adam Przeworski. Tese (doutorado) – Universidade de Chicago")
- [ ] `pesquisas.yaml`: Cloves Oliveira e Luiz Ademir de Oliveira apontam para o mesmo PDF
      (`OLIVEIRA_2005.pdf`) — um dos dois está com o arquivo errado
- [ ] `pesquisas.yaml`: a descrição de *Eleições Municipais 2000* termina cortada ("Este projeto foi
      c e já apresentou os seguintes produtos:"), e a de *Eleições Gerais 2002* promete "as
      seguintes áreas" sem listá-las (hoje as descrições de pesquisa não aparecem no site)
- [ ] O evento *Coordenadora do DOXA recebe prêmio de Excelência Acadêmica da Anpocs* está com a
      data do post (2022-09-01); o prêmio é a edição 2021. Qual foi a data da premiação?
- [ ] `mapas-votacao.yaml`: os itens 90 e 91 (PV, 2002, Deputado Federal) são o **mesmo arquivo** —
      `PV-DF2002.pdf` e `PV-DF2002-1.pdf` têm o mesmo SHA-256 em `extracao/dados/mapas-no-drive.csv`.
      O site antigo já mostrava os dois. Por isso a página lista "PV" duas vezes em 2002 e o total é
      273. Decidir se um deles sai (o contador da home passaria a 272).

---

## 🟡 Baixo impacto — cosmético ou de arquivo

### 10. Nove itens de "Na Mídia" sem link

- Duas matérias impressas nunca tiveram URL na fonte (*"A polarização do vírus"*, Valor;
  *"Desconstruindo Mitos"*, Pesquisa Fapesp).
- Cinco itens audiovisuais são vídeos sem link publicado.
- **Dois perderam o link em 2026-09-13**, por não haver cópia pública: *"O mosaico bolsonarista"*
  (meio político), que apontava para um anexo privado do Gmail, e *"Apoio nas ruas definirá futuro
  do confronto de Bolsonaro com Congresso"* (Folha), que apontava para um clipping do WeSeek fora
  do ar, com captura vazia no Wayback Machine.

**Pesquisado em 2026-09-03:** achado 1 de 8 com confiança alta — o documentário *"Arquitetos do
Poder"* (`youtube.com/watch?v=hHdV_BeIW0M`), já preenchido. Os outros não tiveram uma fonte
confiável o bastante para publicar sem risco de linkar a matéria errada.
`src/data/midia.yaml`

- [ ] Achar os links, se existirem (a coluna do meio político e a matéria da Folha são os mais
      prováveis de existir no site dos próprios veículos)

### 11. Seminários sem descrição, link ou vídeo — todos os 36
O site antigo publicava só *apresentador (instituição) – "título". [data]*. Dezenove também não
têm instituição. `src/data/seminarios.yaml`

- [ ] Decidir se vale enriquecer (gravações no YouTube?)

### 12. Acervo: 81 dos 95 itens sem `estado`, e nenhum com miniatura
A taxonomia `estado` do WordPress só tinha o termo "RJ". As miniaturas eram todas a mesma imagem
genérica, então não foram migradas. `src/data/acervo.yaml`

- [ ] Nada a fazer, a menos que queiram capas reais por vídeo

### 13. A imagem de compartilhamento ainda diz "IESP-UERJ · desde 1996"
`public/img/og-doxa.png` (a imagem que aparece quando alguém compartilha um link do site no WhatsApp
ou nas redes) traz o selo antigo da home, "IESP-UERJ · desde 1996". O texto da home mudou em
2026-09-14 para "Laboratório de pesquisa · desde 1996", porque o DOXA só está no IESP-UERJ desde 2010.

- [ ] Refazer a arte (1200×630) com o selo novo

### 14. Links externos que não dá para conferir daqui

Em 2026-09-13 todos os links externos do site foram testados. Estes não responderam ao teste
automático, mas provavelmente funcionam num navegador — vale abrir um a um de vez em quando:

- **Barram robôs (403):** The Economist, SciELO Books, KAS.
- **Instáveis:** Fundación Giménez Abad (PDF de atas; o servidor inteiro respondia 503) e o site da
  UFPE (`a-politizacao-da-pandemia`; certificado que o teste automático recusou).
- **TSE:** os 627 links de programas de governo em `public/dados/programas-eleitorais-rj.csv`
  (`divulgacandcontas.tse.jus.br`) só respondem a acessos do Brasil.

- [ ] Abrir cada um num navegador e anotar aqui o que estiver quebrado

---

## O que **não** está pendente

Isto já foi resolvido — não perca tempo procurando.

### O site novo dependia do site antigo — resolvido em 2026-09-13

O WordPress saiu do ar e o domínio `lab-doxa.org.br` passou a servir o site novo. Nada mais depende
do site antigo:

- os **273 mapas** estão no Google Drive do DOXA (conta do acervo, pasta *Acervo Doxa (NEW) / Site
  DOXA — Mapas de votação*, compartilhada por link). Conferido: os 273 links abrem sem login com o
  arquivo certo, e 29 arquivos baixados anonimamente têm o SHA-256 do manifesto. O registro de
  cada um está em `extracao/dados/mapas-no-drive.csv`, que o build usa para levar os endereços
  antigos dos mapas aos novos;
- os **7 links internos** que apontavam para páginas do WordPress (4 "Saiba mais" de eventos, 2
  "Página original" de bancos de dados, o anexo do seminário Marcus Figueiredo) foram retirados ou
  trocados — o PDF do cartaz foi recuperado do Wayback Machine;
- os **endereços antigos** que circulam lá fora são levados ao conteúdo novo
  (`src/lib/rotas-antigas.mjs`);
- os 6 PDFs órfãos e o original do livro ganharam cópia **privada** no mesmo Drive.

Um cuidado permanente: no Drive, mover ou renomear não quebra link; **apagar e reenviar quebra**
(o arquivo ganha outro ID).

| Coleção | Arquivos | Peso | Situação |
|---|---:|---:|---|
| Mapas de votação | 273 | 835 MB | no Google Drive do DOXA desde 2026-09-13 |
| Teses e pesquisas | 20 | 43 MB | em `public/pdfs/` desde 2026-09-03 |
| Análises de conjuntura | 33 | 30 MB | em `public/pdfs/` desde 2026-09-03 |
| Textos para discussão | 2 | 2 MB | em `public/pdfs/` desde 2026-09-03 |

*Histórico:* em 2026-09-03, os 55 PDFs de teses, análises e textos para discussão (e os 4 de
`midia-recuperada-do-archive/`) vieram para `public/pdfs/`. Em 2026-09-06 o WordPress começou a
cair, e por uma semana os 273 links de mapas, 5 de eventos e 2 de bancos de dados ficaram quebrados
no site publicado, até a migração dos mapas para o Drive. Entre as opções consideradas para os
mapas — Drive, manter o WordPress como servidor de arquivos, trazer tudo para o GitHub Pages —
ficou o Drive, que o laboratório já usa para o acervo. (Zenodo, com DOI, continua sendo uma
possibilidade futura; o registro em `extracao/dados/mapas-no-drive.csv` tem o SHA-256 de cada
arquivo para uma segunda migração.)

### Links externos mortos na origem — resolvidos em 2026-09-13

A verificação de 2026-09-13 achou 13 links externos quebrados, todos de terceiros (vieram assim do
WordPress). Um deles, do texto de Nara Salles no Horizontes ao Sul, passou a **redirecionar para um
site de spam**. Em `src/data/midia.yaml`, salvo o da EdUERJ:

- **Cópia no Wayback Machine** (captura anterior à perda do domínio, título conferido): Horizontes ao
  Sul; os 2 textos do blog antigo do Vota Aí (o domínio `votaai.com.br` foi tomado por outro site;
  a plataforma hoje vive em `votaai.cesop.unicamp.br`); os 3 do BR Político; a coluna do Valor de
  2010; e a entrevista à Folha reproduzida pelo AVOL (que também corrigiu autor e veículo do item).
- **Endereço novo do próprio veículo:** Exame, O Globo (sem `?versao=amp`) e Jornal GGN (o link
  era uma página de tag, e o veículo estava como "Central Gazeta de Notícias").
- **Livro de homenagem a Marcus Figueiredo** (`publicacoes.yaml`): a EdUERJ mudou de site; o link
  vai para o DOI do SciELO Books, em acesso aberto.
- **Sem cópia pública:** o anexo do Gmail e o clipping do WeSeek ficaram sem link (item 10).

### As teses da BDTD voltaram a abrir — resolvido em 2026-09-03

Dez teses apontam para `www.bdtd.uerj.br:8443`. Nenhuma abria em 2026-07-12, **e no site antigo
também não abriam** — o repositório da UERJ estava fora do ar. Em 2026-09-03 a UERJ restabeleceu o
serviço: as 9 URLs distintas (10 ocorrências) devolvem HTTP 200. Vale reconferir de tempos em
tempos, já que a BDTD já caiu antes. *(Três outras teses apontavam para uma página do IESP que dá
404. Esses links foram removidos: o projeto não cria botões mortos.)*

### Outros

- ✅ **Texto do acervo** (2026-09-03, revisto em 2026-09-13): dizia que a busca estava "ainda em
  construção" e prometia vídeos até 2022; hoje descreve a busca que existe e o período real
  (presidente em 1989, 1994 e 1998; governador em 1994 e 1998).
- ✅ **Publicação "no prelo"** *Vulnerabilidades sociais, modelos de provisão de saúde…*: saiu pela
  EdUERJ em 2023, em acesso livre no SciELO Books (`https://books.scielo.org/id/vpjzm`).
- ✅ **Texto para discussão sem resumo** (*"Tempo é dinheiro"*, Schaefer, 2023): o PDF não tem
  resumo — vai do título direto para a "Introdução". Preencher exigiria escrever um resumo do zero,
  o que o projeto não faz. Fica opcional, como está.
- ✅ **Seis PDFs órfãos** (na biblioteca de mídia do WordPress, sem página que os linkasse; lista em
  `extracao/dados/fontes-externas.yaml` → `pdfs_publicados_sem_pagina`): preservados em
  `arquivos-preservados/orfaos-sem-pagina/` e, desde 2026-09-13, em cópia privada no Drive do DOXA
  (*Site DOXA — Arquivos preservados (não compartilhar)*). Continuam fora do site; decidir se algum
  volta é decisão editorial do DOXA. Se voltar, o caminho é `public/pdfs/`, não compartilhar a pasta.
- ✅ **ID do vídeo da home**: `Ns3jYjf7hx4` (estava escondido num atributo `data-lazy-load`).
- ✅ **URL do Power BI**: a real foi recuperada. O site antigo tinha **um** dashboard, não dois.
- ✅ **Acervo**: os 95 itens, cada um com seu link próprio do Google Drive.
- ✅ **Catálogo mestre do acervo**: 2.034 fitas (1988–2018), em `extracao/dados/acervo-catalogo-mestre.csv`.
- ✅ **Fotos da equipe**: as 16.
- ✅ **Logos dos parceiros**: os 8 (CAPES, CNPq, FAPERJ, FINEP, IBOPE, IESP-UERJ, UERJ, VOX).

---

## Como editar

Passo a passo, sem jargão, em [`docs/GUIA_DE_MANUTENCAO.md`](docs/GUIA_DE_MANUTENCAO.md).

Regra de ouro: se você digitar algo errado, **o build falha e o site não é atualizado**. Nada
quebrado vai ao ar. Pode editar sem medo.

> Corrija sempre em `src/`: é a fonte do conteúdo. `extracao/` é registro histórico da migração e
> não precisa ser tocada (o script que convertia `extracao/` em `src/` está aposentado).
