import { access, readdir, readFile } from "node:fs/promises";
import { dirname, extname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const docs = join(root, "docs");
const pages = (await readdir(docs)).filter((file) => extname(file) === ".html").sort();
const failures = [];

function count(source, pattern) {
  return [...source.matchAll(pattern)].length;
}

async function exists(path) {
  try {
    await access(path);
    return true;
  } catch {
    return false;
  }
}

for (const page of pages) {
  const path = join(docs, page);
  const html = await readFile(path, "utf8");
  if (count(html, /<main\b/g) !== 1) failures.push(`${page}: expected exactly one <main>`);
  if (count(html, /<h1\b/g) !== 1) failures.push(`${page}: expected exactly one <h1>`);
  if (!/<html lang="en">/.test(html)) failures.push(`${page}: missing language declaration`);
  if (!/<a class="skip-link" href="#main">/.test(html)) failures.push(`${page}: missing skip link`);
  if (count(html, /aria-current="page"/g) !== 1) failures.push(`${page}: expected one current nav item`);
  if (/<img\b(?![^>]*\balt=)[^>]*>/g.test(html)) failures.push(`${page}: image missing alt text`);
  if (/\/Users\/|usbmodem|GLOBALFOUNDRIES|\.gds\b|\.oas(?:is)?\b/i.test(html)) failures.push(`${page}: contains a private-path or implementation token`);

  const ids = [...html.matchAll(/\bid="([^"]+)"/g)].map((match) => match[1]);
  const duplicates = ids.filter((id, index) => ids.indexOf(id) !== index);
  if (duplicates.length) failures.push(`${page}: duplicate ids: ${[...new Set(duplicates)].join(", ")}`);

  const references = [...html.matchAll(/\b(?:href|src)="([^"]+)"/g)].map((match) => match[1]);
  for (const reference of references) {
    if (/^(?:https?:|mailto:|tel:|data:)/.test(reference)) continue;
    const [relativePath, fragment] = reference.split("#", 2);
    const target = relativePath ? join(docs, relativePath) : path;
    if (!(await exists(target))) {
      failures.push(`${page}: missing local target ${reference}`);
      continue;
    }
    if (fragment && extname(target) === ".html") {
      const targetHtml = target === path ? html : await readFile(target, "utf8");
      const escaped = fragment.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
      if (!(new RegExp(`\\bid="${escaped}"`).test(targetHtml))) failures.push(`${page}: missing anchor ${reference}`);
    }
  }
}

if (pages.length !== 7) failures.push(`expected 7 HTML pages, found ${pages.length}`);
if (!(await exists(join(docs, "assets", "og.png")))) failures.push("missing social-preview image");

if (failures.length) {
  console.error(`Site validation failed (${failures.length}):`);
  failures.forEach((failure) => console.error(`- ${failure}`));
  process.exitCode = 1;
} else {
  console.log(`Validated ${pages.length} pages: structure, local links, images, navigation, and release-token scan passed.`);
}
