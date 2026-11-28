"""Check the CTC teaching examples against independently enumerated paths."""
from fractions import Fraction
from itertools import product
from pathlib import Path
import unittest
from xml.etree import ElementTree as ET

ASSETS = Path(__file__).resolve().parents[1] / 'docs/assets/concept-animations'
NS = '{http://www.w3.org/2000/svg}'
STEMS = ('ctc-collapse-scan', 'ctc-path-mass')


def read(stem, kind='motion'):
    return ET.parse(ASSETS / f'{stem}-{kind}.svg').getroot()


def collapse(path):
    return ''.join(x for i, x in enumerate(path) if x != '∅' and (i == 0 or x != path[i-1]))


class CTCMotion(unittest.TestCase):
    def test_collapse(self):
        path = 'AA∅AB'
        self.assertEqual([collapse(path[:i]) for i in range(6)], ['', 'A', 'A', 'A', 'AA', 'AAB'])
        root = read(STEMS[0])
        emitted = [g for g in root.iter(NS+'g') if g.get('id', '').startswith('emit-')]
        self.assertEqual(''.join(g.find(NS+'text').text for g in emitted), collapse(path))
        self.assertEqual([float(g.find(NS+'animate').get('keyTimes').split(';')[1]) for g in emitted], [.15, .62, .8])

    def test_path_mass(self):
        probs = {'∅': Fraction(3, 5), 'A': Fraction(2, 5)}
        totals = {'': Fraction(0), 'A': Fraction(0)}
        expected = [(0, 0)]
        for a, b in product(probs, repeat=2):
            totals[collapse(a+b)] += probs[a]*probs[b]
            expected.append(tuple(int(100*totals[k]) for k in ('', 'A')))
        self.assertEqual(totals, {'': Fraction(9, 25), 'A': Fraction(16, 25)})
        groups = [g for g in read(STEMS[1]).iter(NS+'g') if g.get('id', '').startswith('mass-')]
        self.assertEqual(len(groups), len(expected))
        for group, state in zip(groups, expected):
            self.assertEqual([t.text for t in group.findall(NS+'text')], [f'{v}%' for v in state])
            for bar, value in zip(group.findall(NS+'rect'), state):
                self.assertAlmostEqual(float(bar.get('width')), 2.1*value)

    def test_assets(self):
        for stem in STEMS:
            for kind in ('motion', 'still'):
                root = read(stem, kind)
                self.assertEqual(root.get('viewBox'), '0 0 640 360')
                self.assertTrue(root.find(NS+'desc').text)
                ids = [e.get('id') for e in root.iter() if e.get('id')]
                self.assertEqual(len(ids), len(set(ids)))
                self.assertFalse(any(e.tag in (NS+'script', NS+'image', NS+'foreignObject') for e in root.iter()))
                self.assertFalse(any('href' in k or k.lower().startswith('on') for e in root.iter() for k in e.attrib))
                animations = [e for e in root.iter() if e.tag in (NS+'animate', NS+'animateMotion')]
                self.assertEqual(bool(animations), kind == 'motion')
                for e in animations:
                    self.assertEqual(e.get('repeatCount'), 'indefinite')
                    self.assertEqual(e.get('dur'), '12s')
                    times = [float(t) for t in e.get('keyTimes').split(';')]
                    self.assertEqual(times[0], 0)
                    self.assertEqual(times[-1], 1)
                    self.assertTrue(all(a < b for a, b in zip(times, times[1:])))


if __name__ == '__main__':
    unittest.main()
