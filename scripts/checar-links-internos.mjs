#!/usr/bin/env node
/**
 * Confere, no site já montado (`dist/`), que todo link e arquivo interno existe.
 *
 * POR QUE ISTO EXISTE
 * -------------------
 * O Astro não confere links para arquivos de `public/` nem links escritos à mão no conteúdo. Um
 * PDF que não chegou ao commit, um nome de arquivo digitado errado ou uma rota que mudou dão 404
 * no site publicado — com o build verde. Este script roda depois do `astro build` (no CI e em
 * `npm run verificar-links`) e falha com código 1 listando a página e o link quebrado.
 *
 * O que confere: `href` e `src` que apontam para o próprio site — relativos (`../../pdfs/x.pdf`)
 * ou a partir da raiz (`/acervo/`). Links externos, `mailto:`, `tel:` e âncoras da mesma página
 * ficam de fora (os externos têm a checagem mensal em .github/workflows/links-externos.yml).
 *
 * Uso: npm run build && npm run verificar-links
 */
import { readFileSync, readdirSync, existsSync, statSync } from 'node:fs';
import { join, relative, sep } from 'node:path';

const RAIZ = new URL('..', import.meta.url).pathname;
const DIST = join(RAIZ, 'dist');

/** O base path do site (hoje vazio). Lido do astro.config.mjs para não duplicar a configuração. */
function lerBase() {
  const config = readFileSync(join(RAIZ, 'astro.config.mjs'), 'utf8');
  const m = config.match(/const BASE = '([^']*)'/);
  return m ? m[1].replace(/\/$/, '') : '';
}

/**
 * Cópias "nome 2.html" ou pastas "nome 2" que apareçam dentro de dist/ não são parte do site: o
 * build limpo do CI nunca as gera. Não vale conferir os links delas.
 */
const ehCopia = (nome) => / \d+(\.[^.]+)?$/.test(nome);

function listarHtml(pasta) {
  return readdirSync(pasta, { withFileTypes: true }).flatMap((e) => {
    if (ehCopia(e.name)) return [];
    const caminho = join(pasta, e.name);
    if (e.isDirectory()) return listarHtml(caminho);
    return e.name.endsWith('.html') ? [caminho] : [];
  });
}

function existeNoSite(caminhoUrl) {
  let alvo = join(DIST, caminhoUrl);
  if (!existsSync(alvo)) return false;
  if (statSync(alvo).isDirectory()) alvo = join(alvo, 'index.html');
  return existsSync(alvo);
}

if (!existsSync(DIST)) {
  console.error('dist/ não existe. Rode `npm run build` antes de `npm run verificar-links`.');
  process.exit(1);
}

const BASE = lerBase();
const quebrados = [];
let conferidos = 0;

for (const arquivo of listarHtml(DIST)) {
  const rel = relative(DIST, arquivo).split(sep).join('/');
  // Endereço da página, para resolver links relativos: "producao/index.html" -> "/producao/".
  const urlPagina = `https://site.local${BASE}/${rel.replace(/index\.html$/, '')}`;
  const html = readFileSync(arquivo, 'utf8');

  for (const m of html.matchAll(/\s(?:href|src)="([^"]*)"/g)) {
    const bruto = m[1].replace(/&amp;/g, '&').trim();
    if (!bruto || /^(?:[a-z][a-z0-9+.-]*:|\/\/|#)/i.test(bruto)) continue; // externo, mailto:, âncora

    const url = new URL(bruto, urlPagina);
    let caminho;
    try {
      caminho = decodeURIComponent(url.pathname);
    } catch {
      caminho = url.pathname;
    }
    if (BASE && !caminho.startsWith(`${BASE}/`)) {
      quebrados.push({ pagina: rel, link: bruto, motivo: `fora do base path ${BASE}` });
      continue;
    }
    conferidos++;
    if (!existeNoSite(caminho.slice(BASE.length))) quebrados.push({ pagina: rel, link: bruto });
  }
}

if (quebrados.length) {
  console.error(`\n✖ ${quebrados.length} link(s) interno(s) quebrado(s) no site montado:\n`);
  for (const q of quebrados) {
    console.error(`  • ${q.pagina}\n      ${q.link}${q.motivo ? ` (${q.motivo})` : ''}`);
  }
  console.error(
    '\nConfira se o arquivo foi enviado para public/ com o mesmo nome (maiúsculas, acentos e ' +
      'espaços contam) e se o endereço está escrito certo.\n'
  );
  process.exit(1);
}

console.log(`✔ Links internos conferidos: ${conferidos}, nenhum quebrado.`);
