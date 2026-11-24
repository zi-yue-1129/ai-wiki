#!/usr/bin/env python3
"""Numerical and bilingual-source regression for probabilistic teaching motions."""
from pathlib import Path
from xml.etree import ElementTree as ET
import math

assets = Path("docs/assets/concept-animations")
pages = Path("docs/theory/evaluation/metrics/probabilistic")
for stem, page in {
    "brier-murphy-decomposition": "brier-score",
    "ece-bin-merging": "calibration-error",
}.items():
    motion = assets / f"{stem}-motion.svg"
    still = assets / f"{stem}-still.svg"
    assert motion.exists() and still.exists()
    for path in (motion, still):
        root = ET.parse(path).getroot()
        assert root.attrib["viewBox"] == "0 0 640 360"
        assert root.tag.endswith("svg")
        assert not any(el.tag.endswith("script") for el in root.iter())
    assert "<animate " in motion.read_text() and "prefers-reduced-motion" in motion.read_text()
    assert "<animate " not in still.read_text()
    for locale in ("", ".zh-TW"):
        doc = (pages / f"{page}{locale}.md").read_text()
        assert f"{stem}-still.svg" in doc and f"{stem}-motion.svg" in doc
        assert "data-source-asset-urls" in doc
        assert doc.count(f"{stem}-still.svg") >= 2

cases = [(.2, y) for y in (1, 1, 0, 0, 0)] + [(.8, y) for y in (1, 1, 1, 0, 0)]
bs = sum((p-y)**2 for p,y in cases) / len(cases)
rate = sum(y for _,y in cases) / len(cases)
unc = rate * (1-rate)
rel = sum(.5*(p-r)**2 for p,r in ((.2,.4),(.8,.6)))
res = sum(.5*(r-rate)**2 for r in (.4,.6))
assert math.isclose(unc,.25) and math.isclose(rel,.04) and math.isclose(res,.01)
assert math.isclose(bs,.28) and math.isclose(bs,unc+rel-res)
obs = [(.3,y) for y in (1,1,0,0)] + [(.7,y) for y in (1,1,0,0)]
mean_p = sum(p for p,_ in obs)/8
mean_y = sum(y for _,y in obs)/8
ece_two = .5*abs(.3-.5) + .5*abs(.7-.5)
ece_one = abs(mean_p-mean_y)
assert math.isclose(ece_two,.2) and math.isclose(ece_one,0)
print("Probability motion numerical, structure and bilingual source checks passed.")
