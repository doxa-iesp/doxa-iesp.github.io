# Dados que faltam

Tudo o que **não existe no site antigo** e precisa ser preenchido por alguém do DOXA.
O site funciona sem nada disto — os campos são opcionais e as páginas simplesmente omitem o que
falta (nenhum botão morto, nenhum "undefined" na tela).

Ordenado por impacto. Marque `[x]` conforme resolver.

---

## 🔴 Alto impacto — o visitante percebe

### 1. Lattes de 12 dos 16 membros da equipe
**Onde:** `src/content/equipe/<nome>.yaml`, campo `lattes`
**Por que falta:** a página `/institucional/` do site antigo não publicava Lattes. Os 4 que temos
(Argelina Cheibub Figueiredo, Fernando Meireles, Fernando Guarnieri, Bruno Schaefer) vieram da
página de publicações acadêmicas.

- [ ] Carolina Botelho
- [ ] Carolini Silva
- [ ] Felipe Lamarca
- [ ] Flávia Bozza Martins
- [ ] Hellen Guicheney
- [ ] Karime Lima
- [ ] Larissa Mendes
- [ ] Maria Dominguez
- [ ] Matteo Manes
- [ ] Nara Salles
- [ ] Natalia Maciel
- [ ] Thiago Moreira

```yaml
lattes: "http://lattes.cnpq.br/0000000000000000"
```

### 2. E-mail dos 16 membros
**Onde:** mesmo arquivo, campo `email`
**Por que falta:** o site antigo não publicava nenhum e-mail individual, só o do acervo.
Decidam se querem publicar — expor e-mail atrai spam. Se não quiserem, deixem como está.

- [ ] Decidir se publica e-mail individual
- [ ] Se sim, preencher os 16

### 3. Texto do acervo está desatualizado
**Onde:** `src/content/paginas/acervo.md`
O texto veio palavra por palavra do site antigo e diz que a busca está *"ainda em construção"*.
**Ela agora existe e funciona** (filtros por ano, cargo, região, partido e candidato).

- [ ] Reescrever esse parágrafo

### 4. Redes sociais
**Onde:** `src/data/site.yaml`, campos `instagram` e `twitter`
O site antigo só tinha YouTube. Se o DOXA tiver perfis, o rodapé já está pronto para mostrá-los.

- [ ] Instagram (ou confirmar que não existe)
- [ ] Twitter/X (ou confirmar que não existe)

---

## 🟠 Médio impacto — dado incompleto, mas honesto

### 5. Coluna `municipio` da base das Capitais está errada **na origem**
**Onde:** `public/dados/programas-eleitorais-capitais.csv` e `extracao/dados/`
Os municípios estão rotacionados em relação aos candidatos. Verificado: Eduardo Paes (Rio) aparece
como Florianópolis; Rafael Greca (Curitiba) como Vitória; Elson Pereira (Florianópolis) como
Aracaju. Os outros campos (candidato, partido, propostas) estão corretos.

A página `/bancos-de-dados/` já mostra um aviso visível. **Não corrigimos por adivinhação:** o
deslocamento parece ser de 7 blocos, mas os blocos têm tamanhos diferentes.

- [ ] Recuperar o município correto de cada candidato (fonte: TSE) e regravar o CSV
- [ ] Depois, apagar o campo `aviso` em `extracao/dados/bancos-de-dados.yaml`

### 6. Pesquisas sem link para o texto completo — 27 de 61
**Onde:** `src/data/pesquisas.yaml`, campo `url`
Teses e dissertações costumam estar na BDTD da UERJ. Projetos em andamento não têm texto público.

- [ ] Conferir quais das 27 já têm PDF publicado e acrescentar o link

### 7. Pesquisas sem ano — 24 de 61
São as **pesquisas de projeto** (em andamento e concluídas), que no site antigo nunca tiveram data.
As 38 teses/dissertações têm ano. Se quiserem ordenar por data, precisam do ano.

- [ ] Decidir se vale preencher

### 8. Quatro pesquisas concluídas sem autor
A fonte não nomeia um responsável, só lista `Equipe:`. São:
*Eleições Gerais 2002*, *Eleições Municipais 2000*, *Ideologia Política, Persuasão…*, *Eleições 1996*.

- [ ] Definir quem assina cada uma (ou manter sem autor)

---

## 🟡 Baixo impacto — cosmético ou de arquivo

### 9. Uma publicação sem ano
*"Vulnerabilidades sociais, modelos de provisão de saúde e suas relações"* — a fonte diz
**"no prelo"**. Atualizar quando sair.
`src/data/publicacoes.yaml`

- [ ] Preencher o ano quando publicar

### 10. Oito itens de "Na Mídia" sem link
Duas matérias impressas nunca tiveram URL na fonte (*"A polarização do vírus"*, Valor;
*"Desconstruindo Mitos"*, Pesquisa Fapesp) e os seis itens audiovisuais são vídeos/documentários
sem link publicado.
`src/data/midia.yaml`

- [ ] Achar os links, se existirem

### 11. Seminários sem descrição, link ou vídeo — todos os 36
O site antigo publicava só *apresentador (instituição) – "título". [data]*. Dezenove também não
têm instituição. `src/data/seminarios.yaml`

- [ ] Decidir se vale enriquecer (gravações no YouTube?)

### 12. Acervo: 81 dos 95 itens sem `estado`, e nenhum com miniatura
A taxonomia `estado` do WordPress só tinha o termo "RJ". As miniaturas eram todas a mesma imagem
genérica, então não foram migradas. `src/data/acervo.yaml`

- [ ] Nada a fazer, a menos que queiram capas reais por vídeo

### 13. Um texto para discussão sem resumo
*"Tempo é dinheiro"* (Schaefer, 2023). `src/data/textos-discussao.yaml`

- [ ] Copiar o resumo do PDF

### 14. Seis PDFs publicados que nenhuma página linka
Estão na biblioteca de mídia do WordPress mas perderam a página que os referenciava. A lista está
em `extracao/dados/fontes-externas.yaml` → `pdfs_publicados_sem_pagina`.

- [ ] Decidir se algum deles deve voltar ao site

---

## O que **não** está pendente

Isto já foi resolvido — não perca tempo procurando:

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

> ⚠️ Se você corrigir um dado à mão em `src/`, corrija **também** em `extracao/dados/`.
> O script `scripts/converter-conteudo.py` regenera `src/` a partir de `extracao/` e sobrescreve
> edições manuais. (Ou simplesmente não rode o script.)
