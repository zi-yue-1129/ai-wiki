"""Independent arithmetic checks for the GloVe and FaceNet motion tracks."""
import math
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

ASSETS = Path(__file__).resolve().parents[1] / 'docs/assets/concept-animations'
if not ASSETS.is_dir():
    ASSETS = Path(__file__).resolve().parent
NS = '{http://www.w3.org/2000/svg}'


def tracks(stem):
    root = ET.parse(ASSETS / (stem + '-motion.svg')).getroot()
    return [list(map(float, a.attrib['values'].split(';'))) for a in root.iter(NS + 'animate')]


class EmbeddingMotion(unittest.TestCase):
    def test_glove(self):
        x1, x2, tx, ty, wx, wy = tracks('glove-count-weighting')
        self.assertEqual(x1, x2)
        self.assertEqual(x1, tx)
        self.assertEqual(tx, wx)
        self.assertEqual((min(tx), max(tx)), (64, 594))
        for x, y, w in zip(tx, ty, wy):
            u = (x - 64) / 530
            count = 0.5 * 800 ** u
            self.assertAlmostEqual(y, 146 - 72 * u, places=3)
            self.assertAlmostEqual(w, 292 - 88 * min(1, (count / 100) ** .75), places=3)
        self.assertEqual(wy[tx.index(594)], 204)

    def test_facenet(self):
        nx, ny, cx, cy, x1, x2, hx, hy = tracks('facenet-triplet-margin')
        self.assertEqual(nx, cx)
        self.assertEqual(ny, cy)
        self.assertEqual(x1, x2)
        self.assertEqual(x1, hx)
        for x, y, h, loss in zip(nx, ny, hx, hy):
            d = (h - 346) / 260
            self.assertAlmostEqual(((x-162)**2 + (y-191)**2)/10000, 1, places=5)
            self.assertAlmostEqual(((x-262)**2 + (y-191)**2)/10000, d, places=5)
            self.assertAlmostEqual(loss, 275-200*max(.6-d, 0), places=3)
        self.assertAlmostEqual(min(hx), 372)
        self.assertAlmostEqual(max(hx), 580)

    def test_assets(self):
        for stem in ('glove-count-weighting', 'facenet-triplet-margin'):
            for kind in ('motion', 'still'):
                path = ASSETS / (stem + '-' + kind + '.svg')
                root = ET.parse(path).getroot()
                self.assertEqual(root.get('viewBox'), '0 0 640 360')
                self.assertIsNotNone(root.find(NS + 'title'))
                self.assertIsNotNone(root.find(NS + 'desc'))
                self.assertLess(path.stat().st_size, 500000)
                nodes = list(root.iter(NS + 'animate'))
                self.assertEqual(bool(nodes), kind == 'motion')
                for node in nodes:
                    self.assertEqual(node.get('dur'), '12s')
                    self.assertEqual(node.get('repeatCount'), 'indefinite')
                    values = node.get('values').split(';')
                    self.assertEqual(values[0], values[-1])
                for node in root.iter():
                    self.assertNotIn(node.tag, [NS+'script', NS+'foreignObject', NS+'image'])
                    self.assertFalse(any(k.startswith('on') or k.endswith('href') for k in node.attrib))


if __name__ == '__main__':
    unittest.main()
