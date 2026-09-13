/**
 * /arquivos-antigos.json — nome de arquivo do WordPress → endereço atual.
 *
 * A página 404 consulta esta tabela quando alguém chega por um link antigo de
 * /wp-content/uploads/… (um PDF citado num artigo, por exemplo). Só é baixada nesse
 * caso, para não pesar nas outras 404. Gerada no build a partir de:
 *
 *   - public/pdfs/: os PDFs trazidos para o site em 2026-09-03 mantiveram o nome que
 *     tinham no WordPress (conferido: 55 de 55);
 *   - extracao/dados/mapas-no-drive.csv: os 273 mapas de votação, hoje no Google Drive;
 *   - RENOMEADOS, abaixo: os poucos arquivos que mudaram de nome ao vir para cá.
 *
 * As chaves ficam em minúsculas; a 404 procura o nome também em minúsculas.
 */
import { readdirSync, readFileSync, existsSync } from 'node:fs';
import { join, relative, sep } from 'node:path';
import { url } from '../lib/url';

const RAIZ = process.cwd();

/** Arquivos que chegaram aqui com outro nome. */
const RENOMEADOS: Record<string, string> = {
  'cartaz_seminario-marcus-figueiredo.jpg.pdf': '/pdfs/eventos/cartaz-seminario-marcus-figueiredo.pdf',
};

function listarPdfs(pasta: string): string[] {
  if (!existsSync(pasta)) return [];
  return readdirSync(pasta, { withFileTypes: true }).flatMap((e) => {
    const caminho = join(pasta, e.name);
    if (e.isDirectory()) return listarPdfs(caminho);
    return e.name.toLowerCase().endsWith('.pdf') ? [caminho] : [];
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

  const pastaPdfs = join(RAIZ, 'public', 'pdfs');
  for (const arquivo of listarPdfs(pastaPdfs)) {
    const rel = relative(join(RAIZ, 'public'), arquivo).split(sep).join('/');
    const nome = rel.split('/').pop()!.toLowerCase();
    tabela[nome] ??= url(`/${rel}`);
  }

  for (const { arquivo, novo } of lerCsv(join(RAIZ, 'extracao', 'dados', 'mapas-no-drive.csv'))) {
    if (arquivo && novo) tabela[arquivo.toLowerCase()] = novo;
  }

  for (const [nome, destino] of Object.entries(RENOMEADOS)) tabela[nome] = url(destino);

  return new Response(JSON.stringify(tabela), {
    headers: { 'Content-Type': 'application/json; charset=utf-8' },
  });
}
