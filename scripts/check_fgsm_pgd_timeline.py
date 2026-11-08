"""Regression checks for the bilingual FGSM/PGD teaching timeline.

Run from the repository root: python scripts/check_fgsm_pgd_timeline.py
This checks source timing only; it does not replace browser rendering or visual QA.
"""
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SVG = ROOT / "docs/assets/concept-animations/fgsm-pgd-trajectory.svg"
PAGES = [
    ROOT / "docs/theory/machine-learning/adversarial-robustness/pgd-adversarial-training.md",
    ROOT / "docs/theory/machine-learning/adversarial-robustness/pgd-adversarial-training.zh-TW.md",
]
NS = {"s": "http://www.w3.org/2000/svg"}


def close(actual: float, expected: float) -> None:
    assert abs(actual - expected) < 1e-8, (actual, expected)


def main() -> None:
    root = ET.parse(SVG).getroot()
    markers = root.findall(".//s:circle[@class='moving-marker']", NS)
    assert len(markers) == 4, "Expected FGSM, PGD, candidate and projection markers"
    candidate, projection, fgsm, pgd = markers

    def motion(circle: ET.Element) -> ET.Element:
        result = circle.find("s:animateMotion", NS)
        assert result is not None
        assert result.get("dur") == "5s"
        assert result.get("repeatCount") == "1"
        return result

    fgsm_motion = motion(fgsm)
    pgd_motion = motion(pgd)
    candidate_motion = motion(candidate)
    projection_motion = motion(projection)

    def timeline(element: ET.Element, key: str) -> list[float]:
        return [float(v) for v in element.attrib[key].split(";")]

    # The final FGSM position is reached at 2.5 s, not during projection.
    assert timeline(fgsm_motion, "keyTimes") == [0.0, 0.5, 1.0]
    assert timeline(fgsm_motion, "keyPoints") == [0.0, 1.0, 1.0]
    assert timeline(pgd_motion, "keyTimes") == [0.0, 0.25, 0.5, 1.0]

    # Candidate traverses 2.5–3.5 s, projection traverses 3.5–5 s.
    assert timeline(candidate_motion, "keyTimes") == [0.0, 0.5, 0.7, 1.0]
    assert timeline(candidate_motion, "keyPoints") == [0.0, 0.0, 1.0, 1.0]
    assert timeline(projection_motion, "keyTimes") == [0.0, 0.7, 1.0]
    assert timeline(projection_motion, "keyPoints") == [0.0, 0.0, 1.0]
    close(5 * timeline(projection_motion, "keyTimes")[1], 3.5)

    # Visibility must follow motion: the candidate appears just after 2.5 s,
    # disappears at 3.5 s, and projection begins at that handoff.
    candidate_opacity = candidate.find("s:animate[@attributeName='opacity']", NS)
    projection_opacity = projection.find("s:animate[@attributeName='opacity']", NS)
    assert candidate_opacity is not None and projection_opacity is not None
    assert timeline(candidate_opacity, "keyTimes") == [0.0, 0.5, 0.51, 0.69, 0.7, 1.0]
    assert timeline(candidate_opacity, "values") == [0.0, 0.0, 1.0, 1.0, 0.0, 0.0]
    assert timeline(projection_opacity, "keyTimes") == [0.0, 0.69, 0.7]
    assert timeline(projection_opacity, "values") == [0.0, 0.0, 1.0]
    for opacity in (candidate_opacity, projection_opacity):
        assert opacity.get("calcMode") == "discrete"
        assert opacity.get("repeatCount") == "1"
    assert candidate.get("opacity") == "0"
    assert projection.get("opacity") == "0"

    # Verify the geometric endpoint of the projection, not only its timing.
    # The out-of-budget point (660, 87) must return to the L-infinity
    # feasible-set right edge x=636 without changing its y coordinate.
    assert (float(projection.get("cx")), float(projection.get("cy"))) == (660.0, 87.0)
    assert projection_motion.get("path") == "M0 0H-24"
    budget = next(
        rect for rect in root.findall(".//s:rect", NS)
        if rect.get("x") == "448" and rect.get("y") == "80"
    )
    close(float(budget.get("x")) + float(budget.get("width")), 636.0)
    assert float(budget.get("y")) <= float(projection.get("cy")) <= float(budget.get("y")) + float(budget.get("height"))

    # Guard the actual animated PGD geometry as well as its phase timing.
    # The teal marker starts at the clean input and reaches the candidate
    # origin (595, 120) before the orange candidate is revealed.
    assert (float(pgd.get("cx")), float(pgd.get("cy"))) == (542.0, 170.0)
    assert pgd_motion.get("path") == "M0 0L28 -23L53 -50"
    # keyPoints are fractions of total path length, not per-segment indices.
    # At 1.25 s (25% of 5 s), the marker should be at the first teal
    # vertex (570,147), not already partway through the next segment.
    import math
    first_length = math.hypot(28, 23)
    second_length = math.hypot(25, 27)
    first_fraction = first_length / (first_length + second_length)
    points = timeline(pgd_motion, "keyPoints")
    assert len(points) == 4 and points[0] == 0 and points[-2:] == [1, 1]
    assert abs(points[1] - first_fraction) < 1e-6, (points, first_fraction)
    # The static GitHub fallback must tell the same story as SMIL motion.
    # A future edit to the visible strokes must not silently disagree with
    # the moving markers, even if the keyframe-only checks still pass.
    strokes = [p.get("d") for p in root.findall(".//s:path", NS)]
    assert "M180 170L274 80" in strokes, "FGSM visible arrow differs from motion"
    assert "M542 170L570 147L595 120" in strokes, "PGD visible trace differs from motion"
    assert "M595 120L660 87" in strokes, "Candidate visible trace differs from motion"
    assert "M660 87H636" in strokes, "Projection visible trace differs from motion"
    assert (float(pgd.get("cx")) + 53, float(pgd.get("cy")) - 50) == (595.0, 120.0)
    assert (float(fgsm.get("cx")) + 94, float(fgsm.get("cy")) - 90) == (274.0, 80.0)
    assert (float(candidate.get("cx")), float(candidate.get("cy"))) == (595.0, 120.0)
    assert candidate_motion.get("path") == "M0 0L65 -33"
    close(float(candidate.get("cx")) + 65.0, float(projection.get("cx")))
    close(float(candidate.get("cy")) - 33.0, float(projection.get("cy")))

    # Progressive colored traces must reveal the same phases as moving markers.
    # These checks are structural only; the Chromium workflow tests rendered motion.
    animated_strokes = [
        p for p in root.findall(".//s:path", NS)
        if p.find("s:animate[@attributeName='stroke-dashoffset']", NS) is not None
    ]
    assert len(animated_strokes) == 4, "Expected four progressive teaching strokes"
    expected = [
        ("M180 170L274 80", 131.0, [0.0, 0.5, 1.0], [131.0, 0.0, 0.0]),
        ("M542 170L570 147L595 120", 75.0, [0.0, 0.5, 1.0], [75.0, 0.0, 0.0]),
        ("M595 120L660 87", 73.0, [0.0, 0.5, 0.7, 1.0], [73.0, 73.0, 0.0, 0.0]),
        ("M660 87H636", 24.0, [0.0, 0.7, 1.0], [24.0, 24.0, 0.0]),
    ]
    for stroke, (geometry, length, times, values) in zip(animated_strokes, expected):
        assert stroke.get("d") == geometry, (stroke.get("d"), geometry)
        close(float(stroke.get("stroke-dasharray")), length)
        close(float(stroke.get("stroke-dashoffset")), length)
        reveal = stroke.find("s:animate[@attributeName='stroke-dashoffset']", NS)
        assert reveal is not None
        assert timeline(reveal, "keyTimes") == times
        assert timeline(reveal, "values") == values
        assert reveal.get("dur") == "5s"
        assert reveal.get("repeatCount") == "1"
        assert reveal.get("fill") == "freeze"
    # The pale fallback paths must remain present for GitHub's SVG sanitizer.
    for geometry, _, _, _ in expected:
        assert any(
            p.get("d") == geometry and float(p.get("opacity", "1")) < 0.5
            for p in root.findall(".//s:path", NS)
        ), f"Missing static fallback for {geometry}"

    # Fixed destination markers must not reveal a future state before the
    # corresponding moving marker reaches it. This is a known visual-timeline
    # hazard: an endpoint at 2.5 s would spoil the 2.5–3.5 s candidate step.
    # The endpoint must be initially hidden, become visible only at arrival,
    # and remain visible after the one-shot animation finishes. This is a
    # source-level guard, not a substitute for browser visual inspection.
    for class_name, earliest in (("phase-candidate", 0.7), ("phase-projection", 1.0)):
        for element in root.findall(f".//*[@class='{class_name}']"):
            opacity = element.find("s:animate[@attributeName='opacity']", NS)
            assert opacity is not None, (class_name, "missing visibility timing")
            assert opacity.get("calcMode") == "discrete", class_name
            assert opacity.get("dur") == "5s", class_name
            assert opacity.get("repeatCount") == "1", class_name
            assert opacity.get("fill") == "freeze", class_name
            assert element.get("opacity", "1") == "1", (
                class_name, "the initial opacity is controlled by SMIL at t=0",
            )
            times = timeline(opacity, "keyTimes")
            values = timeline(opacity, "values")
            assert len(times) == len(values), class_name
            assert times[0] == 0 and times[-1] <= 1, class_name
            assert all(0 <= t <= 1 for t in times), class_name
            assert all(x < y for x, y in zip(times, times[1:])), class_name
            assert values[0] == 0 and values[-1] == 1, class_name
            assert set(values) <= {0.0, 1.0}, class_name
            first_visible = next((t for t, v in zip(times, values) if v > 0), None)
            assert first_visible is not None and first_visible >= earliest, (
                class_name, first_visible, earliest,
            )

    # Every visible PGD iterate must remain feasible before the proposed
    # out-of-budget step. Guard all polyline vertices rather than only the
    # final marker; an accidentally misplaced intermediate point would
    # otherwise silently contradict the chapter's teaching sequence.
    import math
    pgd_path = pgd_motion.get("path")
    coordinates = re.findall(r"([ML])(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)", pgd_path or "")
    assert len(coordinates) == 3 and coordinates[0][0] == "M", (pgd_path, coordinates)
    for command, dx, dy in coordinates:
        assert command in ("M", "L")
        px, py = float(pgd.get("cx")) + float(dx), float(pgd.get("cy")) + float(dy)
        assert float(budget.get("x")) <= px <= float(budget.get("x")) + float(budget.get("width")) and float(budget.get("y")) <= py <= float(budget.get("y")) + float(budget.get("height")), (px, py)
        assert math.isfinite(px) and math.isfinite(py)

    # The projected point must lie inside the right-hand epsilon rectangle,
    # while the unprojected candidate must lie strictly outside it.
    left = float(budget.get("x"))
    right = left + float(budget.get("width"))
    top = float(budget.get("y"))
    bottom = top + float(budget.get("height"))
    assert left <= 636.0 <= right and top <= 87.0 <= bottom
    assert float(projection.get("cx")) > right
    assert float(candidate.get("cx")) >= left

    # Projection onto an axis-aligned L-infinity ball is coordinate-wise
    # clipping. Reconstruct the projected endpoint from the animated path,
    # rather than assuming the purple static dot is necessarily correct.
    # This also guards against a future candidate whose y coordinate exceeds
    # the feasible interval but whose x coordinate is clipped correctly.
    candidate_end = (
        float(candidate.get("cx")) + 65.0,
        float(candidate.get("cy")) - 33.0,
    )
    projected_end = (
        min(max(candidate_end[0], left), right),
        min(max(candidate_end[1], top), bottom),
    )
    horizontal_projection = re.fullmatch(
        r"M0 0H(-?\d+(?:\.\d+)?)",
        projection_motion.get("path") or "",
    )
    assert horizontal_projection is not None, projection_motion.get("path")
    animated_end = (
        float(projection.get("cx")) + float(horizontal_projection.group(1)),
        float(projection.get("cy")),
    )
    assert animated_end == projected_end, (animated_end, projected_end)
    assert (636.0, 87.0) == projected_end

    # FGSM must finish at its budget corner, not merely at the specified
    # timestamp. Its animated displacement must agree with the static end.
    assert (float(fgsm.get("cx")), float(fgsm.get("cy"))) == (180.0, 170.0)
    assert fgsm_motion.get("path") == "M0 0L94 -90"
    fgsm_budget = next(
        rect for rect in root.findall(".//s:rect", NS)
        if rect.get("x") == "86" and rect.get("y") == "80"
    )
    fgsm_x, fgsm_y = 180.0 + 94.0, 170.0 - 90.0
    assert float(fgsm_budget.get("x")) <= fgsm_x <= float(fgsm_budget.get("x")) + float(fgsm_budget.get("width"))
    assert float(fgsm_budget.get("y")) <= fgsm_y <= float(fgsm_budget.get("y")) + float(fgsm_budget.get("height"))
    # A full FGSM sign update with two nonzero components reaches a corner.
    close(fgsm_x, float(fgsm_budget.get("x")) + float(fgsm_budget.get("width")))
    close(fgsm_y, float(fgsm_budget.get("y")))

    # An L-infinity perturbation set is centered on the clean input, not
    # merely a rectangle that happens to contain the trajectory. Validate
    # both panels independently so changes to their geometry stay honest.
    # Both rectangles were corrected to y=80 (center y=170). Keep this
    # regression guard tied to the actual clean-input coordinates.
    for rectangle, clean_point in ((fgsm_budget, fgsm), (budget, pgd)):
        center_x = float(rectangle.get("x")) + float(rectangle.get("width")) / 2
        center_y = float(rectangle.get("y")) + float(rectangle.get("height")) / 2
        close(center_x, float(clean_point.get("cx")))
        close(center_y, float(clean_point.get("cy")))

    # GitHub's static fallback and reduced-motion view must retain the
    # completed endpoints even when SMIL motion is not available.
    endpoints = root.findall(".//s:circle[@class='endpoint-marker']", NS)
    assert len(endpoints) == 1
    assert (endpoints[0].get("cx"), endpoints[0].get("cy")) == ("274", "80")
    css = " ".join(style.text or "" for style in root.findall(".//s:style", NS))
    assert "prefers-reduced-motion: reduce" in css
    assert ".moving-marker { display: none" in css
    assert ".endpoint-marker { opacity: 1" in css

    for page in PAGES:
        body = page.read_text(encoding="utf-8")
        assert "2.5–3.5" in body, page
        assert "3.5–5" in body, page
        assert not re.search(r"(?:from |於 )4–5 秒?", body), page

    # Independently recompute the bilingual teaching trace. The candidate
    # must be projected after EACH iteration; clipping only the final state
    # produces a different answer even with identical hypothetical signs.
    # Keep the numerical invariant separate from the SVG drawing geometry.
    clean, epsilon, alpha = 0.50, 0.10, 0.08
    signs = (+1, +1, -1)
    lo, hi = clean - epsilon, clean + epsilon
    projected_trace = [clean]
    unprojected_trace = [clean]
    for sign in signs:
        proposed = projected_trace[-1] + alpha * sign
        projected_trace.append(min(hi, max(lo, proposed)))
        unprojected_trace.append(unprojected_trace[-1] + alpha * sign)
    assert all(abs(a - b) < 1e-9 for a, b in zip(
        projected_trace, (0.50, 0.58, 0.60, 0.52)
    )), projected_trace
    assert all(abs(a - b) < 1e-9 for a, b in zip(
        unprojected_trace, (0.50, 0.58, 0.66, 0.58)
    )), unprojected_trace
    assert unprojected_trace[2] > hi
    delayed_projection = min(hi, max(lo, unprojected_trace[-1]))
    assert abs(delayed_projection - 0.58) < 1e-9
    assert abs(delayed_projection - projected_trace[-1]) > 0.05

    # Both translations must preserve the same explanatory numerical trace.
    # These are teaching values, never model-derived measurements.
    for page in PAGES:
        body = page.read_text(encoding="utf-8")
        for trace in (
            "0.50 \\rightarrow 0.58 \\rightarrow 0.60 \\rightarrow 0.52",
            "0.50 \\rightarrow 0.58 \\rightarrow 0.66 \\rightarrow 0.58",
        ):
            assert trace in body, (page, trace)

    # Accessibility and GitHub preview regression guards. These are static
    # checks only: they cannot prove browser or sanitizer behaviour.
    svg_ns = "{http://www.w3.org/2000/svg}"
    assert root.tag == svg_ns + "svg"
    assert root.get("role") == "img"
    labelled = (root.get("aria-labelledby") or "").split()
    assert len(labelled) == 2
    identified = {node.get("id"): node for node in root.iter() if node.get("id")}
    for label_id, tag in zip(labelled, ("title", "desc")):
        assert label_id in identified, (label_id, "missing accessible label")
        assert identified[label_id].tag == svg_ns + tag
        assert "".join(identified[label_id].itertext()).strip()
    description = "".join(identified[labelled[1]].itertext()).lower()
    for concept in ("fgsm", "pgd", "projection", "not measured", "static preview"):
        assert concept in description, concept
    assert not root.findall(".//s:script", NS), "SVG must not embed scripts"
    for node in root.iter():
        for key, value in node.attrib.items():
            assert not key.lower().startswith("on"), (node.tag, key)
            if key.endswith("}href") or key == "href":
                assert value.startswith("#"), (node.tag, key, value)
    # A static source check must cover every animation, not just the four
    # moving markers. A newly introduced looping or delayed element could
    # undermine the one-shot teaching sequence or reduced-motion fallback.
    animations = [node for node in root.iter() if node.tag in (
        svg_ns + "animate", svg_ns + "animateMotion", svg_ns + "animateTransform"
    )]
    assert animations, "Expected a timed teaching animation"
    for animation in animations:
        assert animation.get("dur") == "5s", (animation.tag, animation.attrib)
        assert animation.get("repeatCount") == "1", (animation.tag, animation.attrib)
        assert animation.get("fill") == "freeze", (animation.tag, animation.attrib)
        assert not animation.get("begin"), (animation.tag, "unexpected delayed start")
        if animation.get("keyTimes"):
            times = timeline(animation, "keyTimes")
            assert times[0] == 0.0 and times[-1] <= 1.0, times
            assert all(0 <= t <= 1 for t in times), times
            assert all(a < b for a, b in zip(times, times[1:])), times
        if animation.get("keyPoints"):
            points = timeline(animation, "keyPoints")
            assert len(points) == len(timeline(animation, "keyTimes"))
            assert all(0 <= p <= 1 for p in points), points
            assert all(a <= b for a, b in zip(points, points[1:])), points
    # The SVG must remain self-contained for GitHub's static rendering.
    assert not root.findall(".//s:foreignObject", NS)
    assert not root.findall(".//s:image", NS)
    assert "@import" not in css and "url(" not in css

    # Both language versions must embed the same shared visual asset.
    fgsm_pages = [
        ROOT / "docs/theory/machine-learning/adversarial-robustness/fgsm.md",
        ROOT / "docs/theory/machine-learning/adversarial-robustness/fgsm.zh-TW.md",
    ]
    for page in fgsm_pages:
        body = page.read_text(encoding="utf-8")
        assert body.count("../../../assets/concept-animations/fgsm-pgd-trajectory.svg") == 1, page
        assert "2.5–3.5" in body and "3.5–5" in body, page

    print("FGSM/PGD timing and bilingual captions: OK")
    print("Browser motion, reduced-motion and visual inspection: NOT tested")


if __name__ == "__main__":
    main()
