"""Numeric and temporal regression checks against actual forward-AD SVG data."""
from pathlib import Path
import math,re,unittest,xml.etree.ElementTree as E
P=Path(__file__).resolve().parents[1]/'docs/assets/concept-animations'
N='{http://www.w3.org/2000/svg}'
TOPICS=['directional-jvp','jacobian-columns','dual-chain','branch-kink','loop-tangent','hessian-vector','linear-solve','sparse-packing','softmax-tangent','matmul-tangent','finite-difference','normalization-jvp']
def root(name,kind='motion'):return E.parse(P/f'forward-ad-{name}-{kind}.svg').getroot()
def tracks(element):return {a.get('attributeName'):a for a in element.findall(N+'animate')}
def values(a):return [float(v) for v in a.get('values').split(';')]
def sample(a,t):
 v=values(a);k=[float(x) for x in a.get('keyTimes','').split(';')] if a.get('keyTimes') else [i/(len(v)-1) for i in range(len(v))]
 i=max(j for j,x in enumerate(k) if x<=t)
 if i==len(k)-1 or a.get('calcMode')=='discrete':return v[i]
 return v[i]+(v[i+1]-v[i])*(t-k[i])/(k[i+1]-k[i])
def animated(name,tag):return [e for e in root(name).iter(N+tag) if e.find(N+'animate') is not None]
def text(name):return ' '.join(''.join(e.itertext()) for e in root(name).iter(N+'text'))
class ForwardADTests(unittest.TestCase):
 def test_bilingual_hooks_and_all_timing_tracks(self):
  for name in TOPICS:
   for kind in ['motion','still']:
    r=root(name,kind);self.assertEqual(r.get('viewBox'),'0 0 800 420');self.assertIsNotNone(r.find(N+'title'));self.assertIsNotNone(r.find(N+'desc'))
    for a in r.iter():
     if a.tag in [N+'animate',N+'animateMotion',N+'animateTransform']:
      self.assertEqual(kind,'motion');self.assertEqual(a.get('repeatCount'),'indefinite')
      if a.get('keyTimes'):
       k=list(map(float,a.get('keyTimes').split(';')));self.assertEqual(k[0],0);self.assertEqual(k[-1],1);self.assertTrue(all(x<y for x,y in zip(k,k[1:])))
       if a.get('values'):self.assertEqual(len(k),len(a.get('values').split(';')))
   for lang in ['', '.zh-TW']:
    doc=(P.parents[1]/f'theory/math/automatic-differentiation/forward-mode{lang}.md').read_text()
    self.assertIn(f'forward-ad-{name}-motion.svg',doc);self.assertIn(f'forward-ad-{name}-still.svg',doc)
 def test_directional_jvp_curve(self):
  tr=tracks(animated('directional-jvp','circle')[0]);ys=values(tr['cy'])
  for i,y in enumerate(ys):self.assertAlmostEqual(y,225-15*(5*math.cos(2*math.pi*i/36)+2*math.sin(2*math.pi*i/36)),delta=.011)
 def test_relu_branch_sync_and_kink_exclusion(self):
  r=root('branch-kink');a=tracks(r.find('.//*[@id="relu-primal"]'));b=tracks(r.find('.//*[@id="relu-tangent"]'))
  for t in [.01,.1,.24,.26,.4,.5,.6,.74,.76,.9,.99]:
   x=(sample(a['cx'],t)-300)/76;y=(300-sample(a['cy'],t))/72.5
   self.assertAlmostEqual(y,max(0,x),places=6);self.assertEqual(sample(b['cy'],t),174 if x>0 else 288);self.assertEqual(sample(b['opacity'],t),1)
  for t in [.25,.75]:self.assertEqual(sample(b['opacity'],t),0)
 def test_basis_markers_reach_correct_columns_while_visible(self):
  r=root('jacobian-columns');a=tracks(r.find('.//*[@id="basis-first-sweep"]'));b=tracks(r.find('.//*[@id="basis-second-sweep"]'))
  self.assertEqual(sample(a['cx'],.45),579);self.assertEqual(sample(a['opacity'],.45),1)
  self.assertEqual(sample(b['cx'],.97),719);self.assertEqual(sample(b['cy'],.97),249);self.assertEqual(sample(b['opacity'],.97),1)
  self.assertEqual(sample(a['opacity'],.75),0);self.assertEqual(sample(b['opacity'],.25),0)
 def test_dual_chain_primal_and_tangent(self):
  x,y,dx,dy=2,1,1,.5;a=x*y;da=y*dx+x*dy;b=a*a;db=2*a*da
  self.assertEqual((a,da,b,db,b+x,db+dx),(2,2,4,8,6,9));self.assertIn('Jv = 9',text('dual-chain'))
 def test_loop_exact_six_steps(self):
  a,b=animated('loop-tangent','circle');ta,tb=tracks(a),tracks(b)
  for i in range(6):
   self.assertAlmostEqual(values(ta['cy'])[i],286-66*(2+2**(1-i)-2),delta=.011)
   self.assertAlmostEqual(values(tb['cy'])[i],286-132*2**(-i),delta=.011)
 def test_hessian_correspondence(self):
  a,b=map(tracks,animated('hessian-vector','circle'))
  for i,x in enumerate(values(a['cx'])):
   t=(x-205)/55;self.assertAlmostEqual(values(a['cy'])[i],239+55*t)
   self.assertAlmostEqual(values(b['cx'])[i],597+33*t);self.assertAlmostEqual(values(b['cy'])[i],239+69.5*t)
  self.assertEqual((2*1-1,1-4),(1,-3))
 def test_linear_solve_correspondence(self):
  a,b=map(tracks,animated('linear-solve','circle'))
  for i,x in enumerate(values(a['cx'])):
   t=(x-198)/50;self.assertAlmostEqual(values(b['cx'])[i],602+60*t);self.assertAlmostEqual(values(b['cy'])[i],234+28*t)
  self.assertAlmostEqual(2*(2/3)-1/3,1);self.assertAlmostEqual(2/3+2*(-1/3),0)
 def test_sparse_seed_packing(self):
  J=[[1,0,2,0],[0,3,0,4],[5,0,6,0],[0,7,0,8]]
  for cols,want in [([0,1],[1,3,5,7]),([2,3],[2,4,6,8])]:
   self.assertEqual([sum(row[c] for c in cols) for row in J],want)
   self.assertTrue(all(sum(row[c]!=0 for c in cols)==1 for row in J))
  self.assertIn('(1, 3, 5, 7)',text('sparse-packing'));self.assertIn('(2, 4, 6, 8)',text('sparse-packing'))
 def test_softmax_samples_and_zero_sum_jvp(self):
  bars=animated('softmax-tangent','rect')[:3]
  for i,t in enumerate([-.8,0,.8,0,-.8]):
   w=[2*math.exp(t),1,math.exp(-t)];p=[x/sum(w) for x in w]
   for bar,prob in zip(bars,p):self.assertAlmostEqual(values(tracks(bar)['height'])[i],152*prob,delta=.011)
  self.assertEqual(.375-.0625-.3125,0)
 def test_matmul_formula_is_display_math_not_multiline_inline(self):
  formula=r'\dot C=\dot A B+A\dot B.'
  def require_display(doc):
   self.assertIn('$$\n'+formula+'\n$$',doc)
   self.assertNotRegex(doc,r'(?m)^\$[ \t]*$')
  for lang in ['', '.zh-TW']:
   doc=(P.parents[1]/f'theory/math/automatic-differentiation/forward-mode{lang}.md').read_text()
   require_display(doc)
   old=doc.replace('$$\n'+formula+'\n$$','$\n'+formula+'\n$')
   self.assertNotEqual(old,doc)
   with self.assertRaises(AssertionError):require_display(old)
 def test_matmul_both_paths(self):
  A=[[1,2],[0,1]];B=[[2,0],[1,1]];dA=[[0,1],[0,0]];dB=[[0,0],[1,0]]
  C=[[sum(dA[i][k]*B[k][j]+A[i][k]*dB[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
  self.assertEqual(C,[[3,1],[1,0]]);self.assertIn('Both tangent paths',text('matmul-tangent'))
 def test_finite_difference_samples(self):
  tr=tracks(animated('finite-difference','line')[0]);error=tracks(animated('finite-difference','rect')[0])
  for i in range(len(values(tr['x1']))):
   x1=(values(tr['x1'])[i]-80)/200;x2=(values(tr['x2'])[i]-80)/200;h=(x2-x1)/2
   self.assertAlmostEqual(values(tr['y1'])[i],340-22*x1**3,delta=.011);self.assertAlmostEqual(values(tr['y2'])[i],340-22*x2**3,delta=.011)
   self.assertAlmostEqual(values(error['height'])[i],136*h*h,delta=.011)
   self.assertAlmostEqual((x2**3-x1**3)/(2*h),3+h*h)
 def test_normalization_radial_and_tangent_samples(self):
  lines=animated('normalization-jvp','line');rad,component,seed,out=map(tracks,lines)
  angles=[i*math.pi/18 for i in range(10)]+[i*math.pi/18 for i in range(8,-1,-1)]
  for i,t in enumerate(angles):
   vx=.6*math.cos(t)-.8*math.sin(t);vy=.8*math.cos(t)+.6*math.sin(t)
   self.assertAlmostEqual(values(seed['x2'])[i],233+98*vx,delta=.011);self.assertAlmostEqual(values(seed['y2'])[i],259-98*vy,delta=.011)
   self.assertAlmostEqual(values(out['x2'])[i],665.6-76*.8*math.sin(t),delta=.011);self.assertAlmostEqual(values(out['y2'])[i],192.2-76*.6*math.sin(t),delta=.011)
if __name__=='__main__':unittest.main()
