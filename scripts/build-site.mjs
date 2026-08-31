import { createHash } from "node:crypto";
import { cp, mkdir, readFile, writeFile } from "node:fs/promises";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import katex from "katex";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const source = join(root, "website");
const destination = join(root, "docs");
const katexSource = join(root, "node_modules", "katex");
const katexDestination = join(destination, "assets", "vendor", "katex");
const plexSource = join(root, "node_modules", "@fontsource-variable", "ibm-plex-sans");
const plexDestination = join(destination, "assets", "vendor", "ibm-plex-sans");
const stylesRevision = createHash("sha256").update(await readFile(join(source, "styles.css"))).digest("hex").slice(0, 12);
const appRevision = createHash("sha256").update(await readFile(join(source, "app.js"))).digest("hex").slice(0, 12);

const pages = [
  { file: "index.html", source: "overview.html", label: "Overview", title: "SEC-enabled 22 nm MRAM IMC", description: "From behavioral modeling to measured silicon: a 22 nm MRAM in-memory-computing macro with statistical error compensation." },
  { file: "design.html", source: "design.html", label: "Design", title: "Behavioral model to SEC architecture", description: "How parasitic-aware behavioral modeling became the SEC algorithm, OCCS readout, and fixed-point MRAM IMC macro." },
  { file: "tapeout.html", source: "tapeout.html", label: "Tapeout", title: "Tapeout engineering", description: "How the SEC-enabled MRAM macro moved from frozen interfaces through mixed-signal implementation, physical closure, packaging, and test readiness." },
  { file: "test-platform.html", source: "test-platform.html", label: "Test platform", title: "PCB and PYNQ test platform", description: "The host-to-silicon measurement stack: Python control, PYNQ-Z2, custom PCB, package, power, and bring-up." },
  { file: "measurements.html", source: "measurements.html", label: "Measurements", title: "Measurement methodology and results", description: "Calibration, code-conditioned sampling, SNDR reconstruction, SEC evaluation, and the measured ResNet-20 output-layer result." },
  { file: "repository.html", source: "repository.html", label: "Repository", title: "Repository and reproducibility", description: "Explore the architecture, run the measurement method, follow the hardware workflow, and trace the publication record." },
  { file: "papers.html", source: "papers.html", label: "Papers", title: "JxCDC, ESSCIRC, and JSSC papers", description: "The JxCDC parallel-bar model, ESSCIRC 2023 silicon result, JSSC journal account, citations, authors, and research relationship." },
];

const authors = [
  "Saion K. Roy", "Han-Mo Ou", "Mostafa G. Ahmed", "Peter Deaville",
  "Bonan Zhang", "Naveen Verma", "Pavan K. Hanumolu", "Naresh R. Shanbhag",
];

function nav(current) {
  return pages.map((page) => {
    const active = page.file === current ? ' aria-current="page"' : "";
    const resourceClass = page.file === "repository.html" ? ' class="resource-nav resource-start"' : page.file === "papers.html" ? ' class="resource-nav"' : "";
    return `<a href="${page.file}"${resourceClass}${active}>${page.label}</a>`;
  }).join("\n          ");
}

function journey(current) {
  const steps = [
    { file: "index.html", href: "index.html#signal-challenge", label: "Signal limit" },
    { file: "design.html", href: "design.html#behavioral-model", label: "Behavioral model" },
    { file: "design.html", href: "design.html#sec-architecture", label: "SEC + OCCS" },
    { file: "design.html", href: "design.html#macro", label: "Macro" },
    { file: "tapeout.html", href: "tapeout.html#process", label: "Tapeout" },
    { file: "test-platform.html", href: "test-platform.html#stack", label: "Test stack" },
    { file: "measurements.html", href: "measurements.html#results", label: "Measured result" },
  ];
  return steps.map((step) => `<a href="${step.href}"${step.file === current ? ' class="current"' : ""}>${step.label}</a>`).join("\n        ");
}

const handoffNotes = {
  "index.html": "See how the physical attenuation becomes a compact correction architecture.",
  "design.html": "Carry the fixed-point SEC and OCCS definitions into implementation closure.",
  "tapeout.html": "Follow the released interfaces into the PCB, FPGA, and bring-up sequence.",
  "test-platform.html": "Turn raw ADC captures into calibrated, code-conditioned compute SNDR.",
  "measurements.html": "Run the method and inspect the engineering artifacts behind the result.",
  "repository.html": "Connect the JxCDC parallel-bar model, ESSCIRC silicon result, and JSSC complete account.",
  "papers.html": "Return to the complete model-to-silicon research arc.",
};

function handoff(current) {
  const index = pages.findIndex((page) => page.file === current);
  const previous = index > 0 ? pages[index - 1] : null;
  const next = index < pages.length - 1 ? pages[index + 1] : null;
  const links = [
    previous ? `<a class="handoff-link handoff-previous" href="${previous.file}"><span>Previous · ${previous.label}</span><strong>← Revisit the preceding layer</strong></a>` : "",
    next ? `<a class="handoff-link handoff-next" href="${next.file}"><span>Next · ${next.label}</span><strong>${handoffNotes[current]} →</strong></a>` : "",
  ].filter(Boolean).join("\n      ");
  return `<aside class="page-handoff" aria-label="Continue through the project">
      ${links}
    </aside>`;
}

function renderMath(content, sourceName) {
  const mathPattern = /<(span|div)([^>]*?)\sdata-math="(inline|display)"([^>]*)>([\s\S]*?)<\/\1>/g;
  const rendered = content.replace(mathPattern, (match, tag, before, mode, after, sourceMath) => {
    if (/<[^>]+>/.test(sourceMath)) {
      throw new Error(`${sourceName}: math source cannot contain nested HTML: ${sourceMath.trim()}`);
    }
    const tex = sourceMath.trim();
    const html = katex.renderToString(tex, {
      displayMode: mode === "display",
      output: "htmlAndMathml",
      throwOnError: true,
      strict: "error",
      trust: false,
    });
    return `<${tag}${before} data-math-rendered="${mode}"${after}>${html}</${tag}>`;
  });
  if (/\sdata-math="(?:inline|display)"/.test(rendered)) {
    throw new Error(`${sourceName}: one or more math expressions were not rendered`);
  }
  return rendered;
}

function documentFor(page, content) {
  const hasMath = content.includes('data-math-rendered=');
  const hasClientMath = /data-math-dynamic|data-equation-explainer/.test(content);
  const mathStyles = hasMath ? '    <link rel="stylesheet" href="assets/vendor/katex/katex.min.css" />\n' : "";
  const mathRuntime = hasClientMath ? '    <script src="assets/vendor/katex/katex.min.js" defer></script>\n' : "";
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
    <link rel="preload" href="assets/vendor/ibm-plex-sans/files/ibm-plex-sans-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin />
    <link rel="stylesheet" href="assets/vendor/ibm-plex-sans/index.css" />
    <link rel="stylesheet" href="styles.css?v=${stylesRevision}" />
${mathStyles}    <script type="application/ld+json">${jsonLd}</script>
${mathRuntime}    <script src="app.js?v=${appRevision}" defer></script>
    <title>${page.title} · SEC–MRAM IMC</title>
  </head>
  <body>
    <a class="skip-link" href="#main">Skip to content</a>
    <header class="site-header">
      <a class="brand" href="index.html" aria-label="SEC–MRAM IMC overview">
        <img class="brand-icon" src="assets/project-mark.svg" alt="" width="48" height="48" />
        <span><strong>SEC–MRAM IMC</strong><small>Model · architecture · measured silicon</small></span>
      </a>
      <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>
      <nav id="site-nav" class="site-nav" aria-label="Project sections">
          ${nav(page.file)}
      </nav>
      <a class="repo-link" href="https://github.com/calmyor/SEC-Enabled-MRAM-IMC">GitHub <span aria-hidden="true">↗</span></a>
    </header>
    <nav class="journey-rail" aria-label="Design-to-measurement research path">
      <span>Research path</span>
      <div>${journey(page.file)}</div>
    </nav>
${content}
    ${handoff(page.file)}
    <footer class="site-footer">
      <div>
        <a class="footer-brand" href="index.html">SEC–MRAM IMC</a>
        <p>Statistical error compensation for a measured 22 nm MRAM in-memory-computing macro.</p>
      </div>
      <div class="footer-links">
        <a href="https://doi.org/10.1109/JXCDC.2024.3381888">JxCDC model <span aria-hidden="true">↗</span></a>
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
  await writeFile(join(destination, page.file), documentFor(page, renderMath(content, page.source)));
}
await cp(join(source, "assets"), join(destination, "assets"), { recursive: true, force: true });
await mkdir(katexDestination, { recursive: true });
await cp(join(katexSource, "dist", "fonts"), join(katexDestination, "fonts"), { recursive: true, force: true });
await cp(join(katexSource, "dist", "katex.min.css"), join(katexDestination, "katex.min.css"), { force: true });
await cp(join(katexSource, "dist", "katex.min.js"), join(katexDestination, "katex.min.js"), { force: true });
await cp(join(katexSource, "LICENSE"), join(katexDestination, "LICENSE"), { force: true });
await mkdir(join(plexDestination, "files"), { recursive: true });
await cp(join(plexSource, "index.css"), join(plexDestination, "index.css"), { force: true });
for (const file of [
  "ibm-plex-sans-cyrillic-ext-wght-normal.woff2",
  "ibm-plex-sans-cyrillic-wght-normal.woff2",
  "ibm-plex-sans-greek-wght-normal.woff2",
  "ibm-plex-sans-vietnamese-wght-normal.woff2",
  "ibm-plex-sans-latin-ext-wght-normal.woff2",
  "ibm-plex-sans-latin-wght-normal.woff2",
]) {
  await cp(join(plexSource, "files", file), join(plexDestination, "files", file), { force: true });
}
await cp(join(plexSource, "LICENSE"), join(plexDestination, "LICENSE"), { force: true });
await cp(join(source, "styles.css"), join(destination, "styles.css"), { force: true });
await cp(join(source, "app.js"), join(destination, "app.js"), { force: true });
await writeFile(join(destination, ".nojekyll"), "");
await writeFile(join(destination, "robots.txt"), "User-agent: *\nAllow: /\nSitemap: https://calmyor.github.io/SEC-Enabled-MRAM-IMC/sitemap.xml\n");
await writeFile(join(destination, "sitemap.xml"), `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${pages.map((page) => `  <url><loc>https://calmyor.github.io/SEC-Enabled-MRAM-IMC/${page.file === "index.html" ? "" : page.file}</loc></url>`).join("\n")}\n</urlset>\n`);
console.log(`Built ${pages.length} pages in ${destination}`);
