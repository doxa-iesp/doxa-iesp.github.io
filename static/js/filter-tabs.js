document.addEventListener("DOMContentLoaded", function () {
  const tabs = document.querySelectorAll(".filter-tab");
  if (!tabs.length) return;

  const itemSelector = document.querySelector("[data-filter-items]");
  const items = document.querySelectorAll(
    itemSelector ? itemSelector.dataset.filterItems : ".filter-item"
  );

  tabs.forEach(function (tab) {
    tab.addEventListener("click", function () {
      tabs.forEach(function (t) {
        t.classList.remove("active");
        t.setAttribute("aria-selected", "false");
      });
      this.classList.add("active");
      this.setAttribute("aria-selected", "true");

      var filter = this.dataset.filter;
      items.forEach(function (item) {
        var value = item.dataset.filterValue || item.dataset.status || item.dataset.cycle || "";
        item.style.display = (filter === "all" || value === filter) ? "" : "none";
      });
    });
  });
});
