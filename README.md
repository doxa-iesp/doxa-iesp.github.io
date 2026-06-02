# DOXA — Site do Laboratório

Site estático do [DOXA — Laboratório de Estudos Eleitorais, de Comunicação Política e Opinião Pública](https://www.lab-doxa.org.br) (IESP-UERJ), construído com [Hugo](https://gohugo.io/) e publicado via GitHub Pages.

**URL:** https://felipelamarca.com/DOXA/ (temporária — a URL definitiva será www.lab-doxa.org.br)

---

## Pré-requisitos

- [Hugo](https://gohugo.io/installation/) v0.162.1+ (extended)
- Git

## Rodar localmente

```bash
git clone https://github.com/felipelmc/DOXA.git
cd DOXA
hugo server
```

O site ficará disponível em `http://localhost:1313/DOXA/`.

## Deploy

Qualquer push para o branch `main` dispara o GitHub Actions automaticamente. O site atualiza em ~2 minutos.

---

## Como atualizar o conteúdo

Todos os dados do site ficam em arquivos YAML na pasta `data/`. Edite o arquivo correspondente e faça push para `main`.

### Adicionar membro à equipe

1. Abra `data/team.yaml`
2. Adicione um bloco no final da categoria correta:
   ```yaml
   - name: "Nome Completo"
     role: "Cargo"
     category: "pesquisadores"   # coordenacao | pesquisadores | pos-doutorando | aluno | assistente | associado
     lattes: "https://lattes.cnpq.br/..."
     email: "email@iesp.uerj.br"
     photo: "/img/team/nome-sobrenome.jpg"
   ```
3. Salve a foto em `static/img/team/nome-sobrenome.jpg`
4. Push para `main`

### Publicar nova publicação acadêmica

1. Abra `data/publications.yaml`
2. Adicione o bloco na seção correta (Livros, Capítulos, Artigos ou Outras produções):
   ```yaml
   - title: "Título do Artigo"
     authors: "Sobrenome, Nome"
     year: 2025
     type: "artigo"              # livro | capitulo | artigo | outros
     journal: "Nome da Revista"
     url: "https://..."
   ```
3. Push para `main`

### Adicionar evento

1. Abra `data/events.yaml`
2. Adicione no topo do arquivo (mais recente primeiro):
   ```yaml
   - title: "Nome do Evento"
     date: "2025-06-15"
     description: "Descrição."
     url: "https://..."
   ```
3. Push para `main`

### Adicionar notícia em "Na Mídia"

1. Abra `data/media.yaml`
2. Adicione no topo da seção correta (Impressa, Virtual ou Audiovisual):
   ```yaml
   - title: "Título da Matéria"
     authors: "Pesquisador DOXA"
     outlet: "Veículo"
     date: "2025-06-15"
     type: "virtual"             # impressa | virtual | audiovisual
     url: "https://..."
   ```
3. Push para `main`

### Adicionar seminário

1. Abra `data/seminars.yaml`
2. Adicione no topo do arquivo:
   ```yaml
   - title: "Título da Apresentação"
     presenter: "Nome do Palestrante"
     institution: "Instituição"
     date: "2025-06-15"
     year: 2025
   ```
3. Push para `main`

---

## Estrutura do repositório

```
├── config.yaml           # Configuração global (baseURL, menu, params)
├── content/              # Conteúdo editorial em Markdown
├── data/                 # Dados estruturados em YAML (equipe, publicações, etc.)
│   ├── team.yaml
│   ├── publications.yaml
│   ├── analyses.yaml
│   ├── discussions.yaml
│   ├── pesquisas.yaml
│   ├── events.yaml
│   ├── seminars.yaml
│   ├── media.yaml
│   ├── acervo.yaml
│   └── homepage.yaml
├── layouts/              # Templates HTML (Hugo)
├── static/               # Assets estáticos (CSS, JS, imagens)
│   ├── css/main.css
│   ├── js/
│   └── img/
│       ├── team/         # Fotos da equipe
│       └── logo-doxa.svg
└── .github/workflows/    # CI/CD (GitHub Actions)
    └── deploy.yml
```

## Dados pendentes de preenchimento

- Links de Lattes de cada pesquisador (`data/team.yaml`)
- E-mails individuais dos membros (`data/team.yaml`)
- ID do YouTube para o vídeo em destaque (`data/homepage.yaml` → `featured_video.youtube_id`)
- URLs dos dashboards Power BI (`data/homepage.yaml` → `dashboards.items`)
- Pesquisas em andamento (`data/pesquisas.yaml`)
