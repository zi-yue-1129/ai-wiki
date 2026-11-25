"""Check displayed toy calculations against the SVG data, not a model benchmark."""
from pathlib import Path
from fractions import Fraction as F
from xml.etree import ElementTree as ET
import unittest

ASSETS = Path(__file__).resolve().parents[1] / 'docs/assets/concept-animations'
NS = '{http://www.w3.org/2000/svg}'

def panels(stem):
    for kind in ('still', 'motion'):
        root = ET.parse(ASSETS / f'{stem}-{kind}.svg').getroot()
        if kind == 'still':
            yield root
        else:
            yield next(g for g in root.iter(NS+'g') if g.get('class') == 'still')
            yield next(g for g in root.iter(NS+'g') if g.get('class') == 'moving')

class DataRetrievalMotion(unittest.TestCase):
    def test_confident_joint(self):
        for panel in panels('confident-joint-counting'):
            labels = {(t.get('x'), t.get('y')): t.text for t in panel.iter(NS+'text')}
            rows = [(labels['95', str(109+27*i)], F(labels['161', str(109+27*i)]),
                     F(labels['221', str(109+27*i)])) for i in range(8)]
            self.assertTrue(all(a+b == 1 for _, a, b in rows))
            thresholds = [sum(row[j+1] for row in rows if row[0] == 'AB'[j])/4 for j in range(2)]
            self.assertEqual(thresholds, [F(3,5)]*2)
            expected = {}
            counts = [[0,0],[0,0]]
            for i, (given, *p) in enumerate(rows):
                candidates = [j for j in range(2) if p[j] >= thresholds[j]]
                if candidates:
                    j = max(candidates, key=lambda j:p[j])
                    r = 'AB'.index(given)
                    counts[r][j] += 1
                    expected[f'e{i+1}'] = f'{r},{j}'
            actual = {g.get('data-sample'):g.get('data-cell') for g in panel.iter(NS+'g') if g.get('data-sample')}
            self.assertEqual(actual, expected)
            self.assertEqual(counts, [[2,1],[1,2]])
            self.assertEqual(len(rows)-len(actual), 2)
    def test_anisotropic_residual(self):
        x = (3,0); q = (1,0); codes = [(2,0),(3,1)]
        residuals = [(x[0]-a,x[1]-b) for a,b in codes]
        losses = [sum(v*v for v in e) for e in residuals] + [4*a*a+b*b for a,b in residuals]
        self.assertEqual(losses, [1,1,4,1])
        self.assertEqual([sum(a*b for a,b in zip(q,z)) for z in [x]+codes], [3,2,3])
        for panel in panels('scann-anisotropic-residual'):
            bars = [r for r in panel.iter(NS+'rect') if r.get('data-loss')]
            self.assertEqual([int(r.get('data-loss')) for r in bars], losses)
            for r,v in zip(bars,losses):
                anim = r.find(NS+'animate')
                width = max(map(int,anim.get('values').split(';'))) if anim is not None else int(r.get('width'))
                self.assertEqual(width, 45*v)
            self.assertIn('q · x = 3     q · A = 2     q · B = 3', [t.text for t in panel.iter(NS+'text')])

if __name__ == '__main__':
    unittest.main()
