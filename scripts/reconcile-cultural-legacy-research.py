#!/usr/bin/env python3
"""Validate and merge the three 146-case Cultural Legacy research tranches."""
from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import date
from pathlib import Path

VALID_DECISIONS = {"include", "defer", "none"}
BOUNDARY = "Cultural context — not case evidence"


def load_json(path: Path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--research", nargs=3, required=True)
    parser.add_argument("--output-json")
    parser.add_argument("--output-md")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    atlas = load_json(root / "atlas-data.json")
    canonical = {case["id"]: case for case in atlas["cases"]}
    if len(canonical) != 146:
        raise SystemExit(f"Expected 146 unique canonical cases, found {len(canonical)}")

    reviewed = []
    for file_name in args.research:
        path = Path(file_name)
        payload = load_json(path)
        if not isinstance(payload.get("cases"), list):
            raise SystemExit(f"{path}: missing cases array")
        reviewed.extend(payload["cases"])

    ids = [item.get("id") for item in reviewed]
    duplicates = sorted(case_id for case_id, count in Counter(ids).items() if count > 1)
    missing = sorted(set(canonical) - set(ids))
    extras = sorted(set(ids) - set(canonical))
    if len(reviewed) != 146 or duplicates or missing or extras:
        raise SystemExit(
            f"Coverage failure: reviewed={len(reviewed)} duplicates={duplicates} "
            f"missing={missing} extras={extras}"
        )

    normalized = []
    for item in reviewed:
        case_id = item["id"]
        decision = str(item.get("decision", "")).lower()
        candidates = item.get("candidates") or []
        implemented = canonical[case_id].get("culturalLegacy") or []
        if implemented:
            decision = "include"
            candidates = implemented
            item = dict(item)
            item["reason"] = "Implemented locally after independent connection, source, image, and license verification."
        if decision not in VALID_DECISIONS:
            raise SystemExit(f"{case_id}: invalid decision {decision!r}")
        if decision == "none" and candidates:
            raise SystemExit(f"{case_id}: none decision cannot carry candidates")
        if decision in {"include", "defer"} and not candidates:
            raise SystemExit(f"{case_id}: {decision} requires at least one candidate")
        for index, candidate in enumerate(candidates):
            prefix = f"{case_id} candidate {index + 1}"
            for key in ("title", "connection", "sourceLabel", "sourceUrl", "contextStatus"):
                if not candidate.get(key):
                    raise SystemExit(f"{prefix}: missing {key}")
            if candidate["contextStatus"] != BOUNDARY:
                raise SystemExit(f"{prefix}: incorrect evidence boundary")
            if not str(candidate["sourceUrl"]).startswith("https://"):
                raise SystemExit(f"{prefix}: sourceUrl must be HTTPS")
            for key in ("imageSourceUrl", "licenseUrl"):
                value = candidate.get(key)
                if value and not str(value).startswith("https://"):
                    raise SystemExit(f"{prefix}: {key} must be HTTPS when present")
        normalized.append({
            "id": case_id,
            "title": canonical[case_id]["title"],
            "decision": decision,
            "reason": item.get("reason", ""),
            "candidates": candidates,
        })

    order = {case["id"]: index for index, case in enumerate(atlas["cases"])}
    normalized.sort(key=lambda item: order[item["id"]])
    counts = dict(Counter(item["decision"] for item in normalized))
    for decision in sorted(VALID_DECISIONS):
        counts.setdefault(decision, 0)

    output_json = Path(args.output_json or root / "research" / f"cultural-legacy-tranche-{date.today().isoformat()}.json")
    output_md = Path(args.output_md or root / "research" / f"cultural-legacy-tranche-{date.today().isoformat()}.md")
    output_json.parent.mkdir(parents=True, exist_ok=True)
    report = {
        "schemaVersion": 1,
        "policy": "optional-cultural-context-layer-not-evidence",
        "reviewedOn": date.today().isoformat(),
        "caseCount": 146,
        "counts": counts,
        "boundary": BOUNDARY,
        "cases": normalized,
    }
    output_json.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = [
        "# UAP Atlas Cultural Legacy tranche",
        "",
        f"Reviewed: {report['reviewedOn']}",
        "",
        "All 146 existing dossiers were assessed. Cultural records are optional context and do not affect evidence, confidence, source counts, or case count.",
        "",
        f"- Implemented records: {counts['include']}",
        f"- Deferred candidates: {counts['defer']}",
        f"- No consequential documented artifact located: {counts['none']}",
        "",
        "## Implemented records",
        "",
    ]
    for item in normalized:
        if item["decision"] == "include":
            candidate_titles = "; ".join(candidate["title"] for candidate in item["candidates"])
            lines.append(f"- **{item['title']}** (`{item['id']}`): {candidate_titles}")
    deferred = [item for item in normalized if item["decision"] == "defer"]
    if deferred:
        lines += ["", "## Deferred candidates", ""]
        for item in deferred:
            lines.append(f"- **{item['title']}** (`{item['id']}`): {item['reason']}")
    while lines and not lines[-1]:
        lines.pop()
    output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"status": "passed", "caseCount": 146, "counts": counts, "json": str(output_json), "markdown": str(output_md)}, indent=2))


if __name__ == "__main__":
    main()
