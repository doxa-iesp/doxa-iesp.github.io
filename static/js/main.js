/* Menu mobile e dropdowns */
(function () {
  const toggle = document.querySelector(".nav-toggle");
  const navWrapper = document.querySelector(".header-nav-wrapper");

  if (toggle && navWrapper) {
    toggle.addEventListener("click", function () {
      const open = navWrapper.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open);
    });

    /* Fechar ao clicar fora */
    document.addEventListener("click", function (e) {
      if (!e.target.closest(".site-header")) {
        navWrapper.classList.remove("open");
        toggle.setAttribute("aria-expanded", "false");
      }
    });

    /* Dropdowns no mobile */
    navWrapper.querySelectorAll(".nav-item.has-dropdown > .nav-link").forEach(link => {
      link.addEventListener("click", function (e) {
        if (window.innerWidth <= 900) {
          e.preventDefault();
          const item = this.closest(".nav-item");
          item.classList.toggle("open");
        }
      });
    });
  }
})();
