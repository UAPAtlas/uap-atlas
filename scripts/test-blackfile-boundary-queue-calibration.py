#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
atlas = json.loads((ROOT / "atlas-data.json").read_text())
triage = json.loads((ROOT / "qa/atlas_operational_triage.json").read_text())
weak = json.loads((ROOT / "qa/source-depth-weak-case-priorities.json").read_text())
index = json.loads((ROOT / "source-file-index.json").read_text())
blackfile = json.loads((ROOT / "blackfile-analysis.json").read_text())

cases = {case["id"]: case for case in atlas["cases"]}
by_triage = {row["id"]: row for row in triage["cases"]}
weak_rows = weak.get("cases", []) if isinstance(weak, dict) else weak
weak_ids = {row["id"] for row in weak_rows}
timeline = {row["caseId"]: row for row in atlas.get("timeline", []) if row.get("caseId")}

def text(value):
    return json.dumps(value, ensure_ascii=False).lower()

def require(needle, value, label):
    assert needle.lower() in text(value), f"{label}: missing {needle!r}"

def prohibit(needle, value, label):
    assert needle.lower() not in text(value), f"{label}: stale/unsupported {needle!r}"

# Santilli: current custody does not contain the exact 2006 interview or an original master.
santilli = cases["BF-SF-12"]
assert santilli.get("outcome") != "resolved-fabrication"
require("exact 2006", santilli.get("sourceQuality"), "Santilli sourceQuality")
require("not held", santilli.get("sourceQuality"), "Santilli sourceQuality")
assert len(santilli.get("acquisitionTargets") or []) >= 2
prohibit("rare hoax with a confession", santilli, "Santilli dossier")
prohibit("closed the authenticity question", santilli, "Santilli dossier")
assert by_triage[santilli["id"]]["category"] == "acquisition_target"

# Maury Island: the FBI teletype explicitly says the subject did not admit a hoax.
maury = cases["BF-1947-MI-01"]
require("did not admit", maury.get("keyQuote"), "Maury keyQuote")
require("14 august 1947", maury.get("quoteSource"), "Maury quoteSource")
require("official fbi", maury.get("sourceQuality"), "Maury sourceQuality")
assert maury.get("outcome") != "resolved-fabrication"
assert len(maury.get("acquisitionTargets") or []) >= 2
prohibit("hoax dahl himself disavowed", maury, "Maury dossier")
prohibit("classify the claims as a hoax", maury, "Maury dossier")
prohibit("cost two intelligence officers their lives", maury, "Maury dossier")
obs = maury.get("observation") or {}
prohibit("infrared", obs.get("sensors") or [], "Maury sensors")
prohibit("military police", obs.get("witnessRoles") or [], "Maury witness roles")
assert by_triage[maury["id"]]["category"] == "acquisition_target"
assert timeline[maury["id"]]["date"] == "21 JUN 1947"

# Western U.S.: five separate released memoranda, event in Oct 2023, records in Jun 2026.
wus = cases["BF-2023-WUS-03"]
assert wus.get("date") == "OCT 2023"
assert (wus.get("temporal") or {}).get("eventForm") == "multi-event"
assert (wus.get("observation") or {}).get("witnessCount") == 5
require("federal law enforcement special agents", (wus.get("observation") or {}).get("witnessRoles"), "WUS witness roles")
require("night-vision", (wus.get("observation") or {}).get("sensors"), "WUS sensors")
require("objects initially appeared to mimic vehicles", wus.get("keyQuote"), "WUS keyQuote")
require("witness 2", wus.get("quoteSource"), "WUS quoteSource")
records = wus.get("sourceRecords") or []
assert len(records) == 5, f"WUS: expected five source records, got {len(records)}"
assert {r.get("locator") for r in records} == {f"DOW-UAP-D{i:03d}" for i in range(79, 84)}
for record in records:
    require("02 june 2026", record.get("provenance"), f"WUS {record.get('locator')} provenance")
for i in range(79, 84):
    assert len(index.get(f"DOW-UAP-D{i:03d}", [])) == 1
require("five", wus.get("sourceQuality"), "WUS sourceQuality")
require("october 2023", wus.get("summary"), "WUS summary")
require("june 2026", wus.get("official"), "WUS official")
assert by_triage[wus["id"]]["category"] == "complete"
assert wus["id"] not in weak_ids
require("five federal", timeline[wus["id"]].get("desc"), "WUS timeline")
require("june 2026", timeline[wus["id"]].get("desc"), "WUS timeline")

# Queue-calibration regressions: these complete records were false positives.
for case_id in ("BF-1957-RA-01", "BF-2015-NAV-01", "BF-2023-LG-01"):
    assert by_triage[case_id]["category"] == "complete", (case_id, by_triage[case_id])

# Blackfile interpretive layer: boundary changes, overall q4 conclusion remains intact.
q4 = next(question for question in blackfile["questions"] if question["id"] == "q4")
boundary = next(
    tension for tension in q4["tensions"]
    if tension["label"] == "Maury and Santilli suspicion versus verified admission custody"
)
assert set(boundary["caseIds"]) == {"BF-1947-MI-01", "BF-SF-12"}
require("did not admit", boundary["summary"], "Blackfile q4 boundary")
require("not in mapped atlas custody", boundary["summary"], "Blackfile q4 boundary")
require("does not prove", q4["answer"], "Blackfile q4 answer")

counts = triage["counts"]
assert counts == {
    "trueGaps": 0,
    "acquisitionTargets": 18,
    "qualityUpgrades": 9,
    "complete": 123,
}, counts

print("BLACKFILE BOUNDARY + QUEUE CALIBRATION PASS: 3 cases; three provenance targets reclassified")
