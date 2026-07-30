(() => {
  for (const term of document.querySelectorAll(".md-typeset abbr[title]")) {
    const explanation = term.getAttribute("title");
    if (!explanation) {
      continue;
    }

    term.dataset.tooltip = explanation;
    term.setAttribute(
      "aria-label",
      `${term.textContent.trim()}: ${explanation}`,
    );
    term.setAttribute("tabindex", "0");
    term.removeAttribute("title");
  }
})();
