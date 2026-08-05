#!/usr/bin/env python3
"""Static contract for the Atlas Product Integrity sprint."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--html', default='index.html')
parser.add_argument('--app', default='atlas-app.js')
args = parser.parse_args()
html = (ROOT / args.html).read_text()
app_path = ROOT / args.app
app = app_path.read_text() if app_path.exists() else html
blackfile = (ROOT / 'blackfile-mode.js').read_text()
manifest = json.loads((ROOT / 'image-derivatives.json').read_text())
workflow = (ROOT / '.github/workflows/deploy.yml').read_text() if (ROOT / '.github/workflows/deploy.yml').exists() else ''
errors = []

def require(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)

require(len(manifest.get('entries', {})) >= 300, 'heavy-image derivative coverage below 300 images')
require('image-derivatives.js' in html, 'derivative runtime script missing')
require('displayImageUrl' in app and 'thumbImageUrl' in app and 'originalImageUrl' in app, 'derivative URL helpers missing')
require('loading="lazy" decoding="async"' in app, 'lazy thumbnail delivery missing')
require('originalSrc||it.src' in app and 'originalImageUrl(original)' in app, 'lightbox archival-original routing missing')
require('role="dialog" aria-modal="true" aria-label="Evidence image viewer"' in app, 'lightbox dialog semantics missing')
require('trapModalFocus' in app and "setAttribute('inert','')" in app, 'modal focus/inert contract missing')
require('role="button" tabindex="0" aria-label="Open ${count} Orbital' in app, 'Orbital aggregate keyboard semantics missing')
require("state.filters.precision==='orbital'" in app and "state.stackMode='orbital'" in app, 'Orbital filter routing missing')
require('data-landscape-exit' in html and "setMobilePage('cases')" in app, 'landscape map escape missing')
require("setMobilePage('dossier')" in blackfile, 'Blackfile mobile dossier handoff bypasses mobile controller')
for label in ('Questions', 'Evidence', 'Brief'):
    require(f'data-blackfile="{label}"' in html, f'Blackfile mobile label missing: {label}')
if workflow:
    require("--exclude-from='assets/image-derivatives-exclude.txt'" in workflow, 'Pages derivative exclusion list missing')
    require('test-atlas-artifact-budget.py --root /tmp/site' in workflow, 'Pages artifact budget gate missing')
    require('test-repository-hygiene.py' in workflow, 'repository hygiene gate missing')
if errors:
    raise SystemExit('ATLAS PRODUCT INTEGRITY FAILED:\n- ' + '\n- '.join(errors))
print(f"ATLAS PRODUCT INTEGRITY PASS: {len(manifest['entries'])} derivatives")
