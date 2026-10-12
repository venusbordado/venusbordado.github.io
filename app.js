// Vitrine: lê dados.json e monta os cards. Adicionar produto = editar só o dados.json.
(async function () {
  const cards = document.getElementById("cards");
  const vazio = document.getElementById("vazio");
  const filtros = document.getElementById("filtros");
  let produtos = [];
  try {
    const r = await fetch("dados.json", { cache: "no-store" });
    produtos = (await r.json()).produtos || [];
  } catch (e) {
    produtos = [];
  }
  // mais novo primeiro
  produtos.sort((a, b) => String(b.data || "").localeCompare(String(a.data || "")));

  // quadradinho clicavel: foto + nome pequeno + "ver no Mercado Livre"
  const criaCard = (p) => {
    const li = document.createElement("li");
    li.dataset.categoria = p.categoria || "";
    const a = document.createElement("a");
    a.className = "tile";
    a.href = p.link;
    a.target = "_blank";
    a.rel = "noopener sponsored";
    a.setAttribute("aria-label", p.nome + " (abre no Mercado Livre)");
    const img = document.createElement("img");
    img.src = p.foto;
    img.alt = p.nome;
    img.loading = "lazy";
    img.width = 600;
    img.height = 600;
    const nome = document.createElement("span");
    nome.className = "nome";
    nome.textContent = p.nome;
    const ver = document.createElement("span");
    ver.className = "ver";
    ver.textContent = "Mercado Livre ›";
    a.append(img, nome, ver);
    li.append(a);
    return li;
  };

  if (!produtos.length) {
    vazio.hidden = false;
    return;
  }
  produtos.forEach((p) => cards.append(criaCard(p)));

  // filtros por categoria só quando passar de 6 itens
  const categorias = [...new Set(produtos.map((p) => p.categoria).filter(Boolean))];
  if (produtos.length > 6 && categorias.length > 1) {
    filtros.hidden = false;
    const aplica = (cat) => {
      [...filtros.children].forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.cat === cat)));
      [...cards.children].forEach((li) => {
        li.hidden = cat !== "Todos" && li.dataset.categoria !== cat;
      });
    };
    ["Todos", ...categorias].forEach((c) => {
      const b = document.createElement("button");
      b.className = "filtro";
      b.type = "button";
      b.dataset.cat = c;
      b.textContent = c;
      b.addEventListener("click", () => aplica(c));
      filtros.append(b);
    });
    aplica("Todos");
  }
})();
