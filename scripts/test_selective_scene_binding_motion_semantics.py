"""Regression: displayed selective-classification SVG scenes must match their arithmetic.

The previous tests checked summary fractions and SMIL timing separately, but could
not detect mislabeled rejected cases or the wrong class-conditional acceptance
mask. Inspect real SVG scene glyphs, labels, and fallback panels.
"""
from fractions import Fraction
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path("docs/assets/concept-animations")
NS = {"svg": "http://www.w3.org/2000/svg"}
GREEN, RED = "#16845b", "#cc594c"


def load(stem):
    root = ET.parse(ROOT / f"{stem}-motion.svg").getroot()
    scenes = [g for g in root.findall("svg:g", NS)
              if "scene" in g.get("class", "").split()]
    assert scenes, stem
    for i, scene in enumerate(scenes):
        assert f"stage-{i}" in scene.get("class", "").split()
        anim = scene.find("svg:animate", NS)
        assert anim is not None
        assert anim.get("attributeName") == "opacity"
        assert anim.get("calcMode") == "discrete"
        values = [float(v) for v in anim.get("values").split(";")]
        assert values == [float(j == i) for j in range(len(scenes))] + [float(i == 0)]
    return scenes


def glyphs(scene):
    groups = [g for g in scene.findall("svg:g", NS)
              if g.find("svg:path", NS) is not None]
    parsed = []
    for g in groups:
        path = g.find("svg:path", NS)
        assert path.get("stroke") in (GREEN, RED)
        texts = ["".join(t.itertext()).strip()
                 for t in g.findall("svg:text", NS)]
        parsed.append((path.get("stroke") == GREEN, texts,
                       float(g.get("opacity", "1"))))
    return parsed


def labels(scene):
    return ["".join(t.itertext()).strip()
            for t in scene.findall("svg:text", NS)]


# Topic 1: three changes of the rejection rule, with all predictions fixed.
ranked = [("0.97", True), ("0.91", True), ("0.80", False),
          ("0.72", True), ("0.60", False), ("0.51", True)]
coverage_scenes = load("accuracy-selective-coverage")
assert len(coverage_scenes) == 3
for scene, k in zip(coverage_scenes, (2, 4, 6)):
    cells = glyphs(scene)
    assert len(cells) == len(ranked)
    hits = 0
    for i, ((good, texts, opacity), (score, correct)) in enumerate(zip(cells, ranked)):
        assert good == correct
        assert texts == [score, "ACCEPT" if i < k else "REJECT"]
        assert opacity == (1.0 if i < k else 0.42)
        hits += int(good and i < k)
    shown = labels(scene)
    assert f"COVERAGE   {k}/6" in shown
    assert f"ACC   {hits}/{k}" in shown
    assert f"Correct accepted: {hits}     Rejected: {6-k}" in shown
    assert Fraction(hits, k) + Fraction(k-hits, k) == 1

# Topic 2: class-conditional coverage is audited from visible IN/OUT marks.
class_scenes = load("accuracy-selective-class-coverage")
assert len(class_scenes) == 2
correctness = [True, False, False, True] + [True] * 4
masks = ([True] * 8, [True, False, False, False] + [True] * 4)
for scene, mask in zip(class_scenes, masks):
    cells = glyphs(scene)
    assert len(cells) == 8
    for (good, texts, opacity), correct, keep in zip(cells, correctness, mask):
        assert good == correct
        assert texts == ["IN" if keep else "OUT"]
        assert opacity == (1.0 if keep else 0.33)
    accepted = sum(mask)
    hits = sum(a and c for a, c in zip(mask, correctness))
    shown = labels(scene)
    assert f"ACC  {hits}/{accepted}" in shown
    assert f"POS COV {sum(mask[:4])}/4        NEG COV {sum(mask[4:])}/4" in shown
    assert ("ALL   8/8" if accepted == 8 else "SELECTIVE   5/8") in shown
assert Fraction(1, 4) != Fraction(4, 4)

# GitHub-safe static fallbacks must teach the same comparisons without SMIL.
for stem, expected in (
    ("accuracy-selective-coverage", ("TOP 2", "TOP 4", "TOP 6",
                                     "Risk  0.000", "Risk  0.250", "Risk  0.333")),
    ("accuracy-selective-class-coverage", ("ALL", "SELECTIVE",
                                           "POS 4/4   ·   NEG 4/4",
                                           "POS 1/4   ·   NEG 4/4")),
):
    root = ET.parse(ROOT / f"{stem}-still.svg").getroot()
    assert not list(root.iter("{http://www.w3.org/2000/svg}animate"))
    texts = ["".join(t.itertext()).strip()
             for t in root.iter("{http://www.w3.org/2000/svg}text")]
    assert all(marker in texts for marker in expected), (stem, texts)

print("Selective scene bindings, rate arithmetic and GitHub fallbacks OK")
