import unittest
from fractions import Fraction as F
from pathlib import Path
import xml.etree.ElementTree as ET

ASSETS = Path(__file__).resolve().parents[1] / 'docs/assets/concept-animations'
NS = '{http://www.w3.org/2000/svg}'


class SlimmingFollowupSemantics(unittest.TestCase):
    def test_signed_history_and_selection(self):
        steps = [[F(9,10), F(-6,10), F(3,10), F(-2,10)]]
        for _ in range(2):
            steps.append([g - F(1,10)*(int(g>0)-int(g<0)) for g in steps[-1]])
        def label(g):
            return '0.0' if not g else ('−' if g < 0 else '+') + f'{float(abs(g)):.1f}'
        for kind in ('motion', 'still'):
            root = ET.parse(ASSETS / f'network-slimming-scale-shrink-{kind}.svg').getroot()
            for x, values in zip(('300','356','412'), steps):
                actual = [e.text for e in root.iter(NS+'text') if e.get('x') == x and e.get('y') != '62']
                self.assertEqual(actual, list(map(label, values)))
            self.assertEqual([i for i,g in enumerate(steps[-1]) if abs(g) >= F(3,20)], [0,1])
        # Fixed-step subgradient descent is not a soft-thresholding operator.
        g = F(3,100)
        g1 = g - F(1,10)
        self.assertEqual(g1, F(-7,100))
        self.assertEqual(g1 + F(1,10), g)
        # A zero BN scale can still produce a nonzero ReLU activation.
        beta, w = F(1,2), F(3)
        for z in (-10, 0, 10):
            self.assertEqual(w * max(0, 0*z + beta), F(3,2))

    def test_two_stability_distances(self):
        a = [F(7,10), 0, F(4,10), 0]
        b = [F(6,10), 0, F(5,10), 0]
        dense_masked = [F(9,10), 0, F(-8,10), 0]
        distance_squared = lambda u,v: sum((x-y)**2 for x,y in zip(u,v))
        self.assertEqual(distance_squared(a,b), F(2,100))
        self.assertEqual(distance_squared(a,dense_masked), F(148,100))


if __name__ == '__main__':
    unittest.main()
