"""Check probability-loss SVG coordinates, including between animation keyframes."""
import math
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
NS = "{http://www.w3.org/2000/svg}"


def check(stem, scale, losses):
    svg = ET.parse(ROOT / "docs/assets/concept-animations" / f"{stem}-motion.svg")
    checked = 0
    for circle in svg.getroot().findall(NS + "circle"):
        animations = {a.get("attributeName"): a for a in circle.findall(NS + "animate")}
        if not animations:
            continue
        x = [float(v) for v in animations["cx"].get("values").split(";")]
        y = [float(v) for v in animations["cy"].get("values").split(";")]
        times = [float(v) for v in animations["cx"].get("keyTimes").split(";")]
        assert animations["cx"].get("keyTimes") == animations["cy"].get("keyTimes")
        assert len(x) == len(y) == len(times) and times[0] == 0 and times[-1] == 1
        assert all(a < b for a, b in zip(times, times[1:]))
        loss = losses[circle.get("fill")]
        for i in range(len(x) - 1):
            for alpha in (0, .25, .5, .75, 1):
                xx = x[i] + alpha * (x[i + 1] - x[i])
                yy = y[i] + alpha * (y[i + 1] - y[i])
                probability = (xx - 86) / 476
                expected = 264 - scale * loss(probability)
                assert abs(yy - expected) < .1, (stem, i, alpha, yy, expected)
                checked += 1
    assert checked > 0
    print(f"{stem}: {checked} keyframe/interpolated coordinates passed")


if __name__ == "__main__":
    check("brier-expected-risk", 182, {
        "#007f85": lambda p: (1 - p) ** 2,
        "#c36d33": lambda p: p ** 2,
        "#7456ae": lambda p: (p - .7) ** 2 + .21,
    })
    check("log-loss-tail-penalty", 182 / 5, {
        "#007f85": lambda p: (1 - p) ** 2,
        "#c65070": lambda p: -math.log(p),
    })
    assert math.isclose(.7 * .3, .21)
    assert math.isclose(-math.log(.01), 4.605170185988091)
