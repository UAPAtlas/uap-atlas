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



def source_depth_weakness(case, coverage_row):
    records = case.get("sourceRecords", []) or []
    reasons = []
    score = 0
    if len(records) <= 1:
        score += 30
        reasons.append("one-or-fewer structured source records")
    if any(isinstance(record, dict) and not str(record.get("supports", "")).strip() for record in records):
        score += 20
        reasons.append("empty supports field")
    if any(isinstance(record, dict) and not str(record.get("limitations", "")).strip() for record in records):
        score += 20
        reasons.append("empty limitations field")
    source_quality = str(case.get("sourceQuality", "")).lower()
    if any(term in source_quality for term in ("collection", "summary", "secondary", "preview")):
        score += 12
        reasons.append(f"sourceQuality={case.get('sourceQuality')}")
    quote_conf = str(case.get("quoteConfidence", "")).lower()
    if any(term in quote_conf for term in ("summary", "web article", "unclear", "transcription", "not archived")):
        score += 10
        reasons.append("quote confidence needs verification upgrade")
    if coverage_row.get("indexedLinks", 0) <= 1:
        score += 8
        reasons.append("thin source-index mapping")
    flagship_terms = ("Roswell", "Arnold", "Westall", "Shag", "Malmstrom", "Rendlesham", "Tehran", "JAL", "Foo", "Ghost", "Mantell", "Calvine")
    if any(term.lower() in str(case.get("title", "")).lower() for term in flagship_terms):
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
        "reasons": reasons,
    }

coverage = []
missing_assets = []
for case in cases:
    haystack = source_haystack(case)
    locator = str(case.get("sourceLocator", "")).strip()
    tokens = [locator] if locator in index else [key for key in index if key.lower() in haystack]
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

weak_cases = sorted(
    (source_depth_weakness(case, row) for case, row in zip(cases, coverage)),
    key=lambda item: (-item["score"], item["id"]),
)
weak_cases = [item for item in weak_cases if item["score"] > 0]

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
    "topSourceDepthWeakCases": weak_cases[:10],
}

(QA / "atlas-data-code-audit.json").write_text(json.dumps(report, indent=2) + "\n")
(QA / "all-cases-final-source-coverage.json").write_text(json.dumps(coverage, indent=2) + "\n")
(QA / "source-depth-weak-case-priorities.json").write_text(json.dumps(weak_cases, indent=2) + "\n")
print(json.dumps(report, indent=2))
if missing_assets or any(field_missing.values()) or report["casesWithoutMappedLinks"]:
    raise SystemExit(1)
