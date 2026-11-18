"""Numerical stage geometry and causal bag/split reveals for tree diagrams."""
import re,unittest,xml.etree.ElementTree as E
from pathlib import Path
N='{http://www.w3.org/2000/svg}';P=Path(__file__).resolve().parents[1];A=P/'docs/assets/concept-animations'
def root(stem,mode='motion'):return E.parse(A/f'{stem}-{mode}.svg').getroot()
def nums(s):return list(map(float,re.findall(r'-?(?:\d+(?:\.\d*)?|\.\d+)',s)))
def sample(a,t):
 ts=nums(a.get('keyTimes'));vs=[nums(v) for v in a.get('values').split(';')];i=max(i for i,x in enumerate(ts) if x<=t)
 if i==len(ts)-1 or a.get('calcMode')=='discrete':return vs[i]
 u=(t-ts[i])/(ts[i+1]-ts[i]);return [x+u*(y-x) for x,y in zip(vs[i],vs[i+1])]
class ForestBoosting(unittest.TestCase):
 def test_boosting_exact_affine_geometry_and_residuals(self):
  ys=[1,2,1,4,5,4];f0=sum(ys)/6;stages=[[f0]*6]
  for _ in range(2):
   prev=stages[-1];res=[y-f for y,f in zip(ys,prev)];stages.append([prev[i]+.6*sum(res[(i//3)*3:(i//3+1)*3])/3 for i in range(6)])
  r=root('boosting-residual-steps');lines=[e for e in r.iter(N+'line') if e.find(N+'animate') is not None];path=next(e.find(N+'animate') for e in r.iter(N+'path') if e.find(N+'animate') is not None)
  self.assertEqual(len(lines),6)
  for i,line in enumerate(lines):self.assertEqual(float(line.get('y1')),300-34*ys[i])
  for j in range(1001):
   t=j/1001;k=0 if t<.29 else 1 if t<.62 else 2;u=t/.29 if k==0 else (t-.29)/(.62-.29) if k==1 else 0
   expected=[stages[k][i]+u*(stages[min(k+1,2)][i]-stages[k][i]) for i in range(6)]
   coords=sample(path,t)
   for i,line in enumerate(lines):
    y=sample(line.find(N+'animate'),t)[0];self.assertAlmostEqual(y,300-34*expected[i],places=5);self.assertAlmostEqual(y,coords[1 if i<3 else 3],places=5)
  still=root('boosting-residual-steps','still');res=[e for e in still.iter(N+'line') if e.get('stroke')=='#e8aa57']
  for i,e in enumerate(res):self.assertAlmostEqual(float(e.get('y2')),300-34*stages[-1][i],places=5)
 def test_oob_only_after_all_draws_arrive(self):
  r=root('rf-bootstrap-oob');trans=list(r.iter(N+'animateTransform'));self.assertEqual(len(trans),6)
  groups=[e for e in r.iter(N+'g') if e.find(N+'animateTransform') is not None]
  labels=[''.join(e.itertext()).strip() for e in groups];self.assertEqual(labels,['A','C','C','E','F','F']);self.assertEqual(set('ABCDEF')-set(labels),set('BD'))
  arrival=max(nums(a.get('keyTimes'))[-2] for a in trans);self.assertAlmostEqual(arrival,.74)
  oob=[a for a in r.iter(N+'animate') if a.get('keyTimes')=='0;.67;.75;.82;1'];self.assertEqual(len(oob),2)
  for j in range(1001):
   t=j/1001
   if t<=arrival:self.assertTrue(all(sample(a,t)==[0] for a in oob))
  for a in oob:self.assertEqual(sample(a,.9),[1])
  for a in trans:self.assertEqual(sample(a,.99),nums(a.get('values').split(';')[-1]))
 def test_feature_selection_after_candidates(self):
  r=root('rf-feature-subset');text=[''.join(e.itertext()) for e in r.iter(N+'text')]
  for val in ['0.30','0.18','0.12','0.22']:self.assertIn(val,text)
  self.assertEqual(max({'f2':.18,'f3':.12},key={'f2':.18,'f3':.12}.get),'f2');self.assertEqual(max({'f1':.30,'f4':.22},key={'f1':.30,'f4':.22}.get),'f1')
  transforms=list(r.iter(N+'animateTransform'));self.assertEqual(len(transforms),4)
  for g in r.iter(N+'g'):
   a=g.find(N+'animate')
   if a is not None and a.get('keyTimes') in ['0;0.360;0.370;1','0;0.790;0.800;1']:
    arrival=.285 if '.360' in a.get('keyTimes') else .665
    for j in range(1001):
     t=j/1001
     if t<=arrival:self.assertEqual(sample(a,t),[0])
 def test_moving_draws_clear_section_labels(self):
  r=root('rf-feature-subset')
  for g in r.iter(N+'g'):
   if g.find(N+'animateTransform') is not None:self.assertEqual(g.find(N+'circle').get('cy'),'0')
  # Conservative text boxes for DRAW A/B; moving dots have radius 9 plus a 1px stroke.
  for a in r.iter(N+'animateTransform'):
   for j in range(1001):
    x,y=sample(a,j/1001)
    self.assertFalse(any(x+10>l and x-10<rr and y+10>top and y-10<bottom for l,rr,top,bottom in [(54,111,233,249),(428,485,233,249)]))
  self.assertIn('BAG',[''.join(e.itertext()) for e in root('rf-bootstrap-oob').iter(N+'text')])
  r=root('forest-bootstrap-vote');text=[''.join(e.itertext()) for e in r.iter(N+'text')]
  for x,expected in [('224',[1,1,3,4,5,6]),('310',[2,2,3,4,5,5]),('396',[1,2,4,4,6,6])]:
   rows=[int(e.text[1:]) for e in r.iter(N+'text') if e.get('x')==x and (e.text or '').startswith('#')];self.assertEqual(rows,expected)
  self.assertEqual([v for v in text if v in ['A','B']],['A','B','A','A'])
  for par in r.iter():
   a=par.find(N+'animateMotion')
   if a is not None:
    self.assertEqual(par.get('opacity'),'0');gate=par.find(N+'animate');self.assertEqual(gate.get('begin'),a.get('begin'));self.assertEqual(gate.get('values'),'1;1')
 def test_bilingual_accessible_source_and_caveats(self):
  for topic,count in [('random-forests',3),('gradient-boosting',1)]:
   for lang in ['', '.zh-TW']:
    s=(P/f'docs/theory/paradigms/supervised/trees-and-ensembles/{topic}{lang}.md').read_text()
    self.assertEqual(s.count('data-source-asset-urls'),count);self.assertEqual(s.count('tabindex="0"'),count)
    self.assertEqual(s.count('min-width:800px'),count)
    self.assertIn('不是' if lang else 'not',s)
if __name__=='__main__':unittest.main()
