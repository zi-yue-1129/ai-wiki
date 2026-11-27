import itertools
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET

HERE = Path(__file__).resolve().parent
ASSETS = HERE if (HERE / 'svd-factor-rank-budget-motion.svg').exists() else HERE.parent / 'docs/assets/concept-animations'
NS = '{http://www.w3.org/2000/svg}'

class RankFactorFollowup(unittest.TestCase):
    def test_factor_shapes_and_output(self):
        sigma = [6, 3, 1, .5]
        x = [1, 1, 1, 1]
        for r in range(1, 4):
            b = [[int(i == j) for j in range(4)] for i in range(r)]
            a = [[sigma[i] * int(i == j) for j in range(r)] for i in range(4)]
            h = [sum(v * u for v, u in zip(row, x)) for row in b]
            y = [sum(v * u for v, u in zip(row, h)) for row in a]
            self.assertEqual(y, [s if i < r else 0 for i, s in enumerate(sigma)])
            self.assertEqual(sum(map(len, a)) + sum(map(len, b)), 8 * r)
        for suffix in ['motion', 'still']:
            root = ET.parse(ASSETS / f'svd-factor-rank-budget-{suffix}.svg').getroot()
            labels = {(e.get('x'), e.get('y'), e.text) for e in root.iter(NS+'text')}
            for i, v in enumerate([6, 3, 1]):
                self.assertIn((str(386+26*i), str(81+26*i), str(v)), labels)
                self.assertIn(('553', str(81+26*i), str(v)), labels)
                self.assertIn(('224', str(225+45*i), f'{8*(i+1)} / 16'), labels)

    def test_all_fixed_masks(self):
        w = [4, 3, 2, 1]
        xs = [[0, 1, 3, 4], [1, 1, 0, 0]]
        second_moment = [[sum(x[i]*x[j] for x in xs)/len(xs) for j in range(4)] for i in range(4)]
        scores = {}
        for keep in itertools.combinations(range(4), 2):
            delta = [0 if i in keep else v for i, v in enumerate(w)]
            mse = sum(sum(v*u for v, u in zip(delta, x))**2 for x in xs)/len(xs)
            quadratic = sum(delta[i]*second_moment[i][j]*delta[j] for i in range(4) for j in range(4))
            self.assertAlmostEqual(mse, quadratic)
            scores[tuple(i+1 for i in keep)] = mse
        self.assertEqual(scores, {(1, 2): 50, (1, 3): 29, (1, 4): 45, (2, 3): 16, (2, 4): 26, (3, 4): 29})
        self.assertEqual(min(scores, key=scores.get), (2, 3))

if __name__ == '__main__':
    unittest.main()
