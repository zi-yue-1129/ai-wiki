"""Exact toy arithmetic for masked retraining and integer requantization."""
from fractions import Fraction as F
from pathlib import Path
import unittest
from xml.etree import ElementTree as ET

ASSETS = Path(__file__).resolve().parents[1] / 'docs/assets/concept-animations'
NS = '{http://www.w3.org/2000/svg}'


class MaskedIntegerMotion(unittest.TestCase):
    def labels(self, stem, kind):
        root = ET.parse(ASSETS / f'{stem}-{kind}.svg').getroot()
        return [e.text for e in root.iter(NS + 'text')]

    def test_integer_accumulation_and_requantization(self):
        products = [(x - 3) * w for x, w in zip((7, 2, 5), (4, -2, 1))]
        sums = [sum(products[:i]) for i in range(1, 4)]
        self.assertEqual(products, [16, 2, 2])
        self.assertEqual(sums, [16, 18, 20])
        a = sums[-1]
        self.assertEqual(F(1, 4) * F(1, 2) * a, F(5, 2))
        self.assertEqual(F(1, 4) * F(1, 2) / F(2, 5), F(5, 16))
        self.assertEqual(F(5, 16) * a, F(25, 4))
        q = min(255, max(0, ((5 * a + 8) >> 4) + 10))
        self.assertEqual(q, 16)
        self.assertEqual(F(2, 5) * (q - 10), F(12, 5))
        for kind in ('motion', 'still'):
            labels = self.labels('integer-requantization-accumulator', kind)
            for label in ('16', '18', '20', '20 → 6.25', '6', 'q = 16'):
                self.assertIn(label, labels)

    def test_fixed_mask_gradient(self):
        w = [F('0.8'), F('0.1'), F('-0.4')]
        mask = [int(abs(v) >= F('0.2')) for v in w]
        self.assertEqual(mask, [1, 0, 1])
        v = [m * p for m, p in zip(mask, w)]
        x = [1, 2, 1]
        target = F('1.4')
        residual = sum(a * b for a, b in zip(v, x)) - target
        g = [residual * a for a in x]
        self.assertEqual(g, [-1, -2, -1])
        self.assertEqual([m * a for m, a in zip(mask, g)], [-1, 0, -1])
        updated = [m * (a - F('0.2') * b) for m, a, b in zip(mask, v, g)]
        self.assertEqual(updated, [1, 0, F('-0.2')])
        self.assertEqual(residual ** 2 / 2, F('0.50'))
        self.assertEqual((sum(a * b for a, b in zip(updated, x)) - target) ** 2 / 2, F('0.18'))
        for kind in ('motion', 'still'):
            labels = self.labels('prune-fixed-mask-gradient', kind)
            for label in ('−2', '0', '1.0', '−0.2', '0.50', '0.18'):
                self.assertIn(label, labels)


if __name__ == '__main__':
    unittest.main()
