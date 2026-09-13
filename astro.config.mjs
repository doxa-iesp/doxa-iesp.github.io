// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import { REDIRECIONAMENTOS } from './src/lib/rotas-antigas.mjs';

/**
 * O site é publicado em https://lab-doxa.org.br/ — o domínio próprio do DOXA,
 * servido pelo GitHub Pages na RAIZ. Por isso `base` é vazio.
 *
 * O domínio é o APEX, sem `www`: é o que está configurado em Settings > Pages, e o
 * `www` só redireciona para ele. `site` precisa bater com isso, porque é dele que
 * saem o canonical, o og:url e os endereços do sitemap.
 *
 * (Na hospedagem anterior, em felipelamarca.com/DOXA/, o `base` era '/DOXA'. Se
 * um dia o site voltar a viver num subdiretório, é aqui que se muda — e o helper
 * `url()` de src/lib/url.ts propaga a mudança para todos os links.)
 */
const BASE = '';

/**
 * Endereços antigos que só existem como página-stub de redirecionamento — os deste
 * site e os do WordPress (tabela em src/lib/rotas-antigas.mjs, páginas geradas por
 * src/pages/[...antiga].astro). Ficam fora do sitemap: são `noindex` e o destino é
 * que deve ser indexado.
 */
const ROTAS_ANTIGAS = Object.keys(REDIRECIONAMENTOS).map((r) => `${BASE}${r}`);

// Para trocar de domínio um dia, os três lugares que precisam bater:
//   1. `site` abaixo
//   2. public/CNAME (o CNAME da raiz do repo NÃO é publicado — só public/ entra no build)
//   3. o DNS e o domínio em Settings > Pages (com "Enforce HTTPS")
export default defineConfig({
  site: 'https://lab-doxa.org.br',
  base: BASE,
  trailingSlash: 'always',
  integrations: [
    sitemap({
      filter: (pagina) => !ROTAS_ANTIGAS.includes(new URL(pagina).pathname),
    }),
  ],
  build: { format: 'directory' },
});
