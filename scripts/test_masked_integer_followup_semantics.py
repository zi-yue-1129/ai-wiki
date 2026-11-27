"""Regression checks for the integer branch and permanent gradient gate."""
from fractions import Fraction as F
from pathlib import Path
from xml.etree import ElementTree as ET
import unittest
P = Path(__file__).resolve().parents[1] / 'docs/assets/concept-animations'
NS = '{http://www.w3.org/2000/svg}'


class Followup(unittest.TestCase):
    def test_requantization(self):
        for a in range(-1000, 1001):
            r = (5*a+8)//16
            self.assertEqual(r, (F(5*a, 16)+F(1, 2)).__floor__())
            q = min(255, max(0, r+10))
            self.assertTrue(0 <= q <= 255)
        self.assertEqual((5*20+8)//16, 6)
        self.assertEqual((5*8+8)//16, 3)
        self.assertEqual((5*(-8)+8)//16, -2)
        self.assertEqual(min(255, max(0, (5*1000+8)//16+10)), 255)
        self.assertEqual(min(255, max(0, (5*(-100)+8)//16+10)), 0)
        for kind in ('motion', 'still'):
            root = ET.parse(P / f'integer-requantization-accumulator-{kind}.svg').getroot()
            labels = [e.text for e in root.iter(NS+'text')]
            for label in ('20 → 6.25', '5×20+8 = 108', 'Shift right 4', '6', 'q = 16', 'Math only', 'Integer path'):
                self.assertIn(label, labels)

    def test_masked_retraining(self):
        eta = F(1, 5)
        mu = F(9, 10)
        velocity = F(-2)
        self.assertEqual(-eta*mu*velocity, F(9, 25))
        self.assertEqual(0*(-eta*mu*velocity), 0)
        r = F(-1)
        for _ in range(5):
            r = (1-2*eta)*r
        self.assertEqual(r, -F(3, 5)**5)
        self.assertEqual(F(1, 2)*(1-2*eta)**2, F(9, 50))
        for kind in ('motion', 'still'):
            root = ET.parse(P / f'prune-fixed-mask-gradient-{kind}.svg').getroot()
            labels = [e.text for e in root.iter(NS+'text')]
            for label in ('−2', '0', '1.0', '−0.2', '0.50', '0.18'):
                self.assertIn(label, labels)
            self.assertTrue(any(e.get('d') == 'M386 177H402' for e in root.iter(NS+'path')))


if __name__ == '__main__':
    unittest.main()
