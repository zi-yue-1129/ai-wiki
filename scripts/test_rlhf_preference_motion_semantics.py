"""Independent actual-SVG DPO and segment-comparison arithmetic and timing."""
import copy,math,unittest,xml.etree.ElementTree as E
from pathlib import Path
R=Path(__file__).resolve().parents[1];A=R/'docs/assets/concept-animations';N='{http://www.w3.org/2000/svg}'
STEMS=('rlhf-dpo-margin','rlhf-reward-sums')
def value(node,attr,t):
 a=next((a for a in node.findall(N+'animate') if a.get('attributeName')==attr),None)
 if a is None:return float(node.get(attr,'1' if attr=='opacity' else '0'))
 ts=list(map(float,a.get('keyTimes').split(';')));vs=list(map(float,a.get('values').split(';')))
 i=max(i for i,z in enumerate(ts) if z<=t)
 if i==len(ts)-1 or a.get('calcMode')=='discrete':return vs[i]
 return vs[i]+(vs[i+1]-vs[i])*(t-ts[i])/(ts[i+1]-ts[i])
def root(stem,kind='motion'):return E.parse(A/f'{stem}-{kind}.svg').getroot()
def sigmoid(x):return 1/(1+math.exp(-x))
def check_dpo(r):
 bars=[n for n in r.iter(N+'rect') if n.get('height') in ['22','20']]
 assert len(bars)==3
 end=next(g for g in r.findall(N+'g') if 'End:' in ''.join(g.itertext()))
 for k in range(10001):
  t=k/10000;p,q,pr=[value(b,'width',t)/315 for b in bars]
  assert abs(p+q-1)<1e-10
  margin=math.log(p/.5)-math.log(q/.5)
  assert abs(pr-sigmoid(margin))<1e-10
  if value(end,'opacity',t)>0:assert abs(p-.75)<1e-10
 assert abs(-math.log(pr)+math.log(.75))<1e-10
 for y in ['116','179']:
  dot=next(n for n in r.iter(N+'circle') if n.get('cy')==y)
  bar=bars[0 if y=='116' else 1]
  for t in [0,.1,.333,.749,.75,.99]:assert abs(value(dot,'cx',t)-172-value(bar,'width',t))<1e-10
 refs=[n for n in r.iter(N+'line') if n.get('stroke-dasharray')=='3 3'];assert len(refs)==2
 assert all(float(n.get('x1'))==172+315*.5 and not list(n) for n in refs)
def check_rewards(r):
 sums=[g for g in r.findall(N+'g') if g.find(N+'rect') is not None]
 assert len(sums)==6
 bar=next(n for n in r.iter(N+'rect') if n.get('height')=='19')
 dots=list(r.iter(N+'circle'));assert len(dots)==2
 for k in range(10001):
  t=k/10000;stage=sum(t>=a for a in [.08,.38,.7]);expected=[sum(a[:stage]) for a in [(1,2,1),(1,0,1)]]
  for row in range(2):
   active=[g for g in sums[3*row:3*row+3] if value(g,'opacity',t)>0]
   assert len(active)==(1 if stage else 0)
   if active:assert int(active[0].find(N+'text').text)==expected[row]
  if value(bar,'opacity',t)>0:
   assert stage==3
   assert abs(value(bar,'width',t)/320-sigmoid(expected[0]-expected[1]))<1e-10
 for t,x in [(0,154),(.08,154),(.38,258),(.7,362),(1,362)]:
  assert all(abs(value(d,'cx',t)-x)<1e-10 for d in dots)
class RLHFPreference(unittest.TestCase):
 def test_dpo_actual_geometry_reference_and_probability(self):check_dpo(root(STEMS[0]))
 def test_actual_reward_stages_and_complete_segment_probability(self):check_rewards(root(STEMS[1]))
 def test_static_endpoints(self):
  r=root(STEMS[0],'still');bars=[float(n.get('width')) for n in r.iter(N+'rect') if n.get('height') in ['22','20']];self.assertEqual(bars,[236.25,78.75,236.25])
  r=root(STEMS[1],'still');bar=next(n for n in r.iter(N+'rect') if n.get('height')=='19');self.assertAlmostEqual(float(bar.get('width'))/320,sigmoid(4-2))
 def test_negative_mutations(self):
  r=root(STEMS[0]);g=next(g for g in r.findall(N+'g') if 'End:' in ''.join(g.itertext()));g.find(N+'animate').set('keyTimes','0;.7;.78;1')
  with self.assertRaises(AssertionError):check_dpo(r)
  r=root(STEMS[1]);bar=next(n for n in r.iter(N+'rect') if n.get('height')=='19');bar.find(N+'animate').set('keyTimes','0;.56;1')
  with self.assertRaises(AssertionError):check_rewards(r)
  r=root(STEMS[1]);g=next(g for g in r.findall(N+'g') if g.find(N+'rect') is not None);g.find(N+'text').text='2'
  with self.assertRaises(AssertionError):check_rewards(r)
 def test_pages_sourcehook_focus_bilingual_and_ci_preservation(self):
  d=R/'docs/theory/paradigms/reinforcement-learning/learning-from-human-feedback'
  for topic,stem in zip(['dpo','reward-modelling'],STEMS):
   for lang in ['','.zh-TW']:
    text=(d/topic/f'index{lang}.md').read_text();self.assertIn('tabindex="0"',text);self.assertIn('width:640px;min-width:640px',text);self.assertIn('data-source-asset-urls',text);self.assertIn(f'data-motion-src="../../../../../assets/concept-animations/{stem}-motion.svg"',text);self.assertIn('CC BY-SA 4.0',text);self.assertIn('\\begin{aligned}',text)
  workflow=(R/'.github/workflows/concept-animation-validation.yml').read_text();self.assertIn('python scripts/test_rlhf_motion_browser.py',workflow);self.assertIn('test_adaptive_optimiser_labs_browser.py',workflow)
if __name__=='__main__':unittest.main()
