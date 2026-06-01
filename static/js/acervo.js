/* Filtros do Acervo Audiovisual
   Carrega /acervo-data.json gerado pelo Hugo e aplica filtros client-side */
(function () {
  const grid = document.getElementById("acervo-grid");
  const count = document.getElementById("acervo-count");
  const selCargo   = document.getElementById("filter-cargo");
  const selRegiao  = document.getElementById("filter-regiao");
  const selAno     = document.getElementById("filter-ano");
  const selPartido = document.getElementById("filter-partido");
  const inputBusca = document.getElementById("filter-busca");
  const btnReset   = document.getElementById("acervo-reset");

  if (!grid) return;

  let allItems = [];

  function populate(select, values) {
    values.sort().forEach(v => {
      const opt = document.createElement("option");
      opt.value = v;
      opt.textContent = v;
      select.appendChild(opt);
    });
  }

  function render(items) {
    if (items.length === 0) {
      grid.innerHTML = "<p class='acervo-loading'>Nenhum item encontrado para os filtros selecionados.</p>";
      count.textContent = "0 itens encontrados.";
      return;
    }
    count.textContent = `${items.length} item${items.length !== 1 ? "s" : ""} encontrado${items.length !== 1 ? "s" : ""}.`;
    grid.innerHTML = items.map(item => `
      <div class="acervo-card">
        <div class="acervo-card-thumb">
          ${item.thumb ? `<img src="${item.thumb}" alt="${item.candidate || "Vídeo"}" loading="lazy">` : ""}
        </div>
        <div class="acervo-card-info">
          <p class="acervo-card-candidate">${item.candidate || "—"}</p>
          <p class="acervo-card-meta">${[item.party, item.region, item.year].filter(Boolean).join(" · ")}</p>
          <p class="acervo-card-meta">${item.cargo || ""}</p>
          ${item.url ? `<a href="${item.url}" target="_blank" rel="noopener noreferrer" class="acervo-card-link">Assistir</a>` : ""}
        </div>
      </div>
    `).join("");
  }

  function applyFilters() {
    const cargo   = selCargo.value.toLowerCase();
    const regiao  = selRegiao.value.toLowerCase();
    const ano     = selAno.value;
    const partido = selPartido.value.toLowerCase();
    const busca   = inputBusca.value.toLowerCase().trim();

    const filtered = allItems.filter(item => {
      if (cargo   && (item.cargo   || "").toLowerCase() !== cargo)   return false;
      if (regiao  && (item.region  || "").toLowerCase() !== regiao)  return false;
      if (ano     && String(item.year) !== ano)                       return false;
      if (partido && (item.party   || "").toLowerCase() !== partido)  return false;
      if (busca   && !(item.candidate || "").toLowerCase().includes(busca)) return false;
      return true;
    });

    render(filtered);
  }

  [selCargo, selRegiao, selAno, selPartido].forEach(el => el.addEventListener("change", applyFilters));
  inputBusca.addEventListener("input", applyFilters);
  btnReset.addEventListener("click", function () {
    selCargo.value = ""; selRegiao.value = ""; selAno.value = ""; selPartido.value = ""; inputBusca.value = "";
    applyFilters();
  });

  const data = window.ACERVO_DATA || [];
  allItems = data;

  const cargos   = [...new Set(data.map(d => d.cargo).filter(Boolean))];
  const regioes  = [...new Set(data.map(d => d.region).filter(Boolean))];
  const anos     = [...new Set(data.map(d => String(d.year)).filter(Boolean))].sort().reverse();
  const partidos = [...new Set(data.map(d => d.party).filter(Boolean))];

  populate(selCargo, cargos);
  populate(selRegiao, regioes);
  anos.forEach(a => { const opt = document.createElement("option"); opt.value = a; opt.textContent = a; selAno.appendChild(opt); });
  populate(selPartido, partidos);

  render(data);
})();
