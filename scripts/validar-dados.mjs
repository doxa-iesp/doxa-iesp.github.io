#!/usr/bin/env node
/**
 * Validação dos arquivos de conteúdo ANTES do build do Astro.
 *
 * POR QUE ISTO EXISTE
 * -------------------
 * O loader `file()` do Astro engole exceções do parser: se um `src/data/*.yaml` estiver com a
 * indentação quebrada, ele imprime `[ERROR] [file-loader] Error reading data ...`, **sai com
 * código 0** e publica a página com a coleção VAZIA. Num build frio (que é o do CI), as 70
 * matérias de "Na Mídia" simplesmente somem do site, e o PR fica verde.
 *
 * Reproduzido em 2026-07-10:
 *   rm -rf dist .astro node_modules/.astro && npx astro build   # exit 0, página com 0 itens
 *
 * Este script fecha esse buraco: ele lê cada arquivo de conteúdo, falha com código 1 e
 * aponta arquivo e linha. Roda antes do `astro build` (ver package.json).
 *
 * Os arquivos carregados via `glob()` (equipe, eventos, páginas) JÁ quebram o build sozinhos,
 * mas são validados aqui também para dar a mensagem melhor.
 */
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import YAML from 'yaml';

const RAIZ = new URL('..', import.meta.url).pathname;
const erros = [];

const vermelho = (s) => `\x1b[31m${s}\x1b[0m`;
const amarelo = (s) => `\x1b[33m${s}\x1b[0m`;
const verde = (s) => `\x1b[32m${s}\x1b[0m`;

/** Listas: `src/data/<nome>.yaml` precisa ser uma lista não-vazia de objetos. */
const LISTAS = {
  'publicacoes.yaml': 30,
  'analises.yaml': 20,
  'textos-discussao.yaml': 1,
  'midia.yaml': 60,
  'seminarios.yaml': 30,
  'pesquisas.yaml': 50,
  'acervo.yaml': 90,
  'bancos-de-dados.yaml': 3,
  'mapas-votacao.yaml': 200,
  'parceiros.yaml': 5,
};

/** Pastas carregadas por glob(): um arquivo = uma entrada. */
const PASTAS = [
  { dir: 'src/content/equipe', ext: '.yaml', minimo: 10 },
  { dir: 'src/content/destaques', ext: '.md', minimo: 1 },
  { dir: 'src/content/eventos', ext: '.md', minimo: 3 },
  { dir: 'src/content/projetos', ext: '.md', minimo: 4 },
  { dir: 'src/content/paginas', ext: '.md', minimo: 8 },
];

function parseOuErro(caminho, texto) {
  try {
    return YAML.parse(texto);
  } catch (e) {
    const pos = e.linePos?.[0];
    const onde = pos ? ` (linha ${pos.line}, coluna ${pos.col})` : '';
    erros.push(
      `${caminho}${onde}\n    ${e.message.split('\n')[0]}\n    ` +
        amarelo('Dica: em YAML, todos os campos de um item precisam começar na mesma coluna.')
    );
    return undefined;
  }
}

// ---------------------------------------------------------------- listas
for (const [arquivo, minimo] of Object.entries(LISTAS)) {
  const caminho = join(RAIZ, 'src/data', arquivo);
  if (!existsSync(caminho)) {
    erros.push(`${caminho}\n    Arquivo não encontrado.`);
    continue;
  }
  const dados = parseOuErro(`src/data/${arquivo}`, readFileSync(caminho, 'utf8'));
  if (dados === undefined) continue;

  if (!Array.isArray(dados)) {
    erros.push(
      `src/data/${arquivo}\n    Deveria ser uma LISTA (cada item começa com "- "), ` +
        `mas veio um ${typeof dados}.`
    );
    continue;
  }
  if (dados.length < minimo) {
    erros.push(
      `src/data/${arquivo}\n    Só ${dados.length} itens, esperados pelo menos ${minimo}. ` +
        `Algum item foi apagado por engano?`
    );
    continue;
  }
  dados.forEach((item, i) => {
    if (item === null || typeof item !== 'object' || Array.isArray(item)) {
      erros.push(`src/data/${arquivo}\n    Item nº ${i + 1} não é um objeto com campos.`);
    }
  });
}

// ---------------------------------------------------------------- site.yaml
const siteCaminho = join(RAIZ, 'src/data/site.yaml');
const site = parseOuErro('src/data/site.yaml', readFileSync(siteCaminho, 'utf8'));
if (site !== undefined && (!site || typeof site !== 'object' || !site.geral)) {
  erros.push('src/data/site.yaml\n    Precisa ter uma chave de topo `geral:` com os dados do site.');
}

// ---------------------------------------------------------------- pastas (glob)
for (const { dir, ext, minimo } of PASTAS) {
  const caminho = join(RAIZ, dir);
  if (!existsSync(caminho)) {
    erros.push(`${dir}\n    Pasta não encontrada.`);
    continue;
  }
  const arquivos = readdirSync(caminho).filter((f) => f.endsWith(ext));

  // Cópias que o iCloud cria ao sincronizar ("nome 2.yaml", "nome 3.md"). As coleções
  // usam glob('**/*'), que não distingue cópia de original: cada uma vira uma ENTRADA A
  // MAIS. Em 2026-09-07 havia 142 delas e /institucional/ renderizava 80 cards de equipe
  // em vez de 16 — build verde, página errada. O .gitignore impede que sejam commitadas,
  // mas não impede o build LOCAL de lê-las; só uma checagem aqui pega isso.
  const copias = arquivos.filter((f) => / \d+\.[A-Za-z0-9]+$/.test(f));
  if (copias.length) {
    const amostra = copias.slice(0, 5).join('\n      ');
    const resto = copias.length > 5 ? `\n      ...e mais ${copias.length - 5}.` : '';
    erros.push(
      `${dir}\n    ${copias.length} cópia(s) de sincronização, que virariam itens repetidos ` +
        `no site:\n      ${amostra}${resto}\n    ` +
        amarelo('Apague esses arquivos. São cópias que o iCloud criou; o original, sem o número no fim, fica.')
    );
  }
  if (arquivos.length < minimo) {
    erros.push(`${dir}\n    Só ${arquivos.length} arquivos, esperados pelo menos ${minimo}.`);
  }
  for (const f of arquivos) {
    const texto = readFileSync(join(caminho, f), 'utf8');
    if (ext === '.yaml') {
      parseOuErro(`${dir}/${f}`, texto);
    } else {
      const m = texto.match(/^---\n([\s\S]*?)\n---/);
      if (!m) {
        erros.push(`${dir}/${f}\n    Falta o bloco de frontmatter entre duas linhas de "---".`);
      } else {
        parseOuErro(`${dir}/${f} (frontmatter)`, m[1]);
      }
    }
  }
}

// ---------------------------------------------------------------- resultado
if (erros.length) {
  console.error(`\n${vermelho('✖ Erro no conteúdo do site.')} O build foi interrompido.\n`);
  console.error('Corrija o(s) arquivo(s) abaixo e envie de novo:\n');
  for (const e of erros) console.error(`  ${vermelho('•')} ${e}\n`);
  console.error(
    amarelo('Nada foi publicado. O site continua no ar com a versão anterior.\n') +
      'Se não souber o que fazer, peça ajuda a quem cuida do site.\n'
  );
  process.exit(1);
}

console.log(verde('✔ Conteúdo validado:') + ' listas, páginas, equipe e eventos estão íntegros.');
