#!/usr/bin/env python3
"""Check SVD/power-iteration values and timelines independently of rendering.

Run: python scripts/test_linear_algebra_motion_semantics.py
Standard library only. These source checks do not replace browser visual QA.
"""
from __future__ import annotations

from html.parser import HTMLParser
import math
from pathlib import Path
from types import SimpleNamespace
import sys
import unittest
from urllib.parse import urljoin, urlsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs/assets/concept-animations"
NS = {"s": "http://www.w3.org/2000/svg"}
sys.path.insert(0, str(ROOT / "hooks"))
from source_asset_urls import on_page_content


def svg(stem, kind="motion"):
    return ET.parse(ASSETS / f"{stem}-{kind}.svg").getroot()


def by_id(root, name):
    return next(element for element in root.iter() if element.get("id") == name)


def motion(element, attribute):
    return next(a for a in element.findall("s:animate", NS)
                if a.get("attributeName") == attribute)


def numbers(value):
    return [float(v) for v in value.replace(",", " ").split()]


def sample(animation, seconds):
    duration = float(animation.get("dur").removesuffix("s"))
    time = min(max(seconds / duration, 0), 1)
    keys = [float(k) for k in animation.get("keyTimes").split(";")]
    values = [numbers(v) for v in animation.get("values").split(";")]
    if time >= 1:
        return values[-1]
    i = max(i for i, key in enumerate(keys) if key <= time)
    if animation.get("calcMode") == "discrete":
        return values[i]
    weight = (time - keys[i]) / (keys[i + 1] - keys[i])
    return [a + weight * (b - a) for a, b in zip(values[i], values[i + 1])]


def rotation(degrees):
    angle = math.radians(degrees)
    c, s = math.cos(angle), math.sin(angle)
    return ((c, -s), (s, c))


def multiply(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(2))
                       for j in range(2)) for i in range(2))


def matvec(a, x):
    return tuple(sum(a[i][j] * x[j] for j in range(2)) for i in range(2))


def transpose(a):
    return tuple(zip(*a))


def expected_iterates():
    q = rotation(25)
    a = multiply(multiply(q, ((3, 0), (0, 1))), transpose(q))
    x = (math.cos(math.radians(97)), math.sin(math.radians(97)))
    normalized, applied = [x], []
    for _ in range(5):
        raw = matvec(a, x)
        applied.append(raw)
        x = tuple(v / math.hypot(*raw) for v in raw)
        normalized.append(x)
    return normalized, applied


class LinearAlgebraMotionTests(unittest.TestCase):
    def assertVectorClose(self, actual, expected, tolerance=1e-5):
        self.assertEqual(len(actual), len(expected))
        for a, b in zip(actual, expected):
            self.assertAlmostEqual(a, b, delta=tolerance)

    def test_all_timelines_are_well_formed_and_share_twelve_seconds(self):
        for stem in ("svd-unit-circle", "power-iteration-convergence"):
            root = svg(stem)
            animations = [e for e in root.iter()
                          if e.tag.rsplit("}", 1)[-1] in ("animate", "animateTransform")]
            self.assertTrue(animations)
            for a in animations:
                self.assertEqual(a.get("dur"), "12s")
                self.assertEqual(a.get("repeatCount"), "indefinite")
                keys = [float(v) for v in a.get("keyTimes").split(";")]
                values = a.get("values").split(";")
                self.assertEqual(len(keys), len(values))
                self.assertEqual((keys[0], keys[-1]), (0, 1))
                self.assertTrue(all(a < b for a, b in zip(keys, keys[1:])))
                self.assertEqual(len({len(numbers(v)) for v in values}), 1)

    def test_power_apply_and_normalize_endpoints(self):
        root = svg("power-iteration-convergence")
        vector = by_id(root, "power-vector")
        xs, ys = motion(vector, "x2"), motion(vector, "y2")
        self.assertEqual(xs.get("keyTimes"), ys.get("keyTimes"))
        normalized, applied = expected_iterates()
        self.assertVectorClose(((float(vector.get("x2")) - 180) / 54,
                                (195 - float(vector.get("y2"))) / 54), normalized[0])
        times = [0]
        expected = [normalized[0]]
        for k in range(5):
            times.extend((.6 + 2 * k, 1.2 + 2 * k, 1.8 + 2 * k))
            expected.extend((normalized[k], applied[k], normalized[k + 1]))
        times.append(12)
        expected.append(normalized[5])
        self.assertVectorClose([float(k) * 12 for k in xs.get("keyTimes").split(";")], times)
        for t, value in zip(times, expected):
            x, y = sample(xs, t)[0], sample(ys, t)[0]
            self.assertVectorClose(((x - 180) / 54, (195 - y) / 54), value)
        self.assertEqual(len(expected), 17, "Exactly five updates, followed by the final hold")

    def test_power_highlight_and_phase_labels_match_every_sample(self):
        root = svg("power-iteration-convergence")
        vector, row = by_id(root, "power-vector"), by_id(root, "active-error-row")
        for tick in range(1200):
            t = (tick + .5) / 100
            phases = {name: sample(motion(by_id(root, "phase-" + name), "opacity"), t)[0]
                      for name in ("normalized", "apply", "normalize")}
            self.assertEqual(sum(phases.values()), 1)
            opacity = sample(motion(row, "opacity"), t)[0]
            self.assertEqual(opacity, phases["normalized"])
            if not opacity:
                continue
            k = round((sample(motion(row, "y"), t)[0] - 87) / 36)
            x = (sample(motion(vector, "x2"), t)[0] - 180) / 54
            y = (195 - sample(motion(vector, "y2"), t)[0]) / 54
            self.assertVectorClose((x, y), expected_iterates()[0][k])
            self.assertAlmostEqual(math.hypot(x, y), 1, delta=1e-6)
            angle = math.degrees(math.atan2(y, x)) - 25
            self.assertEqual(by_id(root, f"error-label-{k}").text, f"{angle:.1f}°")
        for k in range(5):
            for name, time in (("apply", .9 + 2 * k), ("normalize", 1.5 + 2 * k)):
                self.assertEqual(sample(motion(by_id(root, "phase-" + name), "opacity"), time), [1])
                self.assertEqual(sample(motion(row, "opacity"), time), [0])

    def test_power_bar_lengths_labels_and_static_iterates(self):
        expected, _ = expected_iterates()
        for kind in ("motion", "still"):
            root = svg("power-iteration-convergence", kind)
            for k, point in enumerate(expected):
                error = math.degrees(math.atan(math.tan(math.radians(72)) / 3 ** k))
                self.assertEqual(by_id(root, f"error-label-{k}").text, f"{error:.1f}°")
                self.assertAlmostEqual(float(by_id(root, f"error-bar-{k}").get("width")),
                                       136 * error / 72, places=7)
                dot = by_id(root, f"iterate-{k}")
                self.assertVectorClose((float(dot.get("cx")), float(dot.get("cy"))),
                                       (180 + 54 * point[0], 195 - 54 * point[1]), .01)

    def test_power_final_hold_reduced_motion_and_still_match(self):
        root = svg("power-iteration-convergence")
        arrow = by_id(root, "power-vector")
        expected = [sample(motion(arrow, axis), 11.9)[0] for axis in ("x2", "y2")]
        for kind in ("motion", "still"):
            final = by_id(svg("power-iteration-convergence", kind), "power-final-vector")
            self.assertVectorClose([float(final.get(axis)) for axis in ("x2", "y2")], expected)
        row = by_id(root, "active-error-row")
        self.assertEqual(sample(motion(row, "y"), 11.9), [267])
        self.assertEqual(sample(motion(row, "opacity"), 11.9), [1])

    def svd_transforms(self):
        root = svg("svd-unit-circle")
        origin = root.find("s:g[@class='animated']", NS)
        self.assertEqual(origin.get("transform"), "translate(466 170)")
        u = origin.find("s:g", NS)
        sigma = u.find("s:g", NS)
        vt = sigma.find("s:g", NS)
        self.assertIsNotNone(vt.find("s:circle", NS))
        transforms = [g.find("s:animateTransform", NS) for g in (u, sigma, vt)]
        self.assertEqual([a.get("type") for a in transforms], ["rotate", "scale", "rotate"])
        return transforms

    def test_svd_transform_order_orthogonality_and_singular_values(self):
        u_anim, sigma_anim, vt_anim = self.svd_transforms()
        self.assertEqual(sample(u_anim, 11.9), [-30])
        self.assertEqual(sample(sigma_anim, 11.9), [2, .65])
        self.assertEqual(sample(vt_anim, 11.9), [35])
        for matrix in (rotation(30), rotation(35)):
            gram = multiply(transpose(matrix), matrix)
            self.assertVectorClose(gram[0], (1, 0))
            self.assertVectorClose(gram[1], (0, 1))
        # SVG has downward-positive y, so J A J must equal its transform product.
        j = ((1, 0), (0, -1))
        a = multiply(multiply(rotation(30), ((2, 0), (0, .65))), rotation(-35))
        screen = multiply(multiply(rotation(-30), ((2, 0), (0, .65))), rotation(35))
        expected = multiply(multiply(j, a), j)
        for row, other in zip(screen, expected):
            self.assertVectorClose(row, other)
        gram = multiply(transpose(a), a)
        trace, determinant = sum(gram[i][i] for i in range(2)), gram[0][0] * gram[1][1] - gram[0][1] * gram[1][0]
        self.assertAlmostEqual(trace, 2 ** 2 + .65 ** 2)
        self.assertAlmostEqual(determinant, (2 * .65) ** 2)
        ellipse = svg("svd-unit-circle").find(".//s:ellipse", NS)
        self.assertVectorClose((float(ellipse.get("rx")), float(ellipse.get("ry"))), (108, 35.1))

    def test_svd_operations_happen_sequentially(self):
        u, sigma, vt = self.svd_transforms()
        for tick in range(1200):
            t = tick / 100
            ur, scale, vr = sample(u, t), sample(sigma, t), sample(vt, t)
            if scale != [1, 1]:
                self.assertEqual(vr, [35], "V-transpose rotation finishes before scaling")
            if ur != [0]:
                self.assertEqual(scale, [2, .65], "Scaling finishes before U rotation")
        for t, expected in ((0, ([0], [1, 1], [0])), (3, ([0], [1, 1], [35])),
                            (6, ([0], [2, .65], [35])), (11, ([-30], [2, .65], [35]))):
            self.assertEqual(tuple(sample(a, t) for a in (u, sigma, vt)), expected)

    def test_svd_reduced_and_still_geometry_match_the_motion_endpoint(self):
        motion_root, still = svg("svd-unit-circle"), svg("svd-unit-circle", "still")
        reduced = motion_root.find("s:g[@class='reduced']/s:g", NS)
        still_group = next(g for g in still.findall("s:g", NS)
                           if g.get("transform") == "translate(466 170)")
        self.assertEqual(ET.tostring(reduced), ET.tostring(still_group))
        transforms = [g.get("transform") for g in reduced.iter() if g.tag.endswith("}g")]
        self.assertEqual(transforms, ["translate(466 170)", "rotate(-30)", "scale(2 .65)", "rotate(35)"])

    def test_static_and_reduced_motion_safety(self):
        for stem in ("power-iteration-convergence", "svd-unit-circle"):
            self.assertFalse([e for e in svg(stem, "still").iter()
                              if e.tag.rsplit("}", 1)[-1].startswith("animate")])
            root = svg(stem)
            style = root.find("s:style", NS).text
            self.assertIn("prefers-reduced-motion:reduce", style)
            self.assertIn(".animated{display:none!important}", style)
            self.assertIn(".reduced{display:inline!important}", style)
            self.assertEqual(root.find("s:g[@class='reduced']", NS).get("display"), "none")

    def test_bilingual_embeds_keep_source_and_built_urls_valid(self):
        class Images(HTMLParser):
            def __init__(self, html):
                super().__init__()
                self.images = []
                self.feed(html)

            def handle_starttag(self, tag, attrs):
                if tag == "img":
                    self.images.append(dict(attrs))

        class Files:
            def get_file_from_path(self, path):
                return SimpleNamespace(url=path) if (ROOT / "docs" / path).is_file() else None

        for topic, stem in (("svd", "svd-unit-circle"), ("eigendecomposition", "power-iteration-convergence")):
            for suffix, prefix in (("", ""), (".zh-TW", "zh-TW/")):
                source = Path(f"theory/math/linear-algebra/{topic}{suffix}.md")
                text = (ROOT / "docs" / source).read_text()
                attrs = next(a for a in Images(text).images if stem in a.get("src", ""))
                self.assertIn("data-source-asset-urls", attrs)
                for attribute in ("src", "data-motion-src", "data-still-src"):
                    self.assertTrue((ROOT / "docs" / source.parent / attrs[attribute]).is_file())
                page = SimpleNamespace(file=SimpleNamespace(src_uri=source.as_posix()),
                                       url=f"{prefix}theory/math/linear-algebra/{topic}/")
                built = next(a for a in Images(on_page_content(text, page, {}, Files())).images
                             if stem in a.get("src", ""))
                self.assertNotIn("data-source-asset-urls", built)
                for attribute in ("src", "data-motion-src", "data-still-src"):
                    value = urljoin("https://example.test/ai-wiki/" + page.url, built[attribute])
                    expected = f"/ai-wiki/assets/concept-animations/{stem}-{'motion' if attribute == 'data-motion-src' else 'still'}.svg"
                    self.assertEqual(urlsplit(value).path, expected)


if __name__ == "__main__":
    unittest.main()
