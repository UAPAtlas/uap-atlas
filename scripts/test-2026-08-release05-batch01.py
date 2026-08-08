#!/usr/bin/env python3
"""Regression gate for PURSUE Release 05 enrichment Batch 01."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHANGED = {'BF-1946-GR-01', 'BF-1950-GF-01', 'BF-1952-TM-01', 'BF-SF-07'}
LANDING = 'https://www.war.gov/UFO/?releaseDate=Release+05&release=05'


def require(ok, message):
    if not ok:
        raise AssertionError(message)


def find_record(records, locator):
    for record in records:
        if record.get('locator') == locator:
            return record
    raise AssertionError(f'missing source record: {locator}')


def find_url(sources, url):
    for source in sources:
        if source.get('url') == url:
            return source
    raise AssertionError(f'missing public source: {url}')


atlas = json.loads((ROOT / 'atlas-data.json').read_text())
by_id = {case['id']: case for case in atlas['cases']}
require(len(atlas['cases']) >= 150, 'Batch 01 evidence must remain valid after later additive tranches')
require(CHANGED <= set(by_id), 'Batch 01 changed-case set is incomplete')

expected_pages = {
    'DOW-UAP-D098': ['assets/sources/PURSUE-RELEASE-05/DOW-UAP-D098-pdf-page-006.png', 'assets/sources/PURSUE-RELEASE-05/DOW-UAP-D098-pdf-page-009.png'],
    'DOW-UAP-D099': ['assets/sources/PURSUE-RELEASE-05/DOW-UAP-D099-pdf-page-005.png', 'assets/sources/PURSUE-RELEASE-05/DOW-UAP-D099-pdf-page-006.png'],
    'DOW-UAP-D100': ['assets/sources/PURSUE-RELEASE-05/DOW-UAP-D100-pdf-page-007.png', 'assets/sources/PURSUE-RELEASE-05/DOW-UAP-D100-pdf-page-008.png', 'assets/sources/PURSUE-RELEASE-05/DOW-UAP-D100-pdf-page-152.png'],
}
for doc_id, paths in expected_pages.items():
    for path in paths:
        require((ROOT / path).is_file(), f'missing Release 05 page render: {path}')
        require(path.endswith('.png'), f'Release 05 display path must be a browser-renderable image: {path}')

# Ghost Rockets: correct the over-broad summary and preserve the review-vs-event boundary.
ghost = by_id['BF-1946-GR-01']
d099 = find_record(ghost['sourceRecords'], 'DOW-UAP-D099 · PDF pp. 5–6')
d100_ghost = find_record(ghost['sourceRecords'], 'DOW-UAP-D100 · PDF p. 152')
require(d099['sha256'] == '59bdcb1406b50d7dab7f13dbce940eb247a0724c744100d34f9a53ea3209e2f4', 'D099 custody hash mismatch')
require(d100_ghost['sha256'] == '4052303ee0d521c15656b65fed3075734c83332ec5db319c744f0dbe53b8ec90', 'D100 Ghost Rockets custody hash mismatch')
require('2 or 3 real incidents' in ghost['keyQuote'], 'Ghost Rockets key quote must use the exact limited 1947 conclusion')
require(any('1,500 or 2,000' in x for x in ghost['evidenceBoundary']['notEstablished']), 'Ghost Rockets inflated-count boundary missing')
require(any('Soviet' in x for x in d099['limitations']), 'D099 hypothesis limitation missing')
require(any('institutional interest' in x for x in d100_ghost['limitations']), 'D100 Project SIGN interest/event boundary missing')
require(any('requested the complete Swedish Incidents file' in x for x in ghost['evidenceBoundary']['established']), 'Project SIGN file-request linkage missing')

# Film analysis: keep the analyst conclusion and methodological caveats together.
for cid in ['BF-1950-GF-01', 'BF-1952-TM-01']:
    case = by_id[cid]
    d098 = find_record(case['sourceRecords'], 'DOW-UAP-D098 · PDF pp. 6 and 9')
    require(d098['sha256'] == 'a8f271bb7bae396631eb3e35070fab285eb0d3258041b042b1a5a6b3e0d9c4f1', f'{cid} D098 custody hash mismatch')
    joined = json.dumps(d098)
    for needle in ['did not necessarily represent the official position', 'lacked proper equipment', 'Distance and trajectory assumptions']:
        require(needle in joined, f'{cid} D098 limitation missing: {needle}')
require('duplicate of a copy' in by_id['BF-1952-TM-01']['sourceQuality'], 'Tremonton film-generation limitation missing')

# Estimate: D100 adds institutional context, never the missing document itself.
estimate = by_id['BF-SF-07']
d100 = find_record(estimate['sourceRecords'], 'DOW-UAP-D100 · PDF pp. 7–8')
require(d100['sha256'] == '4052303ee0d521c15656b65fed3075734c83332ec5db319c744f0dbe53b8ec90', 'D100 custody hash mismatch')
require(any('does not contain the alleged Estimate' in x for x in d100['limitations']), 'D100/Estimate identity boundary missing')
require(any('DOW-UAP-D100 is the Estimate' in x for x in estimate['evidenceBoundary']['notEstablished']), 'Estimate non-identity boundary missing')
require('no tangible evidence' in estimate['gap'], 'Project SIGN physical-evidence boundary missing')

for cid in CHANGED:
    source = find_url(by_id[cid]['publicSources'], LANDING)
    require('custody' in (source.get('scope') or ''), f'{cid} Release 05 public source overstates evidentiary role')
    require(not any(str(path).lower().endswith('.pdf') for path in by_id[cid].get('images', [])), f'{cid} images array contains a PDF')

index = json.loads((ROOT / 'source-file-index.json').read_text())
for doc_id, paths in expected_pages.items():
    require(index.get(doc_id) == paths + [LANDING], f'{doc_id} source-index mapping mismatch')

for name in ['atlas-data.json', 'public-source-manifest.json', 'source-file-index.json']:
    text = (ROOT / name).read_text()
    require('/Users/' not in text and '/Volumes/' not in text and '/private/tmp/' not in text, f'{name} leaks a host-local path')

print('PASS: PURSUE Release 05 enrichment Batch 01 regression (20 audited; 4 enriched)')
