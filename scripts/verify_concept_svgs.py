#!/usr/bin/env python3
"""Validate SVG concept diagrams and their bilingual Markdown references.

Uses the Python standard-library XML parser (not a regex-only SVG check).
"""
from __future__ import annotations

from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path("docs")
ASSETS = ROOT / "assets" / "concept-animations"
SVG_NS = "http://www.w3.org/2000/svg"
XLINK = "{http://www.w3.org/1999/xlink}href"
MANIFEST = {
    "moe-sparse-routing.svg": "theory/models/mixture-of-experts/index",
    "cfg-vector-guidance.svg": "theory/paradigms/unsupervised/density-and-generative-models/diffusion/classifier-free-guidance",
    "gradient-norm-clipping.svg": "theory/optimization/norm-clipping",
}


def validate(path: Path) -> list[str]:
    issues: list[str] = []
    content = path.read_text(encoding="utf-8")
    try:
        tree = ET.fromstring(content)
    except ET.ParseError as exc:
        return [f"{path}: invalid XML: {exc}"]
    if tree.tag != f"{{{SVG_NS}}}svg":
        issues.append(f"{path}: missing SVG namespace/root")
    if not tree.get("viewBox"):
        issues.append(f"{path}: missing viewBox for responsive rendering")
    for required in ("title", "desc"):
        if tree.find(f"{{{SVG_NS}}}{required}") is None:
            issues.append(f"{path}: missing accessible {required}")
    for el in tree.iter():
        local_name = el.tag.rsplit("}", 1)[-1]
        if local_name in {"script", "foreignObject", "image"}:
            issues.append(f"{path}: prohibited element {local_name}")
        for key, value in el.attrib.items():
            key_name = key.rsplit("}", 1)[-1]
            if key_name.startswith("on"):
                issues.append(f"{path}: prohibited event handler {key_name}")
            if (key_name == "href" or key == XLINK) and (
                "://" in value or value.startswith(("javascript:", "data:"))
            ):
                issues.append(f"{path}: external or active URL prohibited")
    if "@keyframes" in content and "prefers-reduced-motion" not in content:
        issues.append(f"{path}: animation missing reduced-motion fallback")
    if path.stat().st_size > 50 * 1024:
        issues.append(f"{path}: larger than 50 KiB SVG budget")
    return issues


def main() -> int:
    issues: list[str] = []
    for svg in sorted(ASSETS.glob("*.svg")):
        issues += validate(svg)
        print(f"SVG {svg.name}: {svg.stat().st_size} bytes")
    for name, stem in MANIFEST.items():
        svg_path = ASSETS / name
        if not svg_path.is_file():
            issues.append(f"{svg_path}: missing expected diagram")
            continue
        for language_suffix in (".md", ".zh-TW.md"):
            page = ROOT / f"{stem}{language_suffix}"
            if not page.exists():
                issues.append(f"{page}: missing page")
                continue
            markdown = page.read_text(encoding="utf-8")
            links = re.findall(r"!\[[^\]]+\]\(([^)]+\.svg)\)", markdown)
            resolved = {(page.parent / link).resolve() for link in links}
            if svg_path.resolve() not in resolved:
                issues.append(f"{page}: missing or broken reference to {name}")
    for issue in issues:
        print(f"ERROR: {issue}", file=sys.stderr)
    print(f"Checked concept SVGs and bilingual references: {len(issues)} issue(s)")
    return bool(issues)


if __name__ == "__main__":
    raise SystemExit(main())
