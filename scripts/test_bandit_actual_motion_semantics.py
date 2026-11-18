import unittest,math,re,xml.etree.ElementTree as E
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'docs/assets/concept-animations';N='{http://www.w3.org/2000/svg}'
def root(s):return E.parse(A/(s+'-motion.svg')).getroot()
def nums(s):return list(map(float,re.findall(r'-?\d+(?:\.\d+)?',s)))
class BanditActualTests(unittest.TestCase):
 def test_bonus_marker_exact_counts(self):
  r=root('ucb1-bonus-sensitivity');cs=[e for e in r.iter(N+'circle') if e.find(N+'animate') is not None]
  for e,t in zip(cs,[64,256]):
   an={a.get('attributeName'):a for a in e.findall(N+'animate')};ys=nums(an['cy'].get('values'));xx=nums(an['cx'].get('values'))
   for j,n in enumerate([1,2,4,8,16,32]):self.assertAlmostEqual(ys[j],322-61*math.sqrt(2*math.log(t)/n),delta=.006);self.assertEqual(xx[j],130+j*110)
 def test_ucb_bars_and_no_backward_unlearning(self):
  r=root('ucb1-optimism-switch');bars=[e for e in r.iter(N+'rect') if e.get('fill') in ['#477DA8','#EB8757'] and e.find(N+'animate') is not None]
  for j,e in enumerate(bars):
   a=next(a for a in e.findall(N+'animate') if a.get('attributeName')=='height');v=nums(a.get('values'));self.assertEqual(v[-1],v[-2]);arm=j//2
   for step,k in enumerate([0,2,4]):
    n=[6,2+step,8][arm];mean=[.65,.9/(2+step),.6][arm];expected=75*(mean if j%2==0 else math.sqrt(2*math.log(16+step)/n));self.assertAlmostEqual(v[k],expected,delta=.011)
 def test_samples_hidden_during_posterior_update(self):
  r=root('thompson-beta-posterior-draws')
  for c in r.iter(N+'circle'):
   an={a.get('attributeName'):a for a in c.findall(N+'animate')}
   if not an:continue
   self.assertEqual(an['cx'].get('calcMode'),'discrete');self.assertEqual(an['opacity'].get('values').split(';')[1],'0');self.assertEqual(an['opacity'].get('keyTimes'),'0;.42;.6;1')
 def test_beta_density_and_credible_endpoints(self):
  r=root('thompson-evidence-concentration');p=next(p for p in r.iter(N+'path') if p.find(N+'animate') is not None);vals=p.find(N+'animate').get('values').split(';');band=next(e for e in r.iter(N+'rect') if e.find(N+'animate') is not None);an={a.get('attributeName'):nums(a.get('values')) for a in band.findall(N+'animate')}
  for a,k in [(1,0),(2,2),(5,4),(11,6)]:
   xy=nums(vals[k]);factor=math.factorial(2*a-1)/math.factorial(a-1)**2
   for x,y in zip(xy[::2],xy[1::2]):
    t=(x-126)/560;pdf=factor*t**(a-1)*(1-t)**(a-1);self.assertAlmostEqual(y,315-52*pdf,delta=.011)
   lo=(an['x'][k]-126)/560;hi=lo+an['width'][k]/560;cdf=lambda x:sum(math.comb(2*a-1,j)*x**j*(1-x)**(2*a-1-j) for j in range(a,2*a));self.assertAlmostEqual(cdf(lo),.05,delta=.00003);self.assertAlmostEqual(cdf(hi),.95,delta=.00003)
 def test_source_hooks_math_and_local_scope(self):
  for lang in ['', '.zh-TW']:
   p=ROOT/f'docs/theory/paradigms/online/stochastic-bandits/index{lang}.md';s=p.read_text();self.assertEqual(s.count('data-source-asset-urls'),4);self.assertIn('tabindex="0"',s)
   for block in re.findall(r'\$\$(.*?)\$\$',s,re.S):self.assertNotIn('$',block)
  self.assertNotIn('.bandit-motion-viewport',(ROOT/'docs/stylesheets/concept-motion.css').read_text())
if __name__=='__main__':unittest.main()
