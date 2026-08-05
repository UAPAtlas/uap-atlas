#!/usr/bin/env python3
"""Reject transient workstation and QA artifacts from the Atlas tree."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
forbidden = []
for path in ROOT.rglob('.DS_Store'):
    if '.git' not in path.parts and 'node_modules' not in path.parts:
        forbidden.append(path.relative_to(ROOT).as_posix())
for relative in ('assets/source_previews/test.pdf', 'atlas-mobile.qa.html'):
    if (ROOT / relative).exists():
        forbidden.append(relative)
if forbidden:
    raise SystemExit('REPOSITORY HYGIENE FAILED: ' + ', '.join(sorted(set(forbidden))))
print('REPOSITORY HYGIENE PASS')
