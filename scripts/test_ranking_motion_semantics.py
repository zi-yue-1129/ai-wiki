"""Source-aware arithmetic and synchronized rank-reveal regression tests."""
from pathlib import Path
import math
import unittest
import xml.etree.ElementTree as E
N='{http://www.w3.org/2000/svg}';A=Path(__file__).resolve().parents[1]/'docs/assets/concept-animations'
def root(stem,kind='motion'):return E.parse(A/f'{stem}-{kind}.svg').getroot()
def vals(a):return list(map(float,a.get('values').split(';')))
class RankingMotion(unittest.TestCase):
    def test_ndcg(self):
        r=root('ndcg-position-discount');bars=[a for a in r.iter(N+'animate') if a.get('attributeName')=='width'];self.assertEqual(len(bars),12)
        scores=[]
        for side,rs in enumerate(([3,2,3,0,1,2],[3,3,2,2,1,0])):
            gains=[rel/math.log2(i+2) for i,rel in enumerate(rs)];scores.append(sum(gains))
            for rank,gain in enumerate(gains):
                a=bars[2*rank+side];v=vals(a)
                self.assertEqual(len(v),13)
                for i in range(6):
                    self.assertAlmostEqual(v[2*i],44*gain if i>rank else 0,delta=.0001)
                    self.assertAlmostEqual(v[2*i+1],44*gain if i>=rank else 0,delta=.0001)
                self.assertAlmostEqual(v[-1],44*gain,delta=.0001)
        self.assertEqual([f'{s:.3f}' for s in scores],['6.861','7.141'])
        self.assertEqual(f'{scores[0]/scores[1]:.3f}','0.961')
        for a in r.iter(N+'animate'):
            if a.get('attributeName')=='y':self.assertEqual(vals(a),[v for i in range(6) for v in (94+28*i,94+28*i)]+[234])
    def test_map(self):
        r=root('map-precision-at-hits');bars=[a for a in r.iter(N+'animate') if a.get('attributeName')=='width'];scores=[]
        for a,rs in zip(bars,([1,0,1,0,0,1],[0,1,1,0,1,0])):
            total=0;hits=0;v=vals(a)
            for i,rel in enumerate(rs):
                self.assertAlmostEqual(v[2*i],220*total,delta=.0001)
                hits+=rel;total+=rel*hits/(i+1)/3
                self.assertAlmostEqual(v[2*i+1],220*total,delta=.0001)
            self.assertAlmostEqual(v[-1],220*total,delta=.0001);scores.append(total)
        self.assertEqual([f'{s:.3f}' for s in scores],['0.722','0.589']);self.assertEqual(f'{sum(scores)/2:.3f}','0.656')
        for a in r.iter(N+'animate'):
            if a.get('attributeName')=='x':self.assertEqual(vals(a),[v for i in range(6) for v in (151+67*i,151+67*i)]+[486])
    def test_shared_clock_and_static(self):
        for stem in ('ndcg-position-discount','map-precision-at-hits'):
            r=root(stem);anims=list(r.iter(N+'animate'))
            self.assertEqual(len({a.get('keyTimes') for a in anims}),1)
            ts=list(map(float,anims[0].get('keyTimes').split(';')))
            self.assertEqual(ts[-2:],[.8,1.])
            self.assertFalse(list(root(stem,'still').iter(N+'animate')))
if __name__=='__main__':unittest.main()
