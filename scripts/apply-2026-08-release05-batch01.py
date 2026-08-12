#!/usr/bin/env python3
"""Apply PURSUE Release 05 evidence to Atlas enrichment Batch 01 (cases 1-20)."""
from __future__ import annotations

import json
from pathlib import Path
from runpy import run_path

ROOT = Path(__file__).resolve().parents[1]
ATLAS = ROOT / 'atlas-data.json'
PUBLIC = ROOT / 'public-source-manifest.json'
INDEX = ROOT / 'source-file-index.json'
HERO_MANIFEST = ROOT / 'atlas-hero-visual-manifest.json'
LANDING = 'https://www.war.gov/UFO/?releaseDate=Release+05&release=05'
BASE = 'assets/sources/PURSUE-RELEASE-05'


def load(path: Path):
    return json.loads(path.read_text())


def save(path: Path, payload):
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + '\n')


def append_unique(items, value, key=None):
    if key is None:
        if value not in items:
            items.append(value)
        return
    marker = value.get(key)
    if not any(isinstance(item, dict) and item.get(key) == marker for item in items):
        items.append(value)


def replace_record(case, locator, record):
    records = case.setdefault('sourceRecords', [])
    records[:] = [item for item in records if item.get('locator') != locator]
    records.append(record)


def add_public(case, note):
    sources = case.setdefault('publicSources', [])
    source = {
        'label': 'War.gov — PURSUE Release 05',
        'url': LANDING,
        'publisher': 'U.S. Department of War',
        'access': 'Public official release landing page',
        'scope': 'official-release-custody',
        'note': note,
    }
    existing = next((item for item in sources if item.get('url') == LANDING), None)
    if existing:
        existing.update(source)
    else:
        sources.append(source)


atlas = load(ATLAS)
by_id = {case['id']: case for case in atlas['cases']}

d098_cover = f'{BASE}/DOW-UAP-D098-pdf-page-001.png'
d098_pages = [f'{BASE}/DOW-UAP-D098-pdf-page-006.png', f'{BASE}/DOW-UAP-D098-pdf-page-009.png']
d099_pages = [f'{BASE}/DOW-UAP-D099-pdf-page-005.png', f'{BASE}/DOW-UAP-D099-pdf-page-006.png']
d100_pages = [f'{BASE}/DOW-UAP-D100-pdf-page-007.png', f'{BASE}/DOW-UAP-D100-pdf-page-008.png']
d100_ghost_page = f'{BASE}/DOW-UAP-D100-pdf-page-152.png'

ghost = by_id['BF-1946-GR-01']
ghost['keyQuote'] = 'The best evidence, at present, is that there have been only 2 or 3 real incidents, perhaps as many as 5 or 10, of low-flying missiles of the V-1 type.'
ghost['quoteSource'] = 'War Department Intelligence Division, “Ghost Rockets Over Scandinavia,” 20 January 1947, DOW-UAP-D099, PDF p. 6 / report p. 20'
ghost['quoteConfidence'] = 'High — visually verified in the exact War.gov Release 05 PDF. This is the U.S. War Department review’s analytical conclusion, not proof that any reported object was a Soviet missile.'
ghost['sourceQuality'] = 'Official Swedish archival custody family plus exact U.S. records released in PURSUE Release 05: a January 1947 War Department Intelligence Division review (DOW-UAP-D099) and a January 1948 Project SIGN request for the complete “Swedish Incidents” file within DOW-UAP-D100. The review records nearly 1,000 Swedish reports by late July 1946, states that U.S. personnel had not seen fragments or impact evidence, and narrows its missile hypothesis to a small residue. Project SIGN interest establishes institutional linkage, not new event evidence. Exact Swedish item shelfmarks and the underlying diplomatic source packet remain unresolved.'
ghost['keyFact'] = 'A January 1947 War Department review records nearly 1,000 Swedish reports by late July 1946 but says no U.S. military or naval personnel had seen fragments, impact points or other direct missile evidence. Its own conclusion reduced the potentially real low-flying missile residue to 2–3 incidents, perhaps 5–10. One year later, Project SIGN formally requested the complete “Swedish Incidents” file for its flying-disc investigation.'
ghost['official'] = 'Swedish communiqués shifted over time. A separate U.S. War Department review judged many reports celestial or explainable, hypothesized only a small low-flying missile residue, and did not establish Soviet origin.'
ghost['gap'] = 'Still needed: item-level Riksarkivet/Krigsarkivet shelfmarks, first-generation Swedish scans, the source diplomatic and attaché reporting behind DOW-UAP-D099, and physical evidence for any specific incident. Release custody authenticates the review, not its Soviet/V-1 hypothesis.'
append_unique(ghost['sources'], 'DOW-UAP-D099 · War Department Intelligence Division review, 20 January 1947')
append_unique(ghost['sources'], 'DOW-UAP-D100 · Project SIGN request for the Swedish Incidents file, 23 January 1948')
for image in d099_pages:
    append_unique(ghost.setdefault('images', []), image)
append_unique(ghost.setdefault('images', []), d100_ghost_page)
replace_record(ghost, 'DOW-UAP-D099 · PDF pp. 5–6', {
    'citation': 'War Department Intelligence Division, “Ghost Rockets Over Scandinavia,” 20 January 1947, DOW-UAP-D099',
    'sourceType': 'primary-official-intelligence-review',
    'provenance': 'Exact PDF published by the U.S. Department of War in PURSUE Release 05; full local copy hash-verified against the original download',
    'locator': 'DOW-UAP-D099 · PDF pp. 5–6',
    'url': LANDING,
    'sha256': '59bdcb1406b50d7dab7f13dbce940eb247a0724c744100d34f9a53ea3209e2f4',
    'sourcePageImages': d099_pages,
    'supports': [
        'Documents the U.S. War Department’s January 1947 assessment of the 1946 Scandinavian reporting wave',
        'Records nearly 1,000 reports received by Swedish authorities by late July 1946',
        'States that no U.S. military or naval personnel in Sweden had seen fragments, impact points or other direct guided-missile evidence',
        'Preserves the review’s limited conclusion that 2–3, perhaps 5–10, low-flying missile incidents might have been real',
    ],
    'limitations': [
        'The review synthesizes intelligence reporting and does not provide the complete underlying Swedish case files or attaché traffic',
        'Its V-1/Soviet hypothesis is an analytical judgment, not an authenticated launch record or recovered object',
        'The review says the evidence was conflicting and attributes many reports to meteors, fireworks or other explainable causes',
    ],
})
replace_record(ghost, 'DOW-UAP-D100 · PDF p. 152', {
    'citation': 'Air Materiel Command, Project SIGN request for the complete “Swedish Incidents” file, 23 January 1948, DOW-UAP-D100',
    'sourceType': 'primary-official-institutional-linkage-record',
    'provenance': 'Exact page within the 245-page DOW-UAP-D100 PDF published by the U.S. Department of War in PURSUE Release 05; full local copy hash-verified against the original download',
    'locator': 'DOW-UAP-D100 · PDF p. 152',
    'url': LANDING,
    'sha256': '4052303ee0d521c15656b65fed3075734c83332ec5db319c744f0dbe53b8ec90',
    'sourcePageImages': [d100_ghost_page],
    'supports': [
        'Documents Project SIGN’s formal request for the complete Swedish Incidents file on 23 January 1948',
        'Establishes a direct institutional link between the 1946 Swedish reports and the early U.S. Air Force flying-disc investigation',
    ],
    'limitations': [
        'A file-transfer request proves institutional interest, not the identity or reality of any reported object',
        'The page does not contain the Swedish case files, physical evidence or a Project SIGN analytical conclusion about the incidents',
        'It is institutional context rather than independent event corroboration',
    ],
})
ghost['evidenceBoundary'] = {
    'established': [
        'Swedish authorities received a large wave of reports in 1946 and opened an official investigation.',
        'The January 1947 War Department review records nearly 1,000 reports by late July and no direct fragments or impact evidence seen by U.S. personnel.',
        'A 23 January 1948 Air Materiel Command letter shows Project SIGN requested the complete Swedish Incidents file for review.',
        'The review treated only a small residue as potentially real low-flying missile incidents.',
    ],
    'notEstablished': [
        'That 1,500 or 2,000 reports were independently verified anomalous objects.',
        'That the reported objects were Soviet weapons, extraterrestrial craft or one uniform phenomenon.',
        'That any recovered fragment in the reviewed record came from an unidentified vehicle.',
    ],
    'competingExplanations': ['Meteors, fireworks, aircraft, V-1-type missiles, public-reporting amplification and observer error all remain part of the historical record.'],
}
add_public(ghost, 'Official custody page for DOW-UAP-D099 and DOW-UAP-D100. The records authenticate a 1947 intelligence assessment and Project SIGN’s 1948 file request—not the Soviet-missile hypothesis or every underlying report.')

film_record = {
    'citation': 'U.S. Naval Photographic Interpretation Center, “Interpretation of Movies of Unidentified Objects,” 4 May 1953, DOW-UAP-D098',
    'sourceType': 'primary-official-photographic-analysis',
    'provenance': 'Exact PDF published by the U.S. Department of War in PURSUE Release 05; full local copy hash-verified against the original download',
    'locator': 'DOW-UAP-D098 · PDF pp. 6 and 9',
    'url': LANDING,
    'sha256': 'a8f271bb7bae396631eb3e35070fab285eb0d3258041b042b1a5a6b3e0d9c4f1',
    'sourcePageImages': d098_pages,
    'supports': [
        'Documents a 1953 Naval Photographic Interpretation Center analysis of the 1952 Utah and 1950 Montana films',
        'Preserves the analysts’ majority view that the Utah images were light sources not identified as natural phenomena or commonly known man-made objects',
        'Records film-generation and measurement limitations, including that the Utah analysis film was a duplicate of a copy',
    ],
    'limitations': [
        'The report explicitly says its analysis did not necessarily represent the official position of the Navy or the Center',
        'The analysts said the investigation lacked proper equipment, money and personnel and that no attempt was made to corroborate the opinions presented',
        'Distance and trajectory assumptions materially affected computed sizes, velocities and accelerations',
        'The document is an analytical layer, not a recovered camera original or a final identification of either film',
    ],
}
for cid in ['BF-1950-GF-01', 'BF-1952-TM-01']:
    case = by_id[cid]
    append_unique(case['sources'], 'DOW-UAP-D098 · Naval Photographic Interpretation Center film analysis, 4 May 1953')
    replace_record(case, film_record['locator'], dict(film_record))
    add_public(case, 'Official custody page for DOW-UAP-D098. The report documents one 1953 analytical position and its limitations; it is not a final object-origin finding.')

great = by_id['BF-1950-GF-01']
great['sourceQuality'] = 'Exact NARA case-file and motion-picture-item custody, plus the exact 1953 Naval Photographic Interpretation Center analysis released as DOW-UAP-D098. The Navy report adds a contemporaneous laboratory layer but expressly disclaims official-policy status and records material resource and corroboration limits. No camera original or complete generation ledger is identified.'
append_unique(great.setdefault('images', []), d098_pages[1])

tremonton = by_id['BF-1952-TM-01']
tremonton['sourceQuality'] = 'Exact NARA case-file and motion-picture custody with copy-generation evidence, now joined by the exact 1953 Naval Photographic Interpretation Center analysis released as DOW-UAP-D098. That report says the analyzed Utah film was a duplicate of a copy, gives a majority unidentified/light-source assessment, and explicitly records resource, corroboration and official-position limitations. The camera original and full laboratory ledger remain unlocated.'
for image in d098_pages:
    append_unique(tremonton.setdefault('images', []), image)
old_film_hero = 'assets/evidence/hero-visuals/TREMONTON-1952-case-sheet-film-inset.jpg'
old_film_visual = {
    'src': old_film_hero,
    'rank': 5,
    'caption': 'Film-frame reproduction embedded in the Project Blue Book/Newhouse case sheet.',
    'visualType': 'historical-film-frame-reproduction',
    'provenance': 'Project Blue Book case-sheet reproduction',
    'evidenceStatus': 'Source-derived reproduction, not an original film scan; alleged objects remain unresolved in this record.',
}
tremonton_hero = {
    'src': d098_cover,
    'mediaType': 'image',
    'visualType': 'official-document-routing-sheet',
    'caption': 'Bureau of Aeronautics routing sheet for the 1953 Navy film-analysis report covering the Tremonton and Great Falls films.',
    'provenance': 'U.S. Navy / Naval Photographic Interpretation Center, DOW-UAP-D098, PDF p. 1',
    'evidenceStatus': 'Official administrative routing sheet for the analysis; documentary evidence of the report, not an image of the reported objects.',
    'isEventEvidence': False,
}
tremonton['image'] = d098_cover
tremonton['heroVisual'] = tremonton_hero
tremonton['images'] = [d098_cover, old_film_visual] + [
    image for image in tremonton.get('images', [])
    if (image.get('src') or image.get('url') if isinstance(image, dict) else image) not in {d098_cover, old_film_hero}
]

estimate = by_id['BF-SF-07']
estimate['sourceQuality'] = 'Exact page-verified public-domain edition of Ruppelt’s 1956 insider account, plus a contemporaneous 1948 Project SIGN/USAF correspondence packet released as DOW-UAP-D100. DOW-UAP-D100 verifies institutional context and actual November 1948 analytical language; it does not contain or authenticate the missing Estimate of the Situation.'
estimate['gap'] = 'No copy, index entry or destruction certificate for the Estimate has been located. DOW-UAP-D100 adds contemporaneous Project SIGN context but not the Estimate itself: the packet reports approximately 180 studied incidents, unresolved cases and no tangible evidence supporting an interplanetary conclusion.'
append_unique(estimate['sources'], 'DOW-UAP-D100 · Air Materiel Command / Project SIGN correspondence, 1947–1948')
for image in d100_pages:
    append_unique(estimate.setdefault('images', []), image)
replace_record(estimate, 'DOW-UAP-D100 · PDF pp. 7–8', {
    'citation': 'Air Materiel Command / Headquarters USAF, Project SIGN correspondence and flying-object assessment, 1947–1948, DOW-UAP-D100',
    'sourceType': 'primary-official-institutional-record-packet',
    'provenance': 'Exact 245-page PDF published by the U.S. Department of War in PURSUE Release 05; full local copy hash-verified against the original download',
    'locator': 'DOW-UAP-D100 · PDF pp. 7–8',
    'url': LANDING,
    'sha256': '4052303ee0d521c15656b65fed3075734c83332ec5db319c744f0dbe53b8ec90',
    'sourcePageImages': d100_pages,
    'supports': [
        'Documents a November 1948 Air Materiel Command study of approximately 180 incidents',
        'Records that some reports lacked a reasonable everyday explanation while no physical evidence had been obtained',
        'Records that the interplanetary possibility was considered but tangible support was completely lacking',
        'Provides contemporaneous Project SIGN institutional context for Ruppelt’s later Estimate account',
    ],
    'limitations': [
        'The packet does not contain the alleged Estimate of the Situation',
        'It does not authenticate the Estimate’s wording, authorship, routing, approval or destruction',
        'A later institutional packet cannot convert Ruppelt’s retrospective account into a recovered primary document',
    ],
})
estimate['evidenceBoundary'] = {
    'established': [
        'Ruppelt published a detailed insider account of an Estimate that concluded the objects were interplanetary.',
        'DOW-UAP-D100 independently establishes active Project SIGN analysis in 1948 and preserves the contemporaneous unresolved/no-physical-evidence boundary.',
    ],
    'notEstablished': [
        'That DOW-UAP-D100 is the Estimate or contains the Estimate’s text.',
        'The exact authorship, approval path, final wording or destruction record of the alleged Estimate.',
        'That Project SIGN possessed physical evidence or reached an institutionally approved extraterrestrial conclusion.',
    ],
    'competingExplanations': ['The missing-document account may preserve a real rejected draft, a later reconstruction of internal debate, or a document whose title and administrative status shifted in recollection.'],
}
add_public(estimate, 'Official custody page for DOW-UAP-D100. It provides contemporaneous Project SIGN context but does not recover or authenticate the missing Estimate.')

save(ATLAS, atlas)

public = load(PUBLIC)
for cid in ['BF-1946-GR-01', 'BF-1950-GF-01', 'BF-1952-TM-01', 'BF-SF-07']:
    public[cid] = by_id[cid]['publicSources']
save(PUBLIC, public)

if HERO_MANIFEST.is_file():
    hero_manifest = load(HERO_MANIFEST)
    hero_manifest['BF-1952-TM-01'] = tremonton_hero
    save(HERO_MANIFEST, hero_manifest)

index = load(INDEX)
index['DOW-UAP-D098'] = [d098_cover] + d098_pages + [LANDING]
index['DOW-UAP-D098 · PDF pp. 6 and 9'] = d098_pages + [LANDING]
index['TREMONTON-1952'] = [d098_cover, old_film_hero] + [
    item for item in index.get('TREMONTON-1952', []) if item not in {d098_cover, old_film_hero}
]
index['DOW-UAP-D099'] = d099_pages + [LANDING]
index['DOW-UAP-D099 · PDF pp. 5–6'] = d099_pages + [LANDING]
index['DOW-UAP-D100'] = d100_pages + [d100_ghost_page, LANDING]
index['DOW-UAP-D100 · PDF pp. 7–8'] = d100_pages + [LANDING]
index['DOW-UAP-D100 · PDF p. 152'] = [d100_ghost_page, LANDING]
save(INDEX, index)

# Keep this historical tranche replay-safe by applying the current authoritative
# Release 05 completion layer after its original mutations.
run_path(str(ROOT / 'scripts/apply-2026-08-release05-source-depth-completion.py'), run_name='__main__')

print('Applied PURSUE Release 05 enrichment to Atlas Batch 01: BF-1946-GR-01, BF-1950-GF-01, BF-1952-TM-01, BF-SF-07')
