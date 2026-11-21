"""Bilingual co-design animation source, arithmetic and safe SVG contracts."""
from pathlib import Path
from xml.etree import ElementTree as ET

root = Path(__file__).resolve().parents[1]
asset = root / "docs/assets/concept-animations"
pages = root / "docs/engineering/hardware/co-design"
svg = "{http://www.w3.org/2000/svg}"
for stem in ("checkpoint-spacing", "fp16-scaling-window"):
    still = ET.parse(asset / (stem + "-still.svg")).getroot()
    motion = ET.parse(asset / (stem + "-motion.svg")).getroot()
    assert still.get("viewBox") == motion.get("viewBox") == "0 0 640 360"
    for doc in (still, motion):
        assert doc.find(svg + "title") is not None
        assert doc.find(svg + "desc") is not None
        for node in doc.iter():
            assert node.tag not in (svg+"script", svg+"foreignObject", svg+"image", svg+"use")
            assert all(not key.lower().startswith("on") and not key.lower().endswith("href") for key in node.attrib)
    assert not list(still.iter(svg+"animate"))
    assert len(list(motion.iter(svg+"animate"))) >= 2
    for en in (True,False):
        p = pages / (("gradient-checkpointing" if stem == "checkpoint-spacing" else "mixed-precision") + (".md" if en else ".zh-TW.md"))
        content = p.read_text(encoding="utf-8")
        assert stem + "-motion.svg" in content and stem + "-still.svg" in content
        assert "data-motion-src" in content and "data-still-src" in content
        assert 'width="640"' in content and 'overflow-x:auto' in content
for n, held, scratch, peak in ((1,17,0,17),(2,9,1,10),(4,5,3,8),(8,3,7,10),(16,2,15,17)):
    assert held == 16//n+1 and scratch == n-1 and peak == 16//n+n
assert 2**-27 < 2**-25 and 2**-17 >= 2**-24
assert 2**15 <= 65504 and 2**17 > 65504
print("Co-design dual visual assets, bilingual links and arithmetic OK")
