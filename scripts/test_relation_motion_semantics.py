import math
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'docs/assets/concept-animations'
if not ASSETS.is_dir():
    ASSETS = Path(__file__).resolve().parent
NS = '{http://www.w3.org/2000/svg}'


def labels(stem):
    root = ET.parse(ASSETS / (stem + '-still.svg')).getroot()
    return {(float(t.get('x')), float(t.get('y'))): t.text for t in root.iter(NS + 'text')}


class RelationMotion(unittest.TestCase):
    def test_rkd_geometry(self):
        lab = labels('rkd-normalized-geometry')
        for j, pts in enumerate([[(0, 0), (3, 0), (0, 4)], [(10, 5), (10, 11), (2, 5)]]):
            distances = [math.dist(pts[a], pts[b]) for a, b in [(0, 1), (0, 2), (1, 2)]]
            mean = sum(distances) / 3
            self.assertEqual(lab[(162 if not j else 474, 274)], f'Mean = {mean:g}' if j else 'Mean = 4')
            for k, d in enumerate(distances):
                self.assertEqual(lab[(72 + 312*j + 90*k, 305)], f'{["AB", "AC", "BC"][k]} {d/mean:.2f}')
            u, v = [[pts[k][i] - pts[0][i] for i in range(2)] for k in (1, 2)]
            self.assertEqual(sum(a*b for a, b in zip(u, v)), 0)

    def test_row_gram_normalization(self):
        lab = labels('sp-row-gram-normalization')
        normalized = []
        for j, features in enumerate([[(1, 0), (1, 1), (0, 1)], [(0, 2), (2, 2), (2, 0)]]):
            gram = [[sum(a*b for a, b in zip(u, v)) for v in features] for u in features]
            normalized.append([[v/math.hypot(*row) for v in row] for row in gram])
            for i, row in enumerate(gram):
                y = 76 + j*132 + 44 + i*30
                for k, v in enumerate(row):
                    self.assertEqual(lab[(265+40*k, y)], str(v))
                    self.assertEqual(lab[(464+52*k, y)], f'{v/math.hypot(*row):.3f}')
        self.assertEqual(normalized[0], normalized[1])
        self.assertNotEqual(normalized[0][0][1], normalized[0][1][0])


if __name__ == '__main__':
    unittest.main()
