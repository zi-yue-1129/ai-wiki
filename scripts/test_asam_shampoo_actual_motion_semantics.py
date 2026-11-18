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

class AdaptiveGeometryTests(unittest.TestCase):
    def test_asam_support_point_matches_actual_gradient(self):
        r=read('asam-neighborhood');lines=[e for e in r.iter(NS+'line') if e.find(NS+'animate') is not None]
        for i in range(10001):
            t=i/10000
            for origin in [164,476]:
                same=[e for e in lines if float(e.get('x1'))==origin]
                ray=next(e for e in same if e.get('stroke-dasharray'))
                step=next(e for e in same if not e.get('stroke-dasharray'))
                gx,gy=at(ray,'x2',t)-origin,195-at(ray,'y2',t)
                if origin==164:den=math.hypot(gx,gy);ex,ey=62.4*gx/den,62.4*gy/den
                else:den=math.hypot(2*gx,gy);ex,ey=62.4*4*gx/den,62.4*gy/den
                self.assertLess(math.hypot(at(step,'x2',t)-origin-ex,195-at(step,'y2',t)-ey),.1)
    def test_shampoo_actual_spectral_bars_and_nonreversing_history(self):
        r=read('shampoo-eigenmode');bars=[e for e in r.iter(NS+'rect') if e.get('y') in ['280','305']]
        for e in bars:
            vals=list(map(float,e.find(NS+'animate').get('values').split(';')))
            self.assertTrue(all(x>=y for x,y in zip(vals,vals[1:])))
        for i in range(10001):
            t=i/10000;step=6*min(t/.9,1)**2
            for e in bars:
                expected=140*(3/math.sqrt(1+9*step) if e.get('y')=='280' else 1/math.sqrt(1+step))
                self.assertLess(abs(at(e,'width',t)-expected),.22)
        self.assertEqual(at(bars[0],'width',0),420)
    def test_zero_coordinate_and_rank_caveats_bilingual(self):
        for lang in ['', '.zh-TW']:
            for topic in ['asam','shampoo']:
                s=(ROOT/f'docs/theory/optimization/{topic}{lang}.md').read_text()
                for token in ['data-source-asset-urls', 'overflow-x:auto', 'tabindex="0"']:
                    self.assertIn(token,s)
            s=(ROOT/f'docs/theory/optimization/shampoo{lang}.md').read_text();self.assertIn('-1/(2k)',s)

if __name__=='__main__':unittest.main()
