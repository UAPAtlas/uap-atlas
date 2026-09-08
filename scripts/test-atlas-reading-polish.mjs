#!/usr/bin/env node
import { readFileSync } from 'node:fs';
import { createServer } from 'node:http';
import { extname, join, normalize } from 'node:path';
import { pathToFileURL } from 'node:url';
import process from 'node:process';

const root = process.cwd();
const htmlPath = process.argv[2] || 'index.html';
const html = readFileSync(join(root, htmlPath), 'utf8');
const app = readFileSync(join(root, 'atlas-app.js'), 'utf8');
const assert = (ok, msg) => { if (!ok) throw new Error(msg); };

assert(!/Last sync/i.test(html), 'footer must not label a ticking local clock as Last sync');
assert(/Local time/i.test(html), 'footer should label the clock as Local time');
assert(!/Classification\s*&nbsp;\s*\/\/|Restricted|Data sources verified/i.test(html), 'footer must avoid restrictive/blanket verification labels');
assert(/Public archive custody/i.test(html) && /source boundaries/i.test(html), 'footer should use precise public archive/source-boundary language');
assert(/function visualRoleLabel/.test(app), 'app should centralize visual role labels');
assert(/detail-media-role/.test(app), 'preview hero should expose the image role label');
assert(/carousel-role-badge/.test(app), 'carousel stage should expose the image role label');
assert(/case-row-title/.test(app) && /case-row-meta/.test(app), 'case rows should render title-first with secondary metadata');
assert(/dossier-lede/.test(app), 'dossier should render title-first key finding/source-boundary lede before media');
assert(/minmax\(0,1fr\) 260px/.test(html), 'desktop Case Stack row should be at least 260px high for readability');
assert(/width:\s*200px/.test(html), 'desktop Case Stack search should be at least 200px wide');

if (process.argv.includes('--static-only')) {
  console.log('atlas reading polish static contract passed');
  process.exit(0);
}
const mime = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.svg': 'image/svg+xml' };
const server = createServer((req, res) => {
  const url = new URL(req.url, 'http://127.0.0.1');
  let file = normalize(url.pathname.replace(/^\/+/, '')) || htmlPath;
  if (file === '/') file = htmlPath;
  const full = join(root, file);
  if (!full.startsWith(root)) { res.writeHead(403); res.end('forbidden'); return; }
  try { res.writeHead(200, { 'content-type': mime[extname(full)] || 'application/octet-stream' }); res.end(readFileSync(full)); }
  catch { res.writeHead(404); res.end('not found'); }
});
await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
const port = server.address().port;
try {
  const pw = await import(process.env.PLAYWRIGHT_MODULE || 'playwright');
  const chromium = pw.default?.chromium || pw.chromium;
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  const desktop = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
  await desktop.goto(`http://127.0.0.1:${port}/${htmlPath}`, { waitUntil: 'networkidle' });
  await desktop.waitForTimeout(2000);
  const footer = await desktop.locator('.console-footer').innerText();
  assert(/LOCAL TIME/i.test(footer) && !/LAST SYNC|RESTRICTED|VERIFIED/i.test(footer), `bad footer copy: ${footer}`);
  const searchBox = await desktop.locator('#caseSearch').boundingBox();
  assert(searchBox && searchBox.width >= 200, `desktop search too narrow: ${searchBox?.width}`);
  const caseListBox = await desktop.locator('.list-panel').boundingBox();
  assert(caseListBox && caseListBox.height >= 260, `case stack too short: ${caseListBox?.height}`);
  const previewRole = await desktop.locator('.detail-media-role').first().innerText();
  assert(/context|not event imagery/i.test(previewRole), `Magenta preview role unclear: ${previewRole}`);
  await desktop.locator('[data-open-case="BF-1933-MG-01"]').last().click();
  await desktop.locator('.dossier-lede').waitFor();
  const ledeText = await desktop.locator('.dossier-lede').innerText();
  assert(/Key finding/i.test(ledeText) && /Source boundary/i.test(ledeText), `dossier lede missing required framing: ${ledeText}`);
  const firstRole = await desktop.locator('.carousel-role-badge').first().innerText();
  assert(/context|not event imagery/i.test(firstRole), `carousel role unclear: ${firstRole}`);

  const mobile = await browser.newPage({ viewport: { width: 390, height: 844 }, isMobile: true });
  await mobile.goto(`http://127.0.0.1:${port}/${htmlPath}#page=cases`, { waitUntil: 'networkidle' });
  await mobile.locator('[data-page="cases"]').click();
  const rowText = await mobile.locator('.case-row').first().innerText();
  const titleBox = await mobile.locator('.case-row .case-row-title').first().boundingBox();
  const idBox = await mobile.locator('.case-row .case-row-meta').first().boundingBox();
  assert(titleBox && idBox && titleBox.y <= idBox.y, `mobile row is not title-first: ${rowText}`);
  const beforeDrawer = await mobile.locator('#drawerBackdrop.open').count();
  await mobile.locator('.case-row').first().click();
  await mobile.waitForTimeout(100);
  assert(await mobile.locator('body[data-mobile-page="map"]').count(), 'mobile row click should select map page');
  assert(beforeDrawer === 0 && await mobile.locator('#drawerBackdrop.open').count() === 0, 'mobile row click must not open dossier');
  await browser.close();
} finally {
  await new Promise(resolve => server.close(resolve));
}
console.log('atlas reading polish regression passed');
