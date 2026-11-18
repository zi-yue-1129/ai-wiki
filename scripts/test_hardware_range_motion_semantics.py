"""Analytical log-axis range and Roofline checks across the full animation."""
import math,unittest,xml.etree.ElementTree as E
from pathlib import Path
N='{http://www.w3.org/2000/svg}'
A=Path(__file__).resolve().parents[1]/'docs/assets/concept-animations'
def value(n,attr,t=None):
 a=next((a for a in n if a.get('attributeName')==attr),None)
 if a is None or t is None:return float(n.get(attr))
 ts=list(map(float,a.get('keyTimes').split(';')));vs=list(map(float,a.get('values').split(';')))
 for i in range(len(ts)-1):
  if t<=ts[i+1]:return vs[i]+(vs[i+1]-vs[i])*(t-ts[i])/(ts[i+1]-ts[i])
 return vs[-1]
class HardwareRanges(unittest.TestCase):
 def test_roofline_bound_and_guide(self):
  for mode in ('motion','still'):
   r=E.parse(A/f'roofline-ridge-sweep-{mode}.svg').getroot()
   markers=[n for n in r.findall(N+'circle') if n.get('fill')=='#FFBD6A']
   for t in ([i/1000 for i in range(1001)] if mode=='motion' else [None]):
    for n in markers:
     x=value(n,'cx',t);y=value(n,'cy',t);intensity=2**((x-100)/65-1);perf=2**((289-y)/43.4)
     self.assertAlmostEqual(perf,min(32,4*intensity),places=10)
    for n in r.findall(N+'line'):
     if n.find(N+'animate') is not None:
      self.assertAlmostEqual(value(n,'x1',t),value(markers[0],'cx',t));self.assertAlmostEqual(value(n,'y1',t),value(markers[0],'cy',t))
   self.assertIn('245.6',r.find(N+'path').get('d'))
 def test_fp8_endpoints_and_slider(self):
  for mode in ('motion','still'):
   r=E.parse(A/f'fp8-scale-range-{mode}.svg').getroot();slider=next(n for n in r.findall(N+'circle') if n.get('cy')=='56')
   for t in ([i/1000 for i in range(1001)] if mode=='motion' else [None]):
    s=16**((value(slider,'cx',t)-477)/88)
    for n in r.findall(N+'rect'):
     if n.get('y') not in ('122','197'):continue
     lo,hi=(2**-16,57344) if n.get('y')=='122' else (2**-9,448)
     for x,v in [(value(n,'x',t),lo/s),(value(n,'x',t)+float(n.get('width')),hi/s)]:self.assertAlmostEqual(x,350+40*math.log10(v),delta=1e-7)
   self.assertTrue(any(n.text=='Scale s (log)' for n in r));self.assertTrue(any(n.text=='4' and n.get('x')=='521' for n in r))
 def test_stills_and_continuous_clocks(self):
  for topic in ('roofline-ridge-sweep','fp8-scale-range'):
   for mode in ('motion','still'):
    a=E.parse(A/f'{topic}-{mode}.svg').getroot().findall('.//'+N+'animate')
    if mode=='still':self.assertFalse(a)
    else:
     self.assertTrue(a)
     for n in a:self.assertEqual(n.get('dur'),'10s');self.assertEqual(n.get('calcMode'),'linear')
if __name__=='__main__':unittest.main()
