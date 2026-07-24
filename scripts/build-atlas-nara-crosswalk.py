#!/usr/bin/env python3
"""Build a conservative 145-case Atlas-to-NARA reconciliation crosswalk.

Exact mappings require an explicit NAID/catalog identifier in Atlas data, the
source index, or a case-linked local manifest. Title/location matches from the
sampled AISS inventory are leads only and never promoted to exact mappings.
"""
from __future__ import annotations

import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
NARA = PROJECT / "nara-rg615"
ATLAS_PATH = ROOT / "atlas-data.json"
INDEX_PATH = ROOT / "source-file-index.json"
COVERAGE_PATH = ROOT / "qa" / "all-cases-final-source-coverage.json"
OUT_JSON = ROOT / "research" / "atlas-nara-crosswalk-2026-07-22.json"
OUT_MD = ROOT / "research" / "atlas-nara-crosswalk-2026-07-22.md"

NAID_RE = re.compile(r"(?i)(?:NAID[-_ :]*|catalog\.archives\.gov/(?:id/)?)(\d{5,12})")
STOP = {
    "case", "file", "report", "reports", "object", "objects", "unidentified",
    "flying", "incident", "sighting", "sightings", "project", "special", "unknown",
    "united", "states", "exact", "location", "county", "city", "near", "area",
    "historical", "aerial", "force", "base", "station", "airport", "international",
    "north", "south", "east", "west", "visual", "radar", "aircraft", "coast",
}
SERIES_NAIDS = {"595466", "597821"}

# The first tranche is deliberately curated rather than blindly taking the
# arithmetic score. It favors consequential cases with identifiable official
# record systems and avoids spending a NARA sprint on primarily private,
# foreign-only, or document-context entries.
FOCUS_ORDER = [
    "BF-1948-MT-01",  # Mantell — Blue Book + accident/operations records
    "BF-1944-FF-01",  # Foo Fighters — AAF unit intelligence and combat records
    "BF-1946-GR-01",  # Ghost Rockets — State/air-intelligence + Swedish records
    "BF-1950-GF-01",  # Great Falls — Blue Book film-analysis packet
    "BF-1952-TM-01",  # Tremonton — Navy film + Blue Book analysis
    "BF-1956-LB-01",  # Lakenheath — Blue Book radar/visual case file
    "BF-1965-KB-01",  # Kecksburg — USAF/NASA/FBI record classes
    "BF-1948-AZ-01",  # Aztec — FBI/Blue Book record trail and disinformation test
    "BF-1953-RP-00",  # Robertson Panel — exact CIA record/package reconciliation
    "BF-1966-WS-01",  # Westall — RAAF/Australian archival recovery
]

ARCHIVE_TARGETS = {
    "BF-1948-MT-01": "RG 341 Project Blue Book file; Kentucky ANG/USAF accident, flight and operations records",
    "BF-1944-FF-01": "AAF unit intelligence summaries, combat mission reports and theater histories in Air Force/Army record groups",
    "BF-1946-GR-01": "State Department diplomatic reporting, U.S. air-intelligence records and Swedish military archives",
    "BF-1950-GF-01": "RG 341 Project Blue Book case file, original film-analysis correspondence and technical reports",
    "BF-1952-TM-01": "RG 341 Project Blue Book case file, U.S. Navy film custody and contractor analysis records",
    "BF-1956-LB-01": "RG 341 Project Blue Book case file, USAF/RAF radar logs and communications record classes",
    "BF-1965-KB-01": "USAF Blue Book, NASA search records, FBI correspondence and recovery/transport record classes",
    "BF-1948-AZ-01": "FBI correspondence, Project Blue Book references and records needed to test the hoax/disinformation account",
    "BF-1953-RP-00": "CIA Robertson Panel package, missing appendices/restricted documents and distribution records",
    "BF-1966-WS-01": "RAAF and Australian National Archives records; NARA only for any U.S. liaison/circulation copies",
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def uniq(items):
    out, seen = [], set()
    for item in items:
        if item is None:
            continue
        item = str(item).strip()
        if item and item not in seen:
            seen.add(item)
            out.append(item)
    return out


def source_haystack(case):
    parts = [case.get("sourceLocator", ""), *(case.get("sources") or [])]
    for row in case.get("sourceRecords") or []:
        if isinstance(row, dict):
            parts.extend(row.get(k, "") for k in ("citation", "provenance", "locator"))
    return " ".join(map(str, parts))


def related_index_paths(case, index):
    haystack = source_haystack(case).lower()
    locator = str(case.get("sourceLocator", "")).strip()
    tokens = [locator] if locator in index else [token for token in index if token.lower() in haystack]
    paths = [item for token in tokens for item in index[token]]
    return tokens, uniq(paths)


def direct_assets(case):
    rows = [case.get("image"), *(case.get("images") or [])]
    hero = case.get("heroVisual") or {}
    if isinstance(hero, dict):
        rows.extend(hero.get(k) for k in ("src", "sourceUrl", "mediaUrl"))
    rows.extend(
        row.get("url") for row in (case.get("publicSources") or []) if isinstance(row, dict)
    )
    return uniq(rows)


def local_case_files(paths):
    files = []
    evidence_dirs = set()
    for item in paths:
        if item.startswith(("http://", "https://")):
            continue
        path = Path(item)
        if not path.is_absolute():
            path = ROOT / path
        if path.exists() and path.is_file():
            files.append(path)
        try:
            rel = path.relative_to(ROOT / "assets" / "evidence")
            if rel.parts:
                evidence_dirs.add(ROOT / "assets" / "evidence" / rel.parts[0])
        except ValueError:
            pass
    for folder in evidence_dirs:
        if folder.exists():
            files.extend(p for p in folder.rglob("*") if p.is_file())
    return list(dict.fromkeys(files))


def extract_naids(case, paths, files):
    material = [json.dumps(case, ensure_ascii=False), *paths]
    for path in files:
        material.append(path.name)
        if path.suffix.lower() in {".json", ".md", ".txt", ".csv"} and path.stat().st_size <= 2_000_000:
            try:
                material.append(path.read_text(encoding="utf-8", errors="ignore"))
            except OSError:
                pass
    return sorted(set(NAID_RE.findall("\n".join(material))), key=int)


def tokens(text):
    return {
        word for word in re.findall(r"[a-z0-9]+", text.lower())
        if len(word) >= 4 and not word.isdigit() and word not in STOP
    }


def aiss_leads(case, aiss):
    year = str(case.get("year", ""))
    if not year or int(year) > 1969:
        return []
    case_terms = tokens(f"{case.get('title', '')} {case.get('location', '')}")
    if not case_terms:
        return []
    scored = []
    seen_naids = set()
    for row in aiss:
        title = row.get("title", "")
        if year not in title:
            continue
        overlap = sorted(case_terms & tokens(title))
        if not overlap:
            continue
        # Leads require a distinctive geographic/name overlap; year alone never counts.
        score = len(overlap)
        naid = str(row.get("naId"))
        if score >= 2 and naid not in seen_naids:
            seen_naids.add(naid)
            scored.append((score, overlap, row))
    scored.sort(key=lambda x: (-x[0], x[2].get("title", "")))
    return [
        {
            "naid": str(row.get("naId")),
            "title": row.get("title"),
            "objects": row.get("objects"),
            "matchedTerms": overlap,
            "confidence": "candidate-lead-only",
        }
        for _, overlap, row in scored[:3]
    ]


def missing_classes(case):
    classes = []
    for row in case.get("sourceRecords") or []:
        if isinstance(row, dict):
            classes.extend(row.get("limitations") or [])
    return uniq(classes)


def upgrade_score(case, exact_naids, local_files, public_urls):
    score, reasons = 0, []
    records = case.get("sourceRecords") or []
    if len(records) <= 1:
        score += 3
        reasons.append("one structured source record")
    if any(not (r.get("supports") or []) for r in records if isinstance(r, dict)):
        score += 2
        reasons.append("empty supports field")
    if any(not (r.get("limitations") or []) for r in records if isinstance(r, dict)):
        score += 2
        reasons.append("empty limitations field")
    if not exact_naids and case.get("year", 9999) <= 1969:
        score += 3
        reasons.append("historical case lacks exact NAID")
    if not any(path.suffix.lower() == ".pdf" for path in local_files):
        score += 2
        reasons.append("no complete local PDF in mapped custody")
    if not exact_naids and any("archives.gov" in url for url in public_urls):
        score += 2
        reasons.append("NARA collection/guide link only")
    quote_conf = str(case.get("quoteConfidence", "")).lower()
    if any(word in quote_conf for word in ("summary", "secondary", "unverified")):
        score += 2
        reasons.append("quote not verified to primary page")
    significance = str(case.get("significance", "")).lower()
    if "high" in significance or "critical" in significance:
        score += 1
        reasons.append("high-significance dossier")
    if exact_naids:
        score -= 2
    return score, reasons


def main():
    atlas = load(ATLAS_PATH)
    index = load(INDEX_PATH)
    coverage = {row["id"]: row for row in load(COVERAGE_PATH)} if COVERAGE_PATH.exists() else {}
    rg615_doc = load(NARA / "rg615_inventory.json")
    rg615 = {str(row["naid"]): row for row in rg615_doc["records"]}
    aiss = load(NARA / "aiss_case_inventory_full.json")
    aiss_by_id = {str(row["naId"]): row for row in aiss}
    unknown = load(NARA / "unknown_case_database.json")
    unknown_by_id = {str(row["naId"]): row for row in unknown}

    rows = []
    for case in atlas["cases"]:
        index_tokens, indexed_paths = related_index_paths(case, index)
        paths = uniq([*indexed_paths, *direct_assets(case)])
        files = local_case_files(paths)
        naids = extract_naids(case, paths, files)
        item_naids = [naid for naid in naids if naid not in SERIES_NAIDS]
        public_urls = [p for p in paths if p.startswith(("http://", "https://"))]
        local_paths = [str(p) for p in files]
        resolved = []
        record_groups = set()
        for naid in naids:
            if naid in rg615:
                rec = rg615[naid]
                record_groups.add(615)
                resolved.append({"naid": naid, "recordGroup": 615, "title": rec.get("title"), "series": rec.get("series"), "access": rec.get("access"), "digitalObjectCount": len(rec.get("digital_objects") or [])})
            elif naid in aiss_by_id:
                rec = aiss_by_id[naid]
                record_groups.add(341)
                resolved.append({"naid": naid, "recordGroup": 341, "title": rec.get("title"), "series": "4602D AISS field files", "access": "online object set", "digitalObjectCount": rec.get("objects")})
            elif naid in unknown_by_id:
                rec = unknown_by_id[naid]
                record_groups.add(341)
                resolved.append({"naid": naid, "recordGroup": 341, "title": rec.get("title"), "series": "Project Blue Book case files", "access": "online object set", "digitalObjectCount": rec.get("objects")})
            elif naid in SERIES_NAIDS:
                record_groups.add(341)
                resolved.append({"naid": naid, "recordGroup": 341, "title": "Project Blue Book series", "series": "series-level identifier", "access": "catalog series", "digitalObjectCount": None})
            else:
                resolved.append({"naid": naid, "recordGroup": None, "title": None, "series": None, "access": "explicit NAID; metadata not present in local inventories", "digitalObjectCount": None})

        has_nara_guide = any("archives.gov" in url for url in public_urls)
        if item_naids:
            status = "exact-naid"
        elif naids:
            status = "series-level-only"
        elif has_nara_guide:
            status = "collection-guide-only"
        else:
            status = "no-exact-nara-mapping"
        leads = [] if item_naids else aiss_leads(case, aiss)
        score, reasons = upgrade_score(case, item_naids, files, public_urls)
        row = {
            "caseId": case["id"],
            "title": case["title"],
            "year": case.get("year"),
            "sourceLocator": case.get("sourceLocator"),
            "mappingStatus": status,
            "exactNaids": item_naids,
            "seriesNaids": [naid for naid in naids if naid in SERIES_NAIDS],
            "recordGroups": sorted(record_groups),
            "resolvedNaraRecords": resolved,
            "candidateAissLeads": leads,
            "sourceIndexTokens": index_tokens,
            "structuredSourceRecords": len(case.get("sourceRecords") or []),
            "publicUrlCount": len(public_urls),
            "localCustodyFileCount": len(files),
            "localPdfCount": sum(path.suffix.lower() == ".pdf" for path in files),
            "coverageLinks": coverage.get(case["id"], {}).get("links"),
            "missingRecordClasses": missing_classes(case),
            "upgradePriorityScore": score,
            "upgradeReasons": reasons,
        }
        rows.append(row)

    status_counts = Counter(row["mappingStatus"] for row in rows)
    by_id = {row["caseId"]: row for row in rows}
    top10 = [by_id[case_id] for case_id in FOCUS_ORDER]
    for row in top10:
        row["archiveTarget"] = ARCHIVE_TARGETS[row["caseId"]]
    output = {
        "generatedAt": datetime.now().astimezone().isoformat(timespec="seconds"),
        "method": {
            "exactRule": "Explicit NAID/catalog identifier in case data, source index, or case-linked local manifest/file name.",
            "candidateRule": "Same-year distinctive token overlap against the sampled 4602D AISS inventory; leads are never promoted to exact mappings.",
            "warning": "unknown_case_database.json is not used for candidate generation because printed ATIC Form 329 checkbox text creates false positives.",
        },
        "caseCount": len(rows),
        "statusCounts": dict(status_counts),
        "exactMappedCaseCount": sum(bool(row["exactNaids"]) for row in rows),
        "candidateLeadCaseCount": sum(bool(row["candidateAissLeads"]) for row in rows),
        "top10SelectionMethod": "Curated NARA-first tranche using significance, official-record tractability, local custody gaps and missing-record value; arithmetic score retained as a secondary triage signal.",
        "top10UpgradeCaseIds": [row["caseId"] for row in top10],
        "cases": rows,
    }
    OUT_JSON.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = [
        "# Atlas-to-NARA Evidence Crosswalk",
        "",
        f"**Generated:** {output['generatedAt']}",
        f"**Atlas cases:** {len(rows)}",
        f"**Exact NAID mappings:** {output['exactMappedCaseCount']}",
        f"**Cases with candidate AISS leads:** {output['candidateLeadCaseCount']}",
        "",
        "## Mapping-status summary",
        "",
        "| Status | Cases |",
        "|---|---:|",
    ]
    lines.extend(f"| {status} | {count} |" for status, count in sorted(status_counts.items()))
    lines += [
        "",
        "## First 10 evidence-depth upgrades",
        "",
        "| Rank | Case | Year | Score | Current NARA status | Primary reasons |",
        "|---:|---|---:|---:|---|---|",
    ]
    for rank, row in enumerate(top10, 1):
        reasons = "; ".join(row["upgradeReasons"])
        target = row["archiveTarget"]
        lines.append(f"| {rank} | `{row['caseId']}` — {row['title']} | {row['year']} | {row['upgradePriorityScore']} | {row['mappingStatus']} | {reasons}; **target:** {target} |")
    lines += [
        "",
        "## Interpretation rules",
        "",
        "- **Exact NAID** means the identifier is explicit in a case-linked record, path, URL or manifest. It does not prove every claim in the underlying document.",
        "- **Series-level only** means the Atlas reaches a NARA series but not the exact event file unit.",
        "- **Collection-guide only** means the current public link is an archive guide/search portal, not a case-level catalog record.",
        "- **Candidate AISS lead** is a research lead based on same-year distinctive-title/location overlap. It requires record-level review before citation.",
        "- The prior `unknown_case_database.json` is excluded from candidate matching because “Unknown” appears as printed checkbox text on ATIC forms and creates mass false positives.",
        "",
        "## Machine-readable output",
        "",
        f"`{OUT_JSON.relative_to(ROOT)}` contains all {len(rows)} rows, resolved local-inventory metadata, local custody counts, candidate leads, missing-record classes and upgrade scores.",
    ]
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({
        "caseCount": len(rows),
        "statusCounts": dict(status_counts),
        "exactMappedCaseCount": output["exactMappedCaseCount"],
        "candidateLeadCaseCount": output["candidateLeadCaseCount"],
        "top10": output["top10UpgradeCaseIds"],
        "json": str(OUT_JSON),
        "markdown": str(OUT_MD),
    }, indent=2))


if __name__ == "__main__":
    main()
