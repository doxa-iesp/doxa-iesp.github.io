# Resumo executivo — Reconstrução do site do DOXA

**Data:** 2026-07-10

O site do DOXA foi reconstruído do zero, saindo do WordPress/Elementor para um site **estático em
Astro 7**, versionado no GitHub e publicado automaticamente pelo GitHub Actions. Nenhuma linha de
PHP, nenhum banco de dados, nenhum plugin.

---

## O que foi construído

**14 páginas**, cobrindo todas as seções do site antigo:

`/` · `/institucional/` · `/pesquisas/` · `/pesquisa-covid/` · `/acervo/` · `/mapas-de-votacao/` ·
`/bancos-de-dados/` · `/publicacoes/` (+ acadêmicas, análises de conjuntura, textos para discussão) ·
`/eventos/` · `/seminarios/` · `/na-midia/`

**Todo o conteúdo migrado**, conferido item a item no HTML gerado:

| | |
|---|---|
| Membros da equipe | 16 (com foto) |
| Itens do acervo audiovisual | 95 (cada um com link próprio no Google Drive) |
| Pesquisas (teses, em andamento, concluídas) | 61 |
| Aparições na mídia | 70 |
| Publicações acadêmicas | 34 |
| Análises de conjuntura | 28 |
| Seminários | 36 |
| Mapas de votação | 273 |
| Eventos | 5 |
| Textos para discussão | 2 |
| Bancos de dados | 3 |

Além disso: o **catálogo mestre do acervo** (2.034 fitas, 1988–2018), a base de **programas
eleitorais** (821 registros) e os **microdados** dos surveys ficaram arquivados em `extracao/`.

**Estado técnico:** `npm run build` verde em build frio · `npx astro check` com 0 erros e 0 avisos ·
0 links internos quebrados · 0 erros de JavaScript · 0 rolagem horizontal no celular · toda imagem
com `alt`.

---

## Principais decisões

**1. Astro, e não Hugo (que já estava no repositório).**
O critério não foi gosto, foi o que acontece quando um estagiário digita errado. No Hugo, escrever
`categoria: pesquisadorS` faz o membro **sumir da página em silêncio** — o build passa. No Astro
com schemas Zod, o build falha dizendo qual entrada, qual campo e quais valores são aceitos.
Isso foi testado antes de decidir, não presumido. O custo aceito é a árvore de dependências do npm;
mitigado com lockfile, Node fixo e nenhum framework de UI.

**2. A home virou a apresentação institucional do grupo.**
Conforme decidido com a Argelina. Deixou de ser um feed de destaques; os projetos aparecem numa
seção secundária. `/institucional/` ficou focada na equipe, sem duplicar o texto.

**3. Um arquivo por pessoa, uma lista por bibliografia.**
Adicionar um membro é criar um arquivo — não há indentação de lista para errar, nem conflito de
merge entre dois estagiários. Publicações, mídia e afins ficam num YAML por coleção, porque criar
200 arquivos não traria ganho.

**4. Fidelidade ao original, com desvios justificados.**
Todos os 11 desvios estão em [MUDANCAS_DE_LAYOUT.md](MUDANCAS_DE_LAYOUT.md), cada um com o problema
concreto que o motivou (embed que rastreia, menu inacessível por teclado, link errado na fonte).

---

## O problema mais sério que encontramos — e consertamos

A validação do Astro tinha um **furo justamente no formato que mais gente vai editar**.

O loader `file()`, usado nas listas (`publicacoes.yaml`, `midia.yaml`…), **engole erros de YAML**.
Com a indentação quebrada, o Astro imprimia um erro, **saía com código 0** e publicava a página
**vazia** — as 70 matérias de "Na Mídia" sumiriam do ar, e o PR ficaria verde. Localmente o bug se
escondia atrás de um cache; num build limpo, que é o do CI, o site iria mutilado.

Ou seja: a própria razão de trocar o Hugo pelo Astro não se sustentava sem conserto.

Foram acrescentadas duas travas, ambas verificadas:
- `scripts/validar-dados.mjs`, executado antes do build, que falha com código 1 e aponta arquivo,
  linha e coluna, em português;
- uma trava no `deploy.yml` que reprova o deploy se um erro de leitura de dados aparecer no log
  (com `set -o pipefail`, sem o qual ela seria decorativa).

Hoje, **nenhum erro de conteúdo passa despercebido**: o PR fica vermelho e o site continua no ar
com a versão anterior.

---

## Defeitos herdados do site antigo (não corrigidos por adivinhação)

1. **`programas-eleitorais-capitais.csv`** — a coluna `municipio` está **rotacionada** em relação
   aos candidatos. Verificado: Eduardo Paes (Rio) aparece como Florianópolis; Rafael Greca
   (Curitiba) como Vitória. A página `/bancos-de-dados/` exibe um aviso visível. **Não use essa
   coluna sem revisão manual.**
2. **Dois cards da home apontavam para a mesma URL do Power BI** ("Eleições Rio e São Paulo 2024" e
   "Textos de discussão do Doxa"). O segundo é um link errado; foi removido da home.
3. **`/teses-e-dissertacoes/` e `/pesquisas-realizadas/`** eram páginas mortas (vazias mesmo com
   JavaScript). Não migradas.
4. **Três teses** apontam para uma página do IESP que hoje dá 404. Os links foram preservados como
   estão na fonte.
5. **Seis PDFs publicados** não são linkados por nenhuma página viva. Listados em
   `extracao/dados/fontes-externas.yaml`.

---

## ✅ Checklist do time do DOXA (o que só vocês podem fazer)

**Antes do primeiro deploy — obrigatório**

- [ ] `git add -A && git commit` e push. **Atenção:** `public/` precisa entrar no commit, senão o
      site vai ao ar sem imagens, fontes e PDFs. (Nada foi commitado por mim.)
- [ ] Ativar o Pages: **Settings → Pages → Source: GitHub Actions**.
- [ ] Conferir o site publicado em `https://felipelamarca.com/DOXA/`.

**Revisão de conteúdo**

- [ ] **Ler os textos das páginas.** Eles vieram do site antigo palavra por palavra. Um exemplo que
      já ficou desatualizado: a página do acervo diz que a busca está *"ainda em construção"* — ela
      agora existe e funciona. O texto está em `src/content/paginas/acervo.md`.
- [ ] **Aprovar as fotos da equipe** (`public/img/equipe/`) e o texto de apresentação da home
      (`src/content/paginas/home.md`).
- [ ] **Coletar Lattes e e-mail** de 12 dos 16 membros. Não existem no site antigo; só 4 pesquisadores
      (Argelina, Meireles, Guarnieri, Schaefer) tinham Lattes publicado. Ver
      `docs/GUIA_DE_MANUTENCAO.md`, receita "adicionar/editar um membro".
- [ ] **Revisar a coluna `municipio`** da base das capitais antes de publicá-la (defeito nº 1 acima).
- [ ] Decidir se o **catálogo mestre de 2.034 fitas** vira uma página navegável (hoje só existe como
      CSV em `extracao/dados/`).

**Domínio próprio (quando quiserem sair de `felipelamarca.com/DOXA/`)**

- [ ] Confirmar quem controla o registro de `lab-doxa.org.br`.
- [ ] Em `astro.config.mjs`: trocar `site` e **remover** a linha `base`.
- [ ] Criar `public/CNAME` com `www.lab-doxa.org.br`. *(O `CNAME` na raiz do repositório não é
      publicado — só o que está em `public/` entra no build. Esse era um bug silencioso do site Hugo.)*
- [ ] Apontar o DNS e habilitar HTTPS no GitHub Pages.

**Limpeza (quando aprovarem o site novo)**

- [x] O site antigo em Hugo já foi removido. Continua recuperável pelo histórico do git
      (`git checkout 073679b -- layouts/ data/ content/ static/`).
- [ ] Considerar tirar o repositório de `~/Desktop` se ele estiver sincronizado com o iCloud — a
      sincronização cria arquivos-cópia (`arquivo 2.yaml`) que o build duplicaria sem avisar.

---

## Onde está cada coisa

| | |
|---|---|
| **Guia do estagiário** | [docs/GUIA_DE_MANUTENCAO.md](GUIA_DE_MANUTENCAO.md) |
| Por que Astro e não Hugo | [docs/DECISAO_ARQUITETURA.md](DECISAO_ARQUITETURA.md) |
| Desvios de layout, com motivo | [docs/MUDANCAS_DE_LAYOUT.md](MUDANCAS_DE_LAYOUT.md) |
| Histórico de decisões por etapa | [checkpoints/](../checkpoints/) |
| Extração completa do WordPress | [extracao/README.md](../extracao/README.md) |
| Notas para quem for programar | [CLAUDE.md](../CLAUDE.md) |

## Pendências assumidas

Nada está bloqueado. As três pendências reais são de **dados**, não de código: Lattes/e-mail da
equipe, a coluna de município da base das capitais, e a revisão dos textos herdados. Todas estão no
checklist acima e registradas nos checkpoints.
