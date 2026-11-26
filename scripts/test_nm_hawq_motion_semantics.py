"""Check the reviewed SR-STE and HAWQ numerical diagrams."""
from pathlib import Path
from xml.etree import ElementTree as ET
import unittest

ASSETS = Path(__file__).resolve().parents[1] / 'docs/assets/concept-animations'
NS = '{http://www.w3.org/2000/svg}'


def labels(stem, kind):
    root = ET.parse(ASSETS / f'{stem}-{kind}.svg').getroot()
    return {node.text for node in root.iter(NS + 'text')}


class MaskAndCurvature(unittest.TestCase):
    def test_sr_ste_mask_turnover(self):
        w = [0.9, 0.8, 0.7, 0.2]
        grad = [0, 0, -0.22, 0]
        mask = lambda v: set(sorted(range(4), key=lambda i: -abs(v[i]))[:2])
        initial = mask(w)
        for lam, expected, sad in [(0, [0.9, 0.8, 0.92, 0.2], 2),
                                   (0.3, [0.9, 0.8, 0.71, 0.14], 0)]:
            updated = [a-g-lam*(i not in initial)*a for i, (a, g) in enumerate(zip(w, grad))]
            for actual, target in zip(updated, expected):
                self.assertAlmostEqual(actual, target)
            self.assertEqual(len(mask(updated)), 2)
            self.assertEqual(len(initial ^ mask(updated)), sad)
            for kind in ('motion', 'still'):
                actual = labels('nm-sr-ste-mask-turnover', kind)
                self.assertTrue({f'{x:.2f}' for x in updated} | {f'SAD = {sad}'} <= actual)

    def test_curvature_budget(self):
        for bits, errors, target in [((4, 8), (0.5, 0.25), 1.0625),
                                     ((8, 4), (0.25, 0.5), 0.5)]:
            self.assertEqual(sum(bits), 12)
            loss = sum(0.5*h*e**2 for h, e in zip((8, 2), errors))
            self.assertEqual(loss, target)
            for kind in ('motion', 'still'):
                self.assertIn(f'Total ΔL = {loss}', labels('hawq-curvature-budget', kind))


if __name__ == '__main__':
    unittest.main()
