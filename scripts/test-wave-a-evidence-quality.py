#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
atlas = json.loads((ROOT / 'atlas-data.json').read_text())
source_index = json.loads((ROOT / 'source-file-index.json').read_text())
public_manifest = json.loads((ROOT / 'public-source-manifest.json').read_text())
cases = {case['id']: case for case in atlas['cases']}

assert len(cases) == 150

rb = cases['BF-1957-RB-01']
rb_text = json.dumps(rb).lower()
assert rb['sources'] == ['RB47-1957']
assert 'nara naid 28970538' in rb['sourceQuality'].lower()
assert 'later published technical analysis' in rb['sourceQuality'].lower()
assert 'four independent detection channels' not in rb_text
assert 'airborne radar' not in rb_text
assert rb['observation']['sensors'] == [
    'unaided-visual',
    'airborne-ECM-direction-finding',
    'ground-radar-reported-in-message',
]
assert rb['observation']['durationSeconds'] == 3120
assert rb['temporal']['startDateTime'] == '1957-07-17T10:10:00Z'
assert rb['temporal']['endDateTime'] == '1957-07-17T11:02:00Z'
assert rb['temporal']['durationSeconds'] == 3120
assert len([r for r in rb['sourceRecords'] if r.get('sourceType') != 'evidence-audit']) == 2

nc = cases['BF-1957-NC-01']
nc_text = json.dumps(nc).lower()
assert nc['sources'] == ['AIIRS-1957, NAID 311001910, raw objects 058-064']
assert 'first confirmed radar skinpaint of a uap' not in nc_text
assert 'intelligent tracking' not in nc_text
assert 'no conventional explanation offered' not in nc_text
assert 'suggested technical explanation' in nc['official'].lower()
assert '058–064' in nc['publicSources'][0]['note']
assert '258–264' in nc['publicSources'][0]['note']
assert 'not selected' in nc['publicSources'][0]['note'].lower()
assert nc['lat'] == 35.5 and nc['lon'] == -124.5
assert nc['geospatial']['geometry']['coordinates'] == [-124.5, 35.5]
assert '35°30′n, 124°30′w' in nc['coordinateBasis'].lower()

tehran = cases['BF-1976-TH-01']
tehran_text = json.dumps(tehran).lower()
assert tehran['sources'] == ['TEHRAN-1976']
assert 'usdao tehran' in tehran['sourceQuality'].lower()
assert 'single official message chain' in tehran['sourceQuality'].lower()
assert 'tower radar' not in tehran_text
assert tehran['observation']['independentWitnessGroups'] is None
assert all(item.startswith('Message reports') for item in tehran['sourceRecords'][0]['supports'])
assert 'causal link' in ' '.join(tehran['sourceRecords'][0]['limitations']).lower()
assert 'source-files/external/TEHRAN-1976-BlackVault-joint_chiefs_staff_report.pdf' in source_index['TEHRAN-1976']

omaha = cases['BF-2019-OM-01']
omaha_text = json.dumps(omaha).lower()
dvids_wrong = 'https://www.dvidshub.net/video/843593/navy-2019-west-coast-video'
debrief = 'https://thedebrief.org/pentagon-confirms-leaked-video-showing-transmedium-ufo-is-authentic/'
assert dvids_wrong not in json.dumps(omaha)
assert dvids_wrong not in source_index['OMAHA-2019']
assert debrief in source_index['OMAHA-2019']
assert debrief in [row['url'] for row in public_manifest['BF-2019-OM-01']]
assert 'perfect chain of custody' not in omaha_text
assert 'pentagon-authenticated shipboard footage' not in omaha_text
assert 'trans-medium candidate' not in omaha_text
assert 'official media custody exists' not in omaha_text
assert omaha['keyQuote'].startswith('I can confirm that the video was taken by Navy personnel')
assert 'reported by the debrief' in omaha['quoteSource'].lower()
assert 'uss omaha attribution remains secondary' in omaha['sourceQuality'].lower()
assert 'does not establish water entry' in ' '.join(omaha['sourceRecords'][0]['limitations']).lower()

print('PASS: Wave A evidence-quality regression (4 cases)')
