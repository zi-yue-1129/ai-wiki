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

class WeightNormSvgTests(unittest.TestCase):
    def test_recurrence_vectors_and_trackers_share_actual_radius(self):
        r=read('rotational-norm-balance')
        for origin,color,a in [(165,'#087f82',.96),(475,'#c46a2b',1)]:
            line=next(e for e in r.iter(NS+'line') if e.get('stroke')==color and e.find(NS+'animate') is not None)
            tracker=next(e for e in r.iter(NS+'circle') if e.get('fill')==color and float(e.get('cy'))>270 and e.find(NS+'animate') is not None)
            rad=.3
            for n in range(25):
                t=.95*n/24
                actual=math.hypot(at(line,'x2',t)-origin,158-at(line,'y2',t))/80
                self.assertAlmostEqual(actual,rad,places=5)
                rad=math.hypot(a*rad,.17)
            for i in range(10001):
                t=i/10000;actual=math.hypot(at(line,'x2',t)-origin,158-at(line,'y2',t))/80
                self.assertLess(abs((334-at(tracker,'cy',t))/59-actual),.0006)
            self.assertAlmostEqual(at(tracker,'cx',1),610)
    def test_epoch_dots_follow_retention_not_path_arclength(self):
        r=read('adamw-epoch-timescale')
        self.assertFalse(any(a.get('attributeName')=='stroke-dashoffset' for a in r.iter(NS+'animate')))
        dots=[e for e in r.iter(NS+'circle') if e.find(NS+'animate') is not None]
        self.assertEqual(len(dots),4)
        for e in dots:
            x0=float(e.get('cx'));steps=8 if e.get('fill')=='#087f82' else 32
            lam=1/(.1*8*3) if x0==66 or steps==8 else 1/(.1*32*3)
            for i in range(1001):
                t=i/1000;epoch=6*min(t/.95,1);expected=288-177*(1-.1*lam)**(epoch*steps)
                self.assertLess(abs(at(e,'cy',t)-expected),.61)
                self.assertLess(abs(at(e,'cx',t)-(x0+220*epoch/6)),.006)
    def test_localized_hooks_and_caveats(self):
        for topic in ['rotational-equilibrium','adamw-weight-decay-scaling']:
            for lang in ['', '.zh-TW']:
                s=(ROOT/f'docs/theory/optimization/weight-norm-dynamics/{topic}{lang}.md').read_text()
                for token in ['data-source-asset-urls','data-still-src','role="region"','min-width:640px','e-folding']:
                    self.assertIn(token,s)

if __name__=='__main__':unittest.main()
