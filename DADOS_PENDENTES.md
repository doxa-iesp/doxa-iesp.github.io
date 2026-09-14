# Dados que faltam

Tudo o que **não existe no site antigo** e precisa ser preenchido por alguém do DOXA.
O site funciona sem nada disto — os campos são opcionais e as páginas simplesmente omitem o que
falta (nenhum botão morto, nenhum "undefined" na tela).

Ordenado por impacto. Marque `[x]` conforme resolver.

---

## 🔴 Alto impacto — o visitante percebe

### 0. ✅ O site novo dependia do site antigo para servir 328 PDFs — resolvido

> ✅ **2026-09-13 — resolvido por completo.** O WordPress saiu do ar e o domínio `lab-doxa.org.br`
> passou a servir o site novo. Nada mais depende do site antigo:
>
> - os **273 mapas** estão no Google Drive do DOXA (conta do acervo, pasta *Acervo Doxa (NEW) / Site
>   DOXA — Mapas de votação*, compartilhada por link). Conferido: os 273 links abrem sem login com o
>   arquivo certo, e 29 arquivos baixados anonimamente têm o SHA-256 do manifesto. O registro de
>   cada um está em `extracao/dados/mapas-no-drive.csv`;
> - os **7 links internos** que apontavam para páginas do WordPress (4 "Saiba mais" de eventos, 2
>   "Página original" de bancos de dados, o anexo do seminário Marcus Figueiredo) foram retirados ou
>   trocados — o PDF do cartaz foi recuperado do Wayback Machine;
> - os **endereços antigos** que circulam lá fora são levados ao conteúdo novo
>   (`src/lib/rotas-antigas.mjs`);
> - os 6 PDFs órfãos e o original do livro ganharam cópia **privada** no mesmo Drive.
>
> Um cuidado permanente: no Drive, mover ou renomear não quebra link; **apagar e reenviar quebra**
> (o arquivo ganha outro ID). O histórico abaixo fica como registro.

| Coleção | Arquivos | Peso | Situação |
|---|---:|---:|---|
| Mapas de votação | 273 | 835 MB | ✅ no Google Drive do DOXA desde 2026-09-13 |
| Teses e pesquisas | 20 | 43 MB | ✅ resolvido em 2026-09-03 |
| Análises de conjuntura | 33 | 30 MB | ✅ resolvido em 2026-09-03 |
| Textos para discussão | 2 | 2 MB | ✅ resolvido em 2026-09-03 |

**✅ 2026-09-03 — Opção A parcialmente feita.** Os 55 PDFs de teses, análises e textos para
discussão (76 MB) já foram trazidos para o repositório (`public/pdfs/`) e os links em
`src/data/` já apontam para lá — deixaram de depender do WordPress. De brinde, os 4 PDFs de
`midia-recuperada-do-archive/` também migraram, consertando 4 links que davam 404 em produção em
`midia.yaml`. Ver `arquivos-preservados/LEIA-ME.md`.

> 🔴 **2026-09-06 — o WordPress antigo começou a cair.** Pela manhã ele respondia normalmente;
> à noite, timeout em todas as tentativas (`https://www.lab-doxa.org.br/` e os PDFs). Enquanto
> ele estiver assim, **os 273 links de mapas estão quebrados no site publicado**, mais 5 links de
> eventos e 2 de bancos de dados. Isso deixou de ser risco futuro e virou problema presente: a
> migração para o Drive é a tarefa mais urgente da lista. O caminho está pronto e testado
> (`arquivos-preservados/LEIA-ME.md`), e só depende de alguém rodar `rclone config` uma vez.

**Decisão sobre os 273 mapas de votação (histórico).**

- [x] **Opção A:** dar aos mapas um endereço próprio. **Escolhido o Google Drive do DOXA**, que o
      laboratório já usa para o acervo — feito em 2026-09-13. (Zenodo, com DOI, continua sendo uma
      possibilidade futura; o registro em `extracao/dados/mapas-no-drive.csv` tem o SHA-256 de cada
      arquivo para uma segunda migração.)
- [ ] ~~Opção B: manter o WordPress antigo no ar apenas como servidor de arquivos.~~ Deixou de
      existir: o WordPress saiu do ar.
- [ ] ~~Opção C: trazer tudo para o GitHub Pages.~~ Descartada.

### 0c. Links externos que morreram na origem — 13 de 455

**Verificado em 2026-09-13**, com todos os links externos do site. Não é efeito da migração: são
páginas de terceiros que saíram do ar ou mudaram de endereço, e os links vieram assim do WordPress.
Todos em `src/data/midia.yaml`, salvo o da EdUERJ (`publicacoes.yaml`).

- **404:** dois posts do blog antigo do Vota Aí (`votaai.com.br/as-propostas-para-a-saude…` e
  `…/eles-sao-todos-iguais/` — a plataforma hoje vive em `votaai.cesop.unicamp.br`); uma tag do
  Jornal GGN; uma notícia em `antonioviana.com.br`; a versão AMP de uma matéria d'O Globo
  (`…roteiro-de-viagens-de-bolsonaro…?versao=amp`); a página do ebook de homenagem a Marcus
  Figueiredo na EdUERJ.
- **Sem resposta:** Exame (`filiacoes-partidarias-no-brasil-mais-do-mesmo`), UFPE
  (`a-politizacao-da-pandemia`), Fundación Giménez Abad (PDF de atas) e WeSeek.
- **403 — funcionam num navegador**, só barram robôs: The Economist, SciELO Books, KAS.

- [ ] Para cada 404, procurar a matéria no endereço novo do veículo ou uma captura no Wayback
      Machine e trocar o `url` (nos dois lugares: `src/data/` e `extracao/dados/`). Na dúvida entre
      duas matérias parecidas, deixar sem link — a regra é não inventar.

### 0b. As teses da BDTD não abrem (e não é culpa da migração)

Dez teses apontam para `www.bdtd.uerj.br:8443`. Nenhuma abria, **e no site antigo também não
abriam**: são exatamente as mesmas URLs. O problema era do repositório da UERJ, que estava fora do
ar. Verificado em 2026-07-12: a porta 443 respondia e redirecionava para a porta 8080, que não
respondia; a porta 8443, onde estão os PDFs, estava fechada.

- [x] **Resolvido sozinho em 2026-09-03 — a UERJ restabeleceu o serviço.** As 9 URLs distintas
      (10 ocorrências) foram testadas uma a uma: todas devolvem HTTP 200 hoje. Nenhuma mudança de
      código foi necessária — os links em `src/data/pesquisas.yaml` já estavam certos, só estavam
      apontando para um serviço fora do ar. Vale reconferir de tempos em tempos, já que o histórico
      mostra que a BDTD já caiu antes.

*(Três outras teses apontavam para uma página do IESP que dá 404. Esses links foram removidos: o
projeto não cria botões mortos.)*


### 1. Lattes de 9 dos 16 membros da equipe
**Onde:** a lista `lattes:` no topo de `extracao/dados/publicacoes-academicas.yaml` (⚠️ não é o
campo `lattes:` de cada `src/content/equipe/<nome>.yaml` — `scripts/converter-conteudo.py` ignora
esse campo e casa o Lattes de cada pessoa por **sobrenome**, usando só essa lista; editar o YAML da
pessoa diretamente não tem efeito depois da próxima regeneração).
**Por que falta:** a página `/institucional/` do site antigo não publicava Lattes. Os 4 que temos
(Argelina Cheibub Figueiredo, Fernando Meireles, Fernando Guarnieri, Bruno Schaefer) vieram da
página de publicações acadêmicas.

- [x] **Flávia Bozza Martins** — resolvido em 2026-09-03, via `iesp.uerj.br/pesquisador/`
      (confiança alta): `http://lattes.cnpq.br/1494895098804362`
- [x] **Thiago Moreira** — resolvido em 2026-09-03, via `iesp.uerj.br/pesquisador/`
      (confiança alta): `http://lattes.cnpq.br/2163358625457191`
- [ ] Carolina Botelho — buscado, não achado com confiança suficiente
- [ ] Carolini Silva — buscado, não achado com confiança suficiente
- [x] **Felipe Lamarca** — resolvido em 2026-09-06: `http://lattes.cnpq.br/2606938112682925`
      (informado por ele; também consta em felipelamarca.com, agora no card como "Site")
- [ ] Hellen Guicheney — buscado, não achado com confiança suficiente
- [ ] Karime Lima — buscado, não achado com confiança suficiente
- [ ] Larissa Mendes — não buscado
- [ ] Maria Dominguez — buscado, não achado (nome comum, resultados ambíguos)
- [ ] Matteo Manes — buscado, não achado
- [ ] Nara Salles — buscado, não achado com confiança suficiente
- [ ] Natalia Maciel — buscado, não achado com confiança suficiente

Para os 9 restantes, a pessoa provavelmente tem Lattes (a maioria aparece em plataformas
acadêmicas como Escavador/ResearchGate/Google Acadêmico), mas essas páginas bloqueiam acesso
automatizado e a busca geral não trouxe o número do Lattes com confiança suficiente para publicar
sem risco de atribuir o currículo errado a alguém. Mais rápido: cada pessoa cola o próprio link.

Para adicionar, entre em `extracao/dados/publicacoes-academicas.yaml` e acrescente à lista
`lattes:` do topo (o nome só precisa bater o **sobrenome** com o `nome:` da pessoa em
`extracao/dados/equipe.yaml`):

```yaml
lattes:
  - name: "Sobrenome, X."
    url: "http://lattes.cnpq.br/0000000000000000"
```

Depois rode `python3 scripts/converter-conteudo.py` para propagar para `src/`.

### 2. E-mail dos membros (nenhum publicado)
**Onde:** mesmo arquivo, campo `email`
**Por que falta:** o site antigo não publicava nenhum e-mail individual, só o do acervo.
Decidam se querem publicar — expor e-mail atrai spam. Se não quiserem, deixem como está.

- [ ] Decidir se publica e-mail individual
- [ ] Se sim, preencher os 16

*(Desde 2026-09-06 existe também o campo `site`, para página pessoal — o card mostra "Site" ao
lado do "Lattes". Preencher é opcional, como todo o resto.)*

### 3. Texto do acervo está desatualizado
**Onde:** `src/content/paginas/acervo.md`
O texto veio palavra por palavra do site antigo e diz que a busca está *"ainda em construção"*.
**Ela agora existe e funciona** (filtros por ano, cargo, região, partido e candidato).

- [x] **Resolvido em 2026-09-03.** Parágrafo reescrito em `src/content/paginas/acervo.md`, via
      `OVERRIDES` em `scripts/converter-conteudo.py` (o texto fiel ao site antigo continua intacto
      em `extracao/dados/paginas/acervo.md`, que é registro histórico).

### 4. Redes sociais
**Onde:** `src/data/site.yaml`, campos `instagram` e `twitter`
O site antigo só tinha YouTube. Se o DOXA tiver perfis, o rodapé já está pronto para mostrá-los.

- [x] **Pesquisado em 2026-09-03: nenhum Instagram ou Twitter/X próprio do DOXA foi encontrado.**
      (O `@iesp.uerj` no Instagram é do instituto todo, não do laboratório — não é o mesmo perfil.)
      Campos deixados vazios, como estavam.
- [ ] **Achado não previsto: existe uma página do DOXA no Facebook**,
      `facebook.com/doxa.iesp.uerj/`. O schema de `site.yaml` não tem campo para Facebook hoje —
      decidam se vale adicionar (mudança de schema, não incluída neste ciclo) ou se o Facebook não
      é prioridade para o site novo.

---

## 🟠 Médio impacto — dado incompleto, mas honesto

### 5. Coluna `municipio` da base das Capitais está errada **na origem**
**Onde:** `public/dados/programas-eleitorais-capitais.csv` e `extracao/dados/`
Os municípios estão rotacionados em relação aos candidatos. Verificado: Eduardo Paes (Rio) aparece
como Florianópolis; Rafael Greca (Curitiba) como Vitória; Elson Pereira (Florianópolis) como
Aracaju. Os outros campos (candidato, partido, propostas) estão corretos.

A página `/bancos-de-dados/` já mostra um aviso visível. **Não corrigimos por adivinhação:** o
deslocamento parece ser de 7 blocos, mas os blocos têm tamanhos diferentes.

- [ ] Recuperar o município correto de cada candidato (fonte: TSE) e regravar o CSV — deixado de
      fora do ciclo de 2026-09-03 a pedido explícito (fora de escopo por ora)
- [ ] Depois, apagar o campo `aviso` em `extracao/dados/bancos-de-dados.yaml`

### 6. Pesquisas sem link para o texto completo — 30 de 61
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

- [x] **Resolvido em 2026-09-03.** O livro (*COVID-19 e agendas de pesquisa nas ciências sociais*,
      org. Fontainha e Milani) saiu pela EdUERJ em 2023 e está de acesso livre no SciELO Books.
      `ano: 2023` preenchido, e `url` acrescentada apontando para o livro
      (`https://books.scielo.org/id/vpjzm` — o link direto do capítulo ficou atrás de proteção
      anti-bot do SciELO, então foi usado o link da coletânea, de onde o capítulo é acessível).

### 10. Oito itens de "Na Mídia" sem link
Duas matérias impressas nunca tiveram URL na fonte (*"A polarização do vírus"*, Valor;
*"Desconstruindo Mitos"*, Pesquisa Fapesp) e os seis itens audiovisuais são vídeos/documentários
sem link publicado.

**Pesquisado em 2026-09-03:** achado 1 de 8 com confiança alta — o documentário *"Arquitetos do
Poder"* está no YouTube com um upload cujo título bate exatamente com a autoria da ficha
(`youtube.com/watch?v=hHdV_BeIW0M`), já preenchido. Os outros 7 não tiveram uma fonte confiável o
bastante para publicar sem risco de linkar a matéria errada (nomes/temas comuns, várias
reportagens parecidas na web) — ficam como estavam.
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

- [x] **Verificado em 2026-09-03, não dá para resolver como previsto.** O PDF (agora local em
      `public/pdfs/textos-discussao/`) foi lido de ponta a ponta: não tem seção de resumo/abstract,
      o texto vai direto do título para a "Introdução". Não é um dado perdido na extração — o
      documento-fonte simplesmente não tem resumo. Preencher esse campo exigiria escrever um resumo
      do zero, o que o projeto não faz (regra "não invente"). Fica opcional, como está.

### 14. Seis PDFs publicados que nenhuma página linka
Estão na biblioteca de mídia do WordPress mas perderam a página que os referenciava. A lista está
em `extracao/dados/fontes-externas.yaml` → `pdfs_publicados_sem_pagina`.

- [x] **Preservados em 2026-09-03**, em `arquivos-preservados/orfaos-sem-pagina/` (verificados,
      todos abrem). Continuam **fora do site** — decidir se algum volta é call editorial do DOXA.
- [x] **Cópia privada no Google Drive do DOXA desde 2026-09-13**, na pasta *Acervo Doxa (NEW) / Site
      DOXA — Arquivos preservados (não compartilhar)* — conferido que não abrem sem login. Se algum
      voltar ao site, o caminho é `public/pdfs/`, não compartilhar essa pasta.

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
