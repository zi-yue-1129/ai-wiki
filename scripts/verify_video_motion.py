#!/usr/bin/env python3
"""Independent checks for GitHub-static / MkDocs-animated video teaching figures."""
from pathlib import Path
from xml.etree import ElementTree as ET
import re

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
ASSETS = DOCS / "assets" / "concept-animations"
VIDEO = DOCS / "theory" / "models" / "computer-vision" / "video"
PAIRS = {"vivit-factorised-attention": "vivit", "i3d-filter-inflation": "i3d"}
NS = "{http://www.w3.org/2000/svg}"
for stem, page in PAIRS.items():
    for kind in ("motion", "still"):
        path = ASSETS / f"{stem}-{kind}.svg"
        assert path.exists() and path.stat().st_size < 50_000, path
        root = ET.parse(path).getroot()
        assert root.tag == NS + "svg" and root.get("viewBox") == "0 0 800 440", path
        assert root.find(NS + "title") is not None and root.find(NS + "desc") is not None, path
        animations = [n for n in root.iter() if n.tag in (NS + "animate", NS + "animateMotion")]
        assert (len(animations) >= 3) if kind == "motion" else not animations, path
        for node in root.iter():
            assert node.tag.split("}")[-1] not in {"script", "foreignObject", "iframe", "image"}, path
            for attr, value in node.attrib.items():
                assert not re.search(r"javascript:|data:|https?://", value, re.I), (path, attr)
            if node in animations:
                assert node.get("repeatCount") == "indefinite" and node.get("dur", "").endswith("s"), path
    for lang in (".md", ".zh-TW.md"):
        doc = VIDEO / (page + lang)
        content = doc.read_text(encoding="utf-8")
        for kind in ("motion", "still"):
            ref = f"../../../../assets/concept-animations/{stem}-{kind}.svg"
            assert ref in content and (doc.parent / ref).resolve().exists(), (doc, kind)
        assert f"]({ref.replace('motion.svg', 'still.svg')})" in content, doc
        assert "CC BY-SA 4.0" in content, doc
print("Video motion: 4 SVGs, 4 bilingual page links, static-first GitHub previews OK")
