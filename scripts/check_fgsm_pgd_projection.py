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


def check_projection_invariants():
    """Exercise boundary cases beyond the worked examples.

    The projection must be feasible, idempotent, and coordinate-wise optimal
    for the intersection of the input range and the L-infinity budget.
    """
    for clean in (0.0, 0.02, 0.5, 0.98, 1.0):
        for epsilon in (0.0, 0.01, 0.1, 0.5):
            lo = max(0.0, clean - epsilon)
            hi = min(1.0, clean + epsilon)
            for candidate in (-0.5, 0.0, 0.15, 0.5, 0.85, 1.0, 1.5):
                (result,) = project((candidate,), (clean,), epsilon)
                assert lo - 1e-12 <= result <= hi + 1e-12
                assert math.isclose(result, min(hi, max(lo, candidate)), abs_tol=1e-12)
                near(project((result,), (clean,), epsilon), (result,))
    # Independent coordinates must not share a clipping interval.
    near(project((-0.5, 1.5), (0.02, 0.98), 0.1), (0.0, 1.0))
    # A mismatched dimensionality is a programming error, not silent truncation.
    try:
        project((0.1, 0.2), (0.1,), 0.1)
    except ValueError:
        pass
    else:
        raise AssertionError("Projection must reject mismatched dimensions")


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




def check_motion_timing_and_fallback():
    """Guard against loops, disappearing fallback paths, and malformed motion timing.

    Structural assertions only: browser playback and visual QA remain separate.
    """
    root = ET.parse(SVG).getroot()
    ns = "{http://www.w3.org/2000/svg}"
    animations = list(root.iter(ns + "animate")) + list(root.iter(ns + "animateMotion"))
    assert animations, "Expected an instructional motion sequence"
    for animation in animations:
        assert animation.get("repeatCount") == "1", "Motion must not loop indefinitely"
        assert animation.get("dur") == "5s", "Motion timing drifted from the documented sequence"
        if animation.tag == ns + "animateMotion":
            assert animation.get("calcMode") == "linear", "Motion interpolation should be explicit"
            path = animation.get("path", "")
            assert path.startswith("M"), "Motion requires an explicit path"
            assert animation.get("keyTimes") and animation.get("keyPoints")
    # All persistent paths are drawn outside animated groups. SVG image fallback
    # should remain intelligible when browser animation is unavailable.
    for path in root.iter(ns + "path"):
        if path.get("d") in {
            "M542 170L570 147L595 120",
            "M595 120L660 87",
            "M660 87H636",
        }:
            assert not any(k.startswith("on") for k in path.attrib), "No inline event handlers"
            assert path.get("opacity", "1") != "0", "Fallback geometry must remain visible"
    title = root.find("s:title", NS)
    desc = root.find("s:desc", NS)
    assert title is not None and (title.text or "").strip()
    assert desc is not None and "projection" in (desc.text or "").lower()

def check_geometric_projection_consistency():
    """Verify the drawn candidate and return motion agree with the budget box.

    This catches a visually misleading endpoint even when SMIL syntax is valid.
    Coordinates are schematic, not an empirical gradient trace.
    """
    root = ET.parse(SVG).getroot()
    ns = "{http://www.w3.org/2000/svg}"
    boxes = [r for r in root.iter(ns + "rect") if r.get("stroke-dasharray")]
    assert len(boxes) == 2, "Expected FGSM and PGD feasible-set boxes"
    box = boxes[1]
    left = float(box.get("x"))
    right = left + float(box.get("width"))
    top = float(box.get("y"))
    bottom = top + float(box.get("height"))
    candidate = (660.0, 87.0)
    projected = (636.0, 87.0)
    assert candidate[0] > right, "Candidate must exceed the illustrated budget"
    assert projected[0] == right, "Projection must land on the right boundary"
    assert top <= projected[1] <= bottom, "Projected point must be feasible"

    projected_markers = [
        c for c in root.iter(ns + "circle")
        if c.get("cx") == "660" and c.get("cy") == "87"
        and c.find(ns + "animateMotion") is not None
    ]
    assert len(projected_markers) == 1, "Expected one projected moving marker"
    motion = projected_markers[0].find(ns + "animateMotion")
    assert motion is not None
    assert motion.get("path") == "M0 0H-24", (
        "Animated projection displacement must match the static endpoint"
    )
    assert candidate[0] - projected[0] == 24
    assert any(
        p.get("d") == "M660 87H636" for p in root.iter(ns + "path")
    ), "Static projection return must agree with animated displacement"


if __name__ == "__main__":
    check_numerical_examples()
    check_projection_invariants()
    check_svg()
    check_motion_timing_and_fallback()
    check_geometric_projection_consistency()
    print("FGSM/PGD numerical examples and SVG semantic checks passed.")
