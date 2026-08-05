#!/usr/bin/env python3
"""Generate bounded WebP derivatives for heavy Atlas display images."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any
from urllib.parse import quote

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "image-derivatives.json"
RUNTIME = ROOT / "image-derivatives.js"
EXCLUDES = ROOT / "assets/image-derivatives-exclude.txt"
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
DEFAULT_THRESHOLD = 350_000
DISPLAY_MAX = 1600
THUMB_MAX = 360
DISPLAY_QUALITY = 84
THUMB_QUALITY = 76
RAW_ROOT = "https://raw.githubusercontent.com/UAPAtlas/uap-atlas/main/"
Image.MAX_IMAGE_PIXELS = None


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def clean_local_path(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    raw = value.strip().split("#", 1)[0].split("?", 1)[0]
    if not raw or re.match(r"^(?:https?:|data:|blob:|file:)", raw, re.I):
        return None
    raw = raw.removeprefix("./").lstrip("/")
    if not raw.startswith("assets/") or Path(raw).suffix.lower() not in IMAGE_EXTENSIONS:
        return None
    return raw


def collect_images() -> list[str]:
    atlas = json.loads((ROOT / "atlas-data.json").read_text())
    source_index = json.loads((ROOT / "source-file-index.json").read_text())
    paths: set[str] = set()

    def add(value: object) -> None:
        if isinstance(value, dict):
            for key in ("url", "src", "image"):
                candidate = clean_local_path(value.get(key))
                if candidate:
                    paths.add(candidate)
                    return
        candidate = clean_local_path(value)
        if candidate:
            paths.add(candidate)

    for values in source_index.values():
        for value in values:
            add(value)
    for case in atlas.get("cases", []):
        add(case.get("image"))
        add((case.get("heroVisual") or {}).get("src"))
        for key in ("images", "evidenceImages"):
            for value in case.get(key, []) or []:
                add(value)
        for item in case.get("culturalLegacy", []) or []:
            add((item or {}).get("image"))
    return sorted(path for path in paths if (ROOT / path).is_file())


def derivative_path(original: str, variant: str) -> str:
    rel = Path(original).relative_to("assets")
    return (Path("assets/derivatives") / variant / rel.parent / f"{rel.name}.webp").as_posix()


def prepared_image(source: Path) -> Image.Image:
    with Image.open(source) as opened:
        if getattr(opened, "is_animated", False):
            opened.seek(0)
        image = ImageOps.exif_transpose(opened)
        image.load()
    if "A" in image.getbands():
        return image.convert("RGBA")
    return image.convert("RGB")


def write_webp(image: Image.Image, destination: Path, max_dimension: int, quality: int) -> None:
    output = image.copy()
    output.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(destination.suffix + ".tmp")
    output.save(temporary, "WEBP", quality=quality, method=6, exact=True)
    temporary.replace(destination)


def file_record(path: Path) -> dict[str, object]:
    with Image.open(path) as image:
        width, height = image.size
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "bytes": path.stat().st_size,
        "width": width,
        "height": height,
        "sha256": sha256(path),
    }


def expected_sources(threshold: int) -> list[str]:
    return [path for path in collect_images() if (ROOT / path).stat().st_size > threshold]


def build(threshold: int) -> dict[str, Any]:
    entries: dict[str, dict[str, Any]] = {}
    original_total = display_total = thumb_total = 0
    sources = expected_sources(threshold)
    source_hash = hashlib.sha256()

    for index, original in enumerate(sources, 1):
        source = ROOT / original
        source_sha = sha256(source)
        source_hash.update(original.encode())
        source_hash.update(source_sha.encode())
        display = ROOT / derivative_path(original, "display")
        thumb = ROOT / derivative_path(original, "thumb")
        image = prepared_image(source)
        write_webp(image, display, DISPLAY_MAX, DISPLAY_QUALITY)
        write_webp(image, thumb, THUMB_MAX, THUMB_QUALITY)
        original_bytes = source.stat().st_size
        original_total += original_bytes
        display_total += display.stat().st_size
        thumb_total += thumb.stat().st_size
        with Image.open(source) as opened:
            original_width, original_height = opened.size
        entries[original] = {
            "originalBytes": original_bytes,
            "originalWidth": original_width,
            "originalHeight": original_height,
            "originalSha256": source_sha,
            "originalUrl": RAW_ROOT + quote(original, safe="/"),
            "display": file_record(display),
            "thumb": file_record(thumb),
        }
        if index % 25 == 0 or index == len(sources):
            print(f"derivatives: {index}/{len(sources)}")

    expected_derivatives = {
        ROOT / record[variant]["path"]
        for record in entries.values()
        for variant in ("display", "thumb")
    }
    derivative_root = ROOT / "assets/derivatives"
    if derivative_root.exists():
        for existing in derivative_root.rglob("*.webp"):
            if existing not in expected_derivatives:
                existing.unlink()
        for directory in sorted(derivative_root.rglob("*"), reverse=True):
            if directory.is_dir() and not any(directory.iterdir()):
                directory.rmdir()

    payload = {
        "schemaVersion": 1,
        "policy": "heavy-image-bounded-derivatives",
        "sourceFingerprint": source_hash.hexdigest(),
        "thresholdBytes": threshold,
        "displayMaxDimension": DISPLAY_MAX,
        "thumbMaxDimension": THUMB_MAX,
        "displayQuality": DISPLAY_QUALITY,
        "thumbQuality": THUMB_QUALITY,
        "summary": {
            "imageCount": len(entries),
            "originalBytes": original_total,
            "displayBytes": display_total,
            "thumbBytes": thumb_total,
        },
        "entries": entries,
    }
    serialized = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    MANIFEST.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    RUNTIME.write_text(f"window.imageDerivativeIndex={serialized};\n")
    EXCLUDES.write_text("".join(f"/{path}\n" for path in entries))
    return payload


def check(threshold: int) -> dict[str, Any]:
    if not MANIFEST.exists() or not RUNTIME.exists() or not EXCLUDES.exists():
        raise SystemExit("IMAGE DERIVATIVE CHECK FAILED: generated contract files are missing")
    payload = json.loads(MANIFEST.read_text())
    expected = expected_sources(threshold)
    if payload.get("schemaVersion") != 1 or payload.get("thresholdBytes") != threshold:
        raise SystemExit("IMAGE DERIVATIVE CHECK FAILED: schema or threshold mismatch")
    if sorted(payload.get("entries", {})) != expected:
        raise SystemExit("IMAGE DERIVATIVE CHECK FAILED: manifest source set is stale")
    original_total = display_total = thumb_total = 0
    source_hash = hashlib.sha256()
    for original, record in payload["entries"].items():
        source = ROOT / original
        source_sha = sha256(source)
        source_hash.update(original.encode())
        source_hash.update(source_sha.encode())
        if source_sha != record.get("originalSha256") or source.stat().st_size != record.get("originalBytes"):
            raise SystemExit(f"IMAGE DERIVATIVE CHECK FAILED: original drift for {original}")
        original_total += source.stat().st_size
        for variant in ("display", "thumb"):
            derivative = ROOT / record[variant]["path"]
            if not derivative.is_file() or sha256(derivative) != record[variant].get("sha256"):
                raise SystemExit(f"IMAGE DERIVATIVE CHECK FAILED: invalid {variant} for {original}")
            with Image.open(derivative) as image:
                image.verify()
            if max(record[variant]["width"], record[variant]["height"]) > (DISPLAY_MAX if variant == "display" else THUMB_MAX):
                raise SystemExit(f"IMAGE DERIVATIVE CHECK FAILED: oversized {variant} for {original}")
            if variant == "display":
                display_total += derivative.stat().st_size
            else:
                thumb_total += derivative.stat().st_size
    if payload.get("sourceFingerprint") != source_hash.hexdigest():
        raise SystemExit("IMAGE DERIVATIVE CHECK FAILED: source fingerprint mismatch")
    summary = payload.get("summary", {})
    expected_summary = {
        "imageCount": len(expected),
        "originalBytes": original_total,
        "displayBytes": display_total,
        "thumbBytes": thumb_total,
    }
    if summary != expected_summary:
        raise SystemExit("IMAGE DERIVATIVE CHECK FAILED: summary mismatch")
    serialized = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    if RUNTIME.read_text() != f"window.imageDerivativeIndex={serialized};\n":
        raise SystemExit("IMAGE DERIVATIVE CHECK FAILED: browser runtime is stale")
    exclude_lines = EXCLUDES.read_text().splitlines()
    if exclude_lines != [f"/{path}" for path in expected]:
        raise SystemExit("IMAGE DERIVATIVE CHECK FAILED: rsync exclusion list is stale")
    print(
        "IMAGE DERIVATIVE CHECK OK: "
        f"{len(expected)} images · originals={original_total / 1048576:.1f} MiB · "
        f"display={display_total / 1048576:.1f} MiB · thumbs={thumb_total / 1048576:.1f} MiB"
    )
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--threshold", type=int, default=DEFAULT_THRESHOLD)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        check(args.threshold)
    else:
        payload = build(args.threshold)
        print(
            "IMAGE DERIVATIVES BUILT: "
            f"{payload['summary']['imageCount']} images · "
            f"display={payload['summary']['displayBytes'] / 1048576:.1f} MiB · "
            f"thumbs={payload['summary']['thumbBytes'] / 1048576:.1f} MiB"
        )


if __name__ == "__main__":
    main()
