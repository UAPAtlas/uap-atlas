#!/usr/bin/env python3
"""Release 07 one-event-family triangle testimony and source boundaries."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
a=json.loads((root/'atlas-data.json').read_text())
cases={c['id']:c for c in a['cases']}
c=cases['BF-2026-TR-01']
t=[t for t in a['timeline'] if t.get('caseId')==c['id']]
assert len(t)==1 and t[0]['id']=='TL-2026-TR-01'
assert set(c['sources'])=={'DOW-UAP-D176','FBI-UAP-D043'}
assert c['temporal']['durationSeconds'] is None and c['observation']['durationSeconds'] is None
assert '1923' in c['summary'] and '2023' in c['summary']
assert 'three seconds' in c['summary'] and '10 + 20 + 2–3 seconds' in c['summary']
assert c['confidenceModel']=={'record':'confirmed','anomaly':'undetermined','provenance':'primary-source'}
assert c['mode']=='redacted' and c['coordinatePrecision']=='country-redacted-generalized'
assert c['heroVisual']['visualType']=='official-document-page' and c['heroVisual']['isEventEvidence'] is False
assert 'LOWER-CONFIDENCE TESTIMONY' in c['confidence']
assert 'unverified illustrations' in c['heroFact'] and 'not event imagery' in c['heroFact']
assert all(s in c['heroFact'] for s in ('1923','2023','~3 seconds','10 + 20 + 2–3 seconds'))
assert len(c['sourceRecords'])==2
assert c['sourceFamilyRelationship']=='same-witness-event'
profile=next(row['sourceProfile'] for row in json.loads((root/'qa/source-depth-enrichment-candidates.json').read_text()) if row['id']==c['id'])
assert profile['label']=='linked-primary-records' and profile['independentSourceFamilies']==1
idx=json.loads((root/'source-file-index.json').read_text())
manifest=json.loads((root/'public-source-manifest.json').read_text())
availability=json.loads((root/'source-availability.json').read_text())['entries']
ledger={r['filename'].split('-',3)[0]+'-'+r['filename'].split('-',3)[1]+'-'+r['filename'].split('-',3)[2]:r for r in json.loads((root/'research/pursue-release07-intake-ledger.json').read_text())['files']}
for token,pages in [('DOW-UAP-D176',[1,2,3]),('FBI-UAP-D043',[1,2])]:
 r=next(x for x in c['sourceRecords'] if x['citation'].startswith(token))
 assert r['sha256']==ledger[token]['sha256'] and r['url']==ledger[token]['sourceUrl']
 assert len(r['sourcePageImages'])==len(pages)
 assert idx[token]==r['sourcePageImages']+[r['url']]
 for path in r['sourcePageImages']:
  assert (root/path).is_file() and availability[path]['status']=='public-local'
 assert any(x['url']==r['url'] for x in manifest[c['id']])
assert all('event photograph' not in x['supports'] for x in c['sourceRecords'])
assert 'instrumented speed measurement' in c['gap']
assert 'not an FBI factual finding' in c['official']
assert len(a['cases'])==163 and len(a['timeline'])==161
print('RELEASE07 TRIANGLE TESTIMONY PASS: one case / two official records / conflicting chronologies preserved')
