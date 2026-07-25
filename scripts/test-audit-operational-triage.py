#!/usr/bin/env python3
"""Validate generated UAP Atlas operational-triage artifacts."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QA = ROOT / "qa"
EXPECTED_CATEGORIES = {"true_gap", "acquisition_target", "quality_upgrade", "complete"}

triage = json.loads((QA / "atlas_operational_triage.json").read_text())
rows = triage["cases"]
counts = triage["counts"]
atlas_count = len(json.loads((ROOT / "atlas-data.json").read_text())["cases"])

assert len(rows) == atlas_count, (len(rows), atlas_count)
assert len({row["id"] for row in rows}) == atlas_count
assert set(row["category"] for row in rows) <= EXPECTED_CATEGORIES
assert sum(counts.values()) == atlas_count
assert counts["trueGaps"] == sum(row["category"] == "true_gap" for row in rows)
assert counts["qualityUpgrades"] == sum(row["category"] == "quality_upgrade" for row in rows)
assert counts["acquisitionTargets"] == sum(row["category"] == "acquisition_target" for row in rows)
assert counts["complete"] == sum(row["category"] == "complete" for row in rows)

for filename, category, count_key in (
    ("atlas_true_gaps.json", "true_gap", "trueGaps"),
    ("atlas_quality_upgrades.json", "quality_upgrade", "qualityUpgrades"),
    ("atlas_acquisition_targets.json", "acquisition_target", "acquisitionTargets"),
):
    artifact = json.loads((QA / filename).read_text())
    assert artifact["category"] == category
    assert artifact["caseCount"] == counts[count_key]
    assert all(row["category"] == category for row in artifact["cases"])

backlog = json.loads((QA / "enrichment-backlog.json").read_text())
assert backlog["schemaVersion"] == 2
assert backlog["caseCount"] == counts["trueGaps"] + counts["qualityUpgrades"]
assert all(row["category"] in {"true_gap", "quality_upgrade"} for row in backlog["cases"])
assert not ({row["id"] for row in backlog["cases"]} & {
    row["id"] for row in rows if row["category"] in {"acquisition_target", "complete"}
})

orbital_rows = [row for row in rows if row["domain"] == "ORBITAL / NASA"]
assert orbital_rows
assert all(row["category"] == "complete" for row in orbital_rows), {
    row["id"]: row["category"] for row in orbital_rows if row["category"] != "complete"
}

print(json.dumps({
    "status": "passed",
    "caseCount": atlas_count,
    "counts": counts,
    "orbitalComplete": len(orbital_rows),
}, indent=2))
