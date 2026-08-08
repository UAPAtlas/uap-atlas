#!/usr/bin/env python3
"""Apply the public-only PURSUE Release 05 evidence-closure sprint deterministically."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ATLAS = ROOT / "atlas-data.json"
PUBLIC = ROOT / "public-source-manifest.json"
INDEX = ROOT / "source-file-index.json"
LEDGER = ROOT / "research/pursue-release05-intake-ledger.json"
CROSSWALK = ROOT / "research/pursue-release05-video-crosswalk.json"
REPORT = ROOT / "research/pursue-release05-evidence-closure-sprint.md"
ADMISSION = ROOT / "research/pursue-release05-new-case-admission-review.md"
WAR = "https://www.war.gov/UFO/?releaseDate=Release+05&release=05"
DVIDS_SEARCH = "https://www.dvidshub.net/search?q=AARO080726"
NARA = "https://catalog.archives.gov/id/212794455"
BASE = "assets/sources/PURSUE-RELEASE-05"
GYATT_BASE = "assets/sources/NARA-GYATT-1964"
GOM_CONTACT = f"{BASE}/DOW-UAP-D101-PR117-PR122-video-contact.jpg"
D032_CONTACT = f"{BASE}/FBI-UAP-D032-PR007-video-contact.jpg"
D032_PAGES = [f"{BASE}/FBI-UAP-D032-pdf-page-001.png", f"{BASE}/FBI-UAP-D032-pdf-page-002.png"]
GYATT_PAGES = [
    f"{GYATT_BASE}/USS-GYATT-1964-11-19-page-A.jpg",
    f"{GYATT_BASE}/USS-GYATT-1964-11-19-page-B.jpg",
    f"{GYATT_BASE}/USS-GYATT-1964-11-24-page-A.jpg",
    f"{GYATT_BASE}/USS-GYATT-1964-11-24-page-B.jpg",
]


def load(path: Path):
    return json.loads(path.read_text())


def save(path: Path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def upsert(items, value, key):
    marker = value[key]
    for idx, item in enumerate(items):
        if item.get(key) == marker:
            items[idx] = value
            return
    items.append(value)


def append_unique(items, value):
    if value not in items:
        items.append(value)


VIDEO_MAP = {
    "DOD_111887376.mp4": ("DOW-UAP-PR125", 1017788, "Pacific Ocean, 2019", "pacific-2019", "corpus-only-officially-crosswalked"),
    "DOD_111887380.mp4": ("DOW-UAP-PR126", 1017790, "Pacific Ocean, 2019", "pacific-2019", "corpus-only-officially-crosswalked"),
    "DOD_111887384.mp4": ("DOW-UAP-PR127", 1017791, "Pacific Ocean, 2019", "pacific-2019", "corpus-only-officially-crosswalked"),
    "DOD_111887390.mp4": ("DOW-UAP-PR134", 1017792, "Middle East, 2025", "middle-east-2025", "corpus-only-officially-crosswalked"),
    "DOD_111887401.mp4": ("DOW-UAP-PR117", 1017793, "Gulf of Oman, 2021", "gulf-of-oman-d101", "mapped-supporting-media"),
    "DOD_111887407.mp4": ("DOW-UAP-PR118", 1017795, "Gulf of Oman, 2021", "gulf-of-oman-d101", "mapped-supporting-media"),
    "DOD_111887413.mp4": ("DOW-UAP-PR136", 1017796, "Middle East, 2023", "middle-east-2023", "corpus-only-officially-crosswalked"),
    "DOD_111887419.mp4": ("DOW-UAP-PR142", 1017797, "Middle East, 2025", "middle-east-2025", "corpus-only-officially-crosswalked"),
    "DOD_111887421.mp4": ("DOW-UAP-PR119", 1017798, "Gulf of Oman, 2021", "gulf-of-oman-d101", "mapped-supporting-media"),
    "DOD_111887426.mp4": ("DOW-UAP-PR149", 1017799, "Middle East, 2023", "middle-east-2023", "corpus-only-officially-crosswalked"),
    "DOD_111887427.mp4": ("DOW-UAP-PR120", 1017800, "Gulf of Oman, 2021", "gulf-of-oman-d101", "mapped-supporting-media"),
    "DOD_111887430.mp4": ("FBI-UAP-PR007", 1017801, "Slow-Moving Objects, 2026", "fbi-d032-2026", "mapped-event-media"),
    "DOD_111887439.mp4": ("DOW-UAP-PR121", 1017802, "Gulf of Oman, 2021", "gulf-of-oman-d101", "mapped-supporting-media"),
    "DOD_111887446.mp4": ("DOW-UAP-PR122", 1017803, "Gulf of Oman, 2021", "gulf-of-oman-d101", "mapped-supporting-media"),
    "DOD_111887456.mp4": ("DOW-UAP-PR123", 1017805, "Pacific Ocean, 2019", "pacific-2019", "corpus-only-officially-crosswalked"),
    "DOD_111887460.mp4": ("DOW-UAP-PR124", 1017806, "Pacific Ocean, 2019", "pacific-2019", "corpus-only-officially-crosswalked"),
}


def dvids_url(pr, video_id, title):
    suffix = title.lower().replace(", ", "-").replace(" ", "-")
    if pr.startswith("FBI-"):
        slug = pr.lower() + "-" + suffix
    else:
        slug = pr.lower() + "-unresolved-uap-report-" + suffix
    return f"https://www.dvidshub.net/video/{video_id}/{slug}"


atlas = load(ATLAS)
by_id = {case["id"]: case for case in atlas["cases"]}

# Gulf of Oman: replace the obsolete anonymous-video boundary with the official DVIDS crosswalk.
gom = by_id["BF-2021-GOM-01"]
gom["summary"] = (
    "A released Intelligence Information Report states that a USSOF AC-130 crew observed approximately 25 UAP instances through EO/IR during live-fire training in the Gulf of Oman on 8 September 2021. "
    "Two approximately four-foot cold objects were reported stationary just above the water near a flare before departing as the 105 mm cannon fired; later observations described pairs and trios maneuvering in formation. "
    "DVIDS now officially associates six public secondary recordings, PR117–PR122, with D101; the report remains not finally evaluated intelligence."
)
gom["keyFact"] = (
    "DVIDS resolves all six public Release 05 clips associated with D101 to PR117–PR122 and exact DOD filenames. They are secondary cellphone recordings of an AC-130J infrared display—not native sensor data—and the corrupted full DVR, telemetry and original PowerPoint package remain unavailable."
)
gom["gap"] = (
    "Missing are the native full-sortie DVR data, raw EO/IR metadata, aircraft telemetry/TACTOOL outputs, independent radar or ship correlation, the original PowerPoint attachment package, and a final analytical disposition. The public clips do not establish range, scale, speed, identity or response to gunfire."
)
gom["heroFact"] = (
    "The six Release 05 clips are now officially crosswalked to D101 as PR117–PR122, but DVIDS identifies them as secondary recordings of a sensor display rather than native sensor data."
)
gom["sourceQuality"] = (
    "Exact official IIR plus six officially associated DVIDS secondary videos with exact filenames; the report is not finally evaluated and native telemetry, full DVR data and independent correlation remain missing."
)
append_unique(gom["images"], GOM_CONTACT)
append_unique(gom["evidenceModes"], "released-video")
gom["sourceRecords"][0]["limitations"] = [
    "The IIR is explicitly not finally evaluated intelligence",
    "DVIDS identifies PR117–PR122 as secondary recordings of an AC-130J infrared display, not native primary sensor data",
    "The corrupted full DVR, raw metadata, telemetry and independent sensor correlation remain absent",
    "Release custody authenticates the report and public clips, not the object interpretation or reported performance",
]
upsert(gom["sourceRecords"], {
    "citation": "DVIDS official video records DOW-UAP-PR117 through DOW-UAP-PR122, associated with DOW-UAP-D101",
    "sourceType": "primary-official-public-video-crosswalk-set",
    "provenance": "Individual DVIDS records published by AARO/DoW on 7 August 2026 map PR117–PR122 to exact Release 05 DOD filenames",
    "locator": "DOW-UAP-PR117–PR122",
    "url": dvids_url("DOW-UAP-PR117", 1017793, "Gulf of Oman, 2021"),
    "relatedUrls": [dvids_url(VIDEO_MAP[f"DOD_111887{x}.mp4"][0], VIDEO_MAP[f"DOD_111887{x}.mp4"][1], "Gulf of Oman, 2021") for x in [401, 407, 421, 427, 439, 446]],
    "sourcePageImages": [GOM_CONTACT],
    "supports": [
        "Officially associates six public clips, PR117–PR122, with the Gulf of Oman D101 report",
        "Maps each PR record to an exact Release 05 DOD filename and public DVIDS video record",
        "States that the six clips were captured contemporaneously and are secondary recordings of an AC-130J infrared display",
    ],
    "limitations": [
        "The public MP4s are not native primary sensor data and screen-recording artifacts may be present",
        "DVIDS does not establish byte identity with the original six PowerPoint embeds or recover the corrupted full-sortie DVR",
        "The clips alone do not establish object identity, range, scale, speed, altitude or extraordinary performance",
    ],
}, "locator")
gom["publicSources"] = [
    {
        "label": "War.gov — PURSUE Release 05", "url": WAR, "publisher": "U.S. Department of War",
        "access": "Public official release landing page", "scope": "official-release-custody",
        "note": "Official custody page for DOW-UAP-D101 and the 16 Release 05 MP4s."
    },
    {
        "label": "DVIDS — DOW-UAP-PR117 through PR122", "url": dvids_url("DOW-UAP-PR117", 1017793, "Gulf of Oman, 2021"),
        "publisher": "Defense Visual Information Distribution Service / AARO", "access": "Public official video records",
        "scope": "official-video-crosswalk", "note": "Six individual DVIDS records map the public filenames to D101 and classify them as secondary recordings of an AC-130J infrared display, not native sensor data."
    },
]
gom["evidenceBoundary"]["established"] = [
    "An official IIR records direct-source AC-130 EO/IR observations during a dated Gulf of Oman sortie.",
    "The report lists GPS-derived coordinates, source-derived speed estimates and six embedded videos as an attachment.",
    "DVIDS officially associates PR117–PR122 and six exact DOD filenames with D101 and states that the clips were captured contemporaneously.",
]
gom["evidenceBoundary"]["notEstablished"] = [
    "The identity or origin of the reported objects.",
    "Independent verification of the source-calculated speeds, dimensions or response to gunfire.",
    "That the public secondary recordings are native sensor data or byte-identical exports of the original PowerPoint embeds.",
]
gom["evidenceBoundary"]["competingExplanations"] = [
    "Sensor or range-estimation effects, thermal contrast near a flare/live-fire environment, seabirds, debris, munitions-related objects, aircraft or UAS, and parallax remain unresolved without native data and telemetry."
]

# Puerto Rico: add the complete digitized November 1964 deck log as context and a negative-record boundary.
pr = by_id["BF-1964-PR-01"]
pr["sourceQuality"] = (
    "Two exact official CIA/Navy records plus the complete digitized USS Gyatt November 1964 deck log. The log confirms operating context on 19 and 24 November but contains no anomalous-contact entry; the referenced radar film, prints, message traffic and final analysis remain missing."
)
for image in GYATT_PAGES:
    append_unique(pr["images"], image)
upsert(pr["sourceRecords"], {
    "citation": "USS Gyatt (DD-712) deck log, November 1964, NARA catalog ID 212794455, Record Group 24",
    "sourceType": "primary-official-ship-deck-log",
    "provenance": "Complete unrestricted November 1964 deck log digitized by NARA; target-day page images use NARA digital-object IDs 212794531–212794532 and 212794551–212794552",
    "locator": "NARA 212794455 · 19 and 24 November 1964",
    "url": NARA,
    "sourcePageImages": GYATT_PAGES,
    "supports": [
        "Confirms USS Gyatt was steaming off the northwest coast of Puerto Rico on 19 November 1964",
        "Records ASW exercises, Hedgehog calibration and routine project operations on 19 November",
        "Records departure from San Juan toward Culebra on 24 November",
    ],
    "limitations": [
        "The target-day deck-log sheets contain no entry describing the reported unidentified target, F-8C intercept, radar track or radar-scope photography",
        "Silence in the permanent deck log does not refute a separate tactical, intelligence or classified reporting chain",
        "The log does not recover the radar film, prints, pilot statement, weapons-range data or final OSI/OEL analysis",
    ],
}, "locator")
upsert(pr["publicSources"], {
    "label": "NARA — USS Gyatt November 1964 deck log", "url": NARA, "publisher": "U.S. National Archives",
    "access": "Complete unrestricted digitized deck log", "scope": "official-operational-context",
    "note": "Confirms ship location and routine operations on the strongest incident dates; no anomalous-contact entry appears in the target-day sheets."
}, "label")
append_unique(pr["evidenceBoundary"]["established"], "The NARA deck log confirms Gyatt's operating context off Puerto Rico on 19 November and movement from San Juan toward Culebra on 24 November.")
append_unique(pr["evidenceBoundary"]["notEstablished"], "The target-day deck-log sheets do not preserve the reported radar anomaly; their silence neither authenticates nor disproves the separate intelligence account.")

# D032 now has an exact official video association and qualifies as a standalone case. D033 remains separate and deferred.
d032 = {
    "id": "BF-2026-SMO-01",
    "title": "Slow-Moving Thermal Objects",
    "date": "[REDACTED] 2026",
    "year": 2026,
    "location": "Western United States [REDACTED]",
    "mode": "redacted",
    "lon": -111.0,
    "lat": 39.5,
    "expectedCountry": "United States of America",
    "geometryExpectation": "country",
    "coordinatePrecision": "regional-redacted-generalized",
    "coordinateBasis": "Map-only generalized western-U.S. point; exact location and date are redacted in the released FBI record",
    "agency": "FBI",
    "domain": "GOVERNMENT / SENSOR",
    "status": "DOCUMENTED · UNRESOLVED",
    "confidence": "CONFIRMED RECORD · RELEASED EVENT FOOTAGE",
    "summary": (
        "A 2026 FBI FD-302 records that a government special agent responded to an RF alert by using a hand-held thermal optical device and observing two black-hot objects moving together slowly above a mountain line for approximately 5–10 minutes. "
        "DVIDS officially maps the 10-second Release 05 clip DOD_111887430 to FBI-UAP-PR007 and states that it was captured by the agent during the event. The released clip shows two small black-hot contrast areas but cannot establish identity, range, altitude, size or speed."
    ),
    "keyFact": "Release 05 originally exposed the interview without a filename mapping; the DVIDS record now identifies DOD_111887430 as FBI-UAP-PR007, a 10-second excerpt captured through the hand-held thermal device during the D032 event.",
    "official": "The FD-302 documents what the interviewed agent reported and explicitly contains no FBI recommendation or conclusion. DVIDS authenticates the public clip's association with the report, not the identity or anomalous nature of the imaged contrast areas.",
    "gap": "Exact date/location, RF system and bearing context, raw thermal metadata, range/altitude/scale, the complete reported photo/video set, other sensor records, independent witnesses and a final analytical disposition remain unavailable. D033 is not merged because its event linkage is not established.",
    "whyItMatters": "A rare modern case with an official interview record, RF-alert chronology, thermal-optical observation and a publicly released event clip that can be inspected while its severe measurement limitations remain explicit.",
    "sources": [
        "FBI-UAP-D032 · FD-302 slow-moving objects record",
        "FBI-UAP-PR007 · officially associated 10-second thermal-optics video",
    ],
    "sourceLabel": "FBI FD-302 / DVIDS event footage",
    "sourceLocator": "FBI-UAP-D032",
    "relatedCaseIds": ["BF-2026-RL-01"],
    "keyQuote": "The objects were moving together at the same speed. Both were black hot.",
    "quoteSource": "FBI-UAP-D032, FD-302, PDF p. 1",
    "quoteConfidence": "High — exact witness-account language in the released FD-302; the record does not establish measured speed, altitude or identity.",
    "heroFact": "The official 10-second clip preserves two black-hot contrast areas, but it has no public ranging, scale, telemetry or raw sensor metadata.",
    "significance": "Moderate significance",
    "sourceQuality": "Exact official FD-302 plus an officially associated released event clip; severe redaction, a short public excerpt and absent measurement/raw-data layers prevent performance or identity claims.",
    "image": D032_CONTACT,
    "images": [D032_CONTACT] + D032_PAGES,
    "caseTypes": ["military-encounter"],
    "evidenceModes": ["testimony", "thermal-optical-observation", "released-video"],
    "environment": ["terrestrial", "military-airspace"],
    "outcome": "unresolved",
    "confidenceModel": {"record": "confirmed", "anomaly": "undetermined", "provenance": "primary-source"},
    "temporal": {"dateLabel": "[REDACTED] 2026", "year": 2026, "startDateTime": None, "endDateTime": None, "timezone": None, "durationSeconds": None, "precision": "year-redacted", "eventForm": "single-event"},
    "geospatial": {"geometry": {"type": "Point", "coordinates": [-111.0, 39.5]}, "role": "representative-centroid", "precision": "regional-redacted-generalized", "uncertaintyKm": 1500, "basis": "Map-only generalized western-U.S. point; exact location and date are redacted in the released FBI record"},
    "sourceRecords": [
        {
            "citation": "FBI FD-302 interview concerning slow-moving black-hot objects observed after an RF alert, FBI-UAP-D032",
            "sourceType": "primary-official-witness-interview-record",
            "provenance": "Exact PDF published by the U.S. Department of War in PURSUE Release 05; full local copy hash-verified against the original download",
            "locator": "FBI-UAP-D032 · PDF pp. 1–2", "url": WAR,
            "sha256": "04684f8e8e0d9292e273b8e3152be6a22e195ce25f9c4a92b21c25b1813bd1e1",
            "sourcePageImages": D032_PAGES,
            "supports": [
                "Records an RF alert followed within minutes by a thermal-optical observation near the requested bearing",
                "Records two black-hot objects moving together slowly for approximately 5–10 minutes above a mountain line",
                "Records that photographs and videos were taken and provided to another FBI special agent",
            ],
            "limitations": [
                "Exact date, location, participants, RF system parameters and operational context are heavily redacted",
                "The observer could not estimate altitude or speed and reported no aviation expertise",
                "An FD-302 records interview content; it is not an FBI factual or analytical conclusion",
            ],
        },
        {
            "citation": "DVIDS official video record FBI-UAP-PR007, Slow-Moving Objects, 2026",
            "sourceType": "primary-official-released-event-video",
            "provenance": "DVIDS/AARO record maps FBI-UAP-PR007 to Release 05 filename DOD_111887430 and states that a government special agent captured the footage through a hand-held thermal optical device",
            "locator": "FBI-UAP-PR007 · DOD_111887430", "url": dvids_url("FBI-UAP-PR007", 1017801, "Slow Moving Objects, 2026"),
            "sha256": "56f0a2691dc2f2c9a23139b7aab119dc4f9f213db9c2f6d05f7cda727b904d54",
            "sourcePageImages": [D032_CONTACT],
            "supports": [
                "Officially associates the 10-second public MP4 with the D032 slow-moving-object report",
                "Shows two black-hot areas of contrast within the thermal field of view",
                "Confirms the public file is event footage rather than a witness reconstruction",
            ],
            "limitations": [
                "The 10-second public excerpt is shorter than the reported 5–10-minute observation",
                "No raw thermal metadata, range, scale, altitude, calibrated angular motion or platform geometry is public",
                "The clip does not identify the areas of contrast or establish unusual performance",
            ],
        },
    ],
    "phenomena": {"shapes": ["unresolved-contrast-area"], "objectCount": 2, "luminosity": "black-hot thermal contrast", "motion": ["slow", "together", "southeast-reported"], "effects": []},
    "observation": {"witnessCount": 1, "witnessRoles": ["government special agent"], "sensors": ["RF alert system (redacted)", "hand-held thermal optical device"], "durationSeconds": None, "independentWitnessGroups": 1},
    "taxonomyOriginal": {"domain": "GOVERNMENT / SENSOR", "status": "UNRESOLVED", "confidence": "CONFIRMED RECORD AND RELEASED FOOTAGE"},
    "taxonomyVersion": "atlas-controlled-v1",
    "heroVisual": {"src": D032_CONTACT, "mediaType": "image", "visualType": "official-event-video-contact-sheet", "caption": "Ten-frame contact sheet from FBI-UAP-PR007 / DOD_111887430, officially associated with D032.", "provenance": "Official DVIDS/AARO public video record; contact sheet generated from the hash-verified Release 05 MP4", "evidenceStatus": "Released event footage; identity, range, scale, altitude and speed are not established.", "isEventEvidence": True},
    "publicSources": [
        {"label": "War.gov — PURSUE Release 05", "url": WAR, "publisher": "U.S. Department of War", "access": "Public official release landing page", "scope": "official-release-custody", "note": "Official custody page for FBI-UAP-D032 and the Release 05 MP4 corpus."},
        {"label": "DVIDS — FBI-UAP-PR007", "url": dvids_url("FBI-UAP-PR007", 1017801, "Slow Moving Objects, 2026"), "publisher": "Defense Visual Information Distribution Service / AARO", "access": "Public official video record", "scope": "official-event-video-crosswalk", "note": "Maps DOD_111887430 to the D032 event and describes two black-hot areas of contrast; no analytical judgment is implied."},
    ],
    "evidenceBoundary": {
        "established": [
            "An official FD-302 records a special agent's thermal-optical observation of two black-hot objects after an RF alert.",
            "DVIDS officially maps a 10-second public clip, FBI-UAP-PR007 / DOD_111887430, to the event.",
            "The public clip contains two black-hot contrast areas and is event footage rather than a reconstruction.",
        ],
        "notEstablished": [
            "The identity, physical size, range, altitude, calibrated speed or origin of the contrast areas.",
            "That the RF alert was caused by the observed objects.",
            "That the public excerpt is the complete photo/video set described in D032.",
            "The contents of absent identifiers D034–D036 are unknown, and neither they nor D033 are established as documenting the same event.",
            "An FBI analytical conclusion validating anomalous performance.",
        ],
        "competingExplanations": ["Distant aircraft or UAS, birds, balloons, atmospheric or thermal-contrast effects, sensor artifacts and range/geometry misperception remain unresolved without raw data and context."],
    },
}
upsert(atlas["cases"], d032, "id")
upsert(atlas["timeline"], {"id": "TL-2026-SMO-THERMAL", "year": 2026, "date": "[REDACTED] 2026", "type": "incident", "caseId": d032["id"], "title": "Slow-moving thermal objects", "desc": "An FBI interview and officially associated 10-second thermal clip document two unresolved black-hot contrast areas after a redacted RF alert."}, "id")
save(ATLAS, atlas)

# Public source manifest and source index.
public = load(PUBLIC)
for case in [pr, gom, d032]:
    public[case["id"]] = case["publicSources"]
save(PUBLIC, public)

index = load(INDEX)
index.update({
    "DOW-UAP-PR117–PR122": [GOM_CONTACT, dvids_url("DOW-UAP-PR117", 1017793, "Gulf of Oman, 2021")],
    "FBI-UAP-D032": D032_PAGES + [WAR],
    "FBI-UAP-D032 · PDF pp. 1–2": D032_PAGES + [WAR],
    "FBI-UAP-PR007": [D032_CONTACT, dvids_url("FBI-UAP-PR007", 1017801, "Slow Moving Objects, 2026")],
    "FBI-UAP-PR007 · DOD_111887430": [D032_CONTACT, dvids_url("FBI-UAP-PR007", 1017801, "Slow Moving Objects, 2026")],
    "NARA 212794455": GYATT_PAGES + [NARA],
    "NARA 212794455 · 19 and 24 November 1964": GYATT_PAGES + [NARA],
})
save(INDEX, index)

# Correct the complete 16-video custody ledger and emit a structured official crosswalk.
ledger = load(LEDGER)
records_by_name = {r["filename"]: r for r in ledger["records"]}
crosswalk_records = []
for filename, (pr_id, video_id, title, group, disposition) in VIDEO_MAP.items():
    record = records_by_name[filename]
    url = dvids_url(pr_id, video_id, title)
    mapping = ["BF-2021-GOM-01"] if group == "gulf-of-oman-d101" else (["BF-2026-SMO-01"] if group == "fbi-d032-2026" else [])
    boundary = {
        "gulf-of-oman-d101": "Officially mapped to D101 through DVIDS PR117–PR122. Secondary screen recording, not native sensor data; identity and performance remain unresolved.",
        "fbi-d032-2026": "Officially mapped to D032 through DVIDS FBI-UAP-PR007. Released event footage, but range, scale, speed, identity and raw sensor metadata remain unavailable.",
        "pacific-2019": "Officially mapped to the contemporaneous Pacific 2019 PR123–PR127 set. Public metadata is too generalized for automatic merger with an existing Atlas case.",
        "middle-east-2023": "Officially mapped to a CENTCOM Middle East 2023 DVIDS record. Public date/location metadata is too generalized for automatic Atlas admission or merger.",
        "middle-east-2025": "Officially mapped to a CENTCOM Middle East 2025 DVIDS record. Public date/location metadata is too generalized for automatic Atlas admission or merger.",
    }[group]
    record.update({
        "atlasDisposition": disposition,
        "atlasMappings": mapping,
        "officialVideoRecord": {"id": pr_id, "videoId": video_id, "url": url, "title": title, "publisher": "DVIDS / AARO", "posted": "2026-08-07", "eventGroup": group},
        "boundary": boundary,
    })
    crosswalk_records.append({
        "filename": filename, "bytes": record["bytes"], "sha256": record["sha256"],
        "officialId": pr_id, "dvidsVideoId": video_id, "dvidsUrl": url, "title": title,
        "eventGroup": group, "atlasDisposition": disposition, "atlasMappings": mapping, "boundary": boundary,
    })
for record in ledger["records"]:
    if record["filename"].startswith("DOW-UAP-D101"):
        record.update({"atlasDisposition": "admitted-case-source", "atlasMappings": ["BF-2021-GOM-01"], "boundary": "Gulf of Oman IIR; six public secondary videos are now officially mapped through DVIDS PR117–PR122. The IIR remains not finally evaluated and native data remain unavailable."})
    elif record["filename"].startswith("CIA-UAP-D022") or record["filename"].startswith("CIA-UAP-D023"):
        record.update({"atlasDisposition": "admitted-case-source", "atlasMappings": ["BF-1964-PR-01"]})
    elif record["filename"].startswith("FBI-UAP-D032"):
        record.update({"atlasDisposition": "admitted-case-source", "atlasMappings": ["BF-2026-SMO-01"], "boundary": "Standalone D032 thermal-observation case supported by an official PR007 video mapping. Exact context, full media set and measurements remain unavailable; D033 is not merged."})
    elif record["filename"].startswith("FBI-UAP-D033"):
        record.update({"atlasDisposition": "corpus-only-deferred", "atlasMappings": [], "boundary": "Separate thermally elevated-object statement remains deferred. Its comparison footage and full context are absent; linkage to D032 is not established. D034–D036 are missing identifiers with unknown contents, not proven attachments."})
ledger["schemaVersion"] = 2
ledger["integrationSummary"] = {
    "existingAtlasCasesEnriched": ["BF-1946-GR-01", "BF-1950-GF-01", "BF-1952-TM-01", "BF-SF-07", "BF-1964-PR-01", "BF-2021-GOM-01"],
    "publishedRelease05NewCases": ["BF-1964-PR-01", "BF-2021-GOM-01", "BF-2026-RL-01"],
    "closureSprintNewCase": ["BF-2026-SMO-01"],
    "separateTestimonyCandidates": ["CANDIDATE-BF-2002-BAGRAM", "CANDIDATE-BF-2023-CS-TRANSLUCENT", "CANDIDATE-BF-2011-TRIANGLE", "CANDIDATE-BF-2023-CS-RED"],
    "deferredRecords": ["FBI-UAP-D024 airline-light sequence", "FBI-UAP-D033", "D034–D036 identifiers (contents unknown)"],
    "videoCrosswalk": {"mapped": 16, "gulfOfOmanD101": 6, "fbiD032": 1, "otherOfficiallyMappedCorpusRecords": 9, "source": DVIDS_SEARCH},
    "releaseVideoRule": "All 16 MP4s now have exact official DVIDS labels. Event-specific Atlas use still requires sufficient chronology, location and evidentiary context; mapping alone does not establish identity or anomalous performance.",
}
save(LEDGER, ledger)
save(CROSSWALK, {
    "schemaVersion": 1,
    "release": "PURSUE Release 05",
    "resolvedDate": "2026-08-08",
    "officialIndex": DVIDS_SEARCH,
    "method": "Exact DVIDS PR identifier, DVIDS video ID and Filename field matched to the hash-verified local Release 05 MP4 filename.",
    "counts": {"total": 16, "gulfOfOmanD101": 6, "fbiD032": 1, "otherOfficiallyMappedCorpusRecords": 9, "unmapped": 0},
    "boundary": "Official association authenticates the public record relationship. It does not establish object identity, extraordinary performance, native-sensor fidelity or byte identity with any original attachment package.",
    "records": sorted(crosswalk_records, key=lambda x: x["filename"]),
})

# Update the admission review without erasing the original reasoning history.
text = ADMISSION.read_text()
text = text.replace(
    "Release 05 supports **three high-priority new Atlas dossiers**, **four lower-confidence testimony dossiers**, and **one incomplete operational sequence that should remain deferred**.",
    "Release 05 supports **three published high-priority dossiers**, **one additional D032 thermal case admitted after the official DVIDS video crosswalk**, **four lower-confidence testimony dossiers**, and **a separate D033 statement that remains deferred**."
)
text = text.replace(
    "8. **2026 thermal/RF operational sequence** — `FBI-UAP-D032`, `FBI-UAP-D033`; D034–D036 and referenced native photographs/videos are absent",
    "8. **2026 D032 slow-moving thermal objects** — admit as a standalone case after DVIDS mapped `DOD_111887430` to `FBI-UAP-PR007`; keep D033 separate and deferred"
)
text = text.replace(
    "- `FBI-UAP-D032`, `FBI-UAP-D033` — defer incomplete thermal/RF sequence.",
    "- `FBI-UAP-D032` plus `FBI-UAP-PR007` / `DOD_111887430` — add one standalone slow-moving thermal-object dossier.\n- `FBI-UAP-D033` — defer separately; do not infer linkage to D032. D034–D036 are absent identifiers whose contents are unknown."
)
old_section = """### 8. 2026 thermal/RF operational sequence — DEFER

**Primary records:** `FBI-UAP-D032`, `D033`

- D032 records an RF alert followed minutes later by thermal-optical observation of two black-hot objects moving together for roughly 5–10 minutes. Photographs and video were reportedly taken and provided to an FBI agent.
- D033 preserves a special agent’s written statement describing a thermally elevated object in the same general observation sector on a subsequent night, with a Black Hawk video used as a comparison reference; the object appeared roughly half the helicopter’s size.

**Page locators:** D032 PDF pp. 1–2; D033 PDF pp. 1–2.

**Why defer:** Exact geography/date and the technical RF parameters are heavily redacted; referenced photographs/videos are absent; D034–D036 are absent from the local release and produced no exact-filename public hits; the relationship between D032 and D033 is not fully established.
"""
new_section = """### 8. 2026 D032 slow-moving thermal objects — ADD AFTER OFFICIAL VIDEO CROSSWALK

**Primary record:** `FBI-UAP-D032`
**Official event video:** `FBI-UAP-PR007` / `DOD_111887430`

- D032 records an RF alert followed minutes later by thermal-optical observation of two black-hot objects moving together slowly for roughly 5–10 minutes. Photographs and video were reportedly taken and provided to another FBI agent.
- DVIDS now maps the 10-second Release 05 clip `DOD_111887430` to `FBI-UAP-PR007`, states that it was captured by the observing government special agent, and describes two black-hot areas of contrast.
- The official mapping makes D032 independently admissible as a redacted sensor/witness case. It does not establish object identity, range, altitude, size, speed, anomalous performance or a causal relationship to the RF alert.

**Page locators:** D032 PDF pp. 1–2; DVIDS video ID 1017801.

**Separate deferment:** D033 remains a distinct thermally elevated-object statement. Its Black Hawk comparison footage and full context are absent, and it must not be merged with D032. D034–D036 are missing sequence identifiers with unknown contents; the public record does not prove that they are D032/D033 attachments.
"""
if old_section in text:
    text = text.replace(old_section, new_section)
elif new_section not in text:
    raise SystemExit("Admission-review D032 section matched neither baseline nor applied state")
text = text.replace(
    "The released 16 MP4 files cannot be assigned to D101 without a per-file crosswalk.",
    "DVIDS now assigns PR117–PR122 and six exact DOD filenames to D101. The clips are secondary recordings of an AC-130J infrared display, not native sensor data, and do not independently validate the reported performance."
)
text = text.replace(
    "4. Keep D032/D033 in acquisition/deferred status until the missing media or D034–D036 relationship is resolved.",
    "4. Admit D032 with PR007 as a standalone redacted thermal case; keep D033 deferred and treat D034–D036 only as absent identifiers with unknown contents."
)
ADMISSION.write_text(text)

REPORT.write_text("""# PURSUE Release 05 evidence-closure sprint

**Completed:** 2026-08-08
**Scope:** Public official sources only; no outreach, requests, purchases, accounts, forms, push, or deployment.

## Result

The sprint closed the two strongest media-attribution gaps and materially narrowed the third:

1. **D101 / Gulf of Oman:** DVIDS officially maps six Release 05 files to `DOW-UAP-PR117`–`PR122` and associates them with D101. All are secondary recordings of an AC-130J infrared display, not native sensor data. The corrupted DVR, raw metadata, telemetry and original PowerPoint package remain unavailable.
2. **D032:** DVIDS maps `DOD_111887430` to `FBI-UAP-PR007`, states that a government special agent captured it through a hand-held thermal optical device, and describes two black-hot areas of contrast. This supports one standalone D032 Atlas dossier with strict measurement and FBI-record boundaries.
3. **D033 / D034–D036:** No official public video or document record was recovered for D033. D034–D036 are absent sequence identifiers whose contents are unknown; they are not proven attachments to D032/D033. D033 remains deferred and unmerged.
4. **All 16 MP4s:** Every formerly anonymous Release 05 video now has an exact official DVIDS PR label and filename mapping. Nine remain corpus-only because their public date/location/chronology is too generalized for automatic Atlas merger or admission.
5. **USS Gyatt:** NARA catalog ID `212794455` provides the complete November 1964 deck log. It confirms Gyatt off northwest Puerto Rico on 19 November conducting ASW/Hedgehog calibration activity and departing San Juan toward Culebra on 24 November. The target-day sheets contain no anomalous-radar, F-8C, unidentified-target, film or unusual-contact entry. This is operational context and a negative-record boundary—not independent confirmation or disproof of the CIA/Navy radar account.

## Evidence boundaries

- DVIDS association authenticates the public record relationship, not object identity or anomalous performance.
- PR117–PR122 are screen recordings, not native AC-130J sensor files.
- PR007 is released event footage, but its 10 seconds cannot establish distance, size, altitude, calibrated speed or identity.
- An FD-302 records interview content and is not an FBI factual conclusion.
- Deck-log silence cannot disprove a separate tactical, intelligence or classified reporting chain.
- The original Gyatt radar film/prints, Navy message traffic, pilot statement and final OSI/OEL analysis remain unrecovered.

## Official locators

- DVIDS release index: https://www.dvidshub.net/search?q=AARO080726
- D101 PR117 entry: https://www.dvidshub.net/video/1017793/dow-uap-pr117-unresolved-uap-report-gulf-of-oman-2021
- D032 PR007 entry: https://www.dvidshub.net/video/1017801/fbi-uap-pr007-unresolved-uap-report-slow-moving-objects-2026
- NARA USS Gyatt November 1964 deck log: https://catalog.archives.gov/id/212794455
- Structured 16-video crosswalk: `research/pursue-release05-video-crosswalk.json`

## Atlas action

- Enrich `BF-2021-GOM-01` and `BF-1964-PR-01`.
- Add `BF-2026-SMO-01` as one standalone D032 case.
- Keep D033 and D034–D036 out of the Atlas pending evidence that establishes their contents and linkage.
- Keep the other nine mapped videos corpus-only pending sufficient event metadata.
""")

print("Applied Release 05 evidence-closure sprint: 16-video crosswalk, D101/Gyatt enrichment, BF-2026-SMO-01")
