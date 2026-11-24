"""Verify actual interpolated source SVG coordinates and causal handoff timing."""
import bisect, math, unittest, xml.etree.ElementTree as E
from pathlib import Path
R=Path(__file__).resolve().parents[1];A=R/'docs/assets/concept-animations';N='{http://www.w3.org/2000/svg}'
def value(a,t):
 vs=list(map(float,a.get('values').split(';')));ts=list(map(float,a.get('keyTimes').split(';')))
 if t==1:return vs[-1]
 i=min(len(vs)-2,max(0,bisect.bisect_right(ts,t)-1))
 return vs[i] if a.get('calcMode')=='discrete' else vs[i]+(vs[i+1]-vs[i])*(t-ts[i])/(ts[i+1]-ts[i])
class NormSeq(unittest.TestCase):
 def test_actual_norm_coordinates(self):
  r=E.parse(A/'layernorm-feature-shift-motion.svg').getroot()
  raw=[e for e in r.iter(N+'circle') if e.find(N+'animate') is not None]
  z=[e for e in r.iter(N+'circle') if e.find(N+'animate') is None]
  mean=next(e for e in r.iter(N+'line') if e.get('stroke')=='#7756b7')
  self.assertEqual(len(raw),5);self.assertEqual(len(z),5)
  for i in range(1001):
   t=i/1000;x=[(356-value(e.find(N+'animate'),t))/20 for e in raw];mu=sum(x)/5
   self.assertAlmostEqual((356-value(mean.find(N+'animate'),t))/20,mu)
   self.assertAlmostEqual(sum((v-mu)**2 for v in x)/5,8)
   for v,e in zip(x,z):self.assertAlmostEqual((245-float(e.get('cy')))/65,(v-mu)/math.sqrt(8))
 def test_context_is_constant_during_decoder(self):
  r=E.parse(A/'seq2seq-context-handoff-motion.svg').getroot()
  bars=[e.find(N+'animate') for e in r.iter(N+'rect') if e.get('y')=='239' and e.find(N+'animate') is not None]
  self.assertEqual(len(bars),4)
  for i in range(1000):
   t=i/1000
   for a in bars:self.assertEqual(value(a,t),int(t>=.5))
  dec=[e.find(N+'animate') for e in r.iter(N+'rect') if e.get('stroke')=='#e88b49' and int(e.get('x'))>=500]
  for t,expected in [(.6,[0,0,0]),(.7,[1,0,0]),(.85,[0,1,0]),(.97,[0,0,1])]:self.assertEqual([value(a,t) for a in dec],expected)
 def test_sources_and_fallback(self):
  for stem in ['layernorm-feature-shift','seq2seq-context-handoff']:
   for kind in ['motion','still']:
    r=E.parse(A/f'{stem}-{kind}.svg').getroot()
    if kind=='still':self.assertFalse(list(r.iter(N+'animate')))
    for e in r.iter(N+'text'):self.assertGreaterEqual(float(e.get('font-size','12')),12)
if __name__=='__main__':unittest.main()
