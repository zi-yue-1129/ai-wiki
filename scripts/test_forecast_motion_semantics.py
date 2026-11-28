import unittest
from pathlib import Path
from xml.etree import ElementTree as ET

ASSETS = Path(__file__).resolve().parents[1] / 'docs/assets/concept-animations'
NS = {'s': 'http://www.w3.org/2000/svg'}

class ForecastMotionTests(unittest.TestCase):
    def root(self, stem, mode='motion'):
        return ET.parse(ASSETS / f'{stem}-{mode}.svg').getroot()

    def test_rolling_origins(self):
        values = [2, 4, 3, 5, 6, 4, 7, 8]
        maes = []
        root = self.root('rolling-origin-forecast-evaluation')
        phases = root.findall('s:g', NS)
        self.assertEqual(len(phases), 6)
        for i, phase in enumerate(phases):
            origin, score = 4 + i // 2, bool(i % 2)
            self.assertEqual(len(phase.findall('s:polyline', NS)[0].get('points').split()), origin)
            labels = [t.text for t in phase.findall('s:text', NS)]
            errors = [abs(v - values[origin-1]) for v in values[origin:origin+2]]
            expected = [f'|e|={e}' for e in errors] if score else []
            self.assertEqual([t for t in labels if t.startswith('|e|=')], expected)
            self.assertEqual(len([t for t in labels if t.startswith('MAE ')]), origin-4+int(score))
            if score:
                maes.append(sum(errors)/2)
            a = phase.find('s:animate', NS)
            self.assertEqual(a.get('calcMode'), 'discrete')
            self.assertEqual([int(v) for v in a.get('values').split(';')], [int(j%6==i) for j in range(7)])
        self.assertEqual(maes, [1, 1.5, 3.5])
        self.assertEqual(sum(maes)/3, 2)

    def test_nbeats_residuals(self):
        for mode in ('motion', 'still'):
            root = self.root('nbeats-double-residual', mode)
            def vector(row, col):
                group = root.find(f'.//*[@id="b{row}-c{col}"]')
                return [int(r.get('data-value')) for r in group.findall('s:rect', NS)]
            r1, r2 = [vector(row, 2) for row in (1, 2)]
            for row in (1, 2):
                self.assertEqual(vector(row, 2), [a-b for a,b in zip(vector(row, 0), vector(row, 1))])
            self.assertEqual(vector(2, 0), r1)
            self.assertEqual(r2, [0, 0, 0, 0])
            self.assertEqual(vector(1, 4), vector(1, 3))
            self.assertEqual(vector(2, 4), [a+b for a,b in zip(vector(1, 4), vector(2, 3))])
            self.assertEqual(vector(2, 4), [7, 5])

    def test_asset_safety(self):
        for stem in ('rolling-origin-forecast-evaluation', 'nbeats-double-residual'):
            for mode in ('motion', 'still'):
                root = self.root(stem, mode)
                self.assertEqual(root.get('viewBox'), '0 0 640 360')
                self.assertIsNotNone(root.find('s:title', NS))
                self.assertIsNotNone(root.find('s:desc', NS))
                motions = [e for e in root.iter() if e.tag.split('}')[-1].startswith('animate')]
                self.assertEqual(bool(motions), mode == 'motion')
                for e in motions:
                    self.assertEqual(e.get('dur'), '12s')
                    self.assertEqual(e.get('repeatCount'), 'indefinite')
                for e in root.iter():
                    self.assertNotIn(e.tag.split('}')[-1], {'script', 'foreignObject', 'image', 'iframe'})
                    self.assertFalse(any(k.startswith('on') or k.endswith('href') for k in e.attrib))

if __name__ == '__main__':
    unittest.main()
