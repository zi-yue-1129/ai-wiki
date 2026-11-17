#!/usr/bin/env python3
"""Check illustrative numerical values underlying bilingual Adam motion figures."""
import math
import unittest

class TestAdamMotionSemantics(unittest.TestCase):
    def test_sign_reversal(self):
        m = v = 0.0
        moments = []
        for t in range(1, 11):
            g = 1.0 if t <= 4 else -1.0
            m = 0.8 * m + 0.2 * g
            v = 0.5 * v + 0.5 * (g * g)
            mhat, vhat = m / (1 - 0.8**t), v / (1 - 0.5**t)
            self.assertAlmostEqual(vhat, 1.0)
            moments.append(mhat / math.sqrt(vhat))
        self.assertAlmostEqual(moments[4], 0.4050, delta=0.001)
        self.assertAlmostEqual(moments[5], 0.0242, delta=0.001)
        self.assertAlmostEqual(moments[6], -0.2350, delta=0.001)
        self.assertGreater(moments[5], 0)
        self.assertLess(moments[6], 0)

    def test_epsilon_regularizes_scale(self):
        for c in (0.02, 0.05, 0.1, 0.15, 0.25, 0.35, 0.5):
            self.assertAlmostEqual(c / math.sqrt(c*c), 1.0)
            self.assertAlmostEqual(c / (math.sqrt(c*c) + 0.1), c/(c+0.1))
        self.assertAlmostEqual(0.1/(0.1+0.1), 0.5)
        self.assertAlmostEqual(0.5/(0.5+0.1), 5/6)

if __name__ == "__main__":
    unittest.main()
