#!/usr/bin/env python3
"""Apply the bounded Release 05 source-depth completion tranche.

Scope: BF-SF-07, BF-2021-GOM-01, BF-1946-GR-01, and Blackfile Q6/Q7.
No cases or timeline entries are added or removed.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ATLAS = ROOT / 'atlas-data.json'
BLACKFILE = ROOT / 'blackfile-analysis.json'
INDEX = ROOT / 'source-file-index.json'
BASE = 'assets/sources/PURSUE-RELEASE-05'
LANDING = 'https://www.war.gov/UFO/?releaseDate=Release+05&release=05'
D100_HASH = '4052303ee0d521c15656b65fed3075734c83332ec5db319c744f0dbe53b8ec90'
D101_HASH = '926f4cf9a852d77bca34e8e7370c4a9da386610a6ba799e060de71c2339b0e92'


def load(path: Path):
    return json.loads(path.read_text())


def save(path: Path, payload):
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + '\n')


def replace_records(case, locators, records):
    remove = set(locators)
    case['sourceRecords'] = [r for r in case.get('sourceRecords', []) if r.get('locator') not in remove] + records


def image_path(doc: str, page: int) -> str:
    return f'{BASE}/{doc}-pdf-page-{page:03d}.png'


def replace_tension(question, tension):
    question['tensions'] = [t for t in question.get('tensions', []) if t.get('label') != tension['label']] + [tension]


atlas = load(ATLAS)
assert len(atlas['cases']) == 155
assert len(atlas.get('timeline', [])) == 153
by_id = {case['id']: case for case in atlas['cases']}

# D099 cover: documentary hero for Ghost Rockets.
ghost = by_id['BF-1946-GR-01']
d099_cover = image_path('DOW-UAP-D099', 1)
prior_ghost_image = 'assets/source_previews/BF-1946-GR-01_source_image.jpg'
ghost_hero = {
    'src': d099_cover,
    'mediaType': 'image',
    'visualType': 'official-intelligence-review-cover',
    'caption': 'Cover of the War Department Intelligence Division’s January 1947 SECRET Intelligence Review containing “Ghost Rockets Over Scandinavia.”',
    'provenance': 'War Department Intelligence Division, DOW-UAP-D099, PDF p. 1',
    'evidenceStatus': 'Official publication cover and documentary evidence of the review; not an image of a reported ghost rocket.',
    'isEventEvidence': False,
}
ghost['image'] = d099_cover
ghost['heroVisual'] = ghost_hero
existing_ghost_images = ghost.get('images', [])
def src(item):
    return item.get('src') or item.get('url') if isinstance(item, dict) else item
ghost['images'] = [
    d099_cover,
    {
        'src': prior_ghost_image,
        'rank': 5,
        'caption': 'Archival context photograph associated with Scandinavian ghost-rocket investigations.',
        'visualType': 'archival-context-photo',
        'provenance': 'Swedish defense file',
        'evidenceStatus': 'Historical context image; not a photograph of a reported ghost rocket.',
    },
] + [item for item in existing_ghost_images if src(item) not in {d099_cover, prior_ghost_image}]

# D100: three bounded primary-record layers under the Estimate special file.
estimate = by_id['BF-SF-07']
d100_ack = [image_path('DOW-UAP-D100', p) for p in [1, 7, 8]]
d100_rand = [image_path('DOW-UAP-D100', 34)]
d100_arch = [image_path('DOW-UAP-D100', p) for p in [232, 240, 244]]
d100_records = [
    {
        'citation': 'Headquarters USAF / Air Materiel Command, flying-object assessment and Project SIGN correspondence, November 1948, DOW-UAP-D100',
        'sourceType': 'primary-official-institutional-assessment',
        'provenance': 'Exact pages within the 245-page DOW-UAP-D100 PDF published through PURSUE Release 05; full local PDF hash verified',
        'locator': 'DOW-UAP-D100 · PDF pp. 1–3 and 7–9',
        'url': LANDING,
        'sha256': D100_HASH,
        'sourcePageImages': d100_ack,
        'supports': [
            'Records Headquarters USAF language that it appeared “inescapable” that some type of flying object had been observed while identity and origin remained undetermined',
            'Documents an Air Materiel Command review of approximately 180 incidents and a residual set without reasonable everyday explanation',
            'Records that no physical evidence had been obtained and tangible support for an interplanetary explanation was lacking',
        ],
        'limitations': [
            'The packet is not the missing Estimate of the Situation and does not authenticate its text, authorship, approval or destruction',
            'Institutional acknowledgment of observed and unresolved reports does not identify one phenomenon or establish extraordinary origin',
        ],
    },
    {
        'citation': 'Air Materiel Command, Project SIGN special-study requirements proposed for RAND, 1948, DOW-UAP-D100',
        'sourceType': 'primary-official-study-request',
        'provenance': 'Exact pages within the 245-page DOW-UAP-D100 PDF published through PURSUE Release 05; full local PDF hash verified',
        'locator': 'DOW-UAP-D100 · PDF pp. 31–34',
        'url': LANDING,
        'sha256': D100_HASH,
        'sourcePageImages': d100_rand,
        'supports': [
            'Documents AMC’s request for RAND to examine whether some reported objects could be experimental “spaceships” or test vehicles',
            'Records proposed technical questions for distinguishing such craft from conventional aircraft, missiles or foreign systems',
        ],
        'limitations': [
            'This is a study request, not a finding that spaceships existed or explained any report',
            'The released packet does not include a completed RAND answer to these requirements',
        ],
    },
    {
        'citation': 'Headquarters USAF / Air Materiel Command, assignment and analysis of flying-disc intelligence, December 1947, DOW-UAP-D100',
        'sourceType': 'primary-official-program-architecture-and-analysis',
        'provenance': 'Exact pages within the 245-page DOW-UAP-D100 PDF published through PURSUE Release 05; full local PDF hash verified',
        'locator': 'DOW-UAP-D100 · PDF pp. 232–244',
        'url': LANDING,
        'sha256': D100_HASH,
        'sourcePageImages': d100_arch,
        'supports': [
            'Documents the formal assignment of flying-disc intelligence collection, collation, evaluation and production to Air Materiel Command',
            'Preserves recurring reported characteristics, selected radar cases, foreign-technology evaluation and recommendations for continued collection and analysis',
            'Establishes a structured Project SIGN institutional architecture before later Project Blue Book public framing',
        ],
        'limitations': [
            'The analysis records unresolved reports and hypotheses but does not establish recovered technology, non-human origin or one common cause',
            'The packet is institutional context and analytical history, not the missing Estimate of the Situation',
        ],
    },
]
replace_records(estimate, ['DOW-UAP-D100 · PDF pp. 7–8', *[r['locator'] for r in d100_records]], d100_records)
estimate['sourceQuality'] = ('Exact page-verified public-domain edition of Ruppelt’s 1956 insider account, plus three contemporaneous DOW-UAP-D100 primary-record layers: the November 1948 USAF/AMC acknowledgment and residual-unexplained assessment, AMC’s RAND study request, and the December 1947 Project SIGN assignment/analysis packet. DOW-UAP-D100 is not the missing Estimate and does not authenticate its wording, approval or destruction.')
estimate['gap'] = ('The original Estimate or authenticated copy, its control-register/routing trail, and any destruction or transfer record remain missing. DOW-UAP-D100 independently documents Project SIGN’s institutional architecture, unresolved residue and hypothesis testing, but it is not the missing Estimate and reports no physical evidence or tangible support for an interplanetary conclusion.')
estimate['keyFact'] = ('DOW-UAP-D100 records that Headquarters USAF considered it “inescapable” that some type of flying object had been observed, while AMC retained unexplained reports, sought a RAND study of experimental “spaceships” or test vehicles, and reported no physical evidence or tangible support for an interplanetary conclusion.')
estimate['primaryRecordUpdate'] = {
    'title': 'Project SIGN primary record',
    'points': [
        'USAF called it “inescapable” that some type of flying object had been observed; identity and origin remained undetermined.',
        'AMC retained an unexplained residue and requested a RAND study of experimental “spaceships” or test vehicles—a study request, not a finding.',
        'The December 1947 packet documents formal collection and analytical responsibility while reporting no physical evidence.',
    ],
    'boundary': 'DOW-UAP-D100 is not the missing Estimate of the Situation and does not authenticate its wording, approval, or destruction.',
}
estimate['images'] = [item for item in estimate.get('images', []) if src(item) not in set(d100_ack + d100_rand + d100_arch)] + d100_ack + d100_rand + d100_arch
estimate['evidenceBoundary']['established'] = [
    'Ruppelt published a detailed insider account of an Estimate that concluded the objects were interplanetary.',
    'DOW-UAP-D100 independently records Headquarters USAF acknowledgment that some type of flying object had been observed while identity and origin remained undetermined.',
    'DOW-UAP-D100 documents a residual unexplained set, a RAND “spaceships”/test-vehicle study request, and formal Project SIGN collection and analysis architecture.',
]
estimate['evidenceBoundary']['notEstablished'] = [
    'That DOW-UAP-D100 is the missing Estimate or contains the Estimate’s text.',
    'The exact authorship, approval path, final wording or destruction record of the alleged Estimate.',
    'That the RAND study request was a finding, or that Project SIGN possessed physical evidence or reached an approved extraterrestrial conclusion.',
]

# D101: surface the primary report details without elevating confidence.
gom = by_id['BF-2021-GOM-01']
d101_pages = [image_path('DOW-UAP-D101', p) for p in [1, 2, 5, 6]]
d101_record = {
    'citation': 'Intelligence Information Report, “Multiple Unidentified Aerial Phenomenon Observed… Over Gulf of Oman During AC-130 Gunship Live Fire Training on 8 September 2021,” DOW-UAP-D101',
    'sourceType': 'primary-official-intelligence-information-report',
    'provenance': 'Exact seven-page PDF published through PURSUE Release 05; full local PDF hash verified',
    'locator': 'DOW-UAP-D101 · PDF pp. 1–2, 5–6',
    'url': LANDING,
    'sha256': D101_HASH,
    'sourcePageImages': d101_pages,
    'supports': [
        'Records a source with direct access via official duties reporting approximately 25 AC-130 EO/IR observations during a dated live-fire sortie',
        'Describes two approximately four-foot cold objects 0–20 feet above the water, stationary near a flare for approximately 15 seconds before rapidly departing immediately after trigger pull and before cannon recoil',
        'Records coordinated “dolphins” motion, groups of three, TACTOOL-derived estimates of 250–1,300 mph and coordinates derived from AC-130 sensor GPS',
        'Documents broad military/intelligence dissemination and an attachment list containing one video plus a PowerPoint containing six embedded videos',
    ],
    'limitations': [
        'The IIR is explicitly not finally evaluated intelligence',
        'The full DVR was reported corrupted; native EO/IR data, metadata, telemetry, TACTOOL outputs and independent sensor correlation remain absent',
        'Public PR117–PR122 clips are secondary recordings of an infrared display and do not independently validate range, dimensions, speed, response to gunfire, identity or origin',
    ],
}
replace_records(gom, ['DOW-UAP-D101 · PDF pp. 1, 5–6', d101_record['locator']], [d101_record])
gom['sourceQuality'] = ('Exact official IIR plus six officially associated DVIDS secondary videos. The IIR records direct-duty source access, AC-130 sensor-GPS coordinate derivation, broad dissemination, and an attachment list of one video plus a PowerPoint containing six embedded videos. It remains not finally evaluated intelligence; the corrupted full DVR, native telemetry and independent correlation remain missing.')
gom['keyFact'] = ('The report describes approximately 25 observations, including two cold objects 0–20 feet above the water for about 15 seconds, and TACTOOL-derived 250–1,300 mph estimates. Its strongest test remains unavailable: the full DVR was corrupted, and the public PR117–PR122 clips are secondary display recordings rather than native sensor data.')
gom['gap'] = ('Missing are the corrupted full-sortie DVR, native EO/IR metadata, aircraft telemetry and TACTOOL outputs, independent radar or ship correlation, and the original one-video/PowerPoint attachment package. Without those layers, the reported range, scale, speed, response to gunfire, identity and origin cannot be independently validated.')
gom['primaryRecordUpdate'] = {
    'title': 'D101 source-access and attachment trail',
    'points': [
        'A direct-duty source reported two cold objects approximately 0–20 feet above the water near a flare for about 15 seconds.',
        'The IIR records approximately 25 observations and TACTOOL-derived estimates of 250–1,300 mph; coordinates came from AC-130 sensor GPS.',
        'The attachment list names one video plus a PowerPoint with six embedded videos, while the full DVR was reported corrupted.',
    ],
    'boundary': 'The IIR is not finally evaluated intelligence; public PR117–PR122 display recordings do not independently validate range, speed, response to gunfire, identity, or origin.',
}
gom['images'] = [item for item in gom.get('images', []) if src(item) not in set(d101_pages)]
# Keep current p.5 event-text hero first, then p.2 direct narrative and p.6 attachment page.
gom['images'] = [image_path('DOW-UAP-D101', 5), image_path('DOW-UAP-D101', 2), image_path('DOW-UAP-D101', 6), image_path('DOW-UAP-D101', 1)] + gom['images']
gom['evidenceBoundary']['established'] = [
    'An official IIR records a source with direct access via official duties reporting AC-130 EO/IR observations during a dated Gulf of Oman sortie.',
    'The report records sensor-GPS coordinate derivation, TACTOOL-derived estimates, broad dissemination, and one video plus a PowerPoint containing six embedded videos.',
    'DVIDS officially associates PR117–PR122 and six exact DOD filenames with D101 and states that the clips were captured contemporaneously.',
]
gom['evidenceBoundary']['notEstablished'] = [
    'The identity or origin of the reported objects.',
    'Independent verification of the reported dimensions, 0–20-foot altitude, 250–1,300 mph estimates, or response to gunfire.',
    'That the public secondary recordings are native sensor data or byte-identical exports of the original PowerPoint embeds.',
]

save(ATLAS, atlas)

# Blackfile: add the same bounded tension to Q6 and Q7; leave confidence untouched.
blackfile = load(BLACKFILE)
blackfile['updated'] = '2026-08-10'
tension = {
    'label': 'Internal uncertainty versus public messaging',
    'summary': ('Project SIGN internally retained unexplained reports, considered domestic, foreign and interplanetary possibilities, and sought RAND analysis while recommending narrower public disclosure centered on balloons, astronomical objects and continuing investigation. This documents information management, not proof of a hidden non-human program.'),
    'caseIds': ['BF-SF-07'],
}
for qid in ['q6', 'q7']:
    replace_tension(next(q for q in blackfile['questions'] if q['id'] == qid), tension)
save(BLACKFILE, blackfile)

# Source aliases own only the exact rendered public pages plus the official release landing page.
index = load(INDEX)
d099_main = [d099_cover, image_path('DOW-UAP-D099', 5), image_path('DOW-UAP-D099', 6)]
index['DOW-UAP-D099'] = d099_main + [LANDING]
index['DOW-UAP-D099 · PDF p. 1'] = [d099_cover, LANDING]
index['DOW-UAP-D099 · PDF pp. 5–6'] = d099_main[1:] + [LANDING]
index['DOW-UAP-D100'] = d100_ack + d100_rand + d100_arch + [image_path('DOW-UAP-D100', 152), LANDING]
for record in d100_records:
    index[record['locator']] = record['sourcePageImages'] + [LANDING]
index['DOW-UAP-D100 · PDF p. 152'] = [image_path('DOW-UAP-D100', 152), LANDING]
index['DOW-UAP-D101'] = d101_pages + [LANDING]
index[d101_record['locator']] = d101_pages + [LANDING]
# Remove superseded locator aliases so generated counts remain intentional.
index.pop('DOW-UAP-D100 · PDF pp. 7–8', None)
index.pop('DOW-UAP-D101 · PDF pp. 1, 5–6', None)
save(INDEX, index)

print('Applied Release 05 source-depth completion: BF-SF-07, BF-2021-GOM-01, BF-1946-GR-01, Blackfile Q6/Q7')
