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
class ContrastiveAlignmentMotion(unittest.TestCase):
 def test_simclr_temperature_geometry(self):
  r=E.parse(A/'simclr-temperature-competition-motion.svg').getroot();an=list(r.iter(N+'animate'));self.assertEqual(len(an),6)
  for i in range(10001):
   t=i/10000;tau=.6+.4*math.cos(2*math.pi*t);p=[math.exp((s-.8)/tau) for s in [.8,.4,.1,-.2,-.4]];z=sum(p);p=[v/z for v in p]
   for a,v in zip(an,p):self.assertAlmostEqual(value(a,t),240*v,delta=.025)
   self.assertAlmostEqual(sum(value(a,t) for a in an[:5]),240,delta=.00003)
   self.assertAlmostEqual(value(an[-1],t),320+238*(1-math.cos(2*math.pi*t))/2,delta=.015)
 def test_alignment_and_highlight(self):
  r=E.parse(A/'bahdanau-alignment-context-motion.svg').getroot();bars=[e for e in r.iter(N+'rect') if e.get('opacity')=='0.9'];lines=[e for e in r.iter(N+'line') if e.get('opacity')=='0.6'];box=next(e for e in r.iter(N+'rect') if e.get('y')=='305' and e.get('stroke')=='#d48647');x,opacity=list(box)
  for i in range(10001):
   t=i/10000;weights=[]
   for bar,line in zip(bars,lines):
    h,y=list(bar);w=value(h,t)/57;weights.append(w);self.assertAlmostEqual(value(h,t)+value(y,t),201,delta=.002);self.assertAlmostEqual(value(next(iter(line)),t),1.2+6*w,delta=.002)
   self.assertAlmostEqual(sum(weights),1,delta=.00005)
   if value(opacity,t)>0:
    state=0 if t<11/48 else 1 if t<27/48 else 2
    self.assertEqual(value(x,t),[260,377,494][state])
    for w,v in zip(weights,[[.65,.2,.1,.05],[.08,.72,.12,.08],[.05,.15,.2,.6]][state]):self.assertAlmostEqual(w,v,delta=.00005)
 def test_scoped_sources_and_fallbacks(self):
  for stem,topic in [('simclr-temperature-competition','theory/paradigms/self-supervised/contrastive-learning/simclr'),('bahdanau-alignment-context','theory/models/transformer/bahdanau-attention/index')]:
   r=E.parse(A/(stem+'-still.svg')).getroot();self.assertFalse(list(r.iter(N+'animate')))
   for el in r.iter(N+'text'):self.assertGreaterEqual(float(el.get('font-size','12')),12)
   for lang in ['', '.zh-TW']:
    s=(R/'docs'/(topic+lang+'.md')).read_text()
    for token in ['data-source-asset-urls','data-still-src','concept-motion-scroll','tabindex="0"','min-width:640px']:self.assertIn(token,s)
if __name__=='__main__':unittest.main()
