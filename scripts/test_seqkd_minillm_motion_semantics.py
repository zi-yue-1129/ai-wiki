"""Check the toy sequence search and on-policy score shown in the motion assets."""
import math
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET

ASSETS = Path(__file__).resolve().parents[1] / "docs/assets/concept-animations"
NS = "{http://www.w3.org/2000/svg}"


def labels(stem):
    return {node.text for node in ET.parse(ASSETS / f"{stem}-still.svg").iter(NS + "text")}


class SequenceMotion(unittest.TestCase):
    def test_beam_mode(self):
        probs = {"AX": .6 * .55, "AY": .6 * .45, "BX": .4 * .9, "BY": .4 * .1}
        self.assertAlmostEqual(sum(probs.values()), 1)
        self.assertEqual(max(probs, key=probs.get), "BX")
        self.assertGreater(probs["BX"], probs["AX"])
        self.assertTrue({f"{p:.2f}" for p in probs.values()} <= labels("seqkd-beam-mode"))
        self.assertIn("B X", labels("seqkd-beam-mode"))

    def test_on_policy_score(self):
        p, q = [.45, .45, .1], [.3, .2, .5]
        self.assertLessEqual(sum(q[:2]), .72)
        self.assertLess(.72, sum(q))
        reward = math.log(p[2] / q[2])
        kl = sum(b * math.log(b / a) for a, b in zip(p, q))
        self.assertAlmostEqual(kl, .520893380541335)
        self.assertIn(f"{reward:.3f}".replace("-", "−"), labels("minillm-on-policy-score"))
        self.assertIn(f"{kl:.3f}", labels("minillm-on-policy-score"))


if __name__ == "__main__":
    unittest.main()
