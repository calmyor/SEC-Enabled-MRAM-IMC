"""Build docs/ from website/ without node.

A byte-for-byte port of scripts/build-site.mjs. The only piece that cannot run
here is KaTeX itself, so rendered math comes from scripts/math-cache.json, a
(mode, TeX) -> rendered-HTML map extracted from a real KaTeX run. Editing prose
needs nothing else; adding or changing a math expression is a cache miss and
this script stops and names it, because only node can render the new one.

    python3 scripts/build_site.py
    python3 scripts/validate_site.py

node scripts/build-site.mjs remains canonical and produces identical output.
"""
import hashlib, json, os, re, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE_PATH = os.path.join(ROOT, "scripts", "math-cache.json")
DEST = os.path.join(ROOT, "docs")

source = os.path.join(ROOT, "website")
destination = DEST
katex_source = os.path.join(ROOT, "node_modules", "katex")
katex_destination = os.path.join(destination, "assets", "vendor", "katex")
plex_source = os.path.join(ROOT, "node_modules", "@fontsource-variable", "ibm-plex-sans")
plex_destination = os.path.join(destination, "assets", "vendor", "ibm-plex-sans")

def sha12(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()[:12]

styles_revision = sha12(os.path.join(source, "styles.css"))
app_revision = sha12(os.path.join(source, "app.js"))

pages = [
  {"file":"index.html","source":"overview.html","label":"Overview","title":"SEC-enabled 22 nm MRAM IMC","description":"From behavioral modeling to measured silicon: a 22 nm MRAM in-memory-computing macro with statistical error compensation."},
  {"file":"design.html","source":"design.html","label":"Design","title":"Behavioral model to SEC architecture","description":"How parasitic-aware behavioral modeling became the SEC algorithm, OCCS readout, and fixed-point MRAM IMC macro."},
  {"file":"tapeout.html","source":"tapeout.html","label":"Tapeout","title":"Tapeout engineering","description":"How the SEC-enabled MRAM macro moved from frozen interfaces through mixed-signal implementation, physical closure, packaging, and test readiness."},
  {"file":"test-platform.html","source":"test-platform.html","label":"Test platform","title":"PCB and PYNQ test platform","description":"The host-to-silicon measurement stack: Python control, PYNQ-Z2, custom PCB, package, power, and bring-up."},
  {"file":"measurements.html","source":"measurements.html","label":"Measurements","title":"Measurement methodology and results","description":"Calibration, code-conditioned sampling, SNDR reconstruction, SEC evaluation, and the measured ResNet-20 output-layer result."},
  {"file":"repository.html","source":"repository.html","label":"Repository","title":"Repository and reproducibility","description":"Explore the architecture, run the measurement method, follow the hardware workflow, and trace the publication record."},
  {"file":"papers.html","source":"papers.html","label":"Papers","title":"ESSCIRC 2023, JxCDC 2024, and JSSC 2025 papers","description":"The JxCDC 2024 parallel-bar model, ESSCIRC 2023 silicon result, JSSC 2025 journal account, citations, authors, and research relationship."},
]

authors = ["Saion K. Roy","Han-Mo Ou","Mostafa G. Ahmed","Peter Deaville",
           "Bonan Zhang","Naveen Verma","Pavan K. Hanumolu","Naresh R. Shanbhag"]

def nav(current):
    items = []
    for page in pages:
        active = ' aria-current="page"' if page["file"] == current else ""
        if page["file"] == "repository.html":
            rc = ' class="resource-nav resource-start"'
        elif page["file"] == "papers.html":
            rc = ' class="resource-nav"'
        else:
            rc = ""
        items.append(f'<a href="{page["file"]}"{rc}{active}>{page["label"]}</a>')
    return "\n          ".join(items)

def journey(current):
    # One entry per project stage. "files" lists every page the stage covers,
    # so Testing stays current across both the test-platform and measurements pages.
    steps = [
      {"files":["design.html"],"href":"design.html#behavioral-model","label":"Modeling"},
      {"files":["design.html"],"href":"design.html#sec-architecture","label":"Design"},
      {"files":["tapeout.html"],"href":"tapeout.html#process","label":"Tapeout"},
      {"files":["test-platform.html","measurements.html"],"href":"test-platform.html#stack","label":"Testing"},
    ]
    return "\n        ".join(
        f'<a href="{s["href"]}"{" class=\"current\"" if current in s["files"] else ""}>{s["label"]}</a>'
        for s in steps)

handoff_notes = {
  "index.html":"See how the physical attenuation becomes a compact correction architecture.",
  "design.html":"Carry the fixed-point SEC and OCCS definitions into implementation closure.",
  "tapeout.html":"Follow the released interfaces into the PCB, FPGA, and bring-up sequence.",
  "test-platform.html":"Turn raw ADC captures into calibrated, code-conditioned compute SNDR.",
  "measurements.html":"Run the method and inspect the engineering artifacts behind the result.",
  "repository.html":"Connect the JxCDC 2024 parallel-bar model, ESSCIRC 2023 silicon result, and JSSC 2025 complete account.",
  "papers.html":"Return to the complete model-to-silicon research arc.",
}

def handoff(current):
    index = next(i for i, p in enumerate(pages) if p["file"] == current)
    previous = pages[index-1] if index > 0 else None
    nxt = pages[index+1] if index < len(pages)-1 else None
    links = []
    if previous:
        links.append(f'<a class="handoff-link handoff-previous" href="{previous["file"]}"><span>Previous · {previous["label"]}</span><strong>← Revisit the preceding layer</strong></a>')
    if nxt:
        links.append(f'<a class="handoff-link handoff-next" href="{nxt["file"]}"><span>Next · {nxt["label"]}</span><strong>{handoff_notes[current]} →</strong></a>')
    joined = "\n      ".join(links)
    return f'''<aside class="page-handoff" aria-label="Continue through the project">
      {joined}
    </aside>'''

CACHE = json.load(open(CACHE_PATH, encoding="utf8"))
MATH = re.compile(r'<(span|div)([^>]*?)\sdata-math="(inline|display)"([^>]*)>([\s\S]*?)</\1>')

def render_math(content, source_name):
    misses = []
    def repl(m):
        tag, before, mode, after, src_math = m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)
        if re.search(r'<[^>]+>', src_math):
            raise SystemExit(f"{source_name}: math source cannot contain nested HTML: {src_math.strip()}")
        tex = src_math.strip()
        key = f"{mode}\x00{tex}"
        if key not in CACHE:
            misses.append((mode, tex))
            return m.group(0)
        return f'<{tag}{before} data-math-rendered="{mode}"{after}>{CACHE[key]}</{tag}>'
    rendered = MATH.sub(repl, content)
    if misses:
        lines = "\n".join(f"  [{mode}] {tex}" for mode, tex in misses)
        raise SystemExit(
            f"{source_name}: {len(misses)} math expression(s) are not in the KaTeX cache.\n"
            f"{lines}\n"
            "New or edited maths needs a real KaTeX run (node scripts/build-site.mjs) to\n"
            "regenerate scripts/math-cache.json. Revert the change or install node.")
    if re.search(r'\sdata-math="(?:inline|display)"', rendered):
        raise SystemExit(f"{source_name}: one or more math expressions were not rendered")
    return rendered

def document_for(page, content):
    has_math = "data-math-rendered=" in content
    has_client_math = bool(re.search(r'data-math-dynamic|data-equation-explainer', content))
    math_styles = '    <link rel="stylesheet" href="assets/vendor/katex/katex.min.css" />\n' if has_math else ""
    math_runtime = '    <script src="assets/vendor/katex/katex.min.js" defer></script>\n' if has_client_math else ""
    slug = "" if page["file"] == "index.html" else page["file"]
    canonical = f'https://calmyor.github.io/SEC-Enabled-MRAM-IMC/{slug}'
    json_ld = json.dumps({
        "@context":"https://schema.org",
        "@type":"ScholarlyArticle",
        "name":"Compute SNDR-Boosted 22-nm MRAM-Based In-Memory Computing Macro Using Statistical Error Compensation",
        "author":[{"@type":"Person","name":n} for n in authors],
        "isPartOf":{"@type":"Periodical","name":"IEEE Journal of Solid-State Circuits"},
        "identifier":"https://doi.org/10.1109/JSSC.2024.3442013",
        "url":canonical,
    }, separators=(",",":"), ensure_ascii=False)

    return f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#071b22" />
    <meta name="description" content="{page["description"]}" />
    <link rel="canonical" href="{canonical}" />
    <meta property="og:title" content="{page["title"]} · SEC–MRAM IMC" />
    <meta property="og:description" content="{page["description"]}" />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="{canonical}" />
    <meta property="og:image" content="https://calmyor.github.io/SEC-Enabled-MRAM-IMC/assets/og.png" />
    <meta property="og:image:alt" content="SEC–MRAM IMC: from behavioral model to measured 22 nm silicon." />
    <meta name="twitter:card" content="summary_large_image" />
    <link rel="icon" href="assets/favicon.svg" type="image/svg+xml" />
    <link rel="preload" href="assets/vendor/ibm-plex-sans/files/ibm-plex-sans-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin />
    <link rel="stylesheet" href="assets/vendor/ibm-plex-sans/index.css" />
    <link rel="stylesheet" href="styles.css?v={styles_revision}" />
{math_styles}    <script type="application/ld+json">{json_ld}</script>
{math_runtime}    <script src="app.js?v={app_revision}" defer></script>
    <title>{page["title"]} · SEC–MRAM IMC</title>
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
          {nav(page["file"])}
      </nav>
      <a class="repo-link" href="https://github.com/calmyor/SEC-Enabled-MRAM-IMC">GitHub <span aria-hidden="true">↗</span></a>
    </header>
    <nav class="journey-rail" aria-label="Design-to-measurement research path">
      <span>Research path</span>
      <div>{journey(page["file"])}</div>
    </nav>
{content}
    {handoff(page["file"])}
    <footer class="site-footer">
      <div>
        <a class="footer-brand" href="index.html">SEC–MRAM IMC</a>
        <p>Statistical error compensation for a measured 22 nm MRAM in-memory-computing macro.</p>
      </div>
      <div class="footer-links">
        <a href="https://doi.org/10.1109/JXCDC.2024.3381888">JxCDC 2024 <span aria-hidden="true">↗</span></a>
        <a href="https://doi.org/10.1109/ESSCIRC59616.2023.10268688">ESSCIRC 2023 <span aria-hidden="true">↗</span></a>
        <a href="https://doi.org/10.1109/JSSC.2024.3442013">JSSC 2025 <span aria-hidden="true">↗</span></a>
        <a href="repository.html">Reproducibility</a>
      </div>
      <p class="footer-note">© <span data-current-year>2026</span> The authors. Paper figures are reproduced for this research artifact.</p>
    </footer>
  </body>
</html>
'''

os.makedirs(destination, exist_ok=True)
for page in pages:
    content = open(os.path.join(source, "pages", page["source"]), encoding="utf8").read()
    out = document_for(page, render_math(content, page["source"]))
    open(os.path.join(destination, page["file"]), "w", encoding="utf8").write(out)

def copytree(src, dst):
    shutil.copytree(src, dst, dirs_exist_ok=True)

copytree(os.path.join(source, "assets"), os.path.join(destination, "assets"))
os.makedirs(katex_destination, exist_ok=True)
copytree(os.path.join(katex_source, "dist", "fonts"), os.path.join(katex_destination, "fonts"))
for f in ["katex.min.css", "katex.min.js"]:
    shutil.copyfile(os.path.join(katex_source, "dist", f), os.path.join(katex_destination, f))
shutil.copyfile(os.path.join(katex_source, "LICENSE"), os.path.join(katex_destination, "LICENSE"))
os.makedirs(os.path.join(plex_destination, "files"), exist_ok=True)
shutil.copyfile(os.path.join(plex_source, "index.css"), os.path.join(plex_destination, "index.css"))
for f in ["ibm-plex-sans-cyrillic-ext-wght-normal.woff2","ibm-plex-sans-cyrillic-wght-normal.woff2",
          "ibm-plex-sans-greek-wght-normal.woff2","ibm-plex-sans-vietnamese-wght-normal.woff2",
          "ibm-plex-sans-latin-ext-wght-normal.woff2","ibm-plex-sans-latin-wght-normal.woff2"]:
    shutil.copyfile(os.path.join(plex_source, "files", f), os.path.join(plex_destination, "files", f))
shutil.copyfile(os.path.join(plex_source, "LICENSE"), os.path.join(plex_destination, "LICENSE"))
shutil.copyfile(os.path.join(source, "styles.css"), os.path.join(destination, "styles.css"))
shutil.copyfile(os.path.join(source, "app.js"), os.path.join(destination, "app.js"))
open(os.path.join(destination, ".nojekyll"), "w").write("")
open(os.path.join(destination, "robots.txt"), "w").write(
    "User-agent: *\nAllow: /\nSitemap: https://calmyor.github.io/SEC-Enabled-MRAM-IMC/sitemap.xml\n")
urls = "\n".join(
    f'  <url><loc>https://calmyor.github.io/SEC-Enabled-MRAM-IMC/{"" if p["file"]=="index.html" else p["file"]}</loc></url>'
    for p in pages)
open(os.path.join(destination, "sitemap.xml"), "w").write(
    f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n')
print(f"Built {len(pages)} pages in {destination}")
