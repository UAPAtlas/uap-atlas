#!/usr/bin/env python3
"""Build the public source-availability contract from the source index and Pages workflow."""
from __future__ import annotations

import argparse
import fnmatch
import json
import re
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_WORKFLOW = ROOT / ".github/workflows/deploy.yml"
DEFAULT_DERIVATIVES = ROOT / "image-derivatives.json"


def workflow_rules(path: Path) -> list[tuple[str, str]]:
    text = path.read_text()
    rules: list[tuple[str, str]] = []
    for action, pattern in re.findall(r"--(include|exclude)='([^']+)'", text):
        rules.append((action, pattern))
    if not rules:
        raise RuntimeError(f"No rsync include/exclude rules found in {path}")
    return rules


def matches(path: str, pattern: str) -> bool:
    # Rsync filter patterns without a slash match path components, so a bare
    # directory rule such as `source-files` excludes its entire subtree. The
    # workflow's slash-containing include rules are matched against the full
    # repository-relative path.
    clean_path = path.strip("/")
    clean_pattern = pattern.strip("/")
    has_glob = any(char in clean_pattern for char in "*?[")
    if "/" not in clean_pattern and not has_glob:
        return clean_pattern in clean_path.split("/")
    return fnmatch.fnmatchcase(clean_path, clean_pattern)


def pages_includes(path: str, rules: list[tuple[str, str]]) -> bool:
    for action, pattern in rules:
        if matches(path, pattern):
            return action == "include"
    return True


def classify(raw: str, rules: list[tuple[str, str]], derivatives: dict[str, dict]) -> dict[str, str]:
    value = raw.strip()
    if re.match(r"^https?://", value, re.I):
        parsed = urlparse(value)
        return {
            "status": "external-public",
            "label": "External public source",
            "host": parsed.netloc.lower(),
        }
    if value.startswith(("data:", "blob:")):
        return {"status": "public-local", "label": "Embedded public asset"}
    if value.startswith(("/Users/", "file://")):
        return {"status": "unavailable", "label": "Unavailable local path"}

    clean = value.split("#", 1)[0].split("?", 1)[0]
    local_path = ROOT / clean
    if not local_path.exists():
        return {"status": "unavailable", "label": "Mapped file not found"}
    derivative = derivatives.get(clean)
    if derivative:
        original_url = derivative.get("originalUrl", "")
        parsed = urlparse(original_url)
        return {
            "status": "external-public",
            "label": "Archival original served from the Atlas Git repository",
            "host": parsed.netloc.lower(),
            "url": original_url,
        }
    if not pages_includes(clean, rules):
        return {
            "status": "custody-only",
            "label": "Held in Atlas research corpus—not publicly served",
        }
    return {"status": "public-local", "label": "Public Atlas asset"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workflow", type=Path, default=DEFAULT_WORKFLOW)
    parser.add_argument("--derivatives", type=Path, default=DEFAULT_DERIVATIVES)
    parser.add_argument("--output", type=Path, default=ROOT / "source-availability.json")
    args = parser.parse_args()

    source_index = json.loads((ROOT / "source-file-index.json").read_text())
    rules = workflow_rules(args.workflow)
    derivative_payload = json.loads(args.derivatives.read_text()) if args.derivatives.exists() else {"entries": {}}
    derivatives = derivative_payload.get("entries", {})
    paths = sorted({item for values in source_index.values() for item in values})
    entries = {item: classify(item, rules, derivatives) for item in paths}
    counts = Counter(row["status"] for row in entries.values())
    payload = {
        "schemaVersion": 1,
        "policy": "explicit-source-availability",
        "generatedFrom": ["source-file-index.json", ".github/workflows/deploy.yml", "image-derivatives.json"],
        "summary": {
            "indexedPaths": len(paths),
            "publicLocal": counts["public-local"],
            "externalPublic": counts["external-public"],
            "custodyOnly": counts["custody-only"],
            "unavailable": counts["unavailable"],
        },
        "entries": entries,
    }
    args.output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    print(
        "source availability: "
        f"{len(paths)} indexed, {counts['public-local']} public local, "
        f"{counts['external-public']} external, {counts['custody-only']} custody-only, "
        f"{counts['unavailable']} unavailable"
    )
    if counts["unavailable"]:
        missing = [p for p, row in entries.items() if row["status"] == "unavailable"]
        print(f"unavailable mappings retained as non-actionable disclosures: {missing[:10]}")


if __name__ == "__main__":
    main()
