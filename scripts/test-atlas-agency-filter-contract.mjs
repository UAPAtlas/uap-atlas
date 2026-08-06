#!/usr/bin/env node
import fs from 'node:fs';
import vm from 'node:vm';

const appPath=process.argv[2] || 'atlas-app.js';
const dataPath=process.argv[3] || 'atlas-data.json';
const app=fs.readFileSync(appPath,'utf8');
const cases=JSON.parse(fs.readFileSync(dataPath,'utf8')).cases;
const failures=[];
const requireCheck=(ok,msg)=>{if(!ok) failures.push(msg);};

function extractFunction(name){
  const start=app.indexOf(`function ${name}(`);
  if(start<0) return '';
  const brace=app.indexOf('{',start);
  let depth=0;
  for(let i=brace;i<app.length;i++){
    if(app[i]==='{') depth++;
    else if(app[i]==='}' && --depth===0) return app.slice(start,i+1);
  }
  return '';
}

const labelsMatch=app.match(/const AGENCY_FILTER_LABELS=Object\.freeze\(\{[\s\S]*?\}\);/);
const labelsSource=labelsMatch?.[0] || '';
const canonicalSource=extractFunction('canonicalAgencyKey');
const keysSource=extractFunction('caseAgencyKeys');
requireCheck(Boolean(labelsSource),'AGENCY_FILTER_LABELS table is required');
requireCheck(Boolean(canonicalSource),'canonicalAgencyKey helper is required');
requireCheck(Boolean(keysSource),'caseAgencyKeys helper is required');
requireCheck(/function buildFilters\(\)[\s\S]*?caseAgencyKeys\(c\)/.test(app),'dropdown counts must use canonical case agency keys');
requireCheck(/function matchesFilters\(c\)[\s\S]*?caseAgencyKeys\(c\)\.includes\(state\.filters\.agency\)/.test(app),'case filtering must use canonical case agency keys');
requireCheck(/state\.filters\.agency==='nasa'/.test(app),'NASA stack routing must use its canonical filter key');

if(labelsSource && canonicalSource && keysSource){
  const sandbox={};
  vm.runInNewContext(`${labelsSource}\n${canonicalSource}\n${keysSource}\nthis.canonicalAgencyKey=canonicalAgencyKey;this.caseAgencyKeys=caseAgencyKeys;`,sandbox);
  const keys=(agency)=>Array.from(sandbox.caseAgencyKeys({agency}));
  const has=(agency,key)=>keys(agency).includes(key);

  requireCheck(has('USAF / 4602D AISS','usaf'),'USAF / 4602D AISS must normalize to USAF');
  requireCheck(has('USAF / Blue Book','usaf'),'USAF / Blue Book must normalize to USAF');
  requireCheck(has('USAF / RAF','usaf') && has('USAF / RAF','raf'),'split USAF / RAF must contribute to both canonical agencies');
  requireCheck(has('U.S. AIR FORCE / NARA','usaf'),'U.S. AIR FORCE spelling must normalize to USAF');
  requireCheck(has('USN / AARO','usn') && has('USN / AARO','aaro'),'USN / AARO must contribute to both canonical agencies');
  requireCheck(has('U.S. Navy / Blue Book','usn'),'U.S. Navy spelling must normalize to USN');
  requireCheck(has('CIA / OSI','cia'),'CIA subdivisions must normalize to CIA');
  requireCheck(has('DOW / AARO RELEASE','dow') && has('DOW / AARO RELEASE','aaro'),'DOW / AARO release labels must aggregate both agencies');
  requireCheck(has('Civilian / USAF film analysis','civilian') && has('Civilian / USAF film analysis','usaf'),'civilian / USAF composite labels must preserve both useful filters');

  requireCheck(!has('Brazilian Air Force','usaf'),'Brazilian Air Force must remain distinct from USAF');
  requireCheck(!has('US Army Air Forces','usaf'),'historical US Army Air Forces must not be merged into USAF');
  requireCheck(!has('Civilian / RAAF','raf'),'RAAF must remain distinct from RAF');

  const counts=new Map();
  for(const c of cases){
    for(const key of keys(c.agency)) counts.set(key,(counts.get(key)||0)+1);
  }
  const visible=[...counts.entries()].filter(([,count])=>count>=2).map(([key])=>key);
  requireCheck(visible.filter(key=>key==='usaf').length===1,'dropdown must contain one canonical USAF option');
  requireCheck(counts.get('usaf')===29,`canonical USAF count must aggregate 29 records (got ${counts.get('usaf')})`);
  requireCheck(counts.get('nasa')===26,`canonical NASA count must remain 26 (got ${counts.get('nasa')})`);
  requireCheck(!visible.includes('4602d-aiss') && !visible.includes('blue-book'),'components and projects must not become agency options');
}

if(failures.length){
  console.error(`Atlas agency filter contract FAILED (${failures.length})`);
  failures.forEach((failure,i)=>console.error(`${i+1}. ${failure}`));
  process.exit(1);
}
console.log('ATLAS AGENCY FILTER CONTRACT OK: canonical aliases, one USAF option, aggregated counts');
