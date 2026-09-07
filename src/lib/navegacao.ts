/** Estrutura do menu principal. */
export interface ItemMenu {
  nome: string;
  href: string;
  filhos?: ItemSubmenu[];
}

export interface ItemSubmenu {
  nome: string;
  href: string;
  /**
   * Marca o item que é a própria capa da seção — o primeiro de cada submenu, que
   * repete o destino do item pai. Ele existe porque, no desktop, clicar no pai é
   * justamente o gesto que abre o menu; sem esse item a capa fica difícil de
   * alcançar (e no toque em tablet, impossível). O Header o separa por uma régua
   * para que os demais se leiam como subtópicos.
   */
  capa?: boolean;
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
      { nome: 'Visão geral', href: '/producao/', capa: true },
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
      { nome: 'Visão geral', href: '/bancos-de-dados/', capa: true },
      { nome: 'Mapas de Votação', href: '/mapas-de-votacao/' },
    ],
  },
  {
    nome: 'Eventos',
    href: '/eventos/',
    filhos: [
      // "Todos os Eventos" era rótulo falso: /eventos/ tem 5 itens e NÃO inclui
      // os 36 seminários — as duas listas são disjuntas.
      { nome: 'Visão geral', href: '/eventos/', capa: true },
      { nome: 'Seminários', href: '/seminarios/' },
    ],
  },
  { nome: 'Na Mídia', href: '/na-midia/' },
];
