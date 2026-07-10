/** Estrutura do menu principal, fiel ao site antigo. */
export interface ItemMenu {
  nome: string;
  href: string;
  filhos?: { nome: string; href: string }[];
}

export const MENU: ItemMenu[] = [
  { nome: 'Início', href: '/' },
  { nome: 'Institucional', href: '/institucional/' },
  {
    nome: 'Pesquisas',
    href: '/pesquisas/',
    filhos: [
      { nome: 'Pesquisas do DOXA', href: '/pesquisas/' },
      { nome: 'Pesquisa COVID', href: '/pesquisa-covid/' },
    ],
  },
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
    nome: 'Publicações',
    href: '/publicacoes/',
    filhos: [
      { nome: 'Publicações Acadêmicas', href: '/publicacoes/academicas/' },
      { nome: 'Análises de Conjuntura', href: '/publicacoes/analises-de-conjuntura/' },
      { nome: 'Textos para Discussão', href: '/publicacoes/textos-para-discussao/' },
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
