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

    for page in PAGES:
        body = page.read_text(encoding="utf-8")
        assert "2.5–3.5" in body, page
        assert "3.5–5" in body, page
        assert not re.search(r"(?:from |於 )4–5 秒?", body), page

    print("FGSM/PGD timing and bilingual captions: OK")
    print("Browser motion, reduced-motion and visual inspection: NOT tested")


if __name__ == "__main__":
    main()
