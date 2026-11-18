"""Enumerated segmentation, shared alpha, actual SMIL interpolation, and causal path."""
from pathlib import Path
import unittest,xml.etree.ElementTree as E
N='{http://www.w3.org/2000/svg}';P=Path(__file__).resolve().parents[1];A=P/'docs/assets/concept-animations'
def load(stem,mode='motion'):return E.parse(A/f'{stem}-{mode}.svg').getroot()
def val(e,t):
 a=e.find(N+'animate');ts=list(map(float,a.get('keyTimes').split(';')));vs=list(map(float,a.get('values').split(';')))
 i=min(len(ts)-2,max(i for i,x in enumerate(ts) if x<=t));u=0 if a.get('calcMode')=='discrete' else (t-ts[i])/(ts[i+1]-ts[i]);return vs[i]+u*(vs[i+1]-vs[i])
class Unigram(unittest.TestCase):
 def test_enumeration_and_viterbi(self):
  vocab={'a':.1,'b':.1,'ab':.4,'aba':.08,'bab':.08,'abab':.05}
  def paths(x):
   if not x:return [((),1.)]
   return [((p,)+s,v*q) for p,v in vocab.items() if x.startswith(p) for s,q in paths(x[len(p):])]
  ps=paths('abab');self.assertEqual(len(ps),7)
  for a,b in zip(sorted(v for _,v in ps),sorted([.16,.05,.008,.008,.004,.004,.0001])):self.assertAlmostEqual(a,b)
  self.assertEqual(max(ps,key=lambda z:z[1])[0],('ab','ab'))
 def test_shared_alpha_dense_actual_interpolation(self):
  r=load('unigram-sampling-alpha');es={e.get('id'):e for e in r.iter() if e.get('id')};scores=[.16,.05,.008,.008,.004,.004,.0001]
  for j in range(10001):
   t=j/10000;a=.3+(val(es['alpha-handle'],t)-88)*2.7/462;p=[s**a for s in scores];z=sum(p);expected=[*p[:3],sum(p[3:])];actual=[val(es[f'probability-{k}'],t) for k in range(4)]
   self.assertAlmostEqual(sum(actual),206,places=4)
   for k in range(4):self.assertLess(abs(actual[k]-206*expected[k]/z),.01)
  for e in r.iter(N+'text'):
   if e.text=='3.0':self.assertGreaterEqual(float(e.get('x')),550+11.5+5)
 def test_single_path_and_causal_edge(self):
  r=load('unigram-viterbi-lattice');es={e.get('id'):e for e in r.iter() if e.get('id')};m=es['path-marker'];ax,ay=m.findall(N+'animate')
  def v(a,t):
   e=E.Element('x');e.append(a);return val(e,t)
  self.assertFalse(list(r.iter(N+'animateMotion')))
  for j in range(10001):
   t=j/10000;u=min(t/.45,2);seg=min(int(u),1);q=u-seg;x,y=v(ax,t),v(ay,t)
   self.assertAlmostEqual(x,65+250*u,places=4);self.assertLess(abs(y-(224-226*q*(1-q))),.002)
   if t<.45:self.assertEqual(val(es['edge-0'],t),7);self.assertEqual(val(es['edge-1'],t),4)
   elif t<.9:self.assertEqual(val(es['edge-0'],t),4);self.assertEqual(val(es['edge-1'],t),7)
   else:self.assertAlmostEqual(x,565);self.assertAlmostEqual(y,224)
 def test_bilingual_sources(self):
  for lang in ['', '.zh-TW']:
   s=(P/f'docs/theory/models/llm/tokenisation/sentencepiece{lang}.md').read_text()
   self.assertEqual(s.count('<img data-source-asset-urls'),2);self.assertEqual(s.count('width:640px;min-width:640px'),2);self.assertNotIn('\n$\n',s)
   self.assertIn('0.01',s);self.assertIn('206',s)
if __name__=='__main__':unittest.main()
