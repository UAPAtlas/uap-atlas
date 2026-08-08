#!/usr/bin/env python3
"""Verify that Atlas generated artifacts are current and reproducible."""

from __future__ import annotations

import argparse
import hashlib
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP_OUTPUTS = (
    ROOT / "assets/generated/atlas-map.json",
    ROOT / "assets/generated/atlas-data.generated.json",
)


def run(*args: str) -> None:
    subprocess.run(args, cwd=ROOT, check=True)


def digest(paths: tuple[Path, ...] | list[Path]) -> str:
    hasher = hashlib.sha256()
    for path in paths:
        hasher.update(str(path.name).encode())
        hasher.update(path.read_bytes())
    return hasher.hexdigest()


def fail(message: str) -> None:
    raise SystemExit(f"ATLAS BUILD REPRODUCIBILITY FAILED: {message}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--html", default="index.html")
    parser.add_argument("--app", default="atlas-app.js")
    args = parser.parse_args()

    html = (ROOT / args.html).resolve()
    app = (ROOT / args.app).resolve()
    if not html.exists():
        fail(f"missing HTML source: {html}")
    if not all(path.exists() for path in MAP_OUTPUTS):
        fail("missing checked-in map outputs")

    protected = [html]
    if app.exists():
        protected.append(app)
    protected_before = digest(protected)

    map_before = digest(list(MAP_OUTPUTS))
    run("node", "scripts/build-atlas-map.mjs")
    map_first = digest(list(MAP_OUTPUTS))
    run("node", "scripts/build-atlas-map.mjs")
    map_second = digest(list(MAP_OUTPUTS))
    if map_before != map_first:
        fail("checked-in map outputs are stale")
    if map_first != map_second:
        fail("map generation is not deterministic")

    with tempfile.TemporaryDirectory(prefix="uap-atlas-build-") as tmp_name:
        tmp = Path(tmp_name)
        target = tmp / "atlas-mobile.qa.html"
        app_target = tmp / "atlas-app.js"
        if app.exists():
            shutil.copy2(app, app_target)
        run(
            sys.executable,
            "scripts/build-atlas-mobile.py",
            "--source",
            str(html),
            "--target",
            str(target),
            "--app",
            str(app_target),
            "--combined",
            "--legacy-full-artifact",
        )
        mobile_paths = [target] + ([app_target] if app_target.exists() else [])
        mobile_first = digest(mobile_paths)
        run(
            sys.executable,
            "scripts/build-atlas-mobile.py",
            "--source",
            str(html),
            "--target",
            str(target),
            "--app",
            str(app_target),
            "--combined",
            "--legacy-full-artifact",
        )
        mobile_second = digest(mobile_paths)
        if mobile_first != mobile_second:
            fail("responsive mobile generation is not deterministic")
        run("node", "scripts/test-atlas-navigation-contract.mjs", str(html), str(target))

    if digest(protected) != protected_before:
        fail("verification mutated the source shell or controller")

    print(
        "ATLAS BUILD REPRODUCIBILITY OK: "
        f"map={map_second[:12]} mobile={mobile_second[:12]}"
    )


if __name__ == "__main__":
    main()
