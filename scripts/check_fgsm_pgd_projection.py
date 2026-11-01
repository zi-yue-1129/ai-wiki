#!/usr/bin/env python3
"""Check the numerical claims and static fallback geometry of the FGSM/PGD visual.

This is a semantic/structural check, NOT a substitute for browser rendering or
manual visual QA. Run from the repository root:
    python scripts/check_fgsm_pgd_projection.py
"""
from pathlib import Path
import math
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SVG = ROOT / "docs/assets/concept-animations/fgsm-pgd-trajectory.svg"
NS = {"s": "http://www.w3.org/2000/svg"}


def project(z, x, epsilon, lower=0.0, upper=1.0):
    """Coordinate-wise Euclidean projection onto the bounded L-infinity ball."""
    if not (epsilon >= 0 and lower <= upper):
        raise ValueError("Invalid projection domain")
    return tuple(
        min(min(upper, center + epsilon), max(max(lower, center - epsilon), value))
        for value, center in zip(z, x, strict=True)
    )


def near(actual, expected):
    assert len(actual) == len(expected)
    assert all(math.isclose(a, b, abs_tol=1e-12) for a, b in zip(actual, expected)), (
        actual, expected
    )


def check_numerical_examples():
    near(project((0.64,), (0.50,), 0.10), (0.60,))
    near(project((1.08, 0.04), (0.95, 0.20), 0.10), (1.00, 0.10))
    x = (0.50,)
    step1 = project((x[0] + 0.08,), x, 0.10)
    step2 = project((step1[0] + 0.08,), x, 0.10)
    near(step1, (0.58,))
    near(step2, (0.60,))
    # Each update projects against the ORIGINAL clean input, not the last iterate.
    assert project((0.66,), (0.58,), 0.10) != step2


def check_svg():
    root = ET.parse(SVG).getroot()
    assert root.tag == "{http://www.w3.org/2000/svg}svg"
    assert root.attrib.get("viewBox") == "0 0 720 310"
    assert root.find("s:title", NS) is not None
    assert root.find("s:desc", NS) is not None
    style = root.find("s:style", NS)
    assert style is not None and "prefers-reduced-motion" in (style.text or "")
    # The complete teaching geometry must be present even when SMIL is disabled.
    paths = {p.attrib.get("d") for p in root.findall(".//s:path", NS)}
    assert "M542 170L570 147L595 120" in paths, "Missing feasible PGD iterates"
    assert "M595 120L660 87" in paths, "Missing out-of-budget candidate"
    assert "M660 87H636" in paths, "Missing projected return path"
    assert any(c.attrib.get("cx") == "636" and c.attrib.get("cy") == "87"
               for c in root.findall(".//s:circle", NS)), "Missing projected endpoint"
    for motion in root.findall(".//s:animateMotion", NS):
        times = [float(v) for v in motion.attrib["keyTimes"].split(";")]
        assert times[0] == 0 and times[-1] == 1
        assert all(a <= b for a, b in zip(times, times[1:]))
        points = [float(v) for v in motion.attrib["keyPoints"].split(";")]
        assert len(times) == len(points)
        assert all(0 <= p <= 1 for p in points)


if __name__ == "__main__":
    check_numerical_examples()
    check_svg()
    print("FGSM/PGD numerical examples and SVG semantic checks passed.")
