#!/usr/bin/env python3
"""Validate the wiki's animated GIF assets using Pillow, independent of the encoder."""

from pathlib import Path
import sys

from PIL import Image, UnidentifiedImageError

ASSETS = Path("docs/assets/concept-animations")
MAX_BYTES = 500 * 1024


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    size = path.stat().st_size
    if size > MAX_BYTES:
        errors.append(f"{path}: {size} bytes exceeds the 500 KiB web budget")
    try:
        with Image.open(path) as gif:
            if gif.format != "GIF":
                errors.append(f"{path}: not a GIF")
                return errors
            frames = getattr(gif, "n_frames", 1)
            loop = gif.info.get("loop")
            width, height = gif.size
            if frames < 2:
                errors.append(f"{path}: expected animation, got {frames} frame")
            if loop != 0:
                errors.append(f"{path}: expected infinite loop (loop=0), got {loop!r}")
            if width < 100 or height < 100:
                errors.append(f"{path}: unexpectedly small dimensions {gif.size}")
            total_ms = 0
            for index in range(frames):
                gif.seek(index)
                duration = gif.info.get("duration", 0)
                if not isinstance(duration, (int, float)) or duration <= 0:
                    errors.append(f"{path}: frame {index} has invalid duration {duration!r}")
                else:
                    total_ms += duration
                # Force Pillow's independent GIF/LZW decoder to materialise all pixels.
                rgba = gif.convert("RGBA")
                rgba.load()
                if rgba.size != (width, height):
                    errors.append(f"{path}: frame {index} has unexpected size")
            print(
                f"OK {path.name}: {width}x{height}, {frames} decoded frames, "
                f"{total_ms} ms/loop, {size} bytes"
            )
    except (OSError, ValueError, EOFError, UnidentifiedImageError) as exc:
        errors.append(f"{path}: Pillow decode failed: {exc}")
    return errors


def main() -> int:
    gifs = sorted(ASSETS.glob("*.gif"))
    if not gifs:
        print(f"ERROR: no GIFs found in {ASSETS}", file=sys.stderr)
        return 1
    errors = [error for path in gifs for error in validate(path)]
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    print(f"Checked {len(gifs)} GIFs; {len(errors)} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
