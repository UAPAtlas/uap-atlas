#!/usr/bin/env python3
"""Run the Atlas audit and print a concise weekly operational state report."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QA = ROOT / "qa"

subprocess.run(
    ["python3", str(ROOT / "scripts" / "audit-atlas-data.py")],
    cwd=ROOT,
    check=True,
    stdout=subprocess.DEVNULL,
)
subprocess.run(
    ["python3", str(ROOT / "scripts" / "test-audit-operational-triage.py")],
    cwd=ROOT,
    check=True,
    stdout=subprocess.DEVNULL,
)

triage = json.loads((QA / "atlas_operational_triage.json").read_text())
counts = triage["counts"]

def top(filename: str, limit: int = 3) -> list[str]:
    rows = json.loads((QA / filename).read_text())["cases"][:limit]
    return [f"- {row['title']} (`{row['id']}`): {', '.join(row['reasons'])}" for row in rows]

lines = [
    "**UAP Atlas — Weekly State**",
    "",
    f"- True gaps: **{counts['trueGaps']}**",
    f"- Acquisition targets: **{counts['acquisitionTargets']}**",
    f"- Quality upgrades: **{counts['qualityUpgrades']}**",
    f"- Operationally complete: **{counts['complete']} / {sum(counts.values())}**",
]

true_gaps = top("atlas_true_gaps.json")
if true_gaps:
    lines.extend(["", "**Immediate structural gaps**", *true_gaps])
else:
    lines.extend(["", "**Immediate structural gaps:** none"])

acquisition = top("atlas_acquisition_targets.json")
if acquisition:
    lines.extend(["", "**Top acquisition targets**", *acquisition])

quality = top("atlas_quality_upgrades.json")
if quality:
    lines.extend(["", "**Top internal upgrades**", *quality])

lines.extend([
    "",
    "No FOIA, archival request, outreach, deployment, or case addition was performed.",
])
print("\n".join(lines))
