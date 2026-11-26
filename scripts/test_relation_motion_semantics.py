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


    def test_anisotropic_geometry_counterexample(self):
        def potentials(pts):
            ds = [math.dist(pts[a], pts[b]) for a, b in [(0, 1), (0, 2), (1, 2)]]
            cs = []
            for i in range(3):
                u, v = [[pts[j][k] - pts[i][k] for k in range(2)] for j in range(3) if i != j]
                cs.append(sum(a*b for a, b in zip(u, v)) / (math.hypot(*u)*math.hypot(*v)))
            return [d/(sum(ds)/3) for d in ds], cs
        a, ac = potentials([(0, 0), (3, 0), (0, 4)])
        b, bc = potentials([(0, 0), (3, 0), (0, 3)])
        for x, y in zip(a, [.75, 1, 1.25]):
            self.assertAlmostEqual(x, y)
        for x, y in zip(b, [.87867965644, .87867965644, 1.24264068712]):
            self.assertAlmostEqual(x, y)
        self.assertEqual(ac[0], bc[0])
        self.assertAlmostEqual(ac[1], .6)
        self.assertAlmostEqual(ac[2], .8)
        self.assertAlmostEqual(bc[1], 1/math.sqrt(2))
        self.assertAlmostEqual(bc[2], 1/math.sqrt(2))
        self.assertGreater(sum((x-y)**2 for x, y in zip(a, b)), 0)
        self.assertGreater(sum((x-y)**2 for x, y in zip(ac, bc)), 0)

    def test_per_sample_scaling_counterexample(self):
        def matrices(q):
            g = [[sum(a*b for a, b in zip(u, v)) for v in q] for u in q]
            return ([[v/math.hypot(*row) for v in row] for row in g],
                    [[g[i][j]/(math.hypot(*q[i])*math.hypot(*q[j])) for j in range(3)] for i in range(3)])
        a, c = matrices([(1, 0), (1, 1), (0, 1)])
        b, d = matrices([(2, 0), (1, 1), (0, 1)])
        self.assertEqual(c, d)
        self.assertEqual(a[2], b[2])
        self.assertAlmostEqual(b[0][0], 4/math.sqrt(20))
        self.assertAlmostEqual(b[1][0], 2/3)
        self.assertAlmostEqual(sum((x-y)**2 for u, v in zip(a, b) for x, y in zip(u, v))/9, .021941635007512405)

    def test_rkd_matching_edge_and_box_pulses(self):
        root = ET.parse(ASSETS / 'rkd-normalized-geometry-motion.svg').getroot()
        moving = next(g for g in root.findall(NS + 'g') if g.get('class') == 'moving')
        pulses = [g for g in moving.findall(NS + 'g') if g.get('opacity') == '0']
        self.assertEqual(len(pulses), 12)
        for i in range(3):
            group = [pulses[j] for j in (i, i+3, i+6, i+9)]
            times = [g.find(NS + 'animate').get('keyTimes') for g in group]
            self.assertEqual(len(set(times)), 1)
            self.assertTrue(all(g.find(NS + 'line') is not None for g in group[:2]))
            self.assertTrue(all(g.find(NS + 'rect') is not None for g in group[2:]))


if __name__ == '__main__':
    unittest.main()
