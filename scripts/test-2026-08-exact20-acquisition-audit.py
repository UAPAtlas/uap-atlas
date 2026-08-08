#!/usr/bin/env python3
"""Regression for the August 2026 exact-20 acquisition-audit tranche."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
AUDIT_DATE = "2026-08-08"
SCOPE = [
    "BF-1994-AR-01", "BF-SF-12", "BF-1975-TW-01", "BF-SF-13", "BF-1966-WS-01",
    "BF-1973-PG-01", "BF-1978-VL-01", "BF-1987-GB-01", "BF-2014-CH-01", "BF-SF-06",
    "BF-1933-MG-01", "BF-1965-KB-01", "BF-1996-VG-01", "BF-1997-PH-01", "BF-1944-FF-01",
    "BF-1990-CV-01", "BF-1978-KK-01", "BF-1980-CLD-01", "BF-2006-OH-01", "BF-2020-AS-01",
]
NEWLY_NORMALIZED = {"BF-1965-KB-01", "BF-1997-PH-01", "BF-1990-CV-01", "BF-1980-CLD-01", "BF-2006-OH-01"}
RESOLVED = {"recovered", "recovered-new", "duplicate-existing", "complete", "closed"}


def require(ok: bool, message: str) -> None:
    if not ok:
        raise SystemExit(f"FAIL: {message}")


data = json.loads((ROOT / "atlas-data.json").read_text())
triage = json.loads((ROOT / "qa/atlas_operational_triage.json").read_text())
queue = json.loads((ROOT / "qa/atlas_acquisition_targets.json").read_text())
by_id = {case["id"]: case for case in data["cases"]}
ranked = queue.get("cases", queue if isinstance(queue, list) else [])

require(len(SCOPE) == len(set(SCOPE)) == 20, "scope is not exactly 20 unique IDs")
require(set(SCOPE) <= set(by_id), "scope contains a non-existing case")
require(len(data["cases"]) == 155, "case count drifted")
require(len(data["timeline"]) == 153, "timeline count drifted")
require([row["id"] for row in ranked[:20]] == SCOPE, "authoritative top-20 rank order drifted")
require(triage["counts"]["trueGaps"] == 0 and triage["counts"]["qualityUpgrades"] == 0, "quality/gap queues reopened")

for cid in SCOPE:
    targets = by_id[cid].get("acquisitionTargets") or []
    require(targets and all(isinstance(t, dict) for t in targets), f"{cid}: targets are not structured")
    require(all(t.get("lastPublicAudit") == AUDIT_DATE for t in targets), f"{cid}: audit date missing")
    require(all(t.get("auditScope") == "public-only" for t in targets), f"{cid}: public-only scope missing")
    require(any(t.get("status") not in RESOLVED for t in targets), f"{cid}: no active target remains despite acquisition rank")

for cid in NEWLY_NORMALIZED:
    require(all("targetType" in t and "publicOnlyResult" in t for t in by_id[cid]["acquisitionTargets"]), f"{cid}: legacy targets not normalized")

k = by_id["BF-1965-KB-01"]
require("public mirror" in k["sourceQuality"].lower(), "Kecksburg mirror custody boundary missing")
require("authenticate" in k["quoteConfidence"].lower(), "Kecksburg authentication boundary missing")
require(any("conclusion-of-nasa-lawsuit" in str(r.get("locator", "")) for r in k.get("sourceRecords", [])), "Kecksburg conclusion record missing")
require(all("NASA-origin" not in r.get("provenance", "") or "not NASA-origin" in r.get("provenance", "") for r in k.get("sourceRecords", [])), "Kecksburg mirror misrepresented as NASA origin")

cash = by_id["BF-1980-CLD-01"]
require(any(r.get("locator") == "https://www.cufon.org/cufon/cashlanC.pdf" for r in cash.get("sourceRecords", [])), "Cash-Landrum CUFON claims packet missing")
require(any(r.get("locator") == "https://www.cufon.org/cufon/cashlani.htm" and r.get("continuationUrl", "").endswith("cashlani2.htm") for r in cash.get("sourceRecords", [])), "Cash-Landrum two-part interview transcript missing")
require("not a complete court-origin" in cash["sourceQuality"].lower(), "Cash-Landrum mirror boundary missing")
ohare = by_id["BF-2006-OH-01"]
require(any(s.get("url") == "https://www.governmentattic.org/docs/FOIA_Logs_FAA_FY2007.pdf" for s in ohare.get("publicSources", [])), "O'Hare FAA FOIA-log locator missing")

report = ROOT / "research" / "exact20-acquisition-audit-tranche-2026-08.md"
require(report.exists(), "tranche report missing")
text = report.read_text()
for cid in SCOPE:
    require(cid in text, f"{cid}: absent from tranche report")

print("PASS: exact-20 acquisition audit (20 ranked existing cases; 155 cases / 153 timeline)")
