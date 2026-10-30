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


if __name__ == "__main__":
    check_temperature()
    check_conformal()
    print("Uncertainty animation numerical and structural regression: PASS")
