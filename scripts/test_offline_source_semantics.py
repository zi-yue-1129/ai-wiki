"""Actual SVG geometry, residual signs, simultaneous CQL gradient and label timing."""
from pathlib import Path
import unittest,xml.etree.ElementTree as E,math
R=Path(__file__).resolve().parents[1];A=R/'docs/assets/concept-animations';N='{http://www.w3.org/2000/svg}';STEMS=['offline-iql-expectile','offline-cql-conservative']
def root(s,k='motion'):return E.parse(A/f'{s}-{k}.svg').getroot()
def sample(an,t):
 v=list(map(float,an.get('values').split(';')));ts=list(map(float,an.get('keyTimes').split(';')))
 for i in range(len(ts)-1):
  if t<ts[i+1]:return v[i] if an.get('calcMode')=='discrete' else v[i]+(v[i+1]-v[i])*(t-ts[i])/(ts[i+1]-ts[i])
 return v[-1]
def num(el,attr,t):
 an=el.find(N+f"animate[@attributeName='{attr}']");return float(el.get(attr)) if an is None else sample(an,t)
def bar(r,y,color):return next(e for e in r.findall(N+'rect') if e.get('y')==str(y) and e.get('fill')==color)
def updates():
 a,b=2.,5.;out=[(a,b)]
 for _ in range(4):p=1/(1+math.exp(a-b));a,b=a-.5*(-p+a-2),b-.5*p;out.append((a,b))
 return out
def check_labels(r):
 iql='IQL' in r.find(N+'title').text
 for el in r.iter():
  label=''.join(el.itertext()).strip();an=el.find(N+"animate[@attributeName='opacity']")
  if an is None:continue
  for j in range(1000):
   t=j/1000
   if sample(an,t)<.99:continue
   if label in ['2.00','2.73','5.00','3.32']:
    b=bar(r,171 if label in ['2.00','2.73'] else 281,'#0a8581' if label in ['2.00','2.73'] else '#d67c39');assert abs(num(b,'width',t)/54-float(label))<.005
   elif label.endswith('%'):
    b=bar(r,int(next(el.iter(N+'text')).get('y'))-17,'#0a8581');assert abs(num(b,'width',t)/255-float(label[:-1])/100)<.005
   elif label in ['Mean 2.33','V = 3.17']:
    line=next(e for e in r.findall(N+'line') if e.find(N+'animate') is not None);assert abs((num(line,'x1',t)-86)/54-float(label.split()[-1]))<.005
class OfflineSource(unittest.TestCase):
 def test_expectile_sign_and_geometry(self):
  v=19/6;grad=sum(-2*(.8 if q-v>=0 else .2)*(q-v) for q in [1,2,4]);self.assertAlmostEqual(grad,0)
  self.assertGreater(sum(-2*(.2 if q-v>=0 else .8)*(q-v) for q in [1,2,4]),0)
  r=root(STEMS[0]);line=next(e for e in r.findall(N+'line') if e.find(N+'animate') is not None);self.assertAlmostEqual(num(line,'x1',.1),86+54*7/3);self.assertAlmostEqual(num(line,'x1',.6),86+54*v)
  for y,q,col in [(140,1,'#3975cb'),(205,2,'#3975cb'),(270,4,'#0a8581')]:self.assertEqual(float(bar(r,y,col).get('width')),54*q)
 def test_weight_geometry_and_common_baseline_cancellation(self):
  probs=[math.exp(.5*q) for q in [1,2,4]];probs=[p/sum(probs) for p in probs]
  for k in ['motion','still']:
   r=root(STEMS[0],k)
   for y,p in zip([418,454,490],probs):self.assertAlmostEqual(num(bar(r,y,'#0a8581'),'width',.85)/255,p)
  shifted=[math.exp(.5*(q-19/6)) for q in [1,2,4]];self.assertTrue(all(abs(x/sum(shifted)-y)<1e-12 for x,y in zip(shifted,probs)))
 def test_cql_simultaneous_gradient_and_data_distribution(self):
  a,b=updates()[-1];self.assertAlmostEqual(a,2.730157113,places=4);self.assertAlmostEqual(b,3.320417687,places=4);self.assertGreater(b,a)
  self.assertLess(math.log1p(math.exp(b-a)),math.log1p(math.exp(3)))
  for k in ['motion','still']:
   r=root(STEMS[1],k);self.assertAlmostEqual(num(bar(r,171,'#0a8581'),'width',.85)/54,a);self.assertAlmostEqual(num(bar(r,281,'#d67c39'),'width',.85)/54,b)
  pb=1/(1+math.exp(-3));self.assertAlmostEqual((1-pb)-1,-pb);self.assertGreater(pb,0)
 def test_cql_penalty_matches_actual_displayed_q(self):
  r=root(STEMS[1]);a=bar(r,171,'#0a8581');b=bar(r,281,'#d67c39');p=bar(r,498,'#3975cb')
  for j in range(1001):
   t=j/1000;expected=math.log1p(math.exp((num(b,'width',t)-num(a,'width',t))/54));self.assertLess(abs(num(p,'width',t)/80-expected),.0002)
 def test_actual_numeric_labels_and_negative(self):
  for s in STEMS:check_labels(root(s))
  r=root(STEMS[1]);e=next(e for e in r.iter() if e.find(N+'animate') is not None and ''.join(e.itertext()).strip()=='2.73');e.find(N+'animate').set('values','0;0;1;1;0;0')
  with self.assertRaises(AssertionError):check_labels(r)
 def test_source_hooks_controls_and_special_size(self):
  for topic in ['iql','cql']:
   for lang in ['', '.zh-TW']:
    s=(R/f'docs/theory/paradigms/reinforcement-learning/offline-rl/{topic}/index{lang}.md').read_text();self.assertEqual(s.count('class="offline-source-scroll" tabindex="0"'),1);self.assertIn('data-source-asset-urls',s);self.assertFalse(any(ord(c)<32 and c not in '\n\r' for c in s))
  for s in STEMS:
   self.assertIn('prefers-reduced-motion',(A/f'{s}-motion.svg').read_text());r=root(s,'still');self.assertEqual(r.get('viewBox'),'0 0 440 548');self.assertFalse(any('animate' in e.tag for e in r.iter()))
if __name__=='__main__':unittest.main()
