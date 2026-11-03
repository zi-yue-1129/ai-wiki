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
