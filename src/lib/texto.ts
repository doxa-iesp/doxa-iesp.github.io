/** Utilidades de texto compartilhadas pelos componentes. */

/**
 * Parte um texto entre "tudo menos a última palavra" e "a última palavra".
 *
 * É a base da assinatura tipográfica do DOXA: o site antigo escrevia
 * "Textos para **Discussão**" e "Argelina **Cheibub Figueiredo**" — primeira
 * parte em peso normal, última em destaque.
 *
 *   partirUltimaPalavra('Acervo Audiovisual')  -> ['Acervo', 'Audiovisual']
 *   partirUltimaPalavra('Produção')            -> ['', 'Produção']
 */
export function partirUltimaPalavra(texto: string): [string, string] {
  const palavras = texto.trim().split(/\s+/);
  if (palavras.length < 2) return ['', texto.trim()];
  return [palavras.slice(0, -1).join(' '), palavras[palavras.length - 1]!];
}

/**
 * Parte um nome de pessoa entre nome e sobrenome.
 * Preposições ("de", "da", "dos"…) ficam com o sobrenome:
 *   'Flávia Bozza Martins'  -> ['Flávia Bozza', 'Martins']
 *   'Maria de Lourdes Silva'-> ['Maria de Lourdes', 'Silva']
 */
export function partirNome(nome: string): [string, string] {
  return partirUltimaPalavra(nome);
}

/**
 * Tira acentos e caixa, para comparar textos em buscas e filtros:
 *   normalizar('  São Paulo ') -> 'sao paulo'
 *
 * Roda dos dois lados — no build, para gravar os atributos `data-*` dos itens, e no
 * navegador, sobre o que a pessoa digita. Os dois precisam normalizar igual, senão
 * "Brasília" digitado não acha "brasilia" gravado.
 */
export function normalizar(texto: string): string {
  return texto
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
    .toLowerCase()
    .trim();
}

/**
 * A busca do site: TODOS os termos digitados precisam aparecer, cada um como INÍCIO
 * de alguma palavra do texto.
 *   casaBusca('mariani ferri de holanda', 'holan')  -> true  (acha enquanto se digita)
 *   casaBusca('mariani ferri de holanda', 'ana')    -> false (não casa no meio da palavra)
 *   casaBusca('mariani ferri de holanda', 'ferri holanda') -> true
 *
 * `textoNormalizado` já deve ter passado por `normalizar()`. Foi este critério que se
 * validou contra os endereços antigos do WordPress: buscar pelos termos do endereço
 * de uma pesquisa acha exatamente aquela pesquisa em 59 de 61 casos.
 */
export function casaBusca(textoNormalizado: string, consulta: string): boolean {
  const termos = normalizar(consulta).split(/[^a-z0-9]+/).filter(Boolean);
  if (termos.length === 0) return true;
  const palavras = textoNormalizado.split(/[^a-z0-9]+/).filter(Boolean);
  return termos.every((termo) => palavras.some((palavra) => palavra.startsWith(termo)));
}
