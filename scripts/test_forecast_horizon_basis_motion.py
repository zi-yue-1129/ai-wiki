"""Check the displayed arithmetic and synchronized SMIL tracks of the toy examples."""
import math
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET

ASSETS = Path(__file__).resolve().parents[1] / 'docs/assets/concept-animations'
NS = {'s': 'http://www.w3.org/2000/svg'}


class HorizonBasisTests(unittest.TestCase):
    def root(self, stem, mode='motion'):
        return ET.parse(ASSETS / f'{stem}-{mode}.svg').getroot()

    def test_horizon_aggregation(self):
        y = [2, 4, 3, 5, 6, 4, 7, 8]
        errors = [[abs(y[t+h-1] - y[t-1]) for h in (1, 2)] for t in (4, 5, 6)]
        self.assertEqual(errors, [[1, 1], [2, 1], [3, 4]])
        root = self.root('forecast-horizon-error')
        rows = root.findall('s:g', NS)[:3]
        for i, row in enumerate(rows):
            self.assertEqual([int(e.text) for e in row.findall('s:text', NS)], errors[i])
            self.assertEqual(row.find('s:animate', NS).get('values'), ';'.join(str(int(i < j < 4)) for j in range(5)))
        tracks = [a for a in root.findall('.//s:animate', NS) if a.get('attributeName') == 'width']
        for h, a in enumerate(tracks):
            sums = [sum(row[h] ** 2 for row in errors[:k]) for k in range(4)] + [0]
            self.assertEqual([float(v) for v in a.get('values').split(';')], [11.5*v for v in sums])
            self.assertEqual(a.get('calcMode'), 'discrete')
        labels = [e.text for e in self.root('forecast-horizon-error', 'still').findall('.//s:text', NS)]
        for h in range(2):
            self.assertIn(f'{sum(row[h] for row in errors)/3:.2f}', labels)
            self.assertIn(f'{math.sqrt(sum(row[h]**2 for row in errors)/3):.2f}', labels)
        self.assertEqual(len(tracks), 2)

    def test_polynomial_basis(self):
        root = self.root('nbeats-basis-expansion')
        lines = [e for e in root.findall('s:line', NS) if e.findall('s:animate', NS)]
        self.assertEqual(len(lines), 2)
        a = [1, -1, 0, 1, 1]
        for line, baseline, intercept in zip(lines, (245, 288), (0, 2)):
            for attr, t in (('y1', -1), ('y2', 1)):
                track = line.find(f's:animate[@attributeName="{attr}"]', NS)
                self.assertEqual([float(v) for v in track.get('values').split(';')], [baseline-43*(intercept+c*t) for c in a])
                self.assertEqual(float(line.get(attr)), baseline-43*(intercept+a[0]*t))
        cursor = root.find('.//s:animate[@attributeName="cx"]', NS)
        self.assertEqual([float(v) for v in cursor.get('values').split(';')], [125+(c+1)*72.5 for c in a])

    def test_assets(self):
        for stem in ('forecast-horizon-error', 'nbeats-basis-expansion'):
            for mode in ('motion', 'still'):
                root = self.root(stem, mode)
                self.assertEqual(root.get('viewBox'), '0 0 640 360')
                self.assertIsNotNone(root.find('s:title', NS))
                self.assertIsNotNone(root.find('s:desc', NS))
                tracks = root.findall('.//s:animate', NS)
                self.assertEqual(bool(tracks), mode == 'motion')
                for a in tracks:
                    self.assertEqual(a.get('dur'), '12s')
                    self.assertEqual(a.get('repeatCount'), 'indefinite')
                    self.assertEqual(a.get('keyTimes'), '0;0.25;0.5;0.75;1')
                for e in root.iter():
                    self.assertNotIn(e.tag.split('}')[-1], {'script', 'foreignObject', 'image', 'iframe'})
                    self.assertFalse(any(k.startswith('on') or k.endswith('href') for k in e.attrib))


if __name__ == '__main__':
    unittest.main()
