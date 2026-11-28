"""CTC forward lattice and repeated-label feasibility teaching checks."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import unittest
from xml.etree import ElementTree as ET

ASSETS = Path(__file__).resolve().parents[1] / 'docs/assets/concept-animations'
NS = '{http://www.w3.org/2000/svg}'
STEMS = ('ctc-forward-lattice', 'ctc-repeat-skip')


def read(stem, kind='motion'):
    return ET.parse(ASSETS / f'{stem}-{kind}.svg').getroot()


def collapse(path):
    return ''.join(v for i, v in enumerate(path) if v != '∅' and (not i or v != path[i-1]))


class CTCForwardMotion(unittest.TestCase):
    def test_forward(self):
        prob = {'∅': F(3, 5), 'A': F(2, 5)}
        expected = []
        for t in range(1, 4):
            masses = [F(0)] * 3
            for path in product(prob, repeat=t):
                result = collapse(path)
                if result not in ('', 'A'):
                    continue
                state = 0 if not result else (1 if path[-1] == 'A' else 2)
                weight = F(1)
                for token in path:
                    weight *= prob[token]
                masses[state] += weight
            expected.append(masses)
        self.assertEqual(expected[-1][1] + expected[-1][2], F(86, 125))
        root = read(STEMS[0])
        for j in (1, 2):
            for i in range(3):
                g = root.find(f'.//{NS}g[@id="dp-{j}-{i}"]')
                self.assertEqual(g.find(NS+'text').text, f'{float(expected[j][i]):.3f}')
                self.assertEqual(float(g.find(NS+'animate').get('keyTimes').split(';')[1]), (.35, .65)[j-1])
        static_values = [e.text for e in read(STEMS[0], 'still').iter(NS+'text')]
        for row in expected:
            for value in row:
                self.assertIn(f'{float(value):.3f}', static_values)
        self.assertIn('P(A) = 0.304 + 0.384 = 0.688', static_values)

    def test_skip(self):
        for target, minimal in [('AB', 2), ('AA', 3)]:
            paths = {t: [p for p in product('A∅B', repeat=t) if collapse(p) == target] for t in (1, 2, 3)}
            self.assertEqual(min(t for t, p in paths.items() if p), minimal)
            self.assertIn(('A', '∅', target[1]), paths[3])
        root = read(STEMS[1])
        for lane, labels in enumerate([('2 frames: A B', '3 frames: A ∅ B'), ('2 frames: impossible', '3 frames: A ∅ A')]):
            for prefix, label, time in zip(('short', 'long'), labels, (.35, .76)):
                g = root.find(f'.//{NS}g[@id="{prefix}-{lane}"]')
                self.assertEqual(g.find(NS+'text').text, label)
                self.assertEqual(float(g.find(NS+'animate').get('keyTimes').split(';')[1]), time)

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
                    self.assertEqual((times[0], times[-1]), (0, 1))
                    self.assertTrue(all(a < b for a, b in zip(times, times[1:])))


if __name__ == '__main__':
    unittest.main()
