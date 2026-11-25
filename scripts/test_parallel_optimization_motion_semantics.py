"""Numerical and route contracts for the two reviewed optimization SVGs."""
from pathlib import Path
from fractions import Fraction as Q
import unittest
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs/assets/concept-animations"
NS = "{http://www.w3.org/2000/svg}"

def root(stem, kind):
    return ET.parse(ASSETS / f"{stem}-{kind}.svg").getroot()

class ParallelOptimizationMotion(unittest.TestCase):
    def test_antithetic_signed_rewards_and_update(self):
        for kind in ("motion", "still"):
            r = root("es-antithetic-weighted-update", kind)
            source = r if kind == "still" else r
            text = {t.text for t in source.iter(NS + "text")}
            self.assertTrue({"+2", "−2", "+1", "−1", "(1, 0)", "½", "(1, ½)"}.issubset(text))
            paths = {p.get("d") for p in source.iter(NS + "path")}
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            self.assertTrue({"M168 182L246 182", "M168 182L90 182", "M168 182L168 104", "M168 182L168 260"}.issubset(paths))
            rewards = [2*x + y for x, y in directions]
            for offset in (0, 100):
                g = tuple(sum(Q((f + offset)*e[j], 4) for f, e in zip(rewards, directions)) for j in range(2))
                self.assertEqual(g, (Q(1), Q(1, 2)))
            self.assertTrue({"M392 240L532 240", "M532 240L532 170", "M392 240L532 170"}.issubset(paths))

    def test_layer_ownership_and_fanout(self):
        expected = {"M68 128V119H202V145H251", "M68 249V240H199V145H251",
                    "M132 165V177H220V267H251", "M132 286V297H220V267H251",
                    "M388 146H420V119H492V128", "M388 146H420V240H492V249",
                    "M388 267H438V177H556V165", "M388 267H438V297H556V286"}
        for kind in ("motion", "still"):
            r = root("distributed-kfac-layer-ownership", kind)
            paths = {p.get("d") for p in r.iter(NS + "path")}
            self.assertTrue(expected.issubset(paths))
            motion = [a.get("path") for a in r.iter(NS + "animateMotion")]
            self.assertEqual(set(motion), expected if kind == "motion" else set())
            self.assertEqual(len(motion), 8 if kind == "motion" else 0)
            # Averaging factors and inverting is not averaging local inverses.
            self.assertNotEqual(1 / ((Q(1) + Q(3)) / 2), (1 / Q(1) + 1 / Q(3)) / 2)

    def test_observation_weighted_reduction(self):
        # Scalar analogue of one factor; counts follow the statistic normalization.
        counts, means = (1, 3), (Q(1), Q(5))
        pooled = sum(n * a for n, a in zip(counts, means)) / sum(counts)
        worker_mean = sum(means) / len(means)
        self.assertEqual((pooled, worker_mean), (4, 3))
        self.assertEqual(Q(10) / (pooled + 1), 2)
        self.assertEqual(Q(10) / (worker_mean + 1), Q(5, 2))
        # Splitting a worker does not change the observation-weighted moment.
        self.assertEqual((means[0] + means[1] + 2 * means[1]) / 4, pooled)

if __name__ == "__main__":
    unittest.main()
