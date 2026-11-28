"""Regression checks for the constructed CLIP examples and displayed values."""
import math
from pathlib import Path
import unittest
from xml.etree import ElementTree as ET

ASSETS = Path(__file__).resolve().parents[1] / 'docs/assets/concept-animations'
NS = '{http://www.w3.org/2000/svg}'


def load(stem, kind='motion'):
    return ET.parse(ASSETS / f'clip-{stem}-{kind}.svg').getroot()


def softmax(values):
    weights = [math.exp(v) for v in values]
    return [v / sum(weights) for v in weights]


class CLIPMotion(unittest.TestCase):
    def test_directions(self):
        rows = [[2, 0], [1.2, 1.6]]
        rp = [softmax(r) for r in rows]
        cp = [softmax(c) for c in zip(*rows)]
        root = load('bidirectional-softmax')
        for p, matrix in [(1, rp), (2, list(zip(*cp)))]:
            for k in range(4):
                g = root.find(f'.//{NS}g[@id="p{p}-{k}"]')
                self.assertEqual(g.find(f'{NS}text').text, f'{matrix[k//2][k%2]:.3f}')
                t = (k//2+1)/6 if p == 1 else (k%2+3)/6
                self.assertAlmostEqual(float(g.find(f'{NS}animate').get('keyTimes').split(';')[1]), t, places=6)
        loss = [-sum(math.log(p[i][i]) for i in range(2))/2 for p in (rp, cp)]
        g = root.find(f'.//{NS}g[@id="losses"]')
        self.assertEqual([t.text for t in g.findall(f'{NS}text')], [f'{v:.4f}' for v in (*loss, sum(loss)/2)])

    def test_candidate_set(self):
        before, after = softmax([2, 0]) + [0], softmax([2, 0, 2])
        root = load('candidate-set')
        for i, (a, b) in enumerate(zip(before, after)):
            bar = root.find(f'.//{NS}rect[@id="bar-{i}"]')
            motion = bar.find(f'{NS}animate')
            self.assertEqual(motion.get('calcMode'), 'discrete')
            self.assertEqual(motion.get('keyTimes'), '0;0.416667;1')
            for actual, expected in zip(map(float, motion.get('values').split(';')), (350*a, 350*b, 350*a)):
                self.assertAlmostEqual(actual, expected, delta=0.001)
        self.assertAlmostEqual(after[0] / after[1], before[0] / before[1])

    def test_assets(self):
        for stem in ('bidirectional-softmax', 'candidate-set'):
            for kind in ('motion', 'still'):
                root = load(stem, kind)
                self.assertEqual(root.get('viewBox'), '0 0 640 360')
                self.assertTrue(root.find(f'{NS}title').text)
                self.assertTrue(root.find(f'{NS}desc').text)
                animations = list(root.iter(f'{NS}animate'))
                self.assertEqual(bool(animations), kind == 'motion')
                for a in animations:
                    self.assertEqual(a.get('dur'), '12s')
                    self.assertEqual(a.get('repeatCount'), 'indefinite')
                    self.assertEqual(len(a.get('keyTimes').split(';')), len(a.get('values').split(';')))
                for element in root.iter():
                    self.assertNotIn(element.tag, {NS+'script', NS+'foreignObject', NS+'image'})
                    self.assertFalse(any('href' in k or k.startswith('on') for k in element.attrib))


if __name__ == '__main__':
    unittest.main()
