"""Independent numerical, timeline and actual JavaScript regressions for LIME/SHAP."""
from pathlib import Path
import math,subprocess,unittest,xml.etree.ElementTree as E
ROOT=Path(__file__).resolve().parents[1];N='{http://www.w3.org/2000/svg}'
def svg(stem,state='motion'):return E.parse(ROOT/f'docs/assets/concept-animations/{stem}-{state}.svg').getroot()
def sample(a,t):
 ts=list(map(float,a.get('keyTimes').split(';')));vs=list(map(float,a.get('values').split(';')))
 i=max(i for i,x in enumerate(ts) if x<=t)
 if i==len(ts)-1 or a.get('calcMode')=='discrete':return vs[i]
 return vs[i]+(vs[i+1]-vs[i])*(t-ts[i])/(ts[i+1]-ts[i])
class ExplanationSemantics(unittest.TestCase):
 def test_actual_js(self):subprocess.run(['node','scripts/test_explanation_math.cjs'],cwd=ROOT,check=True)
 def test_lime_geometry_and_fit(self):
  r=svg('lime-local-surrogate');pts=[e for e in r.iter(N+'circle') if e.find(N+'animate') is not None and e.get('fill')=='#078a80'];self.assertEqual(len(pts),12)
  xs=[.13,.24,.34,.41,.46,.50,.56,.60,.65,.72,.85,.94];f=lambda x:.27+.34*x+.15*math.sin(2*math.pi*x)+.13*(x-.55)**2
  for e,x in zip(pts,xs):
   attrs={a.get('attributeName'):a for a in e.findall(N+'animate')};self.assertAlmostEqual(sample(attrs['cx'],.8),63+351*x,delta=.051);self.assertAlmostEqual(sample(attrs['cy'],.8),301-246*f(x),delta=.051)
   w=math.exp(-(x-.54)**2/(2*.15**2));self.assertAlmostEqual(float(e.get('r')),3+4.3*w,delta=.006)
  ws=[math.exp(-(x-.54)**2/(2*.15**2)) for x in xs];sw=sum(ws);mx=sum(w*x for w,x in zip(ws,xs))/sw;my=sum(w*f(x) for w,x in zip(ws,xs))/sw
  b=sum(w*(x-mx)*(f(x)-my) for w,x in zip(ws,xs))/sum(w*(x-mx)**2 for w,x in zip(ws,xs));a=my-b*mx
  self.assertAlmostEqual(a,.59754858,places=7);self.assertAlmostEqual(b,-.31406995,places=7)
  for line in r.iter(N+'line'):
   if line.get('stroke-width')=='4':
    for k in ['1','2']:
     x=(float(line.get('x'+k))-63)/351;self.assertAlmostEqual(float(line.get('y'+k)),301-246*(a+b*x),delta=.07)
  # Reveal fit only after every point finishes its placement.
  last=max(float(e.find(N+'animate').get('keyTimes').split(';')[1]) for e in pts)
  reveals=[a for a in r.iter(N+'animate') if a.get('keyTimes')=='0;.60;.72;.96;1'];self.assertTrue(reveals)
  for a in reveals:
   for k in range(600):self.assertEqual(sample(a,k/1000),0)
  self.assertLessEqual(last,.60)
 def test_shap_accounting_dense(self):
  r=svg('shap-coalition-marginals');segments=[e for e in r.iter(N+'rect') if e.get('y')=='228' and e.find(N+'animate') is not None];self.assertEqual(len(segments),4)
  labels=[g for g in r.iter(N+'g') if g.find(N+'text') is not None and g.find(N+'animate') is not None];self.assertEqual(len(labels),5)
  ends=[.17,.397,.624,.851];parts=[.2/3,.32/6,.12/6,.3/3]
  for k in range(1000):
   t=k/1000;expected=sum(v for v,end in zip(parts,ends) if t>=end);width=sum(sample(e.find(N+'animate'),t) for e in segments);self.assertAlmostEqual(width,136*expected/.24,delta=.12)
   visible=[g.find(N+'text').text for g in labels if sample(g.find(N+'animate'),t)>0];self.assertEqual(len(visible),1);self.assertAlmostEqual(float(visible[0]),expected,delta=.00051)
 def test_fallback_hooks_and_timing(self):
  for stem,topic in [('lime-local-surrogate','lime'),('shap-coalition-marginals','shap')]:
   r=svg(stem);still=svg(stem,'still');layers=[e for e in r if e.get('class')=='still-layer'];self.assertEqual(len(layers),1);self.assertFalse(list(layers[0].iter(N+'animate')))
   for a in r.iter(N+'animate'):
    ts=list(map(float,a.get('keyTimes').split(';')));self.assertTrue(all(a<b for a,b in zip(ts,ts[1:])));self.assertEqual(len(ts),len(a.get('values').split(';')))
   for lang in ['', '.zh-TW']:
    s=(ROOT/f'docs/society/interpretability/{topic}{lang}.md').read_text();self.assertIn('data-source-asset-urls',s);self.assertIn('tabindex="0"',s);self.assertIn('explanation-motion',s);self.assertIn(f'{stem}-still.svg',s)
if __name__=='__main__':unittest.main()
