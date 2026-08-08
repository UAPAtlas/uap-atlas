#!/usr/bin/env python3
"""Regression for the August 2026 exact-20 quality/acquisition tranche."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
COMPLETE = {
    "BF-SF-08", "BF-1977-CL-01", "BF-2025-YS-01", "BF-1989-BW-01", "BF-SF-04",
}
ACQUISITION = {
    "BF-SF-13", "BF-1978-KK-01", "BF-2020-AS-01", "BF-1944-FF-01",
    "BF-1987-GB-01", "BF-1994-AR-01", "BF-1933-MG-01", "BF-1975-TW-01",
    "BF-1996-VG-01", "BF-SF-12", "BF-1966-WS-01", "BF-1973-PG-01",
    "BF-1978-VL-01", "BF-2014-CH-01", "BF-SF-06",
}
SCOPE = COMPLETE | ACQUISITION


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


data = json.loads((ROOT / "atlas-data.json").read_text())
triage = json.loads((ROOT / "qa/atlas_operational_triage.json").read_text())
by_id = {case["id"]: case for case in data["cases"]}
triage_by_id = {case["id"]: case for case in triage["cases"]}

require(len(SCOPE) == 20, "scope is not exactly 20 existing cases")
require(set(SCOPE) <= set(by_id), "one or more scoped existing cases are absent")
require(len(data["cases"]) == 155, "case count changed")
require(len(data["timeline"]) == 153, "timeline count changed")
require(triage["counts"] == {"trueGaps": 0, "qualityUpgrades": 0, "acquisitionTargets": 22, "complete": 133}, "final triage counts drifted")

for cid in COMPLETE:
    require(triage_by_id[cid]["category"] == "complete", f"{cid} did not close its quality repair")
for cid in ACQUISITION:
    require(triage_by_id[cid]["category"] == "acquisition_target", f"{cid} did not retain structured acquisition status")
    targets = by_id[cid].get("acquisitionTargets") or []
    require(targets and all(isinstance(item, dict) for item in targets), f"{cid} acquisition targets are not structured")

require(by_id["BF-SF-08"]["confidenceModel"]["provenance"] == "public-report-copy", "COMETA institutional boundary drifted")
require(by_id["BF-SF-13"]["domain"] == "CIVILIAN / CONTACTEE CORPUS", "Meier domain drifted")
require(by_id["BF-SF-13"]["heroVisual"]["isEventEvidence"] is False, "Meier reproduction promoted to event evidence")
require(by_id["BF-2020-AS-01"]["quoteConfidence"].startswith("High for 'a few abrupt directional changes'"), "D44 page-verified quote boundary drifted")
require(by_id["BF-1977-CL-01"]["heroVisual"]["isEventEvidence"] is False, "Colares reproduction promoted to original event evidence")
require(by_id["BF-2025-YS-01"]["temporal"]["durationSeconds"] == 15, "Yellow Sea DVIDS duration metadata drifted")
require("18 seconds" in by_id["BF-2025-YS-01"]["summary"] and "00:00:15" in by_id["BF-2025-YS-01"]["summary"], "Yellow Sea duration tension lost")
require(by_id["BF-SF-04"]["domain"] == "SCIENTIFIC / HISTORICAL CONTEXT", "Chapel Hill domain drifted")
require(by_id["BF-SF-04"]["observation"]["sensors"] == [], "Chapel Hill retained event sensors")
require(by_id["BF-1933-MG-01"]["phenomena"]["shapes"] == [], "Magenta anonymous paper claim gained object geometry")
require(by_id["BF-SF-12"]["domain"] == "MEDIA / PROVENANCE", "Santilli media/provenance boundary drifted")
require(by_id["BF-1966-WS-01"]["mode"] == "approximate", "Westall city-level geometry marked exact")
require(by_id["BF-1973-PG-01"]["mode"] == "approximate", "Pascagoula broad location marked exact")
require(by_id["BF-SF-06"]["observation"]["witnessRoles"] == ["anonymous claimant", "media-production/distribution personnel"], "Victor unsupported witness roles returned")
require("149,946,368" not in json.dumps(by_id["BF-SF-06"]), "Victor unverified retained-file size claim returned")

report = ROOT / "research" / "exact20-quality-acquisition-tranche-2026-08.md"
require(report.exists(), "tranche report missing")
report_text = report.read_text()
for cid in SCOPE:
    require(cid in report_text, f"{cid} absent from tranche report")

print(f"PASS: exact-20 tranche ({len(COMPLETE)} complete, {len(ACQUISITION)} acquisition; 155 cases / 153 timeline)")
