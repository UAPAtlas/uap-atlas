#!/usr/bin/env python3
"""Regression gate for the PURSUE Release 05 evidence-closure sprint."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WAR = "https://www.war.gov/UFO/?releaseDate=Release+05&release=05"
D101_FILES = {
    "DOD_111887401.mp4", "DOD_111887407.mp4", "DOD_111887421.mp4",
    "DOD_111887427.mp4", "DOD_111887439.mp4", "DOD_111887446.mp4",
}
EXPECTED_ASSET_HASHES = {
    "assets/sources/PURSUE-RELEASE-05/DOW-UAP-D101-PR117-PR122-video-contact.jpg": "d3c18730b58e1d20e5f02d08f8d8fad5183ae3ded5a6d9c2d9815a7c6f9d9995",
    "assets/sources/PURSUE-RELEASE-05/FBI-UAP-D032-PR007-video-contact.jpg": "58b14de49303afeefd183aaff3873e404753740cd626362687732cfee613d377",
    "assets/sources/NARA-GYATT-1964/USS-GYATT-1964-11-19-page-A.jpg": "88d0dda948cee6993d82ddf1cd967c9b333725a4f20788fc7dc16c1871dc988a",
    "assets/sources/NARA-GYATT-1964/USS-GYATT-1964-11-19-page-B.jpg": "092c3117941f25f213104fb354367bc54ba0d417145302998e63e06f22467353",
    "assets/sources/NARA-GYATT-1964/USS-GYATT-1964-11-24-page-A.jpg": "46e841b57489d43e559fdfc6b3e1593b55baaa12cf3d500eb08aa12847c65dc7",
    "assets/sources/NARA-GYATT-1964/USS-GYATT-1964-11-24-page-B.jpg": "b79367dc5808970912f231501b13661e4697ef74012394992bd9ef10a8c87990",
}


def require(ok, message):
    if not ok:
        raise AssertionError(message)


def source(case, locator):
    return next((row for row in case.get("sourceRecords", []) if row.get("locator") == locator), None)


atlas = json.loads((ROOT / "atlas-data.json").read_text())
by_id = {c["id"]: c for c in atlas["cases"]}
require(len(atlas["cases"]) >= 151, "closure sprint baseline of 151 cases must be retained")
require(len(atlas["timeline"]) >= 149, "closure sprint baseline of 149 timeline entries must be retained")
require("BF-2026-SMO-01" in by_id, "D032 standalone case missing")
require(any(t.get("caseId") == "BF-2026-SMO-01" for t in atlas["timeline"]), "D032 timeline entry missing")

crosswalk = json.loads((ROOT / "research/pursue-release05-video-crosswalk.json").read_text())
rows = crosswalk["records"]
require(len(rows) == 16 and crosswalk["counts"]["unmapped"] == 0, "16-video crosswalk incomplete")
require(len({r["filename"] for r in rows}) == 16, "crosswalk filename duplicate")
require(len({r["officialId"] for r in rows}) == 16, "crosswalk official-ID duplicate")
require(all(r["dvidsUrl"].startswith("https://www.dvidshub.net/video/") for r in rows), "non-DVIDS crosswalk URL")
require({r["filename"] for r in rows if r["eventGroup"] == "gulf-of-oman-d101"} == D101_FILES, "D101 six-file set mismatch")
d032_row = next(r for r in rows if r["filename"] == "DOD_111887430.mp4")
require(d032_row["officialId"] == "FBI-UAP-PR007" and d032_row["atlasMappings"] == ["BF-2026-SMO-01"], "D032 video mapping mismatch")

ledger = json.loads((ROOT / "research/pursue-release05-intake-ledger.json").read_text())
require(ledger["schemaVersion"] == 2 and ledger["recordCount"] == 41, "ledger schema/custody count changed incorrectly")
videos = [r for r in ledger["records"] if r["kind"] == "video"]
require(len(videos) == 16 and all("officialVideoRecord" in r for r in videos), "ledger videos not fully labeled")
require(not any(r["atlasDisposition"] == "corpus-only-pending-crosswalk" for r in videos), "stale pending-crosswalk disposition remains")
require(ledger["integrationSummary"]["videoCrosswalk"]["mapped"] == 16, "ledger video summary mismatch")

# D101: mapped public derivatives without native-sensor inflation.
gom = by_id["BF-2021-GOM-01"]
gom_blob = json.dumps(gom, ensure_ascii=False).lower()
for stale in ["six-video attachment is absent", "does not provide a defensible filename crosswalk", "a defensible mapping between the six"]:
    require(stale not in gom_blob, f"stale D101 boundary remains: {stale}")
for needed in ["pr117–pr122", "secondary recordings", "not native", "not finally evaluated"]:
    require(needed in gom_blob, f"D101 closure boundary missing: {needed}")
require(source(gom, "DOW-UAP-PR117–PR122"), "D101 DVIDS source record missing")
require(any(x.endswith("DOW-UAP-D101-PR117-PR122-video-contact.jpg") for x in gom["images"]), "D101 contact sheet missing")

# Gyatt: positive operating context plus an explicit negative-record boundary.
pr = by_id["BF-1964-PR-01"]
nara = source(pr, "NARA 212794455 · 19 and 24 November 1964")
require(nara and nara["url"] == "https://catalog.archives.gov/id/212794455", "Gyatt NARA record missing")
pr_blob = json.dumps(pr, ensure_ascii=False).lower()
for needed in ["northwest coast of puerto rico", "hedgehog calibration", "no entry describing", "silence"]:
    require(needed in pr_blob, f"Gyatt deck-log boundary missing: {needed}")
require("original radar film" in pr_blob and "remain missing" in pr_blob, "Gyatt missing-radar-media boundary weakened")

# D032: one standalone case, no inferred D033 merger or performance claim.
sm = by_id["BF-2026-SMO-01"]
sm_blob = json.dumps(sm, ensure_ascii=False).lower()
for needed in ["fbi-uap-d032", "fbi-uap-pr007", "dod_111887430", "two black-hot", "5–10 minutes", "10-second"]:
    require(needed in sm_blob, f"D032 case detail missing: {needed}")
for needed in ["range", "scale", "speed", "identity", "fd-302"]:
    require(needed in sm_blob, f"D032 limitation missing: {needed}")
require(sm["heroVisual"]["isEventEvidence"] is True, "D032 released clip must be classified as event footage")
require("reconstruction" not in sm["heroVisual"]["visualType"], "D032 footage mislabeled as reconstruction")
require("d033 is not merged" in sm_blob and "contents of absent identifiers d034–d036 are unknown" in sm_blob, "D033/D034–D036 boundary missing")
require(source(sm, "FBI-UAP-D032 · PDF pp. 1–2")["sha256"] == "04684f8e8e0d9292e273b8e3152be6a22e195ce25f9c4a92b21c25b1813bd1e1", "D032 PDF hash mismatch")
require(source(sm, "FBI-UAP-PR007 · DOD_111887430")["sha256"] == "56f0a2691dc2f2c9a23139b7aab119dc4f9f213db9c2f6d05f7cda727b904d54", "PR007 MP4 hash mismatch")

index = json.loads((ROOT / "source-file-index.json").read_text())
for token in ["DOW-UAP-PR117–PR122", "FBI-UAP-D032", "FBI-UAP-PR007", "NARA 212794455"]:
    require(token in index, f"source-index token missing: {token}")
for rel, expected in EXPECTED_ASSET_HASHES.items():
    path = ROOT / rel
    require(path.is_file(), f"closure asset missing: {rel}")
    require(hashlib.sha256(path.read_bytes()).hexdigest() == expected, f"closure asset hash mismatch: {rel}")

review = (ROOT / "research/pursue-release05-new-case-admission-review.md").read_text().lower()
require("add after official video crosswalk" in review, "admission review not updated for D032")
require("missing sequence identifiers with unknown contents" in review, "D034–D036 boundary not corrected")
report = (ROOT / "research/pursue-release05-evidence-closure-sprint.md").read_text()
require("All 16 MP4s" in report and "NARA catalog ID `212794455`" in report, "closure report incomplete")

for rel in ["atlas-data.json", "public-source-manifest.json", "source-file-index.json", "research/pursue-release05-video-crosswalk.json"]:
    text = (ROOT / rel).read_text()
    for prefix in ["/Users/", "/Volumes/", "/private/tmp/", "file://"]:
        require(prefix not in text, f"{rel} leaks host-local path: {prefix}")

print("PASS: Release 05 evidence-closure sprint (16-video crosswalk + Gyatt + D032)")
