/**
 * /arquivos-antigos.json — nome de arquivo do WordPress → endereço atual.
 *
 * A página 404 consulta esta tabela quando alguém chega por um link antigo de
 * /wp-content/uploads/… (um PDF citado num artigo, por exemplo). Só é baixada nesse
 * caso, para não pesar nas outras 404. Gerada no build a partir de:
 *
 *   - public/pdfs/ e public/dados/: os arquivos trazidos do WordPress mantiveram o nome que
 *     tinham lá (os PDFs de 2026-09-03 e os downloads da Pesquisa COVID, PDF e XLSX);
 *   - extracao/dados/mapas-no-drive.csv: os 273 mapas de votação, hoje no Google Drive;
 *   - RENOMEADOS, abaixo: os arquivos que mudaram de nome ou de lugar ao vir para cá.
 *
 * As chaves ficam em minúsculas; a 404 procura o nome também em minúsculas. Quem acrescentar
 * uma entrada em RENOMEADOS precisa escrever a chave em minúsculas, senão ela nunca casa.
 */
import { readdirSync, readFileSync, existsSync } from 'node:fs';
import { join, relative, sep } from 'node:path';
import { linkPara, url } from '../lib/url';

const RAIZ = process.cwd();

/** Extensões dos arquivos do WordPress que podem ter vindo para `public/`. */
const EXTENSOES = /\.(pdf|xlsx|docx)$/i;

/**
 * Arquivos que chegaram aqui com outro nome, ou que hoje vivem fora do site. Chave em
 * minúsculas; destino é um caminho do site ou um link externo.
 */
const RENOMEADOS: Record<string, string> = {
  'cartaz_seminario-marcus-figueiredo.jpg.pdf': '/pdfs/eventos/cartaz-seminario-marcus-figueiredo.pdf',
  'solicitacao-de-material-do-acervo.docx': '/docs/solicitacao-de-material-do-acervo.docx',
  // Pesquisa COVID: o WordPress guardava versões anteriores com outro nome, e os endereços
  // antigos que circulam são os delas (extracao/dados/enderecos-antigos.txt). Levam à versão
  // que a página linkava por último.
  '3.1.-biblio_-introducao.pdf': '/pdfs/projetos/pesquisa-covid/3.1.-BIBLIO_-Introducao_v2.pdf',
  'survey_opinioes-comportamento.pdf': '/pdfs/projetos/pesquisa-covid/SURVEY_OPINIOES-COMPORTAMENTO-1.pdf',
  // O relatório de 2023 é o mesmo texto do de 2022, com uma nota interna na primeira linha.
  'pandemia-e-mercado-de-trabalho.pdf': '/pdfs/projetos/pesquisa-covid/Pandemia-e-mercado-de-trabalho-no-Rio-de-Janeiro.pdf',
  // O capítulo saiu em livro de acesso aberto; o link vai para lá em vez de hospedar a cópia.
  'figueiredo_guicheney_lazzari.pdf': 'https://books.scielo.org/id/vpjzm',
  'figueiredo_guicheney_lazzari_revisto_ed.pdf': 'https://books.scielo.org/id/vpjzm',
};

function listarArquivos(pasta: string): string[] {
  if (!existsSync(pasta)) return [];
  return readdirSync(pasta, { withFileTypes: true }).flatMap((e) => {
    const caminho = join(pasta, e.name);
    if (e.isDirectory()) return listarArquivos(caminho);
    return EXTENSOES.test(e.name) ? [caminho] : [];
  });
}

/** Leitura mínima de CSV, suficiente para mapas-no-drive.csv (nenhum campo tem vírgula). */
function lerCsv(caminho: string): Record<string, string>[] {
  if (!existsSync(caminho)) return [];
  const [cabecalho, ...linhas] = readFileSync(caminho, 'utf8').trim().split(/\r?\n/);
  const campos = cabecalho.split(',');
  return linhas.map((linha) => {
    const valores = linha.split(',');
    return Object.fromEntries(campos.map((c, i) => [c, valores[i] ?? '']));
  });
}

export function GET() {
  const tabela: Record<string, string> = {};

  for (const pasta of ['pdfs', 'dados']) {
    for (const arquivo of listarArquivos(join(RAIZ, 'public', pasta))) {
      const rel = relative(join(RAIZ, 'public'), arquivo).split(sep).join('/');
      const nome = rel.split('/').pop()!.toLowerCase();
      tabela[nome] ??= url(`/${rel}`);
    }
  }

  for (const { arquivo, novo } of lerCsv(join(RAIZ, 'extracao', 'dados', 'mapas-no-drive.csv'))) {
    if (arquivo && novo) tabela[arquivo.toLowerCase()] = novo;
  }

  for (const [nome, destino] of Object.entries(RENOMEADOS)) tabela[nome] = linkPara(destino);

  return new Response(JSON.stringify(tabela), {
    headers: { 'Content-Type': 'application/json; charset=utf-8' },
  });
}
