#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, '..');
const htmlArg = process.argv[2] || 'index.html';
const htmlPath = path.resolve(root, htmlArg);
const html = fs.readFileSync(htmlPath, 'utf8');
const atlas = JSON.parse(fs.readFileSync(path.join(root, 'atlas-data.json'), 'utf8'));
const sourceIndex = JSON.parse(fs.readFileSync(path.join(root, 'source-file-index.json'), 'utf8'));
const contract = JSON.parse(fs.readFileSync(path.join(root, 'source-availability.json'), 'utf8'));

if (contract.schemaVersion !== 1 || contract.policy !== 'explicit-source-availability') {
  throw new Error('Unexpected source availability contract schema/policy');
}
const allowed = new Set(['public-local', 'external-public', 'custody-only', 'unavailable']);
const indexedPaths = [...new Set(Object.values(sourceIndex).flat())];
const missing = indexedPaths.filter(p => !contract.entries[p]);
const extra = Object.keys(contract.entries).filter(p => !indexedPaths.includes(p));
const invalid = Object.entries(contract.entries).filter(([, row]) => !allowed.has(row.status));
if (missing.length || extra.length || invalid.length) {
  throw new Error(`Contract mismatch: missing=${missing.length} extra=${extra.length} invalid=${invalid.length}`);
}

const constantStart = html.indexOf('const sourceAvailabilityIndex = ');
if (constantStart < 0) throw new Error('sourceAvailabilityIndex constant missing from runtime');
const functionStart = html.indexOf('function sourceAvailability(');
const functionEnd = html.indexOf('function titleCase', functionStart);
if (functionStart < 0 || functionEnd < 0) throw new Error('source availability production functions missing');

const prefix = 'const sourceAvailabilityIndex = ';
const valueStart = constantStart + prefix.length;
const semi = html.indexOf(';', valueStart);
const embedded = JSON.parse(html.slice(valueStart, semi));
if (JSON.stringify(embedded) !== JSON.stringify(contract)) throw new Error('Embedded source availability contract is stale');

const context = { sourceAvailabilityIndex: embedded };
vm.createContext(context);
vm.runInContext(html.slice(functionStart, functionEnd), context);

let actionable = 0;
let custodyOnly = 0;
let unavailable = 0;
for (const p of indexedPaths) {
  const row = context.sourceAvailability(p);
  if (!row || !allowed.has(row.status)) throw new Error(`${p}: invalid runtime status`);
  if (context.sourceIsActionable(p)) actionable += 1;
  if (row.status === 'custody-only') custodyOnly += 1;
  if (row.status === 'unavailable') unavailable += 1;
}
if (!custodyOnly) throw new Error('Expected custody-only source records');
if (html.includes("files.map(f=>`<a class=\"file-link\"")) {
  throw new Error('Source renderer still turns every mapped source into an anchor');
}
if (!html.includes('Held in Atlas research corpus—not publicly served')) {
  throw new Error('Transparent custody-only drawer copy missing');
}
if (!html.includes('source-custody')) throw new Error('Custody-only source state markup missing');

const casesWithCustody = atlas.cases.filter(c => (c.sources || []).some(src => {
  const upper = String(src).toUpperCase();
  return Object.entries(sourceIndex).some(([token, paths]) => upper.includes(token.toUpperCase()) && paths.some(p => contract.entries[p]?.status === 'custody-only'));
})).length;

console.log(`Source availability OK: ${indexedPaths.length} indexed paths, ${actionable} actionable, ${custodyOnly} custody-only, ${unavailable} unavailable, ${casesWithCustody} cases disclose custody-only files`);
