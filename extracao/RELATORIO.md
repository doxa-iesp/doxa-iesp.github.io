# Relatório: extração × `data/` do site Hugo

Comparação entre o que foi extraído do WordPress (`extracao/dados/`) e o que o site Hugo já
carrega em `data/`. **Nada em `data/` foi alterado.**

## Placar

| `data/` (Hugo) | hoje | extraído | situação |
|---|---:|---:|---|
| `acervo.yaml` | 6 | **95** | 🔴 os 6 atuais são placeholders (`Candidato Exemplo 1..6`) |
| `pesquisas.yaml` | 6 | **61** | 🔴 faltam 55 (38 teses, 13 em andamento, 10 concluídas) |
| `homepage.yaml` | — | — | 🔴 3 placeholders substituíveis (abaixo) |
| `analyses.yaml` | 25 | 28 | 🟡 3 análises novas |
| `publications.yaml` | 32 | 34 | 🟡 2 publicações novas + 4 links Lattes |
| `events.yaml` | 4 | 5 | 🟡 1 evento novo (nota editorial, 2014) |
| `team.yaml` | 16 | 15 | 🟢 ok — o 16º é Felipe Lamarca, que não está no site antigo |
| `media.yaml` | 70 | 70 | 🟢 bate |
| `seminars.yaml` | 36 | 36 | 🟢 bate |
| `discussions.yaml` | 2 | 2 | 🟢 bate |

Além disso, quatro conjuntos **não têm equivalente** hoje em `data/`:
`acervo-catalogo-mestre.csv` (2.034 fitas), `programas-eleitorais-rj.csv` (577),
`programas-eleitorais-capitais.csv` (244) e `mapas-votacao.csv` (273).

---

## Os três placeholders que já têm valor real

O `README.md` da raiz lista estes itens como "dados pendentes de preenchimento". Todos foram
encontrados no DOM renderizado da homepage.

**1. `data/homepage.yaml` → `featured_video.youtube_id`**

```yaml
youtube_id: "SUBSTITUA_PELO_ID_DO_VIDEO"   # hoje
youtube_id: "Ns3jYjf7hx4"                  # real — "Melhores momentos do horário eleitoral"
```

O ID estava no atributo `data-lazy-load` do widget de vídeo do JetEngine — por isso nunca
apareceu numa raspagem de HTML comum.

**2. `data/homepage.yaml` → `dashboards`**

O site tem **um** dashboard, não dois. O `data/homepage.yaml` atual inventa "Dashboard Rio de
Janeiro" e "Dashboard São Paulo", ambos apontando para `https://app.powerbi.com/` (a raiz do
Power BI, que não mostra nada). O real:

```yaml
dashboards:
  title: "Eleições Rio e São Paulo 2024"
  items:
    - label: "Eleições Rio e São Paulo 2024"
      url: "https://app.powerbi.com/view?r=eyJrIjoiNDk3MDhjYjktYWNhMC00Y2JhLTgxNDUtZWQzNDM1MGM0N2YwIiwidCI6Ijc0OTMyMDFlLTdhNDUtNDk3OC1iZWZkLTBlZDAwMmIwZjgyMiJ9"
```

**3. `data/acervo.yaml`** — hoje contém 6 registros falsos (`Candidato Exemplo N`, todos com
`url: "https://www.youtube.com/"`). O real está em `extracao/dados/acervo.yaml`: 95 itens, cada um
com link próprio de Google Drive, ano, cargo, região, partidos e candidatos.

⚠️ **Atenção ao schema.** O `data/acervo.yaml` do Hugo usa
`candidate, party, cargo, region, year, url, thumb` (um candidato por linha). O acervo real é
por **fita**, não por candidato: cada item é um programa (HGPE) com *listas* de candidatos e
partidos. A página `/acervo/` e o `static/js/acervo.js` precisam ser adaptados antes de trocar os
dados — não é um `cp`.

---

## Dados extras que o site Hugo ainda não usa

- **`acervo-catalogo-mestre.csv` (2.034 registros)** — o inventário real do acervo, de 1988 a 2018.
  Os 95 itens publicados em `/acervo/` são só a parte com vídeo no Drive. O catálogo cobre HGPE
  (1.235), telejornais (384), direção nacional de partido (253), entrevistas, debates, spots.
  Também traz o estado de conservação de cada fita (DVD físico, backup, cópia no Drive).
- **Lattes de 4 pesquisadores** (Meireles, Guarnieri, Schaefer, Figueiredo) — em
  `publicacoes-academicas.yaml`, sob a chave `lattes`. Preenchem parte do `data/team.yaml`.
- **Anexos de eventos** — o Google Doc da edição digital gratuita de *A Decisão do Voto*, o PDF de
  homenagem a Marcus Figueiredo e o cartaz do seminário estão em `eventos-seminarios.yaml`
  → `attachments`.
- **Microdados** — dois surveys IESP-BR e o banco de decretos COVID do RJ, em `bruto/datasets/`.

---

## Sugestão de próximos passos

1. Aplicar os três placeholders da homepage (baixo risco, ganho imediato).
2. Substituir `data/pesquisas.yaml` pelos 61 registros — o schema já bate.
3. Fundir os itens novos em `analyses.yaml`, `publications.yaml` e `events.yaml`.
4. Decidir o modelo do acervo (por fita vs. por candidato) **antes** de migrar `acervo.yaml`,
   e decidir se o catálogo mestre de 2.034 fitas vira uma página navegável.
5. Revisar manualmente a coluna `municipio` de `programas-eleitorais-capitais.csv` (ver *Defeitos*
   no `README.md`) antes de publicar essa base.
