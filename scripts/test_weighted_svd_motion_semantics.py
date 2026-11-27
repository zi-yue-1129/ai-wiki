import unittest
from pathlib import Path
from xml.etree import ElementTree as ET

HERE = Path(__file__).resolve().parent
STEM = 'svd-input-weighted-rank-one'
ASSETS = HERE if (HERE / f'{STEM}-motion.svg').exists() else HERE.parent / 'docs/assets/concept-animations'
NS = '{http://www.w3.org/2000/svg}'


class WeightedSVDMotion(unittest.TestCase):
    def test_weighted_energy_and_motion(self):
        root = ET.parse(ASSETS / f'{STEM}-motion.svg').getroot()
        p = [.1, .1, .2, .2, .9, .9, .1]
        funcs = [lambda v: 240*v, lambda v: 216*v, lambda v: 54*(1-v)]
        widths = [a for a in root.iter(NS+'animate') if a.get('attributeName') == 'width']
        self.assertEqual(len(widths), len(funcs))
        for a, fn in zip(widths, funcs):
            values = list(map(float, a.get('values').split(';')))
            self.assertEqual(len(values), len(p))
            for v, q in zip(values, p):
                self.assertAlmostEqual(v, fn(q))
        dots = [a for a in root.iter(NS+'animate') if a.get('attributeName') == 'cy']
        self.assertEqual(len(dots), 2)
        for a, fn in zip(dots, [lambda v: 290-45*(1-v), lambda v: 290-180*v]):
            for value, q in zip(map(float, a.get('values').split(';')), p):
                self.assertAlmostEqual(value, fn(q))
        for q in [0, .1, .2, .5, .9, 1]:
            self.assertAlmostEqual(min(36*q, 9*(1-q)), 36*q+9*(1-q)-max(36*q, 9*(1-q)))
        self.assertAlmostEqual(36*.2, 9*(1-.2))
        still = ET.parse(ASSETS / f'{STEM}-still.svg').getroot()
        self.assertFalse(list(still.iter(NS+'animate')))
        self.assertEqual(still.get('viewBox'), root.get('viewBox'))

    def test_pruning_cross_terms(self):
        xs = [(0, 1, 3, 4), (1, 1, 0, 0)]
        for delta, expected in [((0, 0, 2, 1), (26, 24)), ((4, 0, 0, 1), (16, 0))]:
            diagonal = sum(sum((d*v)**2 for d, v in zip(delta, x)) for x in xs)/2
            full = sum(sum(d*v for d, v in zip(delta, x))**2 for x in xs)/2
            self.assertEqual((diagonal, full-diagonal), expected)


if __name__ == '__main__':
    unittest.main()
