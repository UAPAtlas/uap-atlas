#!/usr/bin/env python3
"""Regression gate: public HTML embedded data must match canonical Atlas JSON."""
from __future__ import annotations

import json
from pathlib import Path

from sync_atlas_runtime_data import constant_span

ROOT = Path(__file__).resolve().parents[1]


def embedded(text: str, name: str) -> object:
    start, end = constant_span(text, name)
    return json.loads(text[start:end])


def main() -> None:
    text = (ROOT / "index.html").read_text()
    atlas = json.loads((ROOT / "atlas-data.json").read_text())
    source_index = json.loads((ROOT / "source-file-index.json").read_text())
    embedded_atlas = embedded(text, "atlasData")
    embedded_index = embedded(text, "sourceFileIndex")

    assert len(atlas.get("cases", [])) == 146
    assert embedded_atlas == atlas, "index.html atlasData is stale; run sync-atlas-runtime-data.py"
    assert embedded_index == source_index, "index.html sourceFileIndex is stale; run sync-atlas-runtime-data.py"
    print(f"runtime sync OK: {len(atlas['cases'])} cases, {len(source_index)} source tokens")


if __name__ == "__main__":
    main()
