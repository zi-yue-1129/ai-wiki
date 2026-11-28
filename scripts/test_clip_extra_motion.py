"""Numerical and structural regression checks for CLIP sensitivity illustrations."""
import math
from pathlib import Path
import unittest
from xml.etree import ElementTree as ET

ASSETS = Path(__file__).resolve().parents[1] / 'docs/assets/concept-animations'
NS = '{http://www.w3.org/2000/svg}'


def load(stem, kind='motion'):
    return ET.parse(ASSETS / f'clip-{stem}-{kind}.svg').getroot()


def track(root, ident, attribute):
    el = root.find(f'.//*[@id="{ident}"]')
    anim = el.find(f'{NS}animate[@attributeName="{attribute}"]')
    return [float(v) for v in anim.get('values').split(';')]


class CLIPExtraMotion(unittest.TestCase):
    def test_temperature(self):
        root = load('temperature-scale')
        scales = [1 + i/4 for i in range(37)]
        scales += scales[-2::-1]
        for i in range(2):
            p = [1/(1+math.exp(-.4*s)) for s in scales]
            if i:
                p = [1-v for v in p]
            for ident, attr, expected in [
                (f'prob-bar-{i}', 'width', [185*v for v in p]),
                (f'prob-dot-{i}', 'cy', [282-190*v for v in p]),
                (f'prob-dot-{i}', 'cx', [65+31*(s-1) for s in scales]),
            ]:
                actual = track(root, ident, attr)
                self.assertEqual(len(actual), len(expected))
                for a, b in zip(actual, expected):
                    self.assertAlmostEqual(a, b, delta=.0001)
        self.assertTrue(all(1/(1+math.exp(-.4*s)) > .5 for s in scales))

    def test_prompt(self):
        root = load('prompt-ensemble')
        mean = (.5, .5)
        v = tuple(x/math.hypot(*mean) for x in mean)
        self.assertAlmostEqual(math.hypot(*v), 1)
        self.assertLess(0, .6)
        self.assertGreater(v[1], .6)
        x = track(root, 'ensemble-vector', 'x2')
        y = track(root, 'ensemble-vector', 'y2')
        self.assertEqual((x[2], y[2]), (162, 197))
        self.assertAlmostEqual(x[4], 72+180*v[0], delta=.0001)
        self.assertAlmostEqual(y[4], 287-180*v[1], delta=.0001)
        self.assertEqual((x[-1], y[-1]), (252, 287))
        self.assertAlmostEqual(track(root, 'class-a-score', 'width')[2], 206*v[1], delta=.0001)

    def test_assets(self):
        for stem in ('temperature-scale', 'prompt-ensemble'):
            for kind in ('motion', 'still'):
                root = load(stem, kind)
                self.assertEqual(root.get('viewBox'), '0 0 640 360')
                ids = [el.get('id') for el in root.iter() if el.get('id')]
                self.assertEqual(len(ids), len(set(ids)))
                self.assertTrue(root.find(f'{NS}desc').text)
                animations = list(root.iter(f'{NS}animate'))
                self.assertEqual(bool(animations), kind == 'motion')
                for a in animations:
                    self.assertEqual(a.get('dur'), '12s')
                    self.assertEqual(a.get('repeatCount'), 'indefinite')
                    self.assertEqual(len(a.get('values').split(';')), len(a.get('keyTimes').split(';')))
                for el in root.iter():
                    self.assertNotIn(el.tag, {NS+'script', NS+'foreignObject', NS+'image'})
                    self.assertFalse(any('href' in k or k.startswith('on') for k in el.attrib))


if __name__ == '__main__':
    unittest.main()
