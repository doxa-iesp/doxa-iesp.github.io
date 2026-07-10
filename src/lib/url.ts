/**
 * O site é publicado num subdiretório (`/DOXA/`), então TODO link interno precisa passar
 * por aqui. Escrever `href="/acervo/"` direto gera um 404 em produção.
 */
const BASE = import.meta.env.BASE_URL.replace(/\/$/, '');

export function url(caminho: string): string {
  const limpo = caminho.startsWith('/') ? caminho : `/${caminho}`;
  return `${BASE}${limpo}`;
}

/** Marca o item de menu ativo comparando caminhos normalizados. */
export function ativo(atual: string, alvo: string): boolean {
  const norm = (s: string) => s.replace(BASE, '').replace(/\/+$/, '') || '/';
  const a = norm(atual);
  const b = norm(alvo);
  return b === '/' ? a === '/' : a === b || a.startsWith(`${b}/`);
}
