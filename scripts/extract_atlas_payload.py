#!/usr/bin/env python3
"""Extract the Atlas map, runtime data, and app JS into deferred cacheable assets."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from sync_atlas_runtime_data import ROOT, constant_span, embedded_constant

DATA_NAMES = ("atlasData", "sourceFileIndex", "sourceAvailabilityIndex")


def declaration_span(text: str, name: str) -> tuple[int, int]:
    prefix = f"const {name} = "
    prefix_at = text.find(prefix)
    if prefix_at < 0:
        raise RuntimeError(f"Missing runtime declaration: {name}")
    _, value_end = constant_span(text, name)
    end = value_end + (1 if value_end < len(text) and text[value_end] == ";" else 0)
    while end < len(text) and text[end] in " \t\r\n":
        end += 1
    return prefix_at, end


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--html", default="index.html")
    parser.add_argument("--runtime-output", default="atlas-runtime.js")
    parser.add_argument("--app-output", default="atlas-app.js")
    parser.add_argument("--map-output", default="atlas-map.js")
    args = parser.parse_args()

    html_path = (ROOT / args.html).resolve()
    runtime_path = (ROOT / args.runtime_output).resolve()
    app_path = (ROOT / args.app_output).resolve()
    map_path = (ROOT / args.map_output).resolve()
    html = html_path.read_text()

    refs = [
        f'<script src="{map_path.name}" defer></script>',
        f'<script src="{runtime_path.name}" defer></script>',
        f'<script src="{app_path.name}" defer></script>',
    ]
    if all(ref in html for ref in refs):
        print("Atlas payload is already externalized")
        return
    if any(ref in html for ref in refs):
        raise RuntimeError("Partially externalized payload; refuse to produce an ambiguous build")

    marker = "<script>\nconst atlasData = "
    script_open = html.find(marker)
    if script_open < 0:
        raise RuntimeError("Atlas inline application script not found")
    body_start = script_open + len("<script>\n")
    script_close = html.find("</script>", body_start)
    if script_close < 0:
        raise RuntimeError("Atlas inline application script is unterminated")
    body = html[body_start:script_close]

    payload = {name: embedded_constant(body, name) for name in DATA_NAMES}
    app = body
    for name in reversed(DATA_NAMES):
        start, end = declaration_span(app, name)
        app = app[:start] + app[end:]

    svg_start = html.find('<svg id="atlasSvg"')
    svg_end = html.find("</svg>", svg_start)
    if svg_start < 0 or svg_end < 0:
        raise RuntimeError("Atlas map SVG not found")
    svg_end += len("</svg>")
    map_markup = html[svg_start:svg_end]

    runtime_text = "/* Generated Atlas runtime payload. Update via scripts/sync_atlas_runtime_data.py. */\n" + "\n".join(
        f"const {name} = {json.dumps(payload[name], ensure_ascii=False, separators=(',', ':'))};"
        for name in DATA_NAMES
    ) + "\n"
    app_text = "/* UAP Atlas application runtime. Loaded with defer after atlas-runtime.js. */\n" + app.lstrip()
    map_text = (
        "/* Generated Atlas map markup. Loaded with defer before atlas-app.js. */\n"
        "document.getElementById('atlas-map-mount').outerHTML = "
        f"{json.dumps(map_markup, ensure_ascii=False)};\n"
    )

    external_tags = "\n".join(refs)
    new_html = html[:script_open] + external_tags + html[script_close + len("</script>"):]
    new_html = new_html[:svg_start] + '<div id="atlas-map-mount"></div>' + new_html[svg_end:]

    preload_anchor = '<link rel="apple-touch-icon" sizes="512x512" href="assets/apple-touch-icon.png" />'
    preload_tags = (
        f'{preload_anchor}\n'
        f'<link rel="preload" href="{map_path.name}" as="script" />\n'
        f'<link rel="preload" href="{runtime_path.name}" as="script" />\n'
        f'<link rel="preload" href="{app_path.name}" as="script" />'
    )
    if preload_anchor not in new_html:
        raise RuntimeError("Atlas preload anchor not found")
    new_html = new_html.replace(preload_anchor, preload_tags, 1)

    runtime_path.write_text(runtime_text)
    app_path.write_text(app_text)
    map_path.write_text(map_text)
    html_path.write_text(new_html)
    print(
        f"externalized {html_path.name}: html={len(new_html.encode()):,} bytes, "
        f"map={len(map_text.encode()):,}, runtime={len(runtime_text.encode()):,}, "
        f"app={len(app_text.encode()):,}"
    )


if __name__ == "__main__":
    main()
