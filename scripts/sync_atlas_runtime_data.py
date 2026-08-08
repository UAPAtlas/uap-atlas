#!/usr/bin/env python3
"""Synchronize canonical Atlas JSON into an HTML runtime's embedded constants."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Ordered for byte-for-byte reproducibility across Python processes. A set here
# makes json.dumps field order depend on PYTHONHASHSEED.
DERIVED_CASE_FIELDS = ("coordinateGenerated", "mapGeometry", "projection", "x", "y")


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


def embedded_constant(text: str, name: str) -> object:
    start, end = constant_span(text, name)
    return json.loads(text[start:end])


def has_constant(text: str, name: str) -> bool:
    return f"const {name} = " in text


def insert_constant_after(text: str, anchor: str, name: str, value: object) -> str:
    """Add a missing runtime constant after an existing constant declaration."""
    _, end = constant_span(text, anchor)
    if end < len(text) and text[end] == ";":
        end += 1
    payload = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return text[:end] + f"\nconst {name} = {payload};" + text[end:]


def preserve_map_fields(canonical: dict, embedded_atlas: dict, generated_map: dict | None = None) -> dict:
    """Overlay approved generated map fields by case ID, preferring the map build artifact."""
    existing = {case.get("id"): case for case in embedded_atlas.get("cases", [])}
    generated = {case.get("id"): case for case in (generated_map or {}).get("cases", [])}
    hydrated = json.loads(json.dumps(canonical))
    for case in hydrated.get("cases", []):
        for source in (existing.get(case.get("id"), {}), generated.get(case.get("id"), {})):
            for field in DERIVED_CASE_FIELDS:
                if field in source:
                    case[field] = source[field]
    return hydrated


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--html", default="index.html", help="HTML path relative to repository root")
    parser.add_argument("--runtime", default="atlas-runtime.js", help="External runtime payload relative to repository root")
    parser.add_argument("--map-data", default="assets/generated/atlas-map.json", help="Generated map payload relative to repository root")
    args = parser.parse_args()

    html_path = ROOT / args.html
    atlas = json.loads((ROOT / "atlas-data.json").read_text())
    source_index = json.loads((ROOT / "source-file-index.json").read_text())
    source_availability = json.loads((ROOT / "source-availability.json").read_text())
    if len(atlas.get("cases", [])) != 155:
        raise RuntimeError(f"Refusing to sync unexpected case count: {len(atlas.get('cases', []))}")

    html_text = html_path.read_text()
    runtime_path = ROOT / args.runtime
    external_runtime = not has_constant(html_text, "atlasData")
    if external_runtime:
        if not runtime_path.exists():
            raise RuntimeError(f"External Atlas runtime is missing: {runtime_path}")
        runtime_text = runtime_path.read_text()
    else:
        runtime_text = html_text
    map_path = ROOT / args.map_data
    generated_map = json.loads(map_path.read_text()) if map_path.exists() else None
    existing_runtime_atlas = embedded_constant(runtime_text, "atlasData")
    if not isinstance(existing_runtime_atlas, dict):
        raise RuntimeError("Atlas runtime payload must be an object")
    atlas = preserve_map_fields(atlas, existing_runtime_atlas, generated_map)
    projected = [
        case for case in atlas["cases"]
        if case.get("coordinateGenerated") is True
        and isinstance(case.get("x"), (int, float)) and not isinstance(case.get("x"), bool)
        and isinstance(case.get("y"), (int, float)) and not isinstance(case.get("y"), bool)
    ]
    if len(projected) != 129:
        raise RuntimeError(f"Refusing to sync runtime without 129 projected cases: {len(projected)}")
    runtime_text = replace_constant(runtime_text, "atlasData", atlas)
    runtime_text = replace_constant(runtime_text, "sourceFileIndex", source_index)
    if has_constant(runtime_text, "sourceAvailabilityIndex"):
        runtime_text = replace_constant(runtime_text, "sourceAvailabilityIndex", source_availability)
    else:
        runtime_text = insert_constant_after(runtime_text, "sourceFileIndex", "sourceAvailabilityIndex", source_availability)
    if external_runtime:
        runtime_path.write_text(runtime_text)
        synced_target = runtime_path.name
    else:
        html_path.write_text(runtime_text)
        synced_target = html_path.name
    print(
        f"synced {synced_target}: {len(atlas['cases'])} cases / {len(projected)} projected, "
        f"{len(source_index)} source tokens, "
        f"{source_availability['summary']['indexedPaths']} availability entries"
    )


if __name__ == "__main__":
    main()
