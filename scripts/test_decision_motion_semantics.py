"""Counterfactual sampled passage and event-causal revaluation SVG checks."""
from pathlib import Path
import bisect,unittest,xml.etree.ElementTree as E
P=Path(__file__).resolve().parents[1];N='{http://www.w3.org/2000/svg}'
def root(stem):return E.parse(P/f'docs/assets/concept-animations/{stem}-motion.svg').getroot()
def sample(e,attr,t):
 a=next((x for x in e.findall(N+'animate') if x.get('attributeName')==attr),None)
 if a is None:return float(e.get(attr))
 vs=list(map(float,a.get('values').split(';')));ts=list(map(float,a.get('keyTimes').split(';')));i=min(bisect.bisect_right(ts,t)-1,len(vs)-2)
 if a.get('calcMode')=='discrete':return vs[i]
 f=(t-ts[i])/(ts[i+1]-ts[i]);return vs[i]*(1-f)+vs[i+1]*f
class DecisionTests(unittest.TestCase):
 def test_sampled_first_passages_and_reveal_alignment(self):
  r=root('ddm-first-passage');pts=[tuple(map(float,p.split(','))) for p in next(r.iter(N+'polyline')).get('points').split()]
  levels=[(183-y)/113 for x,y in pts]
  for threshold,k in [(.4,7),(.78,15)]:self.assertEqual(next(i for i,z in enumerate(levels) if abs(z)>=threshold),k)
  box=next(r.iter(N+'clipPath')).find(N+'rect');line=next(e for e in r.iter(N+'line') if e.find(N+'animate') is not None)
  circles=list(r.iter(N+'circle'))
  for i in range(10001):
   t=i/10001;x=70+500*t
   self.assertAlmostEqual(70+sample(box,'width',t),x,places=9);self.assertAlmostEqual(sample(line,'x1',t),x,places=9)
   for c,k in zip(circles,[7,15]):self.assertEqual(sample(c,'opacity',t),int(t>=k/16));self.assertAlmostEqual(float(c.get('cx')),70+31.25*k)
 def test_revaluation_actual_values_choice_and_event_time(self):
  r=root('mbmf-revaluation');cursor=next(e for e in r.iter(N+'circle') if e.find(N+'animate') is not None)
  bars=[e for e in r.iter(N+'rect') if e.find(N+'animate') is not None]
  groups=[e for e in r.iter(N+'g') if e.find(N+'animate') is not None]
  self.assertAlmostEqual((1-.7)*5+.7*0,1.5)
  for i in range(10001):
   t=i/10001;x=sample(cursor,'cx',t);rv=x>=223;fb=x>=449
   self.assertEqual(sample(bars[0],'width',t),0 if rv else 180)
   self.assertEqual(sample(bars[1],'width',t),54 if fb else 180)
   for g in groups:
    tx=g.find(N+'text');s=tx.text;col=tx.get('x')
    active=(not rv if s=='+5' else rv) if col=='176' else ((not fb if s=='A' else fb) if col=='578' else (not rv if s=='A' else rv))
    self.assertEqual(sample(g,'opacity',t),int(active))
  for x in [223,449]:
   t=(x-48)/542
   for dt in [-1e-7,1e-7]:
    self.assertAlmostEqual(sample(cursor,'cx',t+dt),x+542*dt,places=8)
 def test_bilingual_source_and_caveats(self):
  for topic,stem in [('diffusion-model','ddm-first-passage'),('model-based-vs-model-free','mbmf-revaluation')]:
   for lang in ['', '.zh-TW']:
    s=(P/f'docs/brain-mind/decision-reward/{topic}/index{lang}.md').read_text()
    self.assertIn('data-source-asset-urls',s);self.assertIn('width:640px;min-width:640px',s);self.assertIn(f'{stem}-still.svg)',s)
    if topic=='diffusion-model':self.assertIn('first sampled' if not lang else '首次採樣',s);self.assertIn('counterfactual' if not lang else '反事實',s)
    else:self.assertIn(r'Q_A\leftarrow',s);self.assertIn(r'\begin{gathered}',s);self.assertNotIn('((5,2))',s)
if __name__=='__main__':unittest.main()
