"""Regression checks for learning-rate teaching animation semantics.

Run: python scripts/test_learning_rate_motion_semantics.py
These structural/numerical checks do NOT replace browser rendering QA.
"""
from __future__ import annotations

import math
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1] / "docs/assets/concept-animations"
NS = {"svg": "http://www.w3.org/2000/svg"}


def read(name: str):
    root = ET.parse(ROOT / name).getroot()
    marker = root.find(".//svg:circle", NS)
    assert marker is not None, name
    anim = {a.attrib["attributeName"]: a for a in marker.findall("svg:animate", NS)}
    assert set(anim) == {"cx", "cy"}, (name, anim.keys())
    result = {}
    for axis in ("cx", "cy"):
        a = anim[axis]
        times = [float(x) for x in a.attrib["keyTimes"].split(";")]
        values = [float(x) for x in a.attrib["values"].split(";")]
        assert len(times) == len(values) and len(times) > 50
        assert abs(times[0]) < 1e-8 and abs(times[-1] - 1) < 1e-8
        assert all(b > a for a, b in zip(times, times[1:])), name
        assert a.attrib["calcMode"] == "linear"
        assert a.attrib["repeatCount"] == "indefinite"
        result[axis] = (times, values)
    tx, xs = result["cx"]
    ty, ys = result["cy"]
    assert tx == ty, name
    assert all(abs(x - (64 + 510*t)) < 0.012 for x, t in zip(xs, tx)), name
    return tx, xs, ys


def sgdr():
    times, xs, ys = read("sgdr-restart-motion.svg")
    assert len(times) == 145
    for boundary in (1/7, 3/7):
        nearby = [i for i, t in enumerate(times) if abs(t-boundary) < 0.000005]
        assert len(nearby) >= 3, (boundary, nearby)
        # Immediately before restart: low LR (larger y); after: high LR (smaller y).
        assert ys[nearby[0]] > 220 and ys[nearby[-1]] < 100
    for t, y in zip(times, ys):
        if any(abs(t-b) < 0.000005 for b in (1/7, 3/7)):
            continue
        phase = t*7 if t < 1/7 else (t*7-1)/2 if t < 3/7 else (t*7-3)/4
        expected = 159 - 71.4*math.cos(math.pi*phase)
        assert abs(y-expected) < 0.08, (t, y, expected)


def triangular2():
    times, xs, ys = read("clr-triangular2-motion.svg")
    assert len(times) == 121
    for cycle in range(3):
        start, peak, end = cycle*40, cycle*40+20, (cycle+1)*40
        assert abs(ys[start]-223.6) < 0.03
        assert abs(ys[end]-223.6) < 0.03
        assert abs(ys[peak]-(223.6-129.2/2**cycle)) < 0.03
        for j in range(start, end+1):
            phase = (j-start)/40
            expected = 223.6 - (129.2/2**cycle)*(1-abs(2*phase-1))
            assert abs(ys[j]-expected) < 0.035, (j, ys[j], expected)


if __name__ == "__main__":
    sgdr()
    triangular2()
    print("Learning-rate animation numerical and timeline semantics: PASS")
