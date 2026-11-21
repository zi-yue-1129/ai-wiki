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
for language in ("gradient-checkpointing.md", "gradient-checkpointing.zh-TW.md"):
    page = (pages / language).read_text(encoding="utf-8")
    assert chr(36)*2 + "\nM(s)=" in page
    assert r"A_0,A_s,\ldots,A_{16}" in page
for language in ("mixed-precision.md", "mixed-precision.zh-TW.md"):
    page = (pages / language).read_text(encoding="utf-8")
    assert r"8\le S\le1024" in page
    assert r"g_{\mathrm{low}}=2^{-27}" in page
print("Co-design dual visual assets, bilingual links, math markup and arithmetic OK")

# Checkpoint live counters and exact integer-power-of-two frames.
check = ET.parse(asset / "checkpoint-spacing-motion.svg").getroot()
count_texts = [n for n in check.iter(svg+"text") if n.find(svg+"animate") is not None and n.get("x") == "483"]
assert len(count_texts) == 10
for y, expected in ((133, (17,9,5,3,2)), (175, (0,1,3,7,15))):
    row = [n for n in count_texts if int(n.get("y")) == y]
    assert tuple(int(n.text) for n in row) == expected
    for index, node in enumerate(row):
        clock = node.find(svg+"animate")
        assert clock.get("calcMode") == "discrete" and clock.get("dur") == "12s"
        assert list(map(int,clock.get("values").split(";")))[:5] == [int(k==index) for k in range(5)]

fp = ET.parse(asset / "fp16-scaling-window-motion.svg").getroot()
frames = list(range(13)) + list(range(12,-1,-1)) + [0]
assert len(frames) == 27
dots = [n for n in fp.iter(svg+"circle") if n.find(svg+"animate") is not None]
assert len(dots) == 2
for origin, dot in zip((105,425), dots):
    clock = dot.find(svg+"animate")
    assert clock.get("calcMode") == "discrete"
    assert [int(v) for v in clock.get("values").split(";")] == [origin+10*k for k in frames]
    assert len(clock.get("keyTimes").split(";")) == len(frames)
statuses = {"LOW ZERO": lambda k:k<=2, "BOTH FINITE": lambda k:3<=k<=10, "HIGH INF": lambda k:k>=11}
all_text = list(fp.iter(svg+"text"))
for k in range(13):
    active = next(n for n in all_text if n.text == "S = "+str(2**k) and n.find(svg+"animate") is not None)
    assert [int(v) for v in active.find(svg+"animate").get("values").split(";")] == [int(step==k) for step in frames]
for label, condition in statuses.items():
    active = next(n for n in all_text if n.text == label and n.find(svg+"animate") is not None)
    assert [int(v) for v in active.find(svg+"animate").get("values").split(";")] == [int(condition(step)) for step in frames]
assert 2**(-27)*4 == 2**(-25) and 2**(-27)*8 == 2**(-24)
assert 2**5*1024 == 2**15 <= 65504 < 2**5*2048 == 2**16
for language in ("mixed-precision.md","mixed-precision.zh-TW.md"):
    page = (pages/language).read_text(encoding="utf-8")
    assert "S=2048" in page and "S=8" in page
print("Checkpoint live counts and exact binary16 stepwise regime changes OK")
