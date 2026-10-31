"""Regression checks for learning-rate teaching animation semantics.

Run: python scripts/test_learning_rate_motion_semantics.py
These structural/numerical checks do NOT replace browser rendering QA.
"""
from __future__ import annotations

import math
import re
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1] / "docs/assets/concept-animations"
NS = {"svg": "http://www.w3.org/2000/svg"}


def read(name: str):
    root = ET.parse(ROOT / name).getroot()
    marker = root.find(".//svg:circle", NS)
    assert marker is not None, name
    anim = {a.attrib["attributeName"]: a for a in marker.findall("svg:animate", NS)}
    assert set(anim) == {"cx", "cy"}, (name, anim.keys())
    result = {}
    for axis in ("cx", "cy"):
        a = anim[axis]
        times = [float(x) for x in a.attrib["keyTimes"].split(";")]
        values = [float(x) for x in a.attrib["values"].split(";")]
        assert len(times) == len(values) and len(times) > 50
        assert abs(times[0]) < 1e-8 and abs(times[-1] - 1) < 1e-8
        assert all(b > a for a, b in zip(times, times[1:])), name
        assert a.attrib["calcMode"] == "linear"
        assert a.attrib["repeatCount"] == "indefinite"
        result[axis] = (times, values)
    tx, xs = result["cx"]
    ty, ys = result["cy"]
    assert tx == ty, name
    # A shared clock is essential: equal horizontal distances must consume equal time.
    assert all(math.isfinite(v) for v in (*tx, *xs, *ys)), name
    assert all(b >= a for a, b in zip(xs, xs[1:])), name
    assert all(0 <= t <= 1 for t in tx), name
    assert anim["cx"].attrib["dur"] == anim["cy"].attrib["dur"], name
    assert all(anim[axis].attrib.get("begin", "0s") == "0s" for axis in ("cx", "cy")), name
    assert all(abs(x - (64 + 510*t)) < 0.012 for x, t in zip(xs, tx)), name
    return tx, xs, ys


def sgdr():
    times, xs, ys = read("sgdr-restart-motion.svg")
    assert len(times) == 145
    for boundary in (1/7, 3/7):
        nearby = [i for i, t in enumerate(times) if abs(t-boundary) < 0.000005]
        assert len(nearby) >= 3, (boundary, nearby)
        # Immediately before restart: low LR (larger y); after: high LR (smaller y).
        assert ys[nearby[0]] > 220 and ys[nearby[-1]] < 100
    # Restart boundaries are nearly instantaneous relative to the full cycle.
    for boundary in (1/7, 3/7):
        nearby = [i for i, t in enumerate(times) if abs(t-boundary) < 0.000005]
        assert times[nearby[-1]] - times[nearby[0]] < 0.00001
        assert abs(xs[nearby[-1]] - xs[nearby[0]]) < 0.01
    for t, y in zip(times, ys):
        if any(abs(t-b) < 0.000005 for b in (1/7, 3/7)):
            continue
        phase = t*7 if t < 1/7 else (t*7-1)/2 if t < 3/7 else (t*7-3)/4
        expected = 159 - 71.4*math.cos(math.pi*phase)
        assert abs(y-expected) < 0.08, (t, y, expected)


def triangular2():
    times, xs, ys = read("clr-triangular2-motion.svg")
    assert len(times) == 121
    # Exactly three equal-duration cycles, with no phantom fourth-cycle peak.
    assert all(abs(times[k*40] - k/3) < 1e-5 for k in range(4))
    assert abs(ys[0] - ys[-1]) < 0.03
    for cycle in range(3):
        start, peak, end = cycle*40, cycle*40+20, (cycle+1)*40
        assert abs(ys[start]-223.6) < 0.03
        assert abs(ys[end]-223.6) < 0.03
        assert abs(ys[peak]-(223.6-129.2/2**cycle)) < 0.03
        for j in range(start, end+1):
            phase = (j-start)/40
            expected = 223.6 - (129.2/2**cycle)*(1-abs(2*phase-1))
            assert abs(ys[j]-expected) < 0.035, (j, ys[j], expected)



def svg_asset_safety():
    """Reject unsafe dependencies and malformed responsive SVG metadata."""
    for prefix in ("sgdr-restart", "clr-triangular2"):
        for variant in ("motion", "still"):
            name = f"{prefix}-{variant}.svg"
            asset = ROOT / name
            raw = asset.read_text(encoding="utf-8")
            # ElementTree accepts internal DTD entities; instructional SVGs need no DTD.
            assert "<!DOCTYPE" not in raw.upper() and "<!ENTITY" not in raw.upper(), name
            root = ET.fromstring(raw)
            assert root.tag == "{http://www.w3.org/2000/svg}svg", name
            assert root.attrib.get("viewBox") == "0 0 640 300", name
            assert root.attrib.get("role") == "img", name
            ids = {node.attrib["id"] for node in root.iter() if "id" in node.attrib}
            labelled = root.attrib.get("aria-labelledby", "").split()
            assert len(labelled) == 2 and all(ref in ids for ref in labelled), name
            assert root.find("svg:title", NS) is not None, name
            assert root.find("svg:desc", NS) is not None, name
            for node in root.iter():
                tag = node.tag.rsplit("}", 1)[-1].lower()
                assert tag not in {"script", "foreignobject", "image", "iframe"}, (name, tag)
                for key, value in node.attrib.items():
                    local_key = key.rsplit("}", 1)[-1].lower()
                    assert not local_key.startswith("on"), (name, key)
                    if local_key in {"href", "src"}:
                        assert value.startswith("#"), (name, key, value)
                    assert "url(http" not in value.lower(), (name, key)
            assert "http://" not in raw.replace('xmlns="http://www.w3.org/2000/svg"', ""), name
            assert "https://" not in raw, name


def fallback_geometry_parity():
    """GitHub fallback must show the same curve as the animated teaching asset.

    This guards against edits that update only one variant. It is a source-level
    consistency check, not a substitute for rendering both variants.
    """
    for prefix in ("sgdr-restart", "clr-triangular2"):
        motion = ET.parse(ROOT / f"{prefix}-motion.svg").getroot()
        still = ET.parse(ROOT / f"{prefix}-still.svg").getroot()
        def curves(root):
            return [
                (node.attrib.get("d"), node.attrib.get("stroke"),
                 node.attrib.get("stroke-width"))
                for node in root.findall(".//svg:path", NS)
                if node.attrib.get("fill") == "none"
            ]
        motion_curves, still_curves = curves(motion), curves(still)
        assert motion_curves, f"{prefix}: missing schedule curve"
        assert motion_curves == still_curves, (
            f"{prefix}: animated and GitHub fallback schedule geometry diverged"
        )
        for attribute in ("viewBox", "role", "aria-labelledby"):
            assert motion.attrib.get(attribute) == still.attrib.get(attribute), (
                prefix, attribute
            )
        for tag in ("title", "desc"):
            a, b = motion.find(f"svg:{tag}", NS), still.find(f"svg:{tag}", NS)
            assert a is not None and b is not None and a.text == b.text, (
                prefix, tag
            )


def bilingual_fallbacks():
    """Ensure each schedule has a static GitHub preview and a shared bilingual embed."""
    pairs = (
        ("sgdr-restart", "cosine-annealing-warm-restarts"),
        ("clr-triangular2", "cyclical-learning-rates"),
    )
    docs = ROOT.parents[1]
    for asset, chapter in pairs:
        motion = ROOT / (asset + "-motion.svg")
        still = ROOT / (asset + "-still.svg")
        assert motion.is_file() and still.is_file(), asset
        still_root = ET.parse(still).getroot()
        assert still_root.tag == "{http://www.w3.org/2000/svg}svg", asset
        assert still_root.find("svg:title", NS) is not None, asset
        assert not any(node.tag.rsplit("}", 1)[-1] in
                       {"animate", "animateMotion", "animateTransform", "script"}
                       for node in still_root.iter()), asset
        for suffix in (".md", ".zh-TW.md"):
            page = docs / "theory" / "optimization" / (chapter + suffix)
            content = page.read_text(encoding="utf-8")
            assert asset + "-still.svg" in content, str(page)
            assert asset + "-motion.svg" in content, str(page)
            assert "data-motion-src" in content, str(page)
            assert "concept-animations/" in content, str(page)




def marker_follows_visible_curve():
    """Verify the moving marker stays on the rendered schedule, not just its clock.

    The visible trace consists of M/L SVG path segments. Compute geometric
    point-to-segment distance at every animated sample, including restart jumps.
    This catches marker/curve drift even when the fallback geometry matches.
    It remains a numerical test, not a browser screenshot or playback test.
    """
    for prefix in ("sgdr-restart", "clr-triangular2"):
        root = ET.parse(ROOT / f"{prefix}-motion.svg").getroot()
        paths = [p for p in root.findall(".//svg:path", NS)
                 if p.attrib.get("fill") == "none"]
        assert len(paths) == 1, (prefix, "expected one visible schedule trace")
        d = paths[0].attrib["d"]
        # Only the explicitly supported absolute M/L geometry is accepted.
        commands = re.findall(r"[A-Za-z]", d)
        assert commands and commands[0] == "M" and set(commands) <= {"M", "L"}, prefix
        numbers = [float(n) for n in re.findall(
            r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?", d)]
        assert len(numbers) >= 4 and len(numbers) % 2 == 0, prefix
        points = list(zip(numbers[::2], numbers[1::2]))
        assert all(math.isfinite(v) for p in points for v in p), prefix
        _, xs, ys = read(f"{prefix}-motion.svg")
        for i, (x, y) in enumerate(zip(xs, ys)):
            distance_sq = float("inf")
            for (ax, ay), (bx, by) in zip(points, points[1:]):
                dx, dy = bx-ax, by-ay
                length_sq = dx*dx + dy*dy
                u = max(0.0, min(1.0, ((x-ax)*dx + (y-ay)*dy)/length_sq)) if length_sq else 0.0
                distance_sq = min(distance_sq,
                    (x-ax-u*dx)**2 + (y-ay-u*dy)**2)
            assert distance_sq < 2.25, (prefix, i, x, y, math.sqrt(distance_sq))

if __name__ == "__main__":
    sgdr()
    triangular2()
    bilingual_fallbacks()
    svg_asset_safety()
    fallback_geometry_parity()
    marker_follows_visible_curve()
    print("Learning-rate animation numerical and timeline semantics: PASS")
