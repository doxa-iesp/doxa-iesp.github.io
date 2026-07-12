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
