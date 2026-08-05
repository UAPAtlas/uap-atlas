#!/usr/bin/env python3
"""Regression contract for the six-case held-primary credibility repair."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
atlas = json.loads((ROOT / "atlas-data.json").read_text())
index = json.loads((ROOT / "source-file-index.json").read_text())
triage = json.loads((ROOT / "qa" / "atlas_operational_triage.json").read_text())
weak_priorities = json.loads((ROOT / "qa" / "source-depth-weak-case-priorities.json").read_text())
cases = {case["id"]: case for case in atlas["cases"]}
triage_cases = {case["id"]: case for case in triage["cases"]}
weak_ids = {case["id"] for case in weak_priorities}

IDS = {
    "BF-1956-DF-01",
    "BF-1957-B47-01",
    "BF-1957-CG-01",
    "BF-1957-HT-01",
    "BF-1985-PNG-01",
    "BF-1994-KZ-01",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def text(case: dict) -> str:
    return json.dumps(case, ensure_ascii=False).lower()


require(IDS <= cases.keys(), "selective-primary case missing")

expected_index = {
    "AIIRS-1957, NAID 311001910, TR-1-57 raw objects 001-003": ["001.png", "002.png", "003.png"],
    "AIIRS-1957, NAID 311001910, IR-2-57 raw objects 019-021": ["019.png", "020.png", "021.png"],
    "AIIRS-1957, NAID 311001910, raw object 015": ["page-015.png"],
    "AIIRS-1957, NAID 311001910, Report 1-57 raw objects 048-054": [f"{n:03d}.png" for n in range(48, 55)],
    "DOS-UAP-D1, PORT MORESBY 00199": ["png-cable-1.png", "png-cable-2.png"],
    "DOS-UAP-D2, DUSHANBE 00259": ["kazakhstan-cable-1_DOS-UAP-D2.png", "kazakhstan-cable-2_DOS-UAP-D2.png"],
}
for token, suffixes in expected_index.items():
    paths = index.get(token, [])
    for suffix in suffixes:
        require(any(path.endswith(suffix) for path in paths), f"{token}: missing {suffix}")

# DeFuniak — two observers; visual estimate plus the report's own conventional assessment.
df = cases["BF-1956-DF-01"]
require(df["observation"]["witnessCount"] == 2, "DeFuniak witness count must be two")
require("two ground observers" in text(df), "DeFuniak two-observer boundary missing")
require("single-witness" not in text(df), "DeFuniak stale single-witness limitation")
require("tr-1-57" in df["sourceQuality"].lower() and "nara naid 311001910" in df["sourceQuality"].lower(), "DeFuniak provenance not specific")
require("probably a helicopter" in df["official"].lower() and "initial high velocity" in df["official"].lower(), "DeFuniak competing assessment boundary missing")

# B-47 — the B-47 was a distance reference; the observers were ground-based Philco personnel.
b47 = cases["BF-1957-B47-01"]
require(b47["observation"]["witnessCount"] == 2, "B-47 witness count must be two")
require(any("philco technical" in role.lower() for role in b47["observation"]["witnessRoles"]), "B-47 Philco witness roles missing")
for stale in ("b-47 crew", "b-47-crew-observation", "not of a conventional nature", "intelligence value"):
    require(stale not in text(b47), f"B-47 stale unsupported claim remains: {stale}")
for support in ("two-ground-observers", "b-47-distance-reference", "mach-2-3-visual-estimate", "investigator-could-offer-no-explanation"):
    require(support in b47["sourceRecords"][0]["supports"], f"B-47 support missing: {support}")
require(("15 seconds" in b47["sourceQuality"].lower() or "15-second" in b47["sourceQuality"].lower()) and "visual" in b47["sourceQuality"].lower(), "B-47 estimate boundary missing")

# Cigar-Y — exact location is present; one civilian witness and no corroborating packet.
cg = cases["BF-1957-CG-01"]
require(cg["observation"]["witnessCount"] == 1, "Cigar-Y witness count must be one")
require(any("civilian" in role.lower() for role in cg["observation"]["witnessRoles"]), "Cigar-Y civilian role missing")
require("exact-location-not-extracted" not in text(cg), "Cigar-Y stale location limitation")
require("661st aircraft control and warning squadron" in cg["sourceRecords"][0]["provenance"].lower(), "Cigar-Y originating unit missing")
require("single-witness" in cg["sourceRecords"][0]["limitations"], "Cigar-Y single-witness limitation missing")

# Hastings — exact date/duration and witness roster from the complete packet.
ht = cases["BF-1957-HT-01"]
require(ht["date"] == "16 JUL 1957" and ht["temporal"]["dateLabel"] == "16 JUL 1957", "Hastings exact date missing")
require(ht["observation"]["durationSeconds"] == 2100 and ht["temporal"]["durationSeconds"] == 2100, "Hastings 35-minute duration missing")
require(any("16-year-old nephew" in role.lower() for role in ht["observation"]["witnessRoles"]), "Hastings nephew witness role missing")
require("newspaper owner" not in text(ht), "Hastings stale witness role remains")
require("048–054" in ht["sourceQuality"] and "witness statement" in ht["sourceQuality"].lower(), "Hastings packet provenance incomplete")
require("no exact or definite information" in ht["official"].lower(), "Hastings refueling uncertainty not preserved")

# PNG — a radar pickup is reported, but no raw radar plot/record is preserved.
png = cases["BF-1985-PNG-01"]
require(png["date"] == "24 JAN 1985" and png["temporal"]["dateLabel"] == "24 JAN 1985", "PNG event date missing")
require("airborne-radar" in png["observation"]["sensors"], "PNG reported radar sensor missing")
require("air-niugini-pilot-radar-detection" in png["sourceRecords"][0]["supports"], "PNG radar report support missing")
require("no-radar-data" not in text(png), "PNG stale no-radar-data claim")
require("no-raw-radar-plot-or-recording" in png["sourceRecords"][0]["limitations"], "PNG raw-radar limitation missing")
require("28 jan 1985" in png["sourceQuality"].lower() and "24 jan 1985" in png["sourceQuality"].lower(), "PNG cable/event dates not separated")
require("28 January 1985" in png["sources"][0] and "24 January 1985" in png["sources"][0], "PNG source citation dates not separated")

# Kazakhstan — event/cable dates separated; crew interpretation is not an embassy finding.
kz = cases["BF-1994-KZ-01"]
require(kz["date"] == "27 JAN 1994" and kz["temporal"]["dateLabel"] == "27 JAN 1994", "Kazakhstan event date missing")
require("31 jan 1994" in kz["sourceQuality"].lower() and "27 jan 1994" in kz["sourceQuality"].lower(), "Kazakhstan cable/event dates not separated")
require("31 January 1994" in kz["sources"][0] and "27 January 1994" in kz["sources"][0], "Kazakhstan source citation dates not separated")
require("we have no opinion" in kz["official"].lower(), "Kazakhstan embassy boundary missing")
require("crew opinion" in kz["sourceQuality"].lower() and "photographs" in kz["sourceQuality"].lower(), "Kazakhstan interpretation/custody boundary missing")
require("physical evidence" not in kz["whyItMatters"].lower(), "Kazakhstan contrails mislabeled physical evidence")

for case_id in IDS:
    quality = cases[case_id]["sourceQuality"].strip().lower()
    provenance = cases[case_id]["sourceRecords"][0]["provenance"].lower()
    require(not quality.startswith("primary source —"), f"{case_id}: sourceQuality remains generic")
    require("official u.s." in provenance, f"{case_id}: primary custody is not machine-readable")
    require("transcription" not in cases[case_id]["quoteConfidence"].lower(), f"{case_id}: verified-page quote is still tagged for transcription review")
    require(triage_cases[case_id]["category"] == "complete", f"{case_id}: triage remains {triage_cases[case_id]['category']}")
    require(case_id not in weak_ids, f"{case_id}: remains in source-depth weak priorities")

expected_timeline_dates = {
    "BF-1956-DF-01": "26 DEC 1956",
    "BF-1957-B47-01": "15 APR 1957",
    "BF-1957-CG-01": "09 AUG 1957",
    "BF-1957-HT-01": "16 JUL 1957",
    "BF-1985-PNG-01": "24 JAN 1985",
    "BF-1994-KZ-01": "27 JAN 1994",
}
timeline = {event.get("caseId"): event for event in atlas["timeline"] if event.get("caseId") in IDS}
require(timeline.keys() == IDS, "selected timeline entries missing")
for case_id, expected_date in expected_timeline_dates.items():
    require(timeline[case_id]["date"] == expected_date, f"{case_id}: timeline date remains stale")

whole_atlas = json.dumps(atlas, ensure_ascii=False).lower()
for stale in ("a b-47 crew watched", "not of a conventional nature", "investigator-forced-helicopter-explanation", "exact-location-not-extracted", "newspaper owner"):
    require(stale not in whole_atlas, f"stale cross-surface claim remains: {stale}")

print("SELECTIVE PRIMARY-RECORD QUALITY PASS: 6 cases")
