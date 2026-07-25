#!/usr/bin/env python3
"""Synchronize canonical Atlas JSON into an HTML runtime's embedded constants."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def constant_span(text: str, name: str) -> tuple[int, int]:
    prefix = f"const {name} = "
    prefix_at = text.find(prefix)
    if prefix_at < 0:
        raise RuntimeError(f"Missing JavaScript constant: {name}")
    start = prefix_at + len(prefix)
    while start < len(text) and text[start].isspace():
        start += 1
    if start >= len(text) or text[start] not in "[{":
        raise RuntimeError(f"Expected object/array value for {name}")

    depth = 0
    quote: str | None = None
    escaped = False
    for index in range(start, len(text)):
        char = text[index]
        if quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
            continue
        if char in {'"', "'", "`"}:
            quote = char
        elif char in "[{":
            depth += 1
        elif char in "]}":
            depth -= 1
            if depth == 0:
                return start, index + 1
    raise RuntimeError(f"Unterminated JavaScript constant: {name}")


def replace_constant(text: str, name: str, value: object) -> str:
    start, end = constant_span(text, name)
    payload = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return text[:start] + payload + text[end:]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--html", default="index.html", help="HTML path relative to repository root")
    args = parser.parse_args()

    html_path = ROOT / args.html
    atlas = json.loads((ROOT / "atlas-data.json").read_text())
    source_index = json.loads((ROOT / "source-file-index.json").read_text())
    if len(atlas.get("cases", [])) != 146:
        raise RuntimeError(f"Refusing to sync unexpected case count: {len(atlas.get('cases', []))}")

    text = html_path.read_text()
    text = replace_constant(text, "atlasData", atlas)
    text = replace_constant(text, "sourceFileIndex", source_index)
    html_path.write_text(text)
    print(f"synced {html_path.name}: {len(atlas['cases'])} cases, {len(source_index)} source tokens")


if __name__ == "__main__":
    main()
