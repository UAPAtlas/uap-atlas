#!/usr/bin/env python3
"""Regression gate for the bounded Release 05 source-depth completion tranche."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = 'assets/sources/PURSUE-RELEASE-05'
LANDING = 'https://www.war.gov/UFO/?releaseDate=Release+05&release=05'


def require(ok, message):
    if not ok:
        raise AssertionError(message)


def record(case, locator):
    return next((item for item in case.get('sourceRecords', []) if item.get('locator') == locator), None)


atlas = json.loads((ROOT / 'atlas-data.json').read_text())
by_id = {case['id']: case for case in atlas['cases']}
blackfile = json.loads((ROOT / 'blackfile-analysis.json').read_text())
index = json.loads((ROOT / 'source-file-index.json').read_text())

require(len(atlas['cases']) == 155, 'Release 05 completion must preserve the 155-case contract')
require(len(atlas.get('timeline', [])) == 153, 'Release 05 completion must preserve the 153-entry timeline contract')

# D099 cover is documentary hero, never event imagery.
ghost = by_id['BF-1946-GR-01']
d099_cover = f'{BASE}/DOW-UAP-D099-pdf-page-001.png'
require((ROOT / d099_cover).is_file(), 'D099 cover render missing')
require(ghost.get('image') == d099_cover, 'Ghost Rockets image must use the D099 cover')
require(ghost.get('heroVisual', {}).get('src') == d099_cover, 'Ghost Rockets hero must use the D099 cover')
require(ghost['heroVisual'].get('visualType') == 'official-intelligence-review-cover', 'D099 hero type must identify the publication cover')
require(ghost['heroVisual'].get('isEventEvidence') is False, 'D099 cover must not be event evidence')
require('not an image of a reported ghost rocket' in ghost['heroVisual'].get('evidenceStatus', ''), 'D099 documentary boundary missing')

# D100 is represented as three primary-record layers without becoming the missing Estimate.
estimate = by_id['BF-SF-07']
d100_sets = {
    'DOW-UAP-D100 · PDF pp. 1–3 and 7–9': [1, 7, 8],
    'DOW-UAP-D100 · PDF pp. 31–34': [34],
    'DOW-UAP-D100 · PDF pp. 232–244': [232, 240, 244],
}
for locator, pages in d100_sets.items():
    item = record(estimate, locator)
    require(item is not None, f'missing D100 source layer: {locator}')
    assert item is not None
    require(item.get('sha256') == '4052303ee0d521c15656b65fed3075734c83332ec5db319c744f0dbe53b8ec90', f'D100 custody hash mismatch: {locator}')
    require(item.get('sourcePageImages') == [f'{BASE}/DOW-UAP-D100-pdf-page-{page:03d}.png' for page in pages], f'D100 page mapping mismatch: {locator}')
joined_estimate = json.dumps(estimate, ensure_ascii=False)
for needle in ['inescapable', 'experimental “spaceships” or test vehicles', 'study request, not a finding', 'not the missing Estimate']:
    require(needle in joined_estimate, f'D100 boundary/detail missing: {needle}')
require(estimate['heroVisual']['src'].endswith('ESTIMATE-1948-Ruppelt-Report-half-title.png'), 'Estimate hero must remain the Ruppelt source image')
visible_estimate = estimate.get('primaryRecordUpdate', {})
require('inescapable' in json.dumps(visible_estimate, ensure_ascii=False), 'D100 default-visible acknowledgment missing')
require('study request, not a finding' in json.dumps(visible_estimate, ensure_ascii=False), 'D100 default-visible RAND boundary missing')
require('not the missing Estimate' in visible_estimate.get('boundary', ''), 'D100 default-visible Estimate identity boundary missing')

# D101 surfaces direct-source, geometry, dissemination, attachment and corrupted-DVR details without confidence inflation.
gom = by_id['BF-2021-GOM-01']
d101 = record(gom, 'DOW-UAP-D101 · PDF pp. 1–2, 5–6')
require(d101 is not None, 'expanded D101 primary record missing')
for needle in ['direct access via official duties', '0–20 feet', '15 seconds', '250–1,300 mph', 'corrupted full DVR', 'PowerPoint containing six embedded videos', 'not finally evaluated intelligence']:
    require(needle in json.dumps(gom, ensure_ascii=False), f'D101 detail/boundary missing: {needle}')
require(gom['confidence'] == 'CONFIRMED REPORT · NOT FINALLY EVALUATED', 'D101 confidence must not be elevated')
require(f'{BASE}/DOW-UAP-D101-pdf-page-002.png' in gom['images'], 'D101 direct-source narrative page missing from carousel')
require(f'{BASE}/DOW-UAP-D101-pdf-page-006.png' in gom['images'], 'D101 attachment page missing from carousel')
visible_gom = gom.get('primaryRecordUpdate', {})
for needle in ['0–20 feet', '250–1,300 mph', 'not finally evaluated intelligence']:
    require(needle in json.dumps(visible_gom, ensure_ascii=False), f'D101 default-visible detail/boundary missing: {needle}')

# Blackfile Q6/Q7 gain bounded D100 analysis without confidence changes.
q6 = next(q for q in blackfile['questions'] if q['id'] == 'q6')
q7 = next(q for q in blackfile['questions'] if q['id'] == 'q7')
require(q6['confidence'] == 'High · Very high for historical debunking policy and classified-aircraft cover', 'Q6 confidence changed')
require(q7['confidence'] == 'Very high for recurring institutional attention · Low-moderate for one hidden program', 'Q7 confidence changed')
for question in [q6, q7]:
    tension = next((t for t in question.get('tensions', []) if t.get('label') == 'Internal uncertainty versus public messaging'), None)
    require(tension is not None, f'{question["id"]} D100 tension missing')
    assert tension is not None
    require(tension.get('caseIds') == ['BF-SF-07'], f'{question["id"]} D100 tension case linkage mismatch')
    require('not proof of a hidden non-human program' in tension.get('summary', ''), f'{question["id"]} interpretation boundary missing')

# Source index and all new display files remain public-safe.
required = [
    d099_cover,
    *[f'{BASE}/DOW-UAP-D100-pdf-page-{p:03d}.png' for p in [1, 34, 232, 240, 244]],
    f'{BASE}/DOW-UAP-D101-pdf-page-002.png',
]
for path in required:
    require((ROOT / path).is_file(), f'missing display page: {path}')
for token in ['DOW-UAP-D099 · PDF p. 1', *d100_sets.keys(), 'DOW-UAP-D101 · PDF pp. 1–2, 5–6']:
    require(token in index and LANDING in index[token], f'source index mapping missing: {token}')
for name in ['atlas-data.json', 'blackfile-analysis.json', 'source-file-index.json']:
    text = (ROOT / name).read_text()
    for forbidden in ['/Users/', '/Volumes/', '/private/tmp/', "Cortana's Memory"]:
        require(forbidden not in text, f'{name} leaks host-local path: {forbidden}')
app = (ROOT / 'atlas-app.js').read_text()
html = (ROOT / 'index.html').read_text()
require('function primaryRecordUpdateHtml(c)' in app, 'default-visible primary-record renderer missing')
require('${primaryRecordUpdateHtml(c)}${evidenceLensHtml(c)}' in app, 'primary-record update not wired into Brief')
require('.primary-record-update{' in html and '.record-boundary b{' in html, 'primary-record update visual treatment missing')

print('PASS: Release 05 source-depth completion (D100, D101, Blackfile Q6/Q7, D099 hero)')
