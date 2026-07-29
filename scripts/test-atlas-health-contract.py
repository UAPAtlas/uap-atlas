#!/usr/bin/env python3
"""Focused regression checks for release-health defects fixed in July 2026."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("--html", default="index.html", help="HTML artifact relative to the Atlas root")
args = parser.parse_args()
HTML = (ROOT / args.html).read_text()
ATLAS = json.loads((ROOT / "atlas-data.json").read_text())


def asset_src(value):
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return value.get("src") or value.get("url") or value.get("path")
    return None


errors: list[str] = []

required_html = {
    '<main class="main">': "main landmark",
    'id="agencyFilter" aria-label="Filter cases by agency"': "agency filter accessible name",
    'id="domainFilter" aria-label="Filter cases by domain"': "domain filter accessible name",
    'id="precisionFilter" aria-label="Filter cases by location precision"': "precision filter accessible name",
    'aria-label="Cortana UAP Case Atlas — reset to home"': "brand/home accessible name",
}
for needle, label in required_html.items():
    if needle not in HTML:
        errors.append(f"missing {label}")

for case in ATLAS.get("cases", []):
    hero = asset_src(case.get("heroVisual"))
    image = asset_src(case.get("image"))
    images = case.get("images") or []
    first = asset_src(images[0]) if images else None
    if hero and not (hero == image == first):
        errors.append(f"{case.get('id', '?')}: carousel-first hero invariant failed")

stale_urls = {
    "https://media.defense.gov/2010/Dec/01/2001329893/-1/-1/0/roswell-2.pdf",
    "https://media.defense.gov/2010/Dec/01/2001329894/-1/-1/0/roswell-2.pdf",
    "https://www.kathleen-marden.com/betty-and-barney-hill-archive.php",
    "https://www.atsb.gov.au/media/5226347/197802563.pdf",
}
for rel in (
    "atlas-data.json",
    "assets/generated/atlas-data.generated.json",
    "public-source-manifest.json",
    args.html,
):
    text = (ROOT / rel).read_text()
    for url in stale_urls:
        if url in text:
            errors.append(f"{rel}: stale source URL remains: {url}")

if errors:
    print("ATLAS HEALTH CONTRACT FAILED")
    print("\n".join(f"- {error}" for error in errors))
    raise SystemExit(1)

print(f"ATLAS HEALTH CONTRACT OK: {len(ATLAS.get('cases', []))} cases")
