/**
 * Schemas do conteúdo do site (contrato entre conteúdo e código).
 *
 * ⚠️ ESTAGIÁRIOS NÃO PRECISAM MEXER NESTE ARQUIVO.
 * Ele existe para que um erro de digitação num arquivo de conteúdo QUEBRE O BUILD com uma
 * mensagem clara, em vez de publicar uma página faltando conteúdo em silêncio.
 *
 * Regra ao editar schemas: campo que pode faltar de verdade nos dados do DOXA deve ser
 * `.optional()`. Ver checkpoints/00-auditoria-conteudo.md para a lista de lacunas reais
 * (seminários sem descrição/link, equipe sem Lattes/e-mail, pesquisas sem URL). O retrato atual
 * das lacunas está em DADOS_PENDENTES.md.
 */
import { defineCollection } from 'astro:content';
// `astro/zod`, não `astro:schema`: o alias `astro:schema` é obsoleto e sai numa próxima versão.
import { z } from 'astro/zod';
import { file, glob } from 'astro/loaders';
import YAML from 'yaml';

/** Converte "Título Com Acentos!" em "titulo-com-acentos". */
function slug(texto: string): string {
  return texto
    .normalize('NFKD')
    .replace(/[̀-ͯ]/g, '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '')
    .slice(0, 48);
}

/**
 * Carrega um YAML que contém uma LISTA de itens.
 *
 * O loader `file()` do Astro exige que cada item tenha um campo `id`. Escrever `id:` à mão em
 * cada publicação seria fricção pura para quem edita, então geramos o id a partir do título.
 * O id só aparece em mensagens de erro do build — não vira URL.
 */
function listaYaml(caminho: string, campoTitulo = 'titulo') {
  return file(caminho, {
    parser: (texto: string) => {
      const itens = YAML.parse(texto) ?? [];
      if (!Array.isArray(itens)) {
        throw new Error(`${caminho} deveria conter uma lista (itens começando com "- ").`);
      }
      // O id começa pela POSIÇÃO do item no arquivo ("0007-hgpe-eleicoes-1989"). Duas razões:
      //  1. O Astro guarda e devolve toda coleção ORDENADA PELO ID (data store), não na ordem
      //     do arquivo. Com o título puro, as análises de um ciclo e as publicações do mesmo
      //     ano saíam em ordem alfabética, diferente do site antigo. Com a posição na frente,
      //     a ordem alfabética do id É a ordem do arquivo.
      //  2. Fica único por construção (o mesmo seminário apresentado duas vezes não colide), e
      //     a mensagem de erro do build diz o número do item.
      // As páginas ainda desempatam por `id` explicitamente, para não depender só disto.
      const saida: Record<string, Record<string, unknown>> = {};
      itens.forEach((item: Record<string, unknown>, i: number) => {
        const nome = slug(String(item?.[campoTitulo] ?? 'item'));
        saida[`${String(i + 1).padStart(4, '0')}-${nome}`] = item;
      });
      return saida;
    },
  });
}

/**
 * Endereço web (http ou https) ou vazio. `z.httpUrl()`, e não o antigo `z.string().url()` (obsoleto
 * no zod 4), que aceitava qualquer esquema — `javascript:alert(1)` passava num campo de link.
 */
const urlOuVazio = z.union([z.httpUrl(), z.literal('')]).optional();

/**
 * Como `urlOuVazio`, mas também aceita um caminho interno do site (começa com "/") — para campos
 * de `url` que podem apontar tanto para fora quanto para um PDF local em `public/pdfs/` (ver
 * DADOS_PENDENTES.md, item 0). `z.httpUrl()` sozinho rejeita caminhos relativos.
 */
const linkOuVazio = z.union([z.httpUrl(), z.string().startsWith('/'), z.literal('')]).optional();

// ---------------------------------------------------------------- páginas e equipe

const paginas = defineCollection({
  loader: glob({ base: 'src/content/paginas', pattern: '**/*.md' }),
  schema: z.object({
    titulo: z.string(),
    subtitulo: z.string().optional(),
    descricao: z.string().optional(),
  }),
});

const CATEGORIAS = [
  'coordenacao',
  'pesquisadores',
  'pos-doutorando',
  'aluno',
  'assistente',
  'associado',
] as const;

const equipe = defineCollection({
  loader: glob({ base: 'src/content/equipe', pattern: '**/*.yaml' }),
  schema: z.object({
    nome: z.string(),
    cargo: z.string(),
    categoria: z.enum(CATEGORIAS),
    foto: z.string().optional(),
    lattes: urlOuVazio, // o site antigo não publica Lattes; coleta manual pendente
    site: urlOuVazio, // página pessoal, quando a pessoa tiver
    email: z.email().optional().or(z.literal('')),
    ordem: z.number().optional(),
  }),
});

/**
 * Projetos do laboratório — as iniciativas com entrega pública (Vota Aí, os
 * dashboards, a Pesquisa COVID, a Geografia do Voto). Antes viviam espalhadas
 * pela home e dentro de `site.yaml`.
 *
 * Um arquivo por projeto: o nome do arquivo vira a URL (`vota-ai.md` →
 * `/projetos/vota-ai/`) e o corpo do markdown é a descrição longa.
 */
const projetos = defineCollection({
  loader: glob({ base: 'src/content/projetos', pattern: '**/*.md' }),
  schema: z.object({
    titulo: z.string(),
    resumo: z.string(), // 1–2 frases: é o que aparece no card
    periodo: z.string().optional(),
    // opcional de propósito: só preencher com evidência, nunca por suposição
    status: z.enum(['ativo', 'concluido']).optional(),
    imagem: z.string().optional(),
    url: urlOuVazio, // site externo do projeto
    rotulo_url: z.string().optional(),
    embed: urlOuVazio, // iframe (Power BI, YouTube)
    links: z.array(z.object({ rotulo: z.string(), url: z.string() })).default([]),
    ordem: z.number().optional(),
  }),
});

/**
 * Destaques da home — a vitrine curada pela coordenação.
 *
 * Um arquivo por destaque, como em `projetos`. É a única coleção que nasceu depois
 * da migração, sem equivalente em `extracao/` (que hoje é só registro histórico:
 * todo o conteúdo se edita em `src/`). Para tirar um destaque do ar sem perder o
 * texto, basta `ativo: false`.
 *
 * Receita para estagiários: docs/GUIA_DE_MANUTENCAO.md, seção 4.12.
 */
const destaques = defineCollection({
  loader: glob({ base: 'src/content/destaques', pattern: '**/*.md' }),
  schema: z.object({
    titulo: z.string(),
    resumo: z.string(), // 1–2 frases: é o que aparece no card
    etiqueta: z.string().optional(), // "Livro", "Evento", "Documentário"…
    imagem: z.string().optional(),
    url: linkOuVazio, // link externo OU um arquivo local em public/
    rotulo_url: z.string().optional(), // texto do botão; sem isto, o botão diz "Acessar" (sem `url`, não há botão)
    ordem: z.number().optional(),
    ativo: z.boolean().default(true),
  }),
});

const eventos = defineCollection({
  loader: glob({ base: 'src/content/eventos', pattern: '**/*.md' }),
  schema: z.object({
    titulo: z.string(),
    data: z.coerce.date(),
    descricao: z.string().optional(),
    imagem: z.string().optional(),
    url: urlOuVazio,
    anexos: z.array(z.string()).optional(),
  }),
});

// ---------------------------------------------------------------- listas bibliográficas

const publicacoes = defineCollection({
  loader: listaYaml('src/data/publicacoes.yaml'),
  schema: z.object({
    titulo: z.string(),
    autores: z.string(),
    ano: z.number().int().min(1990).max(2100).optional(), // opcional para um item "no prelo" ainda sem ano
    tipo: z.enum(['livro', 'capitulo', 'artigo', 'outros']),
    editora: z.string().optional(),
    revista: z.string().optional(),
    paginas: z.string().optional(),
    url: urlOuVazio,
  }),
});

const analises = defineCollection({
  loader: listaYaml('src/data/analises.yaml'),
  schema: z.object({
    titulo: z.string(),
    ciclo: z.string(),
    periodo: z.string().optional(),
    descricao: z.string().optional(),
    arquivos: z.array(z.object({ rotulo: z.string(), url: z.string() })).default([]),
  }),
});

const textosDiscussao = defineCollection({
  loader: listaYaml('src/data/textos-discussao.yaml'),
  schema: z.object({
    titulo: z.string(),
    autores: z.string(),
    ano: z.number().int(),
    url: linkOuVazio, // pode ser externo ou um PDF local em public/pdfs/
    resumo: z.string().optional(),
  }),
});

const midia = defineCollection({
  loader: listaYaml('src/data/midia.yaml'),
  schema: z.object({
    titulo: z.string(),
    autores: z.string().optional(),
    veiculo: z.string().optional(),
    data: z.string().optional(), // "2022-04-24" ou só "2010"
    tipo: z.enum(['impressa', 'virtual', 'audiovisual']),
    url: linkOuVazio, // pode ser externo ou um PDF local em public/pdfs/ (ver DADOS_PENDENTES.md)
  }),
});

const seminarios = defineCollection({
  loader: listaYaml('src/data/seminarios.yaml'),
  schema: z.object({
    titulo: z.string(),
    apresentador: z.string(),
    instituicao: z.string().optional(),
    data: z.string().optional(),
    ano: z.number().int(),
    // a página antiga não traz descrição, link nem vídeo — mantidos opcionais de propósito
    descricao: z.string().optional(),
    url: urlOuVazio,
  }),
});

const pesquisas = defineCollection({
  loader: listaYaml('src/data/pesquisas.yaml'),
  schema: z.object({
    titulo: z.string(),
    autor: z.string().optional(), // 4 pesquisas concluídas não têm autor único
    ano: z.number().int().optional(),
    orientador: z.string().optional(),
    instituicao: z.string().optional(),
    status: z.enum(['tese', 'andamento', 'concluida']),
    url: linkOuVazio, // pode ser externo ou um PDF local em public/pdfs/; metade das pesquisas não tem link
    descricao: z.string().optional(),
  }),
});

const acervo = defineCollection({
  loader: listaYaml('src/data/acervo.yaml', 'codigo'),
  schema: z.object({
    codigo: z.string(),
    data: z.string().optional(),
    ano: z.number().int(),
    tipo_video: z.string().optional(),
    cargo: z.array(z.string()).default([]),
    regiao: z.string().optional(),
    estado: z.string().optional(),
    candidatos: z.array(z.string()).default([]),
    partidos: z.array(z.string()).default([]),
    url: z.httpUrl(),
    thumb: z.string().optional(),
  }),
});

/**
 * Bancos de dados abertos (`/bancos-de-dados/`). Cada banco pode ter vários arquivos para
 * baixar — CSV, XLSX, PDF de documentação —, cada um com o próprio rótulo, no mesmo formato de
 * `analises.arquivos`. Até 2026-09-13 havia um campo `download` único, com o botão fixo em
 * "Baixar os dados (CSV)", que não servia para os bancos da Pesquisa COVID (XLSX, vários arquivos).
 *
 * O schema é `.strict()`: um `download:` antigo ou um nome de campo digitado errado quebra o build
 * em vez de ser descartado em silêncio — o que faria o botão sumir com o build verde.
 */
const bancosDeDados = defineCollection({
  loader: listaYaml('src/data/bancos-de-dados.yaml', 'nome'),
  schema: z
    .object({
      nome: z.string(),
      descricao: z.string(),
      cobertura: z.string().optional(),
      registros: z.number().int().optional(),
      url: urlOuVazio, // página externa do banco, se houver (a do site antigo foi retirada: o WordPress saiu do ar)
      pagina: z.string().optional(), // rota interna, ex.: "/mapas-de-votacao/"
      rotulo_pagina: z.string().optional(), // texto do botão da `pagina`; sem isto, "Ver no site"
      arquivos: z.array(z.object({ rotulo: z.string(), url: z.string() })).default([]), // em public/dados/ ou public/pdfs/
      aviso: z.string().optional(),
      // Posição na página (menor aparece antes). Sem isto, vale a ordem do arquivo.
      ordem: z.number().optional(),
    })
    .strict(),
});

const mapas = defineCollection({
  loader: listaYaml('src/data/mapas-votacao.yaml'),
  schema: z.object({
    // nas eleições majoritárias não há sigla partidária: o título é o próprio cargo
    titulo: z.string(),
    ano: z.number().int().optional(),
    cargo: z.string().optional(),
    eleicao: z.enum(['Majoritaria', 'Proporcional']).optional(),
    turno: z.string().optional(),
    url: z.httpUrl(),
  }),
});

const parceiros = defineCollection({
  loader: listaYaml('src/data/parceiros.yaml', 'nome'),
  schema: z.object({
    nome: z.string(),
    arquivo: z.string(),
    url: urlOuVazio,
  }),
});

/**
 * `src/data/site.yaml` tem UMA entrada de topo, `geral`, com todos os dados do site.
 * O schema é `.strict()`: uma chave digitada errado (`emial:`) quebra o build em vez de ser
 * ignorada em silêncio.
 */
const configuracao = defineCollection({
  loader: file('src/data/site.yaml'),
  schema: z
    .object({
      titulo: z.string(),
      descricao: z.string(),
      email: z.email(),
      endereco: z.string(),
      cep: z.string(),
      youtube: urlOuVazio,
      instagram: urlOuVazio,
      twitter: urlOuVazio,
      // O vídeo dos "melhores momentos" é conteúdo do acervo, e é lá que ele aparece.
      video_destaque: z.string(),
      // Documentário "Arquitetos do Poder" (coordenação de Marcus Figueiredo).
      video_documentario: z.string(),
      catalogo_acervo: z.httpUrl(),
      formulario_acervo: z.string(),
      // Vota Aí e o dashboard das eleições viraram projetos (src/content/projetos/).
    })
    .strict(),
});

export const collections = {
  paginas,
  equipe,
  destaques,
  projetos,
  eventos,
  publicacoes,
  analises,
  'textos-discussao': textosDiscussao,
  midia,
  seminarios,
  pesquisas,
  acervo,
  'bancos-de-dados': bancosDeDados,
  mapas,
  parceiros,
  configuracao,
};
