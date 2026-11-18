"""Independent ODIN sign/temperature and actual-SVG score geometry checks."""
import bisect, math, unittest, xml.etree.ElementTree as E
from pathlib import Path
R=Path(__file__).resolve().parents[1];N='{http://www.w3.org/2000/svg}'
def value(a,t):
 k=list(map(float,a.get('keyTimes').split(';')));v=list(map(float,a.get('values').split(';')));i=min(bisect.bisect_right(k,t)-1,len(k)-2);u=(t-k[i])/(k[i+1]-k[i]);return v[i]*(1-u)+v[i+1]*u
def confidence(x,T=2):return 1/(1+math.exp(-2*x/T))
class Odin(unittest.TestCase):
 def test_gradient_and_temperature_direction(self):
  for T in [1,2,10,100]:
   x=1;h=1e-5;derivative=(math.log(confidence(x+h,T))-math.log(confidence(x-h,T)))/(2*h)
   self.assertAlmostEqual(derivative,2/T*(1-confidence(x,T)),places=9);self.assertGreater(derivative,0)
   self.assertGreater(confidence(x+.25,T),confidence(x,T))
  self.assertGreater(confidence(1,1),confidence(1,2));self.assertGreater(confidence(1,2),confidence(1,10))
  self.assertLess(confidence(1),.75);self.assertGreater(confidence(1.25),.75)
 def test_actual_score_ring_stays_on_axis_and_matches_input(self):
  r=E.parse(R/'docs/assets/concept-animations/odin-gradient-perturbation-motion.svg').getroot()
  marker=next(c for c in r.iter(N+'circle') if c.get('r')=='9');ring=r.find(".//"+N+"circle[@id='current-confidence']")
  self.assertEqual(ring.get('cy'),'139');self.assertFalse(any(a.get('attributeName')=='cy' for a in ring))
  a=marker.find(N+'animate');b=ring.find(N+'animate');self.assertEqual(a.get('dur'),b.get('dur'))
  for i in range(10001):
   t=i/10000;x=1+(value(a,t)-178)/208;score=.5+(value(b,t)-413)/450
   self.assertGreaterEqual(x,1-1e-10);self.assertLessEqual(x,1.25+1e-10)
   self.assertAlmostEqual(score,confidence(x),delta=2e-7)
  for kind in ['motion','still']:
   root=E.parse(R/f'docs/assets/concept-animations/odin-gradient-perturbation-{kind}.svg').getroot()
   circles=list(root.iter(N+'circle'))
   for y,x in [(206,1),(252,1.25)]:
    c=next(c for c in circles if c.get('cy')==str(y) and c.get('r')=='6')
    self.assertAlmostEqual(float(c.get('cx')),413+450*(confidence(x)-.5),delta=.006)
 def test_bilingual_readable_scrolling_and_source_hooks(self):
  from html.parser import HTMLParser
  class Parser(HTMLParser):
   def __init__(self):super().__init__();self.tags=[]
   def handle_starttag(self,tag,attrs):self.tags.append((tag,dict(attrs)))
  for name in ['odin','mahalanobis-distance']:
   for lang in ['', '.zh-TW']:
    s=(R/f'docs/theory/machine-learning/ood-detection/{name}{lang}.md').read_text();p=Parser();p.feed(s)
    i=next(i for i,(tag,a) in enumerate(p.tags) if tag=='img' and 'data-motion-src' in a)
    outer,inner,img=p.tags[i-2:i+1];self.assertEqual(outer[1]['tabindex'],'0');self.assertIn('overflow-x:auto',outer[1]['style']);self.assertIn('min-width:640px',inner[1]['style'])
    self.assertIn('data-source-asset-urls',img[1]);self.assertEqual(img[1]['src'],img[1]['data-still-src']);self.assertIn('max-width:none',img[1]['style']);self.assertIn('方向鍵' if lang else 'arrow keys',s)
if __name__=='__main__':unittest.main()
