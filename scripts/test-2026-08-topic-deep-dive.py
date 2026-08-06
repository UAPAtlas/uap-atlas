#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def require(ok, message):
    if not ok:
        raise AssertionError(message)

atlas = json.loads((ROOT / 'atlas-data.json').read_text())
by_id = {case['id']: case for case in atlas['cases']}

# New primary-record event case.
require('BF-1960-HF-01' in by_id, 'Hartford archival event case is missing')
hartford = by_id['BF-1960-HF-01']
require(hartford['date'] == '4 SEP 1960', 'Hartford event date must remain 4 September 1960')
require(hartford['location'].startswith('Hartford'), 'Hartford event must not be collapsed into the separate Woodbridge fall')
require(hartford['sourceLocator'].startswith('NARA NAID 28989015'), 'Hartford exact NARA locator missing')
require(any('furnace slag' in x.lower() for x in hartford['evidenceBoundary']['established']), 'Blue Book card disposition missing')
require(any('aluminum' in x.lower() and 'observed fall' in x.lower() for x in hartford['evidenceBoundary']['established']), 'underlying laboratory nuance missing')
require(any('Woodbridge' in x for x in hartford['evidenceBoundary']['notEstablished']), 'Hartford/Woodbridge chronology boundary missing')

manifest_path = ROOT / 'assets/evidence/HARTFORD-1960/HARTFORD-1960-NARA-NAID-28989015-download-manifest.json'
manifest = json.loads(manifest_path.read_text())
require(manifest['acquisition']['objectCountExpected'] == 73, 'Hartford NARA expected count must be 73')
require(manifest['acquisition']['objectCountVerified'] == 73, 'Hartford NARA verified count must be 73')
selected = [o for o in manifest['objects'] if o['includedInAtlas']]
require(len(selected) == 10, 'exactly ten page-adjudicated Hartford scans should be public')
for obj in selected:
    require((ROOT / obj['atlasPath']).is_file(), f"missing selected scan: {obj['atlasPath']}")
manifest_text = manifest_path.read_text()
require('/Users/' not in manifest_text and '/private/tmp/' not in manifest_text, 'deployable manifest leaks a host-local path')

# Existing special files are enriched rather than duplicated.
brown = by_id['BF-SF-03']
require(any('28989015' in json.dumps(record) for record in brown['sourceRecords']), 'Brown file lacks Hartford NARA source family')
require(any('ARL-TR-3005' in json.dumps(record) for record in brown['sourceRecords']), 'Brown file lacks DTIC ARL technical boundary')
require('BF-1960-HF-01' in brown['relatedCaseIds'], 'Brown file must link to Hartford event')

kona = by_id['BF-SF-09']
require(any('499915937' in json.dumps(record) for record in kona['sourceRecords']), 'KONA BLUE NARA custody record missing')
require(any('Lockheed' in json.dumps(record) and 'Knapp' in json.dumps(record) for record in kona['sourceRecords']), 'Lockheed/Bigelow testimony record missing')
require(any('not completed' in x.lower() or 'not establish' in x.lower() for x in kona['evidenceBoundary']['notEstablished']), 'Lockheed transfer completion boundary missing')

institutional = by_id['BF-SF-10']
require(any('Borland' in json.dumps(record) and 'BAE Systems' in json.dumps(record) for record in institutional['sourceRecords']), 'Borland/BAE congressional record missing')
require(any(lead.get('name') == "Project Rubik's Cube" and lead.get('status') == 'unsubstantiated-public-lead' for lead in institutional.get('openLeads', [])), 'Rubik’s Cube must remain an unsubstantiated lead')
require('American Alchemy' in json.dumps(institutional) and 'extremely hinted' in json.dumps(institutional) and 'cannot confirm or deny' in json.dumps(institutional), 'timestamped Borland interview boundaries missing')
require(any('running the show' in x.lower() or 'control the government' in x.lower() for x in institutional['evidenceBoundary']['notEstablished']), 'ICIG/NHI-control boundary missing')

# Historical/theological material stays analysis-only inside Q2.
analysis = json.loads((ROOT / 'blackfile-analysis.json').read_text())
q2 = next(q for q in analysis['questions'] if q['id'] == 'q2')
briefs = q2.get('supplementalAnalysis', [])
brief = next((b for b in briefs if b.get('id') == 'ancient-watchers-catholic-nhi'), None)
require(brief is not None, 'Q2 ancient-text/Catholic-NHI analysis brief missing')
require(brief['classification'] == 'interpretive-analysis-only', 'religious brief must remain analysis-only')
brief_text = json.dumps(brief)
for needle in ['1 Enoch', 'not part of the Catholic deuterocanon', 'Ethiopian Orthodox', 'Paul Thigpen', 'does not prove']:
    require(needle in brief_text, f'analysis brief missing boundary: {needle}')

runtime = (ROOT / 'blackfile-analysis.js').read_text()
require('ancient-watchers-catholic-nhi' in runtime, 'Blackfile runtime not synchronized')
mode = (ROOT / 'blackfile-mode.js').read_text()
require('bf-supplemental-analysis' in mode, 'Blackfile renderer lacks supplemental-analysis support')

print('topic deep-dive regression checks passed')
