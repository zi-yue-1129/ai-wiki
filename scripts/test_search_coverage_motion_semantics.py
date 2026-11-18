"""Source-aware checks for equal-budget grid/random search coverage."""
import unittest
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as E
N='{http://www.w3.org/2000/svg}';A=Path(__file__).resolve().parents[1]/'docs/assets/concept-animations'
def root(topic,kind):return E.parse(A/f'{topic}-x-coverage-{kind}.svg').getroot()
class SearchCoverage(unittest.TestCase):
 def test_projection_and_equal_budget(self):
  for topic in ['grid-search','random-search']:
   for kind in ['motion','still']:
    r=root(topic,kind);groups=r.findall(N+'g');self.assertEqual(len(groups),16);xs=[];ys=[]
    for g in groups:
     cs=g.findall(N+'circle');self.assertEqual(len(cs),2);self.assertEqual(cs[0].get('cx'),cs[1].get('cx'));self.assertEqual(cs[0].get('cy'),cs[1].get('cy'))
     x=(float(cs[0].get('cx'))-72)/288;y=(286-float(cs[0].get('cy')))/192;xs.append(round(x,6));ys.append(round(y,6));self.assertTrue(0<=x<=1 and 0<=y<=1)
     bar=g.find(N+'rect');self.assertAlmostEqual(float(bar.get('x'))+float(bar.get('width'))/2,416+174*x,places=5)
    if topic=='grid-search':self.assertEqual(Counter(xs),Counter({.125:4,.375:4,.625:4,.875:4}));self.assertEqual(len(set(zip(xs,ys))),16);self.assertEqual(len(set(ys)),4)
    else:self.assertEqual(len(set(xs)),16)
    strip=[q for q in r.findall(N+'rect') if q.get('fill')=='#3c927f'][0];self.assertAlmostEqual((float(strip.get('x'))-72)/288,.68);self.assertAlmostEqual(float(strip.get('width'))/288,.12)
 def test_accumulation_clock_and_still_equivalence(self):
  starts=[]
  for topic in ['grid-search','random-search']:
   motion=root(topic,'motion');still=root(topic,'still');self.assertFalse(list(still.iter(N+'animate')));topic_starts=[]
   for i,(m,s) in enumerate(zip(motion.findall(N+'g'),still.findall(N+'g'))):
    for tag in ['circle','rect']:
     self.assertEqual([c.attrib for c in m.findall(N+tag)],[c.attrib for c in s.findall(N+tag)])
    a=m.find(N+'animate');ts=list(map(float,a.get('keyTimes').split(';')));self.assertEqual(a.get('values'),'0;0;1;1');self.assertEqual(ts[0],0);self.assertEqual(ts[-1],1);self.assertLess(ts[1],ts[2]);self.assertLess(ts[2],.81);topic_starts.append(ts[1]);self.assertEqual(a.get('dur'),'12s')
   self.assertEqual(topic_starts,sorted(set(topic_starts)));starts.append(topic_starts)
   rings=[c for c in motion.findall(N+'circle') if c.find(N+'animate') is not None];self.assertEqual(len(rings),16)
   for i,c in enumerate(rings):self.assertEqual(float(c[0].get('keyTimes').split(';')[1]),topic_starts[i])
  self.assertEqual(starts[0],starts[1])
 def test_bilingual_static_first(self):
  for topic in ['grid-search','random-search']:
   for lang in ['', '.zh-TW']:
    p=A.parents[1]/'theory/optimization/hyperparameter-optimisation'/f'{topic}{lang}.md';s=p.read_text();self.assertIn('<img data-source-asset-urls src="../../../assets/concept-animations/'+topic+'-x-coverage-still.svg"',s);self.assertIn('data-motion-src=',s);self.assertIn('tabindex="0"',s)
if __name__=='__main__':unittest.main()
