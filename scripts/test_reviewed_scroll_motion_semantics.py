"""Source/Markdown DOM contracts only: native layout/ArrowRight remain browser tests."""
from pathlib import Path
from html.parser import HTMLParser
import unittest
import markdown
R=Path(__file__).resolve().parents[1]
TOPICS={
 'theory/math/calculus/lagrange-multipliers':1,
 'theory/math/calculus/newtons-method':1,
 'theory/math/probability-statistics/maximum-a-posteriori':1,
 'theory/math/probability-statistics/maximum-likelihood':1,
 'theory/paradigms/probabilistic/uncertainty-calibration/conformal-prediction':1,
 'theory/paradigms/probabilistic/uncertainty-calibration/temperature-scaling':1,
 'theory/paradigms/unsupervised/clustering/k-means':4,
}
class DOM(HTMLParser):
 def __init__(self):super().__init__();self.stack=[];self.scrollers=[];self.images=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'reviewed-motion-scroll' in a.get('class','').split():self.scrollers.append(a)
  if tag=='img' and any('reviewed-motion-scroll' in x[1].get('class','').split() for x in self.stack):self.images.append((a,list(self.stack)))
  if tag not in {'img','br','hr','input','meta','link'}:self.stack.append((tag,a))
 def handle_endtag(self,tag):
  for i in range(len(self.stack)-1,-1,-1):
   if self.stack[i][0]==tag:self.stack=self.stack[:i];break
class ScrollContracts(unittest.TestCase):
 def test_all_bilingual_regions_own_focus_before_enhancement(self):
  for topic,n in TOPICS.items():
   for lang in ['', '.zh-TW']:
    with self.subTest(topic=topic,lang=lang):
     source=(R/'docs'/f'{topic}{lang}.md').read_text();d=DOM();d.feed(markdown.markdown(source,extensions=['md_in_html']))
     self.assertEqual(len(d.scrollers),n);self.assertEqual(len(d.images),n)
     for a in d.scrollers:
      self.assertEqual(a.get('tabindex'),'0');self.assertEqual(a.get('role'),'region');self.assertTrue(a.get('aria-label'));self.assertIn('overflow-x:auto',a['style'])
     for a,parents in d.images:
      self.assertIn('data-source-asset-urls',a);self.assertTrue(a['src'].endswith('-still.svg'));self.assertTrue(a['data-motion-src'].endswith('-motion.svg'));self.assertNotIn('tabindex',a)
      self.assertFalse(any(t=='p' for t,x in parents),'no implicit paragraph scroller')
      self.assertTrue(any(x.get('tabindex')=='0' and 'overflow-x:auto' in x.get('style','') for t,x in parents))
      self.assertTrue('640' in a.get('style','') or a.get('width')=='640')
if __name__=='__main__':unittest.main()
