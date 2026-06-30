# PROPOSTA_FRONTEND.md
# Avaliação e Proposta de Melhorias — Site DOXA (Hugo)

**Data**: junho de 2026  
**Escopo**: Análise do repositório em `/Users/felipelmc/Desktop/DOXA/` e comparação com a identidade visual do site original WordPress (lab-doxa.org.br)

---

## 1. Resumo Executivo

O site Hugo está bem estruturado: paleta de cores correta, header com gradiente e borda terracota fiel ao original, tipografia Montserrat implementada, responsividade básica coberta e acessibilidade inicialmente tratada (skip-nav, aria-labels, aria-expanded). A migração de dados (equipe, pesquisas, acervo, seminários, eventos, mídia, publicações) está arquitetada com YAML/JSON e templates Hugo limpos.

As principais lacunas são: (1) fundo "quadriculado" referencia um SVG genérico (`menu-icon.svg`) em vez de um tile SVG dedicado, e o overlay radial está invertido em relação ao original; (2) todos os membros da equipe estão sem foto, Lattes e e-mail — os cards ficam sem imagem e sem links, degradando radicalmente a seção mais visitada; (3) a homepage não tem conteúdo no bloco `{{ .Content }}`, deixando a seção "Destaques" vazia; (4) os dados do vídeo em destaque (`SUBSTITUA_PELO_ID_DO_VIDEO`) e os links de Power BI são placeholders; (5) o footer tem apenas o ícone do YouTube — Instagram e Twitter/X, presentes no original, estão ausentes; (6) a nav não marca o item ativo corretamente para subpáginas que compartilham prefixo de URL; (7) o `--header-h: 108px` é fixo, mas o header real tem altura variável em mobile (o menu sobrepõe conteúdo). As prioridades imediatas são os dados da equipe e o conteúdo da homepage, pois afetam diretamente a percepção de credibilidade do laboratório.

---

## 2. Tabela de Problemas

| # | Problema | Página/Componente | Severidade | Solução Proposta |
|---|----------|-------------------|------------|------------------|
| 1 | Todos os membros da equipe sem foto, sem URL Lattes e sem e-mail. Cards exibem apenas silhueta SVG e nenhum link. | `/institucional/` — `team-card.html` | **Alta** | Preencher os campos `photo`, `lattes` e `email` em `data/team.yaml` para cada membro. Fotos devem ser armazenadas em `static/img/team/` com dimensão mínima 400×400 px e comprimidas em WebP. |
| 2 | Homepage sem conteúdo no bloco "Destaques" (`{{ .Content }}`). O `_index.md` está vazio; a seção renderiza em branco entre o hero e o Vota Aí. | `layouts/index.html` — `content/_index.md` | **Alta** | Adicionar ao `content/_index.md` um parágrafo de apresentação institucional (2–3 linhas) e/ou cards de destaque em Markdown com shortcodes, ou substituir o bloco por uma seção estática de "highlights" com 3–4 ícones/métricas institucionais (ex.: "35 anos de pesquisa", "maior acervo audiovisual eleitoral do Brasil"). |
| 3 | Vídeo em destaque com `youtube_id: "SUBSTITUA_PELO_ID_DO_VIDEO"` e links de Power BI apontando para `https://app.powerbi.com/` (página raiz, sem embed real). | `data/homepage.yaml` — `layouts/index.html` | **Alta** | Substituir o `youtube_id` pelo ID real do vídeo institucional do canal DOXA no YouTube. Substituir as URLs dos dashboards pelos links de embed público do Power BI (formato: `https://app.powerbi.com/view?r=...`). Enquanto os IDs reais não estiverem disponíveis, ocultar essas seções condicionalmente com `{{ if ne .youtube_id "SUBSTITUA_PELO_ID_DO_VIDEO" }}`. |
| 4 | Fundo "quadriculado" (`bg-grid`) usa `menu-icon.svg` como tile SVG — arquivo que é o ícone do hambúrguer, não um padrão de grid. O `background-size: 5% auto` também é inadequado para um tile repetido. | `static/css/main.css` (`.bg-grid`) | **Alta** | Criar um SVG dedicado para o tile de fundo (ex.: `static/img/bg-grid-tile.svg`) — um quadrado 20×20 px com linhas ou pontos sutis. Ajustar para `background-size: 20px 20px` e aplicar o overlay radial como segunda camada: `radial-gradient(ellipse at top center, rgba(255,255,255,0) 0%, rgba(237,237,237,0.6) 100%)`. |
| 5 | Footer tem apenas ícone do YouTube. O site original possui links para Instagram e Twitter/X. | `layouts/partials/footer.html` | **Média** | Adicionar parâmetros `instagram` e `twitter` ao `config.yaml` e incluir os ícones SVG correspondentes no footer com `aria-label` adequados. Seguir o mesmo padrão de SVG inline já usado para o YouTube. |
| 6 | Indicador de item ativo na nav usa `hasPrefix $.RelPermalink .URL`, o que marca "Início" (`/`) como ativo em todas as páginas (pois toda URL começa com `/`). | `layouts/partials/nav.html` | **Média** | Substituir a lógica de active por: `{{ if and (not $.IsHome) (and (ne .URL "/") (hasPrefix $.RelPermalink .URL)) }}` — ou usar `eq $.RelPermalink .URL` para rotas exatas e `hasPrefix` apenas para itens com filhos, excluindo explicitamente o item raiz. |
| 7 | `--header-h: 108px` hardcoded no CSS. Em mobile o header tem apenas a banda do logo (sem a nav, que some); a variável usada no posicionamento do menu mobile (`top: var(--header-h)`) fica incorreta, causando deslocamento de ~50 px. | `static/css/main.css` — mobile media query | **Média** | Medir a altura real do `.header-brand` em mobile (aproximadamente 56–60 px) e criar uma segunda variável `--header-mobile-h: 60px`. Usar `top: var(--header-mobile-h)` dentro do `@media (max-width: 900px)` ou usar JavaScript para calcular a altura dinamicamente: `navWrapper.style.top = header.offsetHeight + 'px'`. |
| 8 | Iframe do YouTube sem atributo `title` único real — o `title` no iframe é o mesmo de `h2`, gerando redundância para leitores de tela. Além disso, não há fallback de texto para quando JS está desativado no acervo. | `layouts/index.html`, `layouts/acervo/list.html` | **Média** | Usar título descritivo único no iframe: `title="Vídeo institucional do DOXA no YouTube"`. Na página do acervo, adicionar `<noscript>` com mensagem orientando o usuário a habilitar JavaScript, pois todo o conteúdo da grid depende de JS. |
| 9 | Dropdowns na nav desktop são ativados apenas por `:hover` (CSS puro). Em dispositivos touch (tablets) o hover não funciona e o dropdown nunca abre. | `layouts/partials/nav.html`, `static/css/main.css`, `static/js/main.js` | **Média** | Adicionar suporte a `click`/`touchstart` nos itens com dropdown via JS (já existe a lógica mobile; estendê-la para detectar `pointer: coarse` com `matchMedia`). Alternativamente, tornar o clique no `nav-link` em desktop um toggle do dropdown ao invés de navegar para a URL pai. |
| 10 | Logos e ícones sociais sem dimensões explícitas no footer (apenas `width="130" height="40"`). Em mobile, o logo pode colapsar. O footer usa `grid-template-columns: auto 1fr auto` — em telas < 480 px, o grid de 3 colunas não colapsa, empilhando itens que ficam muito estreitos. | `layouts/partials/footer.html`, `static/css/main.css` | **Média** | Adicionar breakpoint `@media (max-width: 600px)` específico para o footer com `grid-template-columns: 1fr` (já existe para 900px; precisa ser estendido para 600px). |
| 11 | Tags `<img>` de membros da equipe sem dimensões explícitas (`width`/`height`). Causa Cumulative Layout Shift (CLS) enquanto as imagens carregam. | `layouts/partials/team-card.html` | **Média** | Adicionar `width="220" height="220"` (ou usar `aspect-ratio: 1` já presente no `.team-card-photo` — o que já mitiga parcialmente). Certificar que o CSS `object-fit: cover` está ativo (está). Avaliar uso de `fetchpriority="high"` para o primeiro card visível. |
| 12 | Fonte Montserrat carregada via `<link rel="stylesheet">` do Google Fonts sem `font-display: swap`. Isso causa FOIT (Flash of Invisible Text) em conexões lentas. | `layouts/_default/baseof.html` | **Média** | Adicionar `&display=swap` à URL do Google Fonts: `?family=Montserrat:wght@400;500;600;700&display=swap` (já presente na URL — verificar se está sendo usado corretamente e considerar auto-hospedar a fonte com `@font-face` + `font-display: swap` para eliminar dependência externa e requisição bloqueante). |
| 13 | Seção "Acervo Audiovisual" na homepage tem texto estático desconectado do dado real. O botão "Acessar o Acervo" não faz parte de um grid de duas colunas funcional — a coluna direita (imagem ou preview do acervo) está ausente, deixando o layout `grid-template-columns: 1fr 1fr` com apenas uma célula preenchida. | `layouts/index.html` — seção Acervo | **Baixa** | Adicionar à coluna direita uma imagem representativa do acervo (ex.: screenshot de uma VT de campanha histórica) ou um contador dinâmico de itens do acervo via `len hugo.Data.acervo`. Isso completa o grid de duas colunas previsto no design. |
| 14 | Cor do texto de parágrafos em `page-content` usa `var(--color-text-light)` (#555), que tem contraste de aproximadamente 5.7:1 contra fundo branco — aprovado pelo WCAG AA, mas abaixo do WCAG AAA (7:1). Para um laboratório acadêmico, AAA é desejável. | `static/css/main.css` | **Baixa** | Substituir `--color-text-light: #555` por `#4a4a4a` (contraste ~7.5:1) ou usar `var(--color-text)` (#26231E, contraste ~15:1) para body text de artigos e publicações. Manter #555 apenas para metadados secundários (datas, badges). |
| 15 | Nenhum arquivo `robots.txt` ou `sitemap.xml` configurado explicitamente. O Hugo gera sitemap automaticamente, mas `robots.txt` requer arquivo em `static/`. Sem ele, crawlers podem indexar o subdiretório `/DOXA/` de forma subótima. | Configuração geral — `config.yaml` | **Baixa** | Criar `static/robots.txt` com `Sitemap: https://felipelamarca.com/DOXA/sitemap.xml` e verificar se o deploy em subdiretório (`baseURL: https://felipelamarca.com/DOXA/`) está gerando o sitemap com URLs absolutas corretas. |
| 16 | Cards de equipe sem `aria-label` na div wrapper do card. Leitores de tela navegam de card em card sem contexto (apenas anunciam os links internos). | `layouts/partials/team-card.html` | **Baixa** | Transformar `.team-card` em `<article aria-label="{{ .name }}">` para que leitores de tela anunciem o nome do pesquisador ao entrar no card. |

---

## 3. Recomendações de UI/UX

### 3.1 Hierarquia visual na homepage
A homepage atual é quase toda texto, sem imagens ou elementos visuais de quebra. O site WordPress original usa banners com imagens, destaques coloridos e elementos de separação visual. Recomenda-se:
- Adicionar pelo menos uma imagem representativa em cada seção "two-column" (Vota Aí e Acervo).
- Criar uma seção de "números do laboratório" (ex.: "35+ anos de pesquisa", "X candidatos no acervo", "X publicações") com ícones simples e os valores dos dados YAML — comunica credibilidade institucional rapidamente.

### 3.2 Cards de pesquisa
Os itens da página `/pesquisas/` são listas planas com título, badge e metadados. O original apresenta as pesquisas com mais destaque visual. Considerar adicionar `border-left: 4px solid` com cor variável por status (já existe no CSS de publicações — `.publication-item` — mas não foi aplicado ao `.pesquisa-item`). Solução: aplicar `border-left: 4px solid` no `.pesquisa-item` usando as mesmas cores dos badges: verde para concluída, laranja para andamento, azul para tese.

### 3.3 Indicadores de seção ativa no breadcrumb
Nenhuma página tem breadcrumb ou indicador de localização além do item ativo na nav. Para seções profundas (ex.: `seminarios`, `analises-de-conjuntura`), o usuário perde o contexto. Recomendar um breadcrumb simples em linha ("Início > Eventos > Seminários") usando o Hugo template `{{ .Ancestors }}`.

### 3.4 Tipografia: hierarquia entre seções
`h2` e `h3` usam a mesma cor `var(--color-primary)`. Em páginas com muito conteúdo (publicações, bancos de dados), a hierarquia fica difusa. Recomendação: `h3` usar `var(--color-text)` (#26231E) com `font-weight: 600` em vez de 700, diferenciando visualmente dos `h2` que permanecem em azul primário.

### 3.5 Feedback visual nos filtros do acervo
O botão "Limpar filtros" está estilizado como `btn-outline` mas não tem estado de loading nem feedback quando nenhum resultado é encontrado além da mensagem de texto. Adicionar uma transição de `opacity` no `#acervo-grid` durante a filtragem (JS já presente) e um estado visual mais destacado para o "0 itens encontrados" (ex.: ícone + mensagem maior).

### 3.6 Mobile: menu hambúrguer sem indicação de estado "aberto"
O botão hambúrguer altera `aria-expanded` mas as 3 barras não animam para "X" quando aberto. O CSS tem as classes mas falta a regra de transformação. Adicionar ao CSS:
```css
.nav-toggle[aria-expanded="true"] span:nth-child(1) { transform: translateY(9px) rotate(45deg); }
.nav-toggle[aria-expanded="true"] span:nth-child(2) { opacity: 0; }
.nav-toggle[aria-expanded="true"] span:nth-child(3) { transform: translateY(-9px) rotate(-45deg); }
```

---

## 4. Limitações do Framework Hugo

### 4.1 Busca full-text
Hugo não tem busca server-side. A busca do acervo é client-side (JS + YAML embutido no HTML via `window.ACERVO_DATA`). Se o acervo crescer para milhares de itens, o payload JSON embutido na página vai degradar o tempo de carregamento. Solução de longo prazo: usar Pagefind (ferramenta de busca estática para Hugo) ou Fuse.js com índice pré-gerado em arquivo JSON separado carregado sob demanda.

### 4.2 Conteúdo dinâmico
Power BI embeds e filtros do acervo funcionam, mas qualquer dado que precise ser atualizado (novas pesquisas, novos membros) requer rebuild e redeploy do site. Isso é aceitável para um laboratório, mas o fluxo de edição exige conhecimento de Git/Hugo. Recomendação: documentar o processo de edição dos arquivos YAML e criar um `CONTRIBUTING.md` simples para que colaboradores não-técnicos possam abrir PRs de atualização de dados.

### 4.3 Dropdowns no menu vs. Hugo
O menu com dropdowns é configurado via `params.children` no `config.yaml`, o que é uma solução funcional mas não é o padrão Hugo (que usa menus aninhados nativos via `menu.main` com `parent`). A solução atual dificulta adicionar novos sublinks sem editar manualmente o YAML de config. Isso não é uma limitação do Hugo em si, mas uma escolha de implementação que pode ser melhorada migrando para menus aninhados nativos do Hugo (`identifier` + `parent`).

### 4.4 Formulários de contato
Hugo é estático — não há como processar formulários server-side. O contato atual é apenas um link `mailto:`, o que é funcional mas limitado. Alternativas sem backend: Netlify Forms (incompatível com GitHub Pages), Formspree, ou Basin — qualquer um deles requer apenas um `action` no `<form>`.

---

## 5. Priorização por Impacto vs. Esforço

| Prioridade | Melhoria | Impacto Visual | Esforço de Implementação |
|------------|----------|----------------|--------------------------|
| 1 | Preencher dados da equipe (fotos + Lattes + e-mail) — Problema #1 | Altíssimo | Baixo (editar YAML + adicionar imagens) |
| 2 | Animação do hambúrguer mobile (X quando aberto) — Seção 3.6 | Alto | Muito baixo (3 regras CSS) |
| 3 | Corrigir lógica de item ativo na nav — Problema #6 | Médio | Baixo (1 linha de template Hugo) |
| 4 | Criar tile SVG dedicado para fundo quadriculado — Problema #4 | Alto | Baixo (criar 1 SVG + 3 linhas CSS) |
| 5 | Adicionar conteúdo à homepage (`_index.md`) — Problema #2 | Altíssimo | Baixo (editar Markdown) |
| 6 | Corrigir `youtube_id` e URLs dos dashboards — Problema #3 | Alto | Baixo (editar YAML com valores reais) |
| 7 | Border-left colorida por status nas pesquisas — Seção 3.2 | Médio | Muito baixo (3 linhas CSS) |
| 8 | Adicionar redes sociais ao footer — Problema #5 | Médio | Baixo (config.yaml + partial footer) |
| 9 | Corrigir `--header-h` mobile — Problema #7 | Médio | Baixo (1 variável CSS + 2 linhas JS) |
| 10 | Suporte a touch nos dropdowns desktop — Problema #9 | Médio | Médio (lógica JS adicional) |
| 11 | Adicionar imagem à seção Acervo na homepage — Problema #13 | Médio | Baixo (1 imagem + HTML) |
| 12 | `<article aria-label>` nos cards de equipe — Problema #16 | Baixo | Muito baixo (1 tag HTML) |
| 13 | Melhorar contraste do texto secundário — Problema #14 | Baixo | Muito baixo (1 valor CSS) |
| 14 | `robots.txt` e verificação do sitemap — Problema #15 | Baixo (SEO) | Baixo (1 arquivo) |
| 15 | Noscript fallback no acervo — Problema #8 | Baixo | Muito baixo (1 tag HTML) |
| 16 | Busca full-text com Pagefind — Seção 4.1 | Alto (longo prazo) | Alto (integração de ferramenta) |
