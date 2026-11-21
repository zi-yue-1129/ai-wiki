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

# Semantic distinction: one-segment peak scratch vs whole-sweep recreated activations.
for s, expected in ((1,0),(2,8),(4,12),(8,14),(16,15)):
    assert expected == (16//s)*(s-1) == 16-16//s
counter = next(n for n in check.iter(svg+"text") if n.text == "TOTAL REBUILT")
assert counter.get("x") == "391" and counter.get("y") == "202"
updated = [n for n in check.iter(svg+"text") if n.get("x") == "531" and n.find(svg+"animate") is not None]
assert tuple(int(n.text) for n in updated) == (0,8,12,14,15)
for index,node in enumerate(updated):
    clock = node.find(svg+"animate")
    assert clock.get("calcMode") == "discrete"
    assert list(map(int,clock.get("values").split(";"))) == [int(i==index) for i in (0,1,2,3,4,0)]
assert any(n.get("class") == "reduced-only" and n.text == "12" for n in check.iter(svg+"text"))
for language in ("gradient-checkpointing.md","gradient-checkpointing.zh-TW.md"):
    page = (pages/language).read_text(encoding="utf-8")
    assert r"B(s)=\frac{16}{s}(s-1)=16-\frac{16}{s}" in page
    assert "TOTAL REBUILT" in page

# Round-to-nearest-even: half of 2^-24 is the actual zero/nonzero cutoff.
assert 2**-25 == (2**-24)/2
background = [n for n in fp.iter(svg+"rect") if n.get("y") == "89" and n.get("height") == "179"]
assert [(n.get("x"),n.get("width")) for n in background] == [("95","30"),("125","410"),("535","30")]
assert any(n.tag == svg+"line" and n.get("x1") == n.get("x2") == "125" and n.get("y1") == "89" for n in fp.iter())
assert any(n.text == "2^-25 tie to 0" for n in fp.iter(svg+"text"))
for language in ("mixed-precision.md","mixed-precision.zh-TW.md"):
    page = (pages/language).read_text(encoding="utf-8")
    assert "2^{-25}" in page and "2^{-24}" in page
print("Whole-chain recomputation total and binary16 rounding-cutoff contracts OK")


# Active segment bracket: one replay segment, not all discarded tensors simultaneously.
brackets = [n for n in check.iter(svg+"path") if n.get("data-teaching-role") == "replay-segment"]
assert len(brackets) == 2
active_bracket = next(n for n in brackets if n.get("class") == "motion-only")
reduced_bracket = next(n for n in brackets if n.get("class") == "reduced-only")
positions = [f"M {108+29*(16-s)} 104 V 111 H 572 V 104" for s in (1,2,4,8,16,1)]
bracket_clock = active_bracket.find(svg+"animate")
assert bracket_clock.get("attributeName") == "d" and bracket_clock.get("calcMode") == "discrete"
assert bracket_clock.get("values").split(";") == positions
assert reduced_bracket.get("d") == positions[2]
assert active_bracket.get("opacity") == "0"
assert active_bracket.findall(svg+"animate")[1].get("attributeName") == "opacity"
assert active_bracket.findall(svg+"animate")[1].get("values") == "0;1;1;1;1;0"
for name in ("gradient-checkpointing.md", "gradient-checkpointing.zh-TW.md"):
    page = (pages/name).read_text(encoding="utf-8")
    assert ("amber bracket" in page) if name.endswith("ing.md") else ("橘色括號" in page)

# Common loss scale shifts both pre-rounding log2 magnitudes without narrowing their separation.
spans = [n for n in fp.iter(svg+"line") if n.get("data-teaching-role") == "common-scale-span"]
assert len(spans) == 2
active_span = next(n for n in spans if n.get("class") == "motion-only")
reduced_span = next(n for n in spans if n.get("class") == "reduced-only")
coordinates = {a.get("attributeName"): [int(v) for v in a.get("values").split(";")] for a in active_span.findall(svg+"animate")}
assert set(coordinates) == {"x1", "x2"}
assert len(coordinates["x1"]) == len(coordinates["x2"]) == 27
assert all(y - x == 320 for x,y in zip(coordinates["x1"], coordinates["x2"]))
assert coordinates["x1"][:4] == [105,115,125,135]
assert coordinates["x2"][11:14] == [535,545,545]
assert reduced_span.get("x1") == "205" and reduced_span.get("x2") == "525"
assert 5 - (-27) == 32
for name in ("mixed-precision.md", "mixed-precision.zh-TW.md"):
    page = (pages/name).read_text(encoding="utf-8")
    assert "32" in page and r"\log_2" in page
print("Segment replay bracket and fixed common-scale exponent spread OK")

# The checkpoint scene gives the arithmetic behind the peak curve in every state.
# The reduced-motion replacement must show the s=4 optimum without SMIL.
sums = [n for n in check.iter(svg+"text")
        if n.get("x") == "142" and n.find(svg+"animate") is not None]
assert [n.text for n in sums] == [
    "17 + 0 = 17", "9 + 1 = 10", "5 + 3 = 8",
    "3 + 7 = 10", "2 + 15 = 17",
]
for i, node in enumerate(sums):
    frame = node.find(svg+"animate")
    expected = ["1" if j == i else "0" for j in range(5)]
    assert frame is not None
    assert frame.get("values").split(";")[:5] == expected
assert any(n.text == "5 + 3 = 8" and n.get("class") == "reduced-only"
           for n in check.iter(svg+"text"))
# Avoid a single unbreakable 32-exponent inline equation on a 390px viewport.
for suffix in (".md", ".zh-TW.md"):
    checkpoint = (pages / ("gradient-checkpointing" + suffix)).read_text(encoding="utf-8")
    mixed = (pages / ("mixed-precision" + suffix)).read_text(encoding="utf-8")
    assert "PEAK SLOTS" in checkpoint
    assert r"\begin{aligned}" in mixed
    assert r"\log_2\frac" in mixed
    assert r"\log_2|Sg_" not in mixed


# A real forward-replay cursor traverses only the active checkpoint segment.
cursor = [n for n in check.iter(svg + "circle")
          if n.get("data-teaching-role") == "segment-replay-cursor"]
assert len(cursor) == 1
cursor_node = cursor[0]
assert cursor_node.get("class") == "motion-only" and cursor_node.get("cy") == "111"
cursor_clocks = {n.get("attributeName"): n for n in cursor_node.findall(svg + "animate")}
assert set(cursor_clocks) == {"cx", "opacity"}
expected_keys = "0;0.2;0.38;0.4;0.4001;0.58;0.6;0.6001;0.78;0.8;0.8001;0.98;1"
assert cursor_clocks["cx"].get("keyTimes") == expected_keys
assert cursor_clocks["cx"].get("values") == "543;514;572;572;456;572;572;340;572;572;108;572;572"
assert cursor_clocks["cx"].get("calcMode") == "linear"
assert cursor_clocks["opacity"].get("values") == "0;1;1;1;1;1;1;1;1;1;1;1;0"
assert cursor_clocks["opacity"].get("calcMode") == "discrete"
assert all(clock.get("dur") == "12s" for clock in cursor_clocks.values())
for name in ("gradient-checkpointing.md", "gradient-checkpointing.zh-TW.md"):
    page = (pages / name).read_text(encoding="utf-8")
    assert "forward recomputation" in page if name.endswith("ing.md") else "前向重算" in page

# The two gradient rows distinguish raw plotted magnitude from rounded FP16 fate.
rounded = [n for n in fp.iter(svg + "g")
           if n.get("data-teaching-role") == "rounded-outcomes"]
assert len(rounded) == 1
rounded_animated = [n for n in rounded[0].iter(svg + "text")
                    if n.find(svg + "animate") is not None]
assert [(n.get("y"), n.text) for n in rounded_animated] == [
    ("153", "0"), ("153", "OK"), ("218", "OK"), ("218", "INF")]
masks = (lambda k: k < 3, lambda k: k >= 3,
         lambda k: k <= 10, lambda k: k > 10)
for node, cond in zip(rounded_animated, masks):
    clock = node.find(svg + "animate")
    assert clock.get("calcMode") == "discrete" and clock.get("dur") == "12s"
    assert [int(v) for v in clock.get("values").split(";")] == [
        int(cond(k)) for k in frames]
    assert len(clock.get("keyTimes").split(";")) == len(frames)
# The static reduced-motion state is S=1024: LOW/HIGH are both OK.
reduced_group = next(n for n in rounded[0].findall(svg + "g")
                     if n.get("class") == "reduced-only")
assert [(n.get("y"), n.text) for n in reduced_group.findall(svg + "text")] == [
    ("153", "OK"), ("218", "OK")]
for name in ("mixed-precision.md", "mixed-precision.zh-TW.md"):
    page = (pages / name).read_text(encoding="utf-8")
    assert "LOW" in page and "HIGH" in page and "INF" in page
print("Forward replay and individually rounded FP16 outcomes OK")

# Browser-reviewed live replay trace and constant binary-exponent gap annotation.
progress = [n for n in check.iter(svg+"line") if n.get("data-teaching-role") == "replay-progress-trace"]
assert len(progress) == 1
trail = progress[0]
assert trail.get("class") == "motion-only" and trail.get("opacity") == "0"
track = {a.get("attributeName"): a for a in trail.findall(svg+"animate")}
assert set(track) == {"x1", "x2", "opacity"}
assert track["x1"].get("values") == "543;514;456;340;108;543"
assert track["x2"].get("values") == next(n for n in check.iter(svg+"circle") if n.get("data-teaching-role") == "segment-replay-cursor").find(svg+"animate").get("values")
assert track["opacity"].get("values").split(";")[0] == "0"
readouts = [n for n in fp.iter(svg+"g") if n.get("data-teaching-role") == "log-gap-readout"]
assert {n.get("class") for n in readouts} == {"motion-only", "reduced-only"}
for readout in readouts:
    assert any("Δ log₂ = 32" in (n.text or "") for n in readout.iter(svg+"text"))
active_gap = next(n for n in readouts if n.get("class") == "motion-only")
travel = active_gap.find(svg+"animateTransform")
assert travel is not None and travel.get("calcMode") == "discrete"
assert travel.get("type") == "translate"
assert [int(s.split()[0]) for s in travel.get("values").split(";")] == [10*k for k in frames]
assert len(travel.get("keyTimes").split(";")) == 27
for name in ("gradient-checkpointing.md", "gradient-checkpointing.zh-TW.md"):
    assert ("trace" if name.endswith("ing.md") else "軌跡") in (pages/name).read_text(encoding="utf-8")
for name in ("mixed-precision.md", "mixed-precision.zh-TW.md"):
    assert "Δ log₂ = 32" in (pages/name).read_text(encoding="utf-8")
print("Checkpoint active-segment replay trace and invariant log-gap badge contracts OK")


# Browser-reviewed reconstruction dots: missing activations are recreated sequentially
# within the *last* active segment.  No dots are added to persistent boundaries.
checkpoint_dots = [
    n for n in check.iter(svg+"circle")
    if n.get("data-teaching-role") == "rebuilt-activation"
]
moving_dots = [n for n in checkpoint_dots if n.get("class") == "motion-only"]
still_dots = [n for n in checkpoint_dots if n.get("class") == "reduced-only"]
assert [int(n.get("data-boundary")) for n in moving_dots] == list(range(1,16))
assert [int(n.get("data-boundary")) for n in still_dots] == [13,14,15]
for j, dot in enumerate(moving_dots, start=1):
    assert dot.get("cx") == str(108+29*j) and dot.get("cy") == "89"
    assert dot.get("opacity") == "0"
    clock = dot.find(svg+"animate")
    assert clock.get("attributeName") == "opacity"
    assert clock.get("calcMode") == "discrete" and clock.get("dur") == "12s"
    expected = [(0,0)]
    for stage, segment in enumerate((1,2,4,8,16)):
        if segment > 1 and j > 16-segment:
            expected.extend([
                (stage/5+0.18*(j-(16-segment))/segment,1),
                ((stage+1)/5,0),
            ])
    assert clock.get("keyTimes") == ";".join(f"{time:.6f}" for time,_ in expected)
    assert clock.get("values") == ";".join(str(state) for _,state in expected)
for name in ("gradient-checkpointing.md", "gradient-checkpointing.zh-TW.md"):
    chapter=(pages/name).read_text(encoding="utf-8")
    assert "three temporary reconstructed boundaries" in chapter if name.endswith("ing.md") else "橘色小點" in chapter

# FP16 finite-gradient gate distinguishes zero underflow from nonfinite overflow.
gate_nodes = [n for n in fp.iter(svg+"g") if n.get("data-teaching-role") == "optimizer-step-gate"]
assert len(gate_nodes) == 1
gate = gate_nodes[0]
gate_texts = [n for n in gate.iter(svg+"text") if n.find(svg+"animate") is not None]
assert [n.text for n in gate_texts] == ["STEP ELIGIBLE", "SKIP (INF)"]
for node, is_on in zip(gate_texts,(lambda k:k<=10,lambda k:k>=11)):
    clock=node.find(svg+"animate")
    assert clock.get("dur")=="12s" and clock.get("calcMode")=="discrete"
    assert len(clock.get("keyTimes").split(";"))==27
    assert [int(v) for v in clock.get("values").split(";")]==[int(is_on(k)) for k in frames]
assert any(n.get("class")=="reduced-only" and n.text=="STEP ELIGIBLE" for n in gate.iter(svg+"text"))
for name in ("mixed-precision.md","mixed-precision.zh-TW.md"):
    chapter=(pages/name).read_text(encoding="utf-8")
    assert "STEP ELIGIBLE" in chapter and "SKIP (INF)" in chapter
    assert "https://docs.pytorch.org/docs/stable/notes/amp_examples.html" in chapter
print("Rebuilt activation sequence and Inf/NaN optimizer gate timing contracts OK")
