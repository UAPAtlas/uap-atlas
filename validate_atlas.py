#!/usr/bin/env python3
from pathlib import Path
import json
import sys

ROOT = Path(__file__).parent
payload = json.loads((ROOT / "atlas-data.json").read_text())
cases = payload["cases"]
events = payload.get("timeline") or payload.get("timelineEvents") or []
valid_modes = {"exact", "approximate", "redacted", "orbital", "institutional"}
valid_expectations = {"admin1", "country", "offshore", "region", "orbital"}
valid_geometry_types = {"Point", "MultiPoint", "LineString", "MultiLineString", "Polygon", "MultiPolygon"}
geometry_pilot_ids = {"BF-1986-JAL-01", "BF-1957-RB-01", "BF-1978-VL-01", "BF-2004-NM-01", "BF-1997-PH-01", "BF-1989-BW-01"}
himalayan_parent_id = "BF-1968-HIM-01"
himalayan_child_ids = {f"BF-1968-HIM-{number:02d}" for number in range(2, 8)}
navy_parent_id = "BF-2015-NAV-01"
navy_child_ids = {"BF-2015-GIMBAL-01", "BF-2015-GOFAST-01"}
normalized_fields = {"caseTypes", "evidenceModes", "environment", "outcome", "confidenceModel", "temporal", "geospatial", "sourceRecords", "phenomena", "observation"}
errors = []
ids = {c.get("id") for c in cases}

if payload.get("schemaVersion") != 2:
    errors.append("atlas-data.json must declare schemaVersion 2")

if len(ids) != len(cases):
    errors.append("duplicate case ids")

case_by_id = {case.get("id"): case for case in cases}
if himalayan_parent_id not in case_by_id or not himalayan_child_ids.issubset(ids):
    errors.append("Himalayan series parent or child records missing")
else:
    parent = case_by_id[himalayan_parent_id]
    if parent.get("recordRole") != "series-parent" or parent.get("countInCaseTotals") is not False:
        errors.append("Himalayan parent must be a non-counted series parent")
    if set(parent.get("childCaseIds", [])) != himalayan_child_ids:
        errors.append("Himalayan parent childCaseIds mismatch")
    orders = set()
    for child_id in himalayan_child_ids:
        child = case_by_id[child_id]
        if child.get("recordRole") != "series-child" or child.get("seriesId") != himalayan_parent_id:
            errors.append(f"{child_id}: invalid Himalayan series linkage")
        if child.get("countInCaseTotals") is not True:
            errors.append(f"{child_id}: Himalayan child must count as an incident")
        orders.add(child.get("seriesOrder"))
        if not (child.get("temporal") or {}).get("timeAsReported"):
            errors.append(f"{child_id}: missing source-reported time field")
    if orders != set(range(1, 7)):
        errors.append("Himalayan child seriesOrder values must be 1 through 6")

if navy_parent_id not in case_by_id or not navy_child_ids.issubset(ids):
    errors.append("Navy video series parent or child records missing")
else:
    parent = case_by_id[navy_parent_id]
    if parent.get("recordRole") != "series-parent" or parent.get("countInCaseTotals") is not False:
        errors.append("Navy video parent must be a non-counted series parent")
    if set(parent.get("childCaseIds", [])) != navy_child_ids:
        errors.append("Navy video parent childCaseIds mismatch")
    orders = set()
    for child_id in navy_child_ids:
        child = case_by_id[child_id]
        if child.get("recordRole") != "series-child" or child.get("seriesId") != navy_parent_id:
            errors.append(f"{child_id}: invalid Navy series linkage")
        if child.get("countInCaseTotals") is not True:
            errors.append(f"{child_id}: Navy child must count as an incident")
        orders.add(child.get("seriesOrder"))
    if orders != {1, 2}:
        errors.append("Navy child seriesOrder values must be 1 and 2")


def valid_lon_lat_tree(value):
    if isinstance(value, list) and len(value) >= 2 and all(isinstance(n, (int, float)) for n in value[:2]):
        return -180 <= value[0] <= 180 and -90 <= value[1] <= 90
    return isinstance(value, list) and bool(value) and all(valid_lon_lat_tree(item) for item in value)


for c in cases:
    cid = c.get("id", "?")
    for field in ["id", "title", "date", "location", "mode", "agency", "domain", "status", "confidence", "summary", "official", "gap", "sources", "publicSources", "keyFact", "heroFact", "whyItMatters", "quoteConfidence", "significance", "sourceQuality", "sourceLabel", "relatedCaseIds"]:
        if not c.get(field):
            errors.append(f"{cid}: missing {field}")
    for source in c.get("publicSources", []):
        if not source.get("label") or not source.get("url", "").startswith(("http://", "https://")):
            errors.append(f"{cid}: invalid public source entry")
    missing_normalized = normalized_fields.difference(c)
    if missing_normalized:
        errors.append(f"{cid}: missing normalized fields {sorted(missing_normalized)}")
    for field in ["caseTypes", "evidenceModes", "environment", "sourceRecords"]:
        if not isinstance(c.get(field), list) or not c.get(field):
            errors.append(f"{cid}: {field} must be a non-empty list")
    for field in ["confidenceModel", "temporal", "geospatial", "phenomena", "observation"]:
        if not isinstance(c.get(field), dict):
            errors.append(f"{cid}: {field} must be an object")
    confidence_model = c.get("confidenceModel") or {}
    for axis in ["record", "anomaly", "provenance"]:
        if not confidence_model.get(axis):
            errors.append(f"{cid}: confidenceModel missing {axis}")
    geospatial = c.get("geospatial") or {}
    geometry = geospatial.get("geometry") or {}
    if c.get("mode") != "orbital" and not geometry:
        errors.append(f"{cid}: terrestrial case requires geospatial geometry")
    if geometry:
        if geometry.get("type") not in valid_geometry_types:
            errors.append(f"{cid}: invalid GeoJSON geometry type")
        if not valid_lon_lat_tree(geometry.get("coordinates")):
            errors.append(f"{cid}: invalid GeoJSON coordinates")
    if cid in geometry_pilot_ids:
        if geometry.get("type") == "Point":
            errors.append(f"{cid}: geometry pilot requires non-point geometry")
        for field in ["geometryLabel", "geometryBasis", "geometryConfidence"]:
            if not geospatial.get(field):
                errors.append(f"{cid}: geometry pilot missing {field}")
    if c.get("mode") != "orbital" and not geospatial.get("basis"):
        errors.append(f"{cid}: terrestrial case requires geospatial basis")
    if c.get("mode") not in valid_modes:
        errors.append(f"{cid}: invalid mode")

    if c.get("keyQuote") and not c.get("quoteSource"):
        errors.append(f"{cid}: keyQuote requires quoteSource")
    if c.get("keyQuote") and c.get("quoteConfidence") == "not-yet-selected":
        errors.append(f"{cid}: selected keyQuote must have real quoteConfidence")
    if c.get("sourceLocator") and not isinstance(c.get("sourceLocator"), str):
        errors.append(f"{cid}: sourceLocator must be a string")
    if not isinstance(c.get("relatedCaseIds"), list):
        errors.append(f"{cid}: relatedCaseIds must be a list")
    else:
        for rid in c.get("relatedCaseIds", []):
            if rid == cid:
                errors.append(f"{cid}: relatedCaseIds includes self")
            if rid not in ids:
                errors.append(f"{cid}: relatedCaseIds references unknown case {rid}")
    if c.get("relatedContext") and not isinstance(c.get("relatedContext"), list):
        errors.append(f"{cid}: relatedContext must be a list")

    expectation = c.get("geometryExpectation")
    if expectation and expectation not in valid_expectations:
        errors.append(f"{cid}: invalid geometryExpectation")

    if c.get("mode") == "orbital":
        if expectation and expectation != "orbital":
            errors.append(f"{cid}: orbital mode must use orbital geometryExpectation")
        continue

    if c.get("mode") == "redacted" and "REDACTED" not in c.get("location", ""):
        errors.append(f"{cid}: redacted mode must say REDACTED")

    if c.get("mode") == "exact" and not c.get("sources"):
        errors.append(f"{cid}: exact location lacks sources")

    if expectation in {"admin1", "country", "offshore", "region"}:
        if not isinstance(c.get("lon"), (int, float)) or not isinstance(c.get("lat"), (int, float)):
            errors.append(f"{cid}: non-orbital geometryExpectation requires lon/lat")
        if not c.get("coordinatePrecision"):
            errors.append(f"{cid}: missing coordinatePrecision")
        if not c.get("coordinateBasis"):
            errors.append(f"{cid}: missing coordinateBasis")

    if expectation == "admin1":
        if not c.get("expectedCountry") or not c.get("expectedAdmin1"):
            errors.append(f"{cid}: admin1 expectation requires expectedCountry and expectedAdmin1")
    if expectation == "country":
        if not c.get("expectedCountry"):
            errors.append(f"{cid}: country expectation requires expectedCountry")

event_ids = [event.get("id") for event in events]
if len(set(event_ids)) != len(event_ids):
    errors.append("duplicate timeline event ids")
himalayan_timeline_case_ids = [event.get("caseId") for event in events if event.get("seriesId") == himalayan_parent_id]
if set(himalayan_timeline_case_ids) != himalayan_child_ids or len(himalayan_timeline_case_ids) != 6:
    errors.append("Himalayan timeline must contain exactly one event per child")
if any(event.get("caseId") == himalayan_parent_id for event in events):
    errors.append("Himalayan aggregate parent must not have a timeline event")
navy_timeline_case_ids = [event.get("caseId") for event in events if event.get("seriesId") == navy_parent_id]
if set(navy_timeline_case_ids) != navy_child_ids or len(navy_timeline_case_ids) != 2:
    errors.append("Navy timeline must contain exactly one event per child")
if any(event.get("caseId") == navy_parent_id for event in events):
    errors.append("Navy aggregate parent must not have a timeline event")

for e in events:
    if e.get("caseId") not in ids:
        errors.append(f"{e.get('id', '?')}: unknown caseId")
    for field in ["id", "date", "type", "title", "desc"]:
        if not e.get(field):
            errors.append(f"{e.get('id', '?')}: missing {field}")

generated_path = ROOT / "assets" / "generated" / "atlas-data.generated.json"
if generated_path.exists():
    generated = json.loads(generated_path.read_text())
    if len(generated.get("cases", [])) != len(cases):
        errors.append("generated atlas data case count does not match canonical atlas-data.json")
    for c in generated.get("cases", []):
        cid = c.get("id", "?")
        if c.get("mode") == "orbital" or c.get("geometryExpectation") == "orbital":
            continue
        if not isinstance(c.get("x"), (int, float)) or not 0 <= c["x"] <= 100:
            errors.append(f"{cid}: generated invalid x")
        if not isinstance(c.get("y"), (int, float)) or not 0 <= c["y"] <= 62:
            errors.append(f"{cid}: generated invalid y")
        if cid in geometry_pilot_ids:
            mapped = c.get("mapGeometry") or {}
            if not mapped.get("d") or mapped.get("type") == "Point":
                errors.append(f"{cid}: generated map geometry missing")

if errors:
    print("ATLAS VALIDATION FAILED")
    print("\n".join(f"- {e}" for e in errors))
    sys.exit(1)

print(f"ATLAS VALID: {len(cases)} cases, {len(events)} timeline events, {len(valid_modes)} location modes")
