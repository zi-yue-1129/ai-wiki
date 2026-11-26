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


    def test_signed_kl_terms_and_sequence_logit_gradient(self):
        p, q = [.45, .45, .1], [.3, .2, .5]
        terms = [b * math.log(b / a) for a, b in zip(p, q)]
        kl = sum(terms)
        gradient = [b * (math.log(b / a) - kl) for a, b in zip(p, q)]
        self.assertAlmostEqual(sum(gradient), 0)
        self.assertGreater(gradient[2], 0)
        self.assertTrue(all(g < 0 for g in gradient[:2]))
        self.assertTrue({f"{t:+.3f}".replace("-", "−") for t in terms}
                        <= labels("minillm-on-policy-score"))
        def objective(z):
            v = [math.exp(x) for x in z]
            qz = [x / sum(v) for x in v]
            return sum(b * math.log(b / a) for a, b in zip(p, qz))
        z = [math.log(b) for b in q]
        eps = 1e-5
        for i, g in enumerate(gradient):
            plus, minus = z[:], z[:]
            plus[i] += eps
            minus[i] -= eps
            self.assertAlmostEqual((objective(plus) - objective(minus)) / (2 * eps), g, places=7)

    def test_hard_target_gradient_counterexample(self):
        teacher = [.33, .27, .36, .04]
        student = [.25] * 4
        hard = [0, 0, 1, 0]
        loss = lambda target: -sum(t * math.log(s) for t, s in zip(target, student))
        self.assertAlmostEqual(loss(teacher), loss(hard))
        soft_grad = [s - t for s, t in zip(student, teacher)]
        hard_grad = [s - t for s, t in zip(student, hard)]
        self.assertLess(soft_grad[0], 0)
        self.assertGreater(hard_grad[0], 0)


if __name__ == "__main__":
    unittest.main()
