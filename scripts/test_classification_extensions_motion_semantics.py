"""Inspect the four newer classification SVGs at actual SMIL times and geometry."""
import bisect
import re
import unittest
import xml.etree.ElementTree as E
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
from test_classification_svg_motion_semantics import svg, sample, moving, NS
ROOT=Path(__file__).resolve().parents[1]
class ClassificationExtensions(unittest.TestCase):
 def test_f1_every_prefix_and_boundary(self):
  r=svg('f1-threshold-topk');dot=moving(r,'circle')[0];groups=moving(r,'g')
  tr=next(r.iter(NS+'animateTransform'));times=list(map(float,tr.get('keyTimes').split(';')))
  shifts=[float(x.split()[0]) for x in tr.get('values').split(';')]
  labels=[1,0,1,1,0,1,0,0]
  for j in range(10001):
   t=(j+.1)/10002;k=min(bisect.bisect_right(times,t)-1,8)
   self.assertEqual([i for i,g in enumerate(groups) if sample(g,'opacity',t)==1],[k])
   tp=sum(labels[:k]);f=2*tp/(k+4)
   self.assertIn(f'TP {tp}  ·  FP {k-tp}  ·  FN {4-tp}',[e.text for e in groups[k].iter(NS+'text')])
   self.assertAlmostEqual(sample(dot,'cx',t),338+32.2*k,places=6)
   self.assertAlmostEqual(sample(dot,'cy',t),275-147*f,delta=.051)
   boundary=36+shifts[k]
   self.assertEqual(sum(55+30*i<boundary for i in range(8)),k)
 def test_randomized_mixture_dense(self):
  r=svg('roc-randomized-operating-mix');dot=moving(r,'circle')[0];bars=moving(r,'rect');lines=moving(r,'line')
  for j in range(10001):
   t=j/10000;w=2*min(t,1-t);fp=.1+.3*w;tp=.6+.3*w
   x=66+245*fp;y=281-169*tp
   self.assertAlmostEqual(sample(dot,'cx',t),x,places=7)
   self.assertAlmostEqual(sample(dot,'cy',t),y,places=7)
   self.assertAlmostEqual(sample(bars[0],'width',t),217*tp,places=7)
   self.assertAlmostEqual(sample(bars[1],'width',t),217*fp,places=7)
   self.assertAlmostEqual(sample(lines[0],'x1',t),x,places=7)
   self.assertAlmostEqual(sample(lines[1],'y1',t),y,places=7)
 def test_all_random_orderings_and_running_means(self):
  r=svg('pr-random-ap-expectation');box=moving(r,'rect')[0];aps=[]
  for hits in combinations(range(4),2):
   aps.append(sum((F(i+1,rank+1)/2 for i,rank in enumerate(hits)),F(0)))
  self.assertEqual(sum(aps)/6,F(49,72))
  txt=list(r.iter(NS+'text'))
  for i,ap in enumerate(aps):
   row=[e.text for e in txt if e.get('y')==str(117+32*i)]
   self.assertIn(f'{float(ap):.3f}',row)
   self.assertIn(f'{float(sum(aps[:i+1])/(i+1)):.3f}',row)
  times=[float(x) for x in next(box.iter(NS+'animate')).get('keyTimes').split(';')]
  for j in range(10001):
   t=j/10001;i=min(bisect.bisect_right(times,t)-1,5)
   self.assertEqual(sample(box,'y',t),98+32*i)
  self.assertIn('ORDERING',[e.text for e in txt])
 def test_cost_marker_row_and_exact_cost(self):
  r=svg('roc-cost-operating-point');dot=moving(r,'circle')[0];box=moving(r,'rect')[0]
  labels=[1,0,1,0];costs=[]
  for k in range(5):
   tp=sum(labels[:k])/2;fp=(k-sum(labels[:k]))/2;cost=.5*(1-tp)+.75*fp;costs.append(cost)
   bars=[e for e in r.iter(NS+'rect') if e.get('y')==str(113+37*k)]
   self.assertAlmostEqual(float(bars[-1].get('width')),86*cost/.75,delta=.051)
  self.assertEqual(costs,[.5,.25,.625,.375,.75])
  for j in range(10001):
   t=j/10001;k=min(int(t*5),4);tp=sum(labels[:k])/2;fp=(k-sum(labels[:k]))/2
   self.assertEqual(sample(box,'y',t),104+37*k)
   self.assertEqual(sample(dot,'cx',t),356+206*fp)
   self.assertEqual(sample(dot,'cy',t),265-168*tp)
 def test_bilingual_source_and_display_math(self):
  for topic,stems,expr in [('f1',['f1-threshold-topk'],r'F_1(k)'),('pr-auc',['pr-random-ap-expectation'],r'\mathbb E[AP]'),('roc-auc',['roc-randomized-operating-mix','roc-cost-operating-point'],r'\mathrm{FPR}_{mix}')]:
   for lang in ['', '.zh-TW']:
    s=(ROOT/f'docs/theory/evaluation/metrics/classification/{topic}{lang}.md').read_text()
    for stem in stems:
     line=next(x for x in s.splitlines() if '<img' in x and stem in x)
     self.assertIn('data-source-asset-urls',line);self.assertIn('min-width:640px',line)
    blocks=re.findall(r'^\$\$\n(.*?)\n\$\$$',s,re.M|re.S)
    self.assertTrue(any(expr in x and '\\\\' in x for x in blocks))
    if topic=='roc-auc':self.assertTrue(any('L(k)' in x and '\\\\' in x for x in blocks))
if __name__=='__main__':unittest.main()
