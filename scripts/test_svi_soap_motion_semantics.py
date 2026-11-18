"""SVI recurrence, clocks, and SOAP basis arithmetic in the actual SVGs."""
from pathlib import Path
import math,unittest,xml.etree.ElementTree as E
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'docs/assets/concept-animations';N='{http://www.w3.org/2000/svg}'
def at(a,t):
 vs=list(map(float,a.get('values').split(';')));ts=list(map(float,a.get('keyTimes').split(';')));i=max(i for i,x in enumerate(ts) if x<=t)
 return vs[i] if a.get('calcMode')=='discrete' or i==len(vs)-1 else vs[i]+(vs[i+1]-vs[i])*(t-ts[i])/(ts[i+1]-ts[i])
class SVISOAP(unittest.TestCase):
 def test_svi_exact_update_and_batch_clock(self):
  vals=[.2]
  for rho,proposal in zip([.25,.3,.2],[.8,.5,.65]):vals.append((1-rho)*vals[-1]+rho*proposal)
  r=E.parse(A/'svi-minibatch-global-motion.svg').getroot();c=next(e for e in r.iter(N+'circle') if e.get('r')=='10');a=c[0]
  for t,v in zip([0,.30,.633333,.966667],vals):self.assertAlmostEqual(at(a,t),439+139*v)
  active=next(e for e in r.iter(N+'circle') if e.get('r')=='4.5')[0]
  rings=[e for e in r.iter(N+'circle') if e.get('r')=='17'];estimates=[e for e in r.iter(N+'circle') if e.get('r')=='5' and e.get('cy') in ['153','200','247']]
  for k in range(10001):
   t=k/10001;idx=0 if t<.333333 else 1 if t<.666667 else 2
   self.assertEqual(at(active,t),[153,200,247][idx]);self.assertEqual(sum(at(e[0],t) for e in rings),3)
   for e in estimates:
    if int(e.get('cy'))!=[153,200,247][idx]:self.assertEqual(at(e[0],t),5)
  self.assertAlmostEqual(at(a,.99999),439+139*.446)
 def test_soap_matrix_and_causal_highlights(self):
  q=[[1/math.sqrt(2),1/math.sqrt(2)],[1/math.sqrt(2),-1/math.sqrt(2)]]
  def mul(a,b):return [[sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
  for actual,want in [(mul(mul(q,[[3,1],[1,3]]),q),[[4,0],[0,2]]),(mul(mul(q,[[1,0],[0,1.6]]),q),[[1.3,-.3],[-.3,1.3]])]:
   for a,b in zip(sum(actual,[]),sum(want,[])):self.assertAlmostEqual(a,b)
  r=E.parse(A/'soap-eigenbasis-adam-motion.svg').getroot()
  numbers=[float(e.text) for e in r.iter(N+'text') if e.get('class')=='num']
  self.assertEqual(numbers,[3,1,1,3,4,0,0,2,1,0,0,1.6,1.3,-.3,-.3,1.3])
  for x,t in [('194',.23),('345',.49),('496',.75)]:
   a=next(e for e in r.iter(N+'rect') if e.get('x')==x)[0]
   for j in range(10001):self.assertEqual(at(a,j/10001),int(j/10001>=t))
 def test_sources(self):
  for path in ['theory/optimization/adaptive/soap','theory/paradigms/probabilistic/variational-inference/stochastic-variational-inference']:
   for lang in ['', '.zh-TW']:
    s=(ROOT/f'docs/{path}{lang}.md').read_text()
    for text in ['data-source-asset-urls','data-still-src','concept-motion-scroll','tabindex="0"','min-width:640px']:self.assertIn(text,s)
    self.assertIn('迴圈' if lang else 'loop resets',s)
if __name__=='__main__':unittest.main()
