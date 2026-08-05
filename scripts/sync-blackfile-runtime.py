#!/usr/bin/env python3
"""Generate the browser-safe Blackfile analysis constant from canonical JSON."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("--root", type=Path, default=ROOT)
args = parser.parse_args()
root = args.root.resolve()
source = root / "blackfile-analysis.json"
target = root / "blackfile-analysis.js"
payload = json.loads(source.read_text())
encoded = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
target.write_text(f"const blackfileAnalysis = {encoded};\n")
print(f"Blackfile runtime sync OK: {len(payload.get('questions', []))} questions · {target.name}")
