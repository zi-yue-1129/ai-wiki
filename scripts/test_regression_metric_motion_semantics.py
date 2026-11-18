#!/usr/bin/env python3
"""Check regression-metric SVG formulas and timelines with the standard library.

Run: python scripts/test_regression_metric_motion_semantics.py
These source/numerical checks complement, rather than replace, browser QA.
"""
from bisect import bisect_right
from copy import deepcopy
import math
import unittest
from xml.etree import ElementTree as ET

from verify_concept_motion import ASSETS, DOCS, verify_source_pair

NS = "{http://www.w3.org/2000/svg}"
OUTLIER = "outlier-mae-rmse"
R2 = "r2-mean-baseline"


def svg(stem, kind="motion"):
    return ET.parse(ASSETS / f"{stem}-{kind}.svg").getroot()


def element(root, tag, **attributes):
    matches = [node for node in root.findall(NS + tag)
               if all(node.get(key) == value for key, value in attributes.items())]
    if len(matches) != 1:
        raise AssertionError((tag, attributes, len(matches)))
    return matches[0]


def animation(node, attribute):
    return next(a for a in node.findall(NS + "animate")
                if a.get("attributeName") == attribute)


def numbers(value):
    return [float(part) for part in value.split(";")]


def sample(node, attribute, phase):
    """Evaluate the actual SMIL linear interpolation, not an idealized curve."""
    a = animation(node, attribute)
    times, values = numbers(a.get("keyTimes")), numbers(a.get("values"))
    if phase >= times[-1]:
        return values[-1]
    index = max(0, bisect_right(times, phase) - 1)
    fraction = (phase - times[index]) / (times[index + 1] - times[index])
    return values[index] + fraction * (values[index + 1] - values[index])


def outlier_nodes(root):
    return (element(root, "rect", x="512"),
            element(root, "rect", x="149", fill="#158D91"),
            element(root, "rect", x="149", fill="#B76A24"))


def r2_nodes(root):
    truth = [element(root, "circle", cx=str(x), r="7")
             for x in (91, 168, 245, 322)]
    predictions = [element(root, "circle", cx=str(x), r="5.7")
                   for x in (91, 168, 245, 322)]
    residuals = [element(root, "line", x1=str(x), x2=str(x))
                 for x in (91, 168, 245, 322)]
    rss = element(root, "rect", x="416", fill="#E38A57")
    score = element(root, "circle", r="10")
    return truth, predictions, residuals, rss, score


def expected_k(phase):
    if phase <= 0.35:
        return (1 + math.cos(math.pi * phase / 0.35)) / 2
    if phase <= 0.7:
        return 0.75 * (1 - math.cos(math.pi * (phase - 0.35) / 0.35))
    return 1.25 + 0.25 * math.cos(math.pi * (phase - 0.7) / 0.3)


class RegressionMetricMotionTests(unittest.TestCase):
    def test_timelines_are_synchronized_closed_twelve_second_loops(self):
        for stem, count in ((OUTLIER, 4), (R2, 10)):
            root = svg(stem)
            self.assertEqual(len(list(root.iter(NS + "animate"))), count)
            for node in root.iter():
                for a in node.findall(NS + "animate"):
                    with self.subTest(stem=stem, attribute=a.get("attributeName")):
                        self.assertEqual(a.get("dur"), "12s")
                        self.assertEqual(a.get("begin", "0s"), "0s")
                        self.assertEqual(a.get("calcMode"), "linear")
                        self.assertEqual(a.get("repeatCount"), "indefinite")
                        values = numbers(a.get("values"))
                        self.assertEqual(numbers(a.get("keyTimes")),
                                         [i / 40 for i in range(41)])
                        self.assertEqual(len(values), 41)
                        self.assertTrue(all(math.isfinite(v) for v in values))
                        self.assertEqual(values[0], values[-1])
                        self.assertEqual(float(node.get(a.get("attributeName"))), values[0])

    def test_outlier_keyframes_encode_mae_and_rmse_on_one_scale(self):
        root = svg(OUTLIER)
        outlier, mae, rmse = outlier_nodes(root)
        for x in (84, 191, 298, 405):
            bar = element(root, "rect", x=str(x))
            self.assertEqual(float(bar.get("height")), 24)
            self.assertEqual(float(bar.get("y")), 173)
            self.assertFalse(bar.findall(NS + "animate"))
        for i in range(41):
            phase = i / 40
            d = 1 + 2.5 * (1 - math.cos(2 * math.pi * phase))
            with self.subTest(frame=i):
                self.assertAlmostEqual(sample(outlier, "height", phase), 24 * d, delta=0.00051)
                self.assertAlmostEqual(sample(outlier, "y", phase), 197 - 24 * d, delta=0.00051)
                self.assertAlmostEqual(sample(mae, "width", phase), 100 * (4 + d) / 5, delta=0.00051)
                self.assertAlmostEqual(sample(rmse, "width", phase),
                                       100 * math.sqrt((4 + d * d) / 5), delta=0.00051)
        labels = [node.text for node in root.findall(NS + "text")]
        for label in ("PEAK", "2.00", "2.83"):
            self.assertIn(label, labels)

    def test_r2_keyframes_encode_predictions_residuals_and_score(self):
        root = svg(R2)
        truth, predictions, residuals, rss, score = r2_nodes(root)
        tss = sum((y - 2.5) ** 2 for y in (1, 2, 3, 4))
        self.assertEqual(tss, 5)
        self.assertEqual(float(element(root, "rect", x="416", fill="#1F708E").get("width")), 14 * tss)
        self.assertIn("5.0", [node.text for node in root.findall(NS + "text")])
        for i in range(41):
            phase, k = i / 40, expected_k(i / 40)
            with self.subTest(frame=i):
                for y, target, prediction, residual in zip((1, 2, 3, 4), truth, predictions, residuals):
                    target_y = 264 - 38 * y
                    predicted_y = 264 - 38 * (y + k * (2.5 - y))
                    self.assertEqual(float(target.get("cy")), target_y)
                    self.assertEqual(float(residual.get("y1")), target_y)
                    self.assertAlmostEqual(sample(prediction, "cy", phase), predicted_y, delta=0.00051)
                    self.assertAlmostEqual(sample(residual, "y2", phase), predicted_y, delta=0.00051)
                self.assertAlmostEqual(sample(rss, "width", phase), 14 * tss * k * k, delta=0.00051)
                self.assertAlmostEqual(sample(score, "cx", phase),
                                       396.4 + 173.6 * (1 - k * k), delta=0.00051)

    def test_between_keyframes_preserve_the_numerical_teaching_relationships(self):
        outlier, mae, rmse = outlier_nodes(svg(OUTLIER))
        truth, predictions, residuals, rss, score = r2_nodes(svg(R2))
        targets = [(264 - float(node.get("cy"))) / 38 for node in truth]
        for i in range(40):
            for fraction in (0.25, 0.5, 0.75):
                phase = (i + fraction) / 40
                with self.subTest(interval=i, fraction=fraction):
                    height = sample(outlier, "height", phase)
                    d = height / 24
                    self.assertAlmostEqual(height + sample(outlier, "y", phase), 197)
                    self.assertAlmostEqual(sample(mae, "width", phase) / 100, (4 + d) / 5, delta=0.00001)
                    # Piecewise-linear interpolation of the nonlinear RMSE
                    # curve differs from the exact formula by < 0.001 units.
                    self.assertAlmostEqual(sample(rmse, "width", phase) / 100,
                                           math.sqrt((4 + d * d) / 5), delta=0.001)
                    self.assertGreaterEqual(sample(rmse, "width", phase), sample(mae, "width", phase))
                    predicted = [(264 - sample(node, "cy", phase)) / 38 for node in predictions]
                    exact_rss = sum((a - b) ** 2 for a, b in zip(predicted, targets))
                    drawn_rss = sample(rss, "width", phase) / 14
                    drawn_r2 = (sample(score, "cx", phase) - 396.4) / 173.6
                    self.assertAlmostEqual(drawn_r2, 1 - drawn_rss / 5, delta=0.00002)
                    # Interpolated squared-error bars approximate the visible
                    # point errors; max R² discrepancy is < 0.0071 (1.24 px).
                    self.assertAlmostEqual(drawn_r2, 1 - exact_rss / 5, delta=0.0071)
                    for prediction, residual in zip(predictions, residuals):
                        self.assertEqual(sample(prediction, "cy", phase), sample(residual, "y2", phase))

    def test_static_fallbacks_match_the_explained_peak_frames(self):
        for stem, phase in ((OUTLIER, 0.5), (R2, 0.7)):
            peak = deepcopy(svg(stem))
            for node in peak.iter():
                for a in list(node):
                    if a.tag == NS + "animate":
                        attribute = a.get("attributeName")
                        node.set(attribute, str(sample(node, attribute, phase)))
                        node.remove(a)
            still = svg(stem, "still")
            self.assertFalse(list(still.iter(NS + "animate")))
            expected_nodes, actual_nodes = list(peak.iter()), list(still.iter())
            self.assertEqual(len(expected_nodes), len(actual_nodes))
            for expected, actual in zip(expected_nodes, actual_nodes):
                self.assertEqual(expected.tag, actual.tag)
                self.assertEqual(expected.text, actual.text)
                self.assertEqual(expected.attrib.keys(), actual.attrib.keys())
                for key, value in expected.attrib.items():
                    if value != actual.get(key):
                        self.assertAlmostEqual(float(value), float(actual.get(key)), delta=0.00051)

    def test_all_six_bilingual_pages_use_the_matching_source_asset_pair(self):
        for chapter, stem in (("mae", OUTLIER), ("rmse", OUTLIER), ("r-squared", R2)):
            for suffix in ("", ".zh-TW"):
                page = DOCS / f"theory/evaluation/metrics/regression/{chapter}{suffix}.md"
                content = page.read_text(encoding="utf-8")
                with self.subTest(page=page.name):
                    self.assertEqual(verify_source_pair(page, content, stem), [])


if __name__ == "__main__":
    unittest.main()
