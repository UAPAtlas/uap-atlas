#!/usr/bin/env python3
"""RED/GREEN regression for Release 05 new-case tranche 01."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANDING = 'https://www.war.gov/UFO/?releaseDate=Release+05&release=05'
NEW_IDS = {'BF-1964-PR-01', 'BF-2021-GOM-01', 'BF-2026-RL-01'}
DOC_HASHES = {
    'CIA-UAP-D022': '358b0d2e45ff0320f4e4ad689f0c918362d6c5d36be765d386018d279d835b01',
    'CIA-UAP-D023': 'aba51f51191bbcd37dc1f591171b6edc78c9bfb9632cfed8fae6a8bf1d61ca40',
    'DOW-UAP-D101': '926f4cf9a852d77bca34e8e7370c4a9da386610a6ba799e060de71c2339b0e92',
    'FBI-UAP-D037': 'df8741ec7bee9778646142e3c2c55c050e3c58d067fa1049683ccd1126f0110a',
    'FBI-UAP-D040': '978ac7226c7ec06f4561c3986732183e3bf2aa4f07c03430daa9111a20eec77e',
}


def require(ok, message):
    if not ok:
        raise AssertionError(message)


def case_record(case, locator):
    return next((r for r in case.get('sourceRecords', []) if r.get('locator') == locator), None)


atlas = json.loads((ROOT / 'atlas-data.json').read_text())
sync_script = (ROOT / 'scripts/sync_atlas_runtime_data.py').read_text()
by_id = {c['id']: c for c in atlas['cases']}
require(len(atlas['cases']) >= 150, 'Release 05 tranche baseline must retain at least 150 cases')
require(len(atlas['timeline']) >= 148, 'Release 05 tranche baseline must retain at least 148 entries')
require('DERIVED_CASE_FIELDS = (' in sync_script, 'runtime synchronizer must use deterministic ordered derived-field iteration')
require(NEW_IDS <= set(by_id), f'missing new cases: {sorted(NEW_IDS - set(by_id))}')
require({t.get('caseId') for t in atlas['timeline']} >= NEW_IDS, 'each new case must have a timeline entry')

# Tremonton: recovered D098 must replace the stale summaries-only claim.
tremonton = by_id['BF-1952-TM-01']
require('survives only in summaries' not in json.dumps(tremonton), 'stale Tremonton summaries-only claim remains')
require('exact 4 may 1953' in tremonton['official'].lower(), 'Tremonton official field must acknowledge the recovered exact 1953 report')
require('duplicate of a copy' in json.dumps(tremonton).lower(), 'Tremonton copy-generation caveat missing')

# Puerto Rico / Gyatt: pilot + radar custody + alternatives without extraordinary-origin inflation.
pr = by_id['BF-1964-PR-01']
require(pr['year'] == 1964 and pr['date'] == '16–24 NOV 1964' and pr['mode'] == 'approximate', 'Puerto Rico chronology/precision mismatch')
require(all(str(day) in pr['summary'] for day in [16, 17, 18, 19, 24]), 'Puerto Rico event-family dates are incomplete')
require('USS Gyatt' in json.dumps(pr) and 'F-8C' in json.dumps(pr), 'Puerto Rico platform chain missing')
require('original radar film' in json.dumps(pr).lower(), 'Puerto Rico radar-film custody missing')
require('YF-12A' in json.dumps(pr) and 'MiG-21' in json.dumps(pr), 'Puerto Rico competing aircraft analysis missing')
require(any('absent' in x.lower() for x in pr['evidenceBoundary']['notEstablished']), 'Puerto Rico missing-media boundary missing')
for locator, doc_id in [('CIA-UAP-D022 · PDF pp. 3–4 and 6', 'CIA-UAP-D022'), ('CIA-UAP-D023 · PDF pp. 1–2', 'CIA-UAP-D023')]:
    rec = case_record(pr, locator)
    require(rec and rec['sha256'] == DOC_HASHES[doc_id], f'{doc_id} source record/hash missing')

# Gulf of Oman: preserve IIR status, sensor chain, and missing attachment boundary.
gom = by_id['BF-2021-GOM-01']
blob = json.dumps(gom)
for needle in ['AC-130', 'EO/IR', 'approximately 25', 'not finally evaluated', 'six embedded videos']:
    require(needle.lower() in blob.lower(), f'Gulf of Oman boundary missing: {needle}')
require(not any('DOD_111887' in str(x) for x in gom.get('images', [])), 'anonymous videos must not be attributed to Gulf of Oman')
rec = case_record(gom, 'DOW-UAP-D101 · PDF pp. 1–2, 5–6')
require(rec and rec['sha256'] == DOC_HASHES['DOW-UAP-D101'], 'D101 source record/hash missing')

# 2026 field event: one case, two corroborating interviews, reconstructions clearly non-evidentiary.
rl = by_id['BF-2026-RL-01']
blob = json.dumps(rl)
for needle in ['Night Optical Devices', '25 minutes', 'dry wash', '6 to 10']:
    require(needle.lower() in blob.lower(), f'2026 field-event detail missing: {needle}')
require('BF-2023-WUS-03' in rl.get('relatedCaseIds', []), '2026/2023 related-but-separate link missing')
for locator, doc_id in [('FBI-UAP-D037 · PDF pp. 1–3', 'FBI-UAP-D037'), ('FBI-UAP-D040 · PDF pp. 1–2', 'FBI-UAP-D040')]:
    rec = case_record(rl, locator)
    require(rec and rec['sha256'] == DOC_HASHES[doc_id], f'{doc_id} source record/hash missing')
require(rl['heroVisual']['isEventEvidence'] is False, '2026 reconstruction must not be marked event evidence')
require('reconstruction' in rl['heroVisual']['visualType'], '2026 hero visual must be classified as reconstruction')

# Source/custody contract and public-safe files.
index = json.loads((ROOT / 'source-file-index.json').read_text())
for doc_id in ['CIA-UAP-D022', 'CIA-UAP-D023', 'DOW-UAP-D101', 'FBI-UAP-D037', 'FBI-UAP-D038', 'FBI-UAP-D039', 'FBI-UAP-D040', 'FBI-UAP-D041', 'FBI-UAP-D042']:
    require(doc_id in index, f'missing source-index key: {doc_id}')
    require(LANDING in index[doc_id], f'missing official release landing page: {doc_id}')
for cid in NEW_IDS:
    require(any(s.get('url') == LANDING and 'custody' in s.get('scope', '') for s in by_id[cid]['publicSources']), f'{cid} official release custody source missing')
    require(not any(str(x).lower().endswith(('.pdf', '.mp4')) for x in by_id[cid].get('images', [])), f'{cid} visual array contains non-display media')

for name in ['atlas-data.json', 'public-source-manifest.json', 'source-file-index.json']:
    text = (ROOT / name).read_text()
    for prefix in ['/Users/', '/Volumes/', '/private/tmp/', 'file://']:
        require(prefix not in text, f'{name} leaks host-local path: {prefix}')

print('PASS: Release 05 new-case tranche 01 (Tremonton correction + 3 new cases)')
