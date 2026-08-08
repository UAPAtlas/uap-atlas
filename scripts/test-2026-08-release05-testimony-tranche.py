#!/usr/bin/env python3
"""Regression gate for the four-case Release 05 lower-confidence testimony tranche."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IDS = {"BF-2002-BG-01", "BF-2023-CST-01", "BF-2011-DT-01", "BF-2023-CSR-01"}
ASSETS = {
    "BF-2002-BG-01": "assets/sources/PURSUE-RELEASE-05/FBI-UAP-D025-witness-reconstruction.jpg",
    "BF-2023-CST-01": "assets/sources/PURSUE-RELEASE-05/FBI-UAP-D027-witness-reconstruction.jpg",
    "BF-2011-DT-01": "assets/sources/PURSUE-RELEASE-05/FBI-UAP-D029-witness-reconstruction.jpg",
    "BF-2023-CSR-01": "assets/sources/PURSUE-RELEASE-05/FBI-UAP-D031-witness-reconstruction.jpg",
}


def require(ok, message):
    if not ok:
        raise AssertionError(message)


atlas = json.loads((ROOT / "atlas-data.json").read_text())
by_id = {c["id"]: c for c in atlas["cases"]}
require(len(atlas["cases"]) == 155, "testimony tranche must produce 155 cases")
require(len(atlas["timeline"]) == 153, "testimony tranche must produce 153 timeline entries")
require(IDS <= set(by_id), "one or more testimony cases missing")
require({t["caseId"] for t in atlas["timeline"] if t["caseId"] in IDS} == IDS, "testimony timeline coverage incomplete")

for cid in IDS:
    c = by_id[cid]
    blob = json.dumps(c, ensure_ascii=False).lower()
    require("lower-confidence testimony" in blob, f"{cid} lacks lower-confidence label")
    require("fd-302" in blob and "not an fbi factual finding" in blob, f"{cid} lacks FBI interview boundary")
    require(c["heroVisual"]["isEventEvidence"] is False, f"{cid} reconstruction misclassified as event evidence")
    require("reconstruction" in c["heroVisual"]["visualType"], f"{cid} hero is not classified as reconstruction")
    require("not event imagery" in c["heroVisual"]["evidenceStatus"].lower(), f"{cid} hero warning missing")
    require(any("subjective" in x.lower() or "not established" in x.lower() or "not measured" in x.lower() for r in c["sourceRecords"] for x in r["limitations"]), f"{cid} subjective-estimate boundary missing")
    require(any("common" in x.lower() or "relationship" in x.lower() for x in c["evidenceBoundary"]["notEstablished"]), f"{cid} common-phenomenon boundary missing")
    p = ROOT / ASSETS[cid]
    require(p.is_file() and p.stat().st_size > 50_000, f"{cid} labeled reconstruction asset missing")

require(by_id["BF-2002-BG-01"]["observation"]["witnessRoles"][1].startswith("second pilot reported"), "Bagram second witness overstated")
require(by_id["BF-2002-BG-01"]["temporal"].get("timeOfDay") == "approximately 04:30 local", "Bagram reported time missing")
require(by_id["BF-2011-DT-01"]["coordinatePrecision"] == "country-redacted-generalized", "2011 redacted location overprecision")
require(by_id["BF-2011-DT-01"]["temporal"].get("durationRangeSeconds") == [10, 15], "2011 duration range flattened")
require(by_id["BF-2011-DT-01"]["temporal"].get("timeOfDay") == "about 20:00–21:00", "2011 reported time range missing")
require(by_id["BF-2023-CST-01"]["temporal"].get("timeOfDay") == "approximately 22:50", "translucent-triangle reported time missing")
require(by_id["BF-2023-CSR-01"]["temporal"].get("timeOfDay") == "between 20:00 and 21:30", "red-light-triangle time range missing")
for cid in ["BF-2023-CST-01", "BF-2023-CSR-01"]:
    require(by_id[cid]["coordinatePrecision"].startswith("city-centroid"), f"{cid} must use city-level generalized coordinates")
    require(by_id[cid].get("expectedAdmin1") == "Colorado" and by_id[cid].get("geometryExpectation") == "admin1", f"{cid} Colorado geometry contract missing")

index = json.loads((ROOT / "source-file-index.json").read_text())
for token in ["FBI-UAP-D024", "FBI-UAP-D025", "FBI-UAP-D026", "FBI-UAP-D027", "FBI-UAP-D028", "FBI-UAP-D029", "FBI-UAP-D030", "FBI-UAP-D031"]:
    require(token in index, f"source index missing {token}")

ledger = json.loads((ROOT / "research/pursue-release05-intake-ledger.json").read_text())
for row in ledger["records"]:
    ident = row["filename"].split("_", 1)[0]
    if ident in {f"FBI-UAP-D{i:03d}" for i in range(24, 32)}:
        require(row["atlasDisposition"] == "integrated-lower-confidence-testimony", f"ledger disposition stale for {ident}")

report = (ROOT / "research/pursue-release05-lower-confidence-testimony-tranche.md").read_text()
require("do not establish a common triangle phenomenon" in report, "report lacks cross-case inference boundary")
require("do not increase Blackfile confidence" in report, "report lacks Blackfile-confidence boundary")

for rel in ["atlas-data.json", "public-source-manifest.json", "source-file-index.json", "research/pursue-release05-lower-confidence-testimony-tranche.md"]:
    text = (ROOT / rel).read_text()
    for prefix in ["/Users/", "/Volumes/", "/private/tmp/", "file://"]:
        require(prefix not in text, f"{rel} leaks host-local path: {prefix}")

print("PASS: Release 05 lower-confidence testimony tranche (4 cases)")
