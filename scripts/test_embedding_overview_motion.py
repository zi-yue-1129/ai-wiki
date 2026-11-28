"""Check the constructed embedding examples against the committed SVG tracks."""
import math
from pathlib import Path
import unittest
from xml.etree import ElementTree as ET

ASSETS = Path(__file__).resolve().parents[1] / 'docs/assets/concept-animations'
NS = '{http://www.w3.org/2000/svg}'


class EmbeddingOverviewMotion(unittest.TestCase):
    def test_norm_ranking(self):
        root = ET.parse(ASSETS / 'embedding-norm-ranking-motion.svg').getroot()
        tracks = {e.get('attributeName'): [float(v) for v in e.get('values').split(';')]
                  for e in root.iter(NS+'animate')}
        for i, r in enumerate([.5, .5, 1.5, 1.5, .5]):
            a = (.8*r, .6*r)
            self.assertAlmostEqual(a[0]/math.hypot(*a), .8)
            self.assertAlmostEqual(tracks['x2'][i], 48+150*a[0])
            self.assertAlmostEqual(tracks['y2'][i], 262-150*a[1])
            self.assertAlmostEqual(tracks['width'][i], 150*a[0])
        self.assertAlmostEqual(.8*.75, .6)
        self.assertLess(.8*.5, .6)
        self.assertGreater(.8*1.5, .6)

    def test_lookup_accumulation(self):
        root = ET.parse(ASSETS / 'embedding-lookup-accumulation-motion.svg').getroot()
        groups = root.find(NS+'g[@class="motion"]').findall(NS+'g')
        rows = [[0, 0] for _ in range(3)]
        fmt = lambda row: '(' + ', '.join(str(v).replace('-', '−') for v in row) + ')'
        for k, group in enumerate(groups[:4]):
            self.assertEqual([e.text for e in group.findall(NS+'text')], list(map(fmt, rows)))
            if k < 3:
                j, g = [(2, (1, 2)), (0, (3, -1)), (2, (-2, 1))][k]
                rows[j] = [a+b for a, b in zip(rows[j], g)]
                circle = groups[4+k].find(NS+'circle')
                y = circle.find(NS+'animate[@attributeName="cy"]').get('values').split(';')
                self.assertEqual(float(y[2]), 121+70*j)
        self.assertEqual(rows, [[3, -1], [0, 0], [-1, 3]])
        still = ET.parse(ASSETS / 'embedding-lookup-accumulation-still.svg').getroot()
        self.assertEqual([e.text for e in still.findall(NS+'text')][-3:], list(map(fmt, rows)))

    def test_assets(self):
        for stem in ('embedding-norm-ranking', 'embedding-lookup-accumulation'):
            for kind in ('motion', 'still'):
                path = ASSETS / f'{stem}-{kind}.svg'
                root = ET.parse(path).getroot()
                self.assertEqual(root.get('viewBox'), '0 0 640 360')
                self.assertIsNotNone(root.find(NS+'desc'))
                self.assertLess(path.stat().st_size, 50000)
                ids = [e.get('id') for e in root.iter() if e.get('id')]
                self.assertEqual(len(ids), len(set(ids)))
                tracks = list(root.iter(NS+'animate'))
                self.assertEqual(bool(tracks), kind == 'motion')
                for e in tracks:
                    times = list(map(float, e.get('keyTimes').split(';')))
                    self.assertEqual((times[0], times[-1]), (0, 1))
                    self.assertEqual(times, sorted(times))
                    self.assertEqual(len(times), len(e.get('values').split(';')))
                    self.assertEqual(e.get('repeatCount'), 'indefinite')
                    self.assertEqual(e.get('dur'), '12s')
                for e in root.iter():
                    self.assertNotIn(e.tag, {NS+'script', NS+'foreignObject', NS+'image'})
                    self.assertFalse(any(k.startswith('on') or k.endswith('href') for k in e.attrib))


if __name__ == '__main__':
    unittest.main()
