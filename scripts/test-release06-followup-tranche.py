#!/usr/bin/env python3
from __future__ import annotations
import json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
atlas = json.loads((ROOT/'atlas-data.json').read_text())
sfi = json.loads((ROOT/'source-file-index.json').read_text())
manifest = json.loads((ROOT/'public-source-manifest.json').read_text())
issues=[]
def req(ok,msg):
    if not ok: issues.append(msg)
def case(cid): return next((c for c in atlas['cases'] if c.get('id')==cid), None)
ids={c['id'] for c in atlas['cases']}
req(len(atlas['cases'])==159, 'Release06 follow-up should produce 159 cases')
req(len(atlas.get('timeline',[]))==157, 'Release06 follow-up should produce 157 timeline entries')
req(sum(1 for c in atlas['cases'] if c.get('mode')=='orbital')==26, 'orbital count must remain 26')
for cid in ['BF-1952-TM-01','BF-2022-ME-01','BF-1950-OK-01','BF-2023-CO-LE-01']:
    req(case(cid) is not None, f'{cid} missing')
    u=(case(cid) or {}).get('sourceUpdateCard') or {}
    req(u.get('findings') and u.get('limitations'), f'{cid} default-visible source update card missing findings/limitations')

tm=case('BF-1952-TM-01')
req('hot' in json.dumps(tm).lower() and 'without comment' in json.dumps(tm).lower(), 'Tremonton release-management language missing')
req('not proof' in json.dumps(tm).lower() or 'does not prove' in json.dumps(tm).lower(), 'Tremonton coverup boundary missing')
req('no range/speed/size/altitude/distance' in json.dumps(tm).lower() or 'range, speed, size, altitude or distance' in json.dumps(tm).lower(), 'Newhouse measurement boundary missing')
req(any('D102-pdf-page-037' in p for r in tm.get('sourceRecords',[]) for p in r.get('sourcePageImages',[])), 'Tremonton D102 p37 render missing')

me=case('BF-2022-ME-01')
obs=json.dumps(me.get('observation',{}))
req('USAF missile crew' not in obs and 'unaided-visual' not in obs, 'legacy D10 missile/unaided fields leaked into BF-2022-ME-01 observation')
req('sourceSpecificObservations' in obs and 'DOW-UAP-D10' in obs and 'DOW-UAP-D106' in obs and 'DOW-UAP-D109' in obs, 'source-specific D10/D106/D109 observations missing')
req('not merged' in json.dumps(me).lower() or 'not one merged' in json.dumps(me).lower(), 'D106/D109 non-collapse boundary missing')

ok=case('BF-1950-OK-01')
req('Guzi' in json.dumps(ok) and 'Oku' in json.dumps(ok) and ('Hedo' in json.dumps(ok) or 'Redo' in json.dumps(ok)), 'Okinawa named witness/location uncertainty missing')
req('no recovery' in json.dumps(ok).lower() or 'does not document recovery' in json.dumps(ok).lower(), 'Okinawa no-recovery boundary missing')
req('DOW-UAP-D105-OKINAWA-1950' in sfi, 'Okinawa source token missing')
req('BF-1950-OK-01' in manifest, 'Okinawa public manifest missing')

co=case('BF-2023-CO-LE-01')
coj=json.dumps(co)
req('300 ft' in coj and '15 minutes' in coj, 'Colorado transcript sighting details missing')
req('not radar tracking' in coj.lower() or 'does not say radar tracked' in coj.lower(), 'Colorado radar boundary missing')
req('native video' in coj.lower() and ('not embedded' in coj.lower() or 'absent' in coj.lower()), 'Colorado native-video boundary missing')
req('LLE-UAP-D001-COLORADO-2023' in sfi, 'Colorado source token missing')
req('BF-2023-CO-LE-01' in manifest, 'Colorado public manifest missing')
html=(ROOT/'atlas-app.js').read_text()
req('sourceUpdateCardHtml(c)' in html, 'Brief renderer source-update hook missing')
req('!/[A-Z0-9]/.test(before)&&!/[A-Z0-9]/.test(after)' in html, 'sourceTokens must use alphanumeric token boundaries so D10 does not match D105/D106/D109')
req('sourceFileIndex[c.sourceLocator]?[c.sourceLocator]:[]' in html, 'filesForCase must add explicit sourceLocator-indexed files')
ok_files=json.dumps(sfi.get('DOW-UAP-D105-OKINAWA-1950', []))
req('DOW-UAP-D105' in ok_files and 'DOW-UAP-D10-' not in ok_files, 'Okinawa evidence must resolve D105 pages, not D10 spillover')
req(all('DOW-UAP-D10-' not in json.dumps(r) for r in ok.get('sourceRecords', [])), 'Okinawa source records must not include D10 evidence')
for cid in ['BF-1950-OK-01','BF-2023-CO-LE-01']:
    req(any(t.get('caseId')==cid and t.get('id') and t.get('type') and t.get('desc') for t in atlas.get('timeline',[])), f'{cid} timeline entry missing required id/type/desc')
for tok in ['DOW-UAP-D105-OKINAWA-1950','LLE-UAP-D001-COLORADO-2023','DOW-UAP-D10-ME-2022']:
    for rel in sfi[tok]:
        if rel.startswith('assets/'):
            req((ROOT/rel).exists(), f'source-index asset missing: {rel}')
if issues:
    print('RELEASE06 FOLLOWUP FAIL')
    for i in issues: print('-', i)
    sys.exit(1)
print('RELEASE06 FOLLOWUP PASS')
print(json.dumps({'cases':len(atlas['cases']),'timeline':len(atlas.get('timeline',[])),'added':['BF-1950-OK-01','BF-2023-CO-LE-01'],'changedExisting':['BF-1952-TM-01','BF-2022-ME-01']}, indent=2))
