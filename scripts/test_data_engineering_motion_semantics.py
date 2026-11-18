"""Independently reconstruct MinHash ranks and Bayesian LF vote fusion."""
from pathlib import Path
import itertools,math,unittest,xml.etree.ElementTree as E
N='{http://www.w3.org/2000/svg}';A=Path(__file__).resolve().parents[1]/'docs/assets/concept-animations'
def root(stem,kind='motion'):return E.parse(A/f'{stem}-{kind}.svg').getroot()
class DataMotion(unittest.TestCase):
 def test_valid_permutations_generate_displayed_signature(self):
  sa=set('abcd');sb=set('abce');self.assertEqual(len(sa&sb)/len(sa|sb),.6)
  orders=['abcde','bcade','eabcd','dabce'];aa=[];bb=[]
  for order in orders:
   ranks={c:i+1 for i,c in enumerate(order)};aa.append(min(ranks[c] for c in sa));bb.append(min(ranks[c] for c in sb))
  for kind in ['motion','still']:
   r=root('minhash-lsh-band-collision',kind)
   for y,want in [('173',aa),('251',bb)]:self.assertEqual([int(e.text) for e in r.iter(N+'text') if e.get('y')==y],want)
  self.assertEqual(sum(a==b for a,b in zip(aa,bb))/4,.5);self.assertEqual(aa[:2],bb[:2]);self.assertNotEqual(aa[2:],bb[2:])
 def test_uniform_permutation_collision_probability(self):
  equal=0
  for order in itertools.permutations('abcde'):
   rank={c:i for i,c in enumerate(order)};equal+=min(rank[c] for c in 'abcd')==min(rank[c] for c in 'abce')
  self.assertEqual(equal/120,.6)
 def test_vote_posteriors_and_unrounded_bar_geometry(self):
  for kind in ['motion','still']:
   r=root('weak-supervision-vote-fusion',kind);texts={(e.get('x'),e.get('y')):e.text for e in r.iter(N+'text')}
   for j,x in enumerate([138,191,244,297]):
    odds=1
    for y,acc in zip([169,222,275],[.85,.7,.75]):
     vote=texts[str(x),str(y)];odds*=acc/(1-acc) if vote=='+' else (1-acc)/acc if vote=='−' else 1
    prob=odds/(1+odds);label=float(texts['558',str(150+43*j)]);self.assertAlmostEqual(label,prob,delta=.005)
    bar=next(e for e in r.iter(N+'rect') if e.get('x')=='397' and e.get('y')==str(133+43*j) and e.get('fill')=='#087f89');self.assertAlmostEqual(float(bar.get('width')),147*prob,places=5)
 def test_cursor_forward_only_synchronized(self):
  for stem in ['minhash-lsh-band-collision','weak-supervision-vote-fusion']:
   for e in root(stem).iter(N+'animate'):
    if e.get('attributeName') not in ['x','y']:continue
    vs=list(map(float,e.get('values').split(';')));self.assertEqual(vs,sorted(vs));self.assertEqual(vs[-1],vs[-2]);self.assertEqual(e.get('keyTimes'),'0;0.2;0.4;0.6;1')
 def test_bilingual_hooks(self):
  for topic in ['minhash-deduplication','data-programming']:
   for lang in ['', '.zh-TW']:
    s=(A.parents[1]/f'engineering/data/{topic}{lang}.md').read_text();self.assertIn('<img data-source-asset-urls',s);self.assertIn('tabindex="0"',s);self.assertIn('overflow-x:auto',s);self.assertIn('min-width:640px;max-width:none',s)
if __name__=='__main__':unittest.main()
