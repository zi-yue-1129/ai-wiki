"""Independent actual-SVG tangent, derivative and clipped-area checks."""
import math,re,unittest,xml.etree.ElementTree as E
from functools import lru_cache
from pathlib import Path
R=Path(__file__).resolve().parents[1];N='{http://www.w3.org/2000/svg}'
@lru_cache(None)
def values(a):return list(map(float,a.get('values').split(';')))
def value(a,t):
 v=values(a);x=t*(len(v)-1);i=min(int(x),len(v)-2);u=x-i;return v[i]*(1-u)+v[i+1]*u
def attr(el,name,t):
 a=next((a for a in el.findall(N+'animate') if a.get('attributeName')==name),None);return value(a,t) if a is not None else float(el.get(name))
def root(stem,kind='motion'):return E.parse(R/f'docs/assets/concept-animations/{stem}-{kind}.svg').getroot()
class Interpretation(unittest.TestCase):
 def test_actual_score_derivative_and_tangent_at_10001_times(self):
  for stem in ['saliency-local-gradient','integrated-gradients-path']:
   r=root(stem);cs=[c for c in r.iter(N+'circle') if c.get('r')=='6.5'];left,right=cs
   tangent=next((e for e in r.iter(N+'line') if e.get('stroke-width')=='3.5'),None)
   for i in range(10001):
    t=i/10000;x=(attr(left,'cx',t)-70)/207;f=1-math.exp(-4*x);g=4*math.exp(-4*x)
    self.assertAlmostEqual((262-attr(left,'cy',t))/126,f,delta=5.1e-5)
    self.assertAlmostEqual((attr(right,'cx',t)-365)/213,x,delta=5e-7)
    self.assertAlmostEqual((262-attr(right,'cy',t))/31.5,g,delta=2.1e-4)
    if tangent is not None:
     x1,x2,y1,y2=[attr(tangent,a,t) for a in ['x1','x2','y1','y2']]
     self.assertAlmostEqual(-(y2-y1)/(x2-x1)*207/126,g,delta=2.1e-4)
     self.assertAlmostEqual((x1+x2)/2,attr(left,'cx',t),delta=.0001);self.assertAlmostEqual((y1+y2)/2,attr(left,'cy',t),delta=.0001)
   if stem.startswith('integrated'):self.assertEqual(attr(left,'cx',0),70);self.assertEqual(attr(left,'cx',.5),277)
 def test_actual_gradient_area_and_completeness(self):
  r=root('integrated-gradients-path');area=next(p for p in r.iter(N+'path') if p.get('fill')=='#008d88');pts=list(map(float,re.findall(r'-?\d+(?:\.\d+)?',area.get('d'))));xy=list(zip(pts[::2],pts[1::2]))[1:-1]
  pref=[0.]
  for (x0,y0),(x1,y1) in zip(xy,xy[1:]):pref.append(pref[-1]+(x1-x0)*(524-y0-y1)/2)
  clip=r.find('.//'+N+'clipPath/'+N+'rect');left=next(c for c in r.iter(N+'circle') if c.get('r')=='6.5')
  for i in range(10001):
   t=i/10000;x=(attr(left,'cx',t)-70)/207;w=attr(clip,'width',t);self.assertAlmostEqual(w/213,x,delta=5e-7)
   z=min(400,max(0,w/213*400));j=min(int(z),399);f=z-j;px,py=xy[j];qx,qy=xy[j+1];endx=px+(qx-px)*f;endy=py+(qy-py)*f
   integrated=(pref[j]+(endx-px)*(524-py-endy)/2)/(213*31.5)
   self.assertAlmostEqual(integrated,1-math.exp(-4*x),delta=9e-6)
  self.assertAlmostEqual(pref[-1]/(213*31.5),1-math.exp(-4),delta=9e-6)
  self.assertAlmostEqual(4*math.exp(-4),.0732625556,places=9)
 def test_source_readability_and_baseline_disclosure(self):
  for name in ['saliency-maps','integrated-gradients']:
   for lang in ['', '.zh-TW']:
    s=(R/f'docs/society/interpretability/{name}{lang}.md').read_text()
    for mark in ['data-source-asset-urls','data-motion-src','data-still-src','min-width:640px','overflow-x:auto','tabindex="0"']:self.assertIn(mark,s)
    self.assertIn('方向鍵' if lang else 'arrow keys',s)
    if name=='integrated-gradients':self.assertIn('基準 0' if lang else 'baseline 0',s)
if __name__=='__main__':unittest.main()
