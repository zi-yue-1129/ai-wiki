"""Independent arithmetic and causal rendering checks for calibration examples."""
from pathlib import Path
import unittest
import xml.etree.ElementTree as E
N='{http://www.w3.org/2000/svg}'
A=Path(__file__).resolve().parents[1]/'docs/assets/concept-animations'
def root(stem,kind='motion'):return E.parse(A/f'{stem}-{kind}.svg').getroot()
def sample(a,t):
 ts=list(map(float,a.get('keyTimes').split(';')));vs=list(map(float,a.get('values').split(';')))
 i=next((i for i in range(len(ts)-1) if ts[i]<=t<ts[i+1]),len(ts)-2)
 return vs[i]+(t-ts[i])/(ts[i+1]-ts[i])*(vs[i+1]-vs[i])
class Calibration(unittest.TestCase):
 def test_ece_arithmetic_and_bar_geometry(self):
  for kind in ['motion','still']:
   r=root('ece-binned-calibration',kind); total=0
   for i,(n,k,c) in enumerate([(10,2,.25),(20,8,.55),(10,6,.85)]):
    acc=k/n;gap=abs(c-acc);term=n/40*gap;total+=term
    for x,v,col in [(142+185*i,c,'#d6edf5'),(151+185*i,acc,'#f0b15b')]:
     b=next(e for e in r.iter(N+'rect') if e.get('x')==str(x) and e.get('fill')==col)
     self.assertAlmostEqual(float(b.get('height')),163*v);self.assertAlmostEqual(float(b.get('y')),275-163*v)
    texts=[e.text for e in r.iter(N+'text')]
    self.assertIn(f'{term:.4f}',texts);self.assertIn(f'Δ {gap:.2f}',texts)
   self.assertAlmostEqual(total,.15);self.assertIn(f'{total:.4f}',texts)
 def test_weighted_highlight_visible_and_after_gap(self):
  r=root('ece-binned-calibration');nodes=list(r);panel=next(e for e in nodes if e.get('x')=='37')
  for i in range(3):
   gap=next(e for e in nodes if e.get('x')==str(128+185*i));term=next(e for e in nodes if e.get('x')==str([135,242,352][i]))
   self.assertLess(nodes.index(panel),nodes.index(term))
   ga=gap.find(N+'animate');ta=term.find(N+'animate');start=i/3
   self.assertGreater(sample(ga,start+.08),.9);self.assertEqual(sample(ta,start+.08),0)
   self.assertGreater(sample(ta,start+.23),.7)
   guide=next(e for e in nodes if e.get('id')==f'weighted-guide-{i}')
   cy=next(a for a in guide if a.get('attributeName')=='cy')
   self.assertAlmostEqual(sample(cy,start+.20),348)
 def test_ensemble_mean_range_and_forward_only_arrival(self):
  for kind in ['motion','still']:
   r=root('deep-ensemble-spread',kind);circles=list(r.iter(N+'circle'))
   for j,ps in enumerate([(.72,.76,.8),(.2,.5,.8)]):
    mean=sum(ps)/3
    self.assertIn(f'μ={mean:.2f}',[e.text for e in r.iter(N+'text')])
    rng=next(e for e in r.iter(N+'rect') if e.get('y')==str(138+j*143))
    self.assertAlmostEqual(float(rng.get('x')),172+433*min(ps));self.assertAlmostEqual(float(rng.get('width')),433*(max(ps)-min(ps)))
    for e,p in zip(circles[j*3:j*3+3],ps):
     if kind=='still':self.assertAlmostEqual(float(e.get('cx')),172+433*p)
     else:
      a=e.find(N+'animate');vs=list(map(float,a.get('values').split(';')))
      self.assertEqual(vs,sorted(vs));self.assertAlmostEqual(vs[-1],172+433*p)
      for t in [.42,.5,.9,.999]:self.assertAlmostEqual(sample(a,t),172+433*p)
    if kind=='motion':
     self.assertEqual(sample(rng.find(N+'animate'),.42),0)
     label=next(e for e in r.iter(N+'text') if e.text==f'μ={mean:.2f}')
     self.assertEqual(sample(label.find(N+'animate'),.42),0)
 def test_bilingual_hooks_and_boundaries(self):
  D=A.parents[1]/'theory/paradigms/probabilistic/uncertainty-calibration'
  for topic in ['expected-calibration-error','deep-ensembles']:
   for lang in ['', '.zh-TW']:
    s=(D/f'{topic}{lang}.md').read_text();self.assertIn('<img data-source-asset-urls',s);self.assertIn('data-still-src=',s);self.assertIn('tabindex="0"',s)
if __name__=='__main__':unittest.main()
