#!/usr/bin/env python3
"""Maintain public Atlas count metadata deterministically."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

DESCRIPTION_FIELDS = (
    ("<meta name=\"description\"", re.compile(r'(<meta name="description" content=")([^"]+)("\s*/?>)')),
    ("<meta itemprop=\"description\"", re.compile(r'(<meta itemprop="description" content=")([^"]+)("\s*/?>)')),
    ("<meta property=\"og:description\"", re.compile(r'(<meta property="og:description" content=")([^"]+)("\s*/?>)')),
    ("<meta name=\"twitter:description\"", re.compile(r'(<meta name="twitter:description" content=")([^"]+)("\s*/?>)')),
)

COUNT_PHRASE = re.compile(r'\b\d+ documented UAP (?:cases|records)\b')


def load_counts(atlas_data: Path) -> dict[str, int]:
    atlas = json.loads(atlas_data.read_text())
    cases = atlas.get("cases") or []
    timeline = atlas.get("timeline") or atlas.get("timelineEvents") or []
    return {
        "records": len(cases),
        "cases": sum(1 for case in cases if case.get("countInCaseTotals", True)),
        "timeline": len(timeline),
        "sourceRecords": sum(len(case.get("sourceRecords") or []) for case in cases),
    }


def replacement_description(current: str, *, count: int, noun: str | None) -> str:
    matches = COUNT_PHRASE.findall(current)
    if len(matches) != 1:
        raise ValueError(f"description must contain exactly one replaceable count phrase: {current!r}")
    existing_noun = "records" if matches[0].endswith("records") else "cases"
    return COUNT_PHRASE.sub(f"{count} documented UAP {noun or existing_noun}", current, count=1)


def update_html(html_path: Path, counts: dict[str, int], *, noun: str | None, check: bool = False) -> bool:
    text = html_path.read_text()
    expected_count = counts["records"]
    changed_any = False
    for label, pattern in DESCRIPTION_FIELDS:
        matches = list(pattern.finditer(text))
        if len(matches) != 1:
            raise ValueError(f"expected exactly one {label}; found {len(matches)}")
        match = matches[0]
        current = match.group(2)
        updated = replacement_description(current, count=expected_count, noun=noun)
        if updated != current:
            changed_any = True
            text = text[:match.start(2)] + updated + text[match.end(2):]
    if changed_any and not check:
        html_path.write_text(text)
    return changed_any


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--atlas-data", type=Path, default=Path("atlas-data.json"))
    parser.add_argument("--html", type=Path, action="append", default=[], help="HTML file to update/check; repeatable")
    parser.add_argument("--noun", choices=("cases", "records"), default=None, help="Optional noun override for public meta descriptions; default preserves existing wording")
    parser.add_argument("--check", action="store_true", help="Fail if any HTML metadata would change")
    args = parser.parse_args()

    counts = load_counts(args.atlas_data)
    changed = []
    for html in args.html:
        if update_html(html, counts, noun=args.noun, check=args.check):
            changed.append(str(html))
    print(json.dumps({"counts": counts, "changed": changed}, sort_keys=True))
    if args.check and changed:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
