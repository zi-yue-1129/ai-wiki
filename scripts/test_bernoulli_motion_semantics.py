#!/usr/bin/env python3
"""Independent Bernoulli SVG numbers and source-URL regressions (stdlib only)."""
from copy import deepcopy
import re
import unittest
from xml.etree import ElementTree as ET

from verify_concept_motion import ASSETS, DOCS, verify_source_pair

NS = "{http://www.w3.org/2000/svg}"
OBSERVATIONS = (1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1)
TOPICS = {
    "mle-bernoulli-likelihood": ("maximum-likelihood", 0),
    "map-beta-posterior": ("maximum-a-posteriori", 2),
}


class BernoulliMotionTests(unittest.TestCase):
    def root(self, stem, kind="motion"):
        return ET.parse(ASSETS / f"{stem}-{kind}.svg").getroot()

    def test_all_twelve_curves_and_markers_match_observations(self):
        for stem, (_, prior_count) in TOPICS.items():
            root = self.root(stem)
            path = next(node for node in root.findall(NS + "path")
                        if node.find(NS + "animate") is not None)
            frames = path.find(NS + "animate").get("values").split(";")
            self.assertEqual(len(frames), 13)
            self.assertEqual(frames[0], frames[-1])
            for n, frame in enumerate(frames[:12], 1):
                with self.subTest(stem=stem, n=n):
                    successes = sum(OBSERVATIONS[:n])
                    a = successes + prior_count
                    b = n - successes + prior_count
                    points = [tuple(map(float, pair)) for pair in
                              re.findall(r"[ML]([\d.]+),([\d.]+)", frame)]
                    self.assertEqual(len(points), 41)
                    density = [(i / 40) ** a * (1 - i / 40) ** b
                               for i in range(41)]
                    peak = max(density)
                    for i, ((x, y), value) in enumerate(zip(points, density)):
                        self.assertAlmostEqual(x, 70 + 354 * i / 40, delta=0.051)
                        self.assertAlmostEqual(y, 267 - 140 * value / peak, delta=0.051)
                    for marker in root.findall(NS + "line"):
                        animations = marker.findall(NS + "animate")
                        if not animations:
                            continue
                        probability = (successes / n if marker.get("stroke") == "#d97706"
                                       else a / (a + b))
                        for animation in animations:
                            position = float(animation.get("values").split(";")[n - 1])
                            self.assertAlmostEqual(position, 70 + 354 * probability, delta=0.051)

    def test_timeline_uses_discrete_synchronized_twelve_second_steps(self):
        for stem in TOPICS:
            for animation in self.root(stem).iter(NS + "animate"):
                self.assertEqual(animation.get("dur"), "12s")
                self.assertEqual(animation.get("calcMode"), "discrete")
                self.assertEqual(animation.get("repeatCount"), "indefinite")
                self.assertEqual(len(animation.get("values").split(";")), 13)
                times = list(map(float, animation.get("keyTimes").split(";")))
                self.assertEqual(len(times), 13)
                for n, time in enumerate(times):
                    self.assertAlmostEqual(time, n / 12, delta=0.000001)

    def test_static_fallbacks_are_exact_final_frames(self):
        for stem in TOPICS:
            final = deepcopy(self.root(stem))
            for node in final.iter():
                for animation in list(node):
                    if animation.tag == NS + "animate":
                        node.set(animation.get("attributeName"),
                                 animation.get("values").split(";")[11])
                        node.remove(animation)
            self.assertEqual(ET.tostring(final), ET.tostring(self.root(stem, "still")))

    def test_bilingual_source_pairs_use_opt_in_source_paths(self):
        for stem, (topic, _) in TOPICS.items():
            for suffix in ("", ".zh-TW"):
                page = DOCS / f"theory/math/probability-statistics/{topic}{suffix}.md"
                text = page.read_text(encoding="utf-8")
                self.assertEqual(verify_source_pair(page, text, stem), [])
                # The original PR's four-parent data attributes must fail.
                broken = text.replace('data-motion-src="../../../assets/',
                                      'data-motion-src="../../../../assets/')
                self.assertTrue(verify_source_pair(page, broken, stem))
                self.assertTrue(verify_source_pair(page,
                                text.replace("data-source-asset-urls", ""), stem))


if __name__ == "__main__":
    unittest.main()
