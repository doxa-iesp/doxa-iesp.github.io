# Checkpoint: Limpeza e verificação final
Status: concluído
Última atualização: 2026-07-10

## O que foi feito

Rodei o site de verdade (não só o build) e apaguei o que era inútil.

### Verificação em execução — 14 rotas, com navegador

Servidor `astro preview` + Playwright em **todas** as 14 rotas:

- **0 erros de JavaScript**
- **0 respostas HTTP ≥ 400** (nenhum link ou asset quebrado)
- **0 links internos quebrados** (15 links distintos, todos resolvem)
- **0 rolagem horizontal** em 360 px de largura, em nenhuma página
- Varredura do HTML publicado por notas internas e placeholders: **0 achados**

*Falso positivo registrado:* o teste acusou 12 "imagens quebradas". São imagens com
`loading="lazy"` abaixo da dobra. Confirmado por requisição direta (HTTP 200) e recontagem após
rolar a página até o fim: **0 quebradas**.

## Correções aplicadas

1. **`robots.txt` apontava para um sitemap inexistente.** Herdado do Hugo, indicava
   `sitemap.xml`; o Astro gera `sitemap-index.xml`.

2. **Nota interna de um agente estava publicada no site.** O card "Mapas Eleitorais" em
   `/bancos-de-dados/` exibia, ao visitante: *"Listagem completa em pagina externa (nao extraida
   nesta tarefa)"*. Substituída pela cobertura real (273 mapas, eleições de 1998 a 2014, cargos
   majoritários e proporcionais), verificada contra o CSV. Os textos de `cobertura` também estavam
   sem acentuação — reescritos.

3. **Conteúdo duplicado em `/bancos-de-dados/` e `/publicacoes/`.** A prosa da página repetia,
   palavra por palavra, os cards gerados a partir dos dados. E **todas** as páginas abriam com um
   `<h2>` que repetia o próprio `<h1>` (era o banner de título do WordPress). Corrigido no
   conversor, com regra explícita por página.

4. **Os três botões "Acessar o banco" apontavam para o WordPress antigo**, que vai ser desligado.
   Agora: Mapas Eleitorais leva à nossa própria página; os três bancos ganharam
   **"Baixar os dados (CSV)"** (servidos de `public/dados/`); a página original virou link
   secundário. Schema estendido com `pagina` e `download`.

## Removido do repositório

| O quê | Por quê |
|---|---|
| `legacy-hugo/` (2,0 MB, 71 arquivos) | site Hugo antigo. Recuperável: `git checkout 073679b -- layouts/ data/ content/ static/` |
| `icon/` | duplicata exata (mesmo md5) de `public/img/logo-doxa.svg` |
| `resources/` | cache do Hugo, vazio |
| `.hugo_build.lock` | lock do Hugo |
| `CNAME` (raiz) | nunca foi publicado — só `public/` entra no build. Instruções de migração no resumo executivo |
| `public/img/bg-grid-tile.svg` | asset órfão, nada o referencia |

Referências pendentes a esses caminhos foram atualizadas em `README.md`, `CLAUDE.md`,
`tsconfig.json`, `docs/RESUMO_EXECUTIVO.md` e `scripts/converter-conteudo.py`.
O `.gitignore` perdeu as entradas do Hugo e ganhou um filtro para os arquivos-cópia do iCloud
(`* 2.*`), que duplicariam entradas no build sem avisar.

## Decisões tomadas

- **`extracao/` foi mantida** (8,8 MB). Não é lixo: é a fonte de verdade dos dados e o registro de
  proveniência, com os parsers reproduzíveis.
- **Os CSVs passaram a ser publicados** em `public/dados/` (360 KB). O site deixa de depender do
  WordPress antigo para entregar os dados.
- **`DADOS_PENDENTES.md` na raiz**, não em `docs/` — é o arquivo que o time do DOXA mais vai abrir.

## Pendências / bloqueios

- Nenhuma pendência de código. As 14 pendências de **dados** estão em `DADOS_PENDENTES.md`.
- Falta ativar o GitHub Pages (Settings → Pages → Source: GitHub Actions) e dar `push`.

## Próximo passo sugerido

`git push` e conferir o site publicado. Depois, `DADOS_PENDENTES.md`.
