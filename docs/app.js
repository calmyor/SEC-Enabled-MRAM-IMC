const menuButton = document.querySelector(".menu-toggle");
const navigation = document.querySelector(".site-nav");

if (menuButton && navigation) {
  const setMenuState = (open, restoreFocus = false) => {
    menuButton.setAttribute("aria-expanded", String(open));
    navigation.classList.toggle("open", open);
    document.body.classList.toggle("menu-open", open);
    if (open) {
      window.requestAnimationFrame(() => navigation.querySelector("a")?.focus());
    } else if (restoreFocus) {
      menuButton.focus();
    }
  };

  menuButton.addEventListener("click", () => {
    setMenuState(menuButton.getAttribute("aria-expanded") !== "true");
  });
  navigation.addEventListener("click", (event) => {
    if (event.target.closest("a")) {
      setMenuState(false);
    }
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && menuButton.getAttribute("aria-expanded") === "true") {
      setMenuState(false, true);
    }
  });
  window.addEventListener("resize", () => {
    if (window.innerWidth > 820 && menuButton.getAttribute("aria-expanded") === "true") {
      setMenuState(false);
    }
  });
}

document.querySelectorAll("[data-current-year]").forEach((node) => {
  node.textContent = new Date().getFullYear();
});

const equationNotes = {
  alpha: "αᵢⱼ captures how row position i and column j shape a cell’s analog contribution through BL/SL parasitics.",
  gamma: "γᵢ pre-scales row i before the dot product. Sharing one learned factor across columns makes the correction compact.",
  theta: "θⱼ normalizes column j after conversion. SEC learns γ and θ so the combined path θⱼγᵢαᵢⱼ approaches unity.",
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
    const expression = calculator.querySelector("[data-expression]");
    if (expression) {
      expression.textContent = `${values.states.toLocaleString()} states × ${values.repeats.toLocaleString()} repeats × ${values.codes.toLocaleString()} codes × ${values.columns.toLocaleString()} columns = ${total.toLocaleString()} captures`;
    }
  };
  inputs.forEach((input) => input.addEventListener("input", update));
  update();
}

const filterButtons = document.querySelectorAll("[data-artifact-filter]");
const artifacts = document.querySelectorAll("[data-artifact-kind]");
filterButtons.forEach((button) => {
  button.addEventListener("click", () => {
    const filter = button.dataset.artifactFilter;
    filterButtons.forEach((candidate) => candidate.setAttribute("aria-pressed", String(candidate === button)));
    artifacts.forEach((artifact) => {
      artifact.hidden = filter !== "all" && artifact.dataset.artifactKind !== filter;
    });
  });
});

const journeyLinks = [...document.querySelectorAll(".journey-rail a")];
const pageName = (pathname) => pathname.endsWith("/") ? "index.html" : pathname.split("/").at(-1) || "index.html";
const journeySections = journeyLinks.flatMap((link) => {
  const destination = new URL(link.href, window.location.href);
  if (pageName(destination.pathname) !== pageName(window.location.pathname) || !destination.hash) return [];
  const section = document.querySelector(destination.hash);
  return section ? [{ link, section }] : [];
});

if (journeySections.length) {
  let journeyFrame;
  let activeLink;
  const updateJourney = () => {
    const readingLine = window.scrollY + 175;
    let active = journeySections[0];
    journeySections.forEach((entry) => {
      const sectionTop = entry.section.getBoundingClientRect().top + window.scrollY;
      if (sectionTop <= readingLine) active = entry;
    });
    journeyLinks.forEach((link) => {
      const selected = link === active.link;
      link.classList.toggle("current", selected);
      link.classList.toggle("is-active", selected);
      if (selected) link.setAttribute("aria-current", "location");
      else link.removeAttribute("aria-current");
    });
    if (activeLink !== active.link) {
      activeLink = active.link;
      const track = active.link.parentElement;
      track.scrollTo({ left: active.link.offsetLeft - (track.clientWidth - active.link.offsetWidth) / 2 });
    }
  };
  const scheduleJourneyUpdate = () => {
    if (journeyFrame) return;
    journeyFrame = window.requestAnimationFrame(() => {
      journeyFrame = undefined;
      updateJourney();
    });
  };
  window.addEventListener("scroll", scheduleJourneyUpdate, { passive: true });
  window.addEventListener("resize", scheduleJourneyUpdate);
  updateJourney();
}

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
