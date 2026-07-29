#!/usr/bin/env python3
"""Regression gate: public runtime data must match canonical Atlas JSON."""
from __future__ import annotations

import json
import argparse
import math
from pathlib import Path

from sync_atlas_runtime_data import DERIVED_CASE_FIELDS, constant_span, has_constant

ROOT = Path(__file__).resolve().parents[1]


def embedded(text: str, name: str) -> object:
    start, end = constant_span(text, name)
    return json.loads(text[start:end])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("html", nargs="?", default="index.html")
    parser.add_argument("--atlas", default="atlas-data.json", help="Expected Atlas JSON, relative to repository root")
    parser.add_argument("--runtime", default="atlas-runtime.js", help="External runtime payload, relative to repository root")
    args = parser.parse_args()
    html_path = (ROOT / args.html).resolve()
    text = html_path.read_text()
    runtime_path = (ROOT / args.runtime).resolve()
    runtime_text = text if has_constant(text, "atlasData") else runtime_path.read_text()
    atlas_path = (ROOT / args.atlas).resolve()
    atlas = json.loads(atlas_path.read_text())
    source_index = json.loads((ROOT / "source-file-index.json").read_text())
    source_availability = json.loads((ROOT / "source-availability.json").read_text())
    embedded_atlas = embedded(runtime_text, "atlasData")
    embedded_index = embedded(runtime_text, "sourceFileIndex")
    embedded_availability = embedded(runtime_text, "sourceAvailabilityIndex") if has_constant(runtime_text, "sourceAvailabilityIndex") else None

    assert len(atlas.get("cases", [])) == 146
    normalized = json.loads(json.dumps(embedded_atlas))
    normalized_expected = json.loads(json.dumps(atlas))
    for case in normalized.get("cases", []):
        for field in DERIVED_CASE_FIELDS:
            case.pop(field, None)
    for case in normalized_expected.get("cases", []):
        for field in DERIVED_CASE_FIELDS:
            case.pop(field, None)
    assert normalized == normalized_expected, f"{html_path.name} canonical atlas fields are stale; run sync_atlas_runtime_data.py"
    projected = [
        case for case in embedded_atlas.get("cases", [])
        if case.get("coordinateGenerated") is True
        and isinstance(case.get("x"), (int, float)) and not isinstance(case.get("x"), bool)
        and isinstance(case.get("y"), (int, float)) and not isinstance(case.get("y"), bool)
        and math.isfinite(case["x"]) and math.isfinite(case["y"])
    ]
    assert len(projected) == 120, f"{html_path.name} must retain 120 finite projected map coordinates, got {len(projected)}"
    assert all(case.get("projection") for case in projected), f"{html_path.name} projected cases must declare projection"
    assert embedded_index == source_index, f"{html_path.name} sourceFileIndex is stale; run sync_atlas_runtime_data.py"
    if embedded_availability is not None:
        assert embedded_availability == source_availability, f"{html_path.name} sourceAvailabilityIndex is stale; run sync_atlas_runtime_data.py"
    print(
        f"runtime sync OK ({html_path.name} <- {atlas_path.name}): "
        f"{len(atlas['cases'])} cases / {len(projected)} projected, {len(source_index)} source tokens, "
        f"{source_availability['summary']['indexedPaths']} availability entries"
    )


if __name__ == "__main__":
    main()
