"""Recompute toy recurrences independently and check the rendered SVG encodings."""
import math
from pathlib import Path
import unittest
import xml.etree.ElementTree as E
A=Path(__file__).resolve().parents[1]/'docs/assets/concept-animations'
N='{http://www.w3.org/2000/svg}'
def root(stem,kind='motion'): return E.parse(A/f'{stem}-{kind}.svg').getroot()
class LionMuon(unittest.TestCase):
 def test_lion_blend_geometry_and_sign(self):
  for kind in ['motion','still']:
   r=root('lion-sign-momentum',kind); m=.8
   for i,g in enumerate([-1,-1,1,-1,1]):
    c=.8*m+.2*g; x=101+100*i
    bar=next(e for e in r.iter(N+'rect') if e.get('x')==str(x) and e.get('fill')=='#d27b39')
    self.assertAlmostEqual(float(bar.get('height')),abs(c)*100,places=5)
    self.assertAlmostEqual(float(bar.get('y')),224-max(0,c)*100,places=5)
    label=next(e for e in r.iter(N+'text') if e.get('x')==str(x+15) and e.get('y')=='251')
    self.assertAlmostEqual(float(label.text),c,delta=.0005)
    arrow=next(e for e in r.iter(N+'line') if e.get('y1')=='294' and float(e.get('x1')) in [x-9,x+39])
    dx=float(arrow.get('x2'))-float(arrow.get('x1'))
    self.assertEqual(abs(dx),48);self.assertEqual(math.copysign(1,dx),-math.copysign(1,c))
    m=.7*m+.3*g
 def test_lion_cursor_never_rewinds_through_prior_steps(self):
  animations=list(root('lion-sign-momentum').iter(N+'animate'))
  self.assertEqual(len(animations),3)
  for a in animations:
   vs=list(map(float,a.get('values').split(';')))
   self.assertEqual(vs,sorted(vs));self.assertEqual(vs[-1],vs[-2])
   self.assertEqual(a.get('keyTimes'),'0;0.2;0.4;0.6;0.8;1')
 def test_muon_cubic_singular_values(self):
  r=root('muon-spectral-balancing')
  bars=[e for e in r.iter(N+'rect') if e.get('class')=='running']
  for initial,bar in zip([1.5,.3],bars):
   expected=[initial]
   for _ in range(6):expected.append(.5*expected[-1]*(3-expected[-1]**2))
   a=bar.find(N+'animate'); actual=list(map(float,a.get('values').split(';')))
   self.assertEqual(len(actual),7)
   for k,(v,s) in enumerate(zip(actual,expected)):
    self.assertAlmostEqual(v,140*s,delta=.00051)
    self.assertAlmostEqual(float(a.get('keyTimes').split(';')[k]),k/6)
   still=root('muon-spectral-balancing','still')
   b=next(e for e in still.iter(N+'rect') if e.get('fill')==bar.get('fill') and e.get('x')=='348')
   self.assertAlmostEqual(float(b.get('width')),140*expected[-1],delta=.00051)
 def test_bilingual_source_asset_hooks(self):
  for topic in ['lion','muon']:
   for suffix in ['', '.zh-TW']:
    text=(A.parents[1]/f'theory/optimization/adaptive/{topic}{suffix}.md').read_text()
    self.assertIn('<img data-source-asset-urls',text)
    self.assertIn('data-motion-src=',text); self.assertIn('data-still-src=',text)
if __name__=='__main__':unittest.main()
