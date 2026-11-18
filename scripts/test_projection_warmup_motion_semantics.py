"""Preserve both distinct power-iteration examples and verify actual geometry."""
import math,bisect,unittest,xml.etree.ElementTree as E
from pathlib import Path
R=Path(__file__).resolve().parents[1];A=R/'docs/assets/concept-animations';N='{http://www.w3.org/2000/svg}'
def value(a,t):
 vs=list(map(float,a.get('values').split(';')));ts=list(map(float,a.get('keyTimes',';'.join(str(i/(len(vs)-1)) for i in range(len(vs)))).split(';')));i=min(len(vs)-2,max(0,bisect.bisect_right(ts,t)-1));return vs[i]+(vs[i+1]-vs[i])*(t-ts[i])/(ts[i+1]-ts[i])
class ProjectionWarmup(unittest.TestCase):
 def test_unit_vector_and_projections(self):
  r=E.parse(A/'power-iteration-projection-contraction-motion.svg').getroot();an=list(r.iter(N+'animate'));self.assertEqual(len(an),4);q=math.radians(28)
  for t in [i/10000 for i in range(10001)]:
   x=(value(an[0],t)-207)/124;y=(205-value(an[1],t))/124
   self.assertAlmostEqual(math.hypot(x,y),1,delta=.0002)
   self.assertAlmostEqual(value(an[2],t),146*abs(x*math.cos(q)+y*math.sin(q)),delta=.00002)
   self.assertAlmostEqual(value(an[3],t),146*abs(-x*math.sin(q)+y*math.cos(q)),delta=.00002)
  for k in range(8):
   t=k/14;x=(value(an[0],t)-207)/124;y=(205-value(an[1],t))/124
   ratio=(-x*math.sin(q)+y*math.cos(q))/(x*math.cos(q)+y*math.sin(q))
   self.assertAlmostEqual(ratio,math.tan(math.radians(-72))*(.45/1.6)**k,delta=.000001)
 def test_warmup(self):
  r=E.parse(A/'large-batch-warmup-ramp-motion.svg').getroot();an=list(r.iter(N+'animate'));self.assertEqual(len(an),6)
  for i in range(10001):
   t=i/10000;epoch=8*(1-abs(2*t-1));rate=.1+.3*min(epoch/5,1)
   for a in an:
    attr=a.get('attributeName');expected=68+43.5*epoch if attr in ('x1','x2','cx') else 278-355*rate if attr=='cy' else 134*rate/.4
    self.assertAlmostEqual(value(a,t),expected,delta=.00001)
 def test_warmup_still(self):
  r=E.parse(A/'large-batch-warmup-ramp-still.svg').getroot();dot=next(e for e in r.iter(N+'circle') if e.get('fill')=='#0b948e');epoch=(float(dot.get('cx'))-68)/43.5;rate=.1+.3*min(epoch/5,1)
  self.assertAlmostEqual(float(dot.get('cy')),278-355*rate,places=5)
  bar=next(e for e in r.iter(N+'rect') if e.get('fill')=='#0b948e');self.assertAlmostEqual(float(bar.get('width')),134*rate/.4,places=5)
 def test_bilingual_preservation(self):
  for lang in ['', '.zh-TW']:
   s=(R/f'docs/theory/math/linear-algebra/eigendecomposition{lang}.md').read_text()
   for stem in ['power-iteration-convergence','power-iteration-projection-contraction','eigen-linear-map','eigen-rotation-no-real','eigen-zero-eigenvalue','eigen-jordan-shear']:self.assertIn(stem,s)
   s=(R/f'docs/theory/optimization/gradual-warm-up{lang}.md').read_text();self.assertIn('\\hat\\eta = 0.1',s);self.assertIn('data-source-asset-urls',s)
if __name__=='__main__':unittest.main()
