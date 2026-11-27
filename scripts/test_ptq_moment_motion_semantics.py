"""Check exact toy arithmetic and matching SVG keyframe geometry."""
import unittest
from fractions import Fraction as F
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'docs/assets/concept-animations'
if not ASSETS.is_dir():  # standalone local QA, same assets beside this test
    ASSETS = Path(__file__).resolve().parent
NS = '{http://www.w3.org/2000/svg}'


def read(stem, kind):
    return ET.parse(ASSETS / f'{stem}-{kind}.svg').getroot()


def values(element):
    return list(map(float, element.get('values').split(';')))


class PTQMomentMotion(unittest.TestCase):
    def test_group_rounding(self):
        small = [F(1), F(3, 2), F(3), F(4)]
        large = [F(8), F(16), F(24), F(28)]
        sse = lambda ws, s: sum((w - round(w / s) * s) ** 2 for w in ws)
        self.assertEqual(sse(small + large, F(4)), F(17, 4))
        self.assertEqual(sse(small, F(4, 7)) + sse(large, F(4)), F(17, 196))
        root = read('ptq-group-scale-grid', 'motion')
        motions = root.findall('.//' + NS + 'animate')
        self.assertEqual(len(motions), 8)
        for j, (left, s) in enumerate([(15, F(4)), (330, F(4, 7))]):
            for i, w in enumerate(small):
                v = values(motions[4*j+i])
                self.assertAlmostEqual(v[0], float(left+65+55*w), places=3)
                self.assertAlmostEqual(v[2], float(left+65+55*round(w/s)*s), places=3)
                self.assertEqual(v[2], v[3])
                self.assertEqual(v[0], v[-1])

    def test_moment_descent(self):
        root = read('data-free-moment-descent', 'motion')
        motions = root.findall('.//' + NS + 'animate')
        self.assertEqual(len(motions), 6)
        steps = [0, 0, 1, 2, 3, 4, 5, 5, 0]
        m, s = F(-1), F(1, 4)
        states = [(m, s)]
        for _ in range(5):
            m -= F(1, 4)*2*(m-2)
            s -= F(1, 4)*2*(s-1)
            states.append((m, s))
        for i, k in enumerate(steps):
            m, s = states[k]
            loss = (m-2)**2 + (s-1)**2
            self.assertEqual(loss, F(153, 16)/4**k)
            a, b = 80+80*(m-s+2), 80+80*(m+s+2)
            expected = [a, b, 80+80*(m+2)-2, a, b, 460*loss/F(153,16)]
            for motion, val in zip(motions, expected):
                self.assertAlmostEqual(values(motion)[i], float(val), places=3)

    def test_asset_contracts(self):
        for stem in ('ptq-group-scale-grid', 'data-free-moment-descent'):
            for kind in ('motion', 'still'):
                root = read(stem, kind)
                self.assertEqual(root.get('viewBox'), '0 0 640 360')
                self.assertIsNotNone(root.find(NS+'title'))
                self.assertIsNotNone(root.find(NS+'desc'))
                self.assertFalse(any(e.tag.split('}')[-1] in ('script','foreignObject','image') for e in root.iter()))
                animations = root.findall('.//' + NS + 'animate')
                self.assertEqual(bool(animations), kind=='motion')
                for a in animations:
                    self.assertEqual(a.get('repeatCount'), 'indefinite')
                    self.assertEqual(a.get('dur'), '12s')
                    times = list(map(float, a.get('keyTimes').split(';')))
                    self.assertEqual(len(times), len(values(a)))
                    self.assertEqual(times, sorted(set(times)))
                    self.assertEqual((times[0],times[-1]),(0,1))


if __name__ == '__main__':
    unittest.main()
