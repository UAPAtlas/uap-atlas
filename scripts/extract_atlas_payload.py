#!/usr/bin/env python3
"""Extract Atlas inline runtime data/application JS into deferred cacheable assets."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from sync_atlas_runtime_data import constant_span, embedded_constant

ROOT = Path(__file__).resolve().parents[1]
DATA_NAMES = ("atlasData", "sourceFileIndex", "sourceAvailabilityIndex")


def declaration_span(text: str, name: str) -> tuple[int, int]:
    prefix_at = text.find(f"const {name} = ")
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
    parser.add_argument("--runtime", default="atlas-runtime.js")
    parser.add_argument("--app", default="atlas-app.js")
    args = parser.parse_args()

    html_path = ROOT / args.html
    runtime_path = ROOT / args.runtime
    app_path = ROOT / args.app
    html = html_path.read_text()

    external_tags = (
        f'<script src="{runtime_path.name}" defer></script>\n'
        f'<script src="{app_path.name}" defer></script>'
    )
    if external_tags in html:
        print(f"Atlas payload already externalized: {html_path.name}")
        return

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

    runtime_text = "/* Generated Atlas runtime payload. Update via scripts/sync_atlas_runtime_data.py. */\n" + "\n".join(
        f"const {name} = {json.dumps(payload[name], ensure_ascii=False, separators=(',', ':'))};"
        for name in DATA_NAMES
    ) + "\n"
    app_text = "/* UAP Atlas application runtime. Loaded with defer after atlas-runtime.js. */\n" + app.lstrip()
    new_html = html[:script_open] + external_tags + html[script_close + len("</script>"):]
    preload_anchor = '<link rel="apple-touch-icon" sizes="512x512" href="assets/apple-touch-icon.png" />'
    preload_tags = (
        f'{preload_anchor}\n'
        f'<link rel="preload" href="{runtime_path.name}" as="script" />\n'
        f'<link rel="preload" href="{app_path.name}" as="script" />'
    )
    if f'<link rel="preload" href="{runtime_path.name}" as="script" />' not in new_html:
        if preload_anchor not in new_html:
            raise RuntimeError("Atlas preload anchor not found")
        new_html = new_html.replace(preload_anchor, preload_tags, 1)

    runtime_path.write_text(runtime_text)
    app_path.write_text(app_text)
    html_path.write_text(new_html)
    print(
        f"externalized {html_path.name}: html={len(new_html.encode()):,} bytes, "
        f"runtime={len(runtime_text.encode()):,}, app={len(app_text.encode()):,}"
    )


if __name__ == "__main__":
    main()
