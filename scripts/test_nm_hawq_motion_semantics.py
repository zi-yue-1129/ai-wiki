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


    def test_mask_turnover_threshold(self):
        from fractions import Fraction as F
        for lam in (F(0), F(3, 10), F(1)):
            threshold = F(1, 10) + F(7, 10)*lam
            for offset in (-F(1, 100), F(0), F(1, 100)):
                u = threshold + offset
                third = F(7, 10) + u - F(7, 10)*lam
                self.assertEqual(third > F(8, 10), offset > 0)
                self.assertEqual(third == F(8, 10), offset == 0)

    def test_quadratic_perturbation_animation(self):
        motion = ET.parse(ASSETS / 'hawq-curvature-budget-motion.svg').getroot()
        still = ET.parse(ASSETS / 'hawq-curvature-budget-still.svg').getroot()
        for j in range(2):
            for i in range(2):
                h = 2 if i else 8
                d = 0.5 if j == i else 0.25
                def track(kind):
                    node = motion.find(f".//*[@id='moving-{j}-{i}-{kind}']")
                    static = still.find(f".//*[@id='still-{j}-{i}-{kind}']")
                    a = node.find(NS + 'animate')
                    return ([float(v) for v in a.get('values').split(';')],
                            a.get('keyTimes'), float(static.get('width')))
                delta, dt, delta_end = track('delta')
                loss, lt, loss_end = track('loss')
                self.assertEqual(dt, lt)
                self.assertEqual(len(delta), len(loss))
                self.assertEqual(delta_end, 300*d)
                self.assertEqual(loss_end, 150*0.5*h*d*d)
                for dw, lw in zip(delta, loss):
                    self.assertAlmostEqual(lw/150, 0.5*h*(dw/300)**2, places=6)
        self.assertEqual(0.5*(8-2)*(0.5**2-0.25**2), 0.5625)


if __name__ == '__main__':
    unittest.main()
