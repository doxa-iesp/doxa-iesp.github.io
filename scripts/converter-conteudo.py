#!/usr/bin/env python3
"""Agente A — converte extracao/dados/ nas content collections do Astro.

Idempotente e reproduzível: apaga e regenera src/content/ e src/data/.
Nada é inventado; campos ausentes na fonte são omitidos.
"""
import csv, json, os, re, shutil, subprocess, sys, unicodedata
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parent.parent
FONTE = RAIZ / "extracao" / "dados"
CONTENT = RAIZ / "src" / "content"
DATA = RAIZ / "src" / "data"
PUBLIC = RAIZ / "public"


def slug(texto: str) -> str:
    s = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


def ler(nome, sub=None):
    d = yaml.safe_load((FONTE / nome).read_text(encoding="utf-8"))
    return d[sub] if sub else d


def yml(dados, cabecalho=""):
    corpo = yaml.safe_dump(dados, allow_unicode=True, sort_keys=False, width=100, default_flow_style=False)
    return (cabecalho + "\n" if cabecalho else "") + corpo


def limpo(d: dict) -> dict:
    """Remove chaves vazias — campo ausente é omitido, não preenchido com ''."""
    return {k: v for k, v in d.items() if v not in ("", None, [], {})}


CAB = "# Gerado por scripts/converter-conteudo.py a partir de extracao/dados/.\n# Pode ser editado à mão: o build valida o schema (src/content.config.ts).\n"

# ---------------------------------------------------------------- equipe

FOTOS = {p.stem: p.name for p in (PUBLIC / "img" / "equipe").glob("*")}


def foto_de(nome: str):
    partes = slug(nome).split("-")
    alvo = f"{partes[0]}-{partes[-1]}"
    if alvo in FOTOS:
        return f"/img/equipe/{FOTOS[alvo]}"
    for stem, arq in FOTOS.items():
        if stem.startswith(partes[0]):
            return f"/img/equipe/{arq}"
    return None


# Padronização editorial de cargos. O site antigo escrevia "Coordenadora" para a
# Argelina e "Coordenação" para o Fernando Meireles — um nomeia a pessoa, o outro a
# função, lado a lado no mesmo grupo. A coordenação pediu um rótulo só. Como o texto
# de origem não está errado (era isso mesmo que o WordPress dizia), a correção mora
# aqui e não em extracao/, que continua sendo registro fiel — mesma ideia do
# dicionário OVERRIDES usado em paginas().
CARGOS = {
    "Coordenadora": "Coordenação",
}


def equipe():
    membros = ler("equipe.yaml")
    # Felipe Lamarca não está no site antigo; veio do data/team.yaml do Hugo (adicionado
    # deliberadamente num commit anterior). Preservado para não regredir o repositório.
    membros.append({"name": "Felipe Lamarca", "role": "Mestrando", "category": "aluno",
                    "lattes": "", "email": "", "site": "https://felipelamarca.com", "photo": ""})

    lattes = {slug(x["name"].split(",")[0]): x["url"]
              for x in ler("publicacoes-academicas.yaml", "lattes")}

    destino = CONTENT / "equipe"
    shutil.rmtree(destino, ignore_errors=True)
    destino.mkdir(parents=True)

    ordem_cat = ["coordenacao", "pesquisadores", "pos-doutorando", "aluno", "assistente", "associado"]
    n = 0
    for m in membros:
        sobrenome = slug(m["name"]).split("-")[-1]
        reg = limpo({
            "nome": m["name"],
            "cargo": CARGOS.get(m["role"], m["role"]),
            "categoria": m["category"],
            "foto": foto_de(m["name"]),
            "lattes": lattes.get(sobrenome, ""),
            "email": m.get("email", ""),
            "site": m.get("site", ""),
            "ordem": ordem_cat.index(m["category"]) * 100,
        })
        (destino / f"{slug(m['name'])}.yaml").write_text(
            yml(reg, f"# {m['name']} — equipe do DOXA"), encoding="utf-8")
        n += 1
    com_lattes = sum(1 for m in membros if lattes.get(slug(m["name"]).split("-")[-1]))
    print(f"  equipe/            {n} arquivos ({com_lattes} com Lattes)")


# ---------------------------------------------------------------- páginas

def paginas():
    destino = CONTENT / "paginas"
    shutil.rmtree(destino, ignore_errors=True)
    destino.mkdir(parents=True)

    def corpo(nome):
        txt = (FONTE / "paginas" / nome).read_text(encoding="utf-8")
        partes = txt.split("---", 2)
        return partes[2].strip() if len(partes) > 2 else txt.strip()

    # Seção 4.1: a home passa a ser a apresentação institucional do grupo.
    inst = corpo("institucional.md")
    # O <h1> da home já nomeia o laboratório; um "## Sobre o DOXA" logo abaixo é redundante.
    inst = re.sub(r"^##\s*Sobre o DOXA\s*\n+", "", inst)
    (destino / "home.md").write_text(
        f'---\ntitulo: "DOXA"\nsubtitulo: "Laboratório de Estudos Eleitorais, de Comunicação Política e Opinião Pública"\n'
        f'descricao: "Laboratório de pesquisa do IESP-UERJ dedicado ao estudo dos processos eleitorais, '
        f'da comunicação política e da opinião pública no Brasil."\n---\n\n{inst}\n', encoding="utf-8")

    # No WordPress, cada página abria com um <h2> repetindo o próprio nome — que aqui vira o <h1>
    # do PageHero. E em três páginas a prosa repete itens que agora vêm das coleções.
    #   sem_primeiro_titulo: remove o "## <nome da página>" inicial
    #   so_introducao:       corta no próximo "##" (o resto duplica os cards da coleção)
    AJUSTES = {
        "bancos-de-dados.md": dict(sem_primeiro_titulo=True, so_introducao=True),
        "publicacoes.md": dict(sem_primeiro_titulo=True, so_introducao=True),
        "eventos.md": dict(sem_primeiro_titulo=True, so_introducao=True),
        "na-midia.md": dict(sem_primeiro_titulo=True),
        "pagina-pesquisas.md": dict(sem_primeiro_titulo=True),
        "seminarios.md": dict(sem_primeiro_titulo=True),
        # A página antiga trazia uma TABELA de partidos com links para cada PDF. Ao extrair a
        # prosa, os links somem e sobram só as siglas separadas por barras — lixo. Os 273
        # mapas já vêm estruturados de mapas-votacao.yaml, então basta a introdução.
        "mapas-de-votacao.md": dict(sem_primeiro_titulo=True, so_introducao=True),
        "textos-para-discussao-2.md": dict(sem_primeiro_titulo=True),
    }

    def ajustar(texto, arq):
        cfg = AJUSTES.get(arq, {})
        if cfg.get("sem_primeiro_titulo"):
            texto = re.sub(r"\A##\s+.*\n+", "", texto)
        if cfg.get("so_introducao"):
            texto = re.split(r"^##\s+", texto, maxsplit=1, flags=re.M)[0]
        return texto.strip()

    # Textos que o site antigo não tinha (ou tinha errado). São editoriais, não
    # extraídos — por isso vivem aqui, e não em extracao/, que é registro histórico.
    OVERRIDES = {
        # O texto institucional integral vive na home; aqui fica só um contexto curto.
        "institucional.md": (
            "O DOXA reúne pesquisadores, pós-doutorandos, alunos de pós-graduação e "
            "assistentes de pesquisa dedicados ao estudo dos processos eleitorais, da "
            "comunicação política e da opinião pública no Brasil."
        ),
        # No WordPress esta página trazia, por engano, o texto genérico de "Publicações" —
        # falava dos dois tipos de publicação, e não de working papers. O erro está fiel em
        # extracao/dados/paginas/textos-para-discussao-2.md; aqui entra o texto correto.
        "textos-para-discussao-2.md": (
            "Os Textos para Discussão do DOXA são *working papers*: pesquisas em desenvolvimento, "
            "publicadas antes da versão definitiva para que sejam avaliadas e debatidas pela "
            "comunidade acadêmica. Todos podem ser baixados livremente."
        ),
        # No WordPress a busca do acervo estava "ainda em construção" e nunca foi atualizada — a
        # busca funciona no site novo (filtros por candidato, ano, cargo, região e partido), então
        # manter a frase da origem publicaria uma informação falsa. O texto fiel ao site antigo
        # está em extracao/dados/paginas/acervo.md; aqui entra a versão corrigida.
        "acervo.md": (
            "## Catálogo Audiovisual\n\n"
            "O acervo audiovisual do Doxa pode ser consultado de duas formas. A primeira, por meio "
            "da busca abaixo, com filtros por candidato, ano, cargo, região e partido. Nela podem "
            "ser encontrados de imediato os vídeos veiculados nos horários gratuitos de propaganda "
            "eleitoral (HGPE) nas campanhas dos candidatos a presidente, de 1989 a 2022, e para "
            "governador, de 1994 a 2014. Os resultados das buscas aparecem de acordo com as siglas "
            "partidárias ou dos partidos das coligações que se formaram em apoio aos candidatos.\n\n"
            "A segunda forma é por meio de consulta ao catálogo do Doxa que contém a listagem "
            "completa do acervo, incluindo material que vai além dos vídeos de HGPE, contido na "
            "pesquisa. Nele há vídeos de debates, entrevistas com candidatos, spots eleitorais e "
            "partidários, telejornais e de propagandas partidárias não vinculadas especificamente "
            "nos períodos eleitorais.\n\n"
            "O acesso ao catálogo é no link abaixo e para ver esses vídeos é necessário que nos "
            "envie um email ( acervo-doxa@iesp.uerj.br ) com o formulário abaixo especificando a "
            "solicitação de material desejado."
        ),
    }

    mapa = {
        "institucional.md": ("Institucional", "A equipe do DOXA."),
        "acervo.md": ("Acervo Audiovisual", "O maior arquivo de propaganda eleitoral do Brasil."),
        "mapas-de-votacao.md": ("Mapas de Votação", "Distribuição da votação por bairro e município."),
        "bancos-de-dados.md": ("Bancos de Dados", "Bases abertas produzidas pelo DOXA."),
        "pagina-pesquisas.md": ("Pesquisas do DOXA", "Teses, dissertações e projetos do laboratório."),
        "publicacoes.md": ("Produção", "Pesquisas, publicações e análises do DOXA."),
        "na-midia.md": ("Na Mídia", "Aparições do DOXA na imprensa."),
        "seminarios.md": ("Seminários", "Seminários promovidos pelo laboratório."),
        "eventos.md": ("Eventos", "Eventos do DOXA."),
        "textos-para-discussao-2.md": ("Textos para Discussão", "Working papers do DOXA."),
    }
    # nome de origem -> nome do arquivo gerado
    saida = {
        "textos-para-discussao-2.md": "textos-para-discussao.md",
        "pagina-pesquisas.md": "pesquisas.md",
        # "Publicações" virou a capa da seção "Produção", que reúne pesquisas + publicações.
        "publicacoes.md": "producao.md",
    }
    n = 1
    for arq, (titulo, desc) in mapa.items():
        if not (FONTE / "paginas" / arq).exists():
            continue
        texto = OVERRIDES.get(arq) or ajustar(corpo(arq), arq)
        nome = saida.get(arq, arq)
        (destino / nome).write_text(
            f'---\ntitulo: "{titulo}"\ndescricao: "{desc}"\n---\n\n{texto}\n', encoding="utf-8")
        n += 1

    # A prosa de /pesquisa-covid/ migrou para o projeto homônimo (src/content/projetos/),
    # por isso não é mais gerada como página.
    print(f"  paginas/           {n} arquivos (home.md = apresentação institucional)")


# ---------------------------------------------------------------- projetos

def projetos():
    """Projetos do laboratório. São editoriais (não vieram de uma listagem do
    WordPress), então moram em extracao/dados/projetos/ e são copiados verbatim."""
    origem = FONTE / "projetos"
    destino = CONTENT / "projetos"
    shutil.rmtree(destino, ignore_errors=True)
    destino.mkdir(parents=True)
    n = 0
    for f in sorted(origem.glob("*.md")):
        shutil.copy(f, destino / f.name)
        n += 1
    print(f"  projetos/          {n} arquivos")


# ---------------------------------------------------------------- eventos

def eventos():
    destino = CONTENT / "eventos"
    shutil.rmtree(destino, ignore_errors=True)
    destino.mkdir(parents=True)
    img_dir = PUBLIC / "img" / "eventos"
    img_dir.mkdir(parents=True, exist_ok=True)

    evs = ler("eventos-seminarios.yaml")["eventos"]
    for e in evs:
        s = slug(e["title"])[:50]
        imagem = ""
        if e.get("image"):
            ext = os.path.splitext(e["image"])[1].split("?")[0] or ".jpg"
            destino_img = img_dir / f"{s}{ext}"
            if not destino_img.exists():
                subprocess.run(["curl", "-sSL", "--max-time", "60", "-o", str(destino_img), e["image"]],
                               check=False)
            if destino_img.exists() and destino_img.stat().st_size > 1000:
                imagem = f"/img/eventos/{destino_img.name}"

        fm = limpo({"titulo": e["title"], "data": e["date"], "descricao": e.get("description", ""),
                    "imagem": imagem, "url": e.get("url", ""), "anexos": e.get("attachments", [])})
        frente = yaml.safe_dump(fm, allow_unicode=True, sort_keys=False, default_flow_style=False)
        (destino / f"{s}.md").write_text(f"---\n{frente}---\n\n{e.get('description','')}\n", encoding="utf-8")
    print(f"  eventos/           {len(evs)} arquivos")


# ---------------------------------------------------------------- listas

def listas():
    DATA.mkdir(parents=True, exist_ok=True)

    pubs = [limpo({"titulo": p["title"], "autores": p["authors"],
                   "ano": p.get("year") or "", "tipo": p["type"],
                   "editora": p.get("publisher", ""), "revista": p.get("journal", ""),
                   "paginas": p.get("pages", ""), "url": p.get("url", "")})
            for p in ler("publicacoes-academicas.yaml", "publications")]
    (DATA / "publicacoes.yaml").write_text(yml(pubs, CAB), encoding="utf-8")

    ans = [limpo({"titulo": a["title"], "ciclo": str(a["cycle"]), "periodo": a.get("period", ""),
                  "descricao": a.get("description", ""),
                  "arquivos": [{"rotulo": f["label"], "url": f["url"]} for f in a.get("files", [])]})
           for a in ler("analises-conjuntura.yaml")]
    (DATA / "analises.yaml").write_text(yml(ans, CAB), encoding="utf-8")

    tds = [limpo({"titulo": t["title"], "autores": t["authors"], "ano": t["year"],
                  "url": t.get("url", ""), "resumo": t.get("abstract", "")})
           for t in ler("textos-discussao.yaml")]
    (DATA / "textos-discussao.yaml").write_text(yml(tds, CAB), encoding="utf-8")

    mid = [limpo({"titulo": m["title"], "autores": m.get("authors", ""), "veiculo": m.get("outlet", ""),
                  "data": m.get("date", ""), "tipo": m["type"], "url": m.get("url", "")})
           for m in ler("na-midia.yaml")]
    (DATA / "midia.yaml").write_text(yml(mid, CAB), encoding="utf-8")

    sem = [limpo({"titulo": s["title"], "apresentador": s["presenter"],
                  "instituicao": s.get("institution", ""), "data": s.get("date", ""), "ano": s["year"]})
           for s in ler("eventos-seminarios.yaml")["seminarios"]]
    (DATA / "seminarios.yaml").write_text(yml(sem, CAB), encoding="utf-8")

    pes = [limpo({"titulo": p["title"], "autor": p.get("author", ""), "ano": p.get("year") or "",
                  "orientador": p.get("advisor", ""), "instituicao": p.get("institution", ""),
                  "status": p["status"], "url": p.get("url", ""), "descricao": p.get("description", "")})
           for p in ler("pesquisas.yaml")]
    (DATA / "pesquisas.yaml").write_text(yml(pes, CAB), encoding="utf-8")

    acv = []
    for a in ler("acervo.yaml"):
        cands = (a.get("candidatos_presidente") or []) + (a.get("candidatos_governador") or [])
        acv.append(limpo({"codigo": a["codigo"], "data": a.get("data", ""), "ano": a["year"],
                          "tipo_video": a.get("tipo_video", ""), "cargo": a.get("cargo", []),
                          "regiao": a.get("region", ""), "estado": a.get("estado", ""),
                          "candidatos": cands, "partidos": a.get("partidos", []),
                          "url": a["url"], "thumb": ""}))
    (DATA / "acervo.yaml").write_text(yml(acv, CAB), encoding="utf-8")

    bds = []
    for b in ler("bancos-de-dados.yaml"):
        reg = limpo({"nome": b["nome"], "descricao": b["descricao"], "cobertura": b.get("cobertura", ""),
                     "registros": int(b["registros"]) if str(b.get("registros", "")).isdigit() else "",
                     "pagina": b.get("pagina", ""), "download": b.get("download", ""),
                     "url": b.get("url", ""), "arquivo": b.get("arquivo", "")})
        if "Capitais" in b["nome"]:
            reg["aviso"] = ("A coluna de município desta base está incorreta na fonte original "
                            "(municípios rotacionados em relação aos candidatos). Em revisão.")
        bds.append(reg)
    (DATA / "bancos-de-dados.yaml").write_text(yml(bds, CAB), encoding="utf-8")

    linhas = list(csv.DictReader((FONTE / "mapas-votacao.csv").open(encoding="utf-8")))
    mps = []
    for r in linhas:
        # Mapas de eleição majoritária não têm sigla partidária: o título vem do cargo.
        titulo = r["titulo"].strip() or r["cargo"].strip()
        mps.append(limpo({"titulo": titulo, "ano": int(r["ano"]) if r["ano"].isdigit() else "",
                          "cargo": r.get("cargo", ""), "eleicao": r.get("eleicao", ""),
                          "turno": r.get("turno", ""), "url": r["url"]}))
    (DATA / "mapas-votacao.yaml").write_text(yml(mps, CAB), encoding="utf-8")

    prs = [{"nome": p["nome"], "arquivo": f"/img/parceiros/{Path(p['arquivo']).name}"}
           for p in ler("parceiros.yaml")]
    (DATA / "parceiros.yaml").write_text(yml(prs, CAB), encoding="utf-8")

    for nome, n in [("publicacoes", len(pubs)), ("analises", len(ans)), ("textos-discussao", len(tds)),
                    ("midia", len(mid)), ("seminarios", len(sem)), ("pesquisas", len(pes)),
                    ("acervo", len(acv)), ("bancos-de-dados", len(bds)), ("mapas-votacao", len(mps)),
                    ("parceiros", len(prs))]:
        print(f"  data/{nome+'.yaml':<26s} {n}")


# ---------------------------------------------------------------- site.yaml

def site():
    h = ler("homepage-institucional.yaml")
    fontes = ler("fontes-externas.yaml")
    catalogo = next(f["url"] for f in fontes["fontes"] if f["tipo"] == "google_sheets")
    geral = {
        "titulo": "DOXA. Laboratório de Estudos Eleitorais",
        "descricao": ("Laboratório de Estudos Eleitorais, de Comunicação Política e Opinião Pública "
                      "do IESP-UERJ"),
        "email": "acervo-doxa@iesp.uerj.br",
        "endereco": "Rua da Matriz, 82, Botafogo, Rio de Janeiro, RJ",
        "cep": "22260-100",
        "youtube": "https://www.youtube.com/channel/UCkcuDdIEuQ9YqOjHsp4-EHQ",
        # O vídeo dos "melhores momentos" é conteúdo do acervo — é lá que ele aparece.
        "video_destaque": h["featured_video"]["youtube_id"],
        # Vota Aí e o dashboard das eleições viraram PROJETOS (extracao/dados/projetos/).
        # O schema de `configuracao` é .strict(): reintroduzir votaai_* / dashboard_* aqui
        # sem atualizar src/content.config.ts derruba o build.
        "catalogo_acervo": catalogo,
        "formulario_acervo": "/docs/solicitacao-de-material-do-acervo.docx",
    }
    (DATA / "site.yaml").write_text(
        yml({"geral": geral}, "# Dados globais do site. Editável.\n"), encoding="utf-8")
    print(f"  data/site.yaml             video={geral['video_destaque']}")


def main():
    print("Convertendo extracao/dados -> src/ ...")
    equipe(); paginas(); projetos(); eventos(); listas(); site()
    # formulário do acervo
    docs = PUBLIC / "docs"
    docs.mkdir(exist_ok=True)
    src = RAIZ / "extracao" / "bruto" / "datasets" / "Solicitacao-de-Material-do-Acervo.docx"
    if src.exists():
        shutil.copy(src, docs / "solicitacao-de-material-do-acervo.docx")
    print("OK")


if __name__ == "__main__":
    main()
