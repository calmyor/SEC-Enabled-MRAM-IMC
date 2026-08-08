const menuButton = document.querySelector(".menu-toggle");
const navigation = document.querySelector(".site-nav");

if (menuButton && navigation) {
  menuButton.addEventListener("click", () => {
    const open = menuButton.getAttribute("aria-expanded") !== "true";
    menuButton.setAttribute("aria-expanded", String(open));
    navigation.classList.toggle("open", open);
    document.body.classList.toggle("menu-open", open);
  });
  navigation.addEventListener("click", (event) => {
    if (event.target.closest("a")) {
      menuButton.setAttribute("aria-expanded", "false");
      navigation.classList.remove("open");
      document.body.classList.remove("menu-open");
    }
  });
}

document.querySelectorAll("[data-current-year]").forEach((node) => {
  node.textContent = new Date().getFullYear();
});

const equationNotes = {
  alpha: "αᵢⱼ is the row- and column-dependent attenuation produced by array parasitics. It is a behavioral description of the error, not an extra hardware state.",
  gamma: "γᵢ is the learned per-row input correction. One factor is shared across ADC columns, which keeps SEC overhead practical.",
  theta: "θⱼ is a per-column output normalization term. Together, θⱼγᵢαᵢⱼ is driven toward unity.",
};

document.querySelectorAll("[data-equation-term]").forEach((button) => {
  button.addEventListener("click", () => {
    const group = button.closest("[data-equation-explainer]");
    group.querySelectorAll("[data-equation-term]").forEach((candidate) => candidate.setAttribute("aria-pressed", String(candidate === button)));
    const output = group.querySelector("[data-equation-readout]");
    output.textContent = equationNotes[button.dataset.equationTerm];
  });
});

const calculator = document.querySelector("[data-protocol-calculator]");
if (calculator) {
  const inputs = [...calculator.querySelectorAll("input")];
  const update = () => {
    const values = Object.fromEntries(inputs.map((input) => [input.name, Math.max(1, Number(input.value) || 1)]));
    const perCodeColumn = values.states * values.repeats;
    const perColumn = perCodeColumn * values.codes;
    const total = perColumn * values.columns;
    calculator.querySelector("[data-per-code]").textContent = perCodeColumn.toLocaleString();
    calculator.querySelector("[data-per-column]").textContent = perColumn.toLocaleString();
    calculator.querySelector("[data-total]").textContent = total.toLocaleString();
  };
  inputs.forEach((input) => input.addEventListener("input", update));
  update();
}

const filterButtons = document.querySelectorAll("[data-artifact-filter]");
const artifacts = document.querySelectorAll("[data-tier]");
filterButtons.forEach((button) => {
  button.addEventListener("click", () => {
    const filter = button.dataset.artifactFilter;
    filterButtons.forEach((candidate) => candidate.setAttribute("aria-pressed", String(candidate === button)));
    artifacts.forEach((artifact) => {
      artifact.hidden = filter !== "all" && artifact.dataset.tier !== filter;
    });
  });
});

document.querySelectorAll("[data-copy-target]").forEach((button) => {
  button.addEventListener("click", async () => {
    const target = document.getElementById(button.dataset.copyTarget);
    if (!target) return;
    try {
      await navigator.clipboard.writeText(target.textContent.trim());
      button.textContent = "Copied";
      window.setTimeout(() => { button.textContent = "Copy citation"; }, 1600);
    } catch {
      button.textContent = "Select citation above";
    }
  });
});
