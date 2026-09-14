#!/usr/bin/env node
/**
 * Confere se os links do Google Drive e do Docs citados no conteúdo ainda abrem para qualquer pessoa.
 *
 * POR QUE ISTO EXISTE
 * -------------------
 * Os mapas de votação e vários outros arquivos moram no Drive do DOXA (CLAUDE.md, armadilha 2d).
 * Arquivo apagado dá 404, mas arquivo que deixou de ser público não dá erro: o Google redireciona
 * para a tela de login. E o Google também redireciona, ou responde 429, quando recebe pedidos
 * demais seguidos. Na segunda rodada da checagem mensal, em 2026-09-14, 18 mapas "quebraram"
 * assim e abriam normalmente logo depois. O lychee, que confere os outros links, não distingue um
 * caso do outro. Este script distingue pelo destino do redirecionamento e confere de novo, com
 * pausa, tudo o que falhou; só entra no relatório como quebrado o que falhar todas as vezes.
 *
 * Roda na checagem mensal (.github/workflows/links-externos.yml). Não bloqueia build nem deploy.
 *
 * Uso: node scripts/checar-links-drive.mjs [--saida relatorio.md]
 *   DRIVE_INTERVALO_MS  espera entre dois pedidos (padrão 1000)
 *   DRIVE_PAUSAS_S      pausas antes de cada nova tentativa, em segundos (padrão "120,600")
 */
import { appendFileSync, mkdirSync, readFileSync, readdirSync, writeFileSync } from 'node:fs';
import { dirname, join, relative, sep } from 'node:path';
import { pathToFileURL } from 'node:url';

const RAIZ = new URL('..', import.meta.url).pathname;
const PADRAO_LINK = /https?:\/\/(?:drive|docs)\.google\.com\/[^\s"'<>)\]]+/g;
const AGENTE = 'checagem-de-links-do-DOXA (+https://github.com/doxa-iesp/doxa-iesp.github.io)';

const esperar = (ms) => new Promise((resolver) => setTimeout(resolver, ms));

/** As mesmas entradas da checagem geral: as listas de src/data e tudo o que há em src/content. */
function listarEntradas() {
  const listar = (pasta) =>
    readdirSync(pasta, { withFileTypes: true }).flatMap((e) =>
      e.isDirectory() ? listar(join(pasta, e.name)) : [join(pasta, e.name)],
    );
  const dados = readdirSync(join(RAIZ, 'src/data'))
    .filter((nome) => nome.endsWith('.yaml'))
    .map((nome) => join(RAIZ, 'src/data', nome));
  return [...dados, ...listar(join(RAIZ, 'src/content'))];
}

/** Cada link, uma vez só, com o lugar onde aparece primeiro ("src/data/mapas-votacao.yaml:1273"). */
export function extrairLinks(arquivos) {
  const links = new Map();
  for (const arquivo of arquivos) {
    const rel = relative(RAIZ, arquivo).split(sep).join('/');
    readFileSync(arquivo, 'utf8')
      .split('\n')
      .forEach((linha, i) => {
        for (const [bruto] of linha.matchAll(PADRAO_LINK)) {
          const url = bruto.replace(/[.,;:]+$/, '');
          if (!links.has(url)) links.set(url, `${rel}:${i + 1}`);
        }
      });
  }
  return links;
}

/**
 * O que uma resposta diz sobre o arquivo:
 *   ok          abre para qualquer pessoa
 *   apagado     404 ou 410
 *   privado     redireciona para o login do Google: o arquivo deixou de ser público
 *   limitado    429, erro 5xx, falha de rede ou a página "sorry" do Google: o pedido foi recusado
 *               naquele momento, e isso não diz nada sobre o arquivo
 *   inesperado  qualquer outra resposta
 */
export function classificar(status, destino = '') {
  const redireciona = status >= 300 && status < 400;
  if (status >= 200 && status < 300) return 'ok';
  if (status === 404 || status === 410) return 'apagado';
  if (redireciona && /^https:\/\/accounts\.google\.com\//.test(destino)) return 'privado';
  if (status === 0 || status === 429 || status >= 500) return 'limitado';
  if (redireciona && /^https:\/\/(www\.)?google\.com\/sorry\//.test(destino)) return 'limitado';
  return 'inesperado';
}

/** Um pedido, seguindo só redirecionamento dentro do próprio Drive/Docs (ex.: /open?id= → /file/d/). */
async function consultar(url, buscar) {
  let atual = url;
  for (let salto = 0; salto < 5; salto++) {
    let resposta;
    try {
      resposta = await buscar(atual, {
        redirect: 'manual',
        headers: { 'user-agent': AGENTE },
        signal: AbortSignal.timeout(30_000),
      });
    } catch (erro) {
      return { situacao: 'limitado', status: 0, destino: '', detalhe: erro.cause?.code ?? erro.name };
    }
    await resposta.body?.cancel().catch(() => {}); // só o status e o destino interessam
    const local = resposta.headers.get('location');
    const destino = local ? new URL(local, atual).href : '';
    const redireciona = resposta.status >= 300 && resposta.status < 400;
    if (redireciona && /^https:\/\/(drive|docs)\.google\.com\//.test(destino)) {
      atual = destino;
      continue;
    }
    return { situacao: classificar(resposta.status, destino), status: resposta.status, destino };
  }
  return { situacao: 'inesperado', status: 0, destino: atual, detalhe: 'redirecionamentos demais' };
}

/** Confere todos os links e, depois de cada pausa, de novo os que falharam. */
export async function checar(
  links,
  { buscar = fetch, intervaloMs = 1000, pausasMs = [120_000, 600_000], log = console.log } = {},
) {
  const resultados = new Map();
  const conferir = async (urls) => {
    for (const [i, url] of urls.entries()) {
      if (i > 0) await esperar(intervaloMs);
      resultados.set(url, await consultar(url, buscar));
    }
  };

  await conferir([...links.keys()]);
  for (const pausa of pausasMs) {
    const falhas = [...resultados].filter(([, r]) => r.situacao !== 'ok').map(([url]) => url);
    if (!falhas.length) break;
    log(`${falhas.length} link(s) falharam; nova tentativa em ${pausa / 1000} s.`);
    await esperar(pausa);
    await conferir(falhas);
  }
  return resultados;
}

const MOTIVOS = {
  apagado: 'o arquivo não existe mais',
  privado: 'o arquivo deixou de ser público (o Google pede login)',
  inesperado: 'resposta inesperada',
};

/** Relatório em Markdown, no formato da issue "Links quebrados". */
export function montarRelatorio(links, resultados, pausasMs) {
  const quebrados = [];
  const naoConferidos = [];
  for (const [url, r] of resultados) {
    if (r.situacao === 'ok') continue;
    (r.situacao === 'limitado' ? naoConferidos : quebrados).push({ url, onde: links.get(url), ...r });
  }
  const resposta = (r) =>
    [r.status || r.detalhe, r.destino && `→ ${r.destino}`].filter(Boolean).join(' ');
  const minutos = pausasMs.map((ms) => `${Math.round(ms / 60_000)} min`).join(' e ');
  const tentativas = pausasMs.length ? ` O que falhou foi conferido de novo ${minutos} depois.` : '';

  const linhas = [
    '# Google Drive e Docs',
    '',
    `${links.size} links conferidos, um de cada vez.${tentativas}`,
    '',
    quebrados.length ? `## Quebrados (${quebrados.length})` : 'Nenhum link do Drive quebrado.',
  ];
  if (quebrados.length) {
    linhas.push('');
    for (const q of quebrados) {
      const motivo = MOTIVOS[q.situacao] + (q.situacao === 'inesperado' ? ` (${resposta(q)})` : '');
      linhas.push(`* [ ] <${q.url}> em \`${q.onde}\`: ${motivo}`);
    }
  }
  if (naoConferidos.length) {
    linhas.push(
      '',
      `## Não deu para conferir (${naoConferidos.length})`,
      '',
      'O Google (ou a rede) recusou estes pedidos em todas as tentativas. Não é sinal de arquivo',
      'quebrado; a checagem do mês que vem confere de novo.',
      '',
      ...naoConferidos.map((q) => `* <${q.url}> em \`${q.onde}\`: ${resposta(q)}`),
    );
  }
  return {
    texto: `${linhas.join('\n')}\n`,
    quebrados: quebrados.length,
    naoConferidos: naoConferidos.length,
  };
}

async function principal() {
  const i = process.argv.indexOf('--saida');
  const saida = i > 0 ? process.argv[i + 1] : null;
  const intervaloMs = Number(process.env.DRIVE_INTERVALO_MS ?? 1000);
  const pausasMs = (process.env.DRIVE_PAUSAS_S ?? '120,600')
    .split(',')
    .filter((s) => s.trim() !== '')
    .map((s) => Number(s) * 1000);

  const links = extrairLinks(listarEntradas());
  if (!links.size) {
    console.error('::error::Nenhum link do Google Drive ou Docs encontrado. A extração quebrou?');
    process.exit(1);
  }
  console.log(`Conferindo ${links.size} links do Google Drive e Docs…`);
  const resultados = await checar(links, { intervaloMs, pausasMs });
  const { texto, quebrados, naoConferidos } = montarRelatorio(links, resultados, pausasMs);

  console.log(`\n${texto}`);
  if (saida) {
    mkdirSync(dirname(saida), { recursive: true });
    writeFileSync(saida, texto);
  }
  if (process.env.GITHUB_OUTPUT) {
    appendFileSync(process.env.GITHUB_OUTPUT, `quebrados=${quebrados}\nnao_conferidos=${naoConferidos}\n`);
  }
  if (process.env.GITHUB_STEP_SUMMARY) appendFileSync(process.env.GITHUB_STEP_SUMMARY, texto);

  // Com mais da metade recusada, a checagem não aconteceu de fato: o job falha (e o GitHub avisa
  // por e-mail) em vez de parecer que está tudo bem.
  if (naoConferidos > links.size / 2) {
    console.error(`::error::O Google recusou ${naoConferidos} de ${links.size} links. Rode mais tarde.`);
    process.exit(1);
  }
  if (naoConferidos) {
    console.log(`::warning::${naoConferidos} link(s) do Drive ficaram sem conferir (pedido recusado).`);
  }
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) await principal();
