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
        if rect.get("x") == "448" and rect.get("y") == "70"
    )
    close(float(budget.get("x")) + float(budget.get("width")), 636.0)
    assert 70.0 <= float(projection.get("cy")) <= 250.0

    # Guard the actual animated PGD geometry as well as its phase timing.
    # The teal marker starts at the clean input and reaches the candidate
    # origin (595, 120) before the orange candidate is revealed.
    assert (float(pgd.get("cx")), float(pgd.get("cy"))) == (542.0, 170.0)
    assert pgd_motion.get("path") == "M0 0L28 -23L53 -50"
    assert timeline(pgd_motion, "keyPoints") == [0.0, 0.53, 1.0, 1.0]
    # The static GitHub fallback must tell the same story as SMIL motion.
    # A future edit to the visible strokes must not silently disagree with
    # the moving markers, even if the keyframe-only checks still pass.
    strokes = [p.get("d") for p in root.findall(".//s:path", NS)]
    assert "M180 170L259 103" in strokes, "FGSM visible arrow differs from motion"
    assert "M542 170L570 147L595 120" in strokes, "PGD visible trace differs from motion"
    assert "M595 120L660 87" in strokes, "Candidate visible trace differs from motion"
    assert "M660 87H636" in strokes, "Projection visible trace differs from motion"
    assert (float(pgd.get("cx")) + 53, float(pgd.get("cy")) - 50) == (595.0, 120.0)
    assert (float(fgsm.get("cx")) + 79, float(fgsm.get("cy")) - 67) == (259.0, 103.0)
    assert (float(candidate.get("cx")), float(candidate.get("cy"))) == (595.0, 120.0)
    assert candidate_motion.get("path") == "M0 0L65 -33"
    close(float(candidate.get("cx")) + 65.0, float(projection.get("cx")))
    close(float(candidate.get("cy")) - 33.0, float(projection.get("cy")))

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
        assert 448.0 <= px <= 636.0 and 70.0 <= py <= 250.0, (px, py)
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

    # FGSM must finish inside its own budget, not merely at the specified
    # timestamp. Its animated displacement must agree with the static end.
    assert (float(fgsm.get("cx")), float(fgsm.get("cy"))) == (180.0, 170.0)
    assert fgsm_motion.get("path") == "M0 0L79 -67"
    fgsm_budget = next(
        rect for rect in root.findall(".//s:rect", NS)
        if rect.get("x") == "86" and rect.get("y") == "70"
    )
    fgsm_x, fgsm_y = 180.0 + 79.0, 170.0 - 67.0
    assert float(fgsm_budget.get("x")) <= fgsm_x <= float(fgsm_budget.get("x")) + float(fgsm_budget.get("width"))
    assert float(fgsm_budget.get("y")) <= fgsm_y <= float(fgsm_budget.get("y")) + float(fgsm_budget.get("height"))

    # GitHub's static fallback and reduced-motion view must retain the
    # completed endpoints even when SMIL motion is not available.
    endpoints = root.findall(".//s:circle[@class='endpoint-marker']", NS)
    assert len(endpoints) == 1
    assert (endpoints[0].get("cx"), endpoints[0].get("cy")) == ("259", "103")
    css = " ".join(style.text or "" for style in root.findall(".//s:style", NS))
    assert "prefers-reduced-motion: reduce" in css
    assert ".moving-marker { display: none" in css
    assert ".endpoint-marker { opacity: 1" in css

    for page in PAGES:
        body = page.read_text(encoding="utf-8")
        assert "2.5–3.5" in body, page
        assert "3.5–5" in body, page
        assert not re.search(r"(?:from |於 )4–5 秒?", body), page

    print("FGSM/PGD timing and bilingual captions: OK")
    print("Browser motion, reduced-motion and visual inspection: NOT tested")


if __name__ == "__main__":
    main()
