"""Validate docs/ without node.

A port of scripts/validate-site.mjs, reporting the same failures in the same
order. node scripts/validate-site.mjs remains canonical.

    python3 scripts/validate_site.py
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
docs = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "docs")
pages = sorted(f for f in os.listdir(docs) if os.path.splitext(f)[1] == ".html")
failures = []

def count(source, pattern):
    return len(re.findall(pattern, source))

for page in pages:
    path = os.path.join(docs, page)
    html = open(path, encoding="utf8").read()
    if count(html, r'<main\b') != 1: failures.append(f"{page}: expected exactly one <main>")
    if count(html, r'<h1\b') != 1: failures.append(f"{page}: expected exactly one <h1>")
    if not re.search(r'<html lang="en">', html): failures.append(f"{page}: missing language declaration")
    if not re.search(r'<a class="skip-link" href="#main">', html): failures.append(f"{page}: missing skip link")
    if count(html, r'aria-current="page"') != 1: failures.append(f"{page}: expected one current nav item")
    if re.search(r'<img\b(?![^>]*\balt=)[^>]*>', html): failures.append(f"{page}: image missing alt text")
    if re.search(r'/Users/|usbmodem|GLOBALFOUNDRIES|\.gds\b|\.oas(?:is)?\b', html, re.I):
        failures.append(f"{page}: contains a private-path or implementation token")
    if re.search(r'\sdata-math="(?:inline|display)"', html): failures.append(f"{page}: contains unrendered math source")

    math_containers = count(html, r'\sdata-math-rendered="(?:inline|display)"')
    katex_containers = count(html, r'class="katex"')
    accessible_math = count(html, r'<math\b')
    if math_containers != katex_containers or math_containers != accessible_math:
        failures.append(f"{page}: expected one visual and accessible KaTeX tree per math expression")
    if math_containers and not re.search(r'href="assets/vendor/katex/katex\.min\.css"', html):
        failures.append(f"{page}: rendered math is missing the local KaTeX stylesheet")

    ids = re.findall(r'\bid="([^"]+)"', html)
    duplicates = [i for n, i in enumerate(ids) if ids.index(i) != n]
    if duplicates: failures.append(f"{page}: duplicate ids: {', '.join(sorted(set(duplicates)))}")

    references = re.findall(r'\b(?:href|src)="([^"]+)"', html)
    for reference in references:
        if re.match(r'^(?:https?:|mailto:|tel:|data:)', reference): continue
        parts = reference.split("#", 1)
        path_and_query = parts[0]
        fragment = parts[1] if len(parts) > 1 else ""
        relative_path = path_and_query.split("?", 1)[0]
        target = os.path.join(docs, relative_path) if relative_path else path
        if not os.path.exists(target):
            failures.append(f"{page}: missing local target {reference}")
            continue
        if fragment and os.path.splitext(target)[1] == ".html":
            target_html = html if os.path.abspath(target) == os.path.abspath(path) else open(target, encoding="utf8").read()
            if not re.search(r'\bid="' + re.escape(fragment) + r'"', target_html):
                failures.append(f"{page}: missing anchor {reference}")

if len(pages) != 7: failures.append(f"expected 7 HTML pages, found {len(pages)}")
if not os.path.exists(os.path.join(docs,"assets","og.png")): failures.append("missing social-preview image")
if not os.path.exists(os.path.join(docs,"assets","project-mark.svg")): failures.append("missing project mark")
for asset in ["katex.min.css","katex.min.js","LICENSE"]:
    if not os.path.exists(os.path.join(docs,"assets","vendor","katex",asset)):
        failures.append(f"missing KaTeX asset {asset}")
if not os.path.exists(os.path.join(docs,"assets","vendor","katex","fonts","KaTeX_Main-Regular.woff2")):
    failures.append("missing KaTeX web fonts")
for asset in ["index.css","LICENSE","files/ibm-plex-sans-latin-wght-normal.woff2"]:
    if not os.path.exists(os.path.join(docs,"assets","vendor","ibm-plex-sans",asset)):
        failures.append(f"missing IBM Plex Sans asset {asset}")

if failures:
    print(f"Site validation failed ({len(failures)}):", file=sys.stderr)
    for f in failures: print(f"- {f}", file=sys.stderr)
    sys.exit(1)
print(f"Validated {len(pages)} pages: structure, local links, images, navigation, and release-token scan passed.")
