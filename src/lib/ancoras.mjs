/**
 * Âncoras estáveis para itens de listas, compartilhadas pela página e pelos
 * redirecionamentos dos endereços antigos (src/lib/rotas-antigas.mjs).
 *
 * `.mjs`, não `.ts`: o astro.config.mjs importa rotas-antigas.mjs, que importa este.
 */

/**
 * `id` do card de um item do acervo, a partir do código.
 *   idItemAcervo('020/98b')      -> 'item-020-98b'
 *   idItemAcervo('1.3.3/94')     -> 'item-1-3-3-94'
 *
 * Pontos, barras e hífens viram hífen — que é exatamente o que o WordPress fazia com o
 * título do item para montar o endereço /acervo-doxa/<slug>/. Por isso 93 dos 95
 * endereços antigos casam direto com o id; os 2 que não casam estão em
 * rotas-antigas.mjs. Se mudar esta função, os redirecionamentos quebram.
 *
 * @param {string} codigo
 */
export function idItemAcervo(codigo) {
  return `item-${codigo.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '')}`;
}
