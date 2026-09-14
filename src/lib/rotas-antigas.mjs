/**
 * Para onde vai cada endereço antigo.
 *
 * POR QUE EXISTE
 * --------------
 * O domínio lab-doxa.org.br era do WordPress antigo e agora serve este site. Todo link
 * de fora que citava uma página do WordPress — no Google, em artigos, em currículos —
 * passou a cair aqui. O GitHub Pages não faz redirecionamento no servidor, então há dois
 * mecanismos, os dois alimentados por este arquivo:
 *
 *   1. REDIRECIONAMENTOS (caminho exato → destino): viram páginas-stub geradas no build
 *      por src/pages/[...antiga].astro, que respondem 200 com meta refresh e canonical.
 *      Ficam fora do sitemap (astro.config.mjs).
 *   2. destinoAntigo() (padrões, como /acervo-doxa/<item>/): roda no navegador, dentro
 *      da página 404 (src/pages/404.astro), porque são centenas de endereços.
 *      Arquivos antigos (/wp-content/uploads/…) são resolvidos pelo nome, com a tabela
 *      gerada em /arquivos-antigos.json (src/pages/arquivos-antigos.json.ts).
 *
 * A lista do que existia no site antigo está em extracao/dados/enderecos-antigos.txt.
 * Ao mexer aqui, confira contra ela: cada endereço da lista precisa cair numa página que
 * existe (CLAUDE.md, "Estrutura do site").
 *
 * `.mjs`, não `.ts`: o astro.config.mjs importa este arquivo.
 */
import { idItemAcervo } from './ancoras.mjs';

/** Caminho exato do site antigo (ou de uma rota antiga deste site) → caminho novo. */
export const REDIRECIONAMENTOS = {
  // Rotas antigas deste próprio site, de antes de /producao/ e /projetos/.
  '/pesquisas/': '/producao/pesquisas/',
  '/pesquisa-covid/': '/projetos/pesquisa-covid/',
  '/publicacoes/': '/producao/',
  '/publicacoes/academicas/': '/producao/publicacoes/',
  '/publicacoes/analises-de-conjuntura/': '/producao/analises-de-conjuntura/',
  '/publicacoes/textos-para-discussao/': '/producao/textos-para-discussao/',

  // Páginas do WordPress.
  '/pagina-pesquisas/': '/producao/pesquisas/',
  '/pesquisas-realizadas/': '/producao/pesquisas/',
  '/teses-e-dissertacoes/': '/producao/pesquisas/',
  '/publicacoes-academicas/': '/producao/publicacoes/',
  '/analises-de-conjuntura-eleitoral/': '/producao/analises-de-conjuntura/',
  '/analise/': '/producao/analises-de-conjuntura/',
  '/textos-para-discussao/': '/producao/textos-para-discussao/',
  '/textos-para-discussao-2/': '/producao/textos-para-discussao/',
  '/covid-no-estado-do-rio-monitoramento-e-efeitos/': '/projetos/pesquisa-covid/',
  '/programas-eleitorais-dos-candidatos-a-prefeito-das-capitais/': '/bancos-de-dados/',
  '/programas-eleitorais-dos-candidatos-a-prefeito-do-estado-do-rio-de-janeiro/': '/bancos-de-dados/',

  // Posts do WordPress.
  '/novo-texto-para-discussao-as-politicas-de-controle-de-armas-de-fogo-e-municoes-no-brasil/':
    '/producao/textos-para-discussao/',
  '/seminario-comemora-25-anos-do-doxa/': '/eventos/',
  '/doxa-20-anos-o-legado-de-marcus-figueiredo/': '/eventos/',
  '/seminario-marcus-figueiredo-eleicoes-opiniao-publica-e-comunicacao-politica-no-brasil-contemporaneo/':
    '/eventos/',
  '/edicao-digital-gratuita-do-livro-a-decisao-do-voto-de-marcus-figueiredo/': '/eventos/',
  '/coordenadora-do-doxa-recebe-premio-de-excelencia-academica-da-anpocs/': '/eventos/',

  // Ficam de fora DE PROPÓSITO, e continuam dando 404: a nota sobre o falecimento de
  // Marcus Figueiredo (removida a pedido da coordenação) e as páginas-padrão do WordPress
  // (/ola-mundo/, /pagina-exemplo/, /nova-pagina-inicial/).
};

/** Endereços antigos do acervo cujo slug não bate com o id do card (ver ancoras.mjs). */
const ACERVO_EXCECOES = {
  '009-98-2': 'item-009-98',
  '1-10-94-dvdi': 'item-1-10-94dvdi',
};

/** Regiões do acervo no WordPress → valor do filtro no site novo. */
const REGIOES = {
  nacional: 'Nacional',
  'estados-df': 'Estados e Distrito Federal',
};

const espacos = (slug) => slug.replace(/-/g, ' ');

/**
 * Destino de um endereço antigo que segue um PADRÃO. Devolve o caminho novo (com busca
 * ou âncora, se for o caso) ou `null` quando não há para onde mandar.
 *
 *   destinoAntigo('/acervo-doxa/020-98b/')                 -> '/acervo/#item-020-98b'
 *   destinoAntigo('/lista-pesquisas/torres-ariel-lopes-2020/')
 *                                     -> '/producao/pesquisas/?busca=torres%20ariel%20lopes%202020'
 *   destinoAntigo('/partidos/pcdob/')                       -> '/acervo/?partido=pcdob'
 *
 * Os caminhos exatos de REDIRECIONAMENTOS não passam por aqui: já existem como página.
 * Arquivos de /wp-content/uploads/ também não: ver `nomeDeArquivoAntigo()`.
 *
 * @param {string} caminho  `location.pathname`, com ou sem barra final
 * @returns {string | null}
 */
export function destinoAntigo(caminho) {
  let c;
  try {
    c = decodeURIComponent(caminho);
  } catch {
    c = caminho;
  }
  c = c.toLowerCase().replace(/\/page\/\d+\/?$/, '/'); // paginação das listas do WordPress
  if (!c.endsWith('/')) c += '/';
  const partes = c.split('/').filter(Boolean);
  const [secao, slug] = partes;
  if (!secao) return null;

  const exato = REDIRECIONAMENTOS[c];
  if (exato) return exato;

  switch (secao) {
    case 'acervo-doxa':
      return slug ? `/acervo/#${ACERVO_EXCECOES[slug] ?? idItemAcervo(slug)}` : '/acervo/';
    case 'lista-pesquisas':
      return slug
        ? `/producao/pesquisas/?busca=${encodeURIComponent(espacos(slug))}`
        : '/producao/pesquisas/';
    case 'candidatos-presidente':
    case 'candidatos-governador': {
      // O último termo do slug é quase sempre o nome pelo qual o candidato aparece no
      // acervo ("anthony-garotinho" → "Garotinho", "brigadeiro-ivan-frota" → "Frota").
      const termo = slug?.split('-').filter(Boolean).pop();
      return termo ? `/acervo/?candidato=${encodeURIComponent(termo)}` : '/acervo/';
    }
    case 'partidos':
      return slug ? `/acervo/?partido=${encodeURIComponent(slug)}` : '/acervo/';
    case 'ano':
      return slug && /^\d{4}$/.test(slug) ? `/acervo/?ano=${slug}` : '/acervo/';
    case 'regiao':
      return slug && REGIOES[slug]
        ? `/acervo/?regiao=${encodeURIComponent(REGIOES[slug])}`
        : '/acervo/';
    // Apesar do nome, /partido/<slug>/ era o endereço da taxonomia de CARGO no WordPress
    // (/partido/governador/, /partido/presidente/); os partidos viviam em /partidos/.
    case 'cargo-eletivo':
    case 'partido':
      return slug ? `/acervo/?cargo=${encodeURIComponent(espacos(slug))}` : '/acervo/';
    case 'estado':
    case 'tipo-de-video':
      return '/acervo/';
    case 'tipo-pesquisa':
      return '/producao/pesquisas/';
    case 'textos-discussao':
      return '/producao/textos-para-discussao/';
    case 'category':
    case 'tag':
      return '/eventos/';
    default:
      return null;
  }
}

/**
 * Nome do arquivo de um endereço antigo de /wp-content/uploads/, em minúsculas, para
 * procurar em /arquivos-antigos.json. `null` se não for um arquivo do WordPress.
 *
 *   nomeDeArquivoAntigo('/wp-content/uploads/2022/10/PAN-DE1998.pdf') -> 'pan-de1998.pdf'
 *
 * @param {string} caminho
 * @returns {string | null}
 */
export function nomeDeArquivoAntigo(caminho) {
  if (!caminho.startsWith('/wp-content/uploads/')) return null;
  const nome = caminho.split('/').pop();
  if (!nome) return null;
  try {
    return decodeURIComponent(nome).toLowerCase();
  } catch {
    return nome.toLowerCase();
  }
}
