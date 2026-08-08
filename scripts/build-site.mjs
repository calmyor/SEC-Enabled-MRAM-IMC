import { cp, mkdir, readFile, writeFile } from "node:fs/promises";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const source = join(root, "website");
const destination = join(root, "docs");

const pages = [
  { file: "index.html", source: "overview.html", label: "Overview", title: "SEC-enabled 22 nm MRAM IMC", description: "From behavioral modeling to measured silicon: a 22 nm MRAM in-memory-computing macro with statistical error compensation." },
  { file: "design.html", source: "design.html", label: "Design", title: "Behavioral model to SEC architecture", description: "How parasitic-aware behavioral modeling became the SEC algorithm, OCCS readout, and fixed-point MRAM IMC macro." },
  { file: "tapeout.html", source: "tapeout.html", label: "Tapeout", title: "Tapeout engineering", description: "A practical, evidence-bounded guide to the mixed-signal tapeout process behind the 22 nm MRAM IMC prototype." },
  { file: "test-platform.html", source: "test-platform.html", label: "Test platform", title: "PCB and PYNQ test platform", description: "The host-to-silicon measurement stack: Python control, PYNQ-Z2, custom PCB, package, power, and bring-up." },
  { file: "measurements.html", source: "measurements.html", label: "Measurements", title: "Measurement methodology and results", description: "Calibration, code-conditioned sampling, SNDR reconstruction, SEC evaluation, and bounded application results." },
  { file: "repository.html", source: "repository.html", label: "Repository", title: "Repository and reproducibility", description: "A curated artifact map, runnable method demo, reproduction paths, and clear public-release boundaries." },
  { file: "papers.html", source: "papers.html", label: "Papers", title: "ESSCIRC and JSSC papers", description: "The ESSCIRC 2023 paper, the JSSC journal extension, citations, authors, and the design lineage." },
];

const authors = [
  "Saion K. Roy", "Han-Mo Ou", "Mostafa G. Ahmed", "Peter Deaville",
  "Bonan Zhang", "Naveen Verma", "Pavan K. Hanumolu", "Naresh R. Shanbhag",
];

function nav(current) {
  return pages.map((page) => {
    const active = page.file === current ? ' aria-current="page"' : "";
    return `<a href="${page.file}"${active}>${page.label}</a>`;
  }).join("\n          ");
}

function documentFor(page, content) {
  const canonical = `https://calmyor.github.io/SEC-Enabled-MRAM-IMC/${page.file === "index.html" ? "" : page.file}`;
  const jsonLd = JSON.stringify({
    "@context": "https://schema.org",
    "@type": "ScholarlyArticle",
    name: "Compute SNDR-Boosted 22-nm MRAM-Based In-Memory Computing Macro Using Statistical Error Compensation",
    author: authors.map((name) => ({ "@type": "Person", name })),
    isPartOf: { "@type": "Periodical", name: "IEEE Journal of Solid-State Circuits" },
    identifier: "https://doi.org/10.1109/JSSC.2024.3442013",
    url: canonical,
  });

  return `<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#071b22" />
    <meta name="description" content="${page.description}" />
    <link rel="canonical" href="${canonical}" />
    <meta property="og:title" content="${page.title} · SEC–MRAM IMC" />
    <meta property="og:description" content="${page.description}" />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="${canonical}" />
    <meta property="og:image" content="https://calmyor.github.io/SEC-Enabled-MRAM-IMC/assets/og.png" />
    <meta property="og:image:alt" content="SEC–MRAM IMC: from behavioral model to measured 22 nm silicon." />
    <meta name="twitter:card" content="summary_large_image" />
    <link rel="icon" href="assets/favicon.svg" type="image/svg+xml" />
    <link rel="stylesheet" href="styles.css" />
    <script type="application/ld+json">${jsonLd}</script>
    <script src="app.js" defer></script>
    <title>${page.title} · SEC–MRAM IMC</title>
  </head>
  <body>
    <a class="skip-link" href="#main">Skip to content</a>
    <header class="site-header">
      <a class="brand" href="index.html" aria-label="SEC–MRAM IMC overview">
        <span class="brand-icon" aria-hidden="true"><i></i><i></i><i></i><i></i></span>
        <span><strong>SEC–MRAM IMC</strong><small>Model → silicon → measurement</small></span>
      </a>
      <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>
      <nav id="site-nav" class="site-nav" aria-label="Project sections">
          ${nav(page.file)}
      </nav>
      <a class="repo-link" href="https://github.com/calmyor/SEC-Enabled-MRAM-IMC">GitHub <span aria-hidden="true">↗</span></a>
    </header>
${content}
    <footer class="site-footer">
      <div>
        <a class="footer-brand" href="index.html">SEC–MRAM IMC</a>
        <p>Statistical error compensation for a measured 22 nm MRAM in-memory-computing macro.</p>
      </div>
      <div class="footer-links">
        <a href="https://doi.org/10.1109/ESSCIRC59616.2023.10268688">ESSCIRC 2023 <span aria-hidden="true">↗</span></a>
        <a href="https://doi.org/10.1109/JSSC.2024.3442013">JSSC extension <span aria-hidden="true">↗</span></a>
        <a href="repository.html">Reproducibility</a>
      </div>
      <p class="footer-note">© <span data-current-year>2026</span> The authors. Paper figures are reproduced for this research artifact.</p>
    </footer>
  </body>
</html>\n`;
}

await mkdir(destination, { recursive: true });
for (const page of pages) {
  const content = await readFile(join(source, "pages", page.source), "utf8");
  await writeFile(join(destination, page.file), documentFor(page, content));
}
await cp(join(source, "assets"), join(destination, "assets"), { recursive: true, force: true });
await cp(join(source, "styles.css"), join(destination, "styles.css"), { force: true });
await cp(join(source, "app.js"), join(destination, "app.js"), { force: true });
await writeFile(join(destination, ".nojekyll"), "");
await writeFile(join(destination, "robots.txt"), "User-agent: *\nAllow: /\nSitemap: https://calmyor.github.io/SEC-Enabled-MRAM-IMC/sitemap.xml\n");
await writeFile(join(destination, "sitemap.xml"), `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${pages.map((page) => `  <url><loc>https://calmyor.github.io/SEC-Enabled-MRAM-IMC/${page.file === "index.html" ? "" : page.file}</loc></url>`).join("\n")}\n</urlset>\n`);
console.log(`Built ${pages.length} pages in ${destination}`);
