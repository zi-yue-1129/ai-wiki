"""Numerical/temporal checks read committed SVG animation values."""
import bisect,math,unittest,xml.etree.ElementTree as E
from functools import lru_cache
from pathlib import Path
R=Path(__file__).resolve().parents[1];A=R/'docs/assets/concept-animations';N='{http://www.w3.org/2000/svg}'
@lru_cache(None)
def parsed(a):
 vs=list(map(float,a.get('values').split(';')));ts=list(map(float,a.get('keyTimes',';'.join(str(i/(len(vs)-1)) for i in range(len(vs)))).split(';')));return ts,vs

def value(a,t):
 ts,vs=parsed(a)
 if t==1:return vs[-1]
 i=min(len(vs)-2,max(0,bisect.bisect_right(ts,t)-1))
 return vs[i] if a.get('calcMode')=='discrete' else vs[i]+(vs[i+1]-vs[i])*(t-ts[i])/(ts[i+1]-ts[i])
class SacDpoMotion(unittest.TestCase):
 def test_sac_geometry(self):
  r=E.parse(A/'sac-entropy-temperature-motion.svg').getroot();an=list(r.iter(N+'animate'))
  for i in range(10001):
   t=i/10000;a=1.25+.75*math.cos(2*math.pi*t);p=[math.exp((q-2)/a) for q in [2,1,0]];z=sum(p);p=[v/z for v in p];H=-sum(v*math.log(v) for v in p)
   for k,v in enumerate(p):
    self.assertAlmostEqual(value(an[2*k],t),194*v,delta=.025);self.assertAlmostEqual(value(an[2*k],t)+value(an[2*k+1],t),330,delta=.00001)
   self.assertAlmostEqual(value(an[-2],t),522+(a-.5)/1.5*184,delta=.025);self.assertAlmostEqual(value(an[-1],t),320-147.32*H,delta=.03)
 def test_dpo_geometry(self):
  r=E.parse(A/'dpo-preference-margin-motion.svg').getroot();an=list(r.iter(N+'animate'))
  for i in range(10001):
   t=i/10000;d=-1.6*math.cos(2*math.pi*t);p=1/(1+math.exp(-d))
   self.assertAlmostEqual(value(an[0],t),198*p,delta=.025);self.assertAlmostEqual(value(an[0],t)+value(an[1],t),198,delta=.00001)
   self.assertAlmostEqual(value(an[2],t),403+(d+1.6)/3.2*296,delta=.025);self.assertAlmostEqual(value(an[3],t),322-87*math.log1p(math.exp(-d)),delta=.03)
 def test_source_hooks_and_math_blocks(self):
  for folder in ['learning-from-human-feedback/dpo','policy-gradient-and-actor-critic/sac']:
   for lang in ['', '.zh-TW']:
    text=(R/'docs/theory/paradigms/reinforcement-learning'/folder/('index'+lang+'.md')).read_text()
    for token in ['data-source-asset-urls','data-still-src','concept-motion-scroll','tabindex="0"','min-width:760px']:self.assertIn(token,text)
    self.assertNotIn('class="concept-motion-wide"',text)
    self.assertEqual(text.count(r'\begin{aligned}'),text.count(r'\end{aligned}'))
if __name__=='__main__':unittest.main()
