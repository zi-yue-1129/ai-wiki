"""Exact scales, causal fixed-value reveals, and true JumpReLU branch jump."""
from pathlib import Path
import unittest,xml.etree.ElementTree as E,re
N='{http://www.w3.org/2000/svg}';P=Path(__file__).resolve().parents[1];A=P/'docs/assets/concept-animations'
def root(stem,mode='motion'):return E.parse(A/f'{stem}-{mode}.svg').getroot()
def val(a,t):
 ts=list(map(float,a.get('keyTimes').split(';')));vs=list(map(float,a.get('values').split(';')));i=max(i for i,x in enumerate(ts) if x<=t)
 if i==len(ts)-1 or a.get('calcMode')=='discrete':return vs[i]
 return vs[i]+(vs[i+1]-vs[i])*(t-ts[i])/(ts[i+1]-ts[i])
def at(e,attr,t):
 a=next((a for a in e.findall(N+'animate') if a.get('attributeName')==attr),None)
 return val(a,t) if a is not None else float(e.get(attr))
class SAE(unittest.TestCase):
 def test_jump_shared_scale_dense(self):
  r=root('jumprelu-threshold-jump');ids={e.get('id'):e for e in r.iter() if e.get('id')}
  for t in [i/10000 for i in range(10000)]+[.45-1e-9,.45+1e-9]:
   z=min(t/.9,1)*3;active='low' if t<.45 else 'high';self.assertEqual(at(ids[active+'-branch'],'opacity',t),1)
   self.assertEqual(at(ids[('high' if active=='low' else 'low')+'-branch'],'opacity',t),0)
   mark=ids[active+'-marker'];f=0 if active=='low' else z
   self.assertAlmostEqual(at(mark,'cx',t),74+85*z,places=8);self.assertAlmostEqual(at(mark,'cy',t),292-54*f,places=8)
   self.assertAlmostEqual(at(ids['input-value'],'width',t),50*z,places=8)
   output=at(ids['output-value'],'width',t) if active=='high' else 0;self.assertAlmostEqual(output,50*f,places=8)
  self.assertGreater(at(ids['low-marker'],'cy',.45-1e-9)-at(ids['high-marker'],'cy',.45+1e-9),80.999)
  for e in [ids['low-branch'],ids['high-branch']]:self.assertEqual(e.find(N+'animate').get('calcMode'),'discrete')
 def test_threshold_strict_static_and_overview(self):
  r=root('jumprelu-threshold-jump','still');circles=list(r.iter(N+'circle'))
  self.assertTrue(any(e.get('cx')=='201.5' and e.get('cy')=='292' and e.get('fill')!='white' for e in circles))
  self.assertTrue(any(e.get('cx')=='201.5' and e.get('cy')=='211' and e.get('fill')=='white' for e in circles))
  c=next(e for e in circles if e.get('id')=='static-input-marker');self.assertAlmostEqual(float(c.get('cx')),74+85*2.25);self.assertAlmostEqual(float(c.get('cy')),292-54*2.25)
  for e in r.iter(N+'rect'):
   if e.get('fill') in ['#dc8a3d','#168f89']:self.assertEqual(float(e.get('width')),50*2.25)
 def test_gated_fixed_bars_scale_and_causality(self):
  for mode in ['motion','still']:
   r=root('gated-sae-gate-magnitude',mode)
   for e in r.iter(N+'rect'):
    if e.get('fill') not in ['#91a8b8','#dc8a3d','#168f89']:continue
    x,y=float(e.get('x')),e.get('y');value={'159':(-.7,1.5,0),'220':(.6,2.,2.),'281':(.9,.7,.7)}[y];col=0 if x<200 else 1 if x<400 else 2;v=value[col]
    self.assertAlmostEqual(float(e.get('width')),abs(v)*40)
    if col==0:self.assertAlmostEqual(x,132+min(v,0)*40)
    self.assertIsNone(e.find(N+'animate'))
  r=root('gated-sae-gate-magnitude');ids={e.get('id'):e for e in r.iter() if e.get('id')}
  for i in range(1001):
   t=i/1001
   if at(ids['output-reveal'],'opacity',t)>0:self.assertEqual(at(ids['magnitude-reveal'],'opacity',t),1)
  self.assertFalse(any(a.get('attributeName')=='width' for a in r.iter(N+'animate')))
 def test_bilingual_hooks_math_and_boundary_caption(self):
  for topic in ['gated-sae','jumprelu-sae']:
   blocks=[]
   for lang in ['', '.zh-TW']:
    s=(P/f'docs/society/interpretability/{topic}{lang}.md').read_text();self.assertIn('data-source-asset-urls',s);self.assertIn('overflow-x:auto',s);self.assertIn('width:640px;min-width:640px',s)
    for eq in re.findall(r'(?<!\$)\$([^$\n]+)\$(?!\$)',re.sub(r'\$\$.*?\$\$','',s,flags=re.S)):self.assertLessEqual(len(eq),55)
    if topic=='jumprelu-sae':self.assertIn('右側極限' if lang else 'right-hand limit',s)
    blocks.append([re.sub(r'\s+','',x) for x in re.findall(r'\$\$(.*?)\$\$',s,flags=re.S)])
   self.assertEqual(*blocks)
  css=(P/'docs/stylesheets/concept-motion.css').read_text();self.assertNotRegex(css,r'concept-motion-scroll\s*>\s*img[^}]*640px[^}]*!important')
if __name__=='__main__':unittest.main()
