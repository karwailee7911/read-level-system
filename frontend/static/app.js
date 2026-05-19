document.addEventListener("click", (event) => {
  const button = event.target.closest("[data-tab]");
  if (!button) return;

  const tab = button.dataset.tab;
  document.querySelectorAll("[data-tab]").forEach((item) => {
    item.classList.toggle("active", item.dataset.tab === tab);
  });
  document.querySelectorAll("[data-tab-panel]").forEach((panel) => {
    panel.hidden = panel.dataset.tabPanel !== tab;
  });
});

