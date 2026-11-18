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
class PredictiveCodingMotion(unittest.TestCase):
 def test_residual_conservation(self):
  r=E.parse(A/'rao-ballard-residual-motion.svg').getroot();an=list(r.iter(N+'animate'))
  for i in range(10001):
   t=i/10000;p,pc,e,ec=[value(a,t) for a in an]
   self.assertAlmostEqual(p+e,.85*335);self.assertAlmostEqual(pc,179+p);self.assertAlmostEqual(ec,179+e)
   self.assertTrue(.25*335-1e-9<=p<=.8*335+1e-9)
 def test_balanced_errors_and_timing(self):
  r=E.parse(A/'predictive-local-settling-motion.svg').getroot();an=list(r.iter(N+'animate'));labels=an[:3];left,right,drive,pulse=an[3:]
  for i in range(10001):
   t=i/10000;l,v,d=[value(a,t)/340 for a in [left,right,drive]];z=.2+l
   self.assertAlmostEqual(l+v,.6);self.assertAlmostEqual(d,v-l);self.assertAlmostEqual(d,.2+.8-2*z)
   if value(labels[0],t):self.assertAlmostEqual(z,.2)
   if value(labels[2],t):self.assertAlmostEqual(z,.5)
   if value(pulse,t)>0:self.assertAlmostEqual(d,0)
 def test_scoped_sources_and_fallbacks(self):
  for stem,topic in [('rao-ballard-residual','rao-ballard-1999'),('predictive-local-settling','whittington-bogacz-2017')]:
   for kind in ['motion','still']:
    r=E.parse(A/(stem+'-'+kind+'.svg')).getroot()
    if kind=='still':self.assertFalse(list(r.iter(N+'animate')))
    for el in r.iter(N+'text'):self.assertGreaterEqual(float(el.get('font-size','12')),12)
   for lang in ['', '.zh-TW']:
    s=(R/'docs/brain-mind/predictive-coding'/topic/('index'+lang+'.md')).read_text()
    for token in ['data-source-asset-urls','data-still-src','concept-motion-scroll','tabindex="0"','min-width:640px']:self.assertIn(token,s)
if __name__=='__main__':unittest.main()
