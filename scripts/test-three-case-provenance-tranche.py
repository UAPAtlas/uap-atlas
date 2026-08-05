#!/usr/bin/env python3
"""Regression contract for the bounded 2026-08-05 three-case provenance tranche."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUTHORIZED_CASE_IDS = {"BF-1997-PH-01", "BF-1978-VL-01", "BF-1973-PG-01"}
AUTHORIZED_TIMELINE_IDS = {"EV-1997-PH-01", "TL-1978A", "TL-1973B"}

atlas = json.loads((ROOT / "atlas-data.json").read_text())
cases = {case["id"]: case for case in atlas["cases"]}
timeline = {event["id"]: event for event in atlas["timeline"]}
triage_path = ROOT / "qa/atlas_operational_triage.json"
triage = {row["id"]: row for row in json.loads(triage_path.read_text())["cases"]} if triage_path.exists() else {}

assert AUTHORIZED_CASE_IDS <= cases.keys()
assert AUTHORIZED_TIMELINE_IDS <= timeline.keys()

phoenix = cases["BF-1997-PH-01"]
assert phoenix["sourceLabel"] == "CNN firsthand commentary / contemporaneous press trail"
assert "no official case file" in phoenix["sourceQuality"].lower()
assert phoenix["confidenceModel"]["provenance"] == "firsthand-retrospective-and-secondary-press"
assert phoenix["temporal"]["eventForm"] == "multi-phase-event"
assert phoenix["geospatial"]["geometryIsObjectTrack"] is False
assert phoenix["geospatial"]["uncertaintyKm"] >= 150
assert phoenix["heroVisual"]["isEventEvidence"] is False
assert any("maryland air national guard" in record["citation"].lower() and "press" in record["sourceType"].lower() for record in phoenix["sourceRecords"])
assert "earlier moving" in phoenix["summary"].lower() and "later stationary" in phoenix["summary"].lower()
assert "moving-formation" in timeline["EV-1997-PH-01"]["desc"].lower()

valentich = cases["BF-1978-VL-01"]
assert "complete primary packet is not locally held" in valentich["sourceQuality"].lower()
assert "public mirror" in valentich["quoteSource"].lower()
assert valentich["confidenceModel"]["provenance"] == "official-locators-and-public-transcript-mirror"
assert valentich["observation"]["witnessRoles"] == ["pilot"]
assert len(valentich["sourceRecords"]) >= 3
assert any("catalog-locator" in record["sourceType"] for record in valentich["sourceRecords"])
assert any("transcript-mirror" in record["sourceType"] for record in valentich["sourceRecords"])
assert "does not establish" in timeline["TL-1978A"]["desc"].lower()

pascagoula = cases["BF-1973-PG-01"]
for stale in ("only abduction narrative tested", "supplies what every testimony case lacks"):
    assert stale not in json.dumps(pascagoula).lower()
assert pascagoula["sourceLabel"] == "Public sheriff-room recording trail; original custody not mapped"
assert pascagoula["observation"]["witnessRoles"] == ["civilian fishermen"]
assert "original audio" in pascagoula["quoteConfidence"].lower()
assert pascagoula["heroVisual"]["provenance"] == "Later publicity context; not a sheriff record"
assert "reported covert recording" in timeline["TL-1973B"]["desc"].lower()

for case_id in AUTHORIZED_CASE_IDS:
    assert cases[case_id].get("acquisitionTargets"), f"{case_id}: structured acquisition targets missing"
    if triage:
        assert triage[case_id]["category"] == "acquisition_target", triage[case_id]

canon_path = ROOT / "scripts/add-canon-cases.py"
if canon_path.exists():
    canon_generator = canon_path.read_text()
    assert '"BF-1978-VL-01"' in canon_generator.split("AUDITED_CANONICAL_ONLY_IDS", 1)[1].split("}", 1)[0]
honorable_path = ROOT / "scripts/add-honorable-mentions.py"
if honorable_path.exists():
    honorable_generator = honorable_path.read_text()
    assert "AUDITED_CANONICAL_ONLY_IDS" in honorable_generator
    assert '"BF-1973-PG-01"' in honorable_generator.split("AUDITED_CANONICAL_ONLY_IDS", 1)[1].split("}", 1)[0]

print(json.dumps({
    "status": "passed",
    "authorizedCaseIds": sorted(AUTHORIZED_CASE_IDS),
    "authorizedTimelineIds": sorted(AUTHORIZED_TIMELINE_IDS),
    "queueDisposition": {case_id: triage.get(case_id, {}).get("category") for case_id in sorted(AUTHORIZED_CASE_IDS)},
}, indent=2))
