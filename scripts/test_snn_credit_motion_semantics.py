"""Numerical/time regression over the real STDP/e-prop SVG attributes."""
import unittest,math,re,bisect,xml.etree.ElementTree as E
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'docs/assets/concept-animations';N='{http://www.w3.org/2000/svg}'
def svg(stem,kind='motion'):return E.parse(A/f'{stem}-{kind}.svg').getroot()
def at(node,attr,u):
 a=next((a for a in node if a.get('attributeName')==attr),None)
 if a is None:return float(node.get(attr))
 ts=list(map(float,a.get('keyTimes').split(';')));vs=list(map(float,a.get('values').split(';')));i=min(len(ts)-2,max(0,bisect.bisect_right(ts,u)-1));w=0 if a.get('calcMode')=='discrete' else (u-ts[i])/(ts[i+1]-ts[i]);return vs[i]+w*(vs[i+1]-vs[i])
class SnnCredit(unittest.TestCase):
 def test_stdp_true_sample_geometry_and_discontinuity(self):
  r=svg('stdp-spike-timing');g=r.find('.//*[@id="stdp-sample"]');post,stem,point=list(g)
  for k in range(10001):
   u=k/10001;dt=(at(point,'cx',u)-326)/6.7
   self.assertGreaterEqual(abs(dt),.99999)
   self.assertAlmostEqual((at(post,'cx',u)-312)/6.7,dt,places=5)
   self.assertAlmostEqual(at(stem,'x1',u),at(post,'cx',u),places=5);self.assertAlmostEqual(at(stem,'x2',u),at(post,'cx',u),places=5)
   w=math.exp(-dt/18) if dt>0 else -math.exp(dt/14)
   self.assertAlmostEqual(at(point,'cy',u),257-60*w,places=5)
  for x in g.iter(N+'animate'):self.assertEqual(x.get('calcMode'),'discrete')
 def test_stdp_static_and_curve_coordinates(self):
  r=svg('stdp-spike-timing','still');g=r.find('.//*[@class="static-only"]');post,stem,point=list(g)
  self.assertEqual(float(post.get('cx')),412.5);self.assertEqual(float(point.get('cx')),426.5)
  self.assertAlmostEqual(float(point.get('cy')),257-60*math.exp(-15/18),places=5)
  for p in r.findall(N+'path'):
   if p.get('stroke') in ('#7953a6','#23785b'):
    xy=list(map(float,re.findall(r'-?\d+(?:\.\d+)?',p.get('d'))))
    for x,y in zip(xy[::2],xy[1::2]):
     dt=(x-326)/6.7;w=math.exp(-dt/18) if dt>0 else -math.exp(dt/14);self.assertAlmostEqual(y,257-60*w,places=5)
 def test_eprop_actual_trace_and_bar_scales(self):
  r=svg('eprop-local-credit');e=[0]
  for t in range(1,8):e.append(.7*e[-1]+int(t in (1,4)))
  points=list(map(float,re.findall(r'-?\d+(?:\.\d+)?',r.find('.//*[@id="eligibility-trace"]').get('d'))))
  for k,(x,y) in enumerate(zip(points[::2],points[1::2])):self.assertAlmostEqual(x,110+60*k);self.assertAlmostEqual(y,149-50*e[k],places=5)
  for t,L in [(3,1.2),(5,-.4)]:
   for row,v,baseline,scale in [('signal',L,227,25),('product',L*e[t],292,35)]:
    b=r.find(f'.//*[@id="{row}-{t}"]/{N}rect');self.assertAlmostEqual(float(b.get('height')),abs(v)*scale,places=5);self.assertAlmostEqual(float(b.get('y')),baseline-max(v,0)*scale,places=5)
  self.assertAlmostEqual(1.2*e[3]-.4*e[5],.21196)
 def test_products_cannot_arrive_before_time_cursor(self):
  r=svg('eprop-local-credit');clip=r.find('.//*[@id="trace-progress"]/'+N+'rect')
  for t in (3,5):
   for row in ('signal','product'):
    g=r.find(f'.//*[@id="{row}-{t}"]');on=float(g.find(N+'animate').get('keyTimes').split(';')[1]);self.assertAlmostEqual(on,.9*t/7,places=6)
    self.assertEqual(at(g,'opacity',on-.00001),0);self.assertEqual(at(g,'opacity',on+.00001),1)
    self.assertAlmostEqual(at(clip,'width',on),60*t,places=3)
  self.assertIn('Σ = +0.21196',''.join(r.itertext()))
 def test_fallbacks_have_no_motion_and_all_data_visible(self):
  for stem in ('stdp-spike-timing','eprop-local-credit'):
   r=svg(stem,'still');self.assertFalse(any(e.tag in (N+'animate',N+'animateTransform',N+'animateMotion') for e in r.iter()));self.assertFalse(r.findall('.//*[@class="motion-only"]'));self.assertIsNone(r.find('.//*[@class="static-only"]').get('style'))
 def test_bilingual_focus_sourcehooks_and_gradient_sign(self):
  from verify_concept_motion import verify_source_pair
  for topic,stem in [('stdp','stdp-spike-timing'),('eprop','eprop-local-credit')]:
   for lang in ('','.zh-TW'):
    p=ROOT/f'docs/brain-mind/snn-neuromorphic/{topic}/index{lang}.md';s=p.read_text();self.assertFalse(verify_source_pair(p,s,stem));self.assertIn('tabindex="0"',s);self.assertIn('overflow-x:auto',s);self.assertIn('width:640px',s);self.assertIn('aria-label=',s)
    if topic=='eprop':self.assertIn(r'\Delta W_{ji} &= -\eta\,\widehat g_{ji}',s);self.assertIn('0.9401',s);self.assertIn('BPTT',s)
 def test_wrong_zero_crossing_is_detected(self):
  r=svg('stdp-spike-timing');point=list(r.find('.//*[@id="stdp-sample"]'))[-1];a=next(x for x in point if x.get('attributeName')=='cy');self.assertEqual(a.get('calcMode'),'discrete');a.attrib.pop('calcMode');u=(.9*29/59+.9*30/59)/2
  dt=(at(point,'cx',u)-326)/6.7;expected=257-60*(-math.exp(dt/14));self.assertGreater(abs(at(point,'cy',u)-expected),30)
if __name__=='__main__':unittest.main()
