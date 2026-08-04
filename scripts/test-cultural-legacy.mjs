#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const data=JSON.parse(fs.readFileSync(path.join(root,'atlas-data.json'),'utf8'));
const html=fs.readFileSync(process.argv[2]||path.join(root,'atlas-fresh.html'),'utf8');
const appPath=path.join(root,'atlas-app.js');
const uiSource=html.includes('function culturalLegacyHtml(c)')
  ? html
  : `${html}\n${fs.existsSync(appPath)?fs.readFileSync(appPath,'utf8'):''}`;
const cases=data.cases.filter(c=>(c.culturalLegacy||[]).length);
if(!cases.length) throw new Error('No Cultural Legacy records found');
if(!cases.some(c=>c.id==='BF-SF-13')) throw new Error('Billy Meier Cultural Legacy record missing');
for(const c of cases){
  const evidence=new Set([c.image,c.heroVisual?.src,...(c.images||[]),...(c.evidenceImages||[])].filter(Boolean));
  for(const item of c.culturalLegacy){
    for(const key of ['title','year','image','imageAlt','connection','contextStatus','sourceLabel','sourceUrl','credit','imageSourceUrl']){
      if(!item[key]) throw new Error(`${c.id}: culturalLegacy missing ${key}`);
    }
    const licensed=Boolean(item.license&&item.licenseUrl);
    const sourceCredited=Boolean(item.rightsStatus);
    if(!licensed&&!sourceCredited) throw new Error(`${c.id}: culturalLegacy requires license metadata or rightsStatus`);
    if(item.contextStatus!=='Cultural context — not case evidence') throw new Error(`${c.id}: invalid evidence boundary`);
    if(!/^https:\/\//.test(item.sourceUrl)||!/^https:\/\//.test(item.imageSourceUrl)||(item.licenseUrl&&!/^https:\/\//.test(item.licenseUrl))) throw new Error(`${c.id}: cultural source/license URLs must use HTTPS`);
    if(!item.image.startsWith('assets/context/')) throw new Error(`${c.id}: cultural image must live under assets/context/`);
    if(!fs.existsSync(path.join(root,item.image))) throw new Error(`${c.id}: missing cultural image ${item.image}`);
    if(evidence.has(item.image)) throw new Error(`${c.id}: cultural image leaked into evidence imagery`);
  }
}
for(const required of ['function culturalLegacyHtml(c)','class="cultural-legacy"','Context · Not evidence']){
  if(!uiSource.includes(required)) throw new Error(`Cultural Legacy UI missing: ${required}`);
}
console.log(`Cultural Legacy OK: ${cases.length} case(s), ${cases.reduce((n,c)=>n+c.culturalLegacy.length,0)} documented artifact(s)`);
