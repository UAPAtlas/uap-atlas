#!/usr/bin/env python3
"""Regression guard for Wave C question-driven evidence upgrades."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ATLAS = ROOT / "atlas-data.json"
INDEX = ROOT / "source-file-index.json"
BACKLOG = ROOT / "qa" / "enrichment-backlog.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def blob(value) -> str:
    return json.dumps(value, ensure_ascii=False).lower()


def require(text: str, *phrases: str) -> None:
    for phrase in phrases:
        assert phrase.lower() in text, f"missing phrase: {phrase}"


def main() -> None:
    atlas = load(ATLAS)
    assert len(atlas["cases"]) == 146
    cases = {c["id"]: c for c in atlas["cases"]}
    index = load(INDEX)
    backlog = load(BACKLOG)

    lazar = cases["BF-SF-01"]
    ltxt = blob(lazar)
    require(
        ltxt,
        "primary evidence that he made the claims, not that s-4",
        "no primary employment, education, program, material-sample, laboratory, or chain-of-custody record",
        "groom lake",
        "does not establish lazar's alleged s-4 program",
        "all-radioactive row 7",
        "does not verify lazar's claimed stable fuel isotope",
        "not a unique prediction",
    )
    assert len(lazar.get("sourceRecords", [])) == 3
    assert lazar.get("confidenceModel", {}).get("anomaly") == "not-established"
    ltypes = {r["sourceType"] for r in lazar["sourceRecords"]}
    assert ltypes == {"broadcast-claim-record", "official-site-history", "official-scientific-reference"}
    lurls = blob(lazar.get("publicSources", []))
    require(lurls, "2grjgbvw9pk", "cia.gov/stories", "nist.gov/blogs")
    assert "wpn5pjoxhbo" not in lurls
    assert "d9tdj2skbkq" not in lurls

    brown = cases["BF-SF-03"]
    btxt = blob(brown)
    require(
        btxt,
        "patent records brown's claims and apparatus, not independent validation",
        "confirm or deny",
        "if experiments prove to be positive",
        "no responsibility can be assumed",
        "does not establish department of defense acceptance, funding, completion, or operational use",
        "no linear thrust was observed",
        "corona wind effects were misinterpreted",
    )
    assert len(brown.get("sourceRecords", [])) == 4
    assert brown.get("confidenceModel", {}).get("anomaly") == "not-established"
    btypes = {r["sourceType"] for r in brown["sourceRecords"]}
    assert btypes == {
        "inventor-patent",
        "proposal-and-archive-custody",
        "official-evaluation-mirror-transcription",
        "independent-technical-test",
    }
    burls = blob(brown.get("publicSources", []))
    require(burls, "patents.google.com/patent/us1974483a", "archives.lib.umd.edu", "winterhaven.pdf", "biefeld-brown-effect-aiaa")

    assert "LAZAR-1989" in index
    assert "WINTERHAVEN-1952" in index
    assert index["LAZAR-1989"] == [
        "assets/evidence/LAZAR/groom_papoose.jpg",
        "assets/evidence/LAZAR/area51_gate.jpg",
    ]
    assert index["WINTERHAVEN-1952-PATENT"] == index["WINTERHAVEN-1952"]

    backlog_ids = {x["id"] for x in backlog.get("cases", [])}
    assert "BF-SF-01" not in backlog_ids
    assert "BF-SF-03" not in backlog_ids

    print("PASS: Wave C evidence-quality regression (2 cases)")


if __name__ == "__main__":
    main()
