"""Analytic checks for the simultaneous SGD and semi-hard screening examples."""
import math
from pathlib import Path
import unittest
from xml.etree import ElementTree as ET

ASSETS = Path(__file__).resolve().parents[1] / 'docs/assets/concept-animations'
NS = '{http://www.w3.org/2000/svg}'


class EmbeddingGradientScreening(unittest.TestCase):
    def test_gradient_step(self):
        w, c = (1, 0), (0, 1)
        b, d = math.log(100) + 1, 0
        r = sum(x*y for x, y in zip(w, c)) + b + d - math.log(100)
        f = min(1, (100/100)**.75)
        g = 2*f*r
        self.assertEqual(g, 2)
        wn = tuple(x-.1*g*y for x, y in zip(w, c))
        cn = tuple(y-.1*g*x for x, y in zip(w, c))
        self.assertEqual(wn, (1, -.2))
        self.assertEqual(cn, (-.2, 1))
        rn = sum(x*y for x, y in zip(wn, cn)) + (b-.1*g) + (d-.1*g) - math.log(100)
        self.assertAlmostEqual(rn, .2)
        self.assertAlmostEqual(f*rn**2, .04)
        root = ET.parse(ASSETS / 'glove-simultaneous-gradient-motion.svg').getroot()
        self.assertEqual(len([e for e in root.iter(NS+'animate') if e.get('attributeName') == 'cx']), 4)
        self.assertIn('Loss 0.04', [e.text for e in root.iter(NS+'text')])

    def test_screening(self):
        distances = [.2, .45, .55, .8]
        self.assertEqual([i+1 for i, d in enumerate(distances) if .4 < d < .6], [2, 3])
        for d, loss in zip(distances, [.4, .15, .05, 0]):
            self.assertAlmostEqual(max(0, .6-d), loss)
        root = ET.parse(ASSETS / 'facenet-semi-hard-screening-motion.svg').getroot()
        motion = root.find('.//'+NS+'animateTransform')
        self.assertEqual(motion.get('values'), '164 205;164 205;294 205;346 205;476 205;476 205;164 205')
        self.assertIn('Eligible: N2, N3', [e.text for e in root.iter(NS+'text')])

    def test_assets(self):
        for stem in ['glove-simultaneous-gradient', 'facenet-semi-hard-screening']:
            for kind in ['motion', 'still']:
                path = ASSETS / f'{stem}-{kind}.svg'
                root = ET.parse(path).getroot()
                self.assertEqual(root.get('viewBox'), '0 0 640 360')
                self.assertLess(path.stat().st_size, 50000)
                self.assertIsNotNone(root.find(NS+'desc'))
                ids = [e.get('id') for e in root.iter() if e.get('id')]
                self.assertEqual(len(ids), len(set(ids)))
                motions = [e for e in root.iter() if e.tag in {NS+'animate', NS+'animateTransform'}]
                self.assertEqual(bool(motions), kind == 'motion')
                for e in motions:
                    self.assertEqual(e.get('dur'), '12s')
                    self.assertEqual(e.get('repeatCount'), 'indefinite')
                    times = [float(t) for t in e.get('keyTimes').split(';')]
                    self.assertEqual(times, sorted(times))
                    self.assertEqual((times[0], times[-1]), (0, 1))
                    self.assertEqual(len(times), len(e.get('values').split(';')))
                for e in root.iter():
                    self.assertNotIn(e.tag, {NS+'script', NS+'foreignObject', NS+'image'})
                    self.assertFalse(any(k.startswith('on') or k.endswith('href') for k in e.attrib))


if __name__ == '__main__':
    unittest.main()
