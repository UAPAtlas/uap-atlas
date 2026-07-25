#!/usr/bin/env python3
"""Regression gate: public HTML embedded data must match canonical Atlas JSON."""
from __future__ import annotations

import json
import argparse
from pathlib import Path

from sync_atlas_runtime_data import constant_span

ROOT = Path(__file__).resolve().parents[1]


def embedded(text: str, name: str) -> object:
    start, end = constant_span(text, name)
    return json.loads(text[start:end])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("html", nargs="?", default="index.html")
    parser.add_argument("--atlas", default="atlas-data.json", help="Expected embedded Atlas JSON, relative to repository root")
    args = parser.parse_args()
    html_path = (ROOT / args.html).resolve()
    text = html_path.read_text()
    atlas_path = (ROOT / args.atlas).resolve()
    atlas = json.loads(atlas_path.read_text())
    source_index = json.loads((ROOT / "source-file-index.json").read_text())
    source_availability = json.loads((ROOT / "source-availability.json").read_text())
    embedded_atlas = embedded(text, "atlasData")
    embedded_index = embedded(text, "sourceFileIndex")
    embedded_availability = embedded(text, "sourceAvailabilityIndex")

    assert len(atlas.get("cases", [])) == 146
    assert embedded_atlas == atlas, f"{html_path.name} atlasData is stale; run sync_atlas_runtime_data.py"
    assert embedded_index == source_index, f"{html_path.name} sourceFileIndex is stale; run sync_atlas_runtime_data.py"
    assert embedded_availability == source_availability, f"{html_path.name} sourceAvailabilityIndex is stale; run sync_atlas_runtime_data.py"
    print(
        f"runtime sync OK ({html_path.name} <- {atlas_path.name}): "
        f"{len(atlas['cases'])} cases, {len(source_index)} source tokens, "
        f"{source_availability['summary']['indexedPaths']} availability entries"
    )


if __name__ == "__main__":
    main()
