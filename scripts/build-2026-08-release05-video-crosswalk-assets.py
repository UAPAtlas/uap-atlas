#!/usr/bin/env python3
"""Build labeled still contact sheets from officially crosswalked Release 05 videos.

Requires --video-dir pointing to the retained Release 05 MP4 directory. The path is
never written into output metadata.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "assets/sources/PURSUE-RELEASE-05"
GOM = [
    ("DOW-UAP-PR117", "DOD_111887401.mp4", 16.666667),
    ("DOW-UAP-PR118", "DOD_111887407.mp4", 30.2),
    ("DOW-UAP-PR119", "DOD_111887421.mp4", 2.8),
    ("DOW-UAP-PR120", "DOD_111887427.mp4", 13.266667),
    ("DOW-UAP-PR121", "DOD_111887439.mp4", 34.4),
    ("DOW-UAP-PR122", "DOD_111887446.mp4", 26.333333),
]
D032 = ("FBI-UAP-PR007", "DOD_111887430.mp4", 10.0)


def font(size: int, bold: bool = False):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def extract(video: Path, second: float, output: Path):
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-ss", f"{second:.3f}", "-i", str(video), "-frames:v", "1", str(output)],
        check=True,
    )


def text(draw, xy, value, size, fill, bold=False):
    draw.text(xy, value, font=font(size, bold), fill=fill)


def gom_sheet(video_dir: Path, output: Path):
    width, header, cell_w, cell_h, gap = 1920, 150, 600, 410, 20
    canvas = Image.new("RGB", (width, header + 2 * cell_h + 3 * gap), "#090d13")
    draw = ImageDraw.Draw(canvas)
    text(draw, (30, 22), "GULF OF OMAN · D101 · OFFICIAL VIDEO CROSSWALK", 38, "#f4f7fb", True)
    text(draw, (30, 78), "PR117–PR122 · Secondary recordings of an AC-130J infrared display · NOT native sensor data", 25, "#f2b84b", True)
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for idx, (pr, filename, duration) in enumerate(GOM):
            frame = tmp / f"{pr}.jpg"
            extract(video_dir / filename, duration / 2, frame)
            im = Image.open(frame).convert("RGB")
            im = ImageOps.fit(im, (cell_w, cell_h - 55), method=Image.Resampling.LANCZOS)
            row, col = divmod(idx, 3)
            x, y = gap + col * (cell_w + gap), header + gap + row * (cell_h + gap)
            canvas.paste(im, (x, y))
            draw.rectangle((x, y + cell_h - 55, x + cell_w, y + cell_h), fill="#111923")
            text(draw, (x + 14, y + cell_h - 46), f"{pr}  ·  {filename.removesuffix('.mp4')}", 24, "#e8edf4", True)
    canvas.save(output, quality=92, optimize=True)


def d032_sheet(video_dir: Path, output: Path):
    header, cell_w, cell_h, gap = 155, 480, 360, 12
    width = 5 * cell_w + 6 * gap
    height = header + 2 * cell_h + 3 * gap
    canvas = Image.new("RGB", (width, height), "#090d13")
    draw = ImageDraw.Draw(canvas)
    text(draw, (28, 20), "FBI-UAP-PR007 · D032 · RELEASED EVENT FOOTAGE", 38, "#f4f7fb", True)
    text(draw, (28, 76), "Ten-second thermal-optics clip · Two black-hot contrast areas · Identity, range, scale and speed NOT established", 24, "#f2b84b", True)
    text(draw, (28, 113), "Official release association does not make the FBI interview an FBI factual conclusion.", 21, "#c8d1dc")
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        video = video_dir / D032[1]
        for idx in range(10):
            frame = tmp / f"frame-{idx:02d}.jpg"
            extract(video, idx + 0.25, frame)
            im = Image.open(frame).convert("RGB")
            im = ImageOps.fit(im, (cell_w, cell_h), method=Image.Resampling.LANCZOS)
            row, col = divmod(idx, 5)
            x, y = gap + col * (cell_w + gap), header + gap + row * (cell_h + gap)
            canvas.paste(im, (x, y))
            draw.rectangle((x + 8, y + 8, x + 86, y + 42), fill="#0b1119")
            text(draw, (x + 15, y + 11), f"+{idx:02d}s", 20, "#f4f7fb", True)
    canvas.save(output, quality=92, optimize=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--video-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    required = [filename for _, filename, _ in GOM] + [D032[1]]
    missing = [name for name in required if not (args.video_dir / name).is_file()]
    if missing:
        raise SystemExit(f"Missing required videos: {missing}")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    outputs = [
        args.output_dir / "DOW-UAP-D101-PR117-PR122-video-contact.jpg",
        args.output_dir / "FBI-UAP-D032-PR007-video-contact.jpg",
    ]
    gom_sheet(args.video_dir, outputs[0])
    d032_sheet(args.video_dir, outputs[1])
    print(json.dumps([
        {"file": str(path.relative_to(ROOT)), "bytes": path.stat().st_size, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
        for path in outputs
    ], indent=2))


if __name__ == "__main__":
    main()
