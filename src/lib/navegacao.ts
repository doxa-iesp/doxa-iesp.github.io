/** Estrutura do menu principal. */
export interface ItemMenu {
  nome: string;
  href: string;
  filhos?: { nome: string; href: string }[];
}

/**
 * "Produção" reúne o que o laboratório produz — pesquisas E publicações — que
 * antes eram duas ilhas separadas no menu.
 *
 * "Projetos" reúne as iniciativas com entrega pública (Vota Aí, dashboards,
 * Pesquisa COVID, Geografia do Voto), que antes ficavam espalhadas pela home.
 */
export const MENU: ItemMenu[] = [
  { nome: 'Início', href: '/' },
  { nome: 'Institucional', href: '/institucional/' },
  {
    nome: 'Produção',
    href: '/producao/',
    filhos: [
      { nome: 'Toda a produção', href: '/producao/' },
      { nome: 'Pesquisas', href: '/producao/pesquisas/' },
      { nome: 'Publicações Acadêmicas', href: '/producao/publicacoes/' },
      { nome: 'Análises de Conjuntura', href: '/producao/analises-de-conjuntura/' },
      { nome: 'Textos para Discussão', href: '/producao/textos-para-discussao/' },
    ],
  },
  { nome: 'Projetos', href: '/projetos/' },
  { nome: 'Acervo', href: '/acervo/' },
  {
    nome: 'Bancos de Dados',
    href: '/bancos-de-dados/',
    filhos: [
      { nome: 'Bancos de Dados', href: '/bancos-de-dados/' },
      { nome: 'Mapas de Votação', href: '/mapas-de-votacao/' },
    ],
  },
  {
    nome: 'Eventos',
    href: '/eventos/',
    filhos: [
      { nome: 'Todos os Eventos', href: '/eventos/' },
      { nome: 'Seminários', href: '/seminarios/' },
    ],
  },
  { nome: 'Na Mídia', href: '/na-midia/' },
];
