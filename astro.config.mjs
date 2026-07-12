// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

const BASE = '/DOXA';

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

// Deploy atual: https://felipelamarca.com/DOXA/
// Para migrar ao domínio próprio (www.lab-doxa.org.br):
//   1. trocar `site` por 'https://www.lab-doxa.org.br'
//   2. REMOVER a linha `base` (e o BASE acima vira '')
//   3. criar public/CNAME com o domínio (o CNAME da raiz do repo NÃO é publicado)
export default defineConfig({
  site: 'https://felipelamarca.com',
  base: BASE,
  trailingSlash: 'always',
  integrations: [
    sitemap({
      filter: (pagina) => !ROTAS_ANTIGAS.includes(new URL(pagina).pathname),
    }),
  ],
  build: { format: 'directory' },
});
