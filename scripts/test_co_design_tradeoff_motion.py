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


# GitHub's non-animated fallback must expose the same conditional step decision
# for the illustrative underflow / finite / overflow cases, without SMIL.
fp16_still = ET.parse(asset / "fp16-scaling-window-still.svg").getroot()
assert not list(fp16_still.iter(svg+"animate"))
decision_labels = [
    n for n in fp16_still.iter(svg+"text")
    if (n.text or "").strip() in ("STEP ELIGIBLE", "SKIP (INF)")
]
assert [n.text for n in decision_labels] == ["STEP ELIGIBLE", "STEP ELIGIBLE", "SKIP (INF)"]
assert [n.get("y") for n in decision_labels] == ["298", "298", "298"]
for name in ("UNDERFLOW", "BOTH FINITE", "OVERFLOW"):
    assert any(n.text == name and n.get("y") == "280"
               for n in fp16_still.iter(svg+"text"))
print("GitHub FP16 finite-step fallback comparison OK")


# Dynamic GradScaler feedback: six consecutive optimizer-step checks.
for stem in ("gradscaler-feedback-motion", "gradscaler-feedback-still"):
    doc = ET.parse(asset / (stem + ".svg")).getroot()
    assert doc.get("viewBox") == "0 0 640 360"
    assert doc.find(svg + "title") is not None and doc.find(svg + "desc") is not None
    for node in doc.iter():
        assert node.tag not in {svg + "script", svg + "foreignObject", svg + "image", svg + "use"}
        assert not any(k.lower().startswith("on") or k.lower().endswith("href") for k in node.attrib)
    clocks = list(doc.iter(svg + "animate"))
    if stem.endswith("-motion"):
        assert len(clocks) == 8
        assert [c.get("attributeName") for c in clocks] == ["cx", "cy"] + ["opacity"] * 6
        assert clocks[0].get("values") == "133;218;303;388;473;558;133"
        assert clocks[1].get("values") == "185;185;115;185;185;115;185"
        assert all(c.get("dur") == "12s" and c.get("repeatCount") == "indefinite" for c in clocks)
    else:
        assert not clocks
scale, consecutive = 1024, 0
scales, checks, upcoming = [], [], []
for _ in range(6):
    scales.append(scale)
    overflow = (2**5 * scale > 65504)
    checks.append("INF" if overflow else "OK")
    if overflow:
        scale, consecutive = int(scale * 0.5), 0
    else:
        consecutive += 1
        if consecutive == 2:
            scale, consecutive = scale * 2, 0
    upcoming.append(scale)
assert scales == [1024, 1024, 2048, 1024, 1024, 2048]
assert checks == ["OK", "OK", "INF", "OK", "OK", "INF"]
assert upcoming == [1024, 2048, 1024, 1024, 2048, 1024]
for chapter in ("mixed-precision.md", "mixed-precision.zh-TW.md"):
    contents = (pages / chapter).read_text(encoding="utf-8")
    assert "gradscaler-feedback-motion.svg" in contents
    assert "gradscaler-feedback-still.svg" in contents
    assert "data-motion-src" in contents
    assert "growth_interval=2" in contents
    assert "https://docs.pytorch.org/docs/stable/amp.html" in contents
print("Dynamic GradScaler six-step control-loop, fallback and bilingual integration OK")


# The published preview must expose the following scale even without SMIL.
# At each animated time, the finite streak is unique and agrees with the scale update.
for stem in ("gradscaler-feedback-motion", "gradscaler-feedback-still"):
    doc = ET.parse(asset / (stem + ".svg")).getroot()
    row = [n for n in doc.iter(svg + "g")
           if n.get("data-teaching-role") == "next-scale-row"]
    assert len(row) == 1
    assert [int(n.text) for n in row[0].findall(svg + "text")[1:]] == [
        1024, 2048, 1024, 1024, 2048, 1024]
    if stem.endswith("-motion"):
        live = [n for n in doc.iter(svg + "text")
                if n.get("data-teaching-role") == "finite-streak"]
        assert len(live) == 6
        assert all(n.get("class") == "live" for n in live)
        assert [n.text.split(" · ")[0] for n in live] == [
            "t1", "t2", "t3", "t4", "t5", "t6"]
        for i, n in enumerate(live):
            clock = n.find(svg + "animate")
            assert clock.get("attributeName") == "opacity"
            assert clock.get("calcMode") == "discrete"
            assert clock.get("dur") == "12s"
            assert clock.get("repeatCount") == "indefinite"
            assert clock.get("keyTimes") == "0;0.166667;0.333333;0.5;0.666667;0.833333;1"
            assert clock.get("values").split(";") == [
                "1" if j == i or (j == 6 and i == 0) else "0"
                for j in range(7)]
    else:
        assert not any(n.get("data-teaching-role") == "finite-streak"
                       for n in doc.iter(svg + "text"))
for name in ("mixed-precision.md", "mixed-precision.zh-TW.md"):
    page = (pages / name).read_text(encoding="utf-8")
    assert "NEXT S" in page and "2/2" in page and "2048" in page
print("GradScaler next-scale and finite-streak bilingual timing contracts OK")

# GitHub and reduced-motion readers can inspect the two-success growth threshold
# and overflow resets without waiting for a SMIL frame or reading a paragraph.
for stem in ("gradscaler-feedback-motion", "gradscaler-feedback-still"):
    root_svg = ET.parse(asset / (stem + ".svg")).getroot()
    history = [n for n in root_svg.iter(svg + "g")
               if n.get("data-teaching-role") == "finite-streak-history"]
    assert len(history) == 1
    history = history[0]
    assert [n.text for n in history.findall(svg + "text")] == ["STREAK"]
    circles = history.findall(svg + "circle")
    assert [int(n.get("cx")) for n in circles] == [128, 138, 213, 223, 303,
                                                   383, 393, 468, 478, 558]
    assert [n.get("fill") for n in circles] == [
        "#16857f", "#fff", "#16857f", "#16857f", "#fff3e9",
        "#16857f", "#fff", "#16857f", "#16857f", "#fff3e9"]
    assert len(history.findall(svg + "path")) == 2
    assert all(path.get("stroke") == "#b66c39"
               for path in history.findall(svg + "path"))
for lang in ("mixed-precision.md", "mixed-precision.zh-TW.md"):
    text = (pages / lang).read_text(encoding="utf-8")
    assert "STREAK" in text and ("filled dot" in text if lang.endswith("precision.md") else "雙圓點" in text)
print("GradScaler static readable streak and exact six-event visual states OK")


# The shared step/seek player now exposes ALL three co-design processes.
# Timing keys are chosen to land just after the SVG's discrete state changes,
# while the slider remains continuous between teaching milestones.
controls_js = (root / "docs/javascripts/distributed-motion-controls.js").read_text(encoding="utf-8")
controls_css = (root / "docs/stylesheets/distributed-motion-controls.css").read_text(encoding="utf-8")
timeline_cases = {
    "checkpoint-spacing": "[0, 2.45, 4.85, 7.25, 9.65]",
    "fp16-scaling-window": "[0, 0.95, 1.42, 4.66, 5.12, 5.59, 6.05, 6.52, 6.98, 9.75, 10.21, 10.67, 11.15]",
    "gradscaler-feedback": "[0, 2.05, 4.05, 6.05, 8.05, 10.05]",
}
for stem, times in timeline_cases.items():
    assert f"'{stem}': {{ duration: 12, steps: {times} }}" in controls_js, stem
    assert (asset / f"{stem}-motion.svg").is_file()
    assert (asset / f"{stem}-still.svg").is_file()
assert "host.classList.add('co-design-motion-timeline')" in controls_js
assert "coDesignRegion.after(bar)" in controls_js
assert "if (coDesignRegion) bar.remove();" in controls_js
assert ".concept-motion-scroll > .concept-motion-player.co-design-motion-timeline" in controls_css
assert ".co-design-motion-controls" in controls_css
assert "reduced.addEventListener('change', onReduce)" in controls_js
assert "if (!reduced.matches) enhance()" in controls_js
# Keyboard-accessible restart and pause on tab hide; clean up with the player.
assert "makeButton('↺ Restart', '↺ 重新開始')" in controls_js
assert "restart?.addEventListener('click', () => {" in controls_js
assert "stop(false); setTime(0);" in controls_js
assert "document.addEventListener('visibilitychange', onVisibility)" in controls_js
assert "document.removeEventListener('visibilitychange', onVisibility)" in controls_js
assert "const viewportTargets = coDesignRegion ? [coDesignRegion, bar] : [host];" in controls_js
assert "every(visible => !visible)" in controls_js
assert "viewportObserver?.disconnect();" in controls_js
for language in ("gradient-checkpointing.md", "gradient-checkpointing.zh-TW.md",
                 "mixed-precision.md", "mixed-precision.zh-TW.md"):
    body = (pages / language).read_text(encoding="utf-8")
    assert ("重新開始" if language.endswith(".zh-TW.md") else "Restart") in body
print("Co-design reset, background-tab pause and bilingual operation guidance OK")
for language in ("gradient-checkpointing.md", "gradient-checkpointing.zh-TW.md",
                 "mixed-precision.md", "mixed-precision.zh-TW.md"):
    body = (pages / language).read_text(encoding="utf-8")
    if language.endswith(".zh-TW.md"):
        assert "上一步／下一步" in body and "時間軸" in body and "速度" in body
    else:
        assert "Previous/Next Step" in body and "seek" in body and "speed" in body
print("Co-design semantic stepping, mobile controls and bilingual operation guidance OK")


# A visually inactive <object> fallback must not duplicate the source image's
# alt description. Playwright get_by_alt_text(..., exact=True) used to find TWO
# matches in every enhanced co-design chapter, failing the built MkDocs CI.
# The object carries the accessible label; its nested image is decorative.
assert "frame.setAttribute('aria-label', img.alt || match[1])" in controls_js
assert "const fallback = img.cloneNode(true)" in controls_js
assert "fallback.alt = ''" in controls_js
assert "fallback.setAttribute('aria-hidden', 'true')" in controls_js
assert "fallback.setAttribute('role', 'presentation')" in controls_js
assert "frame.append(fallback)" in controls_js
assert "frame.append(img.cloneNode(true))" not in controls_js
print("Accessible SVG fallback does not duplicate the original alt text OK")


# The player exposes a localized textual explanation of each synthetic state,
# not merely a playback timestamp. Assistive announcements happen only for
# explicit step/seek operations, rather than on every animation frame.
assert "function teachingState(t)" in controls_js
assert "seek.setAttribute('aria-valuetext', conciseState(time))" in controls_js
assert "interpretation.setAttribute('aria-live', 'off')" in controls_js
assert "status.textContent = interpretation.isConnected ? interpretation.textContent" in controls_js
assert "Math.floor(t / 2.4)" in controls_js  # Five checkpoint stages.
assert "const keep = 16 / spacing + 1, scratch = spacing - 1" in controls_js
assert "const totalRebuilt = 16 - 16 / spacing" in controls_js
assert "TOTAL REBUILT ${totalRebuilt} (all segments)" in controls_js
assert "全區段重建總數 ${totalRebuilt}" in controls_js
assert "silent underflow" in controls_js and "歸零（仍為有限值）" in controls_js
assert "STEP ELIGIBLE" in controls_js and "通過非有限值檢查、符合更新條件" in controls_js
assert "Math.floor(t / config.duration * 26 + 1e-6)" in controls_js  # 27 FP16 states.
assert "const scale = 2 ** exponent" in controls_js
assert "const following = [1024, 2048, 1024, 1024, 2048, 1024]" in controls_js
assert ".distributed-motion-interpretation" in controls_css
assert ".co-design-motion-controls .concept-motion-status" in controls_css
for name in ("gradient-checkpointing.md", "gradient-checkpointing.zh-TW.md",
             "mixed-precision.md", "mixed-precision.zh-TW.md"):
    page = (pages / name).read_text(encoding="utf-8")
    assert ("synchronized" if name.endswith(("checkpointing.md", "precision.md"))
            else "同步文字解讀") in page
assert "TOTAL REBUILT across all segments" in (pages / "gradient-checkpointing.md").read_text(encoding="utf-8")
assert "所有區段的總重建數量" in (pages / "gradient-checkpointing.zh-TW.md").read_text(encoding="utf-8")
assert "zero as silent underflow" in (pages / "mixed-precision.md").read_text(encoding="utf-8")
assert "靜默下溢為零" in (pages / "mixed-precision.zh-TW.md").read_text(encoding="utf-8")
print("Co-design synchronized numerical interpretation, bilingual copy and accessible announcements OK")

# A/B pinning is a teaching comparison, not another static illustration.
# No duplicated language-specific SVG or JavaScript may be introduced.
assert "swapPin.textContent = label('Swap A/B', '交換 A／B')" in controls_js
assert "swapPin?.addEventListener('click', () => {" in controls_js
assert "NEXT S ${nextScale[ia]} → ${nextScale[ib]}" in controls_js
assert "下次縮放 ${nextScale[ia]} → ${nextScale[ib]}" in controls_js
assert "pinnedTime = time;" in controls_js and "setTime(previousA);" in controls_js
assert "swapPin.hidden = true" in controls_js and "swapPin.hidden = false" in controls_js
assert ".distributed-motion-swap" in controls_css
for name in ("gradient-checkpointing.md", "mixed-precision.md"):
    assert "**Swap A/B**" in (pages / name).read_text(encoding="utf-8")
for name in ("gradient-checkpointing.zh-TW.md", "mixed-precision.zh-TW.md"):
    assert "**交換 A／B**" in (pages / name).read_text(encoding="utf-8")
assert "pin.textContent = label('Pin A', '釘選 A')" in controls_js
assert "clearPin.textContent = label('Clear A', '清除 A')" in controls_js
assert "function compareChange(a, b)" in controls_js
assert "LOW ${low(x)} → ${low(y)}" in controls_js
assert "HIGH ${high(x)} → ${high(y)}" in controls_js
assert "scale exponent ${x} → ${y} (Δ ${signed(y - x)})" in controls_js
assert "const streak = [1, 2, 0, 1, 2, 0]" in controls_js
assert "streak ${streak[ia]}/2 → ${streak[ib]}/2" in controls_js
assert "Δ ${signed(nextScale[ib] - nextScale[ia])}" in controls_js
assert "**signed change in scale exponent**" in (pages / "mixed-precision.md").read_text(encoding="utf-8")
assert "**帶正負號的縮放指數差**" in (pages / "mixed-precision.zh-TW.md").read_text(encoding="utf-8")
assert "Δ TOTAL REBUILT" in controls_js
assert "Outcome: " in controls_js and "Finite check: " in controls_js
assert "synthetic, not measured" in controls_js
assert ".distributed-motion-comparison" in controls_css
assert ".distributed-motion-compare-delta" in controls_css
assert "grid-template-columns: minmax(0, 1fr)" in controls_css
for name in ("gradient-checkpointing.md", "mixed-precision.md"):
    assert "**Pin A**" in (pages / name).read_text(encoding="utf-8")
for name in ("gradient-checkpointing.zh-TW.md", "mixed-precision.zh-TW.md"):
    assert "**釘選 A**" in (pages / name).read_text(encoding="utf-8")
print("Co-design A/B state pinning, bilingual instructions and responsive comparisons OK")

# Paired A/B visual gauges are dynamically derived from the same fixed,
# synthetic timelines as the accessible comparison text; never normalize
# A and B independently or turn the illustrative bars into measurements.
assert "const gaugeFills = []" in controls_js
assert "comparison.append(pinA, pinB, comparisonDelta, visual)" in controls_js
assert "a.style.width = (100 * metric.at(pinnedTime) / metric.max) + '%'" in controls_js
assert "b.style.width = (100 * metric.at(time) / metric.max) + '%'" in controls_js
assert "'aria-hidden', 'true'" in controls_js
for metric in ("peak", "rebuilt", "exponent", "low", "high", "streak", "next"):
    assert "id: '" + metric + "'" in controls_js
assert ".distributed-motion-compare-visual" in controls_css
assert "@media (prefers-reduced-motion: reduce)" in controls_css
assert "fixed, shared domains" in (pages / "gradient-checkpointing.md").read_text(encoding="utf-8")
assert "固定且共用的刻度" in (pages / "gradient-checkpointing.zh-TW.md").read_text(encoding="utf-8")
assert "fixed domains shared by A and B" in (pages / "mixed-precision.md").read_text(encoding="utf-8")
assert "相同固定刻度" in (pages / "mixed-precision.zh-TW.md").read_text(encoding="utf-8")
print("Paired A/B gauge rendering contract and bilingual descriptions OK")

# A/B interpretations explicitly distinguish restricted-model dominance,
# binary16 representability regimes and GradScaler history-based decisions.
assert "function comparisonInsight(a, b)" in controls_js
assert "B Pareto-dominates A (no worse on either cost)." in controls_js
assert "A Pareto-dominates B (no worse on either cost)." in controls_js
assert "Memory–recomputation trade-off." in controls_js
assert "Rounded regime: " in controls_js and "LOW SUBNORMAL, HIGH FINITE" in controls_js
assert "Next-scale action: " in controls_js and "backoff" in controls_js
for name in ("gradient-checkpointing.md", "gradient-checkpointing.zh-TW.md"):
    assert "s=8" in (pages / name).read_text(encoding="utf-8")
for name in ("mixed-precision.md", "mixed-precision.zh-TW.md"):
    assert "GradScaler A/B" in (pages / name).read_text(encoding="utf-8")
print("Bilingual trade-off/dominance, FP16 regimes, and GradScaler actions OK")

# Initially reduced-motion pages must install the timeline for preference changes.
assert "  function enhance() {\n    if (reduced.matches) return;" not in controls_js
assert "if (reduced.matches) onReduce({ matches: true });" in controls_js
assert "reduced.addEventListener('change', onReduce)" in controls_js
print("Initial reduced-motion preference restoration contract OK")

# Guided A/B cases are exact discrete SVG states, not arbitrary slider
# endpoints: one checkpoint trade-off and dominance pair, both binary16
# boundary crossings, and two finite-history/overflow GradScaler contrasts.
assert "const guidedCases = match[1] === 'checkpoint-spacing'" in controls_js
assert "const guided = pin ? document.createElement('select') : null;" in controls_js
assert "guided.setAttribute('aria-label', label('Guided A/B comparisons', '引導式 A/B 比較'))" in controls_js
assert "guided?.addEventListener('change', () => {" in controls_js
assert "pinnedTime = example.a;" in controls_js and "setTime(example.b);" in controls_js
assert "guided.value = ''" in controls_js
assert "if (guided) guided.disabled = false" in controls_js
assert ".distributed-motion-scenario:focus-visible" in controls_css
for a, b in ((0, 4.85), (7.25, 4.85), (0.95, 1.42),
             (4.66, 5.12), (0, 8.05), (2.05, 4.05)):
    assert f"a: {a}, b: {b}" in controls_js
for language in ("gradient-checkpointing.md", "gradient-checkpointing.zh-TW.md",
                 "mixed-precision.md", "mixed-precision.zh-TW.md"):
    body = (pages / language).read_text(encoding="utf-8")
    assert ("選擇示範比較" if language.endswith(".zh-TW.md")
            else "Try a worked comparison") in body
print("Guided binary16, checkpoint and GradScaler bilingual scenario contracts OK")

# Directional A→B scans must stop at B (never wrap) and remain cancellable.
assert "sweepPin.textContent = label('▶ Sweep A→B', '▶ 掃描 A→B')" in controls_js
assert "sweepPin?.addEventListener('click', () => {" in controls_js
assert "sweepTarget = target;" in controls_js and "time = pinnedTime;" in controls_js
assert "if (sweepTarget === null && time >= config.duration)" in controls_js
assert "stop(); // Leave B selected; unlike regular Play, never wrap." in controls_js
assert "sweepTarget = null;" in controls_js  # seeking/pause/reduced-motion abort scans
assert ".distributed-motion-sweep[hidden]" in controls_css
for language in ("gradient-checkpointing.md", "gradient-checkpointing.zh-TW.md",
                 "mixed-precision.md", "mixed-precision.zh-TW.md"):
    body = (pages / language).read_text(encoding="utf-8")
    assert ("掃描 A→B" if language.endswith(".zh-TW.md") else "Sweep A→B") in body
print("Directional synthetic A/B scan, bilingual guidance and cancellation contract OK")

# Key-transition navigation is tied to prescribed numeric states, without
# duplicating or replacing any SVG teaching assets.
assert "const landmarkRail = landmarks.length ? document.createElement('div') : null;" in controls_js
assert "landmarkButtons.forEach(({ button }) => { button.disabled = false; });" in controls_js
assert "button.setAttribute('aria-current', 'step')" in controls_js
assert "stop(false); setTime(event.t);" in controls_js
assert ".distributed-motion-landmark:focus-visible" in controls_css
assert ".distributed-motion-landmark.is-current" in controls_css
for transition in ("t: 0, en: 's=1'", "t: 4.85, en: 's=4'",
                   "t: 1.42, en: 'LOW +'", "t: 5.12, en: 'HIGH Inf'",
                   "t: 6.98, en: 'HIGH finite'", "t: 10.67, en: 'LOW 0'",
                   "t: 2.05, en: 't2 · grow'", "t: 4.05, en: 't3 · backoff'"):
    assert transition in controls_js, transition
for language in ("gradient-checkpointing.md", "gradient-checkpointing.zh-TW.md",
                 "mixed-precision.md", "mixed-precision.zh-TW.md"):
    text = (pages / language).read_text(encoding="utf-8")
    assert ("關鍵狀態導覽" if language.endswith(".zh-TW.md")
            else "Key-transition navigation") in text
print("Bilingual semantic landmark navigation, keyboard and state contract OK")

# FP16 temporal selection and all numerical readouts share one discrete frame.
assert "const fp16Frame = t => Math.min(26, Math.floor(t / config.duration * 26 + 1e-6));" in controls_js
assert "const exponent = scaleExponent(t);" in controls_js
assert "const k = scaleExponent(t);" in controls_js
assert "const x = scaleExponent(a), y = scaleExponent(b);" in controls_js
assert "fp16Frame(time) === fp16Frame(event.t)" in controls_js
assert "Math.abs(time - event.t) < 0.20" not in controls_js
assert "6.52, 6.98, 9.75, 10.21, 10.67, 11.15" in controls_js
for name in ("mixed-precision.md", "mixed-precision.zh-TW.md"):
    body = (pages / name).read_text(encoding="utf-8")
    assert ("complete discrete power-of-two state" if name == "mixed-precision.md"
            else "整個離散縮放區段") in body
print("FP16 full-frame boundary highlighting and reverse Step contracts OK")


# Keyboard range control must expose real synthetic-state navigation.
# Chrome's native 1/1000 range arrows alone cannot reach a new FP16 frame
# or checkpoint choice with one keypress. Shift permits precision seeking.
assert "seek.addEventListener('keydown'" in controls_js
assert "event.shiftKey || event.altKey || event.ctrlKey || event.metaKey" in controls_js
assert "(index + 0.12) * config.duration / 26" in controls_js
assert "fp16Frame(time) + direction" in controls_js
assert "Shift+Left/Right" in controls_js
for file in ("gradient-checkpointing.md", "mixed-precision.md"):
    assert "Keyboard timeline navigation (MkDocs)" in (pages / file).read_text(encoding="utf-8")
for file in ("gradient-checkpointing.zh-TW.md", "mixed-precision.zh-TW.md"):
    assert "時間軸鍵盤導覽（MkDocs）" in (pages / file).read_text(encoding="utf-8")
print("Co-design semantic keyboard range and bilingual instruction contracts OK")

# Adjacent-state A/B shortcuts preserve temporal direction and the original
# interactive comparison; first states deliberately have no preceding state.
assert "const comparePrevious = pin ? document.createElement('button') : null;" in controls_js
assert "comparePrevious.textContent = label('Compare previous', '比較前一步');" in controls_js
assert "function previousStateTime(t)" in controls_js
assert "const before = i - 1;" in controls_js
assert "pinnedTime = earlier;" in controls_js
assert ".distributed-motion-previous:focus-visible" in controls_css
for language in ("gradient-checkpointing.md", "gradient-checkpointing.zh-TW.md",
                 "mixed-precision.md", "mixed-precision.zh-TW.md"):
    body = (pages / language).read_text(encoding="utf-8")
    assert ("比較前一步" if language.endswith(".zh-TW.md") else "Compare previous") in body
print("Bilingual adjacent-state comparison shortcuts and temporal direction OK")

# Cancel without a stale render when an explicit seek or semantic jump
# immediately redraws a different SVG state. Normal Pause still renders.
assert "function stop(redraw = true)" in controls_js
assert "if (redraw) draw();" in controls_js
assert controls_js.count("stop(false); setTime(") >= 4
step_block = controls_js.split("function step(direction) {", 1)[1].split(
    "prev.addEventListener('click'", 1)[0]
assert "stop(false);" in step_block and "setTime(candidate" in step_block
print("Co-design single-redraw seek and semantic-step contract OK")

# Continuous touch scrubbing updates the semantics at input frequency, but
# must not flood the polite screen-reader status region until input commits.
seek_block = controls_js.split("seek.addEventListener('input', () => {", 1)[1].split(
    "seek.addEventListener('change', () => {", 1)[0]
assert "stop(false); setTime(selected / 1000 * config.duration);" in seek_block
assert "status.textContent" not in seek_block
commit_block = controls_js.split("seek.addEventListener('change', () => {", 1)[1].split(
    "rate.addEventListener('change'", 1)[0]
assert "status.textContent = interpretation.isConnected ?" in commit_block
assert "svg.pauseAnimations();\n          // SVG <object> can reload" in controls_js
assert "setTime(time);\n          if (pin) pin.disabled = false;" in controls_js
for name in ("gradient-checkpointing.md", "gradient-checkpointing.zh-TW.md",
             "mixed-precision.md", "mixed-precision.zh-TW.md"):
    text = (pages / name).read_text(encoding="utf-8")
    assert ("polite status region" if name.endswith((".md",)) and not name.endswith(".zh-TW.md")
            else "狀態播報") in text
print("Co-design scrubbing quiet-live-region and SVG load continuity contracts OK")

# Reviewable bilingual recovery for an unavailable teaching animation.
assert "const retry = document.createElement('button');" in controls_js
assert "Animation unavailable · Retry" in controls_js and "動畫無法載入 · 重試" in controls_js
assert "url.searchParams.set('_motion_retry', String(++retryCount));" in controls_js
assert "frame.setAttribute('aria-hidden', 'true');" in controls_js
assert "frame.removeAttribute('aria-hidden');" in controls_js
assert ".distributed-motion-retry:focus-visible" in controls_css
for name in ("gradient-checkpointing.md", "gradient-checkpointing.zh-TW.md",
             "mixed-precision.md", "mixed-precision.zh-TW.md"):
    body = (pages / name).read_text(encoding="utf-8")
    assert ("Animation unavailable · Retry" if not name.endswith(".zh-TW.md")
            else "動畫無法載入 · 重試") in body
print("Bilingual in-page SVG recovery source contracts OK")

# A pending <object> request does not always dispatch load/error. The bounded
# watchdog must restore the reviewed still and permit retry, including after
# a reduced-motion preference toggle. The browser regression exercises the
# unresolved-request case with the real watchdog on the built site.
assert "const SVG_LOAD_TIMEOUT_MS = 15000;" in controls_js
assert "const armLoadTimer = () => {" in controls_js
assert "loadTimer = window.setTimeout(() => {" in controls_js
assert "showStaticFallback();" in controls_js
assert "clearLoadTimer();" in controls_js
assert "frame.data = url.href;\n        abandoned.replaceWith(frame);\n        armLoadTimer();" in controls_js
assert "frame = abandoned.cloneNode(true);" in controls_js
assert "if (candidate !== frame) return;" in controls_js
assert "if (acceptingFrameLoad) {\n            onFrameLoad();" in controls_js
assert "candidate.contentDocument?.documentElement?.pauseAnimations?.();" in controls_js
assert "if (candidate === frame && acceptingFrameLoad) showStaticFallback();" in controls_js
assert "frame.data = src;\n          armLoadTimer();" in controls_js
print("Stalled SVG requests have bounded fallback and reusable retry controls OK")

# A request that answers *after* the watchdog has selected its static
# fallback cannot revive the stale object; only Retry starts a new generation.
assert "let acceptingFrameLoad = true;" in controls_js
assert "acceptingFrameLoad = false;\n        clearLoadTimer();" in controls_js
assert "if (!acceptingFrameLoad) return;" in controls_js
assert "acceptingFrameLoad = true;\n        retry.textContent" in controls_js
assert "candidate === frame && acceptingFrameLoad" in controls_js
assert "late_valid_svg_ignored" in (root / "scripts/test_built_motion_browser.py").read_text(encoding="utf-8")
assert "documentElement?.animationsPaused?.() === true" in (
    root / "scripts/test_built_motion_browser.py").read_text(encoding="utf-8")
print("Expired SVG responses cannot silently revive interactive controls OK")



# A successfully parsed but motionless SVG must not unlock the timeline controls.
# The built HTTP fixture exercises this with a real valid SVG navigation and retry.
assert "const hasTeachingTimeline = !coDesignRegion || !!root?.querySelector(" in controls_js
assert "'animate, animateTransform, animateMotion, set'" in controls_js
assert "root.namespaceURI !== 'http://www.w3.org/2000/svg'" in controls_js
browser_source = (root / "scripts/test_built_motion_browser.py").read_text(encoding="utf-8")
assert "qa_static_svg" in browser_source
assert "motionless_svg_rejected_and_recovered" in browser_source
print("Reject valid-but-motionless co-design SVG with a built-browser regression OK")

# Switching out of reduced motion must retain the still preview while the
# controlled SVG <object> is loading. Otherwise the visible <img> starts
# playing the raw motion SVG with no Pause/Step affordances.
pending_reduce_load = controls_js.split("} else if (!svg) {", 1)[1].split(
    "reduced.addEventListener('change', onReduce);", 1)[0]
assert "img.src = img.dataset.stillSrc || src.replace(" in pending_reduce_load
assert "img.hidden = false;" in pending_reduce_load
assert "img.src = src;" not in pending_reduce_load
assert "frame.data = src;\n          armLoadTimer();" in pending_reduce_load
print("Pending SVG initialization retains accessible reduced-motion still preview OK")

# Four guided contrasts per diagram expose equal-peak dominance,
# both directions of FP16 threshold crossings, and GradScaler history.
for snippet in (
    "s=2 → s=8 · equal peak, more replay",
    "s=1 → s=16 · equal peak, extra replay",
    "S=2048 → 1024 · descending recovery",
    "S=8 → 4 · descending underflow",
    "t1 → t2 · finite streak grows",
    "t3 → t4 · finite recovery holds",
):
    assert snippet in controls_js, snippet
assert "to_have_count(5)" in browser_source
for name in ("gradient-checkpointing.md", "gradient-checkpointing.zh-TW.md",
             "mixed-precision.md", "mixed-precision.zh-TW.md"):
    body = (pages / name).read_text(encoding="utf-8")
    assert ("s=2 → s=8" if name.startswith("gradient-") else "S=2048 → 1024") in body
print("Expanded bilingual guided examples and built-browser contracts OK")

# Binary16 boundary reasoning and shared bilingual teaching contracts.
for exponent in range(13):
    low = 2.0 ** (exponent - 27)
    high = 2.0 ** (exponent + 5)
    assert (exponent <= 2) == (low <= 2 ** -25)
    assert (exponent >= 3) == (2 ** -24 <= low < 2 ** -14)
    assert (exponent >= 11) == (high >= 2 ** 16)
assert "LOW SUBNORMAL, HIGH FINITE" in controls_js
assert "Pareto-dominates" in controls_js
assert "counter resets to 0" in controls_js
for name in ("gradient-checkpointing.md", "gradient-checkpointing.zh-TW.md"):
    body = (pages / name).read_text(encoding="utf-8")
    assert "Pareto" in body and ("at least one" in body or "至少一項" in body)
for name in ("mixed-precision.md", "mixed-precision.zh-TW.md"):
    body = (pages / name).read_text(encoding="utf-8")
    assert "2^{-17}" in body and ("subnormal" in body or "次正規" in body)
print("Pareto, binary16 subnormal and GradScaler reset contracts OK")

assert "非零次正規" in controls_js

# Synthetic three-axis interpretation contracts: one global frontier,
# two-gradient representability (not the optimizer's Inf/NaN gate), and
# the post-decision GradScaler streak in addition to the decision-time value.
assert "const pairWindow = k => k >= 3 && k <= 10;" in controls_js
assert "const postDecisionStreak = [1, 0, 0, 1, 0, 0];" in controls_js
for token in ("PARETO FRONTIER", "DOMINATED", "PAIR WINDOW", "POST-DECISION STREAK", "POST-DECISION"):
    assert token in controls_js, token
for lang in ("gradient-checkpointing.md", "gradient-checkpointing.zh-TW.md"):
    content = (pages / lang).read_text(encoding="utf-8")
    assert ("Pareto frontier" in content or "Pareto 前緣" in content)
for lang in ("mixed-precision.md", "mixed-precision.zh-TW.md"):
    content = (pages / lang).read_text(encoding="utf-8")
    assert "1,0,0,1,0,0" in content or "1、0、0、1、0、0" in content
    assert "1024" in content and ("PAIR WINDOW" in content or "兩筆均非零有限" in content)
print("Frontier, two-gradient window and post-decision feedback contracts OK")

# Three additional synthetic teaching quantities: total forward re-executions,
# post-rounding FP32 unscale, and cumulative step eligibility.
for s, expected in ((1, 16), (2, 24), (4, 28), (8, 30), (16, 31)):
    assert 16 + (16 - 16 // s) == expected
import struct
for k in range(13):
    scale = 2 ** k
    scaled_low = 2.0 ** (k - 27)
    rounded = struct.unpack("<e", struct.pack("<e", scaled_low))[0]
    restored = rounded / scale
    assert restored == (0 if k <= 2 else 2.0 ** -27)
assert [sum(i not in (2, 5) for i in range(t + 1)) for t in range(6)] == [1, 2, 2, 3, 4, 4]
for fragment in ("FWD LAYER EVALS", "LOW AFTER FP32 UNSCALE",
                 "ELIGIBLE SO FAR", "const unscaledLow =",
                 "const eligibleSoFar ="):
    assert fragment in controls_js, fragment
for fragment, path in (
    ("forward-layer evaluations", "gradient-checkpointing.md"),
    ("前向層計算總次數", "gradient-checkpointing.zh-TW.md"),
    ("LOW AFTER FP32 UNSCALE", "mixed-precision.md"),
    ("FP32 還原小梯度", "mixed-precision.zh-TW.md"),
):
    assert fragment in (pages / path).read_text(encoding="utf-8")
print("Bilingual forward-work, ideal binary16 FP32-unscale and eligible-step contracts OK")

# Counterfactual flush-to-zero at the binary16 output/storage boundary.
# In this synthetic pair, the low gradient is still subnormal at S=4096;
# making it normal at S=8192 necessarily overflows the high gradient.
for k in range(13):
    low_scaled = 2.0 ** (k - 27)
    high_scaled = 2.0 ** (k + 5)
    assert low_scaled < 2.0 ** -14
    assert not (low_scaled >= 2.0 ** -14 and high_scaled <= 65504)
    assert (3 <= k <= 10) == (k >= 3 and k <= 10)
assert (2.0 ** -27 * 8192) == 2.0 ** -14
assert 2.0 ** 5 * 8192 > 65504
for token in ("FTZ LOW 0", "FTZ PAIR NO", "IEEE/FTZ MISMATCH",
              "沖零假設：小梯度 0", "IEEE／沖零判斷相異"):
    assert token in controls_js, token
for lang, phrase in (("mixed-precision.md", "What if subnormals are flushed to zero?"),
                     ("mixed-precision.zh-TW.md", "次正規數沖零時的反事實比較")):
    assert phrase in (pages / lang).read_text(encoding="utf-8")
print("FTZ vs ideal binary16 arithmetic and bilingual explanation contracts OK")


# The FTZ counterfactual must also explain why a GradScaler nonfinite gate
# cannot notice silent loss of a small (subnormal) gradient.
eligible_history = [1, 2, 2, 3, 4, 4]
scales = [1024, 1024, 2048, 1024, 1024, 2048]
assert all(0 < (2 ** -27) * s < 2 ** -14 for s in scales)
assert [((2 ** -27) * s) >= 2 ** -24 for s in scales] == [True] * 6
assert eligible_history == [1, 2, 2, 3, 4, 4]
for token in ("ELIGIBLE LOW KEPT: IEEE", "ELIGIBLE LOW KEPT IEEE/FTZ",
              "ELIGIBLE LOW KEPT IEEE ${eligibleSoFar[ia]}",
              "符合條件且小梯度非零累計", "符合條件且保留小梯度"):
    assert token in controls_js, token
for lang, text in (("mixed-precision.md", "Why finite-check feedback cannot repair silent FTZ loss"),
                   ("mixed-precision.zh-TW.md", "有限值回饋無法修復 FTZ 的靜默資訊流失")):
    content = (pages / lang).read_text(encoding="utf-8")
    assert text in content and "1, 2, 2, 3, 4, 4" in content.replace("、", ", ")
print("GradScaler FTZ/IEEE low-gradient retention, bilingual contracts OK")

# Real six-iteration retention strip (IEEE vs hypothetical FTZ) is
# synchronized with the controlled SVG's cursor, not auto-animated.
for token in ("retentionTraceCells", "distributed-motion-retention-trace",
              "cell.dataset.state = i > current ? 'future'",
              "policy === 0 ? 'retained' : 'lost'",
              "i === 2 || i === 5",
              "trace.setAttribute('aria-hidden', 'true')"):
    assert token in controls_js, token
for token in ('data-state="retained"', 'data-state="lost"',
              'data-state="skipped"', 'box-sizing: border-box',
              'minmax(0, 1fr)'):
    assert token in controls_css, token
for name, text in (("mixed-precision.md", "Follow information retention (MkDocs)"),
                   ("mixed-precision.zh-TW.md", "追蹤梯度資訊保留（MkDocs）")):
    assert text in (pages / name).read_text(encoding="utf-8")
assert "rows = trace.locator('.distributed-motion-retention-row')" in browser_source
print("IEEE/FTZ six-step visual trace, bilingual text, CSS and E2E contracts OK")
# Interactive Pareto plane: five *sampled* choices, and the same two costs
# as the original animation. It never represents an empirical GPU frontier.
sampled = [(s, 16 // s + s, 16 - 16 // s) for s in (1, 2, 4, 8, 16)]
frontier = [s for s, peak, rebuilt in sampled if not any(
    (other_peak <= peak and other_rebuilt <= rebuilt and
     (other_peak < peak or other_rebuilt < rebuilt))
    for other_s, other_peak, other_rebuilt in sampled if other_s != s)]
assert frontier == [1, 2, 4], frontier
for marker in ("paretoMapDots", "distributed-motion-pareto", "dataset.frontier",
               "dot.addEventListener('click'", "stop(false);",
               "paretoMapDots.forEach(({ button }) => { button.disabled = false; });",
               "button.classList.toggle('is-pinned'", "aria-current"):
    assert marker in controls_js, marker
for marker in (".distributed-motion-pareto-plot", ".distributed-motion-pareto-dot.is-current",
               ".distributed-motion-pareto-dot.is-pinned",
               '.distributed-motion-pareto-dot[data-frontier="false"]',
               ".distributed-motion-pareto-dot:focus-visible"):
    assert marker in controls_css, marker
assert "Interactive Pareto map (MkDocs)" in (pages / "gradient-checkpointing.md").read_text(encoding="utf-8")
assert "互動式 Pareto 成本地圖（MkDocs）" in (pages / "gradient-checkpointing.zh-TW.md").read_text(encoding="utf-8")
# A selected dominated point must show an actual coordinate-consistent
# witness toward s=2, without inventing a continuous optimisation trace.
for spacing, peak, rebuilt in ((8, 10, 14), (16, 17, 15)):
    assert 10 <= peak and 8 < rebuilt
assert "let paretoWitness = null" in controls_js
assert "selected === 8 || selected === 16" in controls_js
assert "s=2 witness: PEAK 10=10; REBUILT 8<14" in controls_js
assert "s=2 witness: PEAK 10<17; REBUILT 8<15" in controls_js
assert ".distributed-motion-pareto-witness" in controls_css
for name, expected in (("gradient-checkpointing.md", "Dominance witness (MkDocs)"),
                       ("gradient-checkpointing.zh-TW.md", "支配關係的動態見證（MkDocs）")):
    page_text = (pages / name).read_text(encoding="utf-8")
    assert expected in page_text
    assert "checkpoint-pareto-witness-still.svg" in page_text
assert (asset / "checkpoint-pareto-witness-still.svg").exists()
ET.parse(asset / "checkpoint-pareto-witness-still.svg")
print("Five-choice Pareto plane, interactive dominance witness and bilingual fallback OK")

# Two counterfactual 13-state policies; FTZ affects LOW storage only.
for k in range(13):
    ieee = "overflow" if k >= 11 else "valid" if 3 <= k <= 10 else "underflow"
    ftz = "overflow" if k >= 11 else "underflow"
    assert ieee in ("underflow", "valid", "overflow")
    assert ftz in ("underflow", "overflow")
for marker in ("policyWindowCells", "distributed-motion-policy-window", "policyWindowDirection.textContent",
               "policy === 'IEEE' && pairWindow(k)", "cell.dataset.current = 'true'"):
    assert marker in controls_js, marker
for marker in ('.distributed-motion-policy-row', '.distributed-motion-policy-cell[data-state="valid"]',
               '.distributed-motion-policy-cell[data-state="underflow"]', '.distributed-motion-policy-cell[data-state="overflow"]'):
    assert marker in controls_css, marker
assert "IEEE/FTZ comparison strip (MkDocs)" in (pages / "mixed-precision.md").read_text(encoding="utf-8")
assert "IEEE／FTZ 雙軌對照（MkDocs）" in (pages / "mixed-precision.zh-TW.md").read_text(encoding="utf-8")
for token in ("distributed-motion-policy-legend", "distributed-motion-policy-legend-swatch",
              "['underflow', 'LOW 0']", "['valid', 'PAIR nonzero']",
              "['overflow', 'HIGH Inf']", "['current', 'Selected']"):
    assert token in controls_js, token
for token in ('.distributed-motion-policy-legend-item',
              '.distributed-motion-policy-legend-swatch[data-state="underflow"]',
              '.distributed-motion-policy-legend-swatch[data-state="overflow"]'):
    assert token in controls_css, token
for name in ("mixed-precision.md", "mixed-precision.zh-TW.md"):
    assert "PAIR nonzero" in (pages / name).read_text(encoding="utf-8"), name
print("Synchronized IEEE/FTZ policy visualization and in-panel texture key contracts OK")
