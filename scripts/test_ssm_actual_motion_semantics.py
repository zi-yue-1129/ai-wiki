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
class SSMMotion(unittest.TestCase):
 def test_s4d_sum_and_reveal(self):
  r=E.parse(A/'s4d-diagonal-modes-motion.svg').getroot()
  circles=[e for e in r.iter(N+'circle') if len(e.findall(N+'animate'))==2]
  paths=[e for e in r.iter(N+'path') if e.find(N+'animate') is not None]
  self.assertEqual(len(circles),3)
  for step in range(10001):
   t=step/10000
   cy=[value(e.findall(N+'animate')[1],t) for e in circles]
   self.assertAlmostEqual((261-cy[2])/72,(165-cy[0])/68+(328-cy[1])/68,delta=.00025)
  import re
  for p in paths:
   a=p.find(N+'animate');coords=list(map(float,re.findall(r'-?\d+(?:\.\d+)?',p.get('d'))));pts=list(zip(coords[::2],coords[1::2]));ds=[math.dist(x,y) for x,y in zip(pts,pts[1:])]
   for i in range(16):self.assertAlmostEqual(value(a,.82*i/15),sum(ds)-sum(ds[:i]),delta=.00001)
 def test_ssd_synchronized_rows(self):
  r=E.parse(A/'mamba2-ssd-causal-map-motion.svg').getroot()
  halos=[e.find(N+'animate') for e in r.iter(N+'circle') if e.get('r')=='27']
  rows=[e.find(N+'animate') for e in r.iter(N+'rect') if e.get('width')=='224']
  for step in range(10000):
   t=step/10000;i=int(4*t)
   self.assertEqual([value(a,t) for a in rows],[float(k==i) for k in range(4)])
   self.assertEqual([value(a,t)==1 for a in halos],[k==i for k in range(4)])
 def test_sources(self):
  for stem in ['s4d-diagonal-modes','mamba2-ssd-causal-map']:
   for variant in ['motion','still']:
    r=E.parse(A/f'{stem}-{variant}.svg').getroot()
    if variant=='still':self.assertFalse(list(r.iter(N+'animate')))
    for e in r.iter(N+'text'):self.assertGreaterEqual(float(e.get('font-size','12')),12)
if __name__=='__main__':unittest.main()
