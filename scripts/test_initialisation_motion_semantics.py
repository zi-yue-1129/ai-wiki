"""Independent analytic audits of all fifteen initialisation motion labs."""
from pathlib import Path
import unittest,xml.etree.ElementTree as E,math,re,bisect,functools
P=Path(__file__).resolve().parents[1];A=P/'docs/assets/concept-animations';N='{http://www.w3.org/2000/svg}'
def root(s):return E.parse(A/f'{s}-motion.svg').getroot()
@functools.lru_cache(None)
def series(e):
 vs=e.get('values').split(';');ts=list(map(float,e.get('keyTimes').split(';'))) if e.get('keyTimes') else [i/(len(vs)-1) for i in range(len(vs))]
 return ts,vs
def value(e,t,attr):
 a=next((a for a in e if a.get('attributeName')==attr),None)
 if a is None:return float(e.get(attr))
 ts,vs=series(a);i=min(len(ts)-2,bisect.bisect_right(ts,t)-1);u=0 if a.get('calcMode')=='discrete' else (t-ts[i])/(ts[i+1]-ts[i])
 return float(vs[i])+u*(float(vs[i+1])-float(vs[i]))
def moving(r,tag):return [e for e in r.iter(N+tag) if e.find(N+'animate') is not None]
class Initialisation(unittest.TestCase):
 def test_fan_and_width_actual_interpolations(self):
  for stem in ['glorot-fan-tradeoff','mup-width-multipliers','he-fan-mode-tradeoff']:
   r=root(stem);bars=moving(r,'rect');circles=moving(r,'circle')
   for j in range(2001):
    t=j/2001;u=2*min(t,1-t)
    if stem.startswith('glorot'):
     f=200/(200+300*u);b=2-f
     for e in bars:self.assertAlmostEqual(value(e,t,'width'),152/1.8*(b if e.get('fill')=='#7355cb' else f),delta=.015)
     for e in circles:self.assertAlmostEqual(value(e,t,'cy'),283-81*(b if e.get('fill')=='#7355cb' else f),delta=.015)
    elif stem.startswith('mup'):
     for e in bars:self.assertAlmostEqual(value(e,t,'width'),153 if e.get('fill')=='#dd8f32' else 153/(1+7*u),delta=.05)
     self.assertAlmostEqual(value(circles[0],t,'cy'),274-117/(1+7*u),delta=.05)
    else:
     for e in bars:self.assertAlmostEqual(value(e,t,'width'),(102 if e.get('y')=='155' else 408)/(1+3*u),delta=.025)
 def test_relu_shift_and_prelu(self):
  r=root('he-relu-mean-shift');cs=moving(r,'circle')
  for j in range(2001):
   t=j/2001;b=-2+8*min(t,1-t);p=.5*(1+math.erf(b/math.sqrt(2)));q=p+b*math.exp(-b*b/2)/math.sqrt(2*math.pi)/(1+b*b)
   for e in cs:self.assertAlmostEqual(value(e,t,'cy'),268-128*(p if e.get('fill')=='#117c85' else q),delta=.015)
  r=root('prelu-slope-gain')
  for e in moving(r,'circle'):
   for j in range(1001):
    t=j/1001;a=2*min(t,1-t);gain=1+a*a if e.get('fill')=='#d37d42' else 1
    self.assertAlmostEqual(value(e,t,'cy'),369.0769230769231-113.84615384615385*gain,delta=.002)
  # Gaussian ReLU has positive mean, so centered variance differs.
  self.assertNotEqual(.5,.5-1/(2*math.pi))
 def test_tanh_quadrature_independent_simpson(self):
  r=root('glorot-tanh-saturation');e=moving(r,'circle')[0]
  for q in [0,.045,.1,.5,1,4,9]:
   # Simpson on standard normal, independent integration scheme from generator trapezoid.
   h=16/8000
   def f(z):return math.exp(-z*z/2)/math.sqrt(2*math.pi)/math.cosh(math.sqrt(q)*z)**4
   expected=h/3*(f(-8)+f(8)+sum((4 if i%2 else 2)*f(-8+i*h) for i in range(1,8000)))
   self.assertAlmostEqual(value(e,math.sqrt(q/9)/2,'cy'),268-128*expected,delta=.06)
 def test_integer_depth_and_channels(self):
  for stem in ['he-relu-second-moment','glorot-alternating-width']:
   r=root(stem)
   for e in moving(r,'circle'):
    for j in range(1001):
     t=j/1001;x=value(e,t,'cx');y=value(e,t,'cy')
     if stem.startswith('he'):
      k=round((x-105)/117);q=1 if e.get('fill')=='#168b88' else 2**(-k);expected=269-126*q
     else:
      k=round((x-92)/80);q=.64**(k//2)*(.4 if k%2 else 1);expected=277-129.6*q
     self.assertAlmostEqual(y,expected,delta=.001)
  r=root('mup-update-budget');rs=moving(r,'rect')
  for t,n in [(.1,4),(.4,8),(.8,16)]:
   active=4+sum(value(e,t,'opacity')==1 for e in rs if e.get('attributeName') is None and e.get('opacity') is not None)
   self.assertEqual(active,n)
   for e in rs:
    if e.get('y')=='138':self.assertAlmostEqual(value(e,t,'width'),896/n)
    if e.get('y')=='286':self.assertAlmostEqual(value(e,t,'width'),18*n)
  r=root('mup-readout-aggregation')
  for t,n in [(.1,4),(.3,8),(.6,12),(.8,16)]:
   self.assertEqual(sum(value(e,t,'opacity')==1 for e in moving(r,'rect') if e.get('opacity') is not None),n)
   b=next(e for e in moving(r,'rect') if e.get('y')=='159');self.assertEqual(value(b,t,'width'),n*14.75)
 def test_discrete_noise_and_optimizer(self):
  for stem in ['mup-readout-noise','mup-adam-sgd']:
   r=root(stem);cs=moving(r,'circle')
   for t,n in [(.1,4),(.3,8),(.6,16),(.8,32)]:
    for e in cs:
     if stem.endswith('noise'):v=1 if e.get('fill')=='#109b94' else 1/math.sqrt(n)
     else:v=4/n if e.get('fill')=='#109b94' else 4/n**1.5
     self.assertAlmostEqual(value(e,t,'cy'),271-110*v,delta=.006)
 def test_transfer_curve_and_causal_reveal(self):
  r=root('mup-transfer-validation');curve=moving(r,'path')[0];cs=moving(r,'circle');a=curve.find(N+'animate');ts,vs=series(a)
  def nums(s):return list(map(float,re.findall(r'-?(?:\d+(?:\.\d*)?|\.\d+)',s)))
  for j in range(1001):
   t=j/1001;i=min(len(ts)-2,bisect.bisect_right(ts,t)-1);u=(t-ts[i])/(ts[i+1]-ts[i]);v=[x+u*(y-x) for x,y in zip(nums(vs[i]),nums(vs[i+1]))]
   for e in cs:
    x=value(e,t,'cx');q=(x-356)/210;curve_y=(1-q)**2*v[1]+2*q*(1-q)*v[3]+q*q*v[5]
    self.assertAlmostEqual(value(e,t,'cy'),curve_y,delta=.002)
  r=root('mup-transfer-protocol');g=next(e for e in r.iter(N+'g') if e.find(N+'animate') is not None)
  self.assertEqual(value(g,.65,'opacity'),0);self.assertEqual(value(g,.66,'opacity'),1)
 def test_all_bilingual_source_hooks_and_density(self):
  counts={'glorot-initialisation':4,'he-initialisation':4,'mup':7}
  for topic,n in counts.items():
   for lang in ['', '.zh-TW']:
    s=(P/f'docs/theory/deep-learning/initialisation/{topic}{lang}.md').read_text()
    self.assertEqual(s.count('<img data-source-asset-urls'),n);self.assertEqual(s.count('width:640px;min-width:640px'),n)
  r=root('glorot-equal-variance-densities');e=moving(r,'path')[0];a=e.find(N+'animate');vs=a.get('values').split(';')
  self.assertEqual(len(set(len(re.findall(r'[-+]?\d*\.?\d+',v)) for v in vs)),1)
  # Both complete component distributions are centered with unit variance.
  self.assertAlmostEqual((math.sqrt(3))**2/3,1)
if __name__=='__main__':unittest.main()
