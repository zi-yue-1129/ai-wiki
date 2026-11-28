"""Check CTC posterior and repeat-prefix visual examples by path enumeration."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import unittest
from xml.etree import ElementTree as ET

ASSETS = Path(__file__).resolve().parents[1] / 'docs/assets/concept-animations'
if not ASSETS.is_dir():
    ASSETS = Path(__file__).resolve().parent
NS = '{http://www.w3.org/2000/svg}'
STEMS = ('ctc-alignment-posterior', 'ctc-prefix-repeat')


def collapse(path):
    return ''.join(x for i, x in enumerate(path) if x != '∅' and (i == 0 or x != path[i-1]))


def mass(path):
    p = F(1)
    for x in path:
        p *= F(3, 5) if x == '∅' else F(2, 5)
    return p


def texts(stem):
    return [e.text for e in ET.parse(ASSETS / f'{stem}-still.svg').iter(NS+'text')]


class CTCPosteriorMotion(unittest.TestCase):
    def test_posterior(self):
        joint = [F(0)] * 3
        for path in product('∅A', repeat=3):
            if collapse(path) == 'A':
                state = 1 if path[1] == 'A' else (2 if path[0] == 'A' else 0)
                joint[state] += mass(path)
        self.assertEqual(joint, [F(18, 125), F(2, 5), F(18, 125)])
        total = sum(joint)
        self.assertEqual(total, F(86, 125))
        p = joint[1] / total
        self.assertEqual(p, F(25, 43))
        expected = [f'{float(x):.3f}' for x in joint] + [f'P(A) = {float(total):.3f}', f'∅ {float(1-p):.2%}', f'A {float(p):.2%}']
        for value in expected:
            self.assertIn(value, texts(STEMS[0]))

    def test_repeat(self):
        old = {x: F(0) for x in '∅A'}
        for path in product('∅A', repeat=2):
            if collapse(path) == 'A':
                old[path[-1]] += mass(path)
                self.assertEqual(collapse(path+('A',)), 'AA' if path[-1] == '∅' else 'A')
        self.assertEqual(old, {'∅': F(6, 25), 'A': F(2, 5)})
        for v in old.values():
            self.assertIn(f'{float(v*F(2, 5)):.3f}', texts(STEMS[1]))

    def test_assets(self):
        for stem in STEMS:
            for kind in ('motion', 'still'):
                root = ET.parse(ASSETS / f'{stem}-{kind}.svg').getroot()
                self.assertEqual(root.get('viewBox'), '0 0 640 360')
                self.assertTrue(root.find(NS+'desc').text)
                ids = [e.get('id') for e in root.iter() if e.get('id')]
                self.assertEqual(len(ids), len(set(ids)))
                self.assertFalse(any(e.tag in (NS+'script', NS+'image', NS+'foreignObject') for e in root.iter()))
                self.assertFalse(any('href' in k or k.lower().startswith('on') for e in root.iter() for k in e.attrib))
                anim = [e for e in root.iter() if e.tag in (NS+'animate', NS+'animateMotion')]
                self.assertEqual(bool(anim), kind == 'motion')
                for e in anim:
                    self.assertEqual(e.get('repeatCount'), 'indefinite')
                    self.assertEqual(e.get('dur'), '12s')
                    ts = list(map(float, e.get('keyTimes').split(';')))
                    self.assertEqual((ts[0], ts[-1]), (0, 1))
                    self.assertTrue(all(a < b for a, b in zip(ts, ts[1:])))


if __name__ == '__main__':
    unittest.main()
