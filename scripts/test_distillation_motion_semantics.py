"""Actual SVG timing, numeric probability and negative-mutation regressions."""
from pathlib import Path
import math,copy,unittest,xml.etree.ElementTree as E
R=Path(__file__).resolve().parents[1];A=R/'docs/assets/concept-animations';N='{http://www.w3.org/2000/svg}'
def value(e,attr,t):
 a=next((a for a in e.findall(N+'animate') if a.get('attributeName')==attr),None)
 if a is None:return float(e.get(attr))
 ts=list(map(float,a.get('keyTimes').split(';')));vs=list(map(float,a.get('values').split(';')));i=max(i for i,x in enumerate(ts) if x<=t)
 return vs[i] if i==len(ts)-1 or a.get('calcMode')=='discrete' else vs[i]+(vs[i+1]-vs[i])*(t-ts[i])/(ts[i+1]-ts[i])
def check(r):
 for t in [i/1000 for i in range(1000)]+[.299999,.30,.599999,.60,.85,.93]:
  T=1 if t<.3 else 3;p=[math.exp(z/T) for z in [3,1,0]];p=[v/sum(p) for v in p]
  for prefix,base in [('teacher',235),('student',367)]:
   hs=[]
   for i in range(3):
    e=r.find(f".//*[@id='{prefix}-{i}']");h=value(e,'height',t);hs.append(h)
    assert abs(h+value(e,'y',t)-base)<1e-9
    if prefix=='teacher':assert abs(h-100*p[i])<1e-9
   assert abs(sum(hs)-100)<1e-9
  g=next(g for g in r.findall(N+'g') if (g.find(N+'text') is not None and g.find(N+'text').text=='T = 3'))
  assert value(g,'opacity',t)==(0 if t<.3 else 1)
class Tests(unittest.TestCase):
 def test_dense_probabilities(self):check(E.parse(A/'kd-soft-target-alignment-motion.svg').getroot())
 def test_negative_linear_teacher(self):
  r=E.parse(A/'kd-soft-target-alignment-motion.svg').getroot();r.find(".//*[@id='teacher-0']/"+N+'animate').set('calcMode','linear')
  with self.assertRaises(AssertionError):check(r)
 def test_negative_scale(self):
  r=E.parse(A/'kd-soft-target-alignment-motion.svg').getroot();a=r.find(".//*[@id='student-0']/"+N+'animate');a.set('values','300;300;300;300')
  with self.assertRaises(AssertionError):check(r)
 def test_directions_and_stages(self):
  r=E.parse(A/'fitnets-hint-then-output-motion.svg').getroot();ps=[e.get('d') for e in r.iter(N+'path')]
  self.assertIn('M529 172 L435 172',ps);self.assertIn('M415 341 L309 341',ps)
  for g in r.findall(N+'g'):
   t=g.find(N+'text')
   if t is not None and t.text=='Hint match':self.assertEqual(value(g,'opacity',.51),1)
   if t is not None and t.text=='2 · Output loss':self.assertEqual(value(g,'opacity',.599),0);self.assertEqual(value(g,'opacity',.6),1)
 def test_actual_shared_js(self):
  import subprocess
  subprocess.run(['node',str(R/'scripts/test_distillation_player.cjs')],cwd=R,check=True)
 def test_static_and_source(self):
  for stem in ['kd-soft-target-alignment','fitnets-hint-then-output']:
   r=E.parse(A/(stem+'-still.svg')).getroot();self.assertFalse(r.findall('.//'+N+'animate'))
  for topic in ['response-based/hinton-distillation','feature-based/fitnets']:
   for lang in ['', '.zh-TW']:
    s=(R/f'docs/theory/model-compression/knowledge-distillation/{topic}/index{lang}.md').read_text()
    self.assertIn('tabindex="0"',s);self.assertIn('overflow-x:auto',s);self.assertIn('data-source-asset-urls',s);self.assertIn('https://arxiv.org/',s)
if __name__=='__main__':unittest.main()
