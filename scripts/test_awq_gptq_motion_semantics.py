"""Check the actual SVG quantizer crossings and correlated quadratic, not fixtures."""
from pathlib import Path
import bisect,math,re,unittest,xml.etree.ElementTree as E
ROOT=Path(__file__).resolve().parents[1];N='{http://www.w3.org/2000/svg}';ASSETS=ROOT/'docs/assets/concept-animations'
def value(a,t):
 ts=list(map(float,a.get('keyTimes').split(';')));vs=list(map(float,a.get('values').split(';')));i=min(len(ts)-2,max(0,bisect.bisect_right(ts,t)-1))
 if t==1:return vs[-1]
 if a.get('calcMode')=='discrete':return vs[i]
 return vs[i]+(vs[i+1]-vs[i])*(t-ts[i])/(ts[i+1]-ts[i])
class QuantizationMotion(unittest.TestCase):
 def test_awq_actual_svg(self):
  r=E.parse(ASSETS/'awq-salient-scaling-motion.svg').getroot();an=list(r.iter(N+'animate'));self.assertEqual(len(an),5)
  for t in [i/10000 for i in range(10001)]:
   s=1+2*min(t,1-t);w=.37*s;q=.25*math.floor(w/.25+.5)
   vals=[value(a,t) for a in an]
   for got,want in zip(vals,[369+210*w,369+210*q,369+210*w,369+210*q,124/.48*abs(4/s*(q-w))]):self.assertAlmostEqual(got,want,delta=.012)
  self.assertAlmostEqual(abs(4/2*(.75-.74)),.02)
 def test_gptq_geometry(self):
  r=E.parse(ASSETS/'gptq-error-compensation-motion.svg').getroot();an=list(r.iter(N+'animate'))
  for t,x,y in [(0,.37,.37),(.39,.25,.37),(.68,.25,.466),(.85,.25,.5),(1,.25,.5)]:
   self.assertAlmostEqual(value(an[0],t),43+470*x,places=5);self.assertAlmostEqual(value(an[1],t),325-340*y,places=5)
  loss=lambda x,y:(x-.37)**2+1.6*(x-.37)*(y-.37)+(y-.37)**2
  self.assertAlmostEqual(loss(.25,.5),.00634);self.assertAlmostEqual(loss(.25,.25),.05184)
  contours=[e for e in r.iter(N+'path') if e.get('stroke-opacity')=='.25']
  self.assertEqual(len(contours),3)
  for p in contours:
   numbers=list(map(float,re.findall(r'-?\d+(?:\.\d+)?',p.get('d'))));ls=[loss((x-43)/470,(325-y)/340) for x,y in zip(numbers[::2],numbers[1::2])]
   self.assertLess(max(ls)-min(ls),.00003)
 def test_bilingual_and_static(self):
  for topic,stem in [('awq','awq-salient-scaling'),('gptq','gptq-error-compensation')]:
   for lang in ['', '.zh-TW']:
    s=(ROOT/f'docs/theory/model-compression/quantisation/post-training/{topic}/index{lang}.md').read_text()
    for token in ['data-source-asset-urls','data-still-src','tabindex="0"','width:640px',stem,'0.37']:self.assertIn(token,s)
   r=E.parse(ASSETS/f'{stem}-still.svg').getroot();self.assertFalse(list(r.iter(N+'animate')))
   for e in r.iter(N+'text'):self.assertGreaterEqual(float(e.get('font-size','12')),12)
if __name__=='__main__':unittest.main()
