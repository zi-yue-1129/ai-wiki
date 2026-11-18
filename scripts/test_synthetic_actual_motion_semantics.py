"""Check animated rounding against actual markers, not just endpoint arithmetic."""
import bisect
import math
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'docs/assets/concept-animations'
NS='{http://www.w3.org/2000/svg}'

def read(stem,kind='motion'):return ET.parse(ASSETS/f'{stem}-{kind}.svg').getroot()

def at(e,attr,t):
    a=next((a for a in e.findall(NS+'animate') if a.get('attributeName')==attr),None)
    if a is None:return float(e.get(attr,'1' if attr=='opacity' else '0'))
    v=list(map(float,a.get('values').split(';')));k=list(map(float,a.get('keyTimes').split(';')))
    i=min(len(k)-1,max(0,bisect.bisect_right(k,t)-1))
    if a.get('calcMode')=='discrete' or i==len(k)-1:return v[i]
    q=(t-k[i])/(k[i+1]-k[i]);return v[i]*(1-q)+v[i+1]*q

class SyntheticSvgTests(unittest.TestCase):
    def test_discrete_generations_conserve_mass_and_extinct_support(self):
        r=read('recursive-tail-loss');bars=[e for e in r.iter(NS+'rect') if any(a.get('attributeName')=='height' for a in e.findall(NS+'animate'))]
        self.assertEqual(len(bars),6);previous=None
        for t,expected in zip([0,.3,.5,.7,.9],[(12,9,5,2,1,1),(8,16,3,2,1,0),(7,21,0,1,1,0),(9,20,0,1,0,0),(9,21,0,0,0,0)]):
            counts=[at(e,'height',t)/7.5 for e in bars];self.assertEqual(counts,list(expected));self.assertEqual(sum(counts),30)
            if previous:self.assertTrue(all(p>0 or n==0 for p,n in zip(previous,counts)))
            previous=counts
        for i in range(10001):
            t=i/10000
            self.assertAlmostEqual(sum(at(e,'height',t)/7.5 for e in bars),30)
            for e in bars:self.assertAlmostEqual(at(e,'y',t)+at(e,'height',t),274)
        for e in bars:self.assertEqual(at(e,'height',.9),at(e,'height',.999))
    def test_counter_only_claims_integer_sample_after_transition(self):
        r=read('recursive-tail-loss');labels=[e for e in r.iter(NS+'text') if e.get('y')=='145'];tail=[e for e in r.iter(NS+'text') if e.get('y')=='215']
        for t,want,number in [(0,'G0','2'),(.2,'Tween','—'),(.3,'G1','1'),(.4,'Tween','—'),(.5,'G2','1'),(.6,'Tween','—'),(.7,'G3','0'),(.8,'Tween','—'),(.9,'G4','0'),(.99,'G4','0')]:
            self.assertEqual([e.text for e in labels if at(e,'opacity',t)==1],[want])
            self.assertEqual([e.text for e in tail if at(e,'opacity',t)==1],[number])
    def test_accepted_token_arrives_before_pool_growth_and_never_leaves_pool(self):
        r=read('self-instruct-filter-loop');c=next(e for e in r.iter(NS+'circle') if e.get('fill')=='#0c938c');m=c.find(NS+'animateMotion')
        self.assertEqual(m.get('path'),'M270 145 H565 V245 H100 V180')
        self.assertEqual(m.get('keyPoints'),'0;0;1;1');self.assertEqual(m.get('keyTimes'),'0;0.1;0.8;1')
        pool=next(e for e in r.iter(NS+'rect') if e.get('y')=='176')
        self.assertEqual(at(pool,'opacity',.79),0);self.assertEqual(at(pool,'opacity',.85),1);self.assertEqual(at(pool,'opacity',.99),1)

if __name__=='__main__':unittest.main()
