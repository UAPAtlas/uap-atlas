#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, '..');
const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const atlas = JSON.parse(fs.readFileSync(path.join(root, 'atlas-data.json'), 'utf8'));
const triage = JSON.parse(fs.readFileSync(path.join(root, 'qa/atlas_operational_triage.json'), 'utf8'));

const start = html.indexOf('function lensRecords');
const end = html.indexOf('function heroTypeLabel', start);
if (start < 0 || end < 0) throw new Error('Evidence Lens production functions not found');
const context = {};
vm.createContext(context);
vm.runInContext(html.slice(start, end), context);

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
  'BF-1961-BH-01': ['Official + supporting records', 'Acquisition required', 'High'],
  'BF-1987-GB-01': ['Media / image record', 'Acquisition required', 'Medium'],
  'BF-SF-09': ['Multiple official records', 'Mapped custody', 'High'],
  'BF-1949-SA-01': ['Primary / official record', 'Mapped custody', 'High'],
  'BF-1994-AR-01': ['Witness / investigator trail', 'Acquisition required', 'Contextual'],
};
for (const [id, want] of Object.entries(expected)) {
  const c = atlas.cases.find(row => row.id === id);
  const records = context.lensRecords(c);
  const got = [context.lensEvidenceClass(c, records), context.lensCustody(c, records).label, context.lensQuoteSignal(c)];
  if (JSON.stringify(got) !== JSON.stringify(want)) throw new Error(`${id}: got ${JSON.stringify(got)} want ${JSON.stringify(want)}`);
}
console.log(`Evidence Lens OK: ${atlas.cases.length} cases, ${actualAcquisition.size} acquisition targets, 5 representative labels`);
