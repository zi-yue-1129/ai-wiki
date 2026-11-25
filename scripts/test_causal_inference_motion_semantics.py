"""Finite-population checks of causal estimands; wrong formulas must fail."""
import unittest,ast,copy
from pathlib import Path
R=Path(__file__).resolve().parents[1]/'docs/theory/causal-inference'
def score(theta,dl,dm):
 # Independent balanced X,V,U; Y=2D+3X+U, D=X+V.
 return sum(((2*(x+v)+3*x+u)-(5*x+dl*x)-theta*((x+v)-(x+dm*x)))*((x+v)-(x+dm*x)) for x in [-1,1] for v in [-1,1] for u in [-1,1])/8
class CausalTests(unittest.TestCase):
 def test_orthogonality_and_second_order_remainder(self):
  self.assertEqual(score(2,0,0),0)
  for eps in [.1,.01,.001]:
   self.assertAlmostEqual(score(2,eps,eps),-eps**2)
   self.assertAlmostEqual(score(2,0,eps),-2*eps**2) # product-only bound misses this
   self.assertAlmostEqual((score(2,eps,eps)-score(2,-eps,-eps))/(2*eps),0)
  self.assertNotEqual(score(1,0,0),0)
 def test_heterogeneous_plr_is_not_ate(self):
  # Equal-size groups with propensities .5 and .1; effects 0 and 10.
  weights=[.5*(1-.5),.1*(1-.1)];effects=[0,10]
  plr=sum(w*t for w,t in zip(weights,effects))/sum(weights)
  self.assertAlmostEqual(plr,45/17);self.assertNotAlmostEqual(plr,sum(effects)/2)
 def test_leaf_signed_contrast_shift_invariance(self):
  contrast=lambda a,b:sum(a)/len(a)-sum(b)/len(b)
  self.assertEqual(contrast([5,7],[1,3]),4)
  self.assertEqual(contrast([15,17],[11,13]),4)
  self.assertNotEqual(sum([15,17,11,13])/4,4)
 def test_frontdoor_not_backdoor(self):
  # U->D, U->Y, D->M->Y. U hidden; M observed. Positive binary probabilities.
  joint={}
  for u in [0,1]:
   for d in [0,1]:
    for m in [0,1]:
     prob=.5*(.8 if d==u else .2)*(.9 if m==d else .1)
     joint[u,d,m]=prob
  pd={d:sum(p for (u,x,m),p in joint.items() if x==d) for d in [0,1]}
  cond=lambda d,m:sum(p*(m+u) for (u,x,z),p in joint.items() if x==d and z==m)/sum(p for (u,x,z),p in joint.items() if x==d and z==m)
  front=lambda d:sum((.9 if m==d else .1)*sum(cond(x,m)*pd[x] for x in [0,1]) for m in [0,1])
  self.assertAlmostEqual(front(1)-front(0),.8)
  observed=[sum(p*(m+u) for (u,x,m),p in joint.items() if x==d)/pd[d] for d in [0,1]]
  self.assertAlmostEqual(observed[1]-observed[0],1.4);self.assertNotAlmostEqual(observed[1]-observed[0],front(1)-front(0))
 def test_browser_matrix_and_workflow_execution(self):
  import yaml
  repo=R.parents[2]
  script=repo/'scripts/test_causal_inference_prose_browser.py'
  tree=ast.parse(script.read_text())
  widths=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='WIDTHS' for t in n.targets))
  self.assertEqual(widths,(320,390,1280))
  self.assertIn("len(report['cases'])==18",script.read_text())
  workflow=yaml.safe_load((repo/'.github/workflows/concept-animation-validation.yml').read_text())
  def connected(w):
   steps=w['jobs']['build-docs']['steps']
   assert any(s.get('run')=='python scripts/test_causal_inference_prose_browser.py --site-dir site' for s in steps)
   assert any(s.get('run')=='python scripts/test_causal_inference_motion_semantics.py' for s in steps)
  connected(workflow)
  bad=copy.deepcopy(workflow);bad['jobs']['build-docs']['steps']=[s for s in bad['jobs']['build-docs']['steps'] if s.get('run')!='python scripts/test_causal_inference_prose_browser.py --site-dir site']
  with self.assertRaises(AssertionError):connected(bad)
 def test_bilingual_source_contract(self):
  for name in ['double-machine-learning','causal-forests']:
   en=(R/(name+'.md')).read_text();zh=(R/(name+'.zh-TW.md')).read_text()
   self.assertIn('translation_reviewed:',zh)
   for formula in ([r'a_n(a_n+b_n)',r'\theta_{\rm PLR}',r'\hat J^2'] if name.startswith('double') else [r'\hat\tau_L',r'\frac1{n_1}',r'\frac1{n_0}']):
    self.assertIn(formula,en);self.assertIn(formula,zh)
   self.assertIn('## References',en);self.assertIn('## 參考文獻',zh)
 def test_crossfit_motion_residual_pooling(self):
  import re
  from xml.etree import ElementTree as ET
  from fractions import Fraction
  assets=R.parents[1]/'assets/concept-animations'
  for kind in ['motion','still']:
   root=ET.parse(assets/f'dml-crossfit-residual-pooling-{kind}.svg').getroot()
   labels=[t.text for t in root.iter('{http://www.w3.org/2000/svg}text')]
   pairs=[re.findall(r'\((-?\d+), (-?\d+)\)',t.replace('−','-')) for t in labels if t.startswith('(')]
   self.assertEqual(len(pairs),2)
   nums=[];dens=[]
   for fold in pairs:
    self.assertEqual(len(fold),2)
    v,u=zip(*[(int(a),int(b)) for a,b in fold])
    nums.append(sum(a*b for a,b in zip(v,u)));dens.append(sum(a*a for a in v))
   self.assertEqual((nums,dens),([4,12],[2,8]))
   self.assertEqual(Fraction(sum(nums),sum(dens)),Fraction(8,5))
   self.assertNotEqual(Fraction(sum(nums),sum(dens)),sum(Fraction(n,d) for n,d in zip(nums,dens))/2)
   self.assertIn('θ̂ = (4 + 12) / (2 + 8) = 1.6',labels)
 def test_honest_tree_motion_leaf_contrasts(self):
  from xml.etree import ElementTree as ET
  assets=R.parents[1]/'assets/concept-animations'
  for kind in ['motion','still']:
   root=ET.parse(assets/f'honest-tree-leaf-contrast-{kind}.svg').getroot()
   labels=[t.text for t in root.iter('{http://www.w3.org/2000/svg}text')]
   values=[list(map(int,t.split(', '))) for t in labels if ', ' in t]
   self.assertEqual(values,[[5,7],[1,3],[4,6],[3,5]])
   for t,c,expected in [(values[0],values[1],4),(values[2],values[3],1)]:
    self.assertEqual(sum(t)/len(t)-sum(c)/len(c),expected)
    self.assertIn(f'τ̂ = {expected}',labels)
   self.assertIn('P1 · P2 · P3 · P4',labels)
   self.assertIn('E1 … E8',labels)
if __name__=='__main__':unittest.main()
