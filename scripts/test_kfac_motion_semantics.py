"""Check the displayed curvature and patch arithmetic in both visual variants."""
from pathlib import Path
from fractions import Fraction
from xml.etree import ElementTree as ET
import unittest

ASSETS = Path(__file__).resolve().parents[1] / 'docs/assets/concept-animations'
NS = '{http://www.w3.org/2000/svg}'

class CurvatureMotion(unittest.TestCase):
    def test_ekfac(self):
        for kind in ('motion', 'still'):
            root = ET.parse(ASSETS / f'ekfac-eigenvalue-correction-{kind}.svg').getroot()
            texts = {(e.get('x'), e.get('y'), e.text) for e in root.iter(NS+'text')}
            for i, moment in enumerate((1, 3, 3, 1)):
                x = 102 + i*145
                self.assertIn((str(x-23), '133', '2'), texts)
                self.assertIn((str(x+22), str(183-moment*25), str(moment)), texts)
                self.assertIn((str(x), '294', '1'), texts)
                self.assertIn((str(x), '339', str(float(Fraction(3, moment+1)))), texts)
                bars = [e for e in root.iter(NS+'rect') if e.get('x') == str(x+6) and e.get('fill') == '#087f82']
                self.assertTrue(bars)
                for bar in bars:
                    self.assertEqual(int(bar.get('height')), moment*25)
                    self.assertEqual(int(bar.get('y')) + int(bar.get('height')), 191)
    def test_ekfac_joint_moment_construction(self):
        # Eight equally weighted pairs a=e_i, g=sqrt(8)*e_j.
        counts = ((1, 3), (3, 1))
        n = sum(map(sum, counts))
        a = [Fraction(sum(row), n) for row in counts]
        g = [Fraction(8*sum(row[j] for row in counts), n) for j in range(2)]
        kfac = [x*y for x in a for y in g]
        corrected = [Fraction(8*c, n) for row in counts for c in row]
        self.assertEqual(a, [Fraction(1, 2)]*2)
        self.assertEqual(g, [4, 4])
        self.assertEqual(kfac, [2]*4)
        self.assertEqual(corrected, [1, 3, 3, 1])
        self.assertEqual(sum((x-y)**2 for x, y in zip(kfac, corrected)), 4)
        self.assertEqual([Fraction(3)/(x+1) for x in corrected],
                         [Fraction(3, 2), Fraction(3, 4), Fraction(3, 4), Fraction(3, 2)])

    def test_kfc(self):
        patches = [(1, 2), (2, 3), (3, 4)]
        sums = [sum(p[j//2]*p[j%2] for p in patches) for j in range(4)]
        for kind in ('motion', 'still'):
            root = ET.parse(ASSETS / f'kfc-patch-second-moment-{kind}.svg').getroot()
            texts = {(e.get('x'), e.get('y'), e.text) for e in root.iter(NS+'text')}
            for i, p in enumerate(patches):
                x = 105 + i*215
                self.assertIn((str(x), '176', f'[{p[0]}, {p[1]}]'), texts)
                for j in range(4):
                    self.assertIn((str(x-28+(j%2)*56), str(216+(j//2)*32), str(p[j//2]*p[j%2])), texts)
            self.assertIn(('320', '336', f'[{sums[0]}, {sums[1]}; {sums[2]}, {sums[3]}] / 3'), texts)

if __name__ == '__main__':
    unittest.main()
