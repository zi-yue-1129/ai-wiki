"""Test actual PBT/FTW geometry and causal schedules, including negative mutations."""
from pathlib import Path
import unittest,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1];A=R/'docs/assets/concept-animations';N='{http://www.w3.org/2000/svg}';STEMS=['pbt-exploit-explore','ftw-two-level-learning']
def root(stem,kind='motion'):return ET.parse(A/f'{stem}-{kind}.svg').getroot()
def sample(a,t):
 v=list(map(float,a.get('values').split(';')));k=list(map(float,a.get('keyTimes').split(';')))
 for i in range(len(k)-1):
  if t<k[i+1]:return v[i] if a.get('calcMode')=='discrete' else v[i]+(v[i+1]-v[i])*(t-k[i])/(k[i+1]-k[i])
 return v[-1]
def anim(e,name):return e.find(N+f"animate[@attributeName='{name}']")
def verify_pbt(r):
 c=r.find(N+"circle[@id='pbt-copy-packet']");assert sample(anim(c,'cy'),.66)==273
 result=next(e for e in r.findall(N+'text') if e.text=='0.010 → 0.012');assert sample(anim(result,'opacity'),.66)==0;assert sample(anim(result,'opacity'),.72)==1
class PopulationMotion(unittest.TestCase):
 def test_pbt_scale_snapshot_and_perturbation(self):
  self.assertAlmostEqual(.010*1.2,.012)
  for kind in ['motion','still']:
   r=root(STEMS[0],kind);bars=[e for e in r.findall(N+'rect') if e.get('x')=='92' and e.get('height')=='10' and e.get('fill')!='#e4edf5'];self.assertEqual(len(bars),4)
   for e,s in zip(bars,[.92,.74,.61,.4]):self.assertAlmostEqual(float(e.get('width'))/112,s);self.assertIsNone(e.find(N+'animate'))
   self.assertIn('weights + settings',[e.text for e in r.findall(N+'text')])
 def test_exploit_before_explore_and_negative(self):
  r=root(STEMS[0]);verify_pbt(r);c=r.find(N+"circle[@id='pbt-copy-packet']")
  for i in range(33):
   u=i/32;t=.44+.22*u;self.assertAlmostEqual(sample(anim(c,'cy'),t),141+132*(3*u*u-2*u**3));self.assertAlmostEqual(sample(anim(c,'cx'),t),(1-u)**3*278+3*(1-u)**2*u*312+3*(1-u)*u*u*309+u**3*279)
  result=next(e for e in r.findall(N+'text') if e.text=='0.010 → 0.012');anim(result,'opacity').set('values','1;1;1')
  with self.assertRaises(AssertionError):verify_pbt(r)
 def test_distinct_pbt_stages_and_resume(self):
  r=root(STEMS[0]);es=[e for e in r.findall(N+'rect') if e.get('class')=='moving' and e.get('y')=='52'];self.assertEqual(len(es),4)
  for t,idx in [(.1,0),(.3,1),(.5,2),(.8,3),(.95,0)]:self.assertEqual([sample(anim(e,'opacity'),t) for e in es],[int(i==idx) for i in range(4)])
 def test_ftw_feedback_and_two_tiers(self):
  r=root(STEMS[1]);self.assertEqual(r.find(N+"path[@id='win-to-outer']").get('d'),'M600 128 H620 V270 H509 V279');cs=[r.find('.//'+N+f"circle[@id='ftw-stage-{i}']") for i in range(3)]
  for c,t,xy in zip(cs,[.4,.62,.76],[(445,159),(162,279),(509,279)]):self.assertAlmostEqual(sample(anim(c,'cx'),t),xy[0]);self.assertAlmostEqual(sample(anim(c,'cy'),t),xy[1])
  self.assertEqual(sample(anim(cs[1],'opacity'),.4),0);self.assertEqual(sample(anim(cs[2],'opacity'),.62),0)
  for i in range(1001):
   for c in cs:
    x=sample(anim(c,'cx'),i/1000);y=sample(anim(c,'cy'),i/1000);self.assertTrue(0<=x<=640 and 0<=y<=360)
  self.assertIn('PBT-evolved',[e.text for e in r.findall(N+'text')])
 def test_bilingual_source_and_static(self):
  for stem,topic in zip(STEMS,['pbt','ftw']):
   for kind in ['motion','still']:
    r=root(stem,kind);self.assertEqual((r.get('width'),r.get('height')),('640','360'))
   self.assertFalse(root(stem,'still').findall('.//'+N+'animate'));self.assertIn('prefers-reduced-motion',root(stem).find(N+'style').text)
   for lang in ['', '.zh-TW']:
    s=(R/f'docs/theory/paradigms/reinforcement-learning/multi-agent-rl/population-based-training/{topic}/index{lang}.md').read_text();self.assertIn('class="population-source-scroll" tabindex="0" role="region"',s);self.assertIn(stem+'-still.svg" data-motion-src=',s)
if __name__=='__main__':unittest.main()
