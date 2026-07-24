#!/usr/bin/env python3
"""Add the Fort Monmouth, NJ (September 1951) case to the UAP Atlas."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ATLAS = ROOT / "atlas-data.json"
INDEX = ROOT / "source-file-index.json"
GENERATED = ROOT / "assets/generated/atlas-data.generated.json"
DESKTOP = ROOT / "atlas-fresh.html"


def uniq(values):
    return list(dict.fromkeys(v for v in values if v))


def sync_generated(canonical):
    if not GENERATED.exists():
        return canonical
    old = json.loads(GENERATED.read_text())
    old_cases = {c["id"]: c for c in old.get("cases", [])}
    merged_cases = []
    for current in canonical["cases"]:
        merged = dict(current)
        previous = old_cases.get(current["id"], {})
        for key in ("x", "y", "mapGeometry"):
            if key in previous:
                merged[key] = previous[key]
        if "x" not in merged:
            lon = merged.get("lon") or 0
            merged["x"] = round((lon + 180) / 360 * 100, 2)
        if "y" not in merged:
            lat = merged.get("lat") or 0
            merged["y"] = round((90 - lat) / 180 * 62, 2)
        merged_cases.append(merged)
    generated = dict(canonical)
    generated["cases"] = merged_cases
    GENERATED.write_text(json.dumps(generated, ensure_ascii=False, separators=(",", ":")) + "\n")
    return generated


def sync_embedded(html_path, payload):
    if not html_path.exists():
        return
    text = html_path.read_text()
    replacement = "const atlasData = " + json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + ";"
    updated, count = re.subn(r"const atlasData = \{.*?\};", replacement, text, count=1)
    if count != 1:
        raise RuntimeError(f"Could not replace embedded atlasData in {html_path}")
    html_path.write_text(updated)


CASE = {
    "id": "BF-1951-FM-01",
    "title": "Fort Monmouth Radar-Visual Incident",
    "date": "10–11 SEP 1951",
    "year": 1951,
    "location": "Fort Monmouth, New Jersey",
    "mode": "exact",
    "lon": -74.05,
    "lat": 40.32,
    "coordinateBasis": "Fort Monmouth Army Signal Corps Center, Monmouth County, NJ",
    "expectedCountry": "United States of America",
    "expectedAdmin1": "New Jersey",
    "geometryExpectation": "admin1",
    "coordinatePrecision": "site",
    "agency": "USAF / U.S. Army Signal Corps",
    "domain": "MILITARY / RADAR-VISUAL",
    "status": "RESOLVED (balloon / anomalous propagation)",
    "confidence": "CONFIRMED RECORD",
    "summary": (
        "Over two consecutive days in September 1951, radar operators at the Fort Monmouth Army Signal Corps training center tracked fast-moving targets that exceeded the tracking capability of their SCR-584 and AN/MPG-1 radar sets. "
        "On the first day, two Air National Guard T-33 pilots visually sighted a silver, discus-shaped object near Sandy Hook, NJ, moving at an estimated 900 mph that disappeared out to sea. "
        "On the second day, radar operators tracked a target that displayed hovering behavior and unusual maneuverability, with speeds judged to be several hundred mph beyond the 700 mph tracking limit of their sets. "
        "The case drew the attention of the Chief of Staff of the Air Force and prompted an immediate ATIC field investigation led by Lt. Col. Rosengarten."
    ),
    "official": (
        "The Project Blue Book record card marked the 10 September target as 'Was Balloon' and the 11 September targets as 'Probably Balloon,' attributing the radar behavior to anomalous propagation. "
        "However, the investigating Signal Corps report noted that the weather on 10 September 'was not favorable for anomalous propagation,' and the analysis conceded that 'it cannot be concluded that the object was definitely a balloon.'"
    ),
    "gap": (
        "Raw radar scope photographs or film are absent. No plotting records, logs, or data tapes were kept by the maintenance-course students who operated the sets. "
        "The names of the T-33 pilots are partially redacted in the file. The underlying weather-station data cited for the anomalous-propagation conclusion is not isolated in the case packet."
    ),
    "sources": [
        "FORT-MONMOUTH-1951 · Project Blue Book case file (NARA NAID 28939862, 87 digital objects)",
        "CSAF teletype message, 28 September 1951, scan 01004",
        "Headquarters Signal Corps Center report, 12 September 1951, scan 01002",
        "Air Intelligence Information Report, Lt. Col. Bruce K. Bauhgardner, scan 01015",
        "Pilot narrative statement, scan 01010",
    ],
    "image": "assets/evidence/FORT-MONMOUTH-1951/FORT-MONMOUTH-1951-NARA-NAID-28939862-p01004-csaf-teletype.jpg",
    "images": [
        "assets/evidence/FORT-MONMOUTH-1951/FORT-MONMOUTH-1951-NARA-NAID-28939862-p01004-csaf-teletype.jpg",
        "assets/evidence/FORT-MONMOUTH-1951/FORT-MONMOUTH-1951-NARA-NAID-28939862-p00978-record-card.jpg",
        "assets/evidence/FORT-MONMOUTH-1951/FORT-MONMOUTH-1951-NARA-NAID-28939862-p01002-signal-corps-report.jpg",
        "assets/evidence/FORT-MONMOUTH-1951/FORT-MONMOUTH-1951-NARA-NAID-28939862-p01010-pilot-narrative.jpg",
        "assets/evidence/FORT-MONMOUTH-1951/FORT-MONMOUTH-1951-NARA-NAID-28939862-p01015-intel-report.jpg",
    ],
    "heroVisual": {
        "src": "assets/evidence/FORT-MONMOUTH-1951/FORT-MONMOUTH-1951-NARA-NAID-28939862-p01004-csaf-teletype.jpg",
        "mediaType": "image",
        "visualType": "declassified-teletype",
        "caption": "CSAF-priority teletype message reporting the Fort Monmouth radar sightings and T-33 visual observation, directing an immediate field investigation.",
        "provenance": "NARA Record Group 341, Project Blue Book file, NAID 28939862",
        "evidenceStatus": "Primary-source document: contemporaneous USAF teletype routed to the Chief of Staff of the Air Force.",
        "isEventEvidence": True,
    },
    "publicSources": [
        {
            "access": "Public",
            "label": "NARA Catalog — Monmouth, New Jersey, September 1951 Project Blue Book file",
            "publisher": "National Archives and Records Administration",
            "scope": "official-complete-public-file-grouping",
            "url": "https://catalog.archives.gov/id/28939862",
            "note": "87 digital objects; contains Signal Corps report, CSAF teletype, pilot narrative, ATIC interrogation, and analysis.",
        },
        {
            "access": "Subscription",
            "label": "Fold3 — Monmouth, New Jersey, September 1951",
            "publisher": "Fold3",
            "scope": "T1206-microfilm-viewer",
            "url": "https://www.fold3.com/image/7010207",
            "note": "Compiled case-file PDF anchor; subscription may be required.",
        },
    ],
    "keyFact": "Radar targets at a premier Army Signal Corps facility exceeded the 700 mph tracking limit of SCR-584 sets and a T-33 pilot reported a silver discus-shaped object at an estimated 900 mph.",
    "whyItMatters": "The case occurred at a sensitive military radar research facility staffed by trained electronics personnel, lending unusual credibility to the radar observations. The CSAF-level urgency and ATIC field investigation response demonstrate that the Air Force took the event seriously at the highest level.",
    "keyQuote": "THESE OBJECTS VARIED IN SPEED FROM ZERO TO OVER 700 MILES PER HOUR AND WERE SIGHTED AT VARYING ALTITUDES",
    "quoteSource": "CSAF teletype message, 28 September 1951, NARA NAID 28939862, scan 01004",
    "quoteConfidence": "confirmed-primary-source-quotation",
    "heroFact": "At a premier Army radar research facility, multiple radar operators tracked targets exceeding 700 mph while a T-33 pilot reported a silver discus-shaped object at an estimated 900 mph.",
    "significance": "High significance",
    "sourceQuality": "Primary source",
    "sourceLabel": "NARA / Project Blue Book",
    "sourceLocator": "NARA NAID 28939862, scans 00978–01064; Fold3 T1206 image 7010207",
    "relatedCaseIds": ["BF-1952-DC-01", "BF-1951-YK-01"],
    "relatedContext": [
        "Precursor to the 1952 Washington D.C. radar flap in demonstrating military-radar-visual correlation cases.",
        "Occurred during the Project Grudge era, before Project Blue Book was formally reactivated under Ruppelt in 1952.",
    ],
    "caseTypes": ["military-encounter", "radar-visual"],
    "evidenceModes": ["radar", "visual", "documentary-record", "multi-witness"],
    "environment": ["military-airspace", "coastal"],
    "outcome": "resolved-balloon",
    "confidenceModel": {
        "record": "confirmed",
        "anomaly": "disputed",
        "provenance": "primary-source",
    },
    "temporal": {
        "dateLabel": "10–11 SEP 1951",
        "year": 1951,
        "startDateTime": "1951-09-10T11:10:00Z",
        "endDateTime": "1951-09-11T14:00:00Z",
        "timezone": "EDT",
        "durationSeconds": None,
        "precision": "day",
        "eventForm": "event-series",
    },
    "geospatial": {
        "geometry": {"type": "Point", "coordinates": [-74.05, 40.32]},
        "role": "event-location",
        "precision": "site",
        "uncertaintyKm": 5,
        "basis": "Fort Monmouth Army Signal Corps Center, Monmouth County, NJ",
    },
    "sourceRecords": [
        {
            "citation": "FORT-MONMOUTH-NARA-28939862 · Monmouth, New Jersey, September 1951",
            "sourceType": "official-project-blue-book-case-file",
            "provenance": "NARA Record Group 341, Project Blue Book public file, NAID 28939862",
            "locator": "87 digital objects; scans 00978–01064",
            "supports": [
                "radar-visual-correlation",
                "multiple-radar-sets-engaged",
                "T-33-pilot-visual-sighting",
                "CSAF-level-urgency",
                "ATIC-field-investigation",
            ],
            "limitations": [
                "raw-radar-scope-film-absent",
                "no-plotting-records-kept-by-maintenance-students",
                "pilot-names-partially-redacted",
                "weather-data-for-anomalous-propagation-not-isolated",
            ],
        },
        {
            "citation": "CSAF-TELETYPE-1951-09-28 · Chief of Staff USAF priority teletype",
            "sourceType": "contemporaneous-high-level-message",
            "provenance": "USAF teletype routed to Chief of Staff of the Air Force",
            "locator": "NARA NAID 28939862, scan 01004",
            "supports": ["speeds-zero-to-700-mph", "T-33-visual-sighting", "estimated-1000-mph", "immediate-investigation-directed"],
            "limitations": ["teletype-compresses-detail", "some-redactions-in-header"],
        },
        {
            "citation": "SIGNAL-CORPS-REPORT-1951-09-12 · HQ Signal Corps Center, Fort Monmouth",
            "sourceType": "contemporaneous-military-report",
            "provenance": "Headquarters, Signal Corps Center and Fort Monmouth",
            "locator": "NARA NAID 28939862, scan 01002",
            "supports": ["AN/MPG-1-radar-track", "SCR-584-tracking", "hovering-target", "unusually-strong-return", "weather-not-favorable-for-anomalous-propagation"],
            "limitations": ["operators-were-maintenance-students-not-operators", "no-logs-or-data-tapes-kept"],
        },
    ],
    "phenomena": {
        "shapes": ["discus", "circular", "flat-when-edge-on"],
        "objectCount": 1,
        "luminosity": "silver or metallic",
        "motion": ["rapid-crossing", "hovering", "extreme-speed-change", "disappeared-out-to-sea"],
        "effects": ["unusually-strong-radar-return"],
    },
    "observation": {
        "witnessCount": 4,
        "witnessRoles": ["two T-33 pilots (Air National Guard)", "radar operators (Signal Corps maintenance students)", "experienced radar operator (giving demonstration)"],
        "sensors": ["AN/MPG-1 radar", "SCR-584 radar (serial nos. 433, 217, 315)", "unaided-visual"],
        "durationSeconds": 120,
        "independentWitnessGroups": 2,
    },
}


def main():
    atlas = json.loads(ATLAS.read_text())
    index = json.loads(INDEX.read_text())

    existing = next((c for c in atlas["cases"] if c["id"] == CASE["id"]), None)
    if existing:
        atlas["cases"] = [c if c["id"] != CASE["id"] else CASE for c in atlas["cases"]]
    else:
        atlas["cases"].append(CASE)

    event = {
        "id": "TL-1951-FM",
        "year": 1951,
        "date": "10–11 SEP 1951",
        "type": "incident",
        "caseId": CASE["id"],
        "title": "Fort Monmouth radar-visual incident",
        "desc": "Signal Corps radar teams tracked fast-moving targets over two days; T-33 pilots reported a silver discus and ATIC opened a field investigation.",
    }
    atlas["timeline"] = [item for item in atlas.get("timeline", []) if item.get("id") != event["id"]]
    atlas["timeline"].append(event)
    atlas["timeline"].sort(key=lambda item: (item.get("year", 0), item.get("date", ""), item.get("id", "")))

    index["FORT-MONMOUTH-1951"] = [
        "assets/evidence/FORT-MONMOUTH-1951/FORT-MONMOUTH-1951-NARA-NAID-28939862-p00978-record-card.jpg",
        "assets/evidence/FORT-MONMOUTH-1951/FORT-MONMOUTH-1951-NARA-NAID-28939862-p01002-signal-corps-report.jpg",
        "assets/evidence/FORT-MONMOUTH-1951/FORT-MONMOUTH-1951-NARA-NAID-28939862-p01004-csaf-teletype.jpg",
        "assets/evidence/FORT-MONMOUTH-1951/FORT-MONMOUTH-1951-NARA-NAID-28939862-p01010-pilot-narrative.jpg",
        "assets/evidence/FORT-MONMOUTH-1951/FORT-MONMOUTH-1951-NARA-NAID-28939862-p01015-intel-report.jpg",
        "source-files/archives/FORT-MONMOUTH-1951-NARA-NAID-28939862/custody-manifest.json",
        "https://catalog.archives.gov/id/28939862",
        "https://www.fold3.com/image/7010207",
    ]

    ATLAS.write_text(json.dumps(atlas, indent=2, ensure_ascii=False) + "\n")
    INDEX.write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n")
    generated = sync_generated(atlas)
    sync_embedded(DESKTOP, generated)
    print(f"Added case {CASE['id']} to Atlas. Total cases: {len(atlas['cases'])}")


if __name__ == "__main__":
    main()
