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
const appSource = html.includes('function lensRecords')
  ? html
  : fs.readFileSync(path.join(root, 'atlas-app.js'), 'utf8');
const atlas = JSON.parse(fs.readFileSync(path.join(root, 'atlas-data.json'), 'utf8'));
const triage = JSON.parse(fs.readFileSync(path.join(root, 'qa/atlas_operational_triage.json'), 'utf8'));

const start = appSource.indexOf('function lensRecords');
const end = appSource.indexOf('function heroTypeLabel', start);
if (start < 0 || end < 0) throw new Error('Evidence Lens production functions not found');
const context = {};
vm.createContext(context);
vm.runInContext(appSource.slice(start, end), context);

const expectedAcquisition = new Set(triage.cases.filter(c => c.category === 'acquisition_target').map(c => c.id));
const actualAcquisition = new Set();
for (const c of atlas.cases) {
  const records = context.lensRecords(c);
  if (!records.length) throw new Error(`${c.id}: no Evidence Lens records`);
  const boundary = records.find(r => (r.supports || []).length && (r.limitations || []).length);
  if (!boundary) throw new Error(`${c.id}: no bounded Evidence Lens record`);
  if (context.lensCustody(c, records).label === 'Acquisition required') actualAcquisition.add(c.id);
}

const missing = [...expectedAcquisition].filter(id => !actualAcquisition.has(id));
const extra = [...actualAcquisition].filter(id => !expectedAcquisition.has(id));
if (missing.length || extra.length) throw new Error(`Acquisition mismatch; missing=${missing.join(',')} extra=${extra.join(',')}`);

const expected = {
  'BF-1961-BH-01': ['Official + supporting records', 'Mapped custody', 'High'],
  'BF-1987-GB-01': ['Media / image record', 'Acquisition required', 'Medium'],
  'BF-SF-09': ['Official + supporting records', 'Mapped custody', 'High'],
  'BF-1949-SA-01': ['Primary / official record', 'Mapped custody', 'High'],
  'BF-1994-AR-01': ['Witness / investigator trail', 'Acquisition required', 'High'],
  'BF-1986-JAL-01': ['Primary / official record', 'Mapped custody', 'High'],
  'BF-2004-NM-01': ['Official + supporting records', 'Mapped custody', 'High'],
  'BF-1980-PE-01': ['Primary / official record', 'Mapped custody', 'High'],
  'BF-1966-CC-00': ['Official + supporting records', 'Mapped custody', 'High'],
  'BF-1951-YK-01': ['Primary / official record', 'Mapped custody', 'High'],
  'BF-1955-USSR-01': ['Primary / official record', 'Mapped custody', 'High'],
};
for (const [id, want] of Object.entries(expected)) {
  const c = atlas.cases.find(row => row.id === id);
  const records = context.lensRecords(c);
  const got = [context.lensEvidenceClass(c, records), context.lensCustody(c, records).label, context.lensQuoteSignal(c)];
  if (JSON.stringify(got) !== JSON.stringify(want)) throw new Error(`${id}: got ${JSON.stringify(got)} want ${JSON.stringify(want)}`);
}
console.log(`Evidence Lens OK: ${atlas.cases.length} cases, ${actualAcquisition.size} acquisition targets, ${Object.keys(expected).length} representative labels`);
