#!/usr/bin/env python3
"""Attach verified public research links to every Atlas dossier.

The manifest is authoritative for curated additions. Existing public URLs already
mapped in source-file-index.json are retained. A clearly labeled institutional
collection fallback is added only when no case-specific public endpoint exists.
"""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import quote_plus, urlparse

ROOT = Path(__file__).resolve().parent
ATLAS = ROOT / "atlas-data.json"
INDEX = ROOT / "source-file-index.json"
MANIFEST = ROOT / "public-source-manifest.json"
VIDEO_MANIFEST = ROOT / "video-source-manifest.json"

COLLECTIONS = {
    "nara-uap": {
        "label": "NARA — UAP records research portal",
        "url": "https://www.archives.gov/research/topics/uaps",
        "publisher": "National Archives and Records Administration",
        "access": "Public",
        "scope": "collection",
        "note": "Official collection guide; search by case name, date, or source locator.",
    },
    "nara-bluebook": {
        "label": "NARA — Project BLUE BOOK records",
        "url": "https://www.archives.gov/research/military/air-force/ufos",
        "publisher": "National Archives and Records Administration",
        "access": "Public",
        "scope": "collection",
        "note": "Official Project BLUE BOOK guide; search by location and incident date.",
    },
    "war-ufo": {
        "label": "War Department — UFO records releases",
        "url": "https://www.war.gov/ufo",
        "publisher": "U.S. Department of War",
        "access": "Public; site may block automated clients",
        "scope": "collection",
        "note": "Official release portal; search by the DOW/DOE/FBI/CIA/ODNI source ID shown above.",
    },
    "nasa-ntrs": {
        "label": "NASA Technical Reports Server",
        "url": "https://ntrs.nasa.gov/",
        "publisher": "NASA",
        "access": "Public",
        "scope": "collection",
        "note": "Official NASA technical archive; search by mission and document title.",
    },
}

def unique(rows):
    out, seen = [], set()
    for row in rows:
        url = row.get("url", "").strip()
        if not url or url in seen:
            continue
        seen.add(url)
        out.append(row)
    return out


def url_record(url: str) -> dict:
    host = urlparse(url).netloc.lower().removeprefix("www.")
    rules = [
        ("war.gov", "War Department — official public record", "U.S. Department of War", "official-record"),
        ("defense.gov", "Department of Defense — official public record", "U.S. Department of Defense", "official-record"),
        ("aaro.mil", "AARO — official UAP record", "All-domain Anomaly Resolution Office", "official-record"),
        ("dvidshub.net", "DVIDS — official media record", "Defense Visual Information Distribution Service", "official-record"),
        ("archives.gov", "NARA — official archival record", "National Archives and Records Administration", "official-record"),
        ("cia.gov", "CIA Reading Room — declassified record", "Central Intelligence Agency", "official-record"),
        ("nsa.gov", "NSA — declassified record", "National Security Agency", "official-record"),
        ("dtic.mil", "DTIC — official technical report", "Defense Technical Information Center", "official-record"),
        ("congress.gov", "Congress.gov — hearing or legislative record", "U.S. Congress", "official-record"),
        ("govinfo.gov", "GovInfo — official government publication", "U.S. Government Publishing Office", "official-record"),
        ("nasa.gov", "NASA — official mission record", "NASA", "official-record"),
        ("ntrs.nasa.gov", "NASA NTRS — official technical record", "NASA", "official-record"),
        ("bac-lac.gc.ca", "Library and Archives Canada — archival record", "Library and Archives Canada", "official-record"),
        ("nationalarchives.gov.uk", "UK National Archives — archival record", "The National Archives (UK)", "official-record"),
        ("sian.an.gov.br", "Brazilian National Archives — archival record", "Arquivo Nacional (Brazil)", "official-record"),
        ("documentcloud.org", "DocumentCloud — public document copy", "DocumentCloud", "public-mirror"),
        ("archive.org", "Internet Archive — public archival copy", "Internet Archive", "public-mirror"),
        ("fold3.com", "Fold3 — digitized archival record", "Fold3", "archive-licensed"),
        ("theblackvault.com", "The Black Vault — FOIA document mirror", "The Black Vault", "public-mirror"),
        ("cufos.org", "CUFOS — research archive", "Center for UFO Studies", "institutional-archive"),
        ("cobeps.org", "COBEPS — research report", "COBEPS", "institutional-archive"),
        ("commons.wikimedia.org", "Wikimedia Commons — public media record", "Wikimedia Commons", "public-mirror"),
    ]
    for needle, label, publisher, scope in rules:
        if needle in host:
            return {"label": label, "url": url, "publisher": publisher, "access": "Public", "scope": scope}
    return {"label": f"Public source — {host}", "url": url, "publisher": host, "access": "Public/access unverified", "scope": "public-source"}


def source_tokens(case, index):
    text = " ".join(case.get("sources", [])).upper()
    return [token for token in index if token.upper() in text]


def fallback_for(case, tokens):
    cid = case["id"]
    joined = " ".join(tokens + case.get("sources", [])).upper()
    if cid.startswith("BF-NASA-") or "NASA-UAP" in joined:
        row = dict(COLLECTIONS["nasa-ntrs"])
        row["url"] = f"https://ntrs.nasa.gov/search?q={quote_plus(case['title'])}"
        row["label"] = f"NASA NTRS — search: {case['title']}"
        return row
    if any(tag in joined for tag in ("DOW-UAP", "DOE-UAP", "FBI-UAP", "FBI-SERIAL", "CIA-UAP", "ODNI-UAP", "ICA-UAP", "GULF2020", "GREECE2023")):
        return dict(COLLECTIONS["war-ufo"])
    if case.get("year", 9999) <= 1969 or any(tag in joined for tag in ("BLUE BOOK", "PROJECT SIGN", "PROJECT GRUDGE")):
        return dict(COLLECTIONS["nara-bluebook"])
    return dict(COLLECTIONS["nara-uap"])


def main():
    atlas = json.loads(ATLAS.read_text())
    index = json.loads(INDEX.read_text())
    manifest = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}
    video_manifest = json.loads(VIDEO_MANIFEST.read_text()) if VIDEO_MANIFEST.exists() else {}
    for case in atlas["cases"]:
        tokens = source_tokens(case, index)
        # Curated videos lead the public drawer, but remain explicitly labeled as
        # witness interviews or contextual analysis rather than primary evidence.
        rows = list(video_manifest.get(case["id"], []))
        rows.extend(manifest.get(case["id"], []))
        for token in tokens:
            for path in index.get(token, []):
                if isinstance(path, str) and path.startswith(("http://", "https://")):
                    rows.append(url_record(path))
        # Keep public links embedded in the lead visual even if source-token mapping missed them.
        hero = case.get("heroVisual") or {}
        for key in ("sourceUrl", "mediaUrl"):
            value = hero.get(key)
            if isinstance(value, str) and value.startswith(("http://", "https://")):
                rows.append(url_record(value))
        rows = unique(rows)
        if not rows:
            rows.append(fallback_for(case, tokens))
        case["publicSources"] = rows[:8]
    ATLAS.write_text(json.dumps(atlas, indent=2, ensure_ascii=False) + "\n")
    missing = [c["id"] for c in atlas["cases"] if not c.get("publicSources")]
    print(json.dumps({"cases": len(atlas["cases"]), "covered": len(atlas["cases"]) - len(missing), "missing": missing}, indent=2))

if __name__ == "__main__":
    main()
