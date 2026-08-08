#!/usr/bin/env python3
"""Generate current Atlas data and source-coverage QA artifacts."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QA = ROOT / "qa"
QA.mkdir(exist_ok=True)
atlas = json.loads((ROOT / "atlas-data.json").read_text())
index = json.loads((ROOT / "source-file-index.json").read_text())
cases = atlas["cases"]
events = atlas.get("timeline") or atlas.get("timelineEvents") or []
normalized = ["caseTypes", "evidenceModes", "environment", "outcome", "confidenceModel", "temporal", "geospatial", "sourceRecords", "phenomena", "observation"]

def unique_strings(items):
    return list(dict.fromkeys(item for item in items if isinstance(item, str) and item.strip()))


def source_haystack(case):
    """Return only source-identifying text, avoiding broad case-body false matches."""
    parts = [str(case.get("sourceLocator", "")), *map(str, case.get("sources", []))]
    for record in case.get("sourceRecords", []) or []:
        if not isinstance(record, dict):
            continue
        parts.extend(str(record.get(field, "")) for field in ("citation", "provenance", "locator"))
    return " ".join(parts).lower()


def evidence_assets(case):
    assets = [case.get("image"), *(case.get("images", []) or []), *(case.get("evidenceImages", []) or [])]
    hero = case.get("heroVisual") or {}
    if isinstance(hero, dict):
        assets.append(hero.get("src"))
    return unique_strings(assets)


def public_urls(case):
    urls = []
    for record in case.get("publicSources", []) or []:
        if isinstance(record, dict):
            urls.append(record.get("url"))
    for record in case.get("sourceRecords", []) or []:
        if isinstance(record, dict):
            urls.extend(record.get(field) for field in (
                "url", "sourceUrl", "publicUrl", "archiveUrl", "recordUrl", "mediaUrl", "downloadUrl"
            ))
    hero = case.get("heroVisual") or {}
    if isinstance(hero, dict):
        urls.extend(hero.get(field) for field in ("sourceUrl", "mediaUrl"))
    return unique_strings(url for url in urls if isinstance(url, str) and url.startswith(("http://", "https://")))


def source_family(record):
    """Coarse origin family; repeated pages from one packet are not independent sources."""
    text = " ".join(str(record.get(field, "")) for field in ("sourceType", "provenance", "citation")).lower()
    families = (
        ("fbi", ("federal bureau of investigation", " fbi")),
        ("civil-aviation", ("civil aeronautics", " faa", " caa")),
        ("usaf-blue-book", ("usaf", "air force", "blue book", "atic", "4602d", "rg 341")),
        ("cia", ("central intelligence", " cia")),
        ("nasa", ("nasa",)),
        ("navy", ("u.s. navy", "us navy", "office of naval intelligence")),
        ("press", ("newspaper", "press", "magazine")),
        ("academic", ("university", "college", "scientific journal")),
        ("private-archive", ("private archive", "private mirror", "cufon", "nicap")),
    )
    for family, terms in families:
        if any(term in text for term in terms):
            return family
    return "other:" + str(record.get("provenance") or record.get("sourceType") or "unknown").strip().lower()


def source_profile(case):
    records = [record for record in (case.get("sourceRecords") or []) if isinstance(record, dict)]
    quality = str(case.get("sourceQuality", "")).lower()
    combined = " ".join(
        [quality]
        + [" ".join(str(record.get(field, "")) for field in ("sourceType", "provenance", "locator")).lower() for record in records]
    )
    primary_terms = ("primary", "official", "government", "nara", "case-file", "case file", "field-investigation", "mission transcript")
    secondary_terms = ("secondary", "press", "web article", "retrospective", "private archive", "public-record trail")
    primary_count = sum(any(term in " ".join(str(record.get(field, "")) for field in ("sourceType", "provenance")).lower() for term in primary_terms) for record in records)
    secondary_count = sum(any(term in " ".join(str(record.get(field, "")) for field in ("sourceType", "provenance")).lower() for term in secondary_terms) for record in records)
    families = {source_family(record) for record in records}
    complete_packet = (
        any(term in combined for term in ("complete exact", "complete official", "complete 4602d", "complete packet", "complete case-file", "complete case file", "official-complete-public-file-grouping"))
        or (any(term in combined for term in ("digital objects", "-page", " pages", "case-file", "field-investigation-packet")) and primary_count and all(record.get("supports") and record.get("limitations") for record in records))
    )
    if complete_packet:
        label = "complete-primary-packet"
    elif len(families) >= 2 and primary_count >= 2:
        label = "multi-source-independent"
    elif primary_count and secondary_count:
        label = "mixed-provenance"
    elif primary_count:
        label = "single-primary-record"
    elif secondary_count or any(term in quality for term in secondary_terms):
        label = "secondary-only"
    else:
        label = "thin-summary"
    return {
        "label": label,
        "primaryRecords": primary_count,
        "secondaryRecords": secondary_count,
        "independentSourceFamilies": len(families),
        "sourceFamilies": sorted(families),
    }



def source_depth_weakness(case, coverage_row):
    records = case.get("sourceRecords", []) or []
    profile = source_profile(case)
    reasons = []
    score = 0
    profile_scores = {
        "complete-primary-packet": 0,
        "multi-source-independent": 0,
        "mixed-provenance": 10,
        "single-primary-record": 12,
        "secondary-only": 25,
        "thin-summary": 30,
    }
    score += profile_scores[profile["label"]]
    if profile_scores[profile["label"]]:
        reasons.append(f"source profile={profile['label']}")
    if any(isinstance(record, dict) and record.get("supports") in (None, "", []) for record in records):
        score += 15
        reasons.append("empty supports field")
    if any(isinstance(record, dict) and record.get("limitations") in (None, "", []) for record in records):
        score += 15
        reasons.append("empty limitations field")
    source_quality = str(case.get("sourceQuality", "")).lower()
    if any(term in source_quality for term in ("summary", "secondary", "preview")) and profile["label"] not in {"complete-primary-packet", "multi-source-independent"}:
        score += 8
        reasons.append(f"sourceQuality={case.get('sourceQuality')}")
    quote_conf = str(case.get("quoteConfidence", "")).lower()
    if any(term in quote_conf for term in ("summary", "web article", "unclear", "transcription", "not archived")):
        score += 10
        reasons.append("quote confidence needs verification upgrade")
    if coverage_row.get("indexedLinks", 0) <= 1 and profile["label"] not in {"complete-primary-packet", "multi-source-independent"}:
        score += 8
        reasons.append("thin source-index mapping")
    flagship_terms = ("Roswell", "Arnold", "Westall", "Shag", "Malmstrom", "Rendlesham", "Tehran", "JAL", "Foo", "Ghost", "Mantell", "Calvine")
    if score and any(term.lower() in str(case.get("title", "")).lower() for term in flagship_terms):
        score += 5
        reasons.append("flagship/contradiction case")
    return {
        "id": case["id"],
        "title": case["title"],
        "score": score,
        "sourceRecords": len(records),
        "indexedLinks": coverage_row.get("indexedLinks", 0),
        "publicSourceUrls": coverage_row.get("publicSourceUrls", 0),
        "evidenceAssets": coverage_row.get("evidenceAssets", 0),
        "sourceQuality": case.get("sourceQuality"),
        "quoteConfidence": case.get("quoteConfidence"),
        "sourceProfile": profile,
        "reasons": reasons,
    }


def main_source_records(case):
    """Exclude generated/local audit notes from the operational source-boundary gate."""
    return [
        record for record in (case.get("sourceRecords") or [])
        if isinstance(record, dict)
        and not str(record.get("locator", "")).startswith("source-files/")
    ]


def source_triage(case, coverage_row, weakness_row):
    """Classify the next action without treating cautious language as structural failure.

    Categories are mutually exclusive and ordered by operational urgency:
    true_gap -> acquisition_target -> quality_upgrade -> complete.
    """
    main_records = main_source_records(case)
    true_gap_reasons = []
    if not main_records:
        true_gap_reasons.append("no main source record")
    if any(record.get("supports") in (None, "", []) for record in main_records):
        true_gap_reasons.append("main source record has empty supports")
    if any(record.get("limitations") in (None, "", []) for record in main_records):
        true_gap_reasons.append("main source record has empty limitations")
    if not coverage_row.get("indexedLinks"):
        true_gap_reasons.append("no source-index mapping")
    if coverage_row.get("missingLocal"):
        true_gap_reasons.append("missing mapped local asset")

    # Acquisition signals must come from case-level custody findings. Generic
    # Active acquisition work is declared structurally. Evidence limitations in
    # prose are not requests: phrases such as "original negatives are absent"
    # may be durable boundaries rather than an authorized recovery target.
    acquisition_reasons = []
    declared_targets = case.get("acquisitionTargets") or []
    for target in declared_targets:
        if isinstance(target, str) and target.strip():
            acquisition_reasons.append(f"declared acquisition target: {target}")
            continue
        if not isinstance(target, dict):
            continue
        status = str(target.get("status", "")).strip().lower()
        if status in {"recovered", "recovered-new", "duplicate-existing", "complete", "closed"}:
            continue
        label = target.get("targetType") or target.get("target") or target.get("description") or "structured target"
        acquisition_reasons.append(f"declared acquisition target: {label}")

    quality_reasons = []
    profile = weakness_row["sourceProfile"]["label"]
    # A conservative profile label alone is not actionable. Only secondary-only
    # custody or concrete metadata/verification gaps enter the upgrade queue.
    orbital_complete = case.get("domain") == "ORBITAL / NASA" and bool(main_records)
    if profile == "secondary-only" and not orbital_complete:
        quality_reasons.append("secondary-only source profile")
    quote_confidence = str(case.get("quoteConfidence", "")).strip().lower()
    # Confidence prose often separates a high-confidence quotation from a
    # lower-confidence interpretation. Only the declared leading tier is the
    # quote-quality signal; matching "medium" anywhere in the sentence turns
    # accurate boundary language into a false-positive upgrade.
    weak_quote_prefixes = ("low", "medium", "summary", "web article", "not verified", "unclear")
    if not orbital_complete and quote_confidence.startswith(weak_quote_prefixes):
        quality_reasons.append("quote/source confidence can be upgraded")
    source_quality = str(case.get("sourceQuality", "")).strip().lower()
    if not orbital_complete and source_quality in {"primary record", "primary source —", "primary source -"}:
        quality_reasons.append("generic sourceQuality needs provenance detail")
    if coverage_row.get("indexedLinks", 0) <= 1:
        quality_reasons.append("thin source-index mapping")

    if true_gap_reasons:
        category = "true_gap"
        reasons = true_gap_reasons
    elif acquisition_reasons:
        category = "acquisition_target"
        reasons = acquisition_reasons
    elif quality_reasons:
        category = "quality_upgrade"
        reasons = quality_reasons
    else:
        category = "complete"
        reasons = []

    priority_base = {
        "true_gap": 100,
        "acquisition_target": 60,
        "quality_upgrade": 20,
        "complete": 0,
    }[category]
    return {
        "id": case["id"],
        "title": case["title"],
        "domain": case.get("domain"),
        "category": category,
        "priorityScore": priority_base + min(weakness_row["score"], 40),
        "legacyWeaknessScore": weakness_row["score"],
        "reasons": reasons,
        "sourceProfile": profile,
        "sourceRecords": len(case.get("sourceRecords") or []),
        "mainSourceRecords": len(main_records),
        "indexedLinks": coverage_row.get("indexedLinks", 0),
        "publicSourceUrls": coverage_row.get("publicSourceUrls", 0),
        "evidenceAssets": coverage_row.get("evidenceAssets", 0),
        "sourceQuality": case.get("sourceQuality"),
        "quoteConfidence": case.get("quoteConfidence"),
    }

coverage = []
missing_assets = []
for case in cases:
    haystack = source_haystack(case)
    locator = str(case.get("sourceLocator", "")).strip()
    # A case can have one primary locator while citing a multi-record source
    # series. Count every exact index alias present in the factual payload;
    # otherwise the primary locator masks sibling records and creates a false
    # "thin source-index mapping" result.
    tokens = unique_strings(
        ([locator] if locator in index else [])
        + [key for key in index if key.lower() in haystack]
    )
    indexed_links = unique_strings(item for token in tokens for item in index[token])
    direct_public_urls = public_urls(case)
    direct_evidence_assets = evidence_assets(case)
    links = unique_strings([*indexed_links, *direct_public_urls, *direct_evidence_assets])
    local = [item for item in links if not item.startswith(("http://", "https://"))]
    urls = [item for item in links if item.startswith(("http://", "https://"))]
    missing = []
    for item in local:
        path = Path(item)
        if not path.is_absolute():
            path = ROOT / path
        if not path.exists():
            missing.append(item)
    missing_assets.extend({"caseId": case["id"], "path": item} for item in missing)
    coverage.append({
        "id": case["id"],
        "title": case["title"],
        "tokens": tokens,
        "indexedLinks": len(indexed_links),
        "structuredSourceRecords": len(case.get("sourceRecords", []) or []),
        "publicSourceUrls": len(direct_public_urls),
        "evidenceAssets": len(direct_evidence_assets),
        "links": len(links),
        "local": len(local),
        "urls": len(urls),
        "missingLocal": missing,
        "hasEvidence": bool(links or case.get("sourceRecords")),
    })

field_missing = {field: [case["id"] for case in cases if field not in case or case[field] in (None, "", [])] for field in normalized}
geometry_types = Counter()
for case in cases:
    geom = (case.get("geospatial") or {}).get("geometry")
    geometry_types[(geom or {}).get("type", "none")] += 1

ranked_cases = sorted(
    (source_depth_weakness(case, row) for case, row in zip(cases, coverage)),
    key=lambda item: (-item["score"], item["id"]),
)
enrichment_candidates = [item for item in ranked_cases if item["score"] > 0]
# Scores below 25 identify modest metadata/quote upgrades, not genuinely weak dossiers.
weak_cases = [item for item in enrichment_candidates if item["score"] >= 25]
source_profiles = {case["id"]: source_profile(case) for case in cases}
triage_rows = [
    source_triage(case, coverage_row, weakness_row)
    for case, coverage_row, weakness_row in zip(cases, coverage, (
        source_depth_weakness(case, row) for case, row in zip(cases, coverage)
    ))
]
triage_rows.sort(key=lambda item: (-item["priorityScore"], item["id"]))
true_gaps = [item for item in triage_rows if item["category"] == "true_gap"]
quality_upgrades = [item for item in triage_rows if item["category"] == "quality_upgrade"]
acquisition_targets = [item for item in triage_rows if item["category"] == "acquisition_target"]
complete_cases = [item for item in triage_rows if item["category"] == "complete"]

report = {
    "schemaVersion": atlas.get("schemaVersion"),
    "caseCount": len(cases),
    "countedCaseCount": sum(case.get("countInCaseTotals", True) for case in cases),
    "aggregateCaseIds": [case["id"] for case in cases if case.get("countInCaseTotals") is False],
    "seriesParentCount": sum(case.get("recordRole") == "series-parent" for case in cases),
    "seriesChildCount": sum(case.get("recordRole") == "series-child" for case in cases),
    "timelineEventCount": len(events),
    "sourceIndexTerms": len(index),
    "sourceIndexFiles": sum(len(v) for v in index.values()),
    "casesWithMappedLinks": sum(bool(row["links"]) for row in coverage),
    "casesWithoutMappedLinks": [row["id"] for row in coverage if not row["links"]],
    "casesWithIndexedSourceLinks": sum(bool(row["indexedLinks"]) for row in coverage),
    "casesWithoutIndexedSourceLinks": [row["id"] for row in coverage if not row["indexedLinks"]],
    "casesWithStructuredSourceRecords": sum(bool(row["structuredSourceRecords"]) for row in coverage),
    "casesWithPublicSourceUrls": sum(bool(row["publicSourceUrls"]) for row in coverage),
    "casesWithEvidenceAssets": sum(bool(row["evidenceAssets"]) for row in coverage),
    "casesWithEvidenceOrPreview": sum(row["hasEvidence"] for row in coverage),
    "missingLocalAssets": missing_assets,
    "normalizedFieldMissing": field_missing,
    "uniqueDisplayTaxonomy": {
        "domains": len({c.get("domain") for c in cases}),
        "statuses": len({c.get("status") for c in cases}),
        "confidenceLabels": len({c.get("confidence") for c in cases}),
        "agencies": len({c.get("agency") for c in cases}),
    },
    "normalizedTaxonomy": {
        "caseTypes": len({v for c in cases for v in c.get("caseTypes", [])}),
        "evidenceModes": len({v for c in cases for v in c.get("evidenceModes", [])}),
        "environments": len({v for c in cases for v in c.get("environment", [])}),
        "outcomes": len({c.get("outcome") for c in cases}),
    },
    "geometryTypes": dict(geometry_types),
    "nonPointGeometryCases": [case["id"] for case in cases if ((case.get("geospatial") or {}).get("geometry") or {}).get("type") not in {None, "Point"}],
    "quotesSelected": sum(bool(c.get("keyQuote")) for c in cases),
    "quotesWithLocators": sum(bool(c.get("keyQuote") and c.get("sourceLocator")) for c in cases),
    "sourceRecordCount": sum(len(c.get("sourceRecords", [])) for c in cases),
    "sourceDepthWeakCaseCount": len(weak_cases),
    "sourceDepthEnrichmentCandidateCount": len(enrichment_candidates),
    "sourceDepthWeakThreshold": 25,
    "operationalTriageCounts": {
        "trueGaps": len(true_gaps),
        "qualityUpgrades": len(quality_upgrades),
        "acquisitionTargets": len(acquisition_targets),
        "complete": len(complete_cases),
    },
    "sourceProfileCounts": dict(Counter(item["label"] for item in source_profiles.values())),
    "sourceProfiles": source_profiles,
    "topSourceDepthWeakCases": weak_cases[:10],
}

(QA / "atlas-data-code-audit.json").write_text(json.dumps(report, indent=2) + "\n")
(QA / "all-cases-final-source-coverage.json").write_text(json.dumps(coverage, indent=2) + "\n")
(QA / "source-depth-weak-case-priorities.json").write_text(json.dumps(weak_cases, indent=2) + "\n")
(QA / "source-depth-enrichment-candidates.json").write_text(json.dumps(enrichment_candidates, indent=2) + "\n")
(QA / "atlas_true_gaps.json").write_text(json.dumps({"schemaVersion": 1, "category": "true_gap", "caseCount": len(true_gaps), "cases": true_gaps}, indent=2) + "\n")
(QA / "atlas_quality_upgrades.json").write_text(json.dumps({"schemaVersion": 1, "category": "quality_upgrade", "caseCount": len(quality_upgrades), "cases": quality_upgrades}, indent=2) + "\n")
(QA / "atlas_acquisition_targets.json").write_text(json.dumps({"schemaVersion": 1, "category": "acquisition_target", "caseCount": len(acquisition_targets), "cases": acquisition_targets}, indent=2) + "\n")
(QA / "atlas_operational_triage.json").write_text(json.dumps({
    "schemaVersion": 1,
    "policy": "mutually-exclusive-operational-triage",
    "priorityOrder": ["true_gap", "acquisition_target", "quality_upgrade", "complete"],
    "counts": report["operationalTriageCounts"],
    "cases": triage_rows,
}, indent=2) + "\n")
(QA / "enrichment-backlog.json").write_text(json.dumps({
    "schemaVersion": 2,
    "policy": "sole-enrichment-backlog",
    "source": "qa/atlas_operational_triage.json",
    "caseCount": len(true_gaps) + len(quality_upgrades),
    "categoryCounts": {
        "trueGaps": len(true_gaps),
        "qualityUpgrades": len(quality_upgrades),
    },
    "exclusions": {
        "acquisitionTargets": "tracked-separately-no-request-authorized",
        "completeCases": "no-active-work",
        "newCases": "not-authorized",
        "foiaOrArchivalRequests": "not-authorized",
        "outreach": "not-authorized",
    },
    "cases": [*true_gaps, *quality_upgrades],
}, indent=2) + "\n")
print(json.dumps(report, indent=2))
if missing_assets or any(field_missing.values()) or report["casesWithoutMappedLinks"]:
    raise SystemExit(1)
