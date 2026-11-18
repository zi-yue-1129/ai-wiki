"""Paired resampling geometry and analytic online Elo probability checks."""
from pathlib import Path
from xml.etree import ElementTree as E
import math,re,unittest
N='{http://www.w3.org/2000/svg}';A=Path(__file__).resolve().parents[1]/'docs/assets/concept-animations'
def root(stem,kind='motion'):return E.parse(A/f'{stem}-{kind}.svg').getroot()
def sample(a,t):
 v=list(map(float,a.get('values').split(';')));ts=list(map(float,a.get('keyTimes').split(';')))
 for i in range(len(ts)-1):
  if t<=ts[i+1]:return v[i]+(v[i+1]-v[i])*(t-ts[i])/(ts[i+1]-ts[i])
 return v[-1]
class BootstrapElo(unittest.TestCase):
 def test_bootstrap_pair_mapping(self):
  indices=[4,2,4,1,5];original=[.3,-.1,.2,.5,-.2];draw=[original[i-1] for i in indices]
  self.assertAlmostEqual(sum(original)/5,.14);self.assertAlmostEqual(sum(draw)/5,.20)
  for kind in ['motion','still']:
   r=root('paired-bootstrap-resampling',kind);texts=list(r.iter(N+'text'))
   self.assertEqual([float(t.text) for t in texts if t.get('y')=='130'],original)
   self.assertEqual([float(t.text) for t in texts if t.get('y')=='272'],draw)
   self.assertEqual([int(t.text[1:]) for t in texts if t.get('y')=='253'],indices)
   self.assertFalse(any(t.get('y')=='213' for t in texts),'heading must not intersect transit lane')
  groups=root('paired-bootstrap-resampling').findall(N+'g');self.assertEqual(len(groups),5)
  for slot,(g,source) in enumerate(zip(groups,indices)):
   start=list(map(float,re.findall(r'-?\d+(?:\.\d+)?',g.get('transform'))));self.assertLessEqual(abs(start[0]-(101+115*(source-1))),4)
   inner=g.find(N+'g');self.assertEqual(len(inner.findall(N+'circle')),2);motion=inner.find(N+'animateMotion');nums=list(map(float,re.findall(r'-?\d+(?:\.\d+)?',motion.get('path'))))
   self.assertAlmostEqual(start[0]+nums[-2],101+115*slot);self.assertAlmostEqual(start[1]+nums[-1],226);self.assertEqual(motion.get('keyPoints'),'0;0;1;1')
 def test_elo_two_sided_update_and_probability(self):
  r=root('elo-online-update');circles=[c for c in r.iter(N+'circle') if c.find(N+'animate') is not None];self.assertEqual(len(circles),2)
  bar=[b for b in r.iter(N+'rect') if b.find(N+'animate') is not None][0][0]
  for i in range(1001):
   t=i/1000;ra=1500+(sample(circles[0][0],t)-365)/2.9;rb=1500+(sample(circles[1][0],t)-365)/2.9
   self.assertAlmostEqual(ra+rb,3000);self.assertAlmostEqual(sample(bar,t)/246,1/(1+10**((rb-ra)/400)),delta=1e-6)
  self.assertAlmostEqual(sample(circles[0][0],1),365+2.9*64*(1-.5));self.assertAlmostEqual(sample(circles[1][0],1),365+2.9*64*(0-.5))
  s=root('elo-online-update','still');width=[float(b.get('width')) for b in s.iter(N+'rect') if b.get('x')=='226' and b.get('fill')=='#158c86'][0];self.assertAlmostEqual(width/246,1/(1+10**(-64/400)),places=8)
 def test_static_assets(self):
  for stem in ['paired-bootstrap-resampling','elo-online-update']:
   r=root(stem,'still');self.assertFalse(list(r.iter(N+'animate')));self.assertFalse(list(r.iter(N+'animateMotion')))
if __name__=='__main__':unittest.main()
