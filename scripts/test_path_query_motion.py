"""Exact teaching arithmetic and completed-state SVG labels."""
import itertools
import math
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET

ASSETS = Path(__file__).resolve().parents[1] / 'docs/assets/concept-animations'
if not ASSETS.is_dir():
    ASSETS = Path(__file__).resolve().parent  # isolated asset QA
NS = {'s': 'http://www.w3.org/2000/svg'}


class PathQueryMotionTests(unittest.TestCase):
    def root(self, stem, mode='still'):
        return ET.parse(ASSETS / f'{stem}-{mode}.svg').getroot()

    def test_path_sums(self):
        paths = [(3+a, 3+a+b) for a,b in itertools.product((-1,1), repeat=2)]
        self.assertEqual(paths, [(2,1),(2,3),(4,3),(4,5)])
        self.assertEqual([sum(p) for p in paths], [3,5,7,9])
        labels = [e.text for e in self.root('deepar-path-sums').findall('.//s:text', NS)]
        for a,b in paths:
            self.assertIn(f'{a} + {b} = {a+b}', labels)
        self.assertIn('Each path: 25%', labels)
        self.assertEqual(sum((a-3)*(b-3) for a,b in paths)/4, 1)

    def test_query_selection(self):
        rows = [[1,1,1,1],[1,1,1,9],[2,1,1,1]]
        values = [0,4,8,12]
        scores = [math.log(max(w))-sum(map(math.log,w))/len(w) for w in rows]
        selected = max(range(len(rows)), key=scores.__getitem__)
        self.assertEqual(selected, 1)
        full = [sum(w*v for w,v in zip(row,values))/sum(row) for row in rows]
        self.assertEqual(full, [6,10,4.8])
        sparse = [full[i] if i==selected else sum(values)/len(values) for i in range(len(rows))]
        self.assertEqual(sparse, [6,10,6])
        labels = { (e.get('x'),e.get('y')):e.text for e in self.root('informer-probsparse-query').findall('.//s:text',NS) }
        for i,y in enumerate((119,186,253)):
            self.assertEqual(labels['423',str(y)], f'{scores[i]:.2f}')
            self.assertEqual(labels['554',str(y)], str(int(sparse[i])))

    def test_asset_contracts(self):
        for stem in ('deepar-path-sums','informer-probsparse-query'):
            for mode in ('motion','still'):
                root=self.root(stem,mode)
                self.assertEqual(root.get('viewBox'),'0 0 640 360')
                self.assertIsNotNone(root.find('s:title',NS))
                self.assertIsNotNone(root.find('s:desc',NS))
                tracks=root.findall('.//s:animate',NS)
                self.assertEqual(bool(tracks),mode=='motion')
                for a in tracks:
                    self.assertEqual(a.get('dur'),'12s')
                    self.assertEqual(a.get('repeatCount'),'indefinite')
                    times=list(map(float,a.get('keyTimes').split(';')))
                    self.assertEqual(len(times),len(a.get('values').split(';')))
                    self.assertEqual((times[0],times[-1]),(0,1))
                    self.assertEqual(times,sorted(set(times)))
                for e in root.iter():
                    self.assertNotIn(e.tag.split('}')[-1],{'script','foreignObject','image','iframe'})
                    self.assertFalse(any(k.startswith('on') or k.endswith('href') for k in e.attrib))


if __name__=='__main__':
    unittest.main()
