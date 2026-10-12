"""Acrescenta um produto de afiliado na página e publica.

Uso (no terminal, dentro da pasta venus-links):
    python adicionar.py LINK_DE_AFILIADO "Categoria"
    python adicionar.py LINK_DE_AFILIADO "Categoria" "Nome que aparece na página"

- LINK_DE_AFILIADO: o link gerado no painel de afiliados do Mercado Livre (ex.: https://meli.la/1XbqzNd).
- Categoria: Marcação, Linhas, Entretela, Camisetas... (com mais de 6 produtos viram filtros).
- Nome: opcional. Sem ele, usa o título do anúncio.

O script abre o link, pega o título e a foto principal do anúncio, salva a foto quadrada em img/,
acrescenta no dados.json, mostra o que vai entrar e só publica se você digitar "s".
"""
import io, json, re, subprocess, sys, unicodedata, datetime
from urllib.request import Request, urlopen
from PIL import Image

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36"


def baixa(url):
    return urlopen(Request(url, headers={"User-Agent": UA}), timeout=30).read()


def slug(texto):
    t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")[:50]


if len(sys.argv) < 3:
    print(__doc__)
    sys.exit(1)
link, categoria = sys.argv[1], sys.argv[2]
dados = json.load(open("dados.json", encoding="utf-8"))
if any(p["link"] == link for p in dados["produtos"]):
    sys.exit("Esse link já está na página.")
html = baixa(link).decode("utf-8", "ignore")
titulo = re.search(r'property="og:title" content="([^"]*)"', html)
foto = re.search(r'property="og:image" content="([^"]*)"', html)
if not titulo or not foto:
    sys.exit("Não consegui ler o anúncio por esse link. Confira se é o link de afiliado certo.")
titulo = titulo.group(1)
nome = sys.argv[3] if len(sys.argv) > 3 else titulo

im = Image.open(io.BytesIO(baixa(foto.group(1)))).convert("RGB")
w, h = im.size
lado = max(w, h)
quadro = Image.new("RGB", (lado, lado), (255, 255, 255))
quadro.paste(im, ((lado - w) // 2, (lado - h) // 2))
arquivo = f"img/{slug(nome)}.webp"
quadro.resize((600, 600), Image.LANCZOS).save(arquivo, "WEBP", quality=82)

hoje = datetime.date.today().isoformat()
dados["produtos"].append({"nome": nome, "foto": arquivo, "link": link, "categoria": categoria, "data": hoje,
                          "anuncio": titulo, "conferido": f"{hoje}: adicionado pelo adicionar.py (foto do anúncio)"})
json.dump(dados, open("dados.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)

print(f"\nAnúncio: {titulo}\nNome na página: {nome}\nCategoria: {categoria}\nFoto: {arquivo}")
if input("\nPublicar agora? (s/n) ").strip().lower() == "s":
    subprocess.run(["git", "add", "dados.json", arquivo], check=True)
    subprocess.run(["git", "commit", "-q", "-m", f"Novo produto: {nome}"], check=True)
    subprocess.run(["git", "push", "-q"], check=True)
    print("Publicado. Em 1 ou 2 minutos aparece em https://venusbordado.github.io")
else:
    print("Ficou só no computador. Para publicar depois: git add -A, git commit, git push.")
