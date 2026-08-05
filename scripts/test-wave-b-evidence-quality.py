#!/usr/bin/env python3
"""Regression guard for Wave B question-driven evidence quality."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IDS = {"BF-1967-MA-01", "BF-1980-RF-01", "BF-SF-11", "BF-SF-05"}
atlas = json.loads((ROOT / "atlas-data.json").read_text())
index = json.loads((ROOT / "source-file-index.json").read_text())
by_id = {case["id"]: case for case in atlas["cases"]}
assert IDS <= by_id.keys()

mal = by_id["BF-1967-MA-01"]
assert mal["date"] == "16 MAR 1967"
assert mal["temporal"]["startDateTime"] == "1967-03-16T08:45:00"
assert mal["temporal"]["timezone"] is None
assert "timezone not stated" in mal["temporal"]["precision"].lower()
assert "rumors of unidentified flying objects" in mal["official"].lower()
assert "were disproven" in mal["official"].lower()
assert "later witness" in mal["summary"].lower()
assert "does not resolve" in mal["summary"].lower()
assert mal["sourceLocator"] == "MALMSTROM-1967"
assert "MALMSTROM-1967" in index and len(index["MALMSTROM-1967"]) >= 6
assert "assets/evidence/MALMSTROM-1967/Malmstrom_FOIA_page_014.jpg" in index["MALMSTROM-1967"]
assert mal["phenomena"]["shapes"] == []
assert "ufo sighting" not in " ".join(mal["observation"]["sensors"]).lower()
assert any("strategic missile wing history" in r["citation"].lower() and "pdf p. 14" in r["locator"].lower() for r in mal["sourceRecords"])
assert any(r["sourceType"] == "later-witness-testimony" and "does not override" in " ".join(r["limitations"]).lower() for r in mal["sourceRecords"])

ren = by_id["BF-1980-RF-01"]
assert ren["date"] == "27–29 DEC 1980"
assert ren["temporal"]["startDateTime"] == "1980-12-27"
assert ren["temporal"]["endDateTime"] == "1980-12-29"
assert ren["temporal"]["eventForm"] == "multi-night-sequence"
assert ren["sourceLocator"] == "RENDLESHAM-1980"
assert len(index["RENDLESHAM-1980"]) >= 7
assert "nuclear-facility" not in ren["environment"]
assert any(r["sourceType"] == "later-administrative-record" and "not independent event evidence" in " ".join(r["limitations"]).lower() for r in ren["sourceRecords"])
assert any(s["publisher"] == "The National Archives (UK)" for s in ren["publicSources"])
assert all(s.get("publisher") != "National Archives and Records Administration" for s in ren["publicSources"])

ben = by_id["BF-SF-11"]
assert ben["status"] == "DOCUMENTED CONTACT · DISPUTED OPERATION"
assert ben["confidence"] == "CONFIRMED OFFICIAL CONTACT · ATTRIBUTED LATER ADMISSION"
assert "afosi would not become involved" in ben["keyQuote"].lower()
assert "later attributed testimony" in ben["summary"].lower()
assert "does not contain an authorization" in ben["summary"].lower()
assert "afosi has never formally acknowledged" not in ben["official"].lower()
assert ben["sourceLocator"] == "BENNEWITZ-1980"
assert len(index["BENNEWITZ-1980"]) >= 9
assert ben["phenomena"]["shapes"] == []
assert ben["observation"]["sensors"] == []
assert any(r["sourceType"] == "official-contact-file" and "does not document an authorized disinformation operation" in " ".join(r["limitations"]).lower() for r in ben["sourceRecords"])
assert any(r["sourceType"] == "later-attributed-testimony" and "admission" in " ".join(r["supports"]).lower() for r in ben["sourceRecords"])
assert any(r["sourceType"] == "disputed-document-artifact" and "does not authenticate" in " ".join(r["limitations"]).lower() for r in ben["sourceRecords"])

mj = by_id["BF-SF-05"]
assert mj["date"] == "1984–1991"
assert mj["status"] == "DOCUMENTED FILE · DOCUMENTS ASSESSED BOGUS"
assert mj["confidence"] == "CONFIRMED FBI CUSTODY · NO AUTHENTICATION"
assert "reported receiving" in mj["summary"].lower()
assert "relays an afosi conclusion" in mj["official"].lower()
assert "does not identify the creator" in mj["official"].lower()
assert "document is bogus and the case should be closed" in mj["keyQuote"].lower()
assert mj["sourceLocator"] == "MJ12-1984"
assert len(index["MJ12-1984"]) >= 3
assert mj["phenomena"]["shapes"] == []
assert mj["observation"]["sensors"] == []
assert mj["temporal"]["eventForm"] == "document-provenance-sequence"
assert any("fbi file 65-81170" in r["citation"].lower() and "does not authenticate" in " ".join(r["limitations"]).lower() for r in mj["sourceRecords"])

# Cross-case source-family boundary: later handling, mirrors, and testimony do not become
# independent event-bearing corroboration merely because they are separately indexed.
for cid in IDS:
    case = by_id[cid]
    assert case["sourceRecords"]
    assert all(r.get("supports") and r.get("limitations") for r in case["sourceRecords"])

print("PASS: Wave B evidence-quality regression (4 cases)")
