"""Evaluate actual SVG scores, discrete axes and synchronized transport clocks."""
from pathlib import Path
import bisect,copy,re,unittest,xml.etree.ElementTree as E
R=Path(__file__).resolve().parents[1];A=R/'docs/assets/concept-animations';N='{http://www.w3.org/2000/svg}'
def value(a,t):
 v=list(map(float,a.get('values').split(';')));k=list(map(float,a.get('keyTimes').split(';')));i=min(len(v)-2,max(0,bisect.bisect_right(k,t)-1))
 if a.get('calcMode')=='discrete':return v[min(len(v)-1,bisect.bisect_right(k,t)-1)]
 return v[i]+(v[i+1]-v[i])*(t-k[i])/(k[i+1]-k[i])
def validate(root,stem):
 if stem.startswith('kivi'):
  axes=list(root.iter(N+'animate'));assert len(axes)==2
  for a,allowed in zip(axes,[{62,86,110,134},{136,161,186,211,236}]):
   assert a.get('calcMode')=='discrete'
   for i in range(1001):assert value(a,i/1000) in allowed
 else:
  scores=[2,1,9,3,7,2,1,0]
  bars=[r for r in root.findall(N+'rect') if r.get('width')=='24' and r.get('fill')!='#edf1f5'];assert len(bars)==8
  for r,s in zip(bars,scores):assert float(r.get('height'))==6*s and float(r.get('y'))+float(r.get('height'))==226
  result=next(g for g in root.findall(N+'g') if g.get('class')=='result');selected=[t.text for t in result.findall(N+'text')]
  assert selected==['t3','t5','t7','t8'];assert sorted(range(6),key=lambda i:scores[i],reverse=True)[:2]==[2,4]
  motion=next(g for g in root.findall(N+'g') if g.get('class')=='motion')
  for r,s in zip(motion.findall(N+'rect'),scores):
   aa={a.get('attributeName'):a for a in r.findall(N+'animate')}
   for i in range(1001):
    t=i/1000;h=value(aa['height'],t);assert abs(h+value(aa['y'],t)-226)<1e-8;assert abs(h-6*s*min(t/.33,1))<1e-8
  circles=motion.findall(N+'circle');assert len(circles)==4
  for c,dst in zip(circles,[(159.5,294),(265.5,294),(371.5,294),(477.5,294)]):
   a=c.find(N+'animateMotion');assert a.get('dur')=='12s' and a.get('begin')=='0s';assert a.get('keyTimes')=='0;.51;.77;1' and a.get('keyPoints')=='0;0;1;1'
   coords=list(map(float,re.findall(r'-?\d+(?:\.\d+)?',a.get('path'))));assert (float(c.get('cx'))+coords[-2],float(c.get('cy'))+coords[-1])==dst
   assert c.find(N+'animate').get('dur')==a.get('dur')
class Motion(unittest.TestCase):
 def test_actual_svg_geometry(self):
  for stem in ['kivi-quantization-axis','h2o-heavy-hitter-selection']:validate(E.parse(A/(stem+'-motion.svg')).getroot(),stem)
 def test_wrong_bar_and_async_clock_rejected(self):
  r=E.parse(A/'h2o-heavy-hitter-selection-motion.svg').getroot();r.find(".//"+N+"animateMotion").set('dur','3.1s')
  with self.assertRaises(AssertionError):validate(r,'h2o')
  r=E.parse(A/'h2o-heavy-hitter-selection-motion.svg').getroot();next(x for x in r.findall(N+'rect') if x.get('x')=='200' and x.get('fill')!='#edf1f5').set('height','55')
  with self.assertRaises(AssertionError):validate(r,'h2o')
 def test_fractional_group_selection_rejected(self):
  r=E.parse(A/'kivi-quantization-axis-motion.svg').getroot();next(r.iter(N+'animate')).set('calcMode','linear')
  with self.assertRaises(AssertionError):validate(r,'kivi')
 def test_source_owned_scroll_and_hooks(self):
  for topic in ['kivi','h2o']:
   for lang in ['', '.zh-TW']:
    s=(R/f'docs/engineering/inference-optimization/{topic}{lang}.md').read_text();assert 'tabindex="0" role="region"' in s and 'overflow-x:auto' in s and 'data-source-asset-urls' in s and 'min-width:640px' in s
if __name__=='__main__':unittest.main()
