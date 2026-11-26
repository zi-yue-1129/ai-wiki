"""Check the teaching traces against independent exact arithmetic."""
from fractions import Fraction as F
from pathlib import Path
from xml.etree import ElementTree as ET
import unittest

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'docs/assets/concept-animations'
NS = '{http://www.w3.org/2000/svg}'


def svg(stem, kind):
    return ET.parse(ASSETS / f'{stem}-{kind}.svg').getroot()


def texts(root):
    return [node.text for node in root.iter(NS + 'text')]


class BinaryTernarySemantics(unittest.TestCase):
    def test_binary_latent_accumulation(self):
        w = F(-3, 5)
        weights = [w]
        for _ in range(4):
            w = max(F(-1), min(F(1), w + F(1, 5)))
            weights.append(w)
        still = svg('binaryconnect-latent-accumulation', 'still')
        moving = svg('binaryconnect-latent-accumulation', 'motion')
        labels = texts(still)
        self.assertEqual([x for x in labels if x in ('−1', '+1')],
                         ['−1' if w < 0 else '+1' for w in weights])
        for i, w in enumerate(weights):
            self.assertIn(f'{float(w):.1f}', labels)
            if i:
                segment = next(e for e in moving.iter() if e.get('id') == f'update-{i}')
                anims = {e.get('attributeName'): e for e in segment.iter(NS + 'animate')}
                self.assertEqual(F(anims['y2'].get('values').split(';')[-1]), 145 - 100*w)
                self.assertEqual(F(anims['x2'].get('values').split(';')[-1]), 150 + 100*i)

    def test_ternary_threshold_and_scale(self):
        w = [F(-1), F(-1, 5), F(2, 5), F(4, 5)]
        delta = F(7, 10) * sum(map(abs, w)) / len(w)
        code = [int(v > 0)-int(v < 0) if abs(v) > delta else 0 for v in w]
        alpha = sum(v*t for v, t in zip(w, code))/sum(t*t for t in code)
        error = sum((v-alpha*t)**2 for v, t in zip(w, code))
        self.assertEqual((delta, alpha, error), (F(21, 50), F(9, 10), F(11, 50)))
        still = svg('twn-threshold-scale', 'still')
        labels = texts(still)
        self.assertEqual([x for x in labels if x in ('−1', '+1', '−0.9', '+0.9', '0')],
                         ['−1', '−0.9', '0', '0', '0', '0', '+1', '+0.9'])
        self.assertIn('0.42', labels)
        self.assertIn('SSE = 0.22', labels[-1])
        moving = svg('twn-threshold-scale', 'motion')
        band = next(e for e in moving.iter() if e.get('id') == 'threshold-band')
        anims = {e.get('attributeName'): e for e in band.iter(NS + 'animate')}
        self.assertEqual(F(anims['height'].get('values').split(';')[-1]), 100*delta)
        self.assertEqual(F(anims['y'].get('values').split(';')[-1]), 200-100*delta)


if __name__ == '__main__':
    unittest.main()
