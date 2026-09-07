/**
 * TODO link interno passa por aqui. Hoje o site é servido na raiz
 * (https://doxa-iesp.github.io/), então `url()` devolve o caminho como está — mas
 * se um dia ele voltar a viver num subdiretório (como já viveu, em
 * felipelamarca.com/DOXA/), basta mudar o `base` em astro.config.mjs e todos os
 * links continuam certos. Escrever `href="/acervo/"` cru quebraria nesse caso.
 */
const BASE = import.meta.env.BASE_URL.replace(/\/$/, '');

export function url(caminho: string): string {
  const limpo = caminho.startsWith('/') ? caminho : `/${caminho}`;
  return `${BASE}${limpo}`;
}

/** Um link é externo quando aponta para outro domínio (ou é um mailto). */
export function externo(destino: string): boolean {
  return /^(https?:)?\/\//.test(destino) || destino.startsWith('mailto:');
}

/**
 * Resolve um link que pode ser interno ou externo. Os projetos, por exemplo,
 * têm `links[]` que tanto podem apontar para `/mapas-de-votacao/` quanto para
 * um site de fora — só os externos levam `target="_blank"`.
 */
export function linkPara(destino: string): string {
  return externo(destino) ? destino : url(destino);
}

/**
 * Igualdade exata de caminhos (ignorando BASE e barra final). Serve para
 * distinguir "esta É a página" de "esta página está dentro desta seção" —
 * `ativo()` casa por prefixo e marcaria "Produção" como página atual em
 * /producao/pesquisas/.
 */
export function mesmaPagina(atual: string, alvo: string): boolean {
  const norm = (s: string) => s.replace(BASE, '').replace(/\/+$/, '') || '/';
  return norm(atual) === norm(alvo);
}

/** Marca o item de menu ativo comparando caminhos normalizados. */
export function ativo(atual: string, alvo: string): boolean {
  const norm = (s: string) => s.replace(BASE, '').replace(/\/+$/, '') || '/';
  const a = norm(atual);
  const b = norm(alvo);
  return b === '/' ? a === '/' : a === b || a.startsWith(`${b}/`);
}
