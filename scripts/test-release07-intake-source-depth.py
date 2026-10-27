#!/usr/bin/env python3
"""Release 07 source-depth and 28-object intake contract."""
import json,re
from pathlib import Path
root=Path(__file__).resolve().parents[1]
data=json.loads((root/'atlas-data.json').read_text())
ledger=json.loads((root/'research/pursue-release07-intake-ledger.json').read_text())
rows=ledger['files'];assert len(rows)==ledger['expectedCount']==28
assert sum(x['pdfPages'] for x in rows)==1139
assert all(x.get('mirrorHashMatch') is True and re.fullmatch(r'[a-f0-9]{64}',x.get('sha256','')) for x in rows)
assert len({x['filename'] for x in rows})==28
assert not any(x['filename'].lower().endswith(('.mp4','.mov')) for x in rows)
ids={}
for row in rows:
 match=re.match(r'((?:DOW|FBI|EOP|USG)-UAP-D\d+)',row['filename'])
 assert match,row['filename']
 ids[match.group(1)]=row
assert len(ids)==28
cases={c['id']:c for c in data['cases']}
program=cases['BF-SF-09'];nimitz=cases['BF-2004-NM-01']
for ident in ['DOW-UAP-D168','DOW-UAP-D173','DOW-UAP-D174','DOW-UAP-D175']:
 r=ids[ident];matches=[s for s in program['sourceRecords'] if s.get('sha256')==r['sha256']]
 assert len(matches)==1,(ident,len(matches))
 s=matches[0]
 assert s['url']==r['sourceUrl'] and s['supports'] and s['limitations']
 assert 'contractor-produced' in s['provenance']
assert len([s for s in nimitz['sourceRecords'] if s.get('sha256')==ids['DOW-UAP-D175']['sha256']])==1
assert 'not newly recovered radar data' in nimitz['keyFact']
assert 'ordinary animals' in program['keyFact']
assert '0.5 to 10 seconds' in nimitz['sourceQuality']
assert 'no transferred non-human material' in program['sourceQuality']
assert 'ordinary canine/raccoon' in program['sourceUpdateCard']['findings'][0]
assert 'not a transfer' in program['sourceUpdateCard']['limitations'][0]
assert 'not newly released SPY-1 radar data' in nimitz['sourceUpdateCard']['limitations'][0]
app=(root/'atlas-app.js').read_text()
assert 'sourceUpdateCardHtml(c)' in app and 'sourceUpdateCardHtml(c)}' in app
assert all('/Volumes/' not in s and '/Users/' not in s for s in [(root/'research/pursue-release07-intake-ledger.json').read_text(),(root/'research/pursue-release07-intake-review-2026-10-27.md').read_text()])
# Strict scope is checked against the reviewed base before committing; CI checks
# the permanent source and custody contract after the base itself advances.
print('Release 07 intake/source-depth contract OK: 28 records, 1139 pages, 2 existing cases, 0 added cases')
