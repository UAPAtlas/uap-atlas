#!/usr/bin/env python3
"""Apply Release 05 new-case tranche 01 and Tremonton correction deterministically."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ATLAS = ROOT / 'atlas-data.json'
PUBLIC = ROOT / 'public-source-manifest.json'
INDEX = ROOT / 'source-file-index.json'
LANDING = 'https://www.war.gov/UFO/?releaseDate=Release+05&release=05'
BASE = 'assets/sources/PURSUE-RELEASE-05'


def load(path: Path):
    return json.loads(path.read_text())


def save(path: Path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def append_unique(items, value):
    if value not in items:
        items.append(value)


def upsert(items, value, key):
    marker = value[key]
    for idx, item in enumerate(items):
        if item.get(key) == marker:
            items[idx] = value
            return
    items.append(value)


def release_source(note):
    return {
        'label': 'War.gov — PURSUE Release 05',
        'url': LANDING,
        'publisher': 'U.S. Department of War',
        'access': 'Public official release landing page',
        'scope': 'official-release-custody',
        'note': note,
    }


pr_pages = [
    f'{BASE}/CIA-UAP-D022-pdf-page-003.png',
    f'{BASE}/CIA-UAP-D022-pdf-page-004.png',
    f'{BASE}/CIA-UAP-D022-pdf-page-006.png',
    f'{BASE}/CIA-UAP-D023-pdf-page-001.png',
    f'{BASE}/CIA-UAP-D023-pdf-page-002.png',
]
gom_pages = [
    f'{BASE}/DOW-UAP-D101-pdf-page-001.png',
    f'{BASE}/DOW-UAP-D101-pdf-page-005.png',
    f'{BASE}/DOW-UAP-D101-pdf-page-006.png',
]
rl_pages = [
    f'{BASE}/FBI-UAP-D037-pdf-page-001.png',
    f'{BASE}/FBI-UAP-D037-pdf-page-002.png',
    f'{BASE}/FBI-UAP-D037-pdf-page-003.png',
    f'{BASE}/FBI-UAP-D040-pdf-page-001.png',
    f'{BASE}/FBI-UAP-D040-pdf-page-002.png',
]
rl_contacts = [
    f'{BASE}/FBI-UAP-D038-reconstruction-contact.jpg',
    f'{BASE}/FBI-UAP-D039-reconstruction-contact.jpg',
    f'{BASE}/FBI-UAP-D041-reconstruction-contact.jpg',
    f'{BASE}/FBI-UAP-D042-reconstruction-contact.jpg',
]
rl_hero = f'{BASE}/FBI-UAP-D037-D042-reconstructions-contact.jpg'

atlas = load(ATLAS)
by_id = {case['id']: case for case in atlas['cases']}

# Correct the stale pre-release wording without erasing the later analytical dispute.
tremonton = by_id['BF-1952-TM-01']
tremonton['summary'] = (
    'Navy Chief Photographer Delbert Newhouse filmed a dozen maneuvering white objects near Tremonton, Utah, on 2 July 1952. '
    'The exact 4 May 1953 Naval Photographic Interpretation Center report records a majority view that the images were light sources not identifiable as natural phenomena or commonly known man-made objects. '
    'The Robertson Panel and a later Air Force memorandum favored a seagull explanation, while the Navy report itself records copy-generation, geometry, resource and corroboration limits.'
)
tremonton['official'] = (
    'The exact 4 May 1953 Naval Photographic Interpretation Center report records the analysts’ majority light-source/unidentified assessment, while stating that it did not necessarily represent the official Navy or Center position and that no corroboration attempt was made. '
    'The Robertson Panel and a 1956 Air Force memorandum favored sunlit seagulls. The official record therefore preserves conflicting analyses rather than a final identification.'
)
tremonton['keyFact'] = (
    'Release 05 recovers the exact 1953 Navy analysis rather than only later summaries. NARA separately lists 42-foot 16 mm reference and preservation elements, but the digital transfer slate identifies a positive copy and the Navy report states that its analysis used “a duplicate of a copy.”'
)

pr = {
    'id': 'BF-1964-PR-01',
    'title': 'Puerto Rico / USS Gyatt Radar-Visual Incidents',
    'date': '16–24 NOV 1964',
    'year': 1964,
    'location': 'North of Puerto Rico / Atlantic Fleet Weapons Range',
    'mode': 'approximate',
    'lon': -65.5,
    'lat': 20.5,
    'expectedCountry': 'Puerto Rico',
    'geometryExpectation': 'offshore',
    'coordinatePrecision': 'offshore-region',
    'coordinateBasis': 'Generalized offshore point north/east of Puerto Rico within the reported Atlantic Fleet Weapons Range vicinity; exact track geometry is absent',
    'agency': 'USN / CIA',
    'domain': 'MILITARY / SENSOR',
    'status': 'DOCUMENTED · UNRESOLVED',
    'confidence': 'CONFIRMED RECORD · UNRESOLVED AIRCRAFT IDENTITY',
    'summary': (
        'CIA and Navy records describe several high-speed targets near the Atlantic Fleet Weapons Range on 16, 17, 18, 19 and 24 November 1964. '
        'On 19 November an F-8C pilot reported a delta-shaped object in full moonlight while USS Gyatt recorded a radar track; on 24 November another high-altitude target reportedly pulled away from a Crusader at Mach 0.99 and 45,000 feet. '
        'CIA rejected a YF-12A identification and considered—but did not substantiate—a MiG-21 reconnaissance explanation.'
    ),
    'keyFact': 'The released memoranda preserve a pilot-visual, shipboard-radar and intelligence-handling chain, including Navy transfer of the original radar film and prints to CIA for analysis; those radar materials are not included in Release 05.',
    'official': 'CIA treated the 19 November object as probably a high-performance delta-wing aircraft and left other observations as unidentified aircraft. Internal correspondence says ONI was convinced it was not a YF-12A or similar Lockheed aircraft. The records do not establish extraordinary origin.',
    'gap': 'The original USS Gyatt radar film and prints, complete Navy message traffic, Atlantic Fleet Weapons Range sensor records, pilot statement, and any final OSI/OEL technical analysis are absent.',
    'whyItMatters': 'A rare historical case in which released intelligence records connect a military pilot observation, shipboard radar-scope photography, weapons-range reporting and explicit competing aircraft analysis.',
    'sources': [
        'CIA-UAP-D022 · CIA memoranda and radar-film custody, 1965',
        'CIA-UAP-D023 · Navy briefing notes on November 1964 incidents',
    ],
    'sourceLabel': 'CIA / U.S. Navy records',
    'sourceLocator': 'CIA-UAP-D022',
    'relatedCaseIds': ['BF-2013-AG-01', 'BF-1957-RB-01'],
    'keyQuote': 'The U.S.S. Gyatt confirmed the tracking with motion pictures of radar scope presentation.',
    'quoteSource': 'CIA-UAP-D023, Briefing Notes for Mr. Walter Elder, PDF p. 2',
    'quoteConfidence': 'High — exact wording in the released briefing note; it establishes the reported radar-film chain, not the object’s identity.',
    'heroFact': 'Navy traffic reportedly delivered the original radar film and prints to CIA, but Release 05 contains the memoranda—not the radar media itself.',
    'significance': 'High significance',
    'sourceQuality': 'Two exact official CIA/Navy records with pilot, radar and custody details; the referenced radar film, prints, traffic and final analysis are missing.',
    'image': pr_pages[0],
    'images': pr_pages,
    'caseTypes': ['military-encounter'],
    'evidenceModes': ['testimony', 'radar', 'documentary-record'],
    'environment': ['military-airspace', 'maritime'],
    'outcome': 'unresolved',
    'confidenceModel': {'record': 'confirmed', 'anomaly': 'undetermined', 'provenance': 'primary-record'},
    'temporal': {
        'dateLabel': '16–24 NOV 1964', 'year': 1964, 'startDateTime': None, 'endDateTime': None,
        'timezone': None, 'durationSeconds': None, 'precision': 'date-range', 'eventForm': 'multi-event',
    },
    'geospatial': {
        'geometry': {'type': 'Point', 'coordinates': [-65.5, 20.5]},
        'role': 'representative-centroid', 'precision': 'offshore-region', 'uncertaintyKm': 350,
        'basis': 'Generalized offshore point north/east of Puerto Rico within the reported Atlantic Fleet Weapons Range vicinity; exact track geometry is absent',
    },
    'sourceRecords': [
        {
            'citation': 'CIA memoranda concerning unidentified flying-object reports near Puerto Rico, 1 and 11 February 1965, CIA-UAP-D022',
            'sourceType': 'primary-official-intelligence-analysis-and-custody-record',
            'provenance': 'Exact PDF published by the U.S. Department of War in PURSUE Release 05; full local copy hash-verified against the original download',
            'locator': 'CIA-UAP-D022 · PDF pp. 3–4 and 6', 'url': LANDING,
            'sha256': '358b0d2e45ff0320f4e4ad689f0c918362d6c5d36be765d386018d279d835b01',
            'sourcePageImages': pr_pages[:3],
            'supports': [
                'Documents CIA analysis of reports from 16–24 November 1964 near the Atlantic Fleet Weapons Range',
                'Records competing YF-12A and possible MiG-21 aircraft interpretations',
                'Records Navy transfer of the original radar film and accompanying prints to CIA',
            ],
            'limitations': [
                'The original radar film, prints and complete message traffic are absent from Release 05',
                'The MiG-21 discussion explicitly states that no evidence supported such reconnaissance activity from Cuba',
                'CIA analysis of a likely aircraft does not identify the aircraft or independently verify every reported observation',
            ],
        },
        {
            'citation': 'Navy briefing notes for Walter Elder on the November 1964 Puerto Rico incidents, CIA-UAP-D023',
            'sourceType': 'primary-official-briefing-record',
            'provenance': 'Exact PDF published by the U.S. Department of War in PURSUE Release 05; full local copy hash-verified against the original download',
            'locator': 'CIA-UAP-D023 · PDF pp. 1–2', 'url': LANDING,
            'sha256': 'aba51f51191bbcd37dc1f591171b6edc78c9bfb9632cfed8fae6a8bf1d61ca40',
            'sourcePageImages': pr_pages[3:],
            'supports': [
                'Records the F-8C pilot’s full-moon visual description of a delta-shaped object',
                'Records USS Gyatt confirmation with motion pictures of the radar-scope presentation',
                'Records a separate 24 November high-altitude target that pulled away from a Crusader at Mach 0.99 and 45,000 feet',
            ],
            'limitations': [
                'A briefing note summarizes underlying reports that are not included in full',
                'Pilot estimates and radar summaries cannot be independently reconstructed without the original media and logs',
            ],
        },
    ],
    'phenomena': {'shapes': ['delta', 'aircraft-like'], 'objectCount': None, 'luminosity': None, 'motion': ['high-speed'], 'effects': []},
    'observation': {
        'witnessCount': None, 'witnessRoles': ['U.S. Navy F-8C pilot', 'USS Gyatt radar personnel'],
        'sensors': ['unaided-visual', 'shipboard-radar', 'radar-scope-photography'], 'durationSeconds': None,
        'independentWitnessGroups': 2,
    },
    'taxonomyOriginal': {'domain': 'MILITARY / SENSOR', 'status': 'UNRESOLVED AIRCRAFT REPORT', 'confidence': 'CONFIRMED RECORD'},
    'taxonomyVersion': 'atlas-controlled-v1',
    'heroVisual': {
        'src': pr_pages[0], 'mediaType': 'image', 'visualType': 'official-document-page',
        'caption': 'CIA analysis page addressing the November 1964 Puerto Rico reports and competing aircraft hypotheses.',
        'provenance': 'CIA record released through PURSUE Release 05',
        'evidenceStatus': 'Official documentary evidence; not event imagery or the referenced radar film.',
        'isEventEvidence': False,
    },
    'publicSources': [release_source('Official custody page for CIA-UAP-D022 and D023. The records authenticate the intelligence and radar-film handling chain, not an extraordinary object origin.')],
    'evidenceBoundary': {
        'established': [
            'Official CIA/Navy records document pilot, shipboard-radar and weapons-range reporting on 16, 17, 18, 19 and 24 November 1964.',
            'The Navy provided original radar film and prints to CIA for analysis.',
            'CIA rejected the proposed YF-12A identification and considered conventional high-performance aircraft possibilities.',
        ],
        'notEstablished': [
            'The original radar film, prints, complete pilot statement and final technical analysis are absent from Release 05.',
            'The exact object identity, trajectory, speed and origin.',
            'That the reports described one object or an extraordinary vehicle.',
        ],
        'competingExplanations': ['High-performance military aircraft, including a speculative MiG-21 reconnaissance configuration; sensor or range reconstruction error; unidentified conventional aircraft.'],
    },
}

gom = {
    'id': 'BF-2021-GOM-01',
    'title': 'Gulf of Oman AC-130 EO/IR Event',
    'date': '8 SEP 2021',
    'year': 2021,
    'location': 'Gulf of Oman [PARTIALLY REDACTED]',
    'mode': 'approximate',
    'lon': 58.0,
    'lat': 24.5,
    'geometryExpectation': 'offshore',
    'coordinatePrecision': 'redacted-offshore-region',
    'coordinateBasis': 'Generalized Gulf of Oman point; released MGRS begins 40REN6 but is partially redacted and cannot support exact plotting',
    'agency': 'USSOF / AFSOC',
    'domain': 'MILITARY / SENSOR',
    'status': 'DOCUMENTED · UNRESOLVED',
    'confidence': 'CONFIRMED REPORT · NOT FINALLY EVALUATED',
    'summary': (
        'A released Intelligence Information Report states that a USSOF AC-130 crew observed approximately 25 UAP instances through EO/IR during live-fire training in the Gulf of Oman on 8 September 2021. '
        'Two approximately four-foot cold objects were reported stationary just above the water near a flare before departing as the 105 mm cannon fired; later observations described pairs and trios maneuvering in formation. '
        'The report is marked not finally evaluated, and its six-video attachment is absent from the released packet.'
    ),
    'keyFact': 'The report provides a direct military-platform and EO/IR sensor chain, GPS-derived location basis and reported speed calculations, but the PowerPoint containing six embedded videos and the corrupted full DVR recording are unavailable.',
    'official': 'The document is an Intelligence Information Report explicitly labeled “not finally evaluated intelligence.” It records source reporting and broad dissemination; it is not an AARO, AFSOC or intelligence-community finding about object identity or origin.',
    'gap': 'Missing are the six embedded AC-130 videos, uncorrupted full-sortie DVR data, raw sensor metadata, aircraft telemetry/TACTOOL outputs, independent radar or ship correlation, and a final analytical disposition.',
    'whyItMatters': 'A unusually detailed modern military sensor report combining a named aircraft class, EO/IR observation, live-fire chronology, location methodology and attachment trail while clearly exposing the decisive missing data.',
    'sources': ['DOW-UAP-D101 · Gulf of Oman AC-130 Intelligence Information Report, 2021/2022'],
    'sourceLabel': 'USSOF / AFSOC Intelligence Information Report',
    'sourceLocator': 'DOW-UAP-D101',
    'relatedCaseIds': ['BF-2020-AG-00', 'BF-2019-OM-01'],
    'keyQuote': 'Immediately upon pulling the trigger… the CSO observed the pair of UAP rapidly fly away from the flare and out of the sensor feed without changing altitude.',
    'quoteSource': 'DOW-UAP-D101, PDF p. 5',
    'quoteConfidence': 'High — exact event text in the released IIR; the document is source reporting marked not finally evaluated intelligence.',
    'heroFact': 'The report lists a PowerPoint containing six embedded AC-130 videos, but Release 05 does not provide a defensible filename crosswalk to the anonymous MP4s.',
    'significance': 'High significance',
    'sourceQuality': 'Exact official IIR with detailed EO/IR chronology and source-access statement; decisive video, telemetry and independent-correlation layers are missing.',
    'image': gom_pages[1],
    'images': [gom_pages[1], gom_pages[0], gom_pages[2]],
    'caseTypes': ['military-encounter'],
    'evidenceModes': ['sensor', 'documentary-record'],
    'environment': ['maritime', 'military-airspace'],
    'outcome': 'unresolved',
    'confidenceModel': {'record': 'confirmed', 'anomaly': 'not-assessed', 'provenance': 'primary-record'},
    'temporal': {
        'dateLabel': '8 SEP 2021', 'year': 2021, 'startDateTime': '2021-09-08', 'endDateTime': None,
        'timezone': None, 'durationSeconds': None, 'precision': 'day', 'eventForm': 'single-sortie-multi-observation',
    },
    'geospatial': {
        'geometry': {'type': 'Point', 'coordinates': [58.0, 24.5]},
        'role': 'representative-centroid', 'precision': 'redacted-offshore-region', 'uncertaintyKm': 300,
        'basis': 'Generalized Gulf of Oman point; released MGRS begins 40REN6 but is partially redacted and cannot support exact plotting',
    },
    'sourceRecords': [{
        'citation': 'Intelligence Information Report, “Multiple Unidentified Aerial Phenomenon Observed… Over Gulf of Oman During AC-130 Gunship Live Fire Training on 8 September 2021,” DOW-UAP-D101',
        'sourceType': 'primary-official-intelligence-information-report',
        'provenance': 'Exact PDF published by the U.S. Department of War in PURSUE Release 05; full local copy hash-verified against the original download',
        'locator': 'DOW-UAP-D101 · PDF pp. 1, 5–6', 'url': LANDING,
        'sha256': '926f4cf9a852d77bca34e8e7370c4a9da386610a6ba799e060de71c2339b0e92',
        'sourcePageImages': gom_pages,
        'supports': [
            'Documents a USSOF AC-130 EO/IR observation during 8 September 2021 live-fire training',
            'Records approximately 25 reported UAP instances, formation behavior and source-calculated speed claims',
            'Records GPS-derived geographic coordinates and a PowerPoint attachment containing six embedded videos',
        ],
        'limitations': [
            'The IIR is explicitly not finally evaluated intelligence',
            'The six-video PowerPoint, full DVR recording, telemetry and independent sensor correlation are absent',
            'Release custody authenticates the report, not the object interpretation or reported performance',
        ],
    }],
    'phenomena': {'shapes': ['sphere', 'formation'], 'objectCount': None, 'luminosity': 'cold in EO/IR', 'motion': ['formation', 'erratic', 'rapid-departure'], 'effects': []},
    'observation': {
        'witnessCount': None, 'witnessRoles': ['USSOF AC-130 aircrew', 'Combat Systems Officer'],
        'sensors': ['EO/IR', 'AC-130 sensor-feed GPS', 'TACTOOL-derived estimates'], 'durationSeconds': None,
        'independentWitnessGroups': 1,
    },
    'taxonomyOriginal': {'domain': 'MILITARY / SENSOR', 'status': 'UNRESOLVED IIR', 'confidence': 'NOT FINALLY EVALUATED INTELLIGENCE'},
    'taxonomyVersion': 'atlas-controlled-v1',
    'heroVisual': {
        'src': gom_pages[1], 'mediaType': 'image', 'visualType': 'official-document-page',
        'caption': 'Event-text page from the Gulf of Oman AC-130 Intelligence Information Report.',
        'provenance': 'USSOF/AFSOC intelligence record released through PURSUE Release 05',
        'evidenceStatus': 'Official documentary evidence; not a frame from the missing six-video attachment.',
        'isEventEvidence': False,
    },
    'publicSources': [release_source('Official custody page for DOW-UAP-D101. The IIR is marked not finally evaluated and its listed six-video attachment is not defensibly mapped to the anonymous Release 05 MP4s.')],
    'evidenceBoundary': {
        'established': [
            'An official IIR records direct-source AC-130 EO/IR observations during a dated Gulf of Oman sortie.',
            'The report lists GPS-derived coordinates, source-derived speed estimates and six embedded videos as an attachment.',
        ],
        'notEstablished': [
            'The identity or origin of the reported objects.',
            'Independent verification of the source-calculated speeds, dimensions or response to gunfire.',
            'A defensible mapping between the six listed videos and any anonymous Release 05 MP4 filename.',
        ],
        'competingExplanations': ['Sensor or range-estimation effects, thermal contrast near a flare/live-fire environment, seabirds, debris, munitions-related objects, aircraft or UAS, and parallax remain unresolved without the missing media and telemetry.'],
    },
}

rl_source_records = [
    {
        'citation': 'FBI FD-302 interview recording the 2026 multiple-red-light/NOD field observation, FBI-UAP-D037',
        'sourceType': 'primary-official-witness-interview-record',
        'provenance': 'Exact PDF published by the U.S. Department of War in PURSUE Release 05; full local copy hash-verified against the original download',
        'locator': 'FBI-UAP-D037 · PDF pp. 1–3', 'url': LANDING,
        'sha256': 'df8741ec7bee9778646142e3c2c55c050e3c58d067fa1049683ccd1126f0110a',
        'sourcePageImages': rl_pages[:3],
        'supports': [
            'Preserves one firsthand witness’s multi-phase chronology using naked-eye and Night Optical Devices',
            'Records low-elevation lights, a moving glow in a dry wash and a reported 25-minute mechanical-watch discrepancy',
            'Records no sound, exhaust, physiological effects or successful thermal acquisition',
        ],
        'limitations': [
            'Exact date, location, identity and operational role are redacted',
            'An FD-302 records what a witness told the FBI; it is not an FBI factual finding',
            'No native event imagery, sensor logs or watch examination record is included',
        ],
    },
    {
        'citation': 'FBI FD-302 companion-witness interview concerning the 2026 multiple-red-light/NOD field observation, FBI-UAP-D040',
        'sourceType': 'primary-official-witness-interview-record',
        'provenance': 'Exact PDF published by the U.S. Department of War in PURSUE Release 05; full local copy hash-verified against the original download',
        'locator': 'FBI-UAP-D040 · PDF pp. 1–2', 'url': LANDING,
        'sha256': '978ac7226c7ec06f4561c3986732183e3bf2aa4f07c03430daa9111a20eec77e',
        'sourcePageImages': rl_pages[3:],
        'supports': [
            'Preserves a companion account of 6 to 10 red lights synchronizing and moving east/southeast',
            'Records closer NOD observations resolving points into three-light triangular or diamond clusters',
            'Corroborates the low-level phase and reported 25-minute watch discrepancy',
        ],
        'limitations': [
            'Exact date, location, identity and operational role are redacted',
            'OCR omitted load-bearing continuation text; PDF p. 2 was visually adjudicated from the released page',
            'No native event imagery or independent clock/sensor record is included',
        ],
    },
]
for doc_id, sha, contact, pages in [
    ('FBI-UAP-D038', '53e69e5d6dbe46fc435574c3f0246fcdfbbd537928a8a6c46c3f35752f68133e', rl_contacts[0], 1),
    ('FBI-UAP-D039', '491d158803934b9c4e5de46ee51388cd9eff8a8aba2cf17dfcc9d957a8952ebd', rl_contacts[1], 3),
    ('FBI-UAP-D041', '7416fff9cc1cb0e19e5d1f5b6efc2b031ea986403a049e3d6fa38d7965fa79e9', rl_contacts[2], 6),
    ('FBI-UAP-D042', '8ccb25fd8f47cdec75cc384bcf7db137c842931428472664fecfd04db69f6a2f', rl_contacts[3], 1),
]:
    rl_source_records.append({
        'citation': f'{doc_id} · FBI digital rendering accompanying the 2026 multiple-red-light witness packet',
        'sourceType': 'official-digital-rendering-reconstruction',
        'provenance': 'Exact rendering PDF published by the U.S. Department of War in PURSUE Release 05; full local copy hash-verified against the original download',
        'locator': doc_id, 'url': LANDING, 'sha256': sha, 'sourcePageImages': [contact],
        'supports': [f'Preserves an FBI-released visual reconstruction ({pages} source page(s)) of a witness description'],
        'limitations': ['Illustrative reconstruction only; not native event imagery, sensor data or independent corroboration'],
    })

rl = {
    'id': 'BF-2026-RL-01',
    'title': 'Red-Light / NOD Field Encounter',
    'date': '[REDACTED] 2026',
    'year': 2026,
    'location': 'United States [REDACTED]',
    'mode': 'redacted',
    'lon': -98.5,
    'lat': 39.8,
    'expectedCountry': 'United States of America',
    'geometryExpectation': 'country',
    'coordinatePrecision': 'country-redacted-generalized',
    'coordinateBasis': 'Map-only generalized continental U.S. centroid; the released records redact the event location',
    'agency': 'FBI',
    'domain': 'GOVERNMENT / INSTITUTIONAL',
    'status': 'DOCUMENTED · UNRESOLVED',
    'confidence': 'CONFIRMED RECORDS · UNRESOLVED INTERPRETATION',
    'summary': (
        'Two FBI interview records preserve companion accounts of a redacted 2026 field outing in rainy mountainous terrain. '
        'The witnesses described red lights through naked-eye and Night Optical Devices, later low-level lights and a moving glow near a dry wash, and a mechanical watch becoming approximately 25 minutes fast while digital clocks agreed. '
        'The released records document the accounts but provide no native event imagery, sensor logs, exact location or FBI analytical conclusion.'
    ),
    'keyFact': 'D037 and D040 share the same distinctive multi-phase chronology and 25-minute mechanical-watch discrepancy, supporting one multi-witness event rather than two cases; D038/D039/D041/D042 are reconstructions only.',
    'official': 'The FD-302s document what two witnesses reported to FBI agents. The forms explicitly contain neither recommendations nor conclusions of the FBI; release custody does not convert the witness accounts into an FBI finding.',
    'gap': 'Missing are exact date/location/identities, native NOD or thermal imagery, independent clock examination, environmental and aviation correlation, agent analytical work product and closure disposition.',
    'whyItMatters': 'Two companion official interviews preserve a distinctive same-event chronology across unaided and NOD observation, including unusual low-level behavior and a mutually observed timing discrepancy, while leaving decisive physical and location data unavailable.',
    'sources': [
        'FBI-UAP-D037 and D040 · companion FD-302 witness records',
        'FBI-UAP-D038/D039/D041/D042 · illustrative digital reconstructions',
    ],
    'sourceLabel': 'FBI FD-302 records',
    'sourceLocator': 'FBI-UAP-D037',
    'relatedCaseIds': ['BF-2023-WUS-03', 'BF-2024-NE-02'],
    'keyQuote': 'The time on his watch was 25 minutes ahead of the time on his phone and the vehicle’s digital clock.',
    'quoteSource': 'FBI-UAP-D037, FD-302 continuation, PDF p. 2',
    'quoteConfidence': 'High — exact witness-account language in the released FD-302; no independent examination of the watch is included.',
    'heroFact': 'Two interviews describe the same field chronology, but the associated visual files are witness reconstructions—not photographs of the event.',
    'significance': 'High significance',
    'sourceQuality': 'Two official companion witness-interview records plus four released reconstruction files; exact context, native sensor data and independent analytical findings are absent.',
    'image': rl_hero,
    'images': [rl_hero] + rl_contacts + rl_pages,
    'caseTypes': ['witness-report'],
    'evidenceModes': ['testimony', 'night-optical-observation'],
    'environment': ['terrestrial'],
    'outcome': 'unresolved',
    'confidenceModel': {'record': 'confirmed', 'anomaly': 'undetermined', 'provenance': 'primary-source'},
    'temporal': {
        'dateLabel': '[REDACTED] 2026', 'year': 2026, 'startDateTime': None, 'endDateTime': None,
        'timezone': None, 'durationSeconds': None, 'precision': 'year-redacted', 'eventForm': 'single-event-multi-phase',
    },
    'geospatial': {
        'geometry': {'type': 'Point', 'coordinates': [-98.5, 39.8]},
        'role': 'representative-centroid', 'precision': 'country-redacted-generalized', 'uncertaintyKm': 2000,
        'basis': 'Map-only generalized continental U.S. centroid; the released records redact the event location',
    },
    'sourceRecords': rl_source_records,
    'phenomena': {'shapes': ['light', 'orb', 'triangle'], 'objectCount': None, 'luminosity': 'dull red', 'motion': ['formation', 'direction-change', 'low-elevation'], 'effects': ['reported-mechanical-watch-discrepancy']},
    'observation': {
        'witnessCount': 2, 'witnessRoles': ['operational witnesses, roles redacted'],
        'sensors': ['unaided-visual', 'Night Optical Devices', 'attempted thermal optics'], 'durationSeconds': None,
        'independentWitnessGroups': 1,
    },
    'taxonomyOriginal': {'domain': 'WITNESS NARRATIVE', 'status': 'UNRESOLVED', 'confidence': 'CONFIRMED TESTIMONY'},
    'taxonomyVersion': 'atlas-controlled-v1',
    'heroVisual': {
        'src': rl_hero, 'mediaType': 'image', 'visualType': 'official-digital-rendering-reconstruction-contact',
        'caption': 'Contact sheet of FBI-released witness-description reconstructions accompanying D037 and D040.',
        'provenance': 'FBI digital renderings released through PURSUE Release 05',
        'evidenceStatus': 'Illustrative reconstructions only; not native event imagery, sensor data or independent corroboration.',
        'isEventEvidence': False,
    },
    'publicSources': [release_source('Official custody page for FBI-UAP-D037–D042. The FD-302s document companion witness accounts; the renderings are illustrative and the records contain no FBI conclusion.')],
    'evidenceBoundary': {
        'established': [
            'Two official FD-302s preserve companion witness accounts with matching event chronology.',
            'The accounts include unaided and NOD observations, low-level phases and the same reported 25-minute mechanical-watch discrepancy.',
            'Four released visual files illustrate witness descriptions.',
        ],
        'notEstablished': [
            'The identity, origin, precise location or physical performance of the reported lights.',
            'That the reported watch discrepancy was caused by the observed phenomenon.',
            'That the digital renderings are event photographs or sensor products.',
            'An FBI analytical finding validating the event account.',
        ],
        'competingExplanations': ['Aircraft or UAS, distant lights with range/terrain misperception, atmospheric and NOD blooming effects, satellites or astronomical sources for higher phases, and an unrelated mechanical-watch timing error.'],
    },
}

for case in [pr, gom, rl]:
    upsert(atlas['cases'], case, 'id')

# New dossiers may point to established related cases without mutating those
# existing records outside this independently reviewable tranche.

for entry in [
    {'id': 'TL-1964-PR-GYATT', 'year': 1964, 'date': '16–24 NOV 1964', 'type': 'incident', 'caseId': pr['id'], 'title': 'Puerto Rico / USS Gyatt radar-visual incidents', 'desc': 'Navy pilot and radar reporting near the Atlantic Fleet Weapons Range entered CIA analysis; the referenced original radar film and prints remain absent.'},
    {'id': 'TL-2021-GOM-AC130', 'year': 2021, 'date': '8 SEP 2021', 'type': 'incident', 'caseId': gom['id'], 'title': 'Gulf of Oman AC-130 EO/IR event', 'desc': 'A released IIR records approximately 25 EO/IR observations during live-fire training while remaining explicitly not finally evaluated intelligence.'},
    {'id': 'TL-2026-RL-NOD', 'year': 2026, 'date': '[REDACTED] 2026', 'type': 'incident', 'caseId': rl['id'], 'title': 'Red-light / NOD field encounter', 'desc': 'Two FBI interview records preserve companion accounts of a multi-phase NOD observation and reported mechanical-watch discrepancy at a redacted U.S. location.'},
]:
    upsert(atlas['timeline'], entry, 'id')

save(ATLAS, atlas)

public = load(PUBLIC)
for case in [tremonton, pr, gom, rl]:
    public[case['id']] = case.get('publicSources', [])
save(PUBLIC, public)

index = load(INDEX)
index.update({
    'CIA-UAP-D022': pr_pages[:3] + [LANDING],
    'CIA-UAP-D022 · PDF pp. 3–4 and 6': pr_pages[:3] + [LANDING],
    'CIA-UAP-D023': pr_pages[3:] + [LANDING],
    'CIA-UAP-D023 · PDF pp. 1–2': pr_pages[3:] + [LANDING],
    'DOW-UAP-D101': gom_pages + [LANDING],
    'DOW-UAP-D101 · PDF pp. 1, 5–6': gom_pages + [LANDING],
    'FBI-UAP-D037': rl_pages[:3] + [LANDING],
    'FBI-UAP-D037 · PDF pp. 1–3': rl_pages[:3] + [LANDING],
    'FBI-UAP-D038': [rl_contacts[0], LANDING],
    'FBI-UAP-D039': [rl_contacts[1], LANDING],
    'FBI-UAP-D040': rl_pages[3:] + [LANDING],
    'FBI-UAP-D040 · PDF pp. 1–2': rl_pages[3:] + [LANDING],
    'FBI-UAP-D041': [rl_contacts[2], LANDING],
    'FBI-UAP-D042': [rl_contacts[3], LANDING],
})
save(INDEX, index)

print('Applied Release 05 new-case tranche 01: Tremonton correction + BF-1964-PR-01, BF-2021-GOM-01, BF-2026-RL-01')
