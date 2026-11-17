"""Render exact SVG assets at desktop and mobile widths for visual QA.

Usage:
  python scripts/render_learning_rate_qa.py --output /tmp/lr-qa
  python scripts/render_learning_rate_qa.py --output /tmp/lr-qa --chromium /usr/bin/chromium

Inspect every generated PNG manually before marking visual QA complete.
This tool does not claim to automate aesthetic or accessibility review.
"""
from __future__ import annotations

import argparse
import shutil
import struct
import subprocess
import tempfile
from pathlib import Path

ASSETS = Path(__file__).resolve().parents[1] / "docs/assets/concept-animations"
NAMES = ("sgdr-restart", "clr-triangular2")
WIDTHS = (360, 640, 1024)


def png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise RuntimeError(f"Not a PNG: {path}")
    return struct.unpack(">II", data[16:24])


def render(chromium: str, source: Path, destination: Path, width: int) -> None:
    # A generous viewport height prevents accidental browser screenshot cropping.
    # Chromium's SVG image viewport scales the 640x300 SVG to viewport width.
    with tempfile.TemporaryDirectory(prefix="lr-browser-") as profile:
        command = [
            chromium, "--headless", "--no-sandbox", "--disable-gpu",
            "--hide-scrollbars", "--disable-extensions", "--disable-background-networking",
            "--force-device-scale-factor=1", "--force-prefers-reduced-motion",
            f"--user-data-dir={profile}", f"--window-size={width},400",
            f"--screenshot={destination}", source.resolve().as_uri(),
        ]
        result = subprocess.run(command, capture_output=True, text=True, timeout=35)
    if result.returncode != 0 or not destination.exists():
        raise RuntimeError(f"Chromium failed for {source.name}: {result.stderr[-1200:]}")
    actual_width, actual_height = png_size(destination)
    if actual_width < width or actual_height < 300:
        raise RuntimeError(f"Unexpected screenshot dimensions: {destination}: {actual_width}x{actual_height}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--chromium", default=None)
    args = parser.parse_args()
    chromium = args.chromium or shutil.which("chromium") or shutil.which("google-chrome")
    if not chromium:
        parser.error("Chromium not found; specify --chromium")
    args.output.mkdir(parents=True, exist_ok=True)
    for name in NAMES:
        for variant in ("still", "motion"):
            source = ASSETS / f"{name}-{variant}.svg"
            if not source.is_file():
                raise FileNotFoundError(source)
            for width in WIDTHS:
                output = args.output / f"{name}-{variant}-{width}px.png"
                render(chromium, source, output, width)
                print(f"Rendered {output} ({png_size(output)})")
    print("Screenshots generated. Human inspection of all sizes is still REQUIRED.")


if __name__ == "__main__":
    main()
