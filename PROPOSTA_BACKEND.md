# PROPOSTA DE BACKEND — Site DOXA
**Auditoria técnica e recomendações de arquitetura**
*Gerado em: 2026-06-01*

---

## 1. Resumo executivo

O site foi migrado do WordPress para Hugo estático de forma estruturalmente competente: separação conteúdo/template está implementada, os dados estão em YAML com comentários de schema, e o pipeline CI/CD funciona. Os problemas críticos são: (1) `hugo-version: "latest"` no workflow expõe o site a breaking changes silenciosos; (2) todos os arquivos de dados contêm apenas dados de exemplo — nenhum dado real foi preenchido; (3) o README é composto de duas linhas, sem qualquer instrução de uso; (4) existe lógica de filtro duplicada entre templates (inline `<script>`) e arquivo JS externo, tornando o código difícil de manter; (5) a dependência da fonte Montserrat via Google Fonts introduz uma requisição externa que pode falhar em redes restritas. A recomendação é **manter Hugo** com um conjunto de refatorações prioritárias listadas na seção 2. Nenhuma migração de framework está justificada neste momento.

---

## 2. Diagnóstico do framework atual

### Recomendação: MANTER Hugo

| Critério | Avaliação |
|---|---|
| Geração estática | Sim — build local e CI/CD geram HTML puro, sem servidor |
| Compatibilidade com GitHub Pages | Sim — `actions/deploy-pages` funciona corretamente |
| Curva de aprendizado para pesquisadores | Parcial — YAML/Markdown são editáveis sem código; o risco é nos templates Golang |
| Ecossistema de longo prazo | Sim — Hugo está maduro, tem releases frequentes e suporte ativo |

**Justificativa para manter:** Todo o conteúdo dinâmico do site (equipe, publicações, eventos, mídia, acervo) já está em arquivos YAML independentes dos templates. Um pesquisador sem perfil de desenvolvedor consegue realizar todas as operações de manutenção editando apenas esses arquivos. O custo de migração para qualquer outra stack (Astro, Jekyll, Eleventy, Next.js estático) não se justifica — os problemas encontrados são de configuração e documentação, não de limitação de framework.

### Refatorações prioritárias

#### P1 — Crítico: fixar versão do Hugo no workflow

**Problema:** `hugo-version: "latest"` no CI/CD fará o build quebrar silenciosamente em qualquer release do Hugo que introduza breaking changes na sintaxe de templates ou na API de dados (`hugo.Data` foi introduzido no Hugo 0.115; releases futuros podem deprecar ou alterar comportamento).

**Solução:** Substituir `"latest"` pela versão atual usada em desenvolvimento. Verificar com `hugo version` e fixar explicitamente, por exemplo `"0.147.0"`. Atualizar intencionalmente quando necessário.

**Arquivo:** `.github/workflows/deploy.yml`, linha 26.

---

#### P2 — Crítico: preencher dados reais em todos os arquivos YAML

**Problema:** Todos os arquivos em `data/` contêm exclusivamente dados de exemplo ("Título do Livro 1", "Candidato Exemplo 1", "Nome do Pesquisador"). O site publicado em produção não exibe nenhuma informação real sobre o laboratório.

**Solução:** Preencher cada arquivo com os dados reais conforme os schemas documentados na seção 3. O arquivo `data/homepage.yaml` também contém `"SUBSTITUA_PELO_ID_DO_VIDEO"` no campo `youtube_id`, que gerará um iframe inválido em produção.

---

#### P3 — Alta: criar documentação mínima no README

**Problema:** O `README.md` tem duas linhas ("# DOXA" e "Proposta de site do DOXA"). Não há nenhuma instrução sobre como adicionar dados, como fazer build local, ou como o deploy funciona.

**Solução:** Expandir o README com pelo menos: pré-requisitos (Hugo instalado), comando de build local (`hugo server`), onde ficam os dados e como editá-los, e uma seção de operações comuns (ver seção 4 deste documento como referência).

---

#### P4 — Alta: remover lógica de filtro inline dos templates

**Problema:** Dois templates contêm blocos `<script>` inline com lógica de filtro por abas: `layouts/pesquisas/list.html` (linhas 45–61) e `layouts/analises-de-conjuntura/list.html` (linhas 41–57). Essa lógica é idêntica entre os dois templates. Existe também `static/js/acervo.js` com lógica mais complexa, corretamente externalizada. O padrão é inconsistente.

**Solução:** Extrair o padrão de filtro por abas para `static/js/filter-tabs.js` e referenciá-lo nos dois templates. Isso reduz o código total e centraliza manutenção.

---

#### P5 — Média: campo `year` redundante em `data/seminars.yaml`

**Problema:** Cada seminário tem os campos `date` (YYYY-MM-DD) e `year` (inteiro). O `year` é derivável da `date`, mas precisa ser informado manualmente duas vezes — criando risco de inconsistência (ex.: `date: "2023-09-15"` com `year: 2022`).

**Solução:** No template `layouts/seminarios/list.html`, substituir a leitura de `.year` por `dateFormat "2006" (time .date)` para extrair o ano da data. Remover o campo `year` do schema do arquivo YAML. Isso simplifica o arquivo de dados e elimina o risco de inconsistência.

---

#### P6 — Média: texto hardcoded sobre Acervo Audiovisual na homepage

**Problema:** O template `layouts/index.html` (linhas 72–77) contém texto descritivo fixo sobre o acervo audiovisual ("O DOXA mantém o maior arquivo audiovisual...") que não passa por nenhum arquivo de dados ou Markdown. Se o texto precisar ser alterado, é necessário editar HTML.

**Solução:** Mover esse texto para `data/homepage.yaml` como campo `acervo.description` e `acervo.url`, e referenciar no template. Alternativamente, mover para `content/_index.md` como conteúdo editável via Markdown, o que é ainda mais simples para pesquisadores.

---

#### P7 — Média: campo `photo` em `data/team.yaml` usa path relativo sem convenção documentada

**Problema:** O campo `photo` nos membros da equipe está vazio em todos os registros. O template `layouts/partials/team-card.html` referencia `.photo` diretamente como URL, mas não está documentado onde as fotos devem ser colocadas (em `static/img/team/`, que já existe, ou em outro local), nem qual convenção de nomenclatura usar.

**Solução:** Documentar a convenção no próprio `data/team.yaml` (no cabeçalho de comentários): fotos devem ser salvas em `static/img/team/nome-sobrenome.jpg` e o campo `photo` deve conter o path relativo `/img/team/nome-sobrenome.jpg`.

---

#### P8 — Baixa: dependência de fonte externa (Google Fonts)

**Problema:** `layouts/_default/baseof.html` carrega Montserrat via `fonts.googleapis.com`. Em redes corporativas ou institucionais com restrições de acesso a domínios externos, a fonte pode não carregar, degradando a apresentação do site.

**Solução:** Baixar os arquivos da fonte e servi-los de `static/fonts/`, atualizando o `@font-face` no CSS. Isso elimina a dependência externa e melhora o tempo de carregamento em conexões lentas.

---

#### P9 — Baixa: campo `type: "outros"` em `data/discussions.yaml` é inconsistente

**Problema:** O arquivo `data/discussions.yaml` (Textos para Discussão / Working Papers) inclui `type: "outros"` em cada entrada, mas esse campo não é usado pelo template `layouts/textos-para-discussao/list.html`, que simplesmente itera sobre `hugo.Data.discussions` sem filtrar por tipo. O campo é ruído no schema.

**Solução:** Remover o campo `type` do schema de `discussions.yaml`, já que o tipo é implícito pelo próprio arquivo. Atualizar o comentário de cabeçalho do arquivo.

---

#### P10 — Baixa: `CNAME` na raiz do repositório está deletado

**Problema:** O git status mostra `D static/CNAME` — o arquivo foi removido do diretório `static/` mas ainda existe na raiz como `CNAME`. O Hugo copia arquivos de `static/` para `public/` durante o build; um `CNAME` na raiz não é incluído automaticamente.

**Observação:** O domínio atual é `felipelamarca.com/DOXA/` (subdiretório), não um domínio customizado, então o `CNAME` pode ser desnecessário. Se o laboratório vier a usar um domínio próprio (ex.: `lab-doxa.org.br`), o arquivo `static/CNAME` deve ser criado com o domínio correto.

---

## 3. Schema recomendado para arquivos de dados

Os schemas abaixo consolidam o que já existe, corrigem inconsistências identificadas e adicionam campos opcionais úteis não presentes na versão atual.

### 3.1 `data/team.yaml` — Equipe

```yaml
# Equipe do DOXA
# -----------------------------------------------
# Campos obrigatórios: name, role, category
# Campos opcionais:    bio, photo, lattes, email, orcid
#
# Categorias válidas:
#   coordenacao | pesquisadores | pos-doutorando | aluno | assistente | associado
#
# Fotos:
#   Salvar o arquivo em static/img/team/
#   Nomear como: nome-sobrenome.jpg  (minúsculas, sem acentos, hifenizado)
#   Referenciar como: /img/team/nome-sobrenome.jpg
# -----------------------------------------------

- name: "Argelina Cheibub Figueiredo"       # obrigatório
  role: "Coordenadora"                        # obrigatório — cargo ou posição
  category: "coordenacao"                     # obrigatório — ver categorias acima
  bio: ""                                     # opcional — texto curto de apresentação
  photo: "/img/team/argelina-figueiredo.jpg"  # opcional — path relativo
  lattes: "https://lattes.cnpq.br/xxxxxxxx"  # opcional — URL completa do Lattes
  email: "nome@iesp.uerj.br"                  # opcional — endereço de email
  orcid: "https://orcid.org/0000-0000-0000-0000"  # opcional — URL do ORCID
```

### 3.2 `data/publications.yaml` — Publicações Acadêmicas

```yaml
# Publicações Acadêmicas do DOXA
# -----------------------------------------------
# Campos obrigatórios: title, authors, year, type
# Campos condicionais:
#   - publisher: obrigatório para type "livro" e "capitulo"
#   - journal:   obrigatório para type "artigo"
# Campos opcionais: pages, doi, url
#
# Tipos válidos: livro | capitulo | artigo | outros
#
# Autores: separar por ponto-e-vírgula quando houver mais de um
#   Exemplo: "Silva, João; Souza, Maria"
# -----------------------------------------------

# --- Livros ---
- title: "Propaganda Eleitoral no Brasil"   # obrigatório
  authors: "Figueiredo, Argelina C."        # obrigatório
  year: 2020                                 # obrigatório — número inteiro
  type: "livro"                              # obrigatório
  publisher: "Editora FGV"                  # obrigatório para livros
  pages: "320 p."                            # opcional
  doi: ""                                    # opcional — DOI sem prefixo "https://doi.org/"
  url: "https://editora.fgv.br/..."         # opcional — link de acesso/compra

# --- Capítulos em livro ---
- title: "Comportamento eleitoral nas eleições de 2018"
  authors: "Meireles, Fernando"
  year: 2021
  type: "capitulo"
  publisher: "In: Silva, J. (org.). Eleições no Brasil. Editora UERJ"  # inclui referência ao livro
  pages: "pp. 45–70"                         # opcional
  url: ""

# --- Artigos em revista ---
- title: "Cobertura jornalística e escolha eleitoral"
  authors: "Guarnieri, Fernando; Schaefer, Bruno"
  year: 2022
  type: "artigo"
  journal: "Dados — Revista de Ciências Sociais"  # obrigatório para artigos
  pages: "v. 65, n. 3"                        # opcional — volume e número
  doi: "10.1590/dados.2022.65.3.xxx"          # opcional
  url: ""

# --- Outras produções ---
- title: "Prefácio: Comunicação política no século XXI"
  authors: "Figueiredo, Argelina C."
  year: 2019
  type: "outros"
  publisher: "In: Autor, X. Título do Livro. Editora"
  url: ""
```

### 3.3 `data/events.yaml` — Eventos

```yaml
# Eventos do DOXA
# -----------------------------------------------
# Campos obrigatórios: title, date
# Campos opcionais:    description, location, image, url, type
#
# Tipos válidos (opcional, para filtros futuros):
#   lancamento | seminario | workshop | coloquio | outro
#
# Ordenação: os eventos são exibidos na ordem do arquivo.
#   Coloque os mais recentes no topo.
# -----------------------------------------------

- title: "Lançamento — Propaganda Eleitoral no Brasil"  # obrigatório
  date: "2024-08-15"                                    # obrigatório — formato YYYY-MM-DD
  description: "Lançamento do livro com debate entre pesquisadores."  # opcional
  location: "IESP-UERJ, Rio de Janeiro"                 # opcional — novo campo
  image: ""                                              # opcional — path em static/img/eventos/
  url: ""                                               # opcional — link externo
  type: "lancamento"                                    # opcional
```

### 3.4 `data/media.yaml` — Na Mídia

```yaml
# Na Mídia — cobertura e aparições do DOXA
# -----------------------------------------------
# Campos obrigatórios: title, outlet, date, type
# Campos opcionais:    authors, url, description
#
# Tipos válidos: impressa | virtual | audiovisual
#
# Ordenação: itens mais recentes no topo de cada seção.
# -----------------------------------------------

- title: "Pesquisa DOXA aponta tendências para as eleições"  # obrigatório
  authors: "Argelina Figueiredo"              # opcional — pesquisador do DOXA citado/entrevistado
  outlet: "Folha de S.Paulo"                  # obrigatório — veículo de comunicação
  date: "2024-10-03"                          # obrigatório — formato YYYY-MM-DD
  type: "impressa"                            # obrigatório — ver tipos válidos
  url: "https://www.folha.uol.com.br/..."    # opcional — link para o conteúdo
  description: ""                             # opcional — novo campo para contexto adicional
```

### 3.5 `data/acervo.yaml` — Acervo Audiovisual

```yaml
# Catálogo Audiovisual do DOXA
# -----------------------------------------------
# Campos obrigatórios: candidate, party, cargo, region, year, url
# Campos opcionais:    thumb, duration, format
#
# Cargos válidos (usados nos filtros): Presidente | Governador | Senador | Outro
# Região: estado por extenso ou "Nacional"
# Thumbs: imagem de pré-visualização do vídeo (URL do YouTube ou path local)
#
# ATENÇÃO: este arquivo pode ter centenas de entradas.
# Para manutenção em escala, consulte a seção de riscos (seção 5)
# sobre exportação automática do Google Sheets.
# -----------------------------------------------

- candidate: "Luiz Inácio Lula da Silva"     # obrigatório — nome completo do candidato
  party: "PT"                                  # obrigatório — sigla do partido
  cargo: "Presidente"                          # obrigatório — ver cargos válidos
  region: "Nacional"                           # obrigatório — estado ou "Nacional"
  year: 2022                                   # obrigatório — número inteiro
  url: "https://www.youtube.com/watch?v=xxx"  # obrigatório — link para o vídeo
  thumb: "https://img.youtube.com/vi/xxx/hqdefault.jpg"  # opcional — thumbnail
  format: "HGPE"                               # opcional — HGPE | Debate | Spot | Outro
```

### 3.6 `data/seminars.yaml` — Seminários (schema corrigido)

```yaml
# Seminários do DOXA
# -----------------------------------------------
# Campos obrigatórios: title, presenter, date
# Campos opcionais:    institution, abstract, recording_url
#
# NOTA: o campo "year" foi REMOVIDO — o ano é extraído automaticamente
# da data pelo template. Não é necessário informá-lo.
#
# Ordenação: o template agrupa automaticamente por ano.
# Coloque as entradas em qualquer ordem.
# -----------------------------------------------

- title: "Propaganda negativa e comportamento eleitoral"  # obrigatório
  presenter: "Maria Silva"                                  # obrigatório
  institution: "USP"                                        # opcional — instituição do palestrante
  date: "2024-09-15"                                        # obrigatório — formato YYYY-MM-DD
  abstract: ""                                              # opcional — resumo da apresentação
  recording_url: ""                                         # opcional — link para gravação
```

---

## 4. Checklist de manutenção

As operações abaixo requerem apenas edição de arquivos de texto. Nenhuma instalação de software é necessária para editar os dados — basta usar o editor de texto do GitHub na interface web, ou qualquer editor de texto local.

**Para qualquer alteração publicar no site:** após editar e salvar o arquivo, fazer commit e push para o branch `main`. O GitHub Actions rodará automaticamente e o site estará atualizado em cerca de 2 minutos.

---

### Adicionar membro à equipe

1. Abrir `data/team.yaml`
2. Adicionar um novo bloco no final da seção correspondente à categoria do membro (ex.: na seção de "pesquisadores")
3. Preencher os campos obrigatórios: `name`, `role`, `category`
4. Opcionalmente, adicionar `lattes`, `email`, `bio`
5. Para adicionar foto: salvar o arquivo de imagem em `static/img/team/` com o nome `nome-sobrenome.jpg`, e preencher o campo `photo: "/img/team/nome-sobrenome.jpg"`
6. Fazer commit e push

**Categorias válidas:** `coordenacao` | `pesquisadores` | `pos-doutorando` | `aluno` | `assistente` | `associado`

Exemplo de bloco a adicionar:
```yaml
- name: "João da Silva"
  role: "Pesquisador"
  category: "pesquisadores"
  lattes: "https://lattes.cnpq.br/xxxxxxxx"
  email: "joao.silva@iesp.uerj.br"
  photo: "/img/team/joao-silva.jpg"
  bio: "Doutor em Ciência Política pela UERJ."
```

---

### Publicar novo artigo ou publicação acadêmica

1. Abrir `data/publications.yaml`
2. Identificar a seção correta (Livros, Capítulos, Artigos, Outras produções)
3. Adicionar um novo bloco na seção correta — preferencialmente no topo da seção para que apareça em evidência
4. Preencher os campos obrigatórios: `title`, `authors`, `year`, `type`
5. Preencher os campos condicionais: `publisher` (para livros/capítulos) ou `journal` (para artigos)
6. Opcionalmente, adicionar `pages`, `doi`, `url`
7. Fazer commit e push

**Tipos válidos:** `livro` | `capitulo` | `artigo` | `outros`

Para **textos para discussão** (working papers), editar `data/discussions.yaml` com os campos `title`, `authors`, `year`, e `url` (quando disponível).

---

### Adicionar evento

1. Abrir `data/events.yaml`
2. Adicionar um novo bloco no **topo** do arquivo (os eventos são exibidos na ordem do arquivo, os mais recentes devem vir primeiro)
3. Preencher `title` e `date` (formato `YYYY-MM-DD`)
4. Opcionalmente adicionar `description`, `location`, `url`
5. Fazer commit e push

---

### Adicionar notícia em "Na Mídia"

1. Abrir `data/media.yaml`
2. Identificar a seção correta: `# ---- Mídia Impressa ----`, `# ---- Mídia Virtual ----` ou `# ---- Audiovisual ----`
3. Adicionar o novo bloco **no topo** da seção correspondente
4. Preencher os campos obrigatórios: `title`, `outlet`, `date` (formato `YYYY-MM-DD`), `type`
5. Opcionalmente adicionar `authors` (pesquisador do DOXA citado), `url` (link para o conteúdo)
6. Fazer commit e push

**Tipos válidos:** `impressa` | `virtual` | `audiovisual`

---

### Adicionar entrada ao acervo audiovisual

1. Abrir `data/acervo.yaml`
2. Adicionar um novo bloco em qualquer posição (o JavaScript de filtro ordena dinamicamente)
3. Preencher os campos obrigatórios: `candidate`, `party`, `cargo`, `region`, `year`, `url`
4. Opcionalmente adicionar `thumb` (URL da thumbnail do YouTube: `https://img.youtube.com/vi/VIDEO_ID/hqdefault.jpg`)
5. Fazer commit e push

**Atenção:** Se o acervo tiver centenas de entradas, a edição manual do arquivo YAML se tornará inviável. Ver seção 5 sobre a estratégia de exportação do Google Sheets.

---

## 5. Riscos e decisões em aberto

### R1 — Hugo version não fixada (risco alto, ação imediata)

O CI/CD usa `hugo-version: "latest"`. Na próxima release do Hugo que introduzir breaking changes, o build vai falhar sem aviso. **Decisão necessária:** verificar a versão atual com `hugo version` e fixá-la no workflow antes de colocar o site em produção real.

---

### R2 — Dados de exemplo em produção (risco alto, ação imediata)

Todos os arquivos `data/*.yaml` contêm apenas dados de exemplo. O campo `youtube_id: "SUBSTITUA_PELO_ID_DO_VIDEO"` em `data/homepage.yaml` vai gerar um `<iframe>` com URL inválida em produção. **Decisão necessária:** coordenar com a equipe do DOXA para mapear e preencher todos os dados reais antes do lançamento público.

---

### R3 — Estratégia para o acervo audiovisual (decisão de arquitetura)

O acervo pode ter centenas ou milhares de entradas (o DOXA cobre eleições presidenciais desde 1989 e de governadores desde 1994). Manter um arquivo `data/acervo.yaml` com esse volume torna inviável a edição manual. O comentário no arquivo menciona "exportar do Google Sheets". **Decisão necessária:** definir se o acervo será:

- (a) **Gerenciado via Google Sheets + exportação automática para YAML:** requer script de exportação (Python/Apps Script) que gera o `acervo.yaml` e faz commit. Solução escalável, mas adiciona uma dependência de processo.
- (b) **Mantido diretamente em YAML para entradas novas:** viável se o volume for pequeno (até ~200 entradas). Acima disso, a edição manual é propensa a erros.
- (c) **JSON estático gerado externamente:** o template atual já converte `hugo.Data.acervo` para `window.ACERVO_DATA` via `jsonify`. Seria possível substituir o `acervo.yaml` por um `acervo.json` gerado por script externo, sem alterar o template.

---

### R4 — Domínio do site (decisão institucional)

O site está publicado em `felipelamarca.com/DOXA/` (domínio pessoal do desenvolvedor, em subdiretório). O `baseURL` em `config.yaml` e todos os paths relativos dependem desse subdiretório. **Decisão necessária:** se o laboratório tiver ou adquirir um domínio próprio (ex.: `lab-doxa.org.br`), será necessário:

1. Atualizar `baseURL` em `config.yaml` para `"https://lab-doxa.org.br/"`
2. Criar `static/CNAME` com o domínio
3. Configurar o domínio nas configurações do GitHub Pages
4. Revisar os links hardcoded no template `layouts/index.html` que usam `{{ .Site.BaseURL }}acervo/` e `{{ .Site.BaseURL }}pesquisas/` (linhas 74 e 84) — esses links funcionam mas poderiam ser substituídos pelo helper `relURL` para mais robustez.

---

### R5 — Ausência de preview de rascunhos

Não há ambiente de staging. Qualquer push para `main` vai para produção imediatamente. Para um laboratório com múltiplos pesquisadores editando, isso pode causar publicações acidentais ou conflitos. **Decisão necessária:** avaliar se é necessário um workflow de branch de staging (ex.: `dev` → preview, `main` → produção) ou se o fluxo atual (editar localmente, revisar, fazer push) é suficiente para o volume de atualizações esperado.

---

### R6 — Seções sem layout personalizado

As seções `bancos-de-dados`, `mapas-de-votacao` e `pesquisa-covid` têm `content/_index.md` mas não têm layout personalizado em `layouts/`. Usam o fallback `_default/list.html`, que renderiza apenas o conteúdo Markdown sem nenhum dado dinâmico de YAML. **Decisão necessária:** definir o que deve aparecer nessas seções — se forem apenas páginas de texto, o layout padrão está correto; se precisarem de dados estruturados (ex.: lista de bancos de dados com links para download), precisarão de arquivo YAML e layout próprio.

---

*Fim do documento*
