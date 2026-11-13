#!/usr/bin/env python3
"""Validate the causal-confusion and copycat static-first teaching assets."""
from pathlib import Path
from xml.etree import ElementTree as ET
import sys
root = Path("docs")
assets = root / "assets/concept-animations"
stems = ("causal-lamp-intervention", "copycat-action-lag")
pages = [root / f"theory/paradigms/imitation/behavioural-cloning/causal-confusion{s}" for s in (".md", ".zh-TW.md")]
errors = []
ns = "{http://www.w3.org/2000/svg}"
for stem in stems:
    for kind in ("motion", "still"):
        path = assets / f"{stem}-{kind}.svg"
        if not path.exists():
            errors.append(f"{path}: missing")
            continue
        if path.stat().st_size > 50*1024:
            errors.append(f"{path}: larger than 50 KiB")
        try:
            svg = ET.parse(path).getroot()
        except ET.ParseError as exc:
            errors.append(f"{path}: {exc}")
            continue
        if svg.tag != ns+"svg" or svg.get("viewBox") != "0 0 640 360":
            errors.append(f"{path}: invalid root or geometry")
        if svg.find(ns+"title") is None or svg.find(ns+"desc") is None:
            errors.append(f"{path}: missing accessibility metadata")
        anim = [node for node in svg.iter() if node.tag == ns+"animate"]
        if (kind == "motion") != bool(anim):
            errors.append(f"{path}: wrong animation state")
        if any(node.get("repeatCount") != "indefinite" for node in anim):
            errors.append(f"{path}: non-looping")
        if any(node.tag.split("}")[-1] in {"script", "foreignObject", "image", "iframe"} for node in svg.iter()):
            errors.append(f"{path}: unsafe element")
for page in pages:
    text = page.read_text(encoding="utf-8")
    for stem in stems:
        if f"{stem}-still.svg)" not in text or f"{stem}-motion.svg)" not in text:
            errors.append(f"{page}: broken motion/static link for {stem}")
    if "CC BY-SA 4.0" not in text:
        errors.append(f"{page}: license missing")
player = (root / "javascripts/concept-motion.js").read_text(encoding="utf-8")
for stem in stems:
    if stem+"-still.svg" not in player or stem+"-motion.svg" not in player:
        errors.append(f"player mapping missing for {stem}")
for err in errors:
    print("ERROR:", err, file=sys.stderr)
print(f"Causal imitation motion: {len(errors)} validation errors")
sys.exit(bool(errors))
