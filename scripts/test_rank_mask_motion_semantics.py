import unittest
from pathlib import Path
from xml.etree import ElementTree as ET

HERE = Path(__file__).resolve().parent
ASSETS = HERE if (HERE / 'svd-factor-rank-budget-motion.svg').exists() else HERE.parent / 'docs/assets/concept-animations'
NS = '{http://www.w3.org/2000/svg}'

class RankMask(unittest.TestCase):
    def test_rank_budget(self):
        sigma = [6, 3, 1, .5]
        for r, error in enumerate([10.25, 1.25, .25], 1):
            self.assertEqual(sum(v*v for v in sigma[r:]), error)
            self.assertEqual(8*r < 16, r == 1)
        for suffix in ['motion', 'still']:
            root = ET.parse(ASSETS / f'svd-factor-rank-budget-{suffix}.svg').getroot()
            labels = [t.text for t in root.iter(NS+'text')]
            for label in ['8 / 16', '16 / 16', '24 / 16', '10.25', '1.25', '0.25']:
                self.assertIn(label, labels)

    def test_matched_sparsity(self):
        w = [4, 3, 2, 1]
        masks = [[1,1,1,1], [1,1,0,0], [0,0,1,1]]
        xs = [[0,1,3,4], [1,1,0,0]]
        ys = [[sum(a*b*c for a,b,c in zip(w,x,m)) for m in masks] for x in xs]
        self.assertEqual(ys, [[13,3,10], [7,7,0]])
        self.assertEqual([sum((y[0]-y[j])**2 for y in ys)/2 for j in [1,2]], [50,29])
        self.assertEqual(sum(masks[1]), sum(masks[2]))
        for suffix in ['motion', 'still']:
            root = ET.parse(ASSETS / f'matched-sparsity-output-error-{suffix}.svg').getroot()
            labels = [t.text for t in root.iter(NS+'text')]
            self.assertIn('Magnitude: 50', labels)
            self.assertIn('Alternate: 29', labels)
        root = ET.parse(ASSETS / 'matched-sparsity-output-error-motion.svg').getroot()
        widths = [a.get('values') for a in root.iter(NS+'animate') if a.get('attributeName')=='width']
        self.assertIn('0;0;0;42;126;182;182;0', widths)

    def test_asset_contracts(self):
        for stem in ['svd-factor-rank-budget', 'matched-sparsity-output-error']:
            for suffix in ['motion', 'still']:
                root = ET.parse(ASSETS / f'{stem}-{suffix}.svg').getroot()
                self.assertEqual(root.get('viewBox'), '0 0 640 360')
                self.assertIsNotNone(root.find(NS+'title'))
                self.assertIsNotNone(root.find(NS+'desc'))
                anims = list(root.iter(NS+'animate'))
                self.assertEqual(bool(anims), suffix=='motion')
                for a in anims:
                    self.assertEqual(a.get('repeatCount'), 'indefinite')
                    self.assertEqual(a.get('dur'), '12s')
                    times = list(map(float,a.get('keyTimes').split(';')))
                    self.assertEqual(times, sorted(times))
                    self.assertEqual(len(times), len(a.get('values').split(';')))
                for e in root.iter():
                    self.assertNotIn(e.tag.split('}')[-1], ['script','foreignObject','image'])
                    self.assertFalse(any(k.startswith('on') or k.endswith('href') for k in e.attrib))

if __name__ == '__main__':
    unittest.main()
