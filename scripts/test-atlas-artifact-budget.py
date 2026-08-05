#!/usr/bin/env python3
"""Enforce Atlas Pages and derivative payload budgets."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

MIB = 1024 * 1024
parser = argparse.ArgumentParser()
parser.add_argument('--root', default='.')
parser.add_argument('--max-site-mib', type=float, default=180)
parser.add_argument('--max-derivatives-mib', type=float, default=70)
parser.add_argument('--max-display-mib', type=float, default=1.5)
parser.add_argument('--max-thumb-mib', type=float, default=0.25)
args = parser.parse_args()
root = Path(args.root).resolve()
manifest_path = root / 'image-derivatives.json'
if not manifest_path.exists():
    raise SystemExit(f'ARTIFACT BUDGET FAILED: missing {manifest_path}')
manifest = json.loads(manifest_path.read_text())
entries = manifest.get('entries', {})
if not entries:
    raise SystemExit('ARTIFACT BUDGET FAILED: empty derivative manifest')
errors = []
derivative_total = 0
for original, record in entries.items():
    for variant, limit in (('display', args.max_display_mib), ('thumb', args.max_thumb_mib)):
        relative = record[variant]['path']
        path = root / relative
        if not path.exists():
            errors.append(f'missing {variant}: {relative}')
            continue
        size = path.stat().st_size
        derivative_total += size
        if size > limit * MIB:
            errors.append(f'{variant} over {limit:.2f} MiB: {relative} ({size/MIB:.2f} MiB)')
site_total = sum(p.stat().st_size for p in root.rglob('*') if p.is_file())
if derivative_total > args.max_derivatives_mib * MIB:
    errors.append(f'derivatives {derivative_total/MIB:.1f} MiB > {args.max_derivatives_mib:.1f} MiB')
if site_total > args.max_site_mib * MIB:
    errors.append(f'site {site_total/MIB:.1f} MiB > {args.max_site_mib:.1f} MiB')
if errors:
    raise SystemExit('ARTIFACT BUDGET FAILED:\n- ' + '\n- '.join(errors[:30]))
print(f'ARTIFACT BUDGET PASS: site={site_total/MIB:.1f} MiB derivatives={derivative_total/MIB:.1f} MiB entries={len(entries)}')
