#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
atlas = json.loads((ROOT / "atlas-data.json").read_text())
triage = json.loads((ROOT / "qa/atlas_operational_triage.json").read_text())

cases = {case["id"]: case for case in atlas["cases"]}
timeline = {row["caseId"]: row for row in atlas.get("timeline", []) if row.get("caseId")}
by_triage = {row["id"]: row for row in triage["cases"]}


def text(value):
    return json.dumps(value, ensure_ascii=False).lower()


def require(needle, value, label):
    assert needle.lower() in text(value), f"{label}: missing {needle!r}"


def prohibit(needle, value, label):
    assert needle.lower() not in text(value), f"{label}: stale/unsupported {needle!r}"


# Maury: recover the adjacent ARS mission report without conflating it with the
# missing formal accident investigation, Seattle FBI report, or slag custody.
maury = cases["BF-1947-MI-01"]
ars = [r for r in maury.get("sourceRecords", []) if r.get("locator") == "MAURY-1947-ARS-FMR"]
assert len(ars) == 1, f"Maury: expected one ARS mission-report source record, got {len(ars)}"
require("4 august 1947", ars[0].get("provenance"), "Maury ARS provenance")
require("fire in the left engine", ars[0].get("supports"), "Maury ARS supports")
require("does not identify", ars[0].get("limitations"), "Maury ARS limitations")
require("maury fragments", ars[0].get("limitations"), "Maury ARS limitations")
require("left-engine fire", maury.get("official"), "Maury official")
require("does not establish", maury.get("official"), "Maury official")
assert len(maury.get("acquisitionTargets") or []) == 3
assert by_triage[maury["id"]]["category"] == "acquisition_target"

# Cash-Landrum: the AFU/Quest packet improves legal custody, but the court did
# not adjudicate object identity, causation, or the event as fact.
cash = cases["BF-1980-CLD-01"]
obs = cash.get("observation") or {}
assert obs.get("witnessCount") == 3
require("civilian", obs.get("witnessRoles"), "Cash witness roles")
require("unaided-visual", obs.get("sensors"), "Cash sensors")
prohibit("military police", obs.get("witnessRoles"), "Cash witness roles")
prohibit("infrared", obs.get("sensors"), "Cash sensors")
quest = [r for r in cash.get("sourceRecords", []) if r.get("locator") == "CASH-LANDRUM-H84-348-AFU-QUEST"]
assert len(quest) == 1, f"Cash: expected one AFU/Quest source record, got {len(quest)}"
require("public mirror", quest[0].get("provenance"), "Cash Quest provenance")
require("order of dismissal", quest[0].get("supports"), "Cash Quest supports")
require("party positions", quest[0].get("limitations"), "Cash Quest limitations")
require("did not adjudicate", cash.get("official"), "Cash official")
prohibit("proved an absence of ownership", cash, "Cash dossier")
prohibit("fails on ownership, not on the event", timeline[cash["id"]], "Cash timeline")
require("legal grounds", timeline[cash["id"]].get("desc"), "Cash timeline")
assert by_triage[cash["id"]]["category"] == "acquisition_target"

# O'Hare: NARCAP published analysis of 13 FAA NTAP data files. Native files and
# a complete FAA/United packet remain missing, and a null correlated return does
# not falsify the visual witness reports.
ohare = cases["BF-2006-OH-01"]
require("13", ohare.get("sourceRecords"), "O'Hare source record")
require("ntap", ohare.get("sourceRecords"), "O'Hare source record")
require("no return", ohare.get("sourceRecords"), "O'Hare source record")
require("does not disprove", ohare.get("sourceRecords"), "O'Hare source record")
require("native", ohare.get("gap"), "O'Hare gap")
require("ntap", ohare.get("gap"), "O'Hare gap")
prohibit("no radar analysis was published", ohare, "O'Hare dossier")
require("aviation", (ohare.get("observation") or {}).get("witnessRoles"), "O'Hare witness roles")
assert by_triage[ohare["id"]]["category"] == "acquisition_target"

print("PUBLIC ACQUISITION INTEGRATION PASS: Maury + Cash-Landrum + O'Hare")
