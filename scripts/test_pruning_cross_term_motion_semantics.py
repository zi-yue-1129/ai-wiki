import unittest
from pathlib import Path
from xml.etree import ElementTree as ET

STEM = 'pruning-cross-term-sweep'
HERE = Path(__file__).resolve().parent
ASSETS = HERE if (HERE / f'{STEM}-motion.svg').exists() else HERE.parent / 'docs/assets/concept-animations'
NS = '{http://www.w3.org/2000/svg}'


class CrossTermMotion(unittest.TestCase):
    def test_signed_cross_term(self):
        for p in (0, .25, .5, .75, 1):
            full = p * (2 + 1)**2 + (1 - p) * (2 - 1)**2
            self.assertAlmostEqual(full, 5 + 4 * (2*p - 1))
        self.assertEqual((2 - 1)**2, 1)
        self.assertEqual((2 + 1)**2, 9)

    def test_motion_tracks_same_mixture(self):
        root = ET.parse(ASSETS / f'{STEM}-motion.svg').getroot()
        p = (1, 1, .5, .5, 0, 0, 1)
        expected = {
            ('mixture', 'width'): [250*v for v in p],
            ('cursor', 'x1'): [369+230*v for v in p],
            ('cursor', 'x2'): [369+230*v for v in p],
            ('cross', 'x1'): [369+230*v for v in p],
            ('cross', 'x2'): [369+230*v for v in p],
            ('cross', 'y2'): [256-16*(1+8*v) for v in p],
            ('total', 'cx'): [369+230*v for v in p],
            ('total', 'cy'): [256-16*(1+8*v) for v in p],
        }
        seen = set()
        for el in root.iter():
            for a in el.findall(NS+'animate'):
                key = (el.get('id'), a.get('attributeName'))
                self.assertNotIn(key, seen)
                seen.add(key)
                self.assertEqual(list(map(float, a.get('values').split(';'))), expected[key])
                self.assertEqual(a.get('keyTimes'), '0;0.125;0.375;0.5;0.75;0.875;1')
                self.assertEqual(a.get('dur'), '12s')
                self.assertEqual(a.get('repeatCount'), 'indefinite')
                self.assertEqual(float(el.get(key[1])), expected[key][0])
        self.assertEqual(seen, set(expected))
        still = ET.parse(ASSETS / f'{STEM}-still.svg').getroot()
        self.assertEqual(still.get('viewBox'), '0 0 640 360')
        self.assertEqual(root.get('viewBox'), still.get('viewBox'))
        self.assertFalse(list(still.iter(NS+'animate')))
        for tree in (root, still):
            for el in tree.iter():
                self.assertNotIn(el.tag, [NS+'script', NS+'foreignObject'])
                self.assertFalse(any(k.endswith('href') or k.startswith('on') for k in el.attrib))


if __name__ == '__main__':
    unittest.main()
