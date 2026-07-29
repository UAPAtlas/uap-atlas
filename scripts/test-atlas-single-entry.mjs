#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const indexPath = path.resolve(process.argv[2] || path.join(root, 'index.html'));
const legacyPath = path.resolve(process.argv[3] || path.join(root, 'atlas-mobile.html'));
const index = fs.readFileSync(indexPath, 'utf8');
const app = index.includes('/* ATLAS_MOBILE_JS_START */')
  ? index
  : fs.readFileSync(path.join(root, 'atlas-app.js'), 'utf8');
const legacy = fs.readFileSync(legacyPath, 'utf8');

const requireText = (text, needle, label) => {
  if (!text.includes(needle)) throw new Error(`Missing ${label}: ${needle}`);
};

requireText(index, '<title>UAP Atlas — Interactive Case Dossier</title>', 'shared Atlas title');
requireText(index, '/* ATLAS_MOBILE_CSS_START */', 'responsive CSS layer');
requireText(index, '<!-- ATLAS_MOBILE_NAV_START -->', 'responsive mobile navigation');
requireText(app, '/* ATLAS_MOBILE_JS_START */', 'responsive mobile controller');
requireText(app, "const isMobileAtlas=()=>mobileMedia.matches;", 'desktop/mobile behavior boundary');
requireText(app, "if(!isMobileAtlas()) return;", 'mobile-only event ownership');
requireText(index, "body:before{content:none!important;display:none!important;}", 'narrow-screen desktop-block override');

if (Buffer.byteLength(legacy) > 4096) throw new Error('atlas-mobile.html must remain a lightweight compatibility redirect');
requireText(legacy, "new URL('./', location.href)", 'legacy root redirect');
requireText(legacy, 'target.search = location.search;', 'legacy query preservation');
requireText(legacy, 'target.hash = location.hash;', 'legacy hash preservation');
requireText(legacy, 'location.replace(target.href);', 'legacy redirect execution');
if (legacy.includes('const atlasData =')) throw new Error('Legacy mobile route must not embed a second Atlas application');

console.log(`Atlas single-entry contract OK: ${path.basename(indexPath)} responsive; ${path.basename(legacyPath)} redirect-only`);
