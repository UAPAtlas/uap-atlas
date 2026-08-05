#!/usr/bin/env python3
"""Regression gate for the Atlas's deferred initial-payload architecture."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
html = (ROOT / "index.html").read_text()
runtime = (ROOT / "atlas-runtime.js").read_text()
app = (ROOT / "atlas-app.js").read_text()
map_runtime = (ROOT / "atlas-map.js").read_text()
blackfile_runtime = (ROOT / "blackfile-analysis.js").read_text()
blackfile_mode = (ROOT / "blackfile-mode.js").read_text()

assert len(html.encode()) < 100_000, f"index.html initial payload regressed to {len(html.encode()):,} bytes"
assert "const atlasData =" not in html, "index.html must not embed Atlas case data"
assert '<div id="atlas-map-mount"></div>' in html
assert '<link rel="preload" href="atlas-map.js" as="script" />' in html
assert '<link rel="preload" href="atlas-runtime.js" as="script" />' in html
assert '<link rel="preload" href="atlas-app.js" as="script" />' in html
assert '<link rel="preload" href="blackfile-analysis.js" as="script" />' in html
assert '<link rel="preload" href="blackfile-mode.js" as="script" />' in html
assert '<script src="atlas-map.js" defer></script>' in html
assert '<script src="atlas-runtime.js" defer></script>' in html
assert '<script src="atlas-app.js" defer></script>' in html
assert '<script src="blackfile-analysis.js" defer></script>' in html
assert '<script src="blackfile-mode.js" defer></script>' in html
assert "const atlasData =" in runtime
assert "const sourceFileIndex =" in runtime
assert "const sourceAvailabilityIndex =" in runtime
assert "function renderAll()" in app
assert "/* ATLAS_MOBILE_JS_START */" in app
assert "const blackfileAnalysis =" in blackfile_runtime
assert "window.blackfileMode" in blackfile_mode
assert "getElementById('atlas-map-mount').outerHTML" in map_runtime
assert '<svg id=\\"atlasSvg\\"' in map_runtime

match = re.search(r"const atlasData = (\{.*?\});\nconst sourceFileIndex", runtime, re.S)
assert match, "atlasData runtime constant not found"
atlas = json.loads(match.group(1))
assert len(atlas.get("cases", [])) == 146
assert len(atlas.get("timeline", [])) == 144
assert len([case for case in atlas["cases"] if case.get("coordinateGenerated") is True]) == 120

print(
    f"Atlas payload contract OK: HTML {len(html.encode()):,} bytes, "
    f"runtime {len(runtime.encode()):,} bytes, app {len(app.encode()):,} bytes"
)
