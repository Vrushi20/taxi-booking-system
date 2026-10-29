document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.getElementById("nav-toggle");
  const menu = document.getElementById("dashboard-menu");

  if (!toggle || !menu) return;

  const setMenuOpen = (isOpen) => {
    toggle.setAttribute("aria-expanded", String(isOpen));
    menu.classList.toggle("is-open", isOpen);
  };

  setMenuOpen(false);

  toggle.addEventListener("click", () => {
    const isOpen = toggle.getAttribute("aria-expanded") === "true";
    setMenuOpen(!isOpen);
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") setMenuOpen(false);
  });

  window.addEventListener("resize", () => setMenuOpen(false));
});
