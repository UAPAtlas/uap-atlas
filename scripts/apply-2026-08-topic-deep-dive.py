#!/usr/bin/env python3
"""Apply the August 2026 NARA/Borland/KONA/Brown provenance tranche."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ATLAS = ROOT / 'atlas-data.json'
PUBLIC = ROOT / 'public-source-manifest.json'
INDEX = ROOT / 'source-file-index.json'
BLACKFILE = ROOT / 'blackfile-analysis.json'


def load(path):
    return json.loads(path.read_text())


def save(path, payload):
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + '\n')


def append_unique(items, value, key=None):
    if key is None:
        if value not in items:
            items.append(value)
        return
    marker = value.get(key)
    if not any(isinstance(item, dict) and item.get(key) == marker for item in items):
        items.append(value)


def add_source_record(case, record):
    records = case.setdefault('sourceRecords', [])
    marker = record['citation']
    if not any(r.get('citation') == marker for r in records):
        records.append(record)


def add_public(case, source):
    sources = case.setdefault('publicSources', [])
    if not any(s.get('url') == source['url'] for s in sources):
        sources.append(source)


atlas = load(ATLAS)
by_id = {case['id']: case for case in atlas['cases']}

hartford_images = [
    ('0305', 'Project 10073 record card dated 4 September 1960. It records a ground-visual report, a physical specimen, a falling object, and the summary disposition “Other — Furnace slag.”'),
    ('0306', 'Wright-Patterson Aeronautical Systems Division evaluation report dated 8 May 1961. Emission spectroscopy found ordinary terrestrial elements and recorded no conclusion or recommendation beyond the submitted data.'),
    ('0310', 'Scientific-analysis page separating eleven sample segments into carbonaceous, aluminum, stone, and slag groups. It says the slag appears local and only the aluminum samples seem clearly associated with the observed fall.'),
    ('0311', 'Continuation of the sample analysis documenting elemental comparisons and uncertainty in individual assignments.'),
    ('0316', 'Air Force message documenting coordination with Hartford police, Professor Robert Brown, and Smithsonian Astrophysical Observatory personnel regarding collection of incident material.'),
    ('0324', 'Air Force Cambridge Research Laboratories report, “Preliminary Analysis and Certain Historical Details Relating to Objects which Fell at Hartford, Connecticut,” recording the 20:15 EDT event chronology.'),
    ('0327', 'T. Townsend Brown letter to Major Robert Friend, 12 October 1960, describing Brown’s interest in the Hartford fall and promising coordinated reports. It records Brown’s involvement, not validation of his gravity claims.'),
    ('0329', 'Professor Robert L. Brown letter distinguishing the later Woodbridge particle from the Hartford fall in space and time.'),
    ('0331', 'T. Townsend Brown letter describing changing-weight, barium/strontium, radiation and induced-weight observations during Whitehall-Rand testing. These are participant claims, not Air Force findings.'),
    ('0332', 'Continuation of Brown’s 26 October 1960 letter, explicitly noting the Woodbridge material was not directly related to the Hartford fall and advancing speculative decay and weight-change interpretations.'),
]
images = []
for object_id, caption in hartford_images:
    url = f'assets/evidence/HARTFORD-1960/NARA-NAID-28989015-object-{object_id}.jpg'
    images.append({
        'url': url,
        'kind': 'primary-document',
        'source': f'https://catalog.archives.gov/medialive/15/9890/28989015/content/TB0106/T1206-ProjectBlueBook/T1206_0040/images/{object_id}.jpg',
        'sourceName': f'NARA NAID 28989015, digital object {object_id}',
        'sourceType': 'federal-archive-scan',
        'caption': caption,
        'rights': 'U.S. federal record in NARA custody; exact NARA scan preserved without recompression.',
    })

hartford = {
    'keyQuote': 'At 2015 E.D.T. on the night of 4 September 1960, a lady standing near the back door of her first floor apartment at [redacted], Hartford, Connecticut, was startled by a “swishing noise” followed by a thud.',
    'quoteSource': 'Air Force Cambridge Research Laboratories, “Preliminary Analysis and Certain Historical Details Relating to Objects which Fell at Hartford, Connecticut,” NARA NAID 28989015, object 0324',
    'quoteConfidence': 'High — visually verified in the exact NARA scan. It records the witness chronology; it does not determine the origin of every collected sample.',
    'significance': 'High archival and physical-trace significance; extraordinary origin not established.',
    'sourceQuality': 'Exact 73-object Project Blue Book file unit acquired from NARA with SHA-256 custody manifest. Page-adjudicated records include the Blue Book card, an AFCRL witness/material report, Wright-Patterson spectroscopy, Air Force collection traffic, and Brown/Whitehall-Rand correspondence. Government custody authenticates the investigation and laboratory work, not Brown’s gravity interpretation or a non-human origin.',
    'coordinateBasis': 'Hartford city centroid; the street address is redacted in the federal record',
    'coordinatePrecision': 'city',
    'id': 'BF-1960-HF-01',
    'title': 'Hartford Material-Fall Investigation',
    'date': '4 SEP 1960',
    'year': 1960,
    'location': 'Hartford, Connecticut',
    'mode': 'approximate',
    'lon': -72.6734,
    'lat': 41.7658,
    'expectedCountry': 'United States of America',
    'expectedAdmin1': 'Connecticut',
    'geometryExpectation': 'admin1',
    'agency': 'USAF / AFCRL / ATIC',
    'domain': 'HISTORICAL / PHYSICAL TRACE',
    'status': 'DOCUMENTED REPORT · CONVENTIONAL DISPOSITION / MATERIAL QUESTIONS RETAINED',
    'confidence': 'PRIMARY FEDERAL RECORD · EXTRAORDINARY ORIGIN NOT ESTABLISHED',
    'summary': 'At 20:15 EDT on 4 September 1960, Hartford witnesses reported a swishing sound, a green pendant or cone-like light, impact, smoke and a smoldering shed. Police, Smithsonian-linked personnel and the Air Force collected material. Project Blue Book’s summary card closed the case as furnace slag, but the underlying AFCRL analysis was more granular: slag appeared local, stones were not analyzed, carbonaceous material was inconclusive, and only aluminum samples seemed clearly associated with the observed fall. Later Wright-Patterson spectroscopy found ordinary elements and made no extraordinary conclusion.',
    'keyFact': 'The file is stronger and more complicated than its one-line “furnace slag” disposition: the federal record documents a witnessed fall and sample investigation while leaving the aluminum-fall relationship unresolved and offering no evidence of exotic composition.',
    'official': 'Project Blue Book classified the event as “Other — Furnace slag.” The underlying AFCRL report said the slag was locally derived but identified aluminum fragments as the samples most clearly associated with the observed fall. A 1961 Wright-Patterson evaluation found ordinary elemental constituents and recorded “Conclusions: None.”',
    'gap': 'The complete contemporaneous sample custody chain, surviving specimens, calibrated raw spectra, and independent replication are not public. The file does not establish where the aluminum originated, and it does not tie the separate Woodbridge fall to the Hartford event.',
    'whyItMatters': 'It shows why archival depth matters: a summary-card identification can coexist with a more qualified laboratory record underneath it, while later gravity claims can outrun both.',
    'sources': [
        'HARTFORD-1960 · NARA NAID 28989015 · complete 73-object Project Blue Book file unit',
        'HARTFORD-1960 · AFCRL historical/material report and Wright-Patterson evaluation',
    ],
    'sourceLabel': 'NARA Project Blue Book file and Air Force laboratory reports',
    'sourceLocator': 'NARA NAID 28989015 · Hartford, Connecticut, September 1960',
    'relatedCaseIds': ['BF-SF-03'],
    'heroFact': 'A witnessed green fall, recovered material and Air Force laboratory work are documented; the official “furnace slag” card compresses a more qualified record underneath.',
    'image': 'assets/evidence/HARTFORD-1960/NARA-NAID-28989015-object-0305.jpg',
    'images': images,
    'caseTypes': ['physical-trace', 'archival-event'],
    'evidenceModes': ['testimony', 'physical-sample', 'laboratory-analysis', 'official-record'],
    'environment': ['terrestrial'],
    'outcome': 'documented',
    'confidenceModel': {
        'record': 'confirmed-primary-federal-file',
        'anomaly': 'reported-fall-origin-unresolved',
        'provenance': 'exact-nara-file-unit',
        'material': 'ordinary-elements-with-association-question',
    },
    'temporal': {
        'dateLabel': '4 SEP 1960',
        'year': 1960,
        'startDateTime': '1960-09-04T20:15:00-04:00',
        'endDateTime': None,
        'timezone': 'America/New_York',
        'durationSeconds': None,
        'precision': 'minute',
        'eventForm': 'single-event',
    },
    'geospatial': {
        'geometry': {'type': 'Point', 'coordinates': [-72.6734, 41.7658]},
        'role': 'representative-centroid',
        'precision': 'city',
        'uncertaintyKm': 8,
        'basis': 'Hartford city centroid; exact street address is redacted in the federal report',
    },
    'sourceRecords': [
        {
            'citation': 'National Archives, Project Blue Book file unit “Hartford, Connecticut, September 1960,” NAID 28989015',
            'sourceType': 'primary-federal-archival-file-unit',
            'provenance': 'NARA Record Group 341, Project Blue Book case-file series; exact file unit NAID 28989015; 73 of 73 media objects acquired and SHA-256 manifested',
            'locator': 'Objects 0305–0377; selected objects 0305, 0306, 0310, 0311, 0316, 0324, 0327, 0329, 0331 and 0332',
            'url': 'https://catalog.archives.gov/id/28989015',
            'supports': [
                'Authenticates Project Blue Book custody for the Hartford September 1960 investigation',
                'Documents witness reports, material collection, agency correspondence and laboratory analysis',
                'Preserves the summary-card furnace-slag disposition and the more qualified underlying material analysis',
            ],
            'limitations': [
                'Federal custody authenticates the records, not an extraordinary origin for the event or samples',
                'The packet includes later correspondence and a distinct Woodbridge fall that must not be merged into the Hartford chronology',
                'Not every analytical page identifies complete custody, calibration or surviving sample disposition',
            ],
        },
        {
            'citation': 'Air Force Cambridge Research Laboratories, “Preliminary Analysis and Certain Historical Details Relating to Objects which Fell at Hartford, Connecticut,” September 1960',
            'sourceType': 'primary-official-witness-and-material-analysis',
            'provenance': 'Exact NARA scans within NAID 28989015',
            'locator': 'Objects 0324 onward for witness chronology; objects 0310–0315 for sample-group analysis',
            'url': 'assets/evidence/HARTFORD-1960/NARA-NAID-28989015-object-0324.jpg',
            'supports': [
                'Records the 20:15 EDT swish, thud, green-fire report, smoke and smoldering shed',
                'Separates sample groups and states that local slag was distinct from aluminum material associated with the observed fall',
            ],
            'limitations': [
                'Association with a fall does not establish aerial origin, manufacture, trajectory or non-human provenance',
                'Some stones were not analyzed and carbonaceous material remained inconclusive',
            ],
        },
        {
            'citation': 'Aeronautical Systems Division, Wright-Patterson AFB, Evaluation Report ASD P 61-11, “Analysis of Foreign Material,” 8 May 1961',
            'sourceType': 'primary-official-laboratory-evaluation',
            'provenance': 'Exact NARA scan within NAID 28989015',
            'locator': 'Object 0306',
            'url': 'assets/evidence/HARTFORD-1960/NARA-NAID-28989015-object-0306.jpg',
            'supports': ['Documents emission spectroscopy and ordinary constituent elements including calcium, silicon, magnesium, iron, manganese, aluminum, titanium and chromium'],
            'limitations': ['The report records “Conclusions: None” and “Recommendations: None, data merely submitted”; it does not identify a source object or extraordinary mechanism'],
        },
    ],
    'phenomena': {
        'shapes': ['pendant-shaped light', 'cone of green fire'],
        'objectCount': 1,
        'luminosity': 'green with orange/red; brief glowing material after impact',
        'motion': ['descending', 'impact reported'],
        'effects': ['smoke', 'smoldering shed', 'recovered material'],
    },
    'observation': {
        'witnessCount': 3,
        'witnessRoles': ['civilian witnesses', 'property superintendent', 'Hartford police'],
        'sensors': ['unaided-visual', 'physical-sample', 'laboratory-spectroscopy'],
        'durationSeconds': None,
        'independentWitnessGroups': 3,
    },
    'evidenceDepthStatus': 'complete-primary-packet-acquired-page-adjudicated',
    'taxonomyOriginal': {
        'domain': 'PROJECT BLUE BOOK / PHYSICAL MATERIAL',
        'status': 'CONVENTIONAL DISPOSITION WITH QUALIFIED UNDERLYING ANALYSIS',
        'confidence': 'CONFIRMED FILE / ORIGIN UNRESOLVED',
    },
    'taxonomyVersion': 'atlas-controlled-v1',
    'heroVisual': {
        'src': 'assets/evidence/HARTFORD-1960/NARA-NAID-28989015-object-0305.jpg',
        'mediaType': 'image',
        'visualType': 'official-record-card',
        'caption': 'Project 10073 record card for Hartford, Connecticut, 4 September 1960.',
        'provenance': 'NARA NAID 28989015, digital object 0305',
        'evidenceStatus': 'Authentic federal record; documents the report and disposition, not the origin of the falling material.',
        'isEventEvidence': True,
        'sourceUrl': 'https://catalog.archives.gov/medialive/15/9890/28989015/content/TB0106/T1206-ProjectBlueBook/T1206_0040/images/0305.jpg',
    },
    'publicSources': [
        {
            'label': 'NARA Catalog — Hartford, Connecticut, September 1960 (NAID 28989015)',
            'url': 'https://catalog.archives.gov/id/28989015',
            'publisher': 'National Archives and Records Administration',
            'access': 'Public catalog and 73 media objects',
            'scope': 'exact-primary-file-unit',
            'note': 'Complete Project Blue Book file unit. Custody authenticates the investigation, not an extraordinary origin.',
        },
    ],
    'evidenceBoundary': {
        'established': [
            'Witnesses reported a swish, a green descending light or cone, impact effects, smoke and a smoldering shed in Hartford at approximately 20:15 EDT on 4 September 1960.',
            'Police, Smithsonian-linked personnel and Air Force organizations collected or analyzed material under Project Blue Book custody.',
            'The Project Blue Book record card carried the disposition “Other — Furnace slag.”',
            'The underlying analysis said slag appeared to be of Hartford origin while only the aluminum samples seemed clearly due to the observed fall.',
            'Later Wright-Patterson spectroscopy found ordinary constituent elements and recorded no extraordinary conclusion.',
        ],
        'notEstablished': [
            'A craft, manufactured aerial object, meteorite, weapon, non-human material or electrogravitic mechanism.',
            'That every collected fragment came from the same source or from the observed fall.',
            'That the distinct Woodbridge fall and Hartford event shared a source, orbit or mechanism.',
            'T. Townsend Brown’s changing-mass, radiation, barium/strontium or gravity-neutralization interpretations.',
        ],
        'competingExplanations': [
            'Local industrial furnace slag and background coal/stone contamination account for part of the recovered material.',
            'An ordinary falling or burning aluminum object could account for the event-associated metallic fragments without exotic composition.',
            'Later Brown/Whitehall-Rand correspondence amplified a qualified material investigation into speculative gravity claims.',
        ],
    },
}

if hartford['id'] in by_id:
    idx = atlas['cases'].index(by_id[hartford['id']])
    atlas['cases'][idx] = hartford
else:
    atlas['cases'].append(hartford)
by_id = {case['id']: case for case in atlas['cases']}

# Brown / Winterhaven enrichment.
brown = by_id['BF-SF-03']
brown['date'] = '1929–1961'
brown['summary'] = brown['summary'].rstrip() + ' NARA NAID 28989015 now adds a complete 1960–1961 federal packet documenting Brown’s Whitehall-Rand participation in the Hartford/Woodbridge material investigation. The packet authenticates his correspondence and testing claims but does not validate variable mass, radiation-induced weight change, gravity neutralization or non-human material.'
brown['sourceQuality'] = brown['sourceQuality'].rstrip() + ' NARA NAID 28989015 adds exact federal custody for Brown’s Hartford/Woodbridge correspondence, while DTIC ARL-TR-3005 confirms force on asymmetric capacitors in air and explicitly leaves vacuum testing unresolved.'
brown['gap'] = 'Still needed are first-party government custody for Project Winterhaven and ONR File 24-185; any contract-award, funding, completion or service-adoption record; first-generation Bahnson notebooks and calibrated vacuum data; and independent replication of Brown’s changing-mass claims. The NARA Hartford/Woodbridge packet preserves the claims but does not validate their mechanism.'
append_unique(brown['relatedCaseIds'], 'BF-1960-HF-01')
for path in [
    'assets/evidence/HARTFORD-1960/NARA-NAID-28989015-object-0327.jpg',
    'assets/evidence/HARTFORD-1960/NARA-NAID-28989015-object-0331.jpg',
    'assets/evidence/HARTFORD-1960/NARA-NAID-28989015-object-0332.jpg',
]:
    append_unique(brown.setdefault('images', []), path)
add_source_record(brown, {
    'citation': 'T. Townsend Brown / Whitehall-Rand correspondence in NARA Project Blue Book file unit NAID 28989015, October 1960–May 1961',
    'sourceType': 'primary-participant-correspondence-in-federal-custody',
    'provenance': 'Exact NARA scans in Record Group 341, file unit “Hartford, Connecticut, September 1960”',
    'locator': 'Objects 0327 and 0331–0332; related correspondence objects within the 73-object file',
    'url': 'https://catalog.archives.gov/id/28989015',
    'supports': [
        'Authenticates Brown’s direct involvement with ATIC, Major Robert Friend and the Hartford/Woodbridge material investigation',
        'Documents that Brown/Whitehall-Rand reported changing sample weight, surface accretion, radiation and induced-weight effects',
        'Documents Brown’s request for confidentiality and expectation that classification might occur',
    ],
    'limitations': [
        'The changing-mass, radiation, barium/strontium and induced-weight statements are Brown’s participant claims, not Air Force findings',
        'The correspondence does not provide a complete calibrated protocol, independent replication or surviving sample chain',
        'The Woodbridge material was explicitly separate from the Hartford fall in time and place',
    ],
})
add_source_record(brown, {
    'citation': 'Thomas B. Bahder and Chris Fazi, “Force on an Asymmetric Capacitor,” ARL-TR-3005, June 2003, DTIC ADA416740',
    'sourceType': 'official-dod-technical-report',
    'provenance': 'U.S. Army Research Laboratory / Defense Technical Information Center',
    'locator': 'ARL-TR-3005, abstract and conclusions',
    'url': 'https://apps.dtic.mil/sti/tr/pdf/ADA416740.pdf',
    'supports': [
        'ARL experimentally verified net force on asymmetric capacitors in air',
        'The report records the Brown/Bahnson patent lineage and identifies vacuum testing as a necessary next step',
    ],
    'limitations': [
        'Force in air does not establish gravity coupling or useful vacuum thrust',
        'The report says the physical basis was not understood at that stage and does not validate an operational electrogravitic craft',
    ],
})
add_source_record(brown, {
    'citation': 'Dennis J. Cravens, “Electric Propulsion Study,” AL-TR-89-040, August 1990, DTIC ADA227121',
    'sourceType': 'official-air-force-contractor-advanced-concepts-review',
    'provenance': 'Air Force Astronautics Laboratory / SAIC report in DTIC custody',
    'locator': 'AL-TR-89-040, preface and Brown/asymmetric-capacitor discussion',
    'url': 'https://apps.dtic.mil/sti/pdfs/ADA227121.pdf',
    'supports': ['Documents Air Force-contractor review of Brown-type propulsion claims as a speculative advanced concept'],
    'limitations': ['A review of a stigmatized or speculative concept is not experimental validation, program adoption or UAP evidence'],
})
for source in [
    {'label':'NARA Catalog — Hartford, Connecticut, September 1960 (NAID 28989015)','url':'https://catalog.archives.gov/id/28989015','publisher':'National Archives and Records Administration','access':'Public catalog and media','scope':'primary-brown-correspondence-in-federal-file','note':'Contains exact Brown/Whitehall-Rand correspondence and Air Force laboratory records. It authenticates participation and claims, not anomalous physics.'},
    {'label':'DTIC — ARL-TR-3005, Force on an Asymmetric Capacitor','url':'https://apps.dtic.mil/sti/tr/pdf/ADA416740.pdf','publisher':'U.S. Army Research Laboratory / DTIC','access':'Public official PDF','scope':'official-technical-test','note':'Confirms force in air and identifies vacuum testing as unresolved; does not establish electrogravity.'},
    {'label':'DTIC — AL-TR-89-040, Electric Propulsion Study','url':'https://apps.dtic.mil/sti/pdfs/ADA227121.pdf','publisher':'Air Force Astronautics Laboratory / DTIC','access':'Public official PDF','scope':'advanced-concepts-review','note':'Documents official awareness/review, not validation or adoption.'},
]: add_public(brown, source)
boundary = brown.setdefault('evidenceBoundary', {'established':[], 'notEstablished':[], 'competingExplanations':[]})
for fact in [
    'NARA NAID 28989015 authenticates Brown/Whitehall-Rand correspondence and reported testing in the Hartford/Woodbridge material investigation.',
    'ARL-TR-3005 documents force on asymmetric capacitors in air while explicitly leaving vacuum performance unresolved.',
]: append_unique(boundary['established'], fact)
for fact in [
    'Independent replication of Brown’s claimed changing mass, induced weight change or gravity-neutralization mechanism.',
    'That the Hartford or Woodbridge samples were non-human technology or evidence of an electrogravitic craft.',
]: append_unique(boundary['notEstablished'], fact)

# KONA BLUE / Lockheed–Bigelow enrichment.
kona = by_id['BF-SF-09']
kona['title'] = 'Special File: AAWSAP / AATIP, KONA BLUE & Skinwalker'
kona['date'] = '2007–2025'
kona['summary'] = "DIA’s AAWSAP contracted Bigelow Aerospace Advanced Space Studies and produced technical reports before ending in 2012. AARO’s KONA BLUE history documents a proposed DHS successor special-access program that was never approved, funded or supplied with material. George Knapp later testified that Bigelow and an AAWSAP colleague negotiated with Lockheed Martin for unusual material held in California, but said the agreement was not completed. The released record supports the proposed pathway and testimony—not an authenticated transfer or recovered craft."
kona['keyFact'] = 'Program existence, contractor lineage and the failed KONA BLUE proposal are official record; the alleged Lockheed-to-BAASS material deal is named congressional testimony without a released agreement or completed custody chain.'
kona['official'] = 'AARO states KONA BLUE was never approved or formally established and received no funding, data or material. That institutional finding does not resolve what Lockheed may have held or discussed outside KONA BLUE, but no public transfer record has been authenticated.'
kona['gap'] = 'Still absent are a named Lockheed executive statement, meeting memorandum, contract modification, material inventory, transfer authorization, sample custody record, or independent physical analysis connecting Lockheed to BAASS/KONA BLUE.'
kona['whyItMatters'] = 'This is the strongest documented bridge between the AAWSAP institutional lineage and the modern material-transfer allegation, while also showing exactly where testimony ends and custody evidence would need to begin.'
kona['evidenceModes'] = sorted(set(kona.get('evidenceModes', [])) | {'contract-record','official-retrospective','congressional-testimony'})
add_source_record(kona, {
    'citation': 'National Archives, AARO Historical Record Report Volume 1, NAID 499915937',
    'sourceType': 'official-report-in-federal-archival-custody',
    'provenance': 'NARA Record Group 615; archival copy of AARO’s March 2024 historical report',
    'locator': 'NAID 499915937; KONA BLUE / legacy-program discussion',
    'url': 'https://catalog.archives.gov/id/499915937',
    'supports': ['Establishes NARA custody for AARO’s official historical report and its KONA BLUE/legacy-program discussion'],
    'limitations': ['Archival custody authenticates the report as an official record; it does not independently validate AARO’s conclusions or the underlying interview claims'],
})
add_source_record(kona, {
    'citation': 'George Knapp, written testimony, House Task Force on the Declassification of Federal Secrets, 9 September 2025',
    'sourceType': 'named-congressional-witness-statement',
    'provenance': 'Official House Oversight witness PDF and public hearing record',
    'locator': 'Written testimony, Lockheed/Bigelow material-negotiation passage; hearing video approximately 31:00–32:10',
    'url': 'https://oversight.house.gov/wp-content/uploads/2025/09/George-Knapp-Written-Testimony.pdf',
    'supports': [
        'Knapp testified that Bigelow and a colleague negotiated with a senior Lockheed executive for unusual material held at a California facility',
        'Knapp attributed confirmation to an unnamed source who was in the room',
        'Knapp stated the agreement was not completed',
    ],
    'limitations': [
        'Knapp is reporting a source account and does not provide the source’s identity, meeting record or transfer paperwork',
        'No released record proves the material was a craft, non-human technology, sold, transferred or independently tested',
        'AARO states no data or material reached DHS under KONA BLUE',
    ],
})
for source in [
    {'label':'NARA Catalog — AARO Historical Record Report Volume 1 (NAID 499915937)','url':'https://catalog.archives.gov/id/499915937','publisher':'National Archives and Records Administration','access':'Public catalog / digital record','scope':'official-report-archival-custody','note':'Authenticates federal archival custody of AARO’s report; not independent corroboration of its conclusions.'},
    {'label':'George Knapp — written testimony, 2025 House UAP hearing','url':'https://oversight.house.gov/wp-content/uploads/2025/09/George-Knapp-Written-Testimony.pdf','publisher':'U.S. House Committee on Oversight and Accountability','access':'Public official PDF','scope':'named-congressional-testimony','note':'Knapp reports an attempted Lockheed-to-BAASS material agreement and says it was not completed. Testimony is not a transfer document.'},
    {'label':'House Oversight — Restoring Public Trust Through UAP Transparency and Whistleblower Protection','url':'https://oversight.house.gov/hearing/restoring-public-trust-through-uap-transparency-and-whistleblower-protection/','publisher':'U.S. House Committee on Oversight and Accountability','access':'Public hearing page and video','scope':'official-hearing-record','note':'Official hearing container for Knapp and Borland testimony.'},
]: add_public(kona, source)
kona['evidenceBoundary'] = {
    'established': [
        'AAWSAP was a funded DIA program and BAASS was its contractor.',
        'KONA BLUE was proposed as a DHS special-access successor but was never approved, funded or formally established.',
        'AARO states no data or material was transferred to or collected by DHS under KONA BLUE.',
        'George Knapp gave named congressional testimony alleging Lockheed/Bigelow negotiations and stated that the agreement was not completed.',
    ],
    'notEstablished': [
        'That Lockheed held a recovered non-human craft or material.',
        'The alleged Lockheed-to-Bigelow/BAASS sale or transfer was not completed.',
        'A released agreement, material inventory, custody receipt, Lockheed confirmation or independent sample analysis.',
        'That KONA BLUE ever possessed material, operated as an approved SAP or became an active recovery program.',
    ],
    'competingExplanations': [
        'Participants may have discussed material believed to be anomalous without authenticating its origin.',
        'A proposed transfer pathway can be historically real even if the underlying material claim was mistaken or never consummated.',
        'AARO’s later institutional review and participant testimony preserve conflicting interpretations without releasing the decisive custody records.',
    ],
}

# Borland / ICIG / BAE / Rubik’s Cube enrichment.
inst = by_id['BF-SF-10']
inst['date'] = '2021–2026'
inst['title'] = 'Special File: Grusch, Borland & the ODNI–AARO Record'
inst['summary'] = "The modern institutional arc now includes ODNI’s 2021 assessment, Grusch’s 2023 sworn recovery-program allegations, AARO’s 2024 written denial, Dylan Borland’s 2025 sworn statement, and his August 2026 long-form interview. Borland describes firsthand UAP observation, BAE Systems employment and an August 2023 ICIG intake; in the interview he says ICIG personnel ‘extremely hinted’ humans were not in charge, while withholding their exact words and identities. His open-hearing refusal to answer a BAE reverse-engineering question without a SCIF is not confirmation. No authenticated ICIG record establishes NHI control, and ‘Project Rubik’s Cube’ remains a relayed but unauthenticated program-name allegation."
inst['official'] = 'The official record authenticates testimony, complaint/intake channels and agency responses. It does not authenticate the alleged programs, BAE involvement, Project Rubik’s Cube, or an ICIG conclusion that NHI control disclosure or government.'
inst['gap'] = 'The underlying ICIG complaint/intake records, program names, documentary exhibits, BAE answer in an authorized classified setting, and authenticated Rubik’s Cube record remain non-public.'
inst['whyItMatters'] = 'It separates four often-conflated layers: what witnesses allege, what they told oversight channels, what agencies publicly conclude, and what the underlying classified records independently establish.'
for path in [
    'assets/evidence/BORLAND-2025/BORLAND-2025-House-Written-Testimony-page-001.png',
    'assets/evidence/BORLAND-2025/BORLAND-2025-House-Written-Testimony.pdf',
]: append_unique(inst.setdefault('images', []), path)
add_source_record(inst, {
    'citation': 'Dylan Borland, written testimony, House Task Force on the Declassification of Federal Secrets, 9 September 2025',
    'sourceType': 'sworn-congressional-witness-statement',
    'provenance': 'Official House Oversight witness PDF; exact Atlas holding and first-page derivative',
    'locator': 'Written testimony pp. 1–6; employment and August 2023 ICIG-intake passages',
    'sourceFilePath': 'assets/evidence/BORLAND-2025/BORLAND-2025-House-Written-Testimony.pdf',
    'sourceUrl': 'https://oversight.house.gov/wp-content/uploads/2025/09/Borland-Written-Testimony.pdf',
    'supports': [
        'Borland states he worked for BAE Systems and Intrepid Solutions as a senior analyst',
        'Borland states he completed an under-oath, video-recorded ICIG intake interview in August 2023',
        'Authenticates Borland’s allegations and oversight-channel account as sworn public testimony',
    ],
    'limitations': [
        'A witness statement authenticates what Borland told Congress, not the alleged program or NHI claims',
        'ICIG receipt, intake or investigation is not an ICIG factual finding or endorsement',
        'The written statement does not authenticate Project Rubik’s Cube or establish that BAE reverse-engineered NHI technology',
    ],
})
add_source_record(inst, {
    'citation': 'House Oversight hearing, “Restoring Public Trust Through UAP Transparency and Whistleblower Protection,” 9 September 2025',
    'sourceType': 'official-congressional-hearing-record',
    'provenance': 'Official House hearing page/video; accessibility transcript separately hosted by Rev',
    'locator': 'Borland/BAE exchange approximately 01:30:29–01:31:00 in the hearing video',
    'url': 'https://oversight.house.gov/hearing/restoring-public-trust-through-uap-transparency-and-whistleblower-protection/',
    'supports': ['Rep. Eric Burlison asked whether BAE Systems was involved in reverse engineering NHI craft; Borland said the answer required a SCIF/legal-authority discussion'],
    'limitations': ['Borland’s SCIF response is a non-answer in open session and cannot be treated as confirmation of BAE involvement'],
})
add_source_record(inst, {
    'citation': 'Dylan Borland, American Alchemy long-form interview, 5 August 2026',
    'sourceType': 'first-person-long-form-interview',
    'provenance': 'Original American Alchemy podcast feed and episode audio; locally generated large-v3-turbo timestamp transcript used for discovery',
    'locator': 'Rubik’s Cube exchange approximately 00:05:43–00:06:46; BAE/program discussion approximately 00:57:12–01:01:10; ICIG/NHI-control discussion approximately 02:30:46–02:34:10',
    'url': 'https://podcasts.apple.com/us/podcast/president-trump-was-briefed-on-ufos-government/id1539482596?i=1000721022643',
    'supports': [
        'Borland says an ICIG interaction “extremely hinted” that humans were not in charge',
        'Borland describes a hypothetical question sequence in which an interviewer asks “who do you think is running the show?”',
        'The Rubik’s Cube exchange preserves the allegation chain as an alleged ODNI source relayed through Jeremy Corbell and George Knapp; Borland says he cannot confirm or deny it',
        'Borland reiterates BAE Systems employment, claims work involving special-access programs, and says colleagues thought he was read into a specific program',
    ],
    'limitations': [
        'Borland withholds the ICIG interviewers’ exact words and identities and characterizes the conclusion as an inference from their questions',
        'His account is a first-person allegation, not an authenticated ICIG transcript, finding or institutional position',
        'The Rubik’s Cube name remains hearsay in this interview and is not independently authenticated',
        'Borland states he has not been through DOPSR for these interview claims; public airing does not equal government validation',
        'Machine-generated timestamps and wording were derived from the original audio and remain approximate locators rather than an official transcript',
    ],
})
inst['openLeads'] = [lead for lead in inst.get('openLeads', []) if lead.get('name') != "Project Rubik's Cube"]
inst['openLeads'].append({
    'name': "Project Rubik's Cube",
    'status': 'unsubstantiated-public-lead',
    'origin': 'Jeremy Corbell question to Dylan Borland during the Oregon UFO Fest / McMenamins panel, May 2026',
    'primaryMediaUrl': 'https://www.youtube.com/watch?v=MXhZrskutYA',
    'currentAssessment': 'In the August 2026 American Alchemy interview, Michels attributes the name to an alleged ODNI source relayed through Corbell and Knapp. Borland answers that he cannot confirm or deny it. No released ICIG, ODNI, AARO or program record using the name has been authenticated.',
    'promotionThreshold': 'A released government record, named sworn corroboration, exact authorized testimony, or independently authenticated program artifact.',
})
for source in [
    {'label':'Dylan Borland — written testimony, 2025 House UAP hearing','url':'https://oversight.house.gov/wp-content/uploads/2025/09/Borland-Written-Testimony.pdf','publisher':'U.S. House Committee on Oversight and Accountability','access':'Public official PDF','scope':'sworn-witness-statement','note':'Confirms the content of Borland’s public sworn account, including BAE employment and ICIG intake; not proof of the alleged programs.'},
    {'label':'Oregon UFO Fest panel — Corbell asks Borland about “Project Rubik’s Cube”','url':'https://www.youtube.com/watch?v=MXhZrskutYA','publisher':'Public panel recording','access':'Public video','scope':'first-generation-public-media-lead','note':'The phrase is introduced in a question and Borland does not confirm it. No documentary authentication has been found.'},
    {'label':'American Alchemy — Dylan Borland long-form interview, 5 August 2026','url':'https://podcasts.apple.com/us/podcast/president-trump-was-briefed-on-ufos-government/id1539482596?i=1000721022643','publisher':'American Alchemy / original podcast feed','access':'Public episode audio','scope':'first-person-witness-interview','note':'Borland says ICIG interviewers “extremely hinted” humans were not in charge, but withholds their exact words and identities. He cannot confirm or deny the relayed Rubik’s Cube name.'},
]: add_public(inst, source)
inst['evidenceBoundary'] = {
    'established': [
        'Grusch and Borland submitted allegations through official congressional or inspector-general channels and later described them publicly under oath.',
        'Borland’s official written testimony states that he worked for BAE Systems and completed an under-oath ICIG intake interview in August 2023.',
        'Borland declined to answer the BAE reverse-engineering question in open session without a SCIF/legal-authority determination.',
        'In his August 2026 American Alchemy interview, Borland said ICIG personnel “extremely hinted” that humans were not in charge; this establishes his allegation and interpretation, not the ICIG’s words or conclusion.',
        'AARO publicly reports that it found no verifiable evidence of reverse-engineering programs or recovered extraterrestrial craft.',
    ],
    'notEstablished': [
        'That ICIG receipt, intake or investigation validated any recovery-program or NHI allegation.',
        'Any authenticated ICIG statement that NHI control the government, cover-up or “run the show.”',
        'The exact words, identities and institutional authority of the ICIG personnel Borland says hinted at that interpretation.',
        'That BAE Systems participated in reverse engineering non-human craft.',
        'That “Project Rubik’s Cube” is an authenticated government program name.',
    ],
    'competingExplanations': [
        'Classified restrictions can explain a SCIF response without proving the premise of the question.',
        'Oversight intake can evaluate credibility, retaliation or jurisdiction without making a factual finding on underlying NHI claims.',
        'Program-name allegations can gain apparent weight through repetition after a public non-answer.',
    ],
}

# Timeline entry for the new event.
entry = {
    'id': 'TL-1960-HF',
    'year': 1960,
    'date': '4 SEP 1960',
    'type': 'incident',
    'caseId': 'BF-1960-HF-01',
    'title': 'Hartford green fall and material analysis',
    'desc': 'Witnesses reported a green descending light, impact and smoke; Blue Book called the material furnace slag while the underlying Air Force analysis retained a narrower aluminum-association question.',
}
if not any(item.get('id') == entry['id'] for item in atlas['timeline']):
    pos = next((i for i, item in enumerate(atlas['timeline']) if item.get('year', 9999) > 1960), len(atlas['timeline']))
    atlas['timeline'].insert(pos, entry)

save(ATLAS, atlas)

# Public manifest mirrors case-facing sources.
public = load(PUBLIC)
for cid in ['BF-SF-03','BF-SF-09','BF-SF-10','BF-1960-HF-01']:
    public[cid] = by_id[cid]['publicSources'] if cid in by_id else hartford['publicSources']
public['BF-1960-HF-01'] = hartford['publicSources']
save(PUBLIC, dict(sorted(public.items())))

# Source index links every public/custody asset without host-local paths.
index = load(INDEX)
hartford_paths = [
    f'assets/evidence/HARTFORD-1960/NARA-NAID-28989015-object-{oid}.jpg' for oid, _ in hartford_images
] + [
    'assets/evidence/HARTFORD-1960/HARTFORD-1960-NARA-NAID-28989015-download-manifest.json',
    'https://catalog.archives.gov/id/28989015',
]
index['HARTFORD-1960'] = hartford_paths
index['NARA NAID 28989015 · Hartford, Connecticut, September 1960'] = hartford_paths
for item in [
    'assets/evidence/HARTFORD-1960/NARA-NAID-28989015-object-0327.jpg',
    'assets/evidence/HARTFORD-1960/NARA-NAID-28989015-object-0331.jpg',
    'assets/evidence/HARTFORD-1960/NARA-NAID-28989015-object-0332.jpg',
    'https://catalog.archives.gov/id/28989015',
    'https://apps.dtic.mil/sti/tr/pdf/ADA416740.pdf',
    'https://apps.dtic.mil/sti/pdfs/ADA227121.pdf',
]: append_unique(index.setdefault('WINTERHAVEN-1952', []), item)
for item in [
    'https://catalog.archives.gov/id/499915937',
    'https://oversight.house.gov/wp-content/uploads/2025/09/George-Knapp-Written-Testimony.pdf',
    'https://oversight.house.gov/hearing/restoring-public-trust-through-uap-transparency-and-whistleblower-protection/',
]: append_unique(index.setdefault('AAWSAP-2008', []), item)
for item in [
    'assets/evidence/BORLAND-2025/BORLAND-2025-House-Written-Testimony.pdf',
    'assets/evidence/BORLAND-2025/BORLAND-2025-House-Written-Testimony-page-001.png',
    'https://oversight.house.gov/wp-content/uploads/2025/09/Borland-Written-Testimony.pdf',
    'https://www.youtube.com/watch?v=MXhZrskutYA',
    'https://podcasts.apple.com/us/podcast/president-trump-was-briefed-on-ufos-government/id1539482596?i=1000721022643',
]: append_unique(index.setdefault('GRUSCH-2023', []), item)
save(INDEX, dict(sorted(index.items())))

# Q2 analysis-only cultural/theological calibration.
blackfile = load(BLACKFILE)
blackfile['updated'] = '2026-08-06'
q2 = next(q for q in blackfile['questions'] if q['id'] == 'q2')
brief = {
    'id': 'ancient-watchers-catholic-nhi',
    'title': 'Ancient Watchers, Catholic NHI Theology & the Evidence Boundary',
    'classification': 'interpretive-analysis-only',
    'status': 'HISTORICAL TEXT / MODERN INTERPRETATION · NOT EVENT EVIDENCE',
    'summary': '1 Enoch preserves an ancient Watchers tradition involving heavenly beings, human contact, forbidden knowledge and giant offspring. Those motifs can be compared with modern NHI narratives, but the textual record does not prove UAP, visitation or non-human technology.',
    'findings': [
        'Israel Antiquities Authority identifies Aramaic 4Q Enoch fragments dated approximately 150–50 BCE and describes the Watchers’ descent and transmission of secret knowledge.',
        '1 Enoch is not part of the Catholic deuterocanon; the Catholic deuterocanonical list is a different, specific set of books.',
        'The Ethiopian Orthodox Tewahedo Church lists Enoch in its canon, so “noncanonical” must always be qualified by tradition.',
        'Paul Thigpen argues that Catholic theology can accommodate possible non-angelic NHI and should prepare intellectually and pastorally for potential confirmation.',
    ],
    'boundaries': [
        '“Apocrypha,” “pseudepigrapha,” and “deuterocanon” are not interchangeable categories.',
        'Thigpen explicitly says Catholic voices and theological possibility do not prove the existence of non-angelic nonhuman intelligence.',
        'Thigpen’s Sol Foundation white paper does not use 1 Enoch as evidence and frames empirical confirmation of NHI as a future contingency.',
        'Watchers-as-NHI is a modern hermeneutic comparison, not an authenticated ancient technical report or empirical event record.',
    ],
    'sources': [
        {'label':'Israel Antiquities Authority — 4Q Enoch / featured scrolls','url':'https://www.deadseascrolls.org.il/featured-scrolls','role':'manuscript-custody-and-description'},
        {'label':'Ethiopian Orthodox Tewahedo Church — Canonical Books','url':'https://www.ethiopianorthodox.org/english/canonical/books.html','role':'tradition-specific-canon'},
        {'label':'USCCB — Questions about the Bible','url':'https://www.usccb.org/faq','role':'Catholic-deuterocanon-boundary'},
        {'label':'Vatican Catechism — The Canon of Scripture','url':'https://www.vatican.va/content/catechism/en/part_one/section_one/chapter_two/article_3/iv_the_canon_of_scripture.html','role':'Catholic-canon-boundary'},
        {'label':'R. H. Charles, The Book of Enoch (1912)','url':'https://www.gutenberg.org/cache/epub/77935/pg77935-images.html','role':'public-domain-textual-translation'},
        {'label':'Paul Thigpen — NHI, UAP, and the Catholic Faith','url':'https://thesolfoundation.org/wp-content/uploads/2024/07/Sol_WhitePaper_Vol1N5.pdf','role':'modern-primary-theological-analysis'},
        {'label':'Paul Thigpen — Aliens and the Catholic Church','url':'https://www.catholic.com/magazine/online-edition/aliens-and-the-catholic-church','role':'author-explicit-proof-boundary'},
    ],
}
q2['supplementalAnalysis'] = [b for b in q2.get('supplementalAnalysis', []) if b.get('id') != brief['id']] + [brief]
save(BLACKFILE, blackfile)

print('Applied 2026-08 topic tranche: Hartford case + BF-SF-03/09/10 + Q2 analysis brief')
