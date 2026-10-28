#!/usr/bin/env python3
"""Idempotent, scoped Release 07 new-case admission: three adjudicated cases + timeline entries.

Adjudicated via page-level primary review of DOW-UAP-D155, D156, D158.
All three returned ADD with bounded evidence: documented records, not
verified anomalous craft. See research/pursue-release07-new-case-admission-review.md
and research/pursue-release07-intake-review-2026-10-27.md for the full rationale.
"""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ATLAS = ROOT / 'atlas-data.json'
LEDGER = ROOT / 'research/pursue-release07-intake-ledger.json'
records = json.loads(LEDGER.read_text())['files']

def record_id(filename):
    m = re.match(r'((?:DOW|FBI|EOP|USG)-UAP-D\d+)', filename)
    assert m, filename
    return m.group(1)

by_id = {record_id(r['filename']): r for r in records}
for key in ('DOW-UAP-D155', 'DOW-UAP-D156', 'DOW-UAP-D158'):
    assert by_id[key]['sha256'] and by_id[key]['mirrorHashMatch'] is True

def src(key, citation, locator, supports, limitations):
    r = by_id[key]
    return {'citation': citation,
            'sourceType': 'air-intelligence-information-report',
            'provenance': 'Department of War PURSUE Release 07; air intelligence information report in official release custody. Public GitHub mirror SHA-256 independently matches archive metadata; official-origin byte identity not independently verified.',
            'locator': locator,
            'url': r['sourceUrl'],
            'sha256': r['sha256'],
            'supports': supports,
            'limitations': limitations}

# ── D155: Saudi Arabia B-52 gunnery-radar contact (18 Jan 1957) ──────────────
d155 = src('DOW-UAP-D155',
    'DOW-UAP-D155 · Air Intelligence Information Report IR-1-57, Saudi Arabia, 1957',
    'PDF p. 1 narrative; p. 2 schematic; duplicate copies pp. 3–5',
    ['A-3A gunnery-scope return reportedly remained near 6,000 yards for five to seven minutes aboard B-52 aircraft 394 near 27°N, 47°E at 39,000 feet.',
     'Return disappeared following ownship left bank; report states disappearance may have resulted from the B-52 change of direction.',
     'Report identifies 22d Bombardment Wing, 328th Bombardment Squadron, call sign Runner 11, and gunner M/Sgt C.E. Ballew.'],
    ['No visual sighting, independent radar confirmation, raw radar recording, or calibrated tracking history accompanies the report.',
     'Ownship speed of 642 knots is B-52 speed, not measured target speed; the schematic is a drawing, not scope photography.',
     'The simultaneously displayed known B-52 is a comparison return on the same sensor, not independent corroboration.',
     'Smaller return amplitude does not establish smaller physical size; approximate constant range does not demonstrate formation flight without heading and sensor records.'])

# ── D156: Guam F-86D blinking-light encounter (31 Dec 1956 Zulu) ────────────
d156 = src('DOW-UAP-D156',
    'DOW-UAP-D156 · Air Intelligence Information Report IR-7-57, Guam, 1956',
    'PDF pp. 1–4; p. 5 is a mirrored duplicate of p. 4',
    ['1st Lt Ted Brunson, 41st Fighter-Interceptor Squadron, reported one blinking white light passing below his F-86D, turning with him, apparently climbing and circling for approximately ten minutes.',
     'A lighted weather balloon launched at 1432Z was last tracked at 1500Z at 20,000 feet; investigators noted slower-than-standard ascent.',
     'Investigator Capt Alan G. Pound concluded a malfunctioned balloon that leveled off or descended could possibly explain the reported sighting.'],
    ['One pilot witness; no supporting observers, no radar corroboration, and no discernible silhouette documented.',
     'Pilot rejected the balloon identification because he believed the light maneuvered with and accelerated past his aircraft; that objection is his interpretation, not independent balloon exclusion.',
     'Aircraft altitude listed as 26,000 feet MSL while narrative describes movement at approximately 20,000 feet and estimated climb to 30,000 feet; do not flatten into one measured target altitude.'])

# ── D158: Prince George airport guards' light report (8 Nov 1953) ───────────
d158 = src('DOW-UAP-D158',
    'DOW-UAP-D158 · Flying Object Report, 918th AC&W Squadron, Prince George, Canada, 1953',
    'PDF pp. 1, 3–4; p. 2 is a reverse-side bleed-through scan',
    ['Two USAF guards guarding a B-29 at Prince George Airport reported one round white-with-blue-tint light initially appearing like a falling star.',
     'Light reportedly approached within approximately 150 feet, remained motionless about 30 seconds, rose straight up about 300 feet, remained motionless nearly 10 seconds, then climbed westward and was lost to distance.',
     '918th AC&W Squadron intelligence officer Capt James F. Mitchell signed the report; no interception or identification action was taken.'],
    ['Ground visual, unaided; no radar, no optical aids, no physical evidence, and no independent instrumental measurement.',
     'Two guards are one co-located group, not two independently documented accounts; all distances and movements are visual estimates.',
     'Disappearance elevation printed as 135° is a source ambiguity; do not silently correct it or derive a trajectory.',
     'Meteor was the initial impression but does not explain the subsequently reported multi-minute stationary phases if those perceptions were accurate.'])

NEW_CASES = [
    {
        'id': 'BF-1957-SA-01',
        'title': 'Saudi Arabia — B-52 Gunnery-Radar Contact',
        'date': '18 JAN 1957',
        'year': 1957,
        'location': 'Saudi Arabia, near reported ownship position 27°N, 47°E',
        'mode': 'approximate',
        'lon': 47.0, 'lat': 27.0,
        'expectedCountry': 'Saudi Arabia',
        'geometryExpectation': 'country',
        'coordinatePrecision': 'region',
        'coordinateBasis': 'Approximate source-stated aircraft position at 27°N, 47°E; not an independently located target',
        'agency': 'USAF / 22d Bombardment Wing (M)',
        'domain': 'MILITARY / SENSOR',
        'status': 'DOCUMENTED · UNRESOLVED',
        'confidence': 'CONFIRMED RECORD · UNRESOLVED IDENTITY',
        'summary': 'A contemporaneous air intelligence report (IR-1-57) records an unexpected A-3A gunnery-radar return aboard B-52 aircraft 394 near Saudi Arabia on 18 January 1957. The return reportedly remained near 6,000 yards for five to seven minutes before disappearing following an ownship left bank. No visual sighting, independent radar confirmation, or raw radar recording accompanies the report.',
        'keyFact': 'A single A-3A gunnery-scope return reportedly persisted near 6,000 yards for five to seven minutes and disappeared after the B-52 banked left; the report states the disappearance may have resulted from the aircraft change of direction.',
        'heroFact': 'A B-52 gunner reported an unexpected radar return that persisted for minutes and disappeared when the aircraft turned; no visual, independent radar, or raw recording accompanied the report.',
        'keyQuote': 'The disappearance may have been caused by the change in direction of the B-52.',
        'quoteSource': 'DOW-UAP-D155, Air Intelligence Information Report IR-1-57, PDF p. 1',
        'quoteConfidence': 'confirmed-primary-source-quotation',
        'significance': 'Moderate significance',
        'official': 'The 22d Bombardment Wing intelligence report labels the return an unidentified aircraft sighting. It records one crew gunner source and an explanatory radar schematic; it does not state an extraordinary origin or provide independent confirmation.',
        'gap': 'Raw radar or mission records, tanker-traffic correlation, radar operating geometry, independent sensor evidence, and final investigative disposition are unavailable in this packet.',
        'whyItMatters': 'A documented airborne radar report from a named B-52 crew with a specific gunnery scope, preserving the ownship-maneuver alternative rather than asserting anomalous motion.',
        'sources': ['DOW-UAP-D155'],
        'sourceLabel': 'USAF air intelligence report (IR-1-57)',
        'sourceLocator': 'DOW-UAP-D155, PDF pp. 1–2',
        'relatedCaseIds': ['BF-1957-RB-01'],
        'caseTypes': ['military-encounter'],
        'evidenceModes': ['radar'],
        'environment': ['military-airspace'],
        'outcome': 'documented',
        'confidenceModel': {'record': 'confirmed', 'anomaly': 'not-assessed', 'provenance': 'primary-record'},
        'sourceQuality': 'Primary official air intelligence report (IR-1-57) from the 22d Bombardment Wing, released through PURSUE Release 07; one gunner source and an explanatory radar schematic. No visual sighting, independent radar, raw radar recording, or calibrated tracking. Smaller return amplitude does not establish physical size.',
        'sourceRecords': [d155],
        'temporal': {'dateLabel': '18 JAN 1957', 'year': 1957, 'startDateTime': None, 'endDateTime': None, 'timezone': 'UTC', 'durationSeconds': 360, 'precision': 'minute', 'eventForm': 'single-event'},
        'geospatial': {'geometry': {'type': 'Point', 'coordinates': [47.0, 27.0]}, 'role': 'representative-centroid', 'precision': 'region', 'uncertaintyKm': 300, 'basis': 'Approximate source-stated aircraft position at 27°N, 47°E; not an independently located target'},
        'observation': {'witnessCount': None, 'witnessRoles': ['B-52 gunner M/Sgt C.E. Ballew'], 'sensors': ['A-3A gunnery-radar'], 'durationSeconds': 360, 'independentWitnessGroups': 1},
        'phenomena': {'shapes': ['unresolved-radar-return'], 'objectCount': 1, 'luminosity': None, 'motion': ['persisted-at-constant-range', 'disappeared-after-ownship-bank'], 'effects': []},
        'publicSources': [{'label': 'War.gov — PURSUE Release 07', 'url': 'https://www.war.gov/ufo/', 'publisher': 'U.S. Department of War', 'access': 'Public official release landing page', 'scope': 'official-release-custody', 'note': 'Official custody page for DOW-UAP-D155. The report documents one gunnery-radar return; it does not establish extraordinary origin or independent confirmation.'}],
        'evidenceBoundary': 'Documented airborne radar report; no visual sighting, independent radar, raw recording, or extraordinary kinematics established.',
    },
    {
        'id': 'BF-1956-GU-01',
        'title': 'Guam F-86D Blinking-Light Encounter',
        'date': '31 DEC 1956',
        'year': 1956,
        'location': 'Airborne over Guam radio-range holding pattern',
        'mode': 'approximate',
        'lon': 144.8, 'lat': 13.5,
        'expectedCountry': 'Guam',
        'geometryExpectation': 'offshore',
        'coordinatePrecision': 'offshore-region',
        'coordinateBasis': 'Approximate regional placement near Guam; exact encounter position unknown',
        'agency': 'USAF / 41st Fighter-Interceptor Squadron',
        'domain': 'MILITARY / VISUAL',
        'status': 'DOCUMENTED · UNRESOLVED',
        'confidence': 'CONFIRMED RECORD · UNRESOLVED IDENTITY',
        'summary': 'A contemporaneous air intelligence report (IR-7-57) records a 31 December 1956 F-86D pilot encounter with a blinking white light near Guam. 1st Lt Ted Brunson reported the light passing below his aircraft, turning with him, and remaining beyond interception despite afterburner use for approximately ten minutes. Investigators confirmed a lighted weather balloon launched that day and concluded a malfunctioned balloon could possibly explain the sighting.',
        'keyFact': 'A pilot reported a maneuvering blinking light that he could not intercept, while investigators documented a contemporaneous weather balloon and explicitly retained a malfunctioned-balloon alternative.',
        'heroFact': 'A pilot reported a maneuvering light he could not intercept; investigators confirmed a weather balloon launched that day and retained a malfunctioned-balloon explanation.',
        'keyQuote': 'If the balloon had malfunctioned and leveled off or descended, it could possibly explain the reported UFOB.',
        'quoteSource': 'DOW-UAP-D156, Air Intelligence Information Report IR-7-57, PDF p. 4',
        'quoteConfidence': 'confirmed-primary-source-quotation',
        'significance': 'Moderate significance',
        'official': 'The 41st Fighter-Interceptor Squadron intelligence report labels the sighting unidentified while qualifying that a lighted balloon could account for it. The investigator retained the balloon alternative rather than adopting the pilot rejection.',
        'gap': 'No radar corroboration, no supporting observers, no discernible silhouette, and no independent exclusion of the documented weather balloon.',
        'whyItMatters': 'A case that preserves both the pilot maneuvering-light report and the investigator contemporaneous balloon alternative, preventing the pilot objection from becoming a resolved anomalous-craft identification.',
        'sources': ['DOW-UAP-D156'],
        'sourceLabel': 'USAF air intelligence report (IR-7-57)',
        'sourceLocator': 'DOW-UAP-D156, PDF pp. 1–4',
        'relatedCaseIds': ['BF-1957-SA-01'],
        'caseTypes': ['military-encounter'],
        'evidenceModes': ['visual'],
        'environment': ['military-airspace'],
        'outcome': 'documented',
        'confidenceModel': {'record': 'confirmed', 'anomaly': 'not-assessed', 'provenance': 'primary-record'},
        'sourceQuality': 'Primary official air intelligence report (IR-7-57) prepared by Capt Alan G. Pound, released through PURSUE Release 07; one pilot witness, no radar, no supporting observers. A lighted weather balloon was launched that day and the investigator explicitly retained a malfunctioned-balloon explanation.',
        'sourceRecords': [d156],
        'temporal': {'dateLabel': '31 DEC 1956', 'year': 1956, 'startDateTime': '1956-12-31T16:10:00Z', 'endDateTime': '1956-12-31T16:20:00Z', 'timezone': 'UTC', 'durationSeconds': 600, 'precision': 'minute', 'eventForm': 'single-event'},
        'geospatial': {'geometry': {'type': 'Point', 'coordinates': [144.8, 13.5]}, 'role': 'representative-centroid', 'precision': 'offshore-region', 'uncertaintyKm': 200, 'basis': 'Approximate regional placement near Guam; exact encounter position unknown'},
        'observation': {'witnessCount': 1, 'witnessRoles': ['F-86D pilot 1st Lt Ted Brunson'], 'sensors': ['unaided-visual'], 'durationSeconds': 600, 'independentWitnessGroups': 1},
        'phenomena': {'shapes': ['unresolved-light'], 'objectCount': 1, 'luminosity': 'blinking white light', 'motion': ['turning-with-aircraft', 'apparent-climb', 'beyond-interception'], 'effects': []},
        'publicSources': [{'label': 'War.gov — PURSUE Release 07', 'url': 'https://www.war.gov/ufo/', 'publisher': 'U.S. Department of War', 'access': 'Public official release landing page', 'scope': 'official-release-custody', 'note': 'Official custody page for DOW-UAP-D156. The report documents a pilot visual encounter with a contemporaneous balloon alternative; it does not establish extraordinary origin.'}],
        'evidenceBoundary': 'Documented pilot visual report with a retained conventional alternative; no radar, no independent confirmation, no balloon exclusion established.',
    },
    {
        'id': 'BF-1953-PG-01',
        'title': 'Prince George Airport Guards\u2019 Light Report',
        'date': '8 NOV 1953',
        'year': 1953,
        'location': 'Prince George Airport, Prince George, British Columbia, Canada',
        'mode': 'approximate',
        'lon': -122.8, 'lat': 53.9,
        'expectedCountry': 'Canada',
        'expectedAdmin1': 'British Columbia',
        'geometryExpectation': 'admin1',
        'coordinatePrecision': 'city',
        'coordinateBasis': 'Published public coordinate for Prince George Airport',
        'agency': 'USAF / 918th AC&W Squadron',
        'domain': 'MILITARY / VISUAL',
        'status': 'DOCUMENTED · IDENTITY UNDETERMINED',
        'confidence': 'CONFIRMED RECORD · IDENTITY UNDETERMINED',
        'summary': 'On 8 November 1953, two USAF guards guarding a B-29 at Prince George Airport, British Columbia, reported a round white-with-blue-tint light that approached, hovered, rose, and climbed westward over approximately four minutes. The 918th AC&W Squadron intelligence officer signed the report; no radar, optical aids, or physical evidence were documented.',
        'keyFact': 'Two guards reported a hovering and climbing light over approximately four minutes, but no radar, optical, or instrumental corroboration accompanies the report; all distances and movements are visual estimates.',
        'heroFact': 'Two guards at a Canadian airport reported a light that hovered and climbed over four minutes; no radar, optical instruments, or physical evidence accompanied the report.',
        'keyQuote': 'None reported as unidentified.',
        'quoteSource': 'DOW-UAP-D158, Flying Object Report, 918th AC&W Squadron, PDF p. 4',
        'quoteConfidence': 'confirmed-primary-source-quotation',
        'significance': 'Low-to-moderate significance',
        'official': 'The 918th AC&W Squadron report records the guards account and states no interception or identification action was taken. The preparing officer recorded the cause as unknown.',
        'gap': 'No radar track, no optical instruments, no physical evidence, no independent instrumental measurement, and no independent witness group beyond the two co-located guards.',
        'whyItMatters': 'A bounded military visual-report case that preserves the multi-phase hover-and-climb description without sensor corroboration or measured dimensions.',
        'sources': ['DOW-UAP-D158'],
        'sourceLabel': 'USAF flying object report (918th AC&W Squadron)',
        'sourceLocator': 'DOW-UAP-D158, PDF pp. 1, 3–4',
        'relatedCaseIds': ['BF-1957-SA-01'],
        'caseTypes': ['military-encounter'],
        'evidenceModes': ['visual'],
        'environment': ['military-airspace'],
        'outcome': 'documented',
        'confidenceModel': {'record': 'confirmed', 'anomaly': 'not-assessed', 'provenance': 'primary-record'},
        'sourceQuality': 'Primary official flying object report from the 918th AC&W Squadron, released through PURSUE Release 07; two co-located guards, unaided visual, no radar or optical aids, no physical evidence, no independent corroboration. All distances and movements are visual estimates; a 135° disappearance elevation is a source ambiguity.',
        'sourceRecords': [d158],
        'temporal': {'dateLabel': '8 NOV 1953', 'year': 1953, 'startDateTime': '1953-11-08T03:15:00Z', 'endDateTime': '1953-11-08T03:19:00Z', 'timezone': 'UTC', 'durationSeconds': 240, 'precision': 'minute', 'eventForm': 'single-event'},
        'geospatial': {'geometry': {'type': 'Point', 'coordinates': [-122.8, 53.9]}, 'role': 'representative-centroid', 'precision': 'city', 'uncertaintyKm': 20, 'basis': 'Published public coordinate for Prince George Airport'},
        'observation': {'witnessCount': 2, 'witnessRoles': ['T/Sgt Arvel Lee Daniel, provost sergeant', 'S/Sgt John Junior Bricker, air policeman'], 'sensors': ['unaided-visual'], 'durationSeconds': 240, 'independentWitnessGroups': 1},
        'phenomena': {'shapes': ['round-light'], 'objectCount': 1, 'luminosity': 'white with blue tint; blinking', 'motion': ['approach', 'hover', 'vertical-ascent', 'climb-westward'], 'effects': ['humming-sound-reported']},
        'publicSources': [{'label': 'War.gov — PURSUE Release 07', 'url': 'https://www.war.gov/ufo/', 'publisher': 'U.S. Department of War', 'access': 'Public official release landing page', 'scope': 'official-release-custody', 'note': 'Official custody page for DOW-UAP-D158. The report documents two guards visual account; it does not establish anomalous origin or measured dimensions.'}],
        'evidenceBoundary': 'Documented ground visual report by two co-located guards; no radar, no optical instruments, no physical evidence, and no independent corroboration.',
    },
]

NEW_TIMELINE = [
    {'id': 'TL-1953-PG-GUARDS', 'date': '8 NOV 1953', 'year': 1953, 'type': 'official report', 'title': 'Prince George Airport guards\u2019 light report', 'caseId': 'BF-1953-PG-01',
     'desc': 'Two USAF guards at Prince George Airport, British Columbia, reported a hovering and climbing white-with-blue light over approximately four minutes; no radar, optical, or physical evidence documented.'},
    {'id': 'TL-1956-GU-F86', 'date': '31 DEC 1956', 'year': 1956, 'type': 'official report', 'title': 'Guam F-86D blinking-light encounter', 'caseId': 'BF-1956-GU-01',
     'desc': 'An F-86D pilot reported a maneuvering blinking light near Guam; investigators confirmed a contemporaneous weather balloon and retained a malfunctioned-balloon alternative.'},
    {'id': 'TL-1957-SA-B52', 'date': '18 JAN 1957', 'year': 1957, 'type': 'official report', 'title': 'Saudi Arabia B-52 gunnery-radar contact', 'caseId': 'BF-1957-SA-01',
     'desc': 'A B-52 gunnery scope reportedly showed an unexpected return near 6,000 yards for five to seven minutes near Saudi Arabia; no visual, independent radar, or raw recording accompanied the report.'},
]

# ── Source page images and hero visuals ─────────────────────────────────────
P7 = 'assets/sources/PURSUE-RELEASE-07'
for nc, pages in zip(NEW_CASES, [
    ['DOW-UAP-D155-pdf-page-001.png', 'DOW-UAP-D155-pdf-page-002.png'],
    ['DOW-UAP-D156-pdf-page-001.png', 'DOW-UAP-D156-pdf-page-002.png'],
    ['DOW-UAP-D158-pdf-page-001.png', 'DOW-UAP-D158-pdf-page-003.png'],
]):
    nc['sourceRecords'][0]['sourcePageImages'] = [f'{P7}/{p}' for p in pages]
    display = pages[0].replace('.png', '-display.jpg')
    thumb = pages[0].replace('.png', '-thumb.jpg')
    nc['heroVisual'] = {
        'src': f'{P7}/{display}', 'mediaType': 'image', 'visualType': 'official-document-page',
        'caption': 'Official air intelligence report page released through PURSUE Release 07.',
        'provenance': 'USAF report released through Department of War PURSUE Release 07',
        'evidenceStatus': 'Official documentary evidence; not event imagery or sensor data.',
        'isEventEvidence': False}
    nc['image'] = f'{P7}/{display}'
    nc['images'] = [f'{P7}/{p.replace(".png", "-display.jpg")}' for p in pages]

# ── Apply ───────────────────────────────────────────────────────────────────
j = json.loads(ATLAS.read_text())
cases = {c['id']: c for c in j['cases']}
timeline = j['timeline']

scope_ids = {'BF-1957-SA-01', 'BF-1956-GU-01', 'BF-1953-PG-01'}
existing = set(cases.keys()) & scope_ids

# Remove existing scoped cases if present (idempotency)
if existing:
    j['cases'] = [c for c in j['cases'] if c['id'] not in scope_ids]
    j['timeline'] = [t for t in j['timeline'] if t.get('caseId') not in scope_ids]
    cases = {c['id']: c for c in j['cases']}

# Insert new cases in year-then-id order
for nc in NEW_CASES:
    cases[nc['id']] = nc
j['cases'] = sorted(cases.values(), key=lambda c: (c.get('year', 0), c['id']))

# Remove existing scoped timeline entries if present
tl_ids = {t['caseId'] for t in NEW_TIMELINE}
j['timeline'] = [t for t in j['timeline'] if t.get('caseId') not in tl_ids] + list(NEW_TIMELINE)
j['timeline'] = sorted(j['timeline'], key=lambda t: (t.get('year', 0), t.get('id')))

text = json.dumps(j, ensure_ascii=False, indent=2) + '\n'
if ATLAS.read_text() != text:
    ATLAS.write_text(text)

print('scopeCaseIds', sorted(scope_ids), 'addedCases', len(NEW_CASES), 'addedTimeline', len(NEW_TIMELINE),
      'totalCases', len(j['cases']), 'totalTimeline', len(j['timeline']))