# Mudanças de layout

Registro de todo desvio em relação ao site antigo (https://www.lab-doxa.org.br).
Formato: **página** → o que mudou → por quê.

A regra é fidelidade por padrão. Cada linha abaixo existe porque havia um problema concreto,
não uma preferência estética.

---

**`/` (home)** → deixou de ser um feed de destaques de projetos e passou a ser a apresentação
institucional do grupo (missão, história, vínculo com o IESP-UERJ), com os destaques rebaixados a
uma seção secundária ("O que fazemos") → decisão de conteúdo já fechada com a Argelina, registrada
na Seção 4.1 do prompt mestre e em `docs/DECISAO_ARQUITETURA.md` §6.

**`/` (home)** → o card "Textos de discussão do Doxa" foi removido da home → no site antigo ele
apontava para a **mesma URL do Power BI** do card "Eleições Rio e São Paulo 2024", o que é
claramente um link errado. Os textos para discussão têm sua própria página no menu.

**`/` (home)** → o dashboard do Power BI virou **um** card, não dois → o site antigo mostrava
"Dashboard Rio de Janeiro" e "Dashboard São Paulo" como se fossem painéis distintos, mas existe uma
única URL de Power BI, rotulada "Eleições Rio e São Paulo 2024".

**`/institucional/`** → o texto institucional integral saiu daqui e a página passou a ser sobre a
**equipe**, com um parágrafo curto de contexto → evita duplicar o mesmo texto em duas páginas,
já que ele agora abre a home (Seção 4.1).

**Todas as páginas** → a fonte Montserrat passou a ser **auto-hospedada** (`@fontsource`), em vez
de carregada do Google Fonts → o site antigo dependia de uma requisição a `fonts.googleapis.com`,
que falha em redes restritas e envia o IP de cada visitante a um terceiro.

**Todas as páginas** → o vídeo do YouTube usa `youtube-nocookie.com` → o embed original grava
cookies de rastreamento antes de qualquer interação do usuário.

**Cabeçalho** → o item de menu ativo agora é marcado com `aria-current="page"` e destaque visual →
no site antigo a lógica de item ativo marcava "Início" em todas as páginas, porque testava se a URL
atual começava com `/`.

**Cabeçalho** → os submenus abrem por `:hover` **e** por `:focus-within` → o original só abria por
hover, então eram inalcançáveis por teclado e não abriam em tablets.

<!-- Agentes: anexem suas linhas abaixo desta marca, usando `>>`. -->

**`/seminarios/`** → o site antigo listava os seminários como texto corrido
("Apresentador (Instituição) – 'Título'. [data]"); a nova página os apresenta em cartões
agrupados por ano (decrescente), com o título em destaque → legibilidade e navegação num
acervo de 36 itens. Nenhum campo foi inventado: seminários não têm descrição nem link, então
não há botões.

**`/acervo/`** → a "pesquisa ainda em construção" do site antigo foi substituída por um filtro
multi-faceta funcional (candidato, ano, cargo, região, partido), 100% client-side → os 95 itens
são renderizados no HTML (SSG) e o JS apenas esconde os que não casam; sem JavaScript, todos
aparecem e nada se perde. O e-mail de solicitação, o catálogo completo e o formulário viraram um
bloco de acesso em destaque, porque no original essa informação vinha diluída no meio do texto.

**`/mapas-de-votacao/`** → os 273 mapas foram agrupados em `<details>` por ano (o mais recente
aberto) e, dentro de cada ano, por cargo → uma lista plana de 273 links de PDF seria uma página
gigante e sem hierarquia. Nada foi inventado: cada mapa continua sendo um link direto para o PDF
hospedado no domínio antigo.

**`/bancos-de-dados/`** → o aviso de defeito do banco das Capitais (coluna de município rotacionada
na fonte) é renderizado como alerta visível (`role="note"`, fundo terracota) dentro do respectivo
cartão → o dado errado precisa ser sinalizado a quem consulta, não silenciado.

**`/pesquisas/` `/na-midia/` `/publicacoes/textos-para-discussao/`** → o primeiro `##` das prosas dessas páginas repetia o título da página; ele é ocultado (`.prosa--intro`, `display:none`, sai também da árvore de acessibilidade) porque o `PageHero` já mostra o mesmo texto como `<h1>` → evitar título duplicado sem editar o conteúdo do Agente A.
**`/pesquisas/`** → em vez de seções fixas por status, as 61 pesquisas ficam em uma lista única ordenada por ano (desc) com etiqueta de status em cada item; as abas de filtro (Todas/Teses e Dissertações/Em Andamento/Concluídas) escondem/mostram no cliente → o filtro pedido no escopo exige um conjunto único de itens, e sem JS a lista aparece inteira.
**`/publicacoes/academicas/` `/publicacoes/analises-de-conjuntura/` `/publicacoes/textos-para-discussao/`** → adicionado link "← Todas as publicações" no topo → navegação de volta ao índice de Publicações, ausente no site antigo.
**`/publicacoes/analises-de-conjuntura/`** → cabeçalho de cada grupo rotulado como "Eleições {ciclo}", ordenados do ciclo mais recente ao mais antigo → o campo `ciclo` é só o ano; o rótulo dá contexto.
**`/na-midia/`** → datas completas exibidas como dd/mm/aaaa (datas de só ano mantidas como estão); itens mais recentes primeiro dentro de cada tipo → legibilidade em pt-BR.

**Todas as páginas** → o `<h2>` inicial da prosa, que no WordPress repetia o nome da própria
página, foi removido → ele duplicava o `<h1>` do cabeçalho da página. (`/acervo/` mantém
"Catálogo Audiovisual", que é um título de seção de verdade, e `/pesquisa-covid/` mantém suas
subseções.)

**`/bancos-de-dados/` e `/publicacoes/`** → a prosa passou a trazer só o parágrafo de introdução →
o restante repetia, palavra por palavra, os cards que já são gerados a partir dos dados. O visitante
lia a mesma descrição duas vezes na mesma tela.

**`/bancos-de-dados/`** → o botão principal deixou de apontar para a página do WordPress antigo. Os
Mapas Eleitorais levam à nossa própria página; os três bancos ganharam **"Baixar os dados (CSV)"**;
a página original virou um link secundário → o site antigo vai ser desligado, e o botão principal
apontava justamente para ele. Os CSVs agora são servidos por nós, em `public/dados/`.

**`/eventos/`** → a página não tem mais o texto introdutório → no site antigo ele era apenas o
título "Eventos DOXA", sem nenhum parágrafo. Um cabeçalho vazio abaixo do `<h1>`.
