"""Actual CTDE SVG geometry/timing, numeric targets and adversarial regressions."""
from pathlib import Path
import unittest,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1];A=R/'docs/assets/concept-animations';N='{http://www.w3.org/2000/svg}'
STEMS=['maddpg-actor-gradient','maddpg-joint-bootstrap','mappo-shared-advantage','mappo-backward-gae']
def root(stem,kind='motion'):return ET.parse(A/f'{stem}-{kind}.svg').getroot()
def sample(a,t):
 v=list(map(float,a.get('values').split(';')));k=list(map(float,a.get('keyTimes').split(';')))
 for i in range(len(k)-1):
  if t<k[i+1]:return v[i] if a.get('calcMode')=='discrete' else v[i]+(v[i+1]-v[i])*(t-k[i])/(k[i+1]-k[i])
 return v[-1]
def anim(e,n):return e.find(N+f"animate[@attributeName='{n}']")
def packet(r,i):return [e for e in r.findall(N+'circle') if e.get('id')][i]
def check_gae(r):
 texts=[e.text for e in r.findall(N+'text')];rs=[.2,.4,.6];vs=[1,.8,.5,0];ds=[rs[i]+.9*vs[i+1]-vs[i] for i in range(3)];As=[0]*4
 for i in reversed(range(3)):As[i]=ds[i]+.9*.8*As[i+1]
 for v,fmt in zip(As,['.5f','.3f','.3f']):assert f'A={v:{fmt}}' in texts
 p0,p1=packet(r,0),packet(r,1)
 assert sample(anim(p0,'cx'),.52)==398 and sample(anim(p1,'cx'),.81)==204
 assert sample(anim(p1,'opacity'),.52)==0
class MarlSource(unittest.TestCase):
 def test_td_actual_printed_values_and_terminal(self):
  for kind in ['motion','still']:
   r=root(STEMS[1],kind);texts=[e.text for e in r.findall(N+'text')]
   self.assertEqual(r.find(N+"path[@id='target-to-bootstrap']").get('d'),'M516 197 L516 239 L373 239 L373 263')
   for v in ['1.80',f'{.5+.9*1.8:.2f}',f'δ = {.5+.9*1.8-1.4:.2f}']:self.assertIn(v,texts)
  self.assertAlmostEqual(.5+.9*(1-1)*1.8,.5)
 def test_gae_values_reverse_direction_and_negative(self):
  r=root(STEMS[3]);check_gae(r)
  next(e for e in r.findall(N+'text') if e.text=='A=0.00784').text='A=0.0784'
  with self.assertRaises(AssertionError):check_gae(r)
  r=root(STEMS[3]);anim(packet(r,1),'opacity').set('values','1;1;1;1;1')
  with self.assertRaises(AssertionError):check_gae(r)
 def test_causal_visible_arrivals(self):
  bounds=[[(.04,.32,(420,159)),(.04,.32,(420,192)),(.4,.64,(188,91)),(.72,.92,(417,317))],[(.08,.2,(238,148)),(.3,.42,(431,148)),(.52,.68,(373,263)),(.78,.88,(466,292))],[(.04,.28,(438,127)),(.04,.28,(438,192)),(.36,.62,(459,306)),(.7,.9,(303,208))],[(.36,.52,(398,269)),(.65,.81,(204,269))]]
  for stem,entries in zip(STEMS,bounds):
   r=root(stem)
   self.assertEqual(len(r.findall('.//'+N+'animateMotion')),0)
   for i,(start,end,xy) in enumerate(entries):
    p=packet(r,i)
    self.assertEqual(sample(anim(p,'opacity'),start-.001),0);self.assertEqual(sample(anim(p,'opacity'),end),1);self.assertEqual(sample(anim(p,'opacity'),end+.01),0)
    for attr,v in zip(['cx','cy'],xy):self.assertAlmostEqual(sample(anim(p,attr),end),v)
    for j in range(1001):
     self.assertTrue(0<=sample(anim(p,'cx'),j/1000)<=640);self.assertTrue(0<=sample(anim(p,'cy'),j/1000)<=360)
   for a in r.findall('.//'+N+'animate'):self.assertEqual(a.get('begin'),'0s');self.assertEqual(a.get('dur'),'12s')
 def test_backward_glow_dependency(self):
  r=root(STEMS[3]);glows=[e for e in r if e.get('class')=='glow']
  for t,i in [(.1,0),(.25,1),(.6,2),(.9,3)]:self.assertEqual([sample(anim(e,'opacity'),t) for e in glows],[.85 if j==i else 0 for j in range(4)])
 def test_bilingual_sources_and_fallback(self):
  for topic in ['maddpg','mappo']:
   for lang in ['', '.zh-TW']:
    s=(R/f'docs/theory/paradigms/reinforcement-learning/multi-agent-rl/{topic}/index{lang}.md').read_text();self.assertEqual(s.count('class="marl-source-scroll" tabindex="0"'),2);self.assertEqual(s.count('data-source-asset-urls'),2)
    if topic=='mappo':self.assertIn('1-\\epsilon,1+\\epsilon',s)
  for stem in STEMS:
   self.assertIn('prefers-reduced-motion',(A/f'{stem}-motion.svg').read_text());r=root(stem,'still');self.assertEqual(r.get('width'),'640');self.assertFalse(any('animate' in e.tag for e in r.iter()))
if __name__=='__main__':unittest.main()
