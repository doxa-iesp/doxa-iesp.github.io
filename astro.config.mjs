// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// Deploy atual: https://felipelamarca.com/DOXA/
// Para migrar ao domínio próprio (www.lab-doxa.org.br):
//   1. trocar `site` por 'https://www.lab-doxa.org.br'
//   2. REMOVER a linha `base`
//   3. criar public/CNAME com o domínio (o CNAME da raiz do repo NÃO é publicado)
export default defineConfig({
  site: 'https://felipelamarca.com',
  base: '/DOXA',
  trailingSlash: 'always',
  integrations: [sitemap()],
  build: { format: 'directory' },
});
