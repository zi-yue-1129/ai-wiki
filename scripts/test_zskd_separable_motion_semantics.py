import math
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET

ASSETS = Path(__file__).resolve().parents[1] / "docs/assets/concept-animations"
NS = "{http://www.w3.org/2000/svg}"

class CompressionMotionSemantics(unittest.TestCase):
    def labels(self, stem):
        return [e.text for e in ET.parse(ASSETS / (stem + "-still.svg")).iter(NS + "text")]

    def test_frozen_teacher_input_steps(self):
        sigmoid = lambda x: 1 / (1 + math.exp(-x))
        x = -1.0
        labels = self.labels("zskd-input-optimization")
        for _ in range(5):
            self.assertIn(f"{x:.2f}", labels)
            self.assertIn(f"{sigmoid(x):.2f}", labels)
            old = sigmoid(x)
            x += 2 * (0.8 - old)
            self.assertGreater(sigmoid(x), old)
            self.assertLess(sigmoid(x), 0.8)

    def test_separable_filter(self):
        x = [[1, 2, 3], [2, 4, 1], [0, 1, 2]]
        h, v = [1, 0, -1], [1, 2, 1]
        u = [sum(a*b for a, b in zip(row, h)) for row in x]
        self.assertEqual(u, [-2, 1, -2])
        y = sum(a*b for a, b in zip(u, v))
        self.assertEqual(y, sum(x[i][j]*v[i]*h[j] for i in range(3) for j in range(3)))
        self.assertEqual(y, -2)
        self.assertIn("−2 + 2 − 2 = −2", self.labels("separable-filter-two-pass"))

    def test_overlapping_windows(self):
        x = [[1, 2, 3], [2, 4, 1], [0, 1, 2], [3, 1, 0]]
        h, v = [1, 0, -1], [1, 2, 1]
        u = [sum(a*b for a, b in zip(row, h)) for row in x]
        self.assertEqual(u, [-2, 1, -2, 3])
        ys = [sum(a*b for a, b in zip(u[i:i+3], v)) for i in range(2)]
        self.assertEqual(ys, [-2, 0])
        self.assertEqual(ys, [sum(x[i+r][c]*v[r]*h[c] for r in range(3) for c in range(3)) for i in range(2)])
        self.assertEqual(4*3 + 2*3, 2*9)
        self.assertEqual(5*3 + 3*3, 24)
        labels = self.labels("separable-filter-two-pass")
        self.assertIn("1 − 4 + 3 = 0", labels)
        self.assertIn("Reused ×2", labels)

    def test_input_update_contraction_and_nonuniqueness(self):
        sigmoid = lambda x: 1/(1+math.exp(-x))
        target = 0.8
        opt = math.log(4)
        for start in [-5., -1., 0., 2., 5.]:
            x = start
            for _ in range(20):
                nxt = x + 2*(target-sigmoid(x))
                self.assertLess(abs(nxt-opt), abs(x-opt))
                self.assertGreater((nxt-opt)*(x-opt), 0)
                x = nxt
        for a,b in [(opt,0),(0,opt),(opt+3,-3)]:
            self.assertAlmostEqual(sigmoid(a+b), target)

if __name__ == "__main__":
    unittest.main()
