# Conteúdo Extraído — Site WordPress DOXA (lab-doxa.org.br)

Extração sistemática realizada em 2026-06-01. Fonte: https://www.lab-doxa.org.br  
Destino: site Hugo em `/Users/felipelmc/Desktop/DOXA/`

---

## Homepage (`https://www.lab-doxa.org.br`)

### Identidade e descrição geral

- **Nome completo:** DOXA — Laboratório de Estudos Eleitorais, de Comunicação Política e Opinião Pública
- **Instituição:** Instituto de Estudos Sociais e Políticos (IESP) — Universidade do Estado do Rio de Janeiro (UERJ)
- **Fundação:** 1996 (em Iuperj/Ucam, transferido para IESP/UERJ em 2010)
- **Endereço:** Rua da Matriz, 82, Botafogo, Rio de Janeiro, RJ, 22260-100, Brasil
- **E-mail:** acervo-doxa@iesp.uerj.br
- **YouTube:** https://www.youtube.com/channel/UCkcuDdIEuQ9YqOjHsp4-EHQ

### Texto "Sobre o DOXA" (extraído da homepage e da página institucional)

> "O DOXA é um laboratório de estudos eleitorais, de comunicação política e opinião pública fundado em 1996. Sediado no IESP-UERJ, no Rio de Janeiro, mantém o maior acervo audiovisual de propaganda eleitoral de candidatos ao executivo e legislativo nos níveis nacional e estadual no Brasil, abrangendo programas eleitorais gratuitos, debates, entrevistas com candidatos, spots eleitorais e partidários e telejornais."

### Destaque: Plataforma Vota Aí

```yaml
votaai:
  title: "Vota Aí"
  description: >
    Ferramenta com inteligência artificial para acessar propostas governamentais
    registradas pelos candidatos às prefeituras de todos os municípios brasileiros
    desde 2012. Desenvolvida em parceria com o CESOP/Unicamp. Coordenada por
    Nara Salles e Argelina Figueiredo (DOXA-IESP-UERJ) e Cesop-Unicamp.
  url: "https://votaai.cesop.unicamp.br"
```

### Destaque: Vídeo em destaque (homepage.yaml)

- O vídeo principal da homepage deve ser o vídeo institucional do DOXA no YouTube.
- Canal: https://www.youtube.com/channel/UCkcuDdIEuQ9YqOjHsp4-EHQ
- **Lacuna:** O ID específico do vídeo a ser exibido no hero não foi identificado na página. Ver seção Lacunas.

### Destaque: Dashboards eleições 2024

```yaml
dashboards:
  title: "Análise das Eleições 2024"
  description: "Dashboards interativos com dados das eleições municipais de 2024 para Rio de Janeiro e São Paulo."
  items:
    - label: "Dashboard Rio de Janeiro"
      url: "https://app.powerbi.com/"   # URL real não estava disponível na página — ver Lacunas
    - label: "Dashboard São Paulo"
      url: "https://app.powerbi.com/"   # URL real não estava disponível na página — ver Lacunas
```

### Parceiros / financiadores (logos na homepage)

| Parceiro | Observação |
|----------|-----------|
| CAPES | Agência federal de fomento |
| CNPq | Agência federal de fomento |
| FAPERJ | Agência estadual (Rio de Janeiro) |
| FINEP | Agência federal de inovação |
| IBOPE | Instituto de pesquisa |
| IESP-UERJ | Instituição sede |
| Vox | Empresa parceira |
| UERJ | Universidade |

**Destino dos logos no novo site:** `static/img/parceiros/[nome].png`  
Os logos precisam ser baixados do WordPress: `https://www.lab-doxa.org.br/wp-content/uploads/` (ver seção Assets)

### Links de destaque na homepage

- Pesquisa COVID: https://www.lab-doxa.org.br/pesquisa-covid/
- Acervo Audiovisual: https://www.lab-doxa.org.br/acervo/
- Mapas de Votação: https://www.lab-doxa.org.br/mapas-de-votacao/
- Vota Aí: https://www.votaai.cesop.unicamp.br/

---

## Institucional (`https://www.lab-doxa.org.br/institucional/`)

### Texto institucional completo

> "O DOXA é um Laboratório de Estudos Eleitorais, de Comunicação Política e Opinião Pública estabelecido em 1996 no Iuperj/Ucam para examinar processos eleitorais e a formação da opinião política. O laboratório se transferiu para o IESP/UERJ em 2010. Fundado e inicialmente dirigido por Marcus Figueiredo, tornou-se referência na pesquisa brasileira de comunicação política. Desde 2014, Argelina Cheibub Figueiredo coordena o laboratório. O DOXA mantém um extenso acervo audiovisual que inclui programação eleitoral, telejornais e aparições de candidatos, apoiando pesquisas acadêmicas no Brasil e no exterior."

### Equipe — YAML pronto para `data/team.yaml`

```yaml
# Coordenação
- name: "Argelina Cheibub Figueiredo"
  role: "Coordenadora"
  category: "coordenacao"
  photo: "https://www.lab-doxa.org.br/wp-content/uploads/2022/10/Foto-Argelina_nova.jpg"
  lattes: ""
  email: ""

- name: "Fernando Meireles"
  role: "Coordenação"
  category: "coordenacao"
  photo: "https://www.lab-doxa.org.br/wp-content/uploads/2023/07/Equipe-DOXA-Fernando-Meireles.jpg"
  lattes: ""
  email: ""

# Pesquisadores
- name: "Bruno Schaefer"
  role: "Professor/Pesquisador"
  category: "pesquisadores"
  photo: "https://www.lab-doxa.org.br/wp-content/uploads/2023/07/Equipe-DOXA-Bruno-Schaefer.jpg"
  lattes: ""
  email: ""

- name: "Fernando Guarnieri"
  role: "Professor/Pesquisador"
  category: "pesquisadores"
  photo: "https://www.lab-doxa.org.br/wp-content/uploads/2022/06/Fernando-G.jpg"
  lattes: ""
  email: ""

# Pós-doutorandos
- name: "Flávia Bozza Martins"
  role: "Pós-doutoranda"
  category: "pos-doutorando"
  photo: "https://www.lab-doxa.org.br/wp-content/uploads/2022/06/Flavia.jpg"
  lattes: ""
  email: ""

# Alunos de pós-graduação
- name: "Carolini Silva"
  role: "Doutoranda"
  category: "aluno"
  photo: "https://www.lab-doxa.org.br/wp-content/uploads/2022/06/Carolini-300x225-1.jpg"
  lattes: ""
  email: ""

- name: "Maria Dominguez"
  role: "Doutoranda"
  category: "aluno"
  photo: "https://www.lab-doxa.org.br/wp-content/uploads/2024/09/Maria-Dominguez.jpeg"
  lattes: ""
  email: ""

- name: "Matteo Manes"
  role: "Doutorando"
  category: "aluno"
  photo: "https://www.lab-doxa.org.br/wp-content/uploads/2024/09/Matteo-de-Barros-Manes.jpg"
  lattes: ""
  email: ""

- name: "Karime Lima"
  role: "Doutoranda"
  category: "aluno"
  photo: "https://www.lab-doxa.org.br/wp-content/uploads/2024/09/Karime-Lima.jpeg"
  lattes: ""
  email: ""

# Assistente de pesquisa
- name: "Larissa Mendes"
  role: "Bolsista de Treinamento Técnico"
  category: "assistente"
  photo: "https://www.lab-doxa.org.br/wp-content/uploads/2022/06/Larissa-300x200-1.jpg"
  lattes: ""
  email: ""

# Pesquisadores Associados
- name: "Carolina Botelho"
  role: "Pesquisadora Associada"
  category: "associado"
  photo: "https://www.lab-doxa.org.br/wp-content/uploads/2022/06/Carolina-Botelho.jpg"
  lattes: ""
  email: ""

- name: "Hellen Guicheney"
  role: "Pesquisadora Associada"
  category: "associado"
  photo: "https://www.lab-doxa.org.br/wp-content/uploads/2022/06/Hellen.jpg"
  lattes: ""
  email: ""

- name: "Nara Salles"
  role: "Pesquisadora Associada"
  category: "associado"
  photo: "https://www.lab-doxa.org.br/wp-content/uploads/2022/06/Lattes1.jpg"
  lattes: ""
  email: ""

- name: "Natalia Maciel"
  role: "Pesquisadora Associada"
  category: "associado"
  photo: "https://www.lab-doxa.org.br/wp-content/uploads/2022/06/Natalia.jpg"
  lattes: ""
  email: ""

- name: "Thiago Moreira"
  role: "Pesquisador Associado"
  category: "associado"
  photo: "https://www.lab-doxa.org.br/wp-content/uploads/2022/06/Thiago.jpg"
  lattes: ""
  email: ""
```

**Nota:** Os links de Lattes e e-mails individuais não estavam disponíveis na página WordPress. Devem ser preenchidos manualmente.

---

## Pesquisas (`https://www.lab-doxa.org.br/pagina-pesquisas/`)

O schema atual (`pesquisas.yaml`) usa campos: `title, author, year, advisor, institution, status, url`.  
A página lista apenas teses concluídas supervisionadas por membros do DOXA. Não há listagem de pesquisas em andamento na página.

### YAML pronto para `data/pesquisas.yaml`

```yaml
# Teses concluídas

- title: "Reformas na previdência social brasileira: processo político de reformas politicamente custosas"
  author: "Mariani Ferri de Holanda"
  year: 2023
  advisor: "Argelina Figueiredo"
  institution: "IESP/UERJ"
  status: "tese"
  url: "https://www.bdtd.uerj.br:8443/bitstream/1/19482/2/Tese%20-%20Mariani%20Ferri%20de%20Holanda%20-%202023%20-%20Completa.pdf"

- title: "O papel esquecido do Congresso na trajetória do Bolsa Família: uma nova abordagem sobre a produção de políticas de transferência condicionada de renda"
  author: "Pedro Brás Martins da Costa"
  year: 2022
  advisor: "Argelina Figueiredo"
  institution: "IESP/UERJ"
  status: "tese"
  url: "https://www.bdtd.uerj.br:8443/bitstream/1/17917/2/Tese%20-%20Pedro%20Bras%20Martins%20da%20Costa%20-%202022%20-%20Completa.pdf"

- title: "Relações Executivo-Legislativo na formulação da política orçamentária do Estado de Mato Grosso"
  author: "Ariel Lopes Torres"
  year: 2020
  advisor: "Argelina Figueiredo"
  institution: "IESP/UERJ"
  status: "tese"
  url: "https://www.bdtd.uerj.br:8443/bitstream/1/17266/2/Tese_%20Ariel%20Lopes%20Torres_2020_Completa.pdf"

- title: "Competição eleitoral no Brasil: uma perspectiva programática"
  author: "Nara Oliveira Salles"
  year: 2019
  advisor: "Fernando Guarnieri"
  institution: "IESP/UERJ"
  status: "tese"
  url: "https://www.bdtd.uerj.br:8443/bitstream/1/12386/1/SALLES,%20Nara_Competicao%20eleitoral%20no%20Brasil%20uma%20perspectiva%20programatica%5bFINAL%5d.pdf"

- title: "As modificações do Legislativo nas proposições do Executivo"
  author: "Márcia Rodriguez da Cruz"
  year: 2018
  advisor: "Argelina Figueiredo"
  institution: "IESP/UERJ"
  status: "tese"
  url: "https://www.bdtd.uerj.br:8443/bitstream/1/12486/1/tese%20Marcia%20Cruz.pdf"

- title: "O sistema de comissões permanentes da câmara dos deputados: análise de sua composição e atuação na 54ª legislatura"
  author: "André Corrêa de Sá do Carneiro"
  year: 2018
  advisor: "Argelina Figueiredo"
  institution: "IESP/UERJ"
  status: "tese"
  url: "https://www.bdtd.uerj.br:8443/bitstream/1/12478/1/tese%20Andre%20Carneiro.pdf"
```

---

## Pesquisa COVID (`https://www.lab-doxa.org.br/pesquisa-covid/`)

### Título e descrição

**Título:** "COVID no Estado do Rio de Janeiro: Monitoramento e Efeitos"  
**Financiamento:** FAPERJ — Chamada de Emergência COVID-19/SARS-CoV-2  
**Coordenação:** Argelina Maria Cheibub Figueiredo e Fernando Guarnieri (IESP-UERJ / DOXA)

### Subprojetos

| # | Título | Descrição resumida |
|---|--------|--------------------|
| 01 | Ação Legislativa dos Prefeitos | Análise de 2.751 decretos COVID de 92 municípios fluminenses em 2020 |
| 02 | Surveys de Opinião e Comportamento | Duas ondas (dez/2020 e dez/2021), ~1.000 respondentes cada |
| 03 | Revisão Bibliográfica | 99 textos citando o Brasil, organizados por tema |
| 04 | Trabalho e Pandemia | Vulnerabilidade e flexibilização no mercado de trabalho fluminense |

### Downloads (arquivos para hospedar em `static/files/covid/`)

| Label | URL original | Tipo |
|-------|-------------|------|
| Lista de buscadores legislativos | https://www.lab-doxa.org.br/wp-content/uploads/2022/10/DOWNLOAD-1_LISTA-DE-BUSCADORES_DECRETOS.xlsx | Excel |
| Banco de dados — Decretos COVID RJ | https://www.lab-doxa.org.br/wp-content/uploads/2022/10/DOWNLOAD-2_-BANCO-DE-DADOS_DECRETOS-COVID_RJ_3006.xlsx | Excel |
| Banco de Dados — Survey 1 | https://www.lab-doxa.org.br/wp-content/uploads/2022/10/DADOS_SURVEY_IESPBR_227821_20211208.xlsx | Excel |
| Banco de Dados — Survey 2 | https://www.lab-doxa.org.br/wp-content/uploads/2022/10/DADOS_SURVEY_IESPBR_208324-Wed-Dec-16-2020_total.xlsx | Excel |
| Distribuição de decretos por tema e município | https://www.lab-doxa.org.br/wp-content/uploads/2022/10/DOWNLOAD-3_DISTRIBUICAO-DOS-DECRETOS-POR-TEMA-E-MUNICIPIOS.pdf | PDF |
| Distribuição e média mensal de decretos | https://www.lab-doxa.org.br/wp-content/uploads/2022/10/DOWNLOAD-4_DISTRIBUICAO-E-MEDIA-MENSAL-DE-DECRETOS-DE-RESTRICAO-E-FLEXIBIZACAO-POR-MUNICIPIO.pdf | PDF |
| Distribuição de decretos por partido | https://www.lab-doxa.org.br/wp-content/uploads/2022/10/DOWNLOAD-5_-DISTRIBUICAO-DOS-DECRETOS-POR-TEMA-E-PARTIDO-NO-GOVERNO.pdf | PDF |
| Análise dos surveys | https://www.lab-doxa.org.br/wp-content/uploads/2022/10/SURVEY_OPINIOES-COMPORTAMENTO-1.pdf | PDF |
| Pandemia e mercado de trabalho no RJ | https://www.lab-doxa.org.br/wp-content/uploads/2022/10/Pandemia-e-mercado-de-trabalho-no-Rio-de-Janeiro.pdf | PDF |
| Pandemia e Mercado de Trabalho (versão atualizada) | https://www.lab-doxa.org.br/wp-content/uploads/2023/08/Pandemia-e-Mercado-de-Trabalho.pdf | PDF |
| BIBLIO — Introdução | https://www.lab-doxa.org.br/wp-content/uploads/2022/10/3.1.-BIBLIO_-Introducao_v2.pdf | PDF |
| BIBLIO — Listagem por Tema | https://www.lab-doxa.org.br/wp-content/uploads/2022/10/3.2.BIBLIO_LISTAGEM-POR-TEMA.pdf | PDF |
| BIBLIO — Listagem por Citação Brasil | https://www.lab-doxa.org.br/wp-content/uploads/2022/10/3.3.BIBLIO_LISTAGEM-POR-CITACAO-BRASIL.pdf | PDF |
| BIBLIO — Links Abstracts por Tema | https://www.lab-doxa.org.br/wp-content/uploads/2022/10/3.4.-BIBLIO_LINKS-ABSTRACTS-POR-TEMA.pdf | PDF |
| Impacto da Covid-19 no comportamento eleitoral (artigo) | https://www.lab-doxa.org.br/wp-content/uploads/2022/11/GUARNIERI-FIGUEIREDO.pdf | PDF |
| Vulnerabilidades sociais e mortalidade COVID (artigo) | https://www.lab-doxa.org.br/wp-content/uploads/2022/11/Figueiredo_Guichney_Lazzari_REVISTO_ed.pdf | PDF |

---

## Acervo (`https://www.lab-doxa.org.br/acervo/`)

### Texto descritivo

> "O acervo audiovisual contém vídeos veiculados nos horários gratuitos de propaganda eleitoral (HGPE) de campanhas presidenciais (1989–2022) e gubernatoriais (1994–2014), pesquisáveis por sigla partidária. Além do HGPE, o catálogo inclui debates, entrevistas com candidatos, spots eleitorais e partidários, telejornais e propagandas partidárias."

### Acesso ao acervo

- **Catálogo (Google Sheets):** https://docs.google.com/spreadsheets/d/1b_OFFW0fJS3B0DFvfeoa6y8l9YG6JmFP/edit
- **Formulário de solicitação de material:** https://www.lab-doxa.org.br/wp-content/uploads/2022/11/Solicitacao-de-Material-do-Acervo.docx
- **Canal YouTube:** https://www.youtube.com/channel/UCkcuDdIEuQ9YqOjHsp4-EHQ
- **E-mail de contato:** acervo-doxa@iesp.uerj.br

### Vídeo embed

Não há vídeo do YouTube embutido na página `/acervo/`. Os vídeos são hospedados no Google Drive e acessados via catálogo. O campo `featured_video.youtube_id` em `homepage.yaml` deve apontar para um vídeo institucional do canal DOXA — ver Lacunas.

---

## Mapas de Votação (`https://www.lab-doxa.org.br/mapas-de-votacao/`)

### Texto descritivo

> "Mapas da distribuição do voto para cargos majoritários — Presidente, Governador e Senador — e proporcionais — Deputados Federais e Estaduais — por bairros do Rio de Janeiro, de 1998 a 2014."

### Estrutura dos PDFs (padrão de URL)

Os mapas seguem padrões de URL sistemáticos. Abaixo estão as categorias e os anos disponíveis.

#### Cargos majoritários (por bairro do Rio de Janeiro)

| Cargo | Anos disponíveis | Padrão de URL |
|-------|-----------------|---------------|
| Presidente | 1998, 2002, 2006, 2010, 2014 | `https://www.lab-doxa.org.br/wp-content/uploads/2022/10/p_[ANO].pdf` |
| Governador | 1998, 2002, 2006, 2010, 2014 | `https://www.lab-doxa.org.br/wp-content/uploads/2022/10/g_[ANO].pdf` |
| Senador | 1998, 2002, 2006, 2010, 2014 | `https://www.lab-doxa.org.br/wp-content/uploads/2022/10/s_[ANO].pdf` |

#### Deputados Federais por partido (Município do Rio de Janeiro)

| Ano | Partidos disponíveis |
|-----|---------------------|
| 2002 | PAN, PC do B, PCB, PCO, PDT, PFL, PGT, PHS, PMDB, PMN, PP, PPS, PR, PRONA, PRP, PRTB, PSB, PSC, PSD, PSDB, PSDC, PSL, PST, PSTU, PT, PT do B, PTB, PTC, PTN, PV |
| 2006 | PC do B, PCB, PCO, PDT, PFL, PHS, PMDB, PMN, PP, PPS, PR, PRB, PRONA, PRP, PRTB, PSB, PSC, PSDB, PSDC, PSL, PSOL, PSTU, PT, PT do B, PTB, PTC, PTN, PV |
| 2010 | DEM, PC do B, PCB, PDT, PHS, PMDB, PMN, PP, PPS, PR, PRB, PRP, PRTB, PSB, PSC, PSDB, PSDC, PSL, PSOL, PSTU, PT, PT do B, PTB, PTC, PTN, PV |
| 2014 | DEM, PC do B, PCB, PCO, PDT, PEN, PHS, PMDB, PMN, PP, PPL, PPS, PR, PRB, PROS, PRP, PRTB, PSB, PSC, PSD, PSDB, PSDC, PSL, PSOL, PSTU, PT, PT do B, PTB, PTC, PTN, PV, SDD |

Padrão de URL: `https://www.lab-doxa.org.br/wp-content/uploads/2022/10/[PARTIDO]-DF[ANO].pdf`

#### Deputados Estaduais por partido

| Ano | Partidos disponíveis |
|-----|---------------------|
| 1998 | PAN, PC do B, PCB, PDT, PFL, PGT, PHS, PMDB, PMN, PP, PPS, PR, PRONA, PRP, PRTB, PSB, PSC, PSD, PSDB, PSDC, PSL, PST, PSTU, PT, PT do B, PTB, PTC, PTN, PV |
| 2002 | PAN, PC do B, PCO, PDT, PFL, PGT, PHS, PMDB, PMN, PP, PPS, PR, PRONA, PRP, PRTB, PSB, PSC, PSD, PSDB, PSDC, PSL, PST, PSTU, PT, PT do B, PTB, PTC, PTN, PV |
| 2006 | PAN, PCB, PCdoB, PCO, PDT, PFL, PHS, PMDB, PMN, PP, PPS, PR, PRB, PRONA, PRP, PRTB, PSB, PSC, PSDB, PSDC, PSL, PSOL, PSTU, PT, PTB, PTC, PTdoB, PV |
| 2010 | DEM, PC do B, PCB, PDT, PHS, PMDB, PMN, PP, PPS, PR, PRP, PRTB, PSB, PSC, PSDB, PSDC, PSL, PSOL, PSTU, PT, PT do B, PTB, PTC, PTN, PV |
| 2014 | DEM, PC do B, PCB, PDT, PEN, PHS, PMDB, PMN, PP, PPL, PPS, PR, PRB, PROS, PRP, PRTB, PSB, PSC, PSD, PSDB, PSDC, PSL, PSOL, PSTU, PT, PT do B, PTB, PTC, PTN, PV, SDD |

Padrão de URL: `https://www.lab-doxa.org.br/wp-content/uploads/2022/10/[PARTIDO]-DE[ANO].pdf`

**Observação:** Os PDFs dos mapas devem ser hospedados em `static/files/mapas/` no novo site, ou mantidos com link externo para o WordPress enquanto o site antigo estiver no ar.

---

## Bancos de Dados (`https://www.lab-doxa.org.br/bancos-de-dados/`)

A página de bancos de dados no WordPress funciona como menu de navegação. Os conteúdos reais estão distribuídos em outras páginas. Abaixo, o que foi identificado:

### 1. Cobertura Jornalística
- Análise quantitativa da cobertura dos principais candidatos presidenciais nos grandes jornais nacionais.
- Mede: visibilidade, valência (positiva/negativa/neutra), enquadramento e agenda.
- Os arquivos ficam na página Análises de Conjuntura Eleitoral (ver seção abaixo).

### 2. Horário Gratuito de Propaganda Eleitoral (HGPE)
- Banco de vídeos do acervo audiovisual (presidenciais 1989–2022 e governadores 1994–2014).
- Acesso via catálogo Google Sheets: https://docs.google.com/spreadsheets/d/1b_OFFW0fJS3B0DFvfeoa6y8l9YG6JmFP/edit

### 3. Mapas Eleitorais
- PDFs com distribuição do voto por bairros do Rio de Janeiro (1998–2014).
- Detalhes na seção "Mapas de Votação" acima.

### 4. Programas de Governo (Eleições Municipais 2020)
- Programas de candidatos a prefeito no Estado do Rio de Janeiro
- Programas de candidatos a prefeito nas capitais brasileiras
- **Lacuna:** Links diretos para esses bancos não foram encontrados na página.

---

## Publicações Acadêmicas (`https://www.lab-doxa.org.br/publicacoes-academicas/`)

### YAML pronto para `data/publications.yaml`

```yaml
# ---- Livros ----

- title: "Corrupção, Como e por quê seu dinheiro sai pelo ladrão"
  authors: "Salomão, L. A.; Guarnieri, Fernando"
  year: 2016
  type: "livro"
  publisher: "Nitpress, Niterói"
  url: ""

- title: "Política Local no Estado do Rio de Janeiro – As eleições municipais de 2020"
  authors: "Borba, Felipe (org.); Figueiredo, Argelina (org.)"
  year: 2022
  type: "livro"
  publisher: "Editora da UERJ"
  url: ""

- title: "25 anos de eleições presidenciais no Brasil"
  authors: "Figueiredo, Argelina (org.); Borba, Felipe (org.)"
  year: 2018
  type: "livro"
  publisher: "Appris, Curitiba"
  url: ""

- title: "Eleições, opinião pública e comunicação política no Brasil contemporâneo: homenagem a Marcus Figueiredo"
  authors: "Borba, Felipe (org.); Aldé, Alessandra (org.)"
  year: 2017
  type: "livro"
  publisher: "Eduerj"
  url: ""

# ---- Capítulos de livro ----

- title: "Magnitude eleitoral e representação de mulheres nos municípios brasileiros"
  authors: "Meireles, F.; Andrade, L."
  year: 2021
  type: "capitulo"
  publisher: "In: Mulheres e representação política: 25 estudos sobre cotas eleitorais no Brasil. Org.: Luis Felipe Miguel. Zouk, Porto Alegre"
  url: ""

- title: "O impacto da Covid-19 no comportamento eleitoral do fluminense nas eleições de 2020"
  authors: "Guarnieri, Fernando; Figueiredo, Argelina"
  year: 2022
  type: "capitulo"
  publisher: "In: As eleições municipais de 2020 no Estado do Rio de Janeiro. Org.: Felipe Borba; Argelina Figueiredo. Editora da UERJ"
  url: ""

- title: "Estudos Legislativos em Perspectiva Comparada"
  authors: "Figueiredo, Argelina; Freitas, Andréa; Medeiros, Danilo"
  year: 2022
  type: "capitulo"
  publisher: "In: Política Comparada. Org.: Renato Perissinoto et al. Editora da UERJ"
  url: ""

- title: "Vulnerabilidades sociais, modelos de provisão de saúde e suas relações com a mortalidade decorrente da pandemia de Covid-19 no Brasil e nos Estados Unidos"
  authors: "Figueiredo, Argelina; Guichney, Hellen; Lazzari, Eduardo"
  year: 2022
  type: "capitulo"
  publisher: "In: COVID-19 e agendas de pesquisa nas ciências sociais. Org.: Fernando Fontainha; Carlos Milani. Editora da UERJ"
  url: ""

- title: "Determinantes Políticos e Institucionales del Éxito Legislativo del Ejecutivo em América Latina"
  authors: "Figueiredo, Argelina; Salles, Denise; Martins, Marcelo"
  year: 2011
  type: "capitulo"
  publisher: "In: Algo más que presidentes. El papel del Poder Legislativo en América Latina. Org.: Manuel Alcántara; Mercedes García Montero. Fundación Manuel Giménez Abad, Zaragoza"
  url: "https://www.fundacionmgimenezabad.es/sites/default/files/Publicar/publicaciones/documentos/a1-actas1_algo_mas_que_presidentes_dig_0.pdf"

- title: "Os partidos nas eleições proporcionais no Estado do Rio"
  authors: "Figueiredo, Argelina; Maciel, Natália"
  year: 2019
  type: "capitulo"
  publisher: "In: Eleições de 2018 e a Crise da Democracia Brasileira. Org.: João Feres Jr.; Carolina de Paula. Appris, Curitiba"
  url: ""

- title: "A implosão da centro-direita e o voto em Bolsonaro"
  authors: "Guarnieri, Fernando; Albuquerque, Felipe"
  year: 2019
  type: "capitulo"
  publisher: "In: Eleições de 2018 e a Crise da Democracia Brasileira. Org.: João Feres Jr.; Carolina de Paula. Appris, Curitiba"
  url: ""

- title: "O voto do eleitor pobre nas eleições presidenciais (1989–2014)"
  authors: "Figueiredo, Argelina; Maciel, Natália; Simoni Jr., Sérgio; Silva, Thiago M."
  year: 2018
  type: "capitulo"
  publisher: "In: 25 anos de eleições presidenciais no Brasil. Org.: Figueiredo, Argelina; Borba, Felipe. Appris, Curitiba"
  pages: "pp. 75–94"
  url: ""

- title: "Political Participation in Brazil"
  authors: "Limongi, Fernando; Cheibub, José A.; Figueiredo, Argelina"
  year: 2018
  type: "capitulo"
  publisher: "In: Paths of Inequality in Brazil: a Half Century of Changes. Org.: Marta Arretche. Springer, Switzerland"
  pages: "pp. 4–24"
  url: ""

- title: "Estudos legislativos no Brasil"
  authors: "Figueiredo, Argelina; Santos, Fabiano"
  year: 2016
  type: "capitulo"
  publisher: "In: A ciência política no Brasil. 1960–2015. Org.: Leonardo Avritzer; Carlos R. S. Milani; Maria do Socorro Braga. Editora FGV; ABCP, Rio de Janeiro"
  url: ""

- title: "Political Institutions and Governmental Performance in Brazilian Democracy"
  authors: "Figueiredo, Argelina; Limongi, Fernando"
  year: 2015
  type: "capitulo"
  publisher: "In: The Political System of Brazil. Org.: Dana de la Fontaine; Thomas Stehnken. Springer, New York. ISBN: 978-3-642-40022-3"
  url: ""

- title: "Participação Política no Brasil"
  authors: "Limongi, Fernando; Cheibub, José A.; Figueiredo, Argelina"
  year: 2015
  type: "capitulo"
  publisher: "In: volume organizado por Marta Arretche. Editora UNESP, São Paulo"
  url: ""

# ---- Artigos em revista ----

- title: "Eleições municipais de 2016 e 2020 em São Paulo: resultados diferentes, alinhamentos iguais"
  authors: "Zolnerkevic, A.; Guarnieri, F."
  year: 2023
  type: "artigo"
  journal: "Opinião Pública"
  pages: "v. 29, pp. 133–165"
  url: ""

- title: "Deu Match? Uma introdução às técnicas de pareamento"
  authors: "Schaefer, B. M.; Figueiredo Filho, Dalson Britto"
  year: 2023
  type: "artigo"
  journal: "Revista Brasileira de Ciências Sociais (Online)"
  pages: "v. 38, pp. 1–20"
  url: ""

- title: "Plutocratas, personalistas ou inexperientes: uma revisão sistemática sobre autofinanciamento eleitoral"
  authors: "Schaefer, B. M."
  year: 2023
  type: "artigo"
  journal: "Agenda Política"
  pages: "v. 10, p. 94"
  url: ""

- title: "Política Distributiva em Coalizão"
  authors: "Meireles, F."
  year: 2024
  type: "artigo"
  journal: "Dados – Revista de Ciências Sociais"
  pages: "v. 67, p. 1"
  url: ""

- title: "Multi-level legislative representation in an inchoate party system: Mass-elite ideological congruence in Brazil"
  authors: "Carroll, Royce; Meireles, F."
  year: 2024
  type: "artigo"
  journal: "Party Politics"
  pages: "v. 30, pp. 151–165"
  url: ""

- title: "Pesquisas eleitorais no Brasil: tendências e desempenho"
  authors: "Meireles, F.; Russo, G."
  year: 2022
  type: "artigo"
  journal: "Estudos Avançados (Online)"
  pages: "v. 36, pp. 117–131"
  url: ""

- title: "O Governo Bolsonaro e a Conjuntura Política Pré-Eleitoral"
  authors: "Guarnieri, F.; Figueiredo, A."
  year: 2022
  type: "artigo"
  journal: "Cadernos Adenauer (São Paulo)"
  pages: "v. 23, p. 9"
  url: ""

- title: "A spatial interaction model of vote dispersion"
  authors: "Guarnieri, F.; Silva, G. P."
  year: 2022
  type: "artigo"
  journal: "Political Geography"
  pages: "v. 98, art. 102709"
  url: ""

- title: "Democratic Principles and Performance: What do the Experts Think?"
  authors: "Russo, G. A.; Avelino, G.; Guarnieri, F."
  year: 2022
  type: "artigo"
  journal: "Journal of Politics in Latin America (Print)"
  pages: "v. 14, pp. 224–236"
  url: ""

- title: "Modelos de competição política e as eleições de 2022"
  authors: "Guarnieri, F.; Figueiredo, A."
  year: 2022
  type: "artigo"
  journal: "Cadernos Adenauer (São Paulo)"
  pages: "v. 4, p. 9"
  url: ""

- title: "O governo Bolsonaro e a conjuntura eleitoral"
  authors: "Guarnieri, Fernando; Figueiredo, Argelina"
  year: 2022
  type: "artigo"
  journal: "Cadernos Adenauer"
  pages: "v. XXIII, n. 2"
  url: ""

- title: "A Crise Atual e o Debate Institucional"
  authors: "Limongi, Fernando; Figueiredo, Argelina"
  year: 2017
  type: "artigo"
  journal: "Novos Estudos Cebrap"
  pages: "v. 36, n. 3"
  url: "https://www.scielo.br/j/nec/a/KBxnHhZWWCPJ5zgJwKTTzSK/abstract/?lang=pt"

- title: "Entrevista a Fabio Kersche e João Feres Junior"
  authors: "Figueiredo, Argelina"
  year: 2016
  type: "artigo"
  journal: "ESCRITOS: Revista da Fundação Casa de Rui Barbosa"
  pages: "v. 8, n. 8, pp. 233–252"
  url: ""

# ---- Outras produções ----

- title: "Contracapa do livro Democracia e Eleições no Brasil. Para onde vamos?"
  authors: "Figueiredo, Argelina"
  year: 2022
  type: "outros"
  publisher: "In: Magna Inácio; Vanessa Elias de Oliveira (orgs.). Hucitec/Anpocs"
  url: ""

- title: "Prefácio do livro Por que eleições são importantes?"
  authors: "Figueiredo, A. M. C."
  year: 2021
  type: "outros"
  publisher: "Prefácio. In: Adam Przeworki. EdUERJ, Rio de Janeiro"
  url: ""

- title: "Prefácio do livro O presidencialismo da Coalizão"
  authors: "Limongi, Fernando; Figueiredo, Argelina"
  year: 2016
  type: "outros"
  publisher: "Prefácio. In: Andréa Marcondes de Freitas. Fundação Konrad Adenauer, Rio de Janeiro"
  url: ""
```

---

## Análises de Conjuntura Eleitoral (`https://www.lab-doxa.org.br/analises-de-conjuntura-eleitoral/`)

A página organiza as análises em dois grandes tipos: (1) Cobertura Jornalística de grandes jornais e (2) Horário Gratuito de Propaganda Eleitoral (HGPE) e Debates.

### YAML pronto para `data/analyses.yaml`

```yaml
# ---- Cobertura Jornalística ----

- title: "Cobertura Jornalística das Eleições 2002 — O Globo"
  cycle: "2002"
  period: "Eleições Gerais 2002"
  description: "Análise quantitativa da cobertura dos candidatos presidenciais em O Globo."
  files:
    - label: "Gráfico"
      url: "https://www.lab-doxa.org.br/wp-content/uploads/2022/11/021-2002-graficos-cobertura-jornalisitca-oglobo.pdf"
    - label: "Tabela"
      url: "https://www.lab-doxa.org.br/wp-content/uploads/2022/11/022-2002-tabelas-cobertura-jornalisitca-oglobo.pdf"

- title: "Cobertura Jornalística das Eleições 2002 — Jornal do Brasil"
  cycle: "2002"
  period: "Eleições Gerais 2002"
  description: "Análise quantitativa da cobertura dos candidatos presidenciais no Jornal do Brasil."
  files:
    - label: "Gráfico"
      url: "https://www.lab-doxa.org.br/wp-content/uploads/2022/11/023-2002-graficos-cobertura-jornalisitca-JB.pdf"
    - label: "Tabela"
      url: "https://www.lab-doxa.org.br/wp-content/uploads/2022/11/024-2002-tabelas-cobertura-jornalisitca-JB.pdf"

- title: "Cobertura Jornalística das Eleições 2002 — Folha de S.Paulo"
  cycle: "2002"
  period: "Eleições Gerais 2002"
  description: "Análise quantitativa da cobertura dos candidatos presidenciais na Folha de S.Paulo."
  files:
    - label: "Gráfico"
      url: "https://www.lab-doxa.org.br/wp-content/uploads/2022/11/025-2002-graficos-cobertura-jornalistica-folha.pdf"
    - label: "Tabela"
      url: "https://www.lab-doxa.org.br/wp-content/uploads/2022/11/026-2002-tabelas-cobertura-jornalistica-folha.pdf"

- title: "Cobertura Jornalística das Eleições 2002 — O Estado de S.Paulo"
  cycle: "2002"
  period: "Eleições Gerais 2002"
  description: "Análise quantitativa da cobertura dos candidatos presidenciais em O Estado de S.Paulo."
  files:
    - label: "Gráfico"
      url: "https://www.lab-doxa.org.br/wp-content/uploads/2022/11/028-2002-graficos-cobertura-jornalistica-OESP.pdf"

- title: "Cobertura Jornalística das Eleições 2006 — O Globo"
  cycle: "2006"
  period: "Eleições Gerais 2006"
  description: "Análise quantitativa da cobertura dos candidatos presidenciais em O Globo."
  files:
    - label: "Gráfico"
      url: "https://www.lab-doxa.org.br/wp-content/uploads/2022/11/031-2006-graficos-cobertura-jornalisitca-oglobo.pdf"
    - label: "Tabela"
      url: "https://www.lab-doxa.org.br/wp-content/uploads/2022/11/032-2006-tabelas-cobertura-jornalisitca-oglobo.pdf"

- title: "Cobertura Jornalística das Eleições 2006 — Jornal do Brasil"
  cycle: "2006"
  period: "Eleições Gerais 2006"
  description: ""
  files:
    - label: "Gráfico"
      url: "https://www.lab-doxa.org.br/wp-content/uploads/2022/11/033-2006-graficos-cobertura-jornalisitca-JB.pdf"
    - label: "Tabela"
      url: "https://www.lab-doxa.org.br/wp-content/uploads/2022/11/034-2006-tabelas-cobertura-jornalisitca-JB.pdf"

- title: "Cobertura Jornalística das Eleições 2006 — Folha de S.Paulo"
  cycle: "2006"
  period: "Eleições Gerais 2006"
  description: ""
  files:
    - label: "Gráfico"
      url: "https://www.lab-doxa.org.br/wp-content/uploads/2022/11/035-2006-graficos-cobertura-jornalisitca-folha.pdf"
    - label: "Tabela"
      url: "https://www.lab-doxa.org.br/wp-content/uploads/2022/11/036-2006-tabelas-cobertura-jornalisitca-folha.pdf"

- title: "Cobertura Jornalística das Eleições 2006 — O Estado de S.Paulo"
  cycle: "2006"
  period: "Eleições Gerais 2006"
  description: ""
  files:
    - label: "Gráfico"
      url: "https://www.lab-doxa.org.br/wp-content/uploads/2022/11/037-2006-graficos-cobertura-jornalisitca-OESP.pdf"
    - label: "Tabela"
      url: "https://www.lab-doxa.org.br/wp-content/uploads/2022/11/038-2006-tabelas-cobertura-jornalisitca-OESP.pdf"

- title: "Cobertura Jornalística das Eleições 2010 — O Globo"
  cycle: "2010"
  period: "Eleições Gerais 2010"
  description: ""
  files:
    - label: "Gráfico"
      url: "https://www.lab-doxa.org.br/wp-content/uploads/2022/11/041-2010-graficos-cobertura-jornalistica-oglobo.pdf"

- title: "Cobertura Jornalística das Eleições 2010 — Valor Econômico"
  cycle: "2010"
  period: "Eleições Gerais 2010"
  description: ""
  files:
    - label: "Gráfico"
      url: "https://www.lab-doxa.org.br/wp-content/uploads/2022/11/042-2010-graficos-cobertura-jornalistica-Valor.pdf"

- title: "Cobertura Jornalística das Eleições 2010 — Folha de S.Paulo"
  cycle: "2010"
  period: "Eleições Gerais 2010"
  description: ""
  files:
    - label: "Gráfico"
      url: "https://www.lab-doxa.org.br/wp-content/uploads/2022/11/043-2010-graficos-cobertura-jornalistica-folha.pdf"

- title: "Cobertura Jornalística das Eleições 2010 — O Estado de S.Paulo"
  cycle: "2010"
  period: "Eleições Gerais 2010"
  description: ""
  files:
    - label: "Gráfico"
      url: "https://www.lab-doxa.org.br/wp-content/uploads/2022/11/044-2010-graficos-cobertura-jornalistica-OESP.pdf"

# ---- HGPE e Debates ----

- title: "HGPE — Eleições 1989"
  cycle: "1989"
  period: "Eleições Presidenciais 1989"
  description: "Resumos transcritos do HGPE presidencial de 1989, baseados na dissertação de doutorado de Afonso de Albuquerque."
  files:
    - label: "PDF"
      url: "https://www.lab-doxa.org.br/wp-content/uploads/2022/11/007-1989-HGPE-Eleicoes-Aqui-voce-ve-a-verdade-na-teve-Afonso-de-Albuquerque.pdf"

- title: "Debates Eleitorais 2002 — 1º Turno, Debate 1"
  cycle: "2002"
  period: "Eleições Presidenciais 2002"
  description: "Análise qualitativa e quantitativa da recepção dos debates presidenciais de 2002, em parceria com o MIT."
  files:
    - label: "PDF"
      url: "https://www.lab-doxa.org.br/wp-content/uploads/2022/11/001-2002-Debates-Eleitorais-primeiroround.pdf"

- title: "Debates Eleitorais 2002 — 1º Turno, Debate 2"
  cycle: "2002"
  period: "Eleições Presidenciais 2002"
  description: ""
  files:
    - label: "PDF"
      url: "https://www.lab-doxa.org.br/wp-content/uploads/2022/11/002-2002-Debates-Eleitorais-segundoround.pdf"

- title: "Debates Eleitorais 2002 — 1º Turno, Debate 3"
  cycle: "2002"
  period: "Eleições Presidenciais 2002"
  description: ""
  files:
    - label: "PDF"
      url: "https://www.lab-doxa.org.br/wp-content/uploads/2022/11/003-2002-Debates-Eleitorais-terceiroround.pdf"

- title: "Debates Eleitorais 2002 — 2º Turno"
  cycle: "2002"
  period: "Eleições Presidenciais 2002"
  description: ""
  files:
    - label: "PDF"
      url: "https://www.lab-doxa.org.br/wp-content/uploads/2022/11/004-2002-Debates-Eleitorais-segundoturno.pdf"

# ---- IESP nas Eleições 2018 ----

- title: "Os partidos nas eleições proporcionais no Estado do Rio — Eleições 2018"
  cycle: "2018"
  period: "Eleições Gerais 2018"
  description: "Parte do projeto IESP nas Eleições 2018."
  files:
    - label: "PDF"
      url: "https://www.lab-doxa.org.br/wp-content/uploads/2022/12/Figueiredo-A._-Maciel-N.-Os-partidos-nas-eleicoes-proporcionais-no-Estado-do-Rio-de-Janeiro.pdf"

- title: "A implosão da centro-direita e o voto em Bolsonaro — Eleições 2018"
  cycle: "2018"
  period: "Eleições Gerais 2018"
  description: "Parte do projeto IESP nas Eleições 2018."
  files:
    - label: "PDF"
      url: "https://www.lab-doxa.org.br/wp-content/uploads/2022/12/Guarnieri-F_-Albuquerque-F.-A-implosao-da-centro-direita-e-o-voto-em-Bolsonaro.pdf"

- title: "Resumo do HGPE — 1ª Semana (31/8–8/9/2018)"
  cycle: "2018"
  period: "Eleições Gerais 2018"
  description: "Resumo semanal do Horário Eleitoral Gratuito presidencial. Autor: Holanda, M."
  files:
    - label: "PDF"
      url: "https://www.lab-doxa.org.br/wp-content/uploads/2022/12/Holanda-M.-Resumo-do-Horario-Eleitoral-Gratuito-de-Propaganda-Eleitoral-HGPE-1°-Semana-3182018-A-892018.pdf"

- title: "Resumo do HGPE — 2ª Semana (10–15/9/2018)"
  cycle: "2018"
  period: "Eleições Gerais 2018"
  description: "Autor: Cunha, C."
  files:
    - label: "PDF"
      url: "https://www.lab-doxa.org.br/wp-content/uploads/2022/12/Cunha-C.-Resumo-do-Horario-Eleitoral-Gratuito-de-Propaganda-Eleitoral-HGPE-–-2°-Semana-1092018-a-1592018.pdf"

- title: "Resumo do HGPE — 3ª Semana (17–22/9/2018)"
  cycle: "2018"
  period: "Eleições Gerais 2018"
  description: "Autor: Cunha, C."
  files:
    - label: "PDF"
      url: "https://www.lab-doxa.org.br/wp-content/uploads/2022/12/Cunha-C.-Resumo-do-Horario-Eleitoral-Gratuito-de-Propaganda-Eleitoral-HGPE-–-3a-Semana-1792018-a-2292018.pdf"

- title: "Resumo do HGPE — 4ª Semana (25–29/9/2018)"
  cycle: "2018"
  period: "Eleições Gerais 2018"
  description: "Autor: Curvelo, D."
  files:
    - label: "PDF"
      url: "https://www.lab-doxa.org.br/wp-content/uploads/2022/12/Curvelo-D.-Resumo-do-Horario-Eleitoral-–-4a-Semana-259-a-2992018.pdf"

- title: "Horário Eleitoral Gratuito — Governador do Estado do Rio de Janeiro (2018)"
  cycle: "2018"
  period: "Eleições Gerais 2018"
  description: "Autor: Curvelo, D."
  files:
    - label: "PDF"
      url: "https://www.lab-doxa.org.br/wp-content/uploads/2022/12/Curvelo-D.-Resumo-do-Horario-Eleitoral-–-4a-Semana-259-a-2992018.pdf"

# ---- Vota Aí 2020 ----

- title: "Vota Aí — Eleições Municipais 2020"
  cycle: "2020"
  period: "Eleições Municipais 2020"
  description: "Plataforma interativa para análise dos programas de governo registrados no TSE pelos candidatos a prefeito. Coordenação: Nara Salles."
  files:
    - label: "Podcasts YouTube"
      url: "https://www.youtube.com/@votaai6247/videos"
```

---

## Textos para Discussão (`https://www.lab-doxa.org.br/textos-para-discussao-2/`)

### YAML pronto para `data/discussions.yaml`

```yaml
- title: "As políticas de controle de armas de fogo e munições no Brasil"
  authors: "Matteo de Barros Manes"
  year: 2024
  type: "outros"
  url: "https://www.lab-doxa.org.br/wp-content/uploads/2026/03/DOXA-Politicas-de-controle-de-armas-de-fogo-e-municao-no-Brasil-Matteo-Manes.pdf"

- title: "Tempo é dinheiro: recursos partidários em eleições para a Câmara Federal"
  authors: "Bruno Marques Schaefer"
  year: 2023
  type: "outros"
  url: "https://www.lab-doxa.org.br/wp-content/uploads/2023/06/Schaefer-B.-2023.-TD-Tempo-e-dinheiro.pdf"
```

---

## Eventos (`https://www.lab-doxa.org.br/eventos/`)

### YAML pronto para `data/events.yaml`

```yaml
- title: "Edição digital gratuita do livro "A Decisão do Voto" de Marcus Figueiredo"
  date: "2022-12-16"
  description: >
    O DOXA disponibiliza gratuitamente a edição digital do livro "A Decisão do Voto"
    de Marcus Figueiredo, fundador do laboratório.
  image: "https://www.lab-doxa.org.br/wp-content/uploads/2022/12/FIGUEIREDO_A-DECISAO-DO-VOTO_CARTAZ-576x1024.jpg"
  url: "https://www.lab-doxa.org.br/edicao-digital-gratuita-do-livro-a-decisao-do-voto-de-marcus-figueiredo/"
  link_livro: "https://docs.google.com/document/d/15D7Ccv0A4fiUiOCtammle_8xdUJ977kkTwx5tWTCSI8/edit?usp=drivesdk"

- title: "Seminário comemora 25 anos do DOXA"
  date: "2021-11-25"
  description: >
    Seminário online para discutir a origem e o legado do laboratório e traçar
    panorama sobre temas centrais para a democracia brasileira. Participantes:
    Fernando Limongi (USP/FGV), Patrícia Campos Mello (Folha de S. Paulo),
    Luciana Veiga (Unirio/ABCP), Felipe Borba (Unirio). Moderação: Fernando Guarnieri.
    Transmitido pelo canal do IESP no YouTube.
  image: "https://www.lab-doxa.org.br/wp-content/uploads/2022/08/Seminario-25-anos-DOXA-1024x576.jpg"
  url: "https://www.lab-doxa.org.br/seminario-comemora-25-anos-do-doxa/"

- title: "DOXA 20 anos: O legado de Marcus Figueiredo"
  date: "2017-11-13"
  description: >
    Evento realizado no IESP/UERJ (Rua da Matriz, 82 – Botafogo, Rio de Janeiro)
    com abertura às 14h por Fernando Azevedo (UFSCar) e Afonso Albuquerque (UFF),
    lançamento do livro "Eleições, Opinião Pública e Comunicação Política no Brasil
    Contemporâneo" (orgs. Felipe Borba e Alessandra Aldé) e homenagem a Marcus Figueiredo.
  image: "https://www.lab-doxa.org.br/wp-content/uploads/2022/11/Doxa_20_parae-mail_azul-1024x682.jpg"
  url: "https://www.lab-doxa.org.br/doxa-20-anos-o-legado-de-marcus-figueiredo/"

- title: "Seminário Marcus Figueiredo: Eleições, Opinião Pública e Comunicação Política no Brasil Contemporâneo"
  date: "2014-11-26"
  description: "Seminário sobre eleições, opinião pública e comunicação política no Brasil contemporâneo."
  image: "https://www.lab-doxa.org.br/wp-content/uploads/2022/12/CARTAZ_Seminario-Marcus-Figueiredo-724x1024.jpg"
  url: "https://www.lab-doxa.org.br/seminario-marcus-figueiredo-eleicoes-opiniao-publica-e-comunicacao-politica-no-brasil-contemporaneo/"

- title: "Nota editorial sobre falecimento de Marcus Figueiredo na Revista Dados"
  date: "2014-08-08"
  description: "Nota editorial publicada na Revista Dados sobre o falecimento de Marcus Figueiredo, fundador do DOXA."
  image: "https://www.lab-doxa.org.br/wp-content/uploads/2022/09/marcusfigueiredo_destaque-1024x615.jpg"
  url: "https://www.lab-doxa.org.br/nota-editorial-sobre-falecimento-de-marcus-figueiredo-na-revista-dados-em-agosto-de-2014/"
```

---

## Seminários (`https://www.lab-doxa.org.br/seminarios/`)

### YAML pronto para `data/seminars.yaml`

```yaml
# 2023
- title: "Conjoint Experiment: representação e preferências no estado do Rio de Janeiro"
  presenter: "Fernando Meireles"
  institution: "IESP-UERJ"
  date: "2023-09-25"
  year: 2023

- title: "Defensive Logic of resource allocation: Brazil's party financing in the state level"
  presenter: "Bruno Schaefer"
  institution: "IESP-UERJ"
  date: "2023-06-19"
  year: 2023

# 2021
- title: "Trustful Voters, Trustworthy Politicians: A Survey Experiment on the Influence of Social Media in Politics"
  presenter: "Tiago Ventura; Natalia Aruguete; Ernesto Calvo; Carlos Scartascini"
  institution: "University of Maryland"
  date: "2021-03-25"
  year: 2021

- title: "O Auxílio Emergencial Salvou Bolsonaro? Um estudo quasi-experimental"
  presenter: "Felipe Nunes"
  institution: "UFMG-Quaest"
  date: "2021-04-21"
  year: 2021

- title: "The Public Opinion Consequences of Lava-Jato in Brazil"
  presenter: "Nara Pavão"
  institution: "UFPE"
  date: "2021-05-27"
  year: 2021

- title: "Government and Opposition in Legislative Speechmaking: Using Text-As-Data"
  presenter: "Mauricio Y. Izumi; Danilo B. Medeiros"
  institution: "UFES / CEBRAP"
  date: "2021-06-24"
  year: 2021

- title: "A Spatial Interaction Model of Vote Dispersion"
  presenter: "Fernando Guarnieri; Glauco Peres da Silva"
  institution: "IESP-UERJ"
  date: "2021-09-01"
  year: 2021

- title: "Congresso Remoto: dinâmicas do legislativo federal em tempos de pandemia"
  presenter: "Júlio Canello"
  institution: "IESP-UERJ"
  date: "2021-09-24"
  year: 2021

- title: "Government and Opposition in Legislative Speechmaking: Using Text-as-Data"
  presenter: "Maurício Izumi; Danilo Medeiros"
  institution: "UFES / CEBRAP"
  date: "2021-10-13"
  year: 2021

- title: "A experiência da energia solar no Brasil – processos decisórios locais e evolução de indicadores"
  presenter: "Carolina Botelho"
  institution: "IESP-UERJ"
  date: "2021-10-22"
  year: 2021

- title: "Celebração dos 25 anos do DOXA"
  presenter: ""
  institution: "DOXA/IESP-UERJ"
  date: "2021-11-18"
  year: 2021

- title: "The Overlooked Role of the Brazilian Congress in Shaping the Bolsa Família Program"
  presenter: "Pedro Bras Martins da Costa"
  institution: "IESP-UERJ"
  date: "2021-11-19"
  year: 2021

# 2020
- title: "Tamanho é documento? Porte de municípios e competição programática no Brasil"
  presenter: "Nara Salles"
  institution: "IESP-UERJ"
  date: "2020-05-11"
  year: 2020

- title: "O uso que o eleitor faz da intuição ao elaborar seu julgamento político"
  presenter: "Luciana Veiga; Flávia Bozza Martins"
  institution: "Unirio / IESP-UERJ"
  date: "2020-06-16"
  year: 2020

- title: "Processo decisório e políticas públicas de energia solar no Brasil"
  presenter: "Carolina Botelho"
  institution: "IESP-UERJ"
  date: "2020-10-22"
  year: 2020

# 2019
- title: "Voto no PT nas Eleições Presidenciais de 2014: Eleitor Pobre do Nordeste?"
  presenter: "Thiago Moreira da Silva; Sergio Simoni Jr; Argelina Figueiredo; Natalia Maciel"
  institution: "IESP-UERJ"
  date: "2019-03-21"
  year: 2019

- title: "Instituições políticas em regimes oligárquicos: partidos e competição eleitoral"
  presenter: "Jaqueline Zulini"
  institution: "CPDOC"
  date: "2019-05-06"
  year: 2019

- title: "The New Politics of Gubernatorial Elections in Brazil (1994–2018)"
  presenter: "Fabiano Santos; Cristiane Batista; Thiago Moreira da Silva"
  institution: "IESP-UERJ / UNIRIO"
  date: "2019-10-10"
  year: 2019

- title: "Quem se abstém no Brasil? Uma descrição do perfil socioeconômico dos eleitores ausentes"
  presenter: "Felipe Borba"
  institution: "Unirio"
  date: "2019-11-19"
  year: 2019

# 2018
- title: "Realinhamento eleitoral e Programa Bolsa Família nas eleições presidenciais brasileiras"
  presenter: "Sergio Simoni Junior"
  institution: "UNICAMP"
  date: "2018-03-12"
  year: 2018

- title: "Cap 3. Voto econômico e Contexto político-institucional"
  presenter: "Flávia Bozza"
  institution: "IESP-UERJ"
  date: "2018-04-17"
  year: 2018

- title: "Territórios eleitorais e estratégia política: reflexões a partir de um quase-experimento"
  presenter: "Fernando Guarnieri; Gabriel Melo"
  institution: "IESP/UERJ"
  date: "2018-08-07"
  year: 2018

- title: "Efeitos práticos da sub-representação política: o desalinhamento das preferências"
  presenter: "Thiago Moreira da Silva"
  institution: "IESP-UERJ"
  date: "2018-10-18"
  year: 2018

# 2017
- title: "Projeto de Pesquisa: Mídias sociais como fonte de informação política"
  presenter: "Natalia Maciel"
  institution: "Doxa-IESP/UERJ"
  date: "2017-03-27"
  year: 2017

- title: "Os determinantes da perda da popularidade da Presidente Dilma"
  presenter: "Luciana Veiga; Flávia Bozza; Steven Ross"
  institution: "Unirio / IESP/UERJ"
  date: "2017-04-27"
  year: 2017

- title: "Quando Governadores vão ao Supremo: razões para o controle direto de constitucionalidade"
  presenter: "Júlio Canello"
  institution: "IESP-UERJ"
  date: "2017-05-27"
  year: 2017

- title: "Nem tão 'Flamengo': o diagnóstico alternativo de uma síndrome antecipada"
  presenter: "Thiago Moreira da Silva"
  institution: "IESP-UERJ"
  date: "2017-09-21"
  year: 2017

- title: "Cap 3. Instituições, estatutos e coalizões dominantes no PSD, UDN e PTB (1950–64)"
  presenter: "Saulo Said"
  institution: "IESP-UERJ"
  date: "2017-10-19"
  year: 2017

# 2016
- title: "Coligação à brasileira: efeitos sobre a fragmentação e a proporcionalidade"
  presenter: "Felipe Munhoz Albuquerque; Saulo Maia Said"
  institution: "IESP-UERJ"
  date: "2016-03-22"
  year: 2016

- title: "The Impact of Violence on Non-Incumbent Party Support in Brazilian Gubernatorial Elections"
  presenter: "Douglas Block"
  institution: ""
  date: "2016-06-23"
  year: 2016

- title: "Desenvolvimento e partidarismo: os programas de governo nos grotões do Brasil"
  presenter: "Fernando Guarnieri; Nara Salles"
  institution: "IESP/UERJ"
  date: "2016-11-24"
  year: 2016

# 2015
- title: "Cap 5. Estratégias de comunicação nas campanhas eleitorais proporcionais"
  presenter: "Cíntia Pinheiro Ribeiro de Souza"
  institution: "IESP-UERJ"
  date: "2015-05-28"
  year: 2015

- title: "PT e PSDB nas eleições para a Câmara dos Deputados: bases sociais e variáveis políticas"
  presenter: "Natalia Maciel"
  institution: "IESP-UERJ"
  date: "2015-06-17"
  year: 2015

- title: "Do Fome Zero ao Bolsa Família? Um estudo comparado a partir dos manifestos do PT"
  presenter: "Pedro Bras Martins da Costa"
  institution: "IESP-UERJ"
  date: "2015-07-28"
  year: 2015

- title: "Incumbency Advantage in Brazilian Mayoral Elections"
  presenter: "Ricardo Caneviva"
  institution: ""
  date: "2015-09-29"
  year: 2015

- title: "Fragmentação Partidária na Câmara dos Deputados: Dilemas de Coordenação no Brasil"
  presenter: "Brenda dos Santos Barboza Cunha"
  institution: "IESP-UERJ"
  date: "2015-11-18"
  year: 2015
```

---

## Na Mídia (`https://www.lab-doxa.org.br/na-midia/`)

### YAML pronto para `data/media.yaml`

O schema usa: `title, authors, outlet, date (YYYY-MM-DD), type (impressa|virtual|audiovisual), url`.

```yaml
# ---- Mídia Impressa ----

- title: "Estimativas de margem de erro no Brasil"
  authors: "Fernando Meireles"
  outlet: "Valor Econômico"
  date: "2022-04-24"
  type: "impressa"
  url: "https://valor.globo.com/politica/coluna/estimativas-de-margem-de-erro-no-brasil.ghtml"

- title: "Prisão não previne ameaças à democracia"
  authors: "Argelina Figueiredo"
  outlet: "Valor Econômico"
  date: "2021-02-22"
  type: "impressa"
  url: "https://valor.globo.com/politica/noticia/2021/02/22/prisao-nao-previne-ameacas-a-democracia.ghtml"

- title: "Respostas das instituições é problemática"
  authors: "Argelina Figueiredo"
  outlet: "Valor Econômico"
  date: "2021-02-22"
  type: "impressa"
  url: "https://valor.globo.com/politica/noticia/2021/02/22/resposta-das-instituicoes-e-problematica.ghtml"

- title: "CPI pode chegar a Bolsonaro, mas ampliar investigação 'embaralha' o jogo político"
  authors: "Argelina Figueiredo"
  outlet: "O Estado de S. Paulo"
  date: "2021-04-12"
  type: "impressa"
  url: "https://politica.estadao.com.br/noticias/geral,cpi-pode-chegar-a-bolsonaro-mas-ampliar-investigacao-embaralha-o-jogo-politico-diz-pesquisadora,70003679247"

- title: "Entenda como a CPI da Covid pode contribuir para responsabilizar Bolsonaro"
  authors: "Argelina Figueiredo"
  outlet: "Folha de São Paulo"
  date: "2021-04-25"
  type: "impressa"
  url: "https://www1.folha.uol.com.br/poder/2021/04/entenda-como-a-cpi-da-covid-pode-contribuir-para-responsabilizar-bolsonaro-por-falas-e-postura-na-pandemia.shtml"

- title: "Chegou o tempo da política"
  authors: "Carolina Botelho"
  outlet: "O Globo"
  date: "2021-05-23"
  type: "impressa"
  url: "https://blogs.oglobo.globo.com/opiniao/post/chegou-o-tempo-da-politica.html"

- title: "Muito do que vai acontecer no 7 de Setembro já aconteceu"
  authors: "Carolina Botelho"
  outlet: "El País"
  date: "2021-09-05"
  type: "impressa"
  url: "https://brasil.elpais.com/brasil/2021-09-05/muito-do-que-vai-acontecer-no-7-de-setembro-ja-aconteceu.html"

- title: "Brasil 'afunda' nas mortes pela covid-19"
  authors: "Carolina Botelho; Paulo Boggio"
  outlet: "El País"
  date: "2021-02-16"
  type: "impressa"
  url: "https://brasil.elpais.com/opiniao/2021-02-16/brasil-afunda-nas-mortes-pela-covid-19-enquanto-o-comandante-fala-e-dai.html"

- title: "Bússola moral para sair da crise"
  authors: "Carolina Botelho; Paulo Boggio"
  outlet: "O Globo"
  date: "2021-03-15"
  type: "impressa"
  url: "https://blogs.oglobo.globo.com/opiniao/post/bussola-moral-para-sair-da-crise.html"

- title: "Bolsonaro uniu todos contra ele"
  authors: "Carolina Botelho"
  outlet: "El País"
  date: "2021-05-22"
  type: "impressa"
  url: "https://brasil.elpais.com/brasil/2021-05-22/carolina-botelho-bolsonaro-uniu-todos-contra-ele-politicos-antes-vistos-como-antagonicos-hoje-conversam.html"

- title: "Apoio nas ruas definirá futuro do confronto de Bolsonaro com Congresso"
  authors: "Argelina Figueiredo"
  outlet: "Folha de São Paulo"
  date: "2020-03-02"
  type: "impressa"
  url: "https://weseek.com.br/viewnews/ViewMateria.html?materiaId=47632554&canalId=486707&clienteId=P9ybjMtObrI="

- title: "Por seu intervencionismo imoderado, STF não terá como evitar confronto"
  authors: "Argelina Figueiredo; Fernando Limongi"
  outlet: "Folha de São Paulo"
  date: "2020-04-30"
  type: "impressa"
  url: "http://doxa.iesp.uerj.br/wp-content/uploads/2020/04/Artigo-Folha-Limongi-Figueiredo.pdf"

- title: "A polarização do vírus"
  authors: "Argelina Figueiredo"
  outlet: "Valor Econômico"
  date: "2020-04-24"
  type: "impressa"
  url: ""

- title: "Roteiro de viagens de Bolsonaro mira obras e auxílio"
  authors: "Carolina Botelho"
  outlet: "O Globo"
  date: "2020-08-30"
  type: "impressa"
  url: "https://oglobo.globo.com/brasil/roteiro-de-viagens-de-bolsonaro-mira-obras-auxilio-24614240?versao=amp"

- title: "Um em cada três candidatos a prefeito no país não tem coligação"
  authors: "Carolina Botelho"
  outlet: "O Globo"
  date: "2020-10-04"
  type: "impressa"
  url: "https://oglobo.globo.com/brasil/eleicoes-2020/um-em-cada-tres-candidatos-prefeito-no-pais-nao-tem-coligacao-com-outro-partido-1-24675913"

- title: "Reforma da Previdência e a articulação política terceirizada"
  authors: "Argelina Figueiredo"
  outlet: "Nexo Jornal"
  date: "2019-06-06"
  type: "impressa"
  url: "https://www.nexojornal.com.br/ensaio/2019/Reforma-da-Previd%C3%AAncia-e-a-articula%C3%A7%C3%A3o-pol%C3%ADtica-terceirizada"

- title: "Desconstruindo Mitos"
  authors: "Argelina Figueiredo"
  outlet: "Pesquisa Fapesp"
  date: "2019-11-01"
  type: "impressa"
  url: ""

- title: "Democracia e Democracias"
  authors: "Argelina Figueiredo"
  outlet: "Valor Econômico"
  date: "2017-02-17"
  type: "impressa"
  url: "http://doxa.iesp.uerj.br/wp-content/uploads/2016/02/Democracia-e-Democracias-_-Valor_17_02_17.pdf"

- title: "Conflito na elite e escândalos de corrupção"
  authors: "Argelina Figueiredo"
  outlet: "Valor Econômico"
  date: "2016-02-15"
  type: "impressa"
  url: "http://doxa.iesp.uerj.br/wp-content/uploads/2016/02/Argelina_artigo-Valor_Conflito-na-elite-e-esc%C3%A2ndalos-de-corrup%C3%A7%C3%A3o.pdf"

- title: "O que deu errado? Não culpemos as instituições"
  authors: "Argelina Figueiredo"
  outlet: "Folha de São Paulo"
  date: "2016-05-13"
  type: "impressa"
  url: "http://www1.folha.uol.com.br/poder/2016/05/1770900-o-que-deu-errado-nao-culpemos-as-instituicoes.shtml"

- title: "A anatomia do PMDB"
  authors: "Natália Maciel"
  outlet: "Valor Econômico"
  date: "2015-05-29"
  type: "impressa"
  url: "http://doxa.iesp.uerj.br/wp-content/uploads/2016/02/A-anatomia-do-PMDB_Valor-Econ%C3%B4mico.pdf"

- title: "The power behind the throne"
  authors: "Natália Maciel"
  outlet: "The Economist"
  date: "2015-07-25"
  type: "impressa"
  url: "http://www.economist.com/news/americas/21659731-junior-partner-government-running-country-power-behind-throne"

- title: "Avaliação de Cabral e voto"
  authors: "Felipe Borba"
  outlet: "O Dia"
  date: "2014-03-21"
  type: "impressa"
  url: "http://odia.ig.com.br/noticia/opiniao/2014-03-21/felipe-borba-avaliacao-de-cabral-e-voto.html"

- title: "Os limites do voto no Rio"
  authors: "Felipe Borba"
  outlet: "O Dia"
  date: "2014-05-16"
  type: "impressa"
  url: "http://odia.ig.com.br/noticia/opiniao/2014-05-16/felipe-borba-os-limites-do-voto-no-rio.html"

- title: "Pela propaganda negativa"
  authors: "Felipe Borba"
  outlet: "O Dia"
  date: "2014-09-27"
  type: "impressa"
  url: "http://odia.ig.com.br/noticia/opiniao/2014-09-27/felipe-borba-pela-propaganda-negativa.html"

- title: "Fora da briga para presidência, estratégia do PMDB é focar em prefeituras"
  authors: "Bertha Maakaroun (entrevistou Natalia Maciel)"
  outlet: "Estado de Minas"
  date: "2012-02-26"
  type: "impressa"
  url: "http://www.em.com.br/app/noticia/politica/2012/02/26/interna_politica,280010/fora-da-briga-para-presidencia-estrategia-do-pmdb-e-focar-em-prefeituras.shtml"

- title: "O povo e as elites nas eleições brasileiras"
  authors: "Argelina Figueiredo"
  outlet: "Valor Econômico"
  date: "2010-10-08"
  type: "impressa"
  url: "http://www.valor.com.br/arquivo/851291/o-povo-e-elites-nas-eleicoes-brasileiras"

# ---- Mídia Virtual ----

- title: "Fraud is not usual, but conspiracy theories are"
  authors: "Flávia Bozza Martins"
  outlet: "Latinoamérica21"
  date: "2023-11-30"
  type: "virtual"
  url: "https://latinoamerica21.com/en/fraud-is-not-usual-but-conspiracy-theories-are/"

- title: "Lula e o desafio de reconstruir o Brasil"
  authors: "Argelina Figueiredo"
  outlet: "DW Made for minds"
  date: "2022-11-04"
  type: "virtual"
  url: "https://www.dw.com/pt-br/lula-e-o-desafio-de-reconstruir-o-brasil/a-63636420?maca=pt-br-Twitter-sharing"

- title: "Distante do povo, Câmara dos Deputados vive dilema"
  authors: "Argelina Figueiredo"
  outlet: "InfoMoney"
  date: "2022-07-08"
  type: "virtual"
  url: "https://www.infomoney.com.br/colunistas/um-brasil/distante-do-povo-camara-dos-deputados-vive-dilema-entre-representacao-e-governabilidade/"

- title: "O Governo Bolsonaro e o Cenário Político Pré-Eleitoral"
  authors: "Argelina Figueiredo; Fernando Guarnieri"
  outlet: "KAS Brasil"
  date: "2022-05-17"
  type: "virtual"
  url: "https://www.kas.de/pt/web/brasilien/einzeltitel/-/content/wahlen-2022-erwartungen-und-perspektiven"

- title: "As eleições importam para quê?"
  authors: "Carolina Botelho"
  outlet: "JOTA"
  date: "2022-03-15"
  type: "virtual"
  url: "https://www.jota.info/opiniao-e-analise/colunas/carolina-botelho/eleicoes-2022-as-eleicoes-importam-para-que-15032022"

- title: "Agora é com vocês, eleitores"
  authors: "Carolina Botelho"
  outlet: "JOTA"
  date: "2022-09-30"
  type: "virtual"
  url: "https://www.jota.info/opiniao-e-analise/colunas/carolina-botelho/agora-e-com-voces-eleitores-30092022"

- title: "Câmara dos Deputados merece mais atenção do que a corrupção no MEC"
  authors: "Carolina Botelho"
  outlet: "JOTA"
  date: "2022-06-23"
  type: "virtual"
  url: "https://www.jota.info/opiniao-e-analise/colunas/carolina-botelho/politica-brasileira-camara-merece-mais-atencao-que-corrupcao-no-mec-23062022"

- title: "Eleições 2022: Qual discurso está mais afinado?"
  authors: "Carolina Botelho"
  outlet: "CNN"
  date: "2022-06-12"
  type: "virtual"
  url: "https://www.youtube.com/watch?v=zkyTYOMeD3g"

- title: "Já é quase agosto e dá para sentir ventos promissores da democracia"
  authors: "Carolina Botelho"
  outlet: "JOTA"
  date: "2022-07-27"
  type: "virtual"
  url: "https://www.jota.info/opiniao-e-analise/colunas/carolina-botelho/ja-e-quase-agosto-e-da-para-sentir-ventos-alvissareiros-da-democracia-27072022?amp"

- title: "O mosaico bolsonarista"
  authors: "Carolina Botelho"
  outlet: "Meio Político"
  date: "2022-10-05"
  type: "virtual"
  url: ""

- title: "Petrobras é a nova fake news de um ano eleitoral desvantajoso"
  authors: "Carolina Botelho"
  outlet: "JOTA"
  date: "2022-05-17"
  type: "virtual"
  url: "https://www.jota.info/opiniao-e-analise/colunas/carolina-botelho/petrobras-e-a-nova-fake-news-de-um-ano-eleitoral-desvantajoso-para-bolsonaro-17052022"

- title: "Por que o Auxílio Brasil não ajuda Bolsonaro nas pesquisas"
  authors: "Carolina Botelho"
  outlet: "Nexo Jornal"
  date: "2022-05-31"
  type: "virtual"
  url: "https://www.nexojornal.com.br/expresso/2022/05/31/Por-que-o-Aux%C3%ADlio-Brasil-n%C3%A3o-ajuda-Bolsonaro-nas-pesquisas?posicao-home-direita=2"

- title: "Teremos muito trabalho pela frente em qualquer cenário após outubro"
  authors: "Carolina Botelho"
  outlet: "JOTA"
  date: "2022-02-15"
  type: "virtual"
  url: "https://www.jota.info/opiniao-e-analise/colunas/carolina-botelho/bolsonarismo-teremos-trabalho-em-qualquer-cenario-apos-outubro-15022022"

- title: "Eleição de 2022 será sobre as consequências da pandemia"
  authors: "Carolina Botelho"
  outlet: "JOTA"
  date: "2022-01-18"
  type: "virtual"
  url: "https://www.jota.info/opiniao-e-analise/colunas/carolina-botelho/eleicao-de-2022-sera-sobre-as-consequencias-da-pandemia-18012022"

- title: "Senado Instala CPI da Pandemia"
  authors: "Argelina Figueiredo"
  outlet: "DW Brasil"
  date: "2021-04-27"
  type: "virtual"
  url: "https://www.dw.com/pt-br/senado-instala-cpi-da-pandemia-e-inicia-investiga%C3%A7%C3%A3o-sobre-governo-bolsonaro/a-57351689"

- title: "Com medo de derrota, Bolsonaro evita apoio explícito"
  authors: "Carolina Botelho"
  outlet: "BR Político / Estadão"
  date: "2020-09-21"
  type: "virtual"
  url: "https://brpolitico.com.br/brp-fique-de-olho/relatorio-21-09/"

- title: "Maia procura candidato que segure governo e fale com a oposição"
  authors: "Carolina Botelho"
  outlet: "BR Político"
  date: "2020-08-03"
  type: "virtual"
  url: "https://brpolitico.com.br/brp-fique-de-olho/relatorio-semanal-3-de-agosto/"

- title: "Por que Bolsonaro recuou e não demitiu Mandetta"
  authors: "Carolina Botelho"
  outlet: "Nexo Jornal"
  date: "2020-04-07"
  type: "virtual"
  url: "https://www.nexojornal.com.br/ensaio/debate/2020/Por-que-Bolsonaro-recuou-e-n%C3%A3o-demitiu-Mandetta"

- title: "Por uma comunidade cívica no Brasil"
  authors: "Carolina Botelho"
  outlet: "Le Monde Diplomatique Brasil"
  date: "2020-05-29"
  type: "virtual"
  url: "https://diplomatique.org.br/por-uma-comunidade-civica-no-brasil/"

- title: "Why Bolsonaro backtracked on firing Mandetta"
  authors: "Carolina Botelho"
  outlet: "CLAS Berkeley"
  date: "2020-04-21"
  type: "virtual"
  url: "https://clasberkeley.wordpress.com/2020/04/21/why-bolosonaro-backtracked-on-firing-mandetta/"

- title: "Aproximação do governo com o Centrão atinge bolsonaristas 'raiz'"
  authors: "Carolina Botelho"
  outlet: "BR Político / Estadão"
  date: "2020-08-05"
  type: "virtual"
  url: "https://brpolitico.com.br/noticias/aproximacao-do-governo-com-o-centrao-atinge-bolsonaristas-raiz/"

- title: "A politização da pandemia"
  authors: "Carolina Botelho"
  outlet: "Coronavírus em Xeque, UFPE"
  date: "2020-08-11"
  type: "virtual"
  url: "https://sites.ufpe.br/rpf/2020/08/11/a-politizacao-da-pandemia/"

- title: "Collectivism and populism in the era of antivax"
  authors: "Carolina Botelho; Paulo Boggio"
  outlet: "Nature Research"
  date: "2020-09-17"
  type: "virtual"
  url: "https://go.nature.com/2RtC21t"

- title: "Siga o líder?"
  authors: "Carolina Botelho"
  outlet: "Le Monde Diplomatique Brasil"
  date: "2020-05-04"
  type: "virtual"
  url: "https://diplomatique.org.br/siga-o-lider/"

- title: "Como bolsonaristas radicais são atingidos pela adesão do centrão"
  authors: "Carolina Botelho"
  outlet: "Nexo Jornal"
  date: "2020-07-27"
  type: "virtual"
  url: "https://www.nexojornal.com.br/expresso/2020/07/27/Como-bolsonaristas-radicais-s%C3%A3o-atingidos-pela-ades%C3%A3o-do-centr%C3%A3o"

- title: "Por que Bolsonaro vem sofrendo derrotas no Senado"
  authors: "Carolina Botelho"
  outlet: "Nexo Jornal"
  date: "2020-08-30"
  type: "virtual"
  url: "https://www.nexojornal.com.br/expresso/2020/08/30/Por-que-Bolsonaro-vem-sofrendo-derrotas-no-Senado"

- title: "Descrença nos políticos e pandemia devem aumentar abstenção"
  authors: "Argelina Figueiredo"
  outlet: "RFI Convida (Podcast)"
  date: "2020-11-10"
  type: "virtual"
  url: "https://www.rfi.fr/br/podcasts/rfi-convida/20201110-descren%C3%A7a-nos-pol%C3%ADticos-e-pandemia-devem-aumentar-absten%C3%A7%C3%A3o-nas-elei%C3%A7%C3%B5es-brasileiras-afirma-especialista"

- title: "Democracia e Independência dos Poderes"
  authors: "Argelina Figueiredo"
  outlet: "TV Cultura-SP: Opinião Nacional"
  date: "2020-03-11"
  type: "virtual"
  url: "https://cultura.uol.com.br/programas/opiniao/videos/4997_opiniao-democracia-e-independencia-dos-poderes-11-03-2020.html"

- title: "Eles são todos iguais?"
  authors: "Cynthia Coutinho"
  outlet: "VOTAAÍ!"
  date: "2020-01-01"
  type: "virtual"
  url: "http://votaai.com.br/eles-sao-todos-iguais/"

- title: "Programas de Governo entre a Política e a Ciência Política"
  authors: "Nara Salles"
  outlet: "Horizontes ao Sul"
  date: "2020-11-13"
  type: "virtual"
  url: "https://www.horizontesaosul.com/single-post/2020/11/13/PROGRAMAS-DE-GOVERNO-ENTRE-A-POLITICA-E-A-CIENCIA-POLITICA-UM-DESABAFO"

- title: "As propostas para a saúde e a pandemia como um fator contextual"
  authors: "Carolini Silva"
  outlet: "VOTAAÍ!"
  date: "2020-01-01"
  type: "virtual"
  url: "http://votaai.com.br/as-propostas-para-a-saude-e-a-pandemia-como-um-fator-contextual/"

- title: "Filiações partidárias no Brasil: mais do mesmo?"
  authors: "Carolina Botelho"
  outlet: "Exame"
  date: "2018-04-19"
  type: "virtual"
  url: "https://exame.abril.com.br/blog/opiniao/filiacoes-partidarias-no-brasil-mais-do-mesmo/"

- title: "Reforma da Previdência: as lições de FHC e Lula"
  authors: "Carolina Botelho"
  outlet: "Exame"
  date: "2017-11-23"
  type: "virtual"
  url: "https://exame.com/economia/reforma-da-previdencia-as-licoes-de-fhc-e-lula/"

- title: "Como a percepção da corrupção dificulta a adesão à reforma da Previdência"
  authors: "Flávia Bozza; Luciana Veiga"
  outlet: "O Globo Online (Na base dos dados)"
  date: "2017-05-26"
  type: "virtual"
  url: "http://blogs.oglobo.globo.com/na-base-dos-dados/post/como-percepcao-da-corrupcao-dificulta-adesao-reforma-da-previdencia.html"

- title: "Dilma está vivendo o mesmo que FHC antes"
  authors: "Argelina Figueiredo"
  outlet: "AVOL"
  date: "2015-03-15"
  type: "virtual"
  url: "http://www.antonioviana.com.br/2009/site/ver_noticia.php?id=110318"

- title: "Quem avança primeiro, Dilma ou os apoiadores do impeachment?"
  authors: "Argelina Figueiredo"
  outlet: "Central Gazeta de Notícias"
  date: "2015-02-09"
  type: "virtual"
  url: "http://jornalggn.com.br/tag/blogs/argelina-figueiredo"

- title: "A Ditadura interna do PMDB ou a Era Temer?"
  authors: "Natalia Maciel"
  outlet: "Escuta"
  date: "2015-05-04"
  type: "virtual"
  url: "https://revistaescuta.wordpress.com/2016/05/04/escuta-especial-conjuntura-a-ditadura-interna-do-pmdb-ou-a-era-temer/"

# ---- Audiovisual ----

- title: "Arquitetos do Poder"
  authors: "Marcus Figueiredo (coord.); Vicente Ferraz; Alessandra Aldé (direção)"
  outlet: "Urca Filmes"
  date: "2010-01-01"
  type: "audiovisual"
  url: ""

- title: "Caminhamos rumo ao impasse? #98"
  authors: "Argelina Figueiredo"
  outlet: "Fora da Política Não há Salvação"
  date: "2021-01-01"
  type: "audiovisual"
  url: ""

- title: "A Ciência Política e as Crises Brasileiras: Instituições e Políticas"
  authors: "Argelina Figueiredo"
  outlet: "ANPOCS (44º Congresso)"
  date: "2020-01-01"
  type: "audiovisual"
  url: ""

- title: "Democracia busca equilíbrio entre representação e governabilidade"
  authors: "Argelina Figueiredo"
  outlet: "UM BRASIL (Humberto Dantas)"
  date: "2022-01-01"
  type: "audiovisual"
  url: ""

- title: "O Brasil votou, primeiro turno"
  authors: "Argelina Figueiredo"
  outlet: "KAS – Brasil"
  date: "2022-10-02"
  type: "audiovisual"
  url: ""

- title: "Bate-papo: 50 anos do golpe militar"
  authors: "Argelina Figueiredo"
  outlet: "Rede EBC (João Vicente Goulart)"
  date: "2014-01-01"
  type: "audiovisual"
  url: ""
```

---

## Assets

Tabela de todos os assets identificados no WordPress, com destino sugerido no novo site.

| URL original | Descrição | Destino no novo site |
|-------------|-----------|---------------------|
| https://www.lab-doxa.org.br/wp-content/uploads/2022/10/Foto-Argelina_nova.jpg | Foto Argelina Cheibub Figueiredo | `static/img/team/argelina-figueiredo.jpg` |
| https://www.lab-doxa.org.br/wp-content/uploads/2023/07/Equipe-DOXA-Fernando-Meireles.jpg | Foto Fernando Meireles | `static/img/team/fernando-meireles.jpg` |
| https://www.lab-doxa.org.br/wp-content/uploads/2023/07/Equipe-DOXA-Bruno-Schaefer.jpg | Foto Bruno Schaefer | `static/img/team/bruno-schaefer.jpg` |
| https://www.lab-doxa.org.br/wp-content/uploads/2022/06/Fernando-G.jpg | Foto Fernando Guarnieri | `static/img/team/fernando-guarnieri.jpg` |
| https://www.lab-doxa.org.br/wp-content/uploads/2022/06/Flavia.jpg | Foto Flávia Bozza Martins | `static/img/team/flavia-bozza.jpg` |
| https://www.lab-doxa.org.br/wp-content/uploads/2022/06/Carolini-300x225-1.jpg | Foto Carolini Silva | `static/img/team/carolini-silva.jpg` |
| https://www.lab-doxa.org.br/wp-content/uploads/2024/09/Maria-Dominguez.jpeg | Foto Maria Dominguez | `static/img/team/maria-dominguez.jpg` |
| https://www.lab-doxa.org.br/wp-content/uploads/2024/09/Matteo-de-Barros-Manes.jpg | Foto Matteo Manes | `static/img/team/matteo-manes.jpg` |
| https://www.lab-doxa.org.br/wp-content/uploads/2024/09/Karime-Lima.jpeg | Foto Karime Lima | `static/img/team/karime-lima.jpg` |
| https://www.lab-doxa.org.br/wp-content/uploads/2022/06/Larissa-300x200-1.jpg | Foto Larissa Mendes | `static/img/team/larissa-mendes.jpg` |
| https://www.lab-doxa.org.br/wp-content/uploads/2022/06/Carolina-Botelho.jpg | Foto Carolina Botelho | `static/img/team/carolina-botelho.jpg` |
| https://www.lab-doxa.org.br/wp-content/uploads/2022/06/Hellen.jpg | Foto Hellen Guicheney | `static/img/team/hellen-guicheney.jpg` |
| https://www.lab-doxa.org.br/wp-content/uploads/2022/06/Lattes1.jpg | Foto Nara Salles | `static/img/team/nara-salles.jpg` |
| https://www.lab-doxa.org.br/wp-content/uploads/2022/06/Natalia.jpg | Foto Natalia Maciel | `static/img/team/natalia-maciel.jpg` |
| https://www.lab-doxa.org.br/wp-content/uploads/2022/06/Thiago.jpg | Foto Thiago Moreira | `static/img/team/thiago-moreira.jpg` |
| https://www.lab-doxa.org.br/wp-content/uploads/2022/12/FIGUEIREDO_A-DECISAO-DO-VOTO_CARTAZ-576x1024.jpg | Cartaz do livro "A Decisão do Voto" | `static/img/eventos/decisao-do-voto.jpg` |
| https://www.lab-doxa.org.br/wp-content/uploads/2022/08/Seminario-25-anos-DOXA-1024x576.jpg | Banner do Seminário 25 anos DOXA | `static/img/eventos/seminario-25anos.jpg` |
| https://www.lab-doxa.org.br/wp-content/uploads/2022/11/Doxa_20_parae-mail_azul-1024x682.jpg | Banner DOXA 20 anos | `static/img/eventos/doxa-20anos.jpg` |
| https://www.lab-doxa.org.br/wp-content/uploads/2022/12/CARTAZ_Seminario-Marcus-Figueiredo-724x1024.jpg | Cartaz Seminário Marcus Figueiredo 2014 | `static/img/eventos/seminario-marcus-figueiredo.jpg` |
| https://www.lab-doxa.org.br/wp-content/uploads/2022/09/marcusfigueiredo_destaque-1024x615.jpg | Foto Marcus Figueiredo (destaque) | `static/img/eventos/marcus-figueiredo.jpg` |
| https://www.lab-doxa.org.br/wp-content/uploads/2022/11/Solicitacao-de-Material-do-Acervo.docx | Formulário de solicitação de material do acervo | `static/files/Solicitacao-de-Material-do-Acervo.docx` |
| Logos parceiros (CAPES, CNPq, FAPERJ, FINEP, IBOPE, IESP-UERJ, Vox, UERJ) | Logos dos financiadores/parceiros | `static/img/parceiros/[nome].png` — URLs não identificadas; buscar na pasta wp-content |

**Nota sobre PDFs de Análises e mapas:** Há dezenas de arquivos PDF em `https://www.lab-doxa.org.br/wp-content/uploads/2022/10/` e `https://www.lab-doxa.org.br/wp-content/uploads/2022/11/`. Todos os links estão mapeados nas seções acima. Esses arquivos devem ser baixados em bulk e armazenados em `static/files/analises/` e `static/files/mapas/` respectivamente.

---

## Lacunas

| # | Descrição do problema | Sugestão de tratamento |
|---|----------------------|------------------------|
| 1 | **YouTube ID do vídeo principal da homepage** — o campo `featured_video.youtube_id` em `homepage.yaml` tem valor placeholder. O canal DOXA é `UCkcuDdIEuQ9YqOjHsp4-EHQ` mas não foi identificado qual vídeo específico deve ser o destaque. | Acessar https://www.youtube.com/channel/UCkcuDdIEuQ9YqOjHsp4-EHQ e escolher o vídeo institucional mais recente ou o do seminário de 25 anos. |
| 2 | **URLs dos dashboards Power BI (eleições 2024)** — os links reais de Rio de Janeiro e São Paulo não estavam disponíveis na extração. | Solicitar ao responsável pelo laboratório os links diretos dos dashboards do Power BI. |
| 3 | **Links de Lattes de todos os membros da equipe** — a página Institucional não exibe os links do Currículo Lattes de nenhum membro. | Preencher manualmente consultando a plataforma Lattes (lattes.cnpq.br) com o nome de cada pesquisador. |
| 4 | **E-mails individuais dos membros da equipe** — não expostos na página. | Deixar campo em branco ou usar apenas o e-mail geral do laboratório (acervo-doxa@iesp.uerj.br). |
| 5 | **HGPE 1998 — arquivo ausente** — a análise do HGPE de 1998 (Luciana Veiga; Raul Magalhães) é citada mas não tem link de download disponível. | Contatar os autores ou buscar no acervo físico do DOXA. |
| 6 | **Tabela de OESP 2002** — o arquivo de tabela para O Estado de S.Paulo nas eleições de 2002 não aparece listado (apenas o gráfico). | Verificar se o arquivo existe no servidor WordPress: padrão seria `027-2002-tabelas-cobertura-jornalistica-OESP.pdf`. |
| 7 | **Bancos de dados — Programas de Governo 2020** — a página `/bancos-de-dados/` menciona bancos de programas de governo de candidatos a prefeito (RJ e capitais), mas os links diretos não foram identificados. | Verificar se há subpáginas dedicadas ou se o acesso é via download direto a partir do WordPress. |
| 8 | **Acervo audiovisual — sem embed de vídeo** — a página `/acervo/` não tem YouTube embutido; os vídeos ficam no Google Drive. | Considerar migrar vídeos de amostra para o YouTube DOXA e embeder na página do acervo. |
| 9 | **Logos de parceiros — URLs não identificadas** — as imagens dos logos de CAPES, CNPq, FAPERJ, FINEP, IBOPE, Vox na homepage não tiveram suas URLs extraídas. | Acessar o HTML bruto da homepage ou o painel WordPress para localizar os arquivos em wp-content/uploads. |
| 10 | **URLs de aparições audiovisuais sem link** — seis itens de mídia audiovisual não têm URL (documentário "Arquitetos do Poder", podcasts, entrevistas em TV). | Buscar no YouTube, ANPOCS, RFI e outros veículos; registrar links quando encontrados. |
| 11 | **Pesquisas em andamento** — a página `/pagina-pesquisas/` exibe apenas teses concluídas. Não há listagem de projetos em andamento acessível publicamente. | Solicitar ao laboratório a lista atualizada de pesquisas em andamento para preencher `data/pesquisas.yaml`. |
| 12 | **data/acervo.yaml** — o schema atual usa campos de vídeos individuais (candidato, partido, cargo, região). O acervo real tem centenas de itens acessíveis via Google Sheets. Manter a exportação em bulk via planilha é a solução mais viável; o arquivo YAML provavelmente não deve listar itens individualmente. | Decidir se o site exibirá um catálogo filtrado (exportação parcial do Google Sheets) ou apenas um link para a planilha/formulário de solicitação. |

---

## Links externos

Todos os links encontrados nas páginas do WordPress que apontam para fora de `lab-doxa.org.br`:

| URL | Página onde aparece | Contexto |
|-----|--------------------|-|
| https://votaai.cesop.unicamp.br | Homepage, Análises | Plataforma Vota Aí |
| https://www.youtube.com/channel/UCkcuDdIEuQ9YqOjHsp4-EHQ | Homepage, Acervo | Canal YouTube DOXA |
| https://www.youtube.com/@votaai6247/videos | Análises | Canal YouTube Vota Aí |
| https://www.youtube.com/watch?v=zkyTYOMeD3g | Na Mídia | Vídeo CNN com Carolina Botelho |
| https://docs.google.com/spreadsheets/d/1b_OFFW0fJS3B0DFvfeoa6y8l9YG6JmFP/edit | Acervo | Catálogo do acervo audiovisual |
| https://docs.google.com/document/d/15D7Ccv0A4fiUiOCtammle_8xdUJ977kkTwx5tWTCSI8/edit?usp=drivesdk | Eventos | Livro "A Decisão do Voto" (Google Docs) |
| https://www.bdtd.uerj.br:8443/bitstream/1/19482/2/ | Pesquisas | Tese Mariani Holanda 2023 |
| https://www.bdtd.uerj.br:8443/bitstream/1/17917/2/ | Pesquisas | Tese Pedro Costa 2022 |
| https://www.bdtd.uerj.br:8443/bitstream/1/17266/2/ | Pesquisas | Tese Ariel Torres 2020 |
| https://www.bdtd.uerj.br:8443/bitstream/1/12386/1/ | Pesquisas | Tese Nara Salles 2019 |
| https://www.bdtd.uerj.br:8443/bitstream/1/12486/1/ | Pesquisas | Tese Márcia Cruz 2018 |
| https://www.bdtd.uerj.br:8443/bitstream/1/12478/1/ | Pesquisas | Tese André Carneiro 2018 |
| https://www.scielo.br/j/nec/a/KBxnHhZWWCPJ5zgJwKTTzSK/ | Publicações | Artigo Limongi/Figueiredo 2017 |
| https://www.fundacionmgimenezabad.es/sites/default/files/ | Publicações | Capítulo Figueiredo et al. 2011 |
| https://valor.globo.com/politica/coluna/estimativas-de-margem-de-erro-no-brasil.ghtml | Na Mídia | Artigo Fernando Meireles 2022 |
| https://valor.globo.com/politica/noticia/2021/02/22/ | Na Mídia | Argelina Figueiredo — Valor Econômico 2021 |
| https://politica.estadao.com.br/noticias/geral,cpi-pode-chegar-a-bolsonaro | Na Mídia | Argelina Figueiredo — Estadão 2021 |
| https://www1.folha.uol.com.br/poder/2021/04/ | Na Mídia | Argelina Figueiredo — Folha 2021 |
| https://brasil.elpais.com/ | Na Mídia | Vários artigos de Carolina Botelho |
| https://blogs.oglobo.globo.com/opiniao/ | Na Mídia | Artigos Carolina Botelho 2021 |
| https://www.dw.com/pt-br/ | Na Mídia | Argelina Figueiredo — DW Brasil 2021/2022 |
| https://www.infomoney.com.br/ | Na Mídia | Argelina Figueiredo 2022 |
| https://www.kas.de/pt/web/brasilien/ | Na Mídia | Figueiredo/Guarnieri 2022 |
| https://www.jota.info/ | Na Mídia | Vários artigos Carolina Botelho 2022 |
| https://www.nexojornal.com.br/ | Na Mídia | Vários (Figueiredo, Botelho, Maciel) |
| https://www.nexojornal.com.br/ensaio/2019/ | Na Mídia | Figueiredo — Reforma Previdência 2019 |
| https://latinoamerica21.com/en/ | Na Mídia | Flávia Bozza 2023 |
| https://www.rfi.fr/br/podcasts/ | Na Mídia | Argelina Figueiredo 2020 |
| https://cultura.uol.com.br/ | Na Mídia | Argelina Figueiredo — TV Cultura 2020 |
| https://brpolitico.com.br/ | Na Mídia | Carolina Botelho 2020 |
| https://diplomatique.org.br/ | Na Mídia | Carolina Botelho 2020 |
| https://sites.ufpe.br/rpf/ | Na Mídia | Carolina Botelho 2020 |
| https://go.nature.com/2RtC21t | Na Mídia | Botelho/Boggio — Nature Research 2020 |
| https://clasberkeley.wordpress.com/ | Na Mídia | Carolina Botelho 2020 |
| https://www.horizontesaosul.com/ | Na Mídia | Nara Salles 2020 |
| http://votaai.com.br/ | Na Mídia | VOTAAÍ! (Cynthia Coutinho, Carolini Silva) |
| https://exame.com/ | Na Mídia | Carolina Botelho 2017/2018 |
| http://blogs.oglobo.globo.com/na-base-dos-dados/ | Na Mídia | Flávia Bozza / Luciana Veiga 2017 |
| https://revistaescuta.wordpress.com/ | Na Mídia | Natalia Maciel 2015 |
| http://doxa.iesp.uerj.br/ | Na Mídia | URL antiga do DOXA (redirecionamento) |
| https://app.powerbi.com/ | Homepage | Dashboards eleições 2024 (URLs parciais) |
| http://www.economist.com/news/americas/21659731 | Na Mídia | Natália Maciel — The Economist 2015 |
