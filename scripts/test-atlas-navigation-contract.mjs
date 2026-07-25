#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const desktopPath = process.argv[2] || 'atlas-fresh.html';
const mobilePath = process.argv[3] || 'atlas-mobile.html';
const read = p => fs.readFileSync(path.resolve(root, p), 'utf8');
const desktop = read(desktopPath);
const mobile = read(mobilePath);
const failures = [];
const requireMatch = (condition, message) => { if (!condition) failures.push(message); };

// Desktop Case Stack selection focuses the map; dossier opening remains explicit.
requireMatch(
  /function renderCaseList\(\)[\s\S]*?const choose=\(\)=>selectCase\(el\.dataset\.id,true\)/.test(desktop),
  'desktop Case Stack rows must select and zoom the case'
);
requireMatch(
  /function renderDetail\(\)[\s\S]*?data-open-case=[\s\S]*?openFullCase\(btn\.dataset\.openCase\)/.test(desktop),
  'desktop preview must retain an explicit dossier-opening action'
);
requireMatch(
  /if\(e\.key==='Enter'&&\(tag==='button'\|\|e\.target\.closest\?\.\('\.case-row'\)\)\) return/.test(desktop),
  'desktop Case Stack keyboard selection must not bubble into the global dossier shortcut'
);

// Mobile Case Stack selection must return to/focus the map, not open the dossier.
requireMatch(
  /function focusMobileCaseFromStack\(id\)\{\s*selectCase\(id,true\);\s*setMobilePage\('map'\);\s*\}/.test(mobile),
  'mobile Case Stack selection must select, zoom, and route to the map'
);
requireMatch(
  /caseList\.addEventListener\('click',[\s\S]*?focusMobileCaseFromStack\(id\)/.test(mobile),
  'mobile Case Stack click handler must use the map-focus path'
);
requireMatch(
  /caseList\.addEventListener\('keydown',[\s\S]*?focusMobileCaseFromStack\(id\)/.test(mobile),
  'mobile Case Stack keyboard handler must use the map-focus path'
);
requireMatch(
  !/caseList\.addEventListener\('click',[\s\S]{0,350}?setMobilePage\('dossier'\)/.test(mobile),
  'mobile Case Stack click must not open the dossier'
);
requireMatch(
  /function setMobilePage\(page,[\s\S]*?else\{[\s\S]*?drawerBackdrop[\s\S]*?classList\.remove\('open'\)[\s\S]*?urlCaseId=null/.test(mobile),
  'mobile Map/Cases transitions must close stale dossier state'
);
requireMatch(
  /getElementById\('peekOpen'\)\?\.addEventListener\('click',\(\)=>setMobilePage\('dossier'\)\)/.test(mobile),
  'mobile map peek must retain an explicit dossier-opening action'
);

if (failures.length) {
  console.error(`Atlas navigation contract FAILED (${failures.length})`);
  failures.forEach((failure, i) => console.error(`${i + 1}. ${failure}`));
  process.exit(1);
}
console.log(`Atlas navigation contract OK: ${desktopPath} + ${mobilePath}`);
