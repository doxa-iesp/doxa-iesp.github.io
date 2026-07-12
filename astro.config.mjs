// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

/**
 * O site é publicado em https://doxa-iesp.github.io/ — um site de ORGANIZAÇÃO do
 * GitHub Pages, servido na RAIZ do domínio. Por isso `base` é vazio.
 *
 * (Na hospedagem anterior, em felipelamarca.com/DOXA/, o `base` era '/DOXA'. Se
 * um dia o site voltar a viver num subdiretório, é aqui que se muda — e o helper
 * `url()` de src/lib/url.ts propaga a mudança para todos os links.)
 */
const BASE = '';

/**
 * Rotas antigas que hoje só existem como página-stub de redirecionamento
 * (ver src/components/Redirecionamento.astro). Ficam fora do sitemap: são
 * `noindex` e o destino é que deve ser indexado.
 */
const ROTAS_ANTIGAS = [
  '/pesquisas/',
  '/publicacoes/',
  '/publicacoes/academicas/',
  '/publicacoes/analises-de-conjuntura/',
  '/publicacoes/textos-para-discussao/',
  '/pesquisa-covid/',
].map((r) => `${BASE}${r}`);

// Para migrar ao domínio próprio (www.lab-doxa.org.br):
//   1. trocar `site` por 'https://www.lab-doxa.org.br'
//   2. criar public/CNAME com o domínio (o CNAME da raiz do repo NÃO é publicado)
//   3. apontar o DNS e habilitar HTTPS em Settings > Pages
export default defineConfig({
  site: 'https://doxa-iesp.github.io',
  base: BASE,
  trailingSlash: 'always',
  integrations: [
    sitemap({
      filter: (pagina) => !ROTAS_ANTIGAS.includes(new URL(pagina).pathname),
    }),
  ],
  build: { format: 'directory' },
});
