#!/usr/bin/env python3
"""Apply Priority 4 public-record recoveries and preserve negative findings."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ATLAS = ROOT / "atlas-data.json"
INDEX = ROOT / "source-file-index.json"
MANIFEST = ROOT / "public-source-manifest.json"
RESEARCH = ROOT / "research"
DATE = "2026-07-24"


def dump(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def add_unique(rows: list[dict], row: dict, key: str) -> None:
    if not any(item.get(key) == row.get(key) for item in rows):
        rows.append(row)


atlas = json.loads(ATLAS.read_text())
by_id = {case["id"]: case for case in atlas["cases"]}

# Ghost Rockets: the official archive topic is verified; the Internet Archive
# corpus is retained only as an unverified scan lead, never laundered as custody.
ghost = by_id["BF-1946-GR-01"]
ghost["sourceQuality"] = (
    "Official Riksarkivet topic and internal order citation verified; item-level shelfmark and scan-to-record mapping remain incomplete."
)
for row in [
    {
        "label": "Riksarkivet — Spökraketer archive topic",
        "url": "https://riksarkivet.se/resurser/spokraketer",
        "publisher": "Riksarkivet (Swedish National Archives)",
        "access": "Public",
        "scope": "official-archive-topic",
        "note": "Official archive context; not an item-level catalog record or complete packet."
    },
    {
        "label": "Internet Archive — Swedish Ghost Rockets scan corpus",
        "url": "https://archive.org/details/SwedishGhostRockets",
        "publisher": "Internet Archive / private uploader",
        "access": "Public; Public Domain Mark asserted by uploader",
        "scope": "unverified-scan-corpus-lead",
        "note": "1,779 original PDF files are publicly listed, but uploader identity, archival order, and item-level custody mapping are unverified; lead only."
    },
]:
    add_unique(ghost.setdefault("publicSources", []), row, "url")

ghost["gap"] = (
    "Still needed: an item-level Riksarkivet/Krigsarkivet shelfmark, first-generation scan provenance, and any exact RG 59 diplomatic reporting. "
    "A large Internet Archive scan corpus is preserved as a lead only until its internal markings can be mapped to official custody."
)

# Kecksburg: recover the federal court opinion as a primary legal record. It
# proves the FOIA dispute and search inadequacy finding, not the object narrative.
kecksburg = by_id["BF-1965-KB-01"]
add_unique(kecksburg.setdefault("sourceRecords", []), {
    "citation": "Kean v. National Aeronautics and Space Administration, 480 F. Supp. 2d 150 (D.D.C. 2007).",
    "sourceType": "federal-court-opinion",
    "provenance": "United States District Court for the District of Columbia; public opinion copy via CourtListener",
    "locator": "480 F. Supp. 2d 150 · Civil Action No. 03-2500",
    "supports": [
        "A January 31, 2003 FOIA request sought NASA records concerning the December 9, 1965 Kecksburg incident",
        "The court found NASA had not yet carried its burden to demonstrate an adequate search at the summary-judgment stage",
        "The public-record dispute is documented independently of the later UFO narrative"
    ],
    "limitations": [
        "The opinion does not establish that an anomalous object was recovered",
        "It does not supply Army recovery logs or a physical chain of custody",
        "Later search results must be evaluated separately"
    ]
}, "locator")
add_unique(kecksburg.setdefault("publicSources", []), {
    "label": "Kean v. NASA — 2007 federal court opinion",
    "url": "https://www.courtlistener.com/opinion/2487204/kean-v-national-aeronautics-and-space-admin/",
    "publisher": "CourtListener / U.S. District Court opinion",
    "access": "Public",
    "scope": "primary-legal-record",
    "note": "Documents the Kecksburg FOIA litigation and adequacy-of-search dispute; does not prove a recovery."
}, "url")
kecksburg["sourceQuality"] = "Primary federal-court record for the NASA FOIA dispute; underlying incident and recovery packet remain unrecovered."
kecksburg["gap"] = (
    "Still needed: original Army/local-response logs, NASA technical records tied to the event, and any recovery/transport chain. "
    "The 2007 court opinion confirms a records-search dispute but does not validate the recovery narrative."
)

# Aztec: recover the contemporaneous exposé/follow-up and the FBI Newton file
# collection as direct contradiction records.
aztec = by_id["BF-1948-AZ-01"]
aztec_records = [
    {
        "citation": "J. P. Cahn, ‘The Flying Saucers and the Mysterious Little Men,’ True, September 1952, 14-page scan.",
        "sourceType": "contemporaneous-investigative-article",
        "provenance": "True magazine; public scan hosted by Southern Methodist University",
        "locator": "Cahn1.pdf · 14 pages",
        "supports": [
            "Contemporaneous investigation of the Scully/Newton/Gebauer claim chain",
            "The article states that True and Cahn tracked the alleged Venus-craft story across five western states",
            "Direct period source for the fraud/hoax classification"
        ],
        "limitations": [
            "Investigative journalism, not a court judgment or complete agency file",
            "The public host is an academic mirror rather than the magazine publisher"
        ]
    },
    {
        "citation": "J. P. Cahn, ‘Flying Saucer Swindlers,’ True, August 1956, 6-page scan.",
        "sourceType": "contemporaneous-investigative-follow-up",
        "provenance": "True magazine; public scan hosted by Southern Methodist University",
        "locator": "Cahn2.pdf · 6 pages",
        "supports": [
            "Period follow-up linking Newton and Gebauer’s saucer story to their fraudulent business activity",
            "Provides the published basis for treating Aztec as a contradiction/hoax calibration case"
        ],
        "limitations": [
            "Investigative journalism, not a substitute for the underlying court exhibits",
            "The public host is an academic mirror"
        ]
    },
    {
        "citation": "FBI Records: The Vault — Silas M. Newton, six-part released file collection.",
        "sourceType": "federal-investigative-file-collection",
        "provenance": "Federal Bureau of Investigation, The Vault",
        "locator": "vault.fbi.gov/silas-newton · Parts 01–06",
        "supports": [
            "Official FBI custody for investigations into Newton’s fraudulent activities",
            "Confirms Newton was cited as an authority in Scully’s crashed-saucer account"
        ],
        "limitations": [
            "The collection concerns Newton broadly and is not itself an Aztec crash-investigation packet",
            "Page-level Aztec citations still require a dedicated file review"
        ]
    }
]
for row in aztec_records:
    add_unique(aztec.setdefault("sourceRecords", []), row, "locator")
for row in [
    {
        "label": "J. P. Cahn — The Flying Saucers and the Mysterious Little Men (1952)",
        "url": "https://www.physics.smu.edu/~pseudo/UFOs/Scully/Cahn1.pdf",
        "publisher": "True magazine scan / Southern Methodist University host",
        "access": "Public",
        "scope": "contemporaneous-investigative-source"
    },
    {
        "label": "J. P. Cahn — Flying Saucer Swindlers (1956)",
        "url": "https://www.physics.smu.edu/pseudo/UFOs/Scully/Cahn2.pdf",
        "publisher": "True magazine scan / Southern Methodist University host",
        "access": "Public",
        "scope": "contemporaneous-investigative-follow-up"
    },
    {
        "label": "FBI Vault — Silas M. Newton file collection",
        "url": "https://vault.fbi.gov/silas-newton",
        "publisher": "Federal Bureau of Investigation",
        "access": "Public",
        "scope": "primary-federal-record-collection"
    },
]:
    add_unique(aztec.setdefault("publicSources", []), row, "url")
aztec["sourceQuality"] = "Contemporaneous Cahn exposé/follow-up plus official FBI Newton file custody; no extraordinary-object evidence recovered."
aztec["keyQuote"] = (
    "Back in 1952, the September issue of TRUE ran a story of mine titled The Flying Saucers and the Mysterious Little Men. "
    "It was an exposé of a best-selling book that maintained flying saucers from Venus, manned by 3-foot characters in blue suits, had landed on earth."
)
aztec["quoteSource"] = "J. P. Cahn, ‘Flying Saucer Swindlers,’ True, August 1956, page 36 (visually verified against scan)."
aztec["quoteConfidence"] = "High — visually verified contemporaneous publication; establishes Cahn’s exposé claim, not a judicial finding."
aztec["summary"] = (
    "The Aztec crash story entered print through Frank Scully’s 1950 book and claims supplied by Silas Newton and Leo Gebauer. "
    "Cahn’s 1952 investigation and 1956 follow-up directly challenged the story and connected its promoters to fraudulent business activity; the FBI’s released Newton files independently document that fraud-investigation context."
)
aztec["official"] = (
    "No verified government crash-retrieval file or physical evidence supports an Aztec recovery. The documentary record instead supports treating the story as a hoax/fraud boundary case."
)
aztec["gap"] = (
    "The decisive next records are page-level FBI citations and original Newton/GeBauer court exhibits. Their absence does not rescue the crash claim; it limits how precisely the fraud chain can be reconstructed."
)
aztec_assets = [
    "assets/evidence/AZTEC-1948/AZTEC-1948-Cahn-1952-True-p1.png",
    "assets/evidence/AZTEC-1948/AZTEC-1948-Cahn-1956-True-p1.png"
]
aztec["heroVisual"] = {
    "src": aztec_assets[0],
    "caption": "Opening spread of J. P. Cahn’s 1952 True investigation, visually verified from the public scan.",
    "alt": "Opening spread of The Flying Saucers and the Mysterious Little Men by J. P. Cahn",
    "rights": "Documentary excerpt used for source criticism; magazine copyright status not asserted",
    "visualType": "document-excerpt",
    "mediaType": "image"
}
aztec["image"] = aztec_assets[0]
aztec["images"] = list(dict.fromkeys(aztec_assets + aztec.get("images", [])))

# Synchronize indexes/manifests.
index = json.loads(INDEX.read_text())
index.setdefault("AZTEC-1948", [])
index["AZTEC-1948"] = list(dict.fromkeys(index["AZTEC-1948"] + aztec_assets))
manifest = json.loads(MANIFEST.read_text())
manifest_by_id = {item.get("id") or item.get("caseId"): item for item in manifest.get("cases", [])}
for cid in ["BF-1946-GR-01", "BF-1965-KB-01", "BF-1948-AZ-01"]:
    if cid in manifest_by_id:
        manifest_by_id[cid]["publicSources"] = by_id[cid].get("publicSources", [])

queue = {
    "generated": DATE,
    "scope": "Existing Atlas cases only; public sources and existing local records; no outreach or archival requests.",
    "cases": [
        {
            "caseId": "BF-1946-GR-01", "title": ghost["title"], "status": "lead-recovered-not-promoted",
            "recovered": ["Official Riksarkivet Spökraketer topic", "Internet Archive corpus: 1,779 original PDFs, 895,871,795 bytes; private uploader; Public Domain Mark asserted"],
            "negativeFindings": ["No item-level Riksarkivet shelfmark recovered", "No scan-to-shelfmark mapping verified", "No exact NARA RG 59 diplomatic file identified"],
            "next": "Map internal markings from a small corpus sample to Riksarkivet custody before promoting any scan as primary evidence."
        },
        {
            "caseId": "BF-1944-FF-01", "title": by_id["BF-1944-FF-01"]["title"], "status": "exact-custody-no-scans",
            "recovered": ["AFHRA IRIS 60059, call SQ-FI-415-HI, reel 848, frames 1519–1631", "IRIS 60074, reel 848, frames 1763–1867", "IRIS 1026183, reel 33170, frame 886 onward"],
            "negativeFindings": ["No public original microfilm images recovered", "Current quotation remains transcription-dependent"],
            "next": "Retain exact AFHRA identifiers and wait for a public reel scan; do not promote transcriptions to image-verified status."
        },
        {
            "caseId": "BF-1966-WS-01", "title": by_id["BF-1966-WS-01"]["title"], "status": "institutional-context-only",
            "recovered": ["State Library Victoria archival review", "Kingston Local History institutional article"],
            "negativeFindings": ["No exact NAA item for Westall located", "Tested A9755/22 public PDF contains no Westall, Clayton, school, or April 1966 match", "No RAAF, police, or school administrative packet recovered"],
            "next": "Preserve the negative search; keep press/library material as occurrence context, not official-case custody."
        },
        {
            "caseId": "BF-1965-KB-01", "title": kecksburg["title"], "status": "primary-legal-record-recovered",
            "recovered": ["Kean v. NASA, 480 F. Supp. 2d 150 (D.D.C. 2007), Civil Action No. 03-2500"],
            "negativeFindings": ["No Army recovery/transport record located", "No NASA technical event packet recovered", "Court opinion documents FOIA search adequacy, not object identity"],
            "next": "Use the court opinion as the legal-record anchor and keep recovery claims explicitly unproven."
        },
        {
            "caseId": "BF-1948-AZ-01", "title": aztec["title"], "status": "contradiction-record-upgraded",
            "recovered": ["Cahn 1952 True article, 14-page scan", "Cahn 1956 True follow-up, 6-page scan", "FBI Vault Silas Newton six-part file collection"],
            "negativeFindings": ["No government crash-retrieval file located", "No physical evidence located", "FBI collection still needs page-level Aztec indexing"],
            "next": "Review the FBI Newton PDFs for page-level Aztec/Scully references and court exhibits; the extraordinary claim remains contradicted."
        }
    ]
}

RESEARCH.mkdir(exist_ok=True)
dump(RESEARCH / "public-record-recovery-queue-2026-07-24.json", queue)
md = [
    "# UAP Atlas — Public-Record Recovery Queue", "", "**Date:** July 24, 2026", "",
    "> Scope: existing Atlas cases, existing local records, and public sources only. No FOIA, outreach, archival request, or new-case acquisition.", "",
    "| Case | Status | Recovered | Record gap |", "|---|---|---|---|"
]
for item in queue["cases"]:
    md.append(f"| `{item['caseId']}` — {item['title']} | {item['status']} | {'; '.join(item['recovered'])} | {'; '.join(item['negativeFindings'])} |")
md += ["", "## Handling rule", "", "Public availability is not custody. Private uploads and mirror scans remain leads until internal markings, completeness, and official archival identity are verified.", ""]
(RESEARCH / "public-record-recovery-queue-2026-07-24.md").write_text("\n".join(md))

dump(ATLAS, atlas)
dump(INDEX, index)
dump(MANIFEST, manifest)
print("Priority 4 recoveries applied; queue written for 5 cases.")
