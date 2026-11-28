"""Check the original wav2vec visual examples and their animation structure."""
from itertools import product
from pathlib import Path
import unittest
from xml.etree import ElementTree as ET

ASSETS = Path(__file__).resolve().parents[1] / 'docs/assets/concept-animations'
if not ASSETS.is_dir():
    ASSETS = Path(__file__).resolve().parent
NS = '{http://www.w3.org/2000/svg}'
STEMS = ('wav2vec-mask-target', 'wav2vec-product-quantization')


def root(stem, kind='still'):
    return ET.parse(ASSETS / f'{stem}-{kind}.svg').getroot()


def text_at(node, x, y):
    return next(e.text for e in node.iter(NS+'text') if e.get('x') == str(x) and e.get('y') == str(y))


class Wav2vecMotion(unittest.TestCase):
    def test_mask_routing(self):
        node = root(STEMS[0])
        latents = [f'z{i}' for i in range(1, 5)]
        masked = [v if i not in (1, 2) else 'M' for i, v in enumerate(latents)]
        self.assertEqual([text_at(node, 53+40*i, 187) for i in range(4)], latents)
        self.assertEqual([text_at(node, 259+40*i, 119) for i in range(4)], masked)
        self.assertEqual([text_at(node, 259+40*i, 255) for i in range(4)], latents)
        self.assertEqual(text_at(node, 531, 120), 'c2')
        self.assertEqual(text_at(node, 531, 256), 'q2')

    def test_product_quantization(self):
        node = root(STEMS[1])
        groups = [[(0, 1), (1, 0), (-1, 0)], [(1, 1), (0, 1), (0, 2)]]
        tuples = {a+b for a, b in product(*groups)}
        self.assertEqual(len(tuples), 9)
        self.assertIn(groups[0][1]+groups[1][2], tuples)
        self.assertEqual(text_at(node, 319, 122), '[1, 0]')
        self.assertEqual(text_at(node, 319, 260), '[0, 2]')
        self.assertEqual(text_at(node, 461, 185), '1, 0')
        self.assertEqual(text_at(node, 549, 185), '0, 2')
        self.assertEqual(text_at(node, 320, 326), '3 × 3 = 9 possible tuples')

    def test_assets(self):
        for stem in STEMS:
            for kind in ('motion', 'still'):
                node = root(stem, kind)
                self.assertEqual(node.get('viewBox'), '0 0 640 360')
                self.assertTrue(node.find(NS+'desc').text)
                ids = [e.get('id') for e in node.iter() if e.get('id')]
                self.assertEqual(len(ids), len(set(ids)))
                self.assertFalse(any(e.tag in (NS+'script', NS+'image', NS+'foreignObject') for e in node.iter()))
                self.assertFalse(any('href' in k or k.lower().startswith('on') for e in node.iter() for k in e.attrib))
                animations = [e for e in node.iter() if e.tag in (NS+'animate', NS+'animateMotion')]
                self.assertEqual(bool(animations), kind == 'motion')
                for e in animations:
                    self.assertEqual(e.get('repeatCount'), 'indefinite')
                    self.assertEqual(e.get('dur'), '12s')
                    ts = list(map(float, e.get('keyTimes').split(';')))
                    self.assertEqual((ts[0], ts[-1]), (0, 1))
                    self.assertTrue(all(a < b for a, b in zip(ts, ts[1:])))


if __name__ == '__main__':
    unittest.main()
