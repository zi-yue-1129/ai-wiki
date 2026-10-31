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
    # Causal sequence: the quantile cannot appear until every calibration
    # score has been revealed; candidate decisions follow the quantile.
    threshold = next(a for a in root.findall(".//s:animate", NS)
                     if a.get("attributeName") == "stroke-dashoffset")
    threshold_times = [float(t) for t in threshold.get("keyTimes").split(";")]
    assert threshold_times[1] >= reveal[-1], (threshold_times, reveal[-1])
    candidate_times = []
    for text in root.findall(".//s:text", NS):
        if (text.text or "").strip() not in ("IN", "OUT"):
            continue
        opacity = next(a for a in text.findall("s:animate", NS)
                       if a.get("attributeName") == "opacity")
        candidate_times.append(float(opacity.get("keyTimes").split(";")[1]))
    assert len(candidate_times) == 3
    assert min(candidate_times) >= threshold_times[2]
    summary = next(t for t in root.findall(".//s:text", NS)
                   if "Set =" in (t.text or ""))
    summary_motion = next(a for a in summary.findall("s:animate", NS)
                          if a.get("attributeName") == "opacity")
    summary_times = [float(t) for t in summary_motion.get("keyTimes").split(";")]
    assert summary_times[1] >= max(candidate_times)
    # The threshold badge and label must not disclose the result before the
    # quantile line, and the completed set must remain hidden until decisions.
    threshold_label = next(t for t in root.findall(".//s:text", NS)
                           if (t.text or "").strip() == "q = 0.54")
    label_motion = next(a for a in threshold_label.findall("s:animate", NS)
                        if a.get("attributeName") == "opacity")
    label_times = [float(t) for t in label_motion.get("keyTimes").split(";")]
    assert label_times[1] >= reveal[-1]
    assert label_times[2] >= threshold_times[2]
    assert summary_times[1] >= threshold_times[2]
    # Each candidate's visible decision must match its illustrative score.
    decisions = []
    for t in root.findall(".//s:text", NS):
        if (t.text or "").strip() in ("IN", "OUT"):
            decisions.append((t.text or "").strip())
    assert decisions == ["IN", "IN", "OUT"], decisions
    # Candidate outcomes must be genuinely concealed before the quantile is known.
    # A pale IN/OUT label or tinted decision pill leaks the result prematurely.
    decision_text = [t for t in root.findall(".//s:text", NS)
                     if (t.text or "").strip() in ("IN", "OUT")]
    assert len(decision_text) == 3
    for t in decision_text:
        assert float(t.get("opacity", "1")) == 0, t.text
        motion = next(a for a in t.findall("s:animate", NS)
                      if a.get("attributeName") == "opacity")
        values = [float(v) for v in motion.get("values").split(";")]
        times = [float(v) for v in motion.get("keyTimes").split(";")]
        assert values[:2] == [0, 0] and values[-1] == 1
        assert times[1] >= threshold_times[2]
    pills = [r for r in root.findall(".//s:rect", NS)
             if r.get("width") == "62" and r.get("height") == "29"]
    assert len(pills) == 3
    for pill in pills:
        assert float(pill.get("opacity", "1")) == 0
        motion = next(a for a in pill.findall("s:animate", NS)
                      if a.get("attributeName") == "opacity")
        values = [float(v) for v in motion.get("values").split(";")]
        times = [float(v) for v in motion.get("keyTimes").split(";")]
        assert values[:2] == [0, 0] and values[-1] == 1
        assert times[1] >= threshold_times[2]



def check_github_fallback_parity() -> None:
    """GitHub stills must encode the same numerical result as the motion."""
    animated = ET.parse(ROOT / "temperature-softmax-motion.svg").getroot()
    still = ET.parse(ROOT / "temperature-softmax-still.svg").getroot()
    motion_bars = [r for r in animated.findall(".//s:rect", NS)
                   if any(a.get("attributeName") == "height"
                          for a in r.findall("s:animate", NS))]
    still_bars = [r for r in still.findall(".//s:rect", NS)
                  if r.get("width") == "76" and r.get("rx") == "5"]
    assert len(motion_bars) == len(still_bars) == 3
    for i, (motion_bar, still_bar) in enumerate(zip(motion_bars, still_bars)):
        weights = [math.exp(z) for z in (3., 1., 0.)]
        expected = 148 * weights[i] / sum(weights)
        height = float(still_bar.get("height"))
        assert abs(height - expected) < 0.002, (i, height, expected)
        assert abs(float(still_bar.get("y")) + height - 260) < 0.002
        # The static fallback is T=1, not the motion's first T=0.5 frame.
    cursor = next(c for c in still.findall(".//s:circle", NS)
                  if c.get("r") == "11")
    assert abs(float(cursor.get("cx")) - (104 + 427 / 3)) < 0.002
    assert not still.findall(".//s:animate", NS)

    conformal = ET.parse(ROOT / "conformal-quantile-still.svg").getroot()
    labels = " ".join((t.text or "") for t in conformal.findall(".//s:text", NS))
    for expected in ("q = 0.54", "Set = {A, B}", "s = 0.19",
                     "s = 0.48", "s = 0.71", "IN", "OUT"):
        assert expected in labels, expected
    assert labels.count("IN") == 2 and labels.count("OUT") == 1
    circles = [c for c in conformal.findall(".//s:circle", NS)
               if c.get("cy") == "155"]
    assert len(circles) == 8
    assert all(float(c.get("opacity", "1")) == 1 for c in circles)
    threshold = next(p for p in conformal.findall(".//s:path", NS)
                     if p.get("d") == "M431.5 105V145")
    assert threshold.get("stroke-dashoffset") == "0"
    assert not conformal.findall(".//s:animate", NS)
    for doc in (still, conformal):
        assert doc.get("role") == "img"
        assert doc.get("aria-labelledby") == "title desc"
        assert doc.find("s:title", NS) is not None
        assert doc.find("s:desc", NS) is not None


def check_motion_accessibility_and_safety() -> None:
    """Reject unsafe SVG dependencies and inaccessible looping motion.

    This is structural protection, not a substitute for browser screenshots.
    """
    for filename in ("temperature-softmax-motion.svg", "conformal-quantile-motion.svg"):
        root = ET.parse(ROOT / filename).getroot()
        assert root.get("role") == "img", filename
        assert root.get("aria-labelledby") == "title desc", filename
        for name in ("title", "desc"):
            element = root.find(f"s:{name}", NS)
            assert element is not None and (element.text or "").strip(), (filename, name)
            assert element.get("id") == name, (filename, name)
        style = root.find("s:style", NS)
        assert style is not None
        css = "".join(style.itertext())
        assert "prefers-reduced-motion" in css and "animate" in css, filename
        for node in root.iter():
            tag = node.tag.rsplit("}", 1)[-1]
            assert tag not in ("script", "foreignObject", "image"), (filename, tag)
            for key, value in node.attrib.items():
                attr = key.rsplit("}", 1)[-1].lower()
                assert not attr.startswith("on"), (filename, attr)
                if attr in ("href", "src"):
                    assert value.startswith("#"), (filename, attr, value)
            if tag != "animate":
                continue
            assert node.get("repeatCount") == "indefinite", filename
            assert node.get("dur") in ("9s", "10s"), filename
            times = [float(v) for v in node.get("keyTimes", "").split(";")]
            values = node.get("values", "").split(";")
            assert len(times) == len(values) >= 2, (filename, tag)
            assert abs(times[0]) < 1e-9 and abs(times[-1] - 1) < 1e-9
            assert all(0 <= a < b <= 1 for a, b in zip(times, times[1:])), filename

if __name__ == "__main__":
    check_temperature()
    check_temperature_timeline()
    check_conformal()
    check_conformal_geometry()
    check_github_fallback_parity()
    check_motion_accessibility_and_safety()
    print("Uncertainty animation numerical and structural regression: PASS")
