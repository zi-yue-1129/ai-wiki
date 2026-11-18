#!/usr/bin/env python3
"""Check synthetic information-theory SVG timelines against exact definitions."""
from math import log, log2, isclose
from pathlib import Path
from xml.etree import ElementTree as ET

ASSETS = Path("docs/assets/concept-animations")
PAGES = Path("docs/theory/information-theory")
NS = "{http://www.w3.org/2000/svg}"


def binary_h(p: float) -> float:
    return -p * log2(p) - (1 - p) * log2(1 - p) if 0 < p < 1 else 0.0


def binary_kl(p: float, q: float) -> float:
    return p * log(p / q) + (1 - p) * log((1 - p) / (1 - q))


def animated_values(root: ET.Element, color: str, attribute: str) -> list[float]:
    for circle in root.iter(NS + "circle"):
        if circle.get("class") == "moving" and circle.get("fill") == color:
            for node in circle.findall(NS + "animate"):
                if node.get("attributeName") == attribute:
                    return [float(value) for value in node.attrib["values"].split(";")]
    raise AssertionError(f"Missing moving {color} circle / {attribute}")


def same_trace(got: list[float], expected: list[float]) -> None:
    assert len(got) == len(expected) == 49, (len(got), len(expected))
    for i, (actual, target) in enumerate(zip(got, expected)):
        assert isclose(actual, target, abs_tol=0.011), (i, actual, target)
    assert got[0] == got[-1], "animation must return continuously to its first frame"


def run() -> None:
    q = [0.25 + i * 0.65 / 24 for i in range(25)]
    q = q + list(reversed(q[:-1]))
    e = [i * 0.5 / 24 for i in range(25)]
    e = e + list(reversed(e[:-1]))
    kl_root = ET.parse(ASSETS / "bernoulli-kl-direction-motion.svg").getroot()
    same_trace(animated_values(kl_root, "#157c8c", "cx"), [76 + 410 * (v - 0.2) / 0.75 for v in q])
    for color, formula in (("#157c8c", lambda v: binary_kl(0.8, v)),
                           ("#d97737", lambda v: binary_kl(v, 0.8))):
        same_trace(animated_values(kl_root, color, "cy"),
                   [113 + 204 - 204 * formula(v) / 1.1 for v in q])
    channel_root = ET.parse(ASSETS / "binary-channel-information-motion.svg").getroot()
    for color, formula in (("#157c8c", lambda v: 1 - binary_h(v)),
                           ("#d97737", binary_h)):
        same_trace(animated_values(channel_root, color, "cx"), [402 + 245 * v / 0.5 for v in e])
        same_trace(animated_values(channel_root, color, "cy"),
                   [151 + 147 - 147 * formula(v) for v in e])
    assert isclose(binary_kl(0.8, 0.25), 0.6661694798, abs_tol=1e-9)
    assert isclose(binary_kl(0.25, 0.8), 0.7005291775, abs_tol=1e-9)
    assert isclose(binary_h(0.25), 0.8112781245, abs_tol=1e-9)
    assert isclose(1 - binary_h(0.25), 0.1887218755, abs_tol=1e-9)
    assert binary_h(0.5) == 1.0
    for stem in ("bernoulli-kl-direction", "binary-channel-information"):
        still = ET.parse(ASSETS / f"{stem}-still.svg").getroot()
        assert not any(n.tag == NS + "animate" for n in still.iter())
        for page in (PAGES / "index.md", PAGES / "index.zh-TW.md"):
            body = page.read_text(encoding="utf-8")
            for suffix in ("still", "motion"):
                assert f"{stem}-{suffix}.svg" in body, (page, stem, suffix)
            assert "CC BY-SA 4.0" in body
    print("Information motion numerical traces, bilingual links, and static fallbacks: PASS")


if __name__ == "__main__":
    run()
