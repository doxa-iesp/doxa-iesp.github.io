# Checkpoint: Fase 1 — Decisão de arquitetura
Status: concluído
Última atualização: 2026-07-09

## O que foi feito

- Escrito `docs/DECISAO_ARQUITETURA.md` com o comparativo de 4 stacks (Astro, Hugo, Eleventy, Quarto).
- **Spike empírico antes de decidir**: instalei o Astro (v7.0.7), montei uma content collection
  a partir de um YAML, introduzi um erro de digitação num campo `enum` e rodei o build.
  Resultado: `[InvalidContentEntryDataError] equipe → bruno ... category: Invalid option: expected
  one of "coordenacao"|"pesquisadores"|"aluno"`. Corrigido o typo, o build passa.
  A decisão não se apoia em suposição sobre a API.

## Decisões tomadas

1. **Stack: Astro 7 + TypeScript + CSS puro.** Sem framework de UI, sem Tailwind.
2. **Critério decisivo:** validação de schema com erro de build claro. O Hugo atual falha em
   silêncio — um `category` errado em `data/team.yaml` faz o membro sumir da página sem erro algum.
   Verifiquei isso no template `layouts/institucional/list.html`, que filtra por uma lista literal
   de categorias.
3. **Astro 7, não 5.** A versão instalada é a 7.0.7; a API de loaders (`file()`, `glob()` de
   `astro/loaders`) foi confirmada por inspeção, e `file()` já entende YAML nativamente.
4. **Um arquivo por membro da equipe** (`src/content/equipe/*.yaml`); listas bibliográficas em um
   YAML por coleção.
5. **Montserrat auto-hospedada**, sem Google Fonts.
6. **Sem preview com URL pública.** O job de PR faz build e publica `dist/` como artefato. Um
   preview com URL exigiria Netlify/Cloudflare — outra conta para o laboratório manter.
7. **`base: '/DOXA'`** mantido (deploy atual em `felipelamarca.com/DOXA/`). A troca para
   `www.lab-doxa.org.br` está documentada.

## Pendências / bloqueios

- Nenhum bloqueio. Os schemas precisam tornar **opcionais** os campos das lacunas registradas em
  `checkpoints/00-auditoria-conteudo.md` (seminários sem descrição/link; equipe sem Lattes/e-mail;
  17 pesquisas sem URL), senão a validação reprova dados verdadeiros.

## Próximo passo sugerido

Fase 2. Scaffold do Astro + `src/content.config.ts` (feito pelo orquestrador, pois é o contrato
compartilhado), e depois os Agentes A (conteúdo), B (infra) e C (frontend) em paralelo.
