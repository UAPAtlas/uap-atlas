#!/usr/bin/env python3
from __future__ import annotations
import json, pathlib, re, sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
atlas=json.loads((ROOT/'atlas-data.json').read_text())
case=next(c for c in atlas['cases'] if c.get('id')=='BF-1978-VL-01')
tl=next(t for t in atlas['timeline'] if t.get('id')=='TL-1978A')
sfi=json.loads((ROOT/'source-file-index.json').read_text())
manifest=json.loads((ROOT/'public-source-manifest.json').read_text())
issues=[]
def req(ok,msg):
    if not ok: issues.append(msg)
req(case['date']=='21 OCT 1978','case date must be exact 21 OCT 1978')
req(case['temporal']['precision']=='day' and '1978-10-21' in case['temporal']['startDateTime'],'temporal day precision/start date missing')
req(case['keyQuote']=="it is hovering and it's not an aircraft",'exact keyQuote mismatch')
req('The reason for the disappearance of the aircraft has not been determined.' in case['official'],'official unresolved conclusion missing')
req('compatible' in json.dumps(case).lower() and 'not identified as VH-DSJ debris' in case['gap'],'cowl flap compatibility/not-identified boundary missing')
req('bunkering fuel oil' in json.dumps(case),'oil lab finding missing')
req('radar-analysis memo is not a raw object track' in case['gap'],'radar memo/raw track boundary missing')
req('historical 2012' in json.dumps(case).lower() and 'remain restricted today' in json.dumps(case).lower(),'historical access-mask boundary missing')
req('SAR p.106 concerns different aircraft' in json.dumps(case),'SAR p106 exclusion missing')
req('original flight-service audio' in json.dumps(case) and 'raw radar/sensor provenance' in json.dumps(case),'open original audio/raw sensor targets missing')
req('VALENTICH-B1497-1978' in sfi and len(sfi['VALENTICH-B1497-1978'])==1,'B1497 scoped source token missing or broad')
req('VALENTICH-A4703-SAR' in sfi and len(sfi['VALENTICH-A4703-SAR'])==1,'A4703 scoped source token missing or broad')
for tok in ['VALENTICH-B1497-1978','VALENTICH-A4703-SAR']:
    for rel in sfi[tok]:
        req((ROOT/rel).exists(), f'source-index path missing: {rel}')
        req(rel.startswith('source-files/public-mirrors/VALENTICH-1978/'), f'source token {tok} not scoped: {rel}')
req(len(case['sourceRecords'])==7,'expected 7 Valentich source records including audit')
req(case.get('sourceUpdateCard') and len(case['sourceUpdateCard']['findings'])==4 and len(case['sourceUpdateCard']['limitations'])==3,'default source-update card incomplete')
req(tl['date']=='21 OCT 1978' and 'cause was not determined' in tl['desc'],'timeline TL-1978A not reconciled')
req(any('B1497' in r.get('label','') and 'Black Vault' in r.get('publisher','') for r in manifest['BF-1978-VL-01']),'public manifest B1497 mirror missing')
req(any('A4703' in r.get('label','') and 'Black Vault' in r.get('publisher','') for r in manifest['BF-1978-VL-01']),'public manifest A4703 mirror missing')
html=(ROOT/'atlas-app.js').read_text()
req('sourceUpdateCardHtml(c)' in html,'renderer does not include source update card in default Brief')
# no PDFs in visual imagery fields
visual=json.dumps({k:case.get(k) for k in ['image','images','heroVisual']})
req('.pdf' not in visual.lower(),'PDF leaked into visual media fields')
if issues:
    print('VALENTICH INTEGRATION FAIL')
    for i in issues: print('-',i)
    sys.exit(1)
print('VALENTICH INTEGRATION PASS')
print(json.dumps({
 'caseId':case['id'], 'timelineId':tl['id'], 'sourceRecords':len(case['sourceRecords']),
 'sourceIndexTokens':['VALENTICH-B1497-1978','VALENTICH-A4703-SAR'],
 'publicManifestRows':len(manifest['BF-1978-VL-01']),
 'acquisitionTargets':len(case.get('acquisitionTargets',[])),
 'sourceUpdateFindings':len(case['sourceUpdateCard']['findings']),
 'sourceUpdateLimitations':len(case['sourceUpdateCard']['limitations'])
}, indent=2))
