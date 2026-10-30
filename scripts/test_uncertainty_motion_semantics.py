"""Regression checks for the two uncertainty-calibration teaching animations.

Run: python scripts/test_uncertainty_motion_semantics.py
No third-party packages required. These checks are deliberately independent of
the visual/browser QA and do not replace it.
"""
from __future__ import annotations

import math
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1] / "docs/assets/concept-animations"
NS = {"s": "http://www.w3.org/2000/svg"}


def check_temperature() -> None:
    root = ET.parse(ROOT / "temperature-softmax-motion.svg").getroot()
    animations = root.findall(".//s:animate", NS)
    assert animations, "Temperature motion must contain real SVG animations"
    # The bars encode exact softmax values at T=0.5, ... 2.0, ... 0.5.
    bars = [r for r in root.findall(".//s:rect", NS)
            if any(a.get("attributeName") == "height" for a in r.findall("s:animate", NS))]
    assert len(bars) == 3, f"Expected three animated class bars, got {len(bars)}"
    for i, bar in enumerate(bars):
        motion = next(a for a in bar.findall("s:animate", NS)
                      if a.get("attributeName") == "height")
        values = [float(v) for v in motion.attrib["values"].split(";")]
        keys = [float(v) for v in motion.attrib["keyTimes"].split(";")]
        assert len(values) == len(keys) == 81
        assert all(b > a for a, b in zip(keys, keys[1:]))
        assert math.isclose(keys[0], 0) and math.isclose(keys[-1], 1)
        for j, height in enumerate(values):
            t = 0.5 + 1.5 * (min(j, 80 - j) / 40)
            logits = (3., 1., 0.)
            weights = [math.exp(z / t) for z in logits]
            p = weights[i] / sum(weights)
            # Plot height: 148 SVG units for probability 1.
            assert abs(height - 148 * p) < 0.012, (i, j, height, p)
        assert all(abs(values[j] - values[80 - j]) < 0.002 for j in range(41))
    # Ensure bars remain grounded on the same baseline and normalized.
    # Height-only checks miss an SVG y-coordinate regression.
    for j in range(81):
        total = 0.0
        for bar in bars:
            motions = {a.get("attributeName"): a for a in bar.findall("s:animate", NS)}
            assert "y" in motions
            heights = [float(v) for v in motions["height"].get("values").split(";")]
            positions = [float(v) for v in motions["y"].get("values").split(";")]
            assert len(heights) == len(positions) == 81
            assert abs(positions[j] + heights[j] - 260) < 0.002
            assert 0 <= heights[j] <= 148
            total += heights[j]
        assert abs(total - 148) < 0.002
    # Strict ordering means temperature changes confidence, not the argmax.
    for j in range(81):
        heights = []
        for bar in bars:
            a = next(a for a in bar.findall("s:animate", NS)
                     if a.get("attributeName") == "height")
            heights.append(float(a.attrib["values"].split(";")[j]))
        assert heights[0] > heights[1] > heights[2]



def check_temperature_timeline() -> None:
    """The temperature cursor must encode the same samples as all three bars."""
    root = ET.parse(ROOT / "temperature-softmax-motion.svg").getroot()
    bars = [r for r in root.findall(".//s:rect", NS)
            if any(a.get("attributeName") == "height" for a in r.findall("s:animate", NS))]
    cursor = next(c for c in root.findall(".//s:circle", NS)
                  if any(a.get("attributeName") == "cx" for a in c.findall("s:animate", NS)))
    cursor_motion = next(a for a in cursor.findall("s:animate", NS)
                         if a.get("attributeName") == "cx")
    cursor_x = [float(x) for x in cursor_motion.get("values").split(";")]
    timeline = cursor_motion.get("keyTimes")
    assert len(cursor_x) == 81
    assert all(abs(cursor_x[j] - (104 + 427 * min(j, 80-j) / 40)) < 0.002
               for j in range(81))
    for bar in bars:
        animations = {a.get("attributeName"): a for a in bar.findall("s:animate", NS)}
        assert animations["height"].get("keyTimes") == timeline
        assert animations["y"].get("keyTimes") == timeline
        assert animations["height"].get("dur") == cursor_motion.get("dur") == "9s"
        assert animations["y"].get("dur") == "9s"
        assert animations["height"].get("repeatCount") == "indefinite"
        assert animations["y"].get("repeatCount") == "indefinite"
    assert cursor_motion.get("repeatCount") == "indefinite"
    # SVG's initial attributes must agree with the first animation frame:
    # otherwise the fallback/first paint shows an inconsistent probability.
    for bar in bars:
        animations = {a.get("attributeName"): a for a in bar.findall("s:animate", NS)}
        for attr in ("height", "y"):
            first = float(animations[attr].get("values").split(";")[0])
            assert abs(float(bar.get(attr)) - first) < 0.002, attr
    assert abs(float(cursor.get("cx")) - cursor_x[0]) < 0.002


def check_conformal() -> None:
    root = ET.parse(ROOT / "conformal-quantile-motion.svg").getroot()
    labels = " ".join((t.text or "") for t in root.findall(".//s:text", NS))
    scores = (0.08, 0.13, 0.21, 0.29, 0.35, 0.41, 0.54, 0.68)
    assert all(f"{v:.2f}" in labels for v in scores)
    n, alpha = len(scores), 0.25
    rank = math.ceil((n + 1) * (1 - alpha))
    assert rank == 7 and scores[rank - 1] == 0.54
    candidates = {"A": 0.19, "B": 0.48, "C": 0.71}
    assert {k for k, v in candidates.items() if v <= scores[rank - 1]} == {"A", "B"}
    for score in candidates.values():
        assert f"{score:.2f}" in labels
    # Ensure the threshold and set-membership outcomes are genuinely animated,
    # rather than presenting a static completed answer at every time point.
    animated = root.findall(".//s:animate", NS)
    assert len(animated) >= 10
    assert any(a.get("attributeName") == "stroke-dashoffset" for a in animated)
    assert any(a.get("attributeName") == "opacity" for a in animated)
    assert "prefers-reduced-motion" in (root.find("s:style", NS).text or "")



def check_conformal_geometry() -> None:
    """Calibration positions must encode their scores on one common axis."""
    root = ET.parse(ROOT / "conformal-quantile-motion.svg").getroot()
    circles = [c for c in root.findall(".//s:circle", NS)
               if c.get("cy") == "155"]
    scores = (0.08, 0.13, 0.21, 0.29, 0.35, 0.41, 0.54, 0.68)
    assert len(circles) == len(scores), len(circles)
    positions = [float(c.get("cx")) for c in circles]
    assert positions == sorted(positions)
    # The schematic uses x = 65 + 678.75 * nonconformity score.
    for x, score in zip(positions, scores):
        assert abs(x - (65 + 678.75 * score)) < 0.11, (x, score)
    threshold = next(p for p in root.findall(".//s:path", NS)
                     if p.get("stroke-dashoffset") == "40")
    assert threshold.get("d") == "M431.5 105V145"
    assert abs(positions[6] - 431.5) < 0.11
    # Each successive calibration marker is revealed no earlier than
    # the previous one.  A regression must not reorder the sample.
    reveal = []
    for circle in circles:
        opacity = next(a for a in circle.findall("s:animate", NS)
                       if a.get("attributeName") == "opacity")
        times = [float(t) for t in opacity.get("keyTimes").split(";")]
        assert opacity.get("dur") == "10s"
        assert opacity.get("repeatCount") == "indefinite"
        reveal.append(times[1])
    assert reveal == sorted(reveal)
    assert reveal[0] >= 0 and reveal[-1] < 1


if __name__ == "__main__":
    check_temperature()
    check_temperature_timeline()
    check_conformal()
    check_conformal_geometry()
    print("Uncertainty animation numerical and structural regression: PASS")
