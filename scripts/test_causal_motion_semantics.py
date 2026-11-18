"""Independent SCM enumeration, dense timing/geometry and actual DOM regressions."""
from pathlib import Path
import subprocess,unittest,xml.etree.ElementTree as E
ROOT=Path(__file__).resolve().parents[1];N='{http://www.w3.org/2000/svg}'
def svg(stem):return E.parse(ROOT/f'docs/assets/concept-animations/{stem}-motion.svg').getroot()
def at(a,t):
 ts=list(map(float,a.get('keyTimes').split(';')));vs=list(map(float,a.get('values').split(';')));i=max(i for i,x in enumerate(ts) if x<=t)
 if i==len(ts)-1 or a.get('calcMode')=='discrete':return vs[i]
 return vs[i]+(vs[i+1]-vs[i])*(t-ts[i])/(ts[i+1]-ts[i])
class CausalSemantics(unittest.TestCase):
 def test_joint_enumeration(self):
  # Independent enumeration of P(U,X,Y), not copied display constants.
  joint={(u,x,y):.5*(.2+.6*u if x else .8-.6*u)*((.1+.4*x+.4*u) if y else (1-.1-.4*x-.4*u)) for u in [0,1] for x in [0,1] for y in [0,1]}
  self.assertAlmostEqual(sum(joint.values()),1)
  obs=[]
  for x in [0,1]:
   den=sum(p for (u,a,y),p in joint.items() if a==x);risk=sum(p for (u,a,y),p in joint.items() if a==x and y)/den;obs.append(risk)
   self.assertAlmostEqual(sum(p for (u,a,y),p in joint.items() if a==x and u)/den,[.2,.8][x]);self.assertAlmostEqual(risk,[.18,.82][x])
  self.assertAlmostEqual(obs[1]-obs[0],.64)
  for k in range(101):
   q=k/100;risks=[sum((q if u else 1-q)*(.1+.4*x+.4*u) for u in [0,1]) for x in [0,1]];self.assertAlmostEqual(risks[1]-risks[0],.4)
 def test_backdoor_timing(self):
  r=svg('backdoor-standardisation');bars={(e.get('x'),e.get('y')):e.find(N+'animate') for e in r.iter(N+'rect') if e.find(N+'animate') is not None}
  for k in range(1000):
   t=k/1000;w0=at(bars['62','252'],t)/230;w1=at(bars['439','252'],t)/230;p0=at(bars['62','315'],t)/230;p1=at(bars['439','315'],t)/230
   self.assertAlmostEqual(p0,.1+.4*w0);self.assertAlmostEqual(p1,.5+.4*w1);self.assertAlmostEqual(w0+w1,1)
 def test_collider_nonlinear_geometry(self):
  r=svg('collider-selection');self.assertTrue(any(e.text=='OR: S = 0' for e in r.iter(N+'text')));bar=next(e.find(N+'animate') for e in r.iter(N+'rect') if e.get('y')=='298' and e.find(N+'animate') is not None)
  for k in range(10000):
   t=k/10000;retention=1-min(1,max(0,(t-.18)/.42));expected=.25/(.25+.25*retention);self.assertAlmostEqual(at(bar,t)/475,expected,delta=.000025)
  self.assertAlmostEqual(at(bar,.999),475);self.assertAlmostEqual(at(bar,0),237.5)
 def test_fallback_labels_source(self):
  for stem in ['backdoor-standardisation','collider-selection']:
   r=svg(stem);self.assertEqual(len([e for e in r if e.get('class')=='still-layer']),1)
   for a in r.iter(N+'animate'):
    ts=list(map(float,a.get('keyTimes').split(';')));self.assertTrue(all(x<y for x,y in zip(ts,ts[1:])));self.assertEqual(len(ts),len(a.get('values').split(';')))
   for txt in r.iter(N+'text'):
    a=txt.find(N+'animate')
    if txt.get('class')=='val' and a is not None:
     for t in [.19,.3,.5,.59,.95]:self.assertEqual(at(a,t),0)
  for suffix in ['', '.zh-TW']:
   text=(ROOT/f'docs/theory/causal-inference/index{suffix}.md').read_text();self.assertEqual(text.count('data-source-asset-urls'),2);self.assertEqual(text.count('data-still-src'),2);self.assertEqual(text.count('tabindex="0"'),2);self.assertNotIn('\\\\mid',text);self.assertNotIn('\n$\n',text);self.assertIn('CC BY-SA 4.0',text)
 def test_actual_dom(self):subprocess.run(['node','scripts/test_causal_math.cjs'],cwd=ROOT,check=True)
if __name__=='__main__':unittest.main()
