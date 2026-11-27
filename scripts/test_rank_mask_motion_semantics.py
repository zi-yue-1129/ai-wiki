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
        import itertools
        kept = list(itertools.combinations(range(4), 2))
        errors = [[sum(w[i]*x[i] for i in range(4) if i not in k)**2 for x in xs] for k in kept]
        self.assertEqual(errors, [[100,0],[49,9],[81,9],[16,16],[36,16],[9,49]])
        cost = lambda p: [p*a+(1-p)*b for a,b in errors]
        for p, winner in [(0,0),(.1625,1),(.5,3),(1,5)]:
            self.assertEqual(min(range(6), key=lambda i:cost(p)[i]),winner)
        for p, i, j in [(.15,0,1),(.175,1,3),(.825,3,5)]:
            self.assertAlmostEqual(cost(p)[i],cost(p)[j])
            self.assertAlmostEqual(cost(p)[i],min(cost(p)))
        for suffix in ['motion','still']:
            root = ET.parse(ASSETS / f'matched-sparsity-output-error-{suffix}.svg').getroot()
            labels = [t.text for t in root.iter(NS+'text')]
            for label in ['Kept weights','Expected MSE','Minimum across masks','P(input 1)']:
                self.assertIn(label,labels)
            if suffix == 'still':
                for value in [50,29,45,16,26]:
                    self.assertIn(str(value),labels)
            else:
                bars = [a for a in root.iter(NS+'animate') if a.get('attributeName')=='width']
                self.assertEqual(len(bars),6)
                for i,a in enumerate(bars):
                    for q,v in zip([0,0,.15,.1625,.1625,.175,.5,.5,.825,1,1,1],map(float,a.get('values').split(';'))):
                        self.assertAlmostEqual(v,1.3*cost(q)[i],places=3)
        for p in [0,.1,.2,.5,1]:
            self.assertEqual(36*p < 9*(1-p), p < .2)

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
