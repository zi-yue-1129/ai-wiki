#!/usr/bin/env python3
"""Validate self-contained SVG teaching animations and their bilingual embeds."""
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs/assets/concept-animations"
SVG_NS = "{http://www.w3.org/2000/svg}"
PAIRS = {
    "flashattention-streaming-tiles.svg": "theory/models/transformer/attention-variants/flash-attention/index",
    "lstm-write-retain-read.svg": "theory/models/rnn/gated-cells/lstm/index",
}


def validate(name: str, page_stem: str) -> list[str]:
    path = ASSETS / name
    problems = []
    if not path.is_file():
        return [f"Missing asset: {path}"]
    data = path.read_text(encoding="utf-8")
    if len(data.encode("utf-8")) > 24 * 1024:
        problems.append(f"{name}: exceeds 24 KiB")
    try:
        svg = ET.fromstring(data)
    except ET.ParseError as exc:
        return [f"{name}: malformed XML: {exc}"]
    if svg.tag != SVG_NS + "svg":
        problems.append(f"{name}: invalid SVG namespace")
    if svg.attrib.get("role") != "img" or svg.attrib.get("tabindex") != "0":
        problems.append(f"{name}: missing image role or keyboard focus")
    ids = {node.get("id") for node in svg.iter() if node.get("id")}
    labels = svg.attrib.get("aria-labelledby", "").split()
    if len(labels) != 2 or any(label not in ids for label in labels):
        problems.append(f"{name}: missing accessible title/description references")
    if svg.find(SVG_NS + "title") is None or svg.find(SVG_NS + "desc") is None:
        problems.append(f"{name}: missing title or description")
    for node in svg.iter():
        tag = node.tag.rsplit("}", 1)[-1]
        if tag in {"script", "foreignObject", "iframe", "image"}:
            problems.append(f"{name}: disallowed element {tag}")
        for key, value in node.attrib.items():
            attr = key.rsplit("}", 1)[-1].lower()
            if attr.startswith("on") or attr in {"href", "src"} and not value.startswith("#"):
                problems.append(f"{name}: unsafe attribute {key}={value}")
    if re.search(r"@import|url\s*\(\s*['\"]?\s*(?:https?:|//|data:)", data, re.I):
        problems.append(f"{name}: external stylesheet or resource")
    if "@keyframes" not in data or "prefers-reduced-motion" not in data:
        problems.append(f"{name}: missing motion or reduced-motion fallback")
    if "animation-play-state:paused" not in data:
        problems.append(f"{name}: missing pause on keyboard focus / hover")
    for suffix in (".md", ".zh-TW.md"):
        page = ROOT / "docs" / (page_stem + suffix)
        if not page.is_file():
            problems.append(f"{name}: missing page {page}")
            continue
        content = page.read_text(encoding="utf-8")
        link = "../../../../../assets/concept-animations/" + name
        if not re.search(r"!\[[^\]]+\]\(" + re.escape(link) + r"\)", content):
            problems.append(f"{name}: missing bilingual image in {page}")
        resolved = (page.parent / link).resolve()
        if resolved != path.resolve():
            problems.append(f"{name}: broken relative link from {page}")
    return problems


def main() -> int:
    errors = [error for name, page in PAIRS.items() for error in validate(name, page)]
    for error in errors:
        print("ERROR:", error, file=sys.stderr)
    print(f"Validated {len(PAIRS)} animated SVGs, {len(errors)} error(s)")
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
