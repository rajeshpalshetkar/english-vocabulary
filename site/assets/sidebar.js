(() => {
  const sidebar = document.getElementById("site-sidebar");
  const toggle = document.querySelector(".sidebar-toggle");
  const backdrop = document.querySelector(".sidebar-backdrop");
  if (!sidebar || !toggle || !backdrop) return;
  const close = () => {
    sidebar.classList.remove("is-open");
    backdrop.classList.remove("is-visible");
    toggle.setAttribute("aria-expanded", "false");
    document.body.classList.remove("sidebar-open");
  };
  const open = () => {
    sidebar.classList.add("is-open");
    backdrop.classList.add("is-visible");
    toggle.setAttribute("aria-expanded", "true");
    document.body.classList.add("sidebar-open");
  };
  toggle.addEventListener("click", () => sidebar.classList.contains("is-open") ? close() : open());
  backdrop.addEventListener("click", close);
  document.addEventListener("keydown", event => { if (event.key === "Escape") close(); });
  sidebar.querySelectorAll("a").forEach(link => {
    const target = new URL(link.href, location.origin);
    if (target.pathname === location.pathname || (target.pathname !== "/" && location.pathname.startsWith(target.pathname))) {
      link.classList.add("active");
      link.setAttribute("aria-current", "page");
    }
    link.addEventListener("click", close);
  });
})();
