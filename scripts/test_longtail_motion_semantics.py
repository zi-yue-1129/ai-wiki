"""Full forward/return coupling for effective counts and post-hoc logit winners."""
import math,unittest,xml.etree.ElementTree as E
from pathlib import Path
N='{http://www.w3.org/2000/svg}'
A=Path(__file__).resolve().parents[1]/'docs/assets/concept-animations'
def value(n,attr,t=None):
 a=next((a for a in n if a.get('attributeName')==attr),None)
 if a is None or t is None:return float(n.get(attr,'1' if attr=='opacity' else '0'))
 ts=list(map(float,a.get('keyTimes').split(';')));vs=list(map(float,a.get('values').split(';')))
 for i in range(len(ts)-1):
  if t<ts[i+1]:
   if a.get('calcMode')=='discrete':return vs[i]
   return vs[i]+(vs[i+1]-vs[i])*(t-ts[i])/(ts[i+1]-ts[i])
 return vs[-1]
class Longtail(unittest.TestCase):
 def test_effective_curve_and_dot_count(self):
  for mode in ('motion','still'):
   r=E.parse(A/f'effective-number-growth-{mode}.svg').getroot();dots=[n for n in r.findall(N+'circle') if n.get('r')=='10'];marker=next(n for n in r.findall(N+'circle') if n.get('r')=='7');guide=r.find(N+'line')
   for t in ([i/1000 for i in range(1001)] if mode=='motion' else [None]):
    count=(value(marker,'cx',t)-290)/14.25;eff=(276-value(marker,'cy',t))/7.65
    self.assertAlmostEqual(eff,(1-.9**count)/.1,delta=.0003)
    self.assertAlmostEqual(sum((value(n,'opacity',t)-.12)/.88 for n in dots),count,delta=1e-7)
    self.assertAlmostEqual(value(guide,'x1',t),value(marker,'cx',t),delta=1e-7)
   e=(1-.9**20)/.1;self.assertAlmostEqual(e,8.784233454094307);self.assertGreater(1/e,1/20)
 def test_logit_scores_and_bidirectional_winner(self):
  cross=1.5/math.log(9);edges=[.9*cross,1-.1*cross]
  for mode in ('motion','still'):
   r=E.parse(A/f'logit-prior-decision-{mode}.svg').getroot();dots=r.findall(N+'circle');bars=[n for n in r.findall(N+'rect') if n.get('fill') in ('#3470bd','#de9238')];labels=[n for n in r.findall(N+'text') if n.text in ('HEAD','TAIL')]
   for t in ([i/1000 for i in range(1001)]+[x+d for x in edges for d in (-1e-7,1e-7)] if mode=='motion' else [None]):
    tau=(value(dots[0],'cx',t)-312)/271;scores=[2-tau*math.log(.9),.5-tau*math.log(.1)]
    for n,b,score in zip(dots,bars,scores):
     self.assertAlmostEqual(value(n,'cy',t),278-155*score/3.3,delta=1e-7);self.assertAlmostEqual(value(b,'width',t),178*score/3.3,delta=1e-7)
    active=[n.text for n in labels if value(n,'opacity',t)==1];self.assertEqual(active,['HEAD' if scores[0]>scores[1] else 'TAIL'])
 def test_static_fallbacks(self):
  for t in ('effective-number-growth','logit-prior-decision'):
   self.assertFalse(E.parse(A/f'{t}-still.svg').getroot().findall('.//'+N+'animate'))
if __name__=='__main__':unittest.main()
