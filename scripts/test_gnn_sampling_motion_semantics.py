"""Independent arithmetic and direction checks for the GNN toy illustrations."""
from pathlib import Path
import unittest
import xml.etree.ElementTree as E
A=Path(__file__).resolve().parents[1]/'docs/assets/concept-animations'
N='{http://www.w3.org/2000/svg}'
def root(stem,kind='motion'):return E.parse(A/f'{stem}-{kind}.svg').getroot()
class GraphExamples(unittest.TestCase):
 def test_gin_multiset_results(self):
  for kind in ['motion','still']:
   r=root('gin-multiset-counts',kind)
   for ys,features in [(177,[1,1]),(278,[1,1,1])]:
    texts={e.get('x'):e.text for e in r.iter(N+'text') if e.get('y')==str(ys)}
    self.assertEqual(float(texts['398']),sum(features)/len(features))
    self.assertEqual(float(texts['535']),sum(features))
 def test_graphsage_mean_and_concat(self):
  for kind in ['motion','still']:
   r=root('graphsage-sample-aggregate',kind)
   sample=[int(e.text) for e in r.iter(N+'text') if e.get('y')=='175'];self.assertEqual(sample,[1,2,5])
   texts={(e.get('x'),e.get('y')):e.text for e in r.iter(N+'text')}
   self.assertAlmostEqual(float(texts['509','223']),sum(sample)/len(sample),delta=.005)
   self.assertEqual(float(texts['467','263']),4)
   self.assertEqual(texts['553','263'],texts['509','223'])
 def test_messages_only_move_forward_then_hold(self):
  for stem,count,target in [('gin-multiset-counts',5,78),('graphsage-sample-aggregate',3,160)]:
   r=root(stem);moving=[c for c in r.iter(N+'circle') if c.find(N+'animate') is not None];self.assertEqual(len(moving),count)
   for c in moving:
    for a in c.findall(N+'animate'):
     if a.get('attributeName') not in ['cx','cy']:continue
     v=list(map(float,a.get('values').split(';')));self.assertEqual(v[0],v[1]);self.assertEqual(v[-1],v[-2]);self.assertEqual(a.get('keyTimes'),'0;0.15;0.6;1')
     if a.get('attributeName')=='cx':self.assertEqual(v[-1],target)
 def test_graphsage_long_equations_use_scrollable_display_math(self):
  for lang in ["", ".zh-TW"]:
   s=(A.parents[1]/f"theory/models/gnn/message-passing/graphsage/index{lang}.md").read_text()
   import re
   inline=re.findall(r"\\\((.*?)\\\)",s)
   self.assertFalse(any("MEAN" in t or "AGGREGATE" in t for t in inline))
   self.assertIn("\\[\nh_v^{k} =",s)
 def test_bilingual_hooks_and_static_fallback(self):
  for topic in ['gin','graphsage']:
   for lang in ['', '.zh-TW']:
    s=(A.parents[1]/f'theory/models/gnn/message-passing/{topic}/index{lang}.md').read_text();self.assertIn('<img data-source-asset-urls',s);self.assertIn('data-motion-src=',s)
  for stem in ['gin-multiset-counts','graphsage-sample-aggregate']:self.assertFalse(list(root(stem,'still').iter(N+'animate')))
if __name__=='__main__':unittest.main()
