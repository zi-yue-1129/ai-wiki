"""Numerical and flow checks for GroupNorm and RMSNorm teaching SVGs."""
from pathlib import Path
from xml.etree import ElementTree as E
import math,unittest
N='{http://www.w3.org/2000/svg}';A=Path(__file__).resolve().parents[1]/'docs/assets/concept-animations'
def root(stem,kind='motion'):return E.parse(A/f'{stem}-{kind}.svg').getroot()
def sample(a,t):
 vs=list(map(float,a.get('values').split(';')));ts=list(map(float,a.get('keyTimes').split(';'))) if a.get('keyTimes') else [i/(len(vs)-1) for i in range(len(vs))]
 for i in range(len(ts)-1):
  if t<=ts[i+1]:return vs[i]+(vs[i+1]-vs[i])*(t-ts[i])/(ts[i+1]-ts[i])
 return vs[-1]
class Normalisation(unittest.TestCase):
 def test_rms_sweep(self):
  r=root('rmsnorm-shift-response');bars=[b for b in r.iter(N+'rect') if b.find(N+'animate') is not None];self.assertEqual(len(bars),6)
  for k in range(1025):
   t=k/1024;b=2*(1-abs(2*t-1));x=[1+b,3+b];rms=math.sqrt(sum(v*v for v in x)/2)
   expected=[27*x[0],27*x[1],56*x[0]/rms,56*x[1]/rms,56,56]
   for j,bar in enumerate(bars):
    anim=list(bar);y=sample(anim[0],t);h=sample(anim[1],t)
    self.assertAlmostEqual(h,expected[j],delta=.003)
    self.assertAlmostEqual(y if j==4 else y+h,271 if j<2 else 218,places=5)
  for bar in bars:self.assertEqual(len(bar[0].get('values').split(';')),129)
 def test_group_statistics_and_reaching_output(self):
  for kind in ['motion','still']:
   r=root('group-norm-statistics',kind);texts=list(r.iter(N+'text'))
   for row in range(2):
    ins=[float(t.text) for t in texts if t.get('y')==str(159+125*row)];outs=[float(t.text.replace('−','-')) for t in texts if t.get('y')==str(158+125*row)]
    self.assertEqual(ins,[2+10*row,4+10*row,6+10*row,8+10*row]);mean=sum(ins)/4;var=sum((x-mean)**2 for x in ins)/4
    self.assertEqual(mean,5+10*row);self.assertEqual(var,5)
    for x,y in zip(ins,outs):self.assertAlmostEqual(y,(x-mean)/math.sqrt(var),delta=.005)
   if kind=='motion':
    dots=[c for c in r.iter(N+'circle') if c.find(N+'animateMotion') is not None];self.assertEqual(len(dots),8)
    for c in dots:
     m=c.find(N+'animateMotion');a=c.find(N+'animate');self.assertEqual(m.get('keyPoints'),'0;0;1;1');self.assertEqual(m.get('keyTimes'),'0;.08;.9;1');self.assertEqual(sample(a,.92),1);self.assertEqual(m.get('begin'),a.get('begin'))
 def test_static_assets_and_bilingual_source_markers(self):
  for stem in ['group-norm-statistics','rmsnorm-shift-response']:
   self.assertFalse(list(root(stem,'still').iter(N+'animate')))
  for topic in ['group-normalisation','rms-normalisation']:
   for lang in ['', '.zh-TW']:
    p=A.parents[1]/'theory/deep-learning/normalisation'/f'{topic}{lang}.md';self.assertIn('<img data-source-asset-urls',p.read_text())
if __name__=='__main__':unittest.main()
