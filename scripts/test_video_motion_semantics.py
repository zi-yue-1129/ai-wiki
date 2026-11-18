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
class VideoMotion(unittest.TestCase):
 def test_i3d_discrete_contributions(self):
  r=E.parse(A/'i3d-filter-inflation-motion.svg').getroot();an=list(r.iter(N+'animate'));bar=an[-1]
  self.assertEqual(bar.get('calcMode'),'discrete')
  for i in range(10001):
   t=i/10000;stage=0 if t<.2 or t==1 else 1 if t<.5 else 2 if t<.8 else 3
   self.assertAlmostEqual(value(bar,t),416*stage/3,delta=.000001)
  for t,a in zip([.2,.5,.8],an[:3]):self.assertEqual(value(a,t),1)
 def test_vivit_marker_connectivity(self):
  r=E.parse(A/'vivit-factorised-attention-motion.svg').getroot();moves=[e for e in r.iter() if e.find(N+'animate') is not None]
  for e in moves:
   if e.tag==N+'circle':
    a=e.find(N+'animate');attr=a.get('attributeName')
    if attr=='cx':self.assertEqual(float(e.get('cy')),230)
    if attr=='cy':self.assertEqual(float(e.get('cx')),558)
 def test_sources(self):
  for topic,stem in [('vivit','vivit-factorised-attention'),('i3d','i3d-filter-inflation')]:
   for kind in ['motion','still']:
    r=E.parse(A/(stem+'-'+kind+'.svg')).getroot()
    if kind=='still':self.assertFalse(list(r.iter(N+'animate')))
    for e in r.iter(N+'text'):self.assertGreaterEqual(float(e.get('font-size','12')),12)
   for lang in ['', '.zh-TW']:
    s=(R/f'docs/theory/models/computer-vision/video/{topic}{lang}.md').read_text()
    for token in ['data-source-asset-urls','data-still-src','tabindex="0"','min-width:800px']:self.assertIn(token,s)
if __name__=='__main__':unittest.main()
