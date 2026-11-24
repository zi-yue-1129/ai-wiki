"""Actual IA3 gain geometry and prefix softmax, including interpolated frames."""
import bisect,math,unittest
from pathlib import Path
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1];ASSETS=ROOT/'docs/assets/concept-animations';NS='{http://www.w3.org/2000/svg}'
def read(stem,kind='motion'):return ET.parse(ASSETS/f'{stem}-{kind}.svg').getroot()
def at(e,attr,t):
 a=next((a for a in e.findall(NS+'animate') if a.get('attributeName')==attr),None)
 if a is None:return float(e.get(attr,'1' if attr=='opacity' else '0'))
 v=list(map(float,a.get('values').split(';')));k=list(map(float,a.get('keyTimes').split(';'))) if a.get('keyTimes') else [i/(len(v)-1) for i in range(len(v))];i=min(len(k)-1,max(0,bisect.bisect_right(k,t)-1))
 if a.get('calcMode')=='discrete' or i==len(k)-1:return v[i]
 q=(t-k[i])/(k[i+1]-k[i]);return v[i]*(1-q)+v[i+1]*q
class VqSplatSvgTests(unittest.TestCase):
 def test_actual_hard_assignments_and_boundary_geometry(self):
  r=read('vqvae-codebook-snap');link=next(r.iter(NS+'line'));groups=r.findall(NS+'g');codes=[(139,187),(290,187),(220,266)]
  for i in range(20001):
   t=i/20000;x=at(link,'x1',t);q=at(link,'x2',t);d=[(x-a)**2+(146-b)**2 for a,b in codes]
   self.assertIn(q,[139,290]);idx=0 if q==139 else 1;self.assertLessEqual(d[idx],min(d)+1e-8)
   self.assertEqual([at(g,'opacity',t) for g in groups],[float(idx==0),float(idx==1)])
  path=next(e for e in r.iter(NS+'path') if e.get('d','').startswith('M214.5'));end=float(path.get('d').split('V')[1]);self.assertAlmostEqual(end,190.6139240506,places=5)
  for y in [124,146,end]:
   d=[(214.5-a)**2+(y-b)**2 for a,b in codes];self.assertAlmostEqual(d[0],d[1]);self.assertLessEqual(d[0],d[2]+1e-4)
 def test_alpha_steps_mass_and_transmittance_text(self):
  r=read('gaussian-splat-alpha-composite');segments=[e for e in r.findall(NS+'rect') if e.get('y')=='143' and e.get('rx') is None];texts=[e for e in r.findall(NS+'text') if (e.text or '').startswith('Remaining T')]
  for t,ws,T in [(0,[0,0,0],1),(.17999,[0,0,0],1),(.18,[.5,0,0],.5),(.47999,[.5,0,0],.5),(.48,[.5,.3,0],.2),(.69,[.5,.3,.16],.04),(.999,[.5,.3,.16],.04)]:
   visible=[at(e,'width',t)*at(e,'opacity',t)/158 for e in segments[:3]];self.assertEqual(len(visible),3)
   for a,b in zip(visible,ws):self.assertAlmostEqual(a,b)
   self.assertAlmostEqual(at(segments[-1],'width',t)/158,T);self.assertAlmostEqual(sum(visible)+T,1)
   shown=[e.text for e in texts if at(e,'opacity',t)==1];self.assertEqual(shown,[f'Remaining T = {T:.2f}'])
 def test_local_bilingual_wrappers_and_labs_preserved(self):
  for topic in ['theory/paradigms/unsupervised/density-and-generative-models/vae/vq-vae','theory/models/computer-vision/3d-and-neural-rendering/gaussian-splatting']:
   for lang in ['', '.zh-TW']:
    s=(ROOT/f'docs/{topic}{lang}.md').read_text()
    for token in ['data-source-asset-urls','data-still-src','width:100%;overflow-x:auto','width:640px','tabindex="0"','data-vq-splat-lab']:self.assertIn(token,s)
if __name__=='__main__':unittest.main()
