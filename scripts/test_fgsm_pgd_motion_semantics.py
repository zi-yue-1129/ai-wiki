"""Educational quadratic/sign-step SVG arithmetic and actual discrete motion."""
from pathlib import Path
import bisect, math, unittest, xml.etree.ElementTree as E
P=Path(__file__).resolve().parents[1];N='{http://www.w3.org/2000/svg}'
def root(stem):return E.parse(P/f'docs/assets/concept-animations/{stem}-motion.svg').getroot()
def moving(r):return [e for e in r.iter(N+'circle') if e.find(N+'animate') is not None]
def sample(e,attr,t):
 a=next(a for a in e.findall(N+'animate') if a.get('attributeName')==attr);vs=list(map(float,a.get('values').split(';')));ts=list(map(float,a.get('keyTimes').split(';')));i=min(bisect.bisect_right(ts,t)-1,len(vs)-2)
 if a.get('calcMode')=='discrete':return vs[i]
 f=(t-ts[i])/(ts[i+1]-ts[i]);return vs[i]*(1-f)+vs[i+1]*f
class SignProjectionTests(unittest.TestCase):
 def test_fgsm_dense_linear_gain_and_budget(self):
  r=root('fgsm-sign-step');a,b=moving(r)
  lab=next(e for e in r.iter(N+'text') if e.text=='1.35');self.assertEqual(lab.get('text-anchor'),'end');self.assertLess(float(lab.get('x')),391)
  for i in range(10001):
   t=i/10001;dx=(sample(a,'cx',t)-188)/85;dy=(211-sample(a,'cy',t))/85
   self.assertAlmostEqual(dx,dy,places=10);self.assertGreaterEqual(dx,-1e-12);self.assertLessEqual(dx,1+1e-12)
   gain=.9*dx+.45*dy
   self.assertAlmostEqual(sample(b,'cx',t),391+194*dx,places=9)
   self.assertAlmostEqual(sample(b,'cy',t),285-130*gain/1.35,places=9)
 def test_pgd_dense_state_loss_and_projection(self):
  r=root('pgd-projection-path');a,b=moving(r);pts=[];x=y=-.85
  for k in range(7):
   pts.append((x,y));x=min(1,x+.4);y+=.4 if y<.55 else -.4
  for i in range(10001):
   t=i/10001;k=min(int(t/.14),6);x,y=pts[k];j=2-.6*(x-1.3)**2-1.1*(y-.55)**2
   self.assertAlmostEqual(sample(a,'cx',t),188+85*x,places=6);self.assertAlmostEqual(sample(a,'cy',t),209-85*y,places=6)
   self.assertAlmostEqual(sample(b,'cx',t),391+31.8*k,places=6);self.assertAlmostEqual(sample(b,'cy',t),286-26.4*(j+3),places=4)
  self.assertAlmostEqual(pts[4][0]+.4,1.15);self.assertEqual(pts[5][0],1)
  self.assertAlmostEqual(pts[5][1]-.55,-(pts[6][1]-.55))
 def test_exact_contour_quadratic(self):
  r=root('pgd-projection-path')
  for e,c in zip(r.iter(N+'ellipse'),[.12,.4,.9,1.7]):
   self.assertAlmostEqual(float(e.get('cx')),188+85*1.3);self.assertAlmostEqual(float(e.get('cy')),209-85*.55)
   for i in range(101):
    th=2*math.pi*i/100;dx=float(e.get('rx'))/85*math.cos(th);dy=float(e.get('ry'))/85*math.sin(th)
    self.assertAlmostEqual(.6*dx*dx+1.1*dy*dy,c,places=10)
 def test_bilingual_sources_and_caveats(self):
  for topic in ['fgsm','pgd-adversarial-training']:
   for lang in ['', '.zh-TW']:
    s=(P/f'docs/theory/machine-learning/adversarial-robustness/{topic}{lang}.md').read_text()
    self.assertIn('data-source-asset-urls',s);self.assertIn('width:640px;min-width:640px',s);self.assertIn(r'\begin{gathered}',s)
    self.assertIn(('not classifier measurements' if topic.startswith('pgd') else 'not measured') if not lang else '不是',s)
    if topic.startswith('pgd'):self.assertIn('step-5 reference' if not lang else '第 5 步參考',s)
if __name__=='__main__':unittest.main()
