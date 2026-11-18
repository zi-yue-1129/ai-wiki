"""Numerical and causal contracts read the actual four DDPG SVG pairs."""
import bisect, copy, math, re, unittest
from pathlib import Path
from xml.etree import ElementTree as E
R=Path(__file__).resolve().parents[1]; A=R/'docs/assets/concept-animations'; N='{http://www.w3.org/2000/svg}'
def root(stem,kind='motion'):return E.parse(A/f'ddpg-{stem}-{kind}.svg').getroot()
def value(a,t):
 ts=list(map(float,a.get('keyTimes').split(';')));vs=[list(map(float,v.split())) for v in a.get('values').split(';')];i=min(len(ts)-2,max(0,bisect.bisect_right(ts,t)-1));f=0 if a.get('calcMode')=='discrete' else (t-ts[i])/(ts[i+1]-ts[i]);return [u+f*(v-u) for u,v in zip(vs[i],vs[i+1])]
def xycurve(t):return [501+74*t-12*t*t,215-206*t+102*t*t]
def assert_curve(test,rt):
 c=next(c for c in rt.findall(N+'circle') if c.get('class')=='moving');xs,ys=c.findall(N+'animate')
 for j in range(1001):
  u=j/1000;x=value(xs,u)[0];y=value(ys,u)[0];q=(74-math.sqrt(74**2-48*(x-501)))/24
  test.assertLess(abs(y-xycurve(q)[1]),.004)
class DDPGSource(unittest.TestCase):
 def test_actor_curve_and_negative_geometry(self):
  rt=root('actor-gradient');assert_curve(self,rt)
  bad=copy.deepcopy(rt);c=next(c for c in bad.findall(N+'circle') if c.get('class')=='moving');c.findall(N+'animate')[1].set('values',';'.join(['176']*len(c.findall(N+'animate')[1].get('values').split(';'))))
  with self.assertRaises(AssertionError):assert_curve(self,bad)
 def test_actor_forward_then_backward_then_update(self):
  rt=root('actor-gradient');gs=[g for g in rt.findall(N+'g') if g.get('class')=='moving'];f,b=gs
  self.assertEqual(value(f.find(N+'animateTransform'),.3),[417,125]);self.assertEqual(value(b.find(N+'animateTransform'),.35),[417,155]);self.assertEqual(value(b.find(N+'animateTransform'),.70),[177,156])
  c=next(c for c in rt.findall(N+'circle') if c.get('class')=='moving');a=c.find(N+'animate');self.assertEqual(value(a,0),value(a,.75));self.assertGreater(value(a,.95)[0],value(a,.75)[0])
  for kind in ['still','motion']:
   dots=[c for c in root('actor-gradient',kind).iter(N+'circle') if c.get('fill')=='#db9638' and not c.findall(N+'animate')]
   self.assertTrue(dots)
   for c in dots:
    for k,v in zip(['cx','cy'],xycurve(.9)):self.assertAlmostEqual(float(c.get(k)),v)
 def test_polyak_actual_positions_and_completion_order(self):
  rt=root('polyak-target');cs=[c for c in rt.findall(N+'circle') if c.get('class')=='moving'];target=0
  for i,theta in enumerate([0,1,-.2,.8,.4]):
   if i:target=.2*theta+.8*target
   t=i*.2+(.12 if i else 0)
   self.assertAlmostEqual(value(cs[0].find(N+'animate'),t)[0],182+200*theta)
   self.assertAlmostEqual(value(cs[1].find(N+'animate'),t)[0],182+200*target)
  groups=[g for g in rt.findall(N+'g') if g.get('class')=='reveal']
  for i,g in enumerate(groups,1):self.assertEqual(value(g.find(N+'animate'),i*.2+.119),[0])
 def test_ou_and_iid_actual_coordinates(self):
  for kind in ['motion','still']:
   rt=root('ou-noise',kind);self.assertIn('M48 227 H292 M349 227 H593',[p.get('d') for p in rt.iter(N+'path')]);v=0
   for i,xi in enumerate([.8,.7,-.3,-.9,-.8,.6],1):
    v=.75*v+.2*xi
    for x,y in [(54+38*i,227-100*v),(354+38*i,227-100*.2*xi)]:
     c=next(c for c in rt.iter(N+'circle') if float(c.get('cx','-1'))==x);self.assertAlmostEqual(float(c.get('cy')),y,delta=.0051)
  rt=root('ou-noise');groups=[g for g in rt.findall(N+'g') if g.get('class')=='reveal'];self.assertEqual(len(groups),12)
  for i in range(6):self.assertEqual(groups[2*i].find(N+'animate').attrib,groups[2*i+1].find(N+'animate').attrib)
 def test_replay_causal_arrivals_and_terminal_arithmetic(self):
  rt=root('replay-bootstrap');a=rt.find('.//'+N+'animateTransform');self.assertEqual(value(a,.35),[340,235]);self.assertEqual(value(a,.5),[445,235])
  for label,earliest in [('Q′ = 1.50',.35),('y = 1.75',.5),('y = 1.20',.7)]:
   g=next(g for g in rt.iter(N+'g') if label in ''.join(g.itertext()));self.assertEqual(value(g.find(N+'animate'),earliest-1e-6),[0])
  self.assertAlmostEqual(.4+.9*(1-0)*1.5,1.75);self.assertAlmostEqual(1.2+.9*(1-1)*1.5,1.2)
  for kind in ['motion','still']:
   text=''.join(root('replay-bootstrap',kind).itertext())
   for label in ['done=0','done=1','y = 1.75','y = 1.20']:self.assertIn(label,text)
 def test_static_and_bilingual_source_contract(self):
  stems=['actor-gradient','polyak-target','replay-bootstrap','ou-noise']
  for stem in stems:self.assertFalse(any('animate' in x.tag for x in root(stem,'still').iter()))
  for suffix in ['', '.zh-TW']:
   p=R/f'docs/theory/paradigms/reinforcement-learning/policy-gradient-and-actor-critic/ddpg/index{suffix}.md';s=p.read_text();self.assertEqual(s.count('class="ddpg-motion-scroll" tabindex="0"'),4);self.assertEqual(s.count('width:640px;min-width:640px'),4)
   for stem in stems:
    from verify_concept_motion import verify_source_pair
    self.assertEqual(verify_source_pair(p,s,'ddpg-'+stem),[])
   for block in re.findall(r'\\\[(.*?)\\\]',s,re.S):
    self.assertNotIn(r'\(',block);self.assertNotIn(r'\)',block)
   self.assertIn('d_i',s);self.assertIn('0.2848',s);self.assertIn('Euler',s)
 def test_ci_preserves_browser_and_executes_semantics(self):
  import yaml
  cfg=yaml.safe_load((R/'.github/workflows/concept-animation-validation.yml').read_text());runs='\n'.join(s.get('run','') for j in cfg['jobs'].values() for s in j['steps'])
  self.assertIn('python scripts/test_ddpg_motion_browser.py',runs);self.assertIn('python scripts/test_ddpg_motion_semantics.py',runs)
if __name__=='__main__':unittest.main()
