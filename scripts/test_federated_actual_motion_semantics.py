"""Validate actual source SVG geometry, transfer scheduling and mask arithmetic."""
from pathlib import Path
import unittest,xml.etree.ElementTree as ET,re,math
R=Path(__file__).resolve().parents[1];A=R/'docs/assets/concept-animations';N='{http://www.w3.org/2000/svg}'
STEMS=['fedavg-weighted-round','secagg-mask-cancellation']
def sample(a,t):
 v=list(map(float,a.get('values').split(';')));k=list(map(float,a.get('keyTimes').split(';')))
 for i in range(len(k)-1):
  if t<=k[i+1]:return v[i]+(v[i+1]-v[i])*(t-k[i])/(k[i+1]-k[i])
 return v[-1]
def root(stem,kind='motion'):return ET.parse(A/f'{stem}-{kind}.svg').getroot()
class FederatedMotion(unittest.TestCase):
 def test_weighted_scalar_and_shared_scale(self):
  self.assertAlmostEqual(sum(n*w for n,w in zip([2,3,5],[-1,.5,2]))/10,.95)
  r=root(STEMS[0]);circles=r.findall(N+'circle');self.assertEqual(len(circles),3)
  for c,origin,w in zip(circles,[116,320,524],[-1,.5,2]):
   a=c.find(N+'animate');self.assertEqual(sample(a,0),origin);self.assertEqual(sample(a,.6),origin+22*w)
   for i in range(181,490):
    t=i/1000;self.assertAlmostEqual(sample(a,t),origin+22*w*(t-.18)/.31)
  self.assertEqual([float(c.get('cx')) for c in root(STEMS[0],'still').findall(N+'circle')],[94,331,568])
 def test_transfer_direction_and_causal_arrival(self):
  for stem,start,end,aggregate in [(STEMS[0],.54,.72,.76),(STEMS[1],.43,.76,.78)]:
   r=root(stem);paths=[p for p in r.findall(N+'path') if p.get('class')=='motion'];self.assertEqual(len(paths),3)
   for p in paths:
    length=float(p.get('stroke-dasharray'));self.assertGreater(length,30);a=p.find(N+'animate')
    x0,y0,x1,y1,x2,y2=map(float,re.findall(r'-?\d+(?:\.\d+)?',p.get('d')))
    points=[((1-t)**2*x0+2*(1-t)*t*x1+t*t*x2,(1-t)**2*y0+2*(1-t)*t*y1+t*t*y2) for t in [i/10000 for i in range(10001)]]
    actual=sum(math.dist(a,b) for a,b in zip(points,points[1:]));self.assertAlmostEqual(length,actual,delta=.002)
    self.assertEqual(sample(a,start),length);self.assertAlmostEqual(sample(a,end),0)
    self.assertTrue(p.get('d').endswith('320 140' if stem==STEMS[0] else '320 260'))
    self.assertAlmostEqual(sample(a,(start+end)/2),length/2)
   final=next(t for t in r.findall(N+'text') if (t.text or '').startswith('θ = 0.95' if stem==STEMS[0] else 'Σ = +5'))
   self.assertEqual(sample(final.find(N+'animate'),end),0);self.assertEqual(sample(final.find(N+'animate'),aggregate),0)
 def test_masks_and_server_scope(self):
  masks=[3-2,-3+1,2-1];updates=[4,-1,2];sent=[u+m for u,m in zip(updates,masks)]
  self.assertEqual(masks,[1,-2,1]);self.assertEqual(sum(masks),0);self.assertEqual(sent,[5,-3,3]);self.assertEqual(sum(sent),sum(updates))
  for kind in ['motion','still']:
   texts=[t.text for t in root(STEMS[1],kind).findall(N+'text')]
   for v in ['+4','−1','+2','+1','−2','+5','−3','+3','RECOVERS ONLY SUM']:self.assertIn(v,texts)
 def test_static_and_reduced(self):
  for stem in STEMS:
   self.assertFalse(root(stem,'still').findall('.//'+N+'animate'))
   css=root(stem).find(N+'style').text;self.assertIn('prefers-reduced-motion:reduce',css);self.assertIn('.final{opacity:1!important}',css)
 def test_bilingual_source_hooks(self):
  for stem,topic in zip(STEMS,['federated-averaging','privacy-and-secure-aggregation']):
   for lang in ['', '.zh-TW']:
    text=(R/f'docs/theory/paradigms/federated/{topic}/index{lang}.md').read_text()
    self.assertIn('class="federated-source-scroll" tabindex="0" role="region"',text)
    self.assertIn(f'{stem}-still.svg" data-motion-src=',text);self.assertIn('data-source-asset-urls',text);self.assertIn('min-width:640px',text)
if __name__=='__main__':unittest.main()
