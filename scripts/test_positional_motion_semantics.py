"""Independent numerical audit of the actual positional SVG timelines, not JS mocks."""
import math, re, unittest
from pathlib import Path
from xml.etree import ElementTree as E
N='{http://www.w3.org/2000/svg}'
ROOT=Path(__file__).resolve().parents[1]
STEMS=('alibi-content-recency','alibi-distance-softmax','alibi-head-prefix','rope-axial-2d','rope-cache-reindex','rope-frequency-bands','rope-interpolation-angle','shaw-relative-clipping','shaw-relative-value','sinusoidal-multiscale','yarn-attention-temperature','yarn-frequency-ramp')
def root(s):return E.parse(ROOT/f'docs/assets/concept-animations/{s}-motion.svg').getroot()
def active(s):return root(s).find(N+"g[@class='motion-layer']")
def elements(s,tag):return [e for e in active(s).iter(N+tag) if any(a.tag in (N+'animate',N+'animateTransform') for a in e)]
def value(e,attr,t):
 a=next((a for a in e if a.get('attributeName')==attr),None)
 if a is None:return float(e.get(attr))
 vs=(a.get('values') or a.get('from')+';'+a.get('to')).split(';');vs=[list(map(float,v.split())) for v in vs];dis=a.get('calcMode')=='discrete'
 ts=list(map(float,a.get('keyTimes').split(';'))) if a.get('keyTimes') else [i/(len(vs) if dis else len(vs)-1) for i in range(len(vs))]
 i=max(i for i,x in enumerate(ts) if x<=t+1e-12)
 if i==len(vs)-1 or dis:v=vs[i]
 else:
  u=(t-ts[i])/(ts[i+1]-ts[i]);v=[x+u*(y-x) for x,y in zip(vs[i],vs[i+1])]
 return v if attr=='transform' else v[0]
def soft(xs):
 es=[math.exp(x-max(xs)) for x in xs];return [x/sum(es) for x in es]
class PositionalAudit(unittest.TestCase):
 def test_contracts(self):
  for s in STEMS:
   r=root(s);self.assertIsNotNone(active(s));self.assertIsNotNone(r.find(N+"g[@class='still-layer']"));self.assertIn('prefers-reduced-motion',E.tostring(r,encoding='unicode'))
   self.assertLess((ROOT/f'docs/assets/concept-animations/{s}-motion.svg').stat().st_size,51200)
   for a in r.iter(N+'animate'):
    vs=a.get('values').split(';');ts=a.get('keyTimes')
    if ts:
     ts=list(map(float,ts.split(';')));self.assertEqual(len(vs),len(ts));self.assertEqual(ts[0],0);self.assertEqual(ts[-1],1);self.assertTrue(all(b>a for a,b in zip(ts,ts[1:])))
 def test_alibi_distribution_actual_axis(self):
  bars=elements('alibi-distance-softmax','rect');self.assertEqual(len(bars),8)
  for k in range(1001):
   t=k/1000;m=min(t/.83,1);expected=soft([-m*d for d in range(7,-1,-1)])
   for e,p in zip(bars,expected):
    self.assertAlmostEqual(value(e,'y',t)+value(e,'height',t),260,places=3);self.assertLess(abs(value(e,'height',t)-225*p),.025)
   self.assertAlmostEqual(sum(value(e,'height',t) for e in bars)/225,1,places=5)
 def test_alibi_competition(self):
  cs=elements('alibi-content-recency','circle');self.assertEqual(len(cs),2)
  for k in range(501):
   t=k/500;m=(value(cs[0],'cx',t)-82)/494;p=soft([2-4*m,-3*m,-2*m,-m,0])
   for e,q in zip(cs,[p[0],p[-1]]):self.assertLess(abs(value(e,'cy',t)-(303-200*q)),.04)
 def test_prefix_distribution_and_causality(self):
  es=elements('alibi-head-prefix','rect');bars=es[:24];self.assertEqual(len(bars),24)
  for h,m in enumerate([.25,.5,1]):
   for i in range(8):
    ps=soft([-m*(i-j) for j in range(i+1)])
    for j in range(8):self.assertAlmostEqual(value(bars[h*8+j],'opacity',(i+.2)/8),0 if j>i else .06+.9*ps[j],delta=.00051)
 def test_axial_rotations_and_cosine(self):
  cs=elements('rope-axial-2d','circle');ar=elements('rope-axial-2d','g')
  for k in range(1001):
   t=k/1000;dx=(value(cs[0],'cx',t)-110)/43;dy=(value(cs[0],'cy',t)-143)/43
   ax=value(ar[0],'transform',t)[0];ay=value(ar[1],'transform',t)[0]
   self.assertAlmostEqual(ax,-60*dx);self.assertAlmostEqual(ay,-90*dy)
   self.assertLess(abs(value(cs[1],'cx',t)-(485+50*(math.cos(math.radians(ax))+math.cos(math.radians(ay))))),.026)
 def test_frequency_shared_phase_and_norm(self):
  cs=elements('rope-frequency-bands','circle');ar=elements('rope-frequency-bands','g')
  for k in range(1001):
   t=k/1000
   for e,a,w in zip(cs,ar,[math.pi/2,math.pi/10]):
    d=(value(e,'cx',t)-63)/516*16;ang=value(a,'transform',t)[0]*math.pi/180
    self.assertAlmostEqual(ang,-w*d,places=6);self.assertAlmostEqual(math.sin(ang)**2+math.cos(ang)**2,1)
    self.assertLess(abs(value(e,'cy',t)-(292-38*math.cos(ang))),.12)
 def test_sinusoidal_continuous_channels(self):
  cs=elements('sinusoidal-multiscale','circle');ar=elements('sinusoidal-multiscale','g')
  for k in range(1001):
   t=k/1000
   for e,a,mid,period in zip(cs,ar,[109,191,273],[4,12,24]):
    p=(value(e,'cx',t)-70)/26.5;ang=value(a,'transform',t)[0]*math.pi/180
    self.assertAlmostEqual(ang,2*math.pi*p/period,places=5);self.assertLess(abs(value(e,'cy',t)-(mid-25*math.sin(ang))),.08)
 def test_pi_phase_scale(self):
  ar=elements('rope-interpolation-angle','g');cs=elements('rope-interpolation-angle','circle');bs=elements('rope-interpolation-angle','rect')
  for k in range(101):
   t=k/100;p=(value(cs[0],'cx',t)-100)/416*16
   for a,scale in zip(ar,[1,2]):self.assertAlmostEqual(-value(a,'transform',t)[0]*math.pi/180,.6*p/scale,delta=.0001)
   self.assertAlmostEqual(value(bs[0],'width',t),2*value(bs[1],'width',t))
 def test_shaw_clip(self):
  cs=elements('shaw-relative-clipping','circle')
  for k in range(1001):
   t=k/1000;i=(value(cs[0],'cx',t)-87)/60
   self.assertAlmostEqual(value(cs[0],'cy',t),226-22*(4-i));self.assertAlmostEqual(value(cs[1],'cy',t),226-22*max(-2,min(2,4-i)))
 def test_shaw_value_sync(self):
  cs=elements('shaw-relative-value','circle');q=elements('shaw-relative-value','rect')[0]
  for k in range(1001):
   t=k/1000;i=(value(cs[0],'cx',t)-85)/110;rel=.3*sum(w*max(-2,min(2,j-i)) for j,w in enumerate([.2,.5,.3]))
   self.assertAlmostEqual((value(q,'x',t)-62)/110,i)
   for e,v in zip(cs,[rel,rel-.1]):self.assertAlmostEqual(value(e,'cy',t),277.2-61*v)
 def test_yarn_ramp(self):
  bars=elements('yarn-frequency-ramp','rect')
  for k in range(101):
   t=k/100;rec=value(bars[0],'height',t)/178
   for e,r in zip(bars,[.5,1,1.5,2,3,4]):
    g=max(0,min(1,(r-1)/3));self.assertAlmostEqual(value(e,'height',t)/178,g+(1-g)*rec);self.assertAlmostEqual(value(e,'height',t)+value(e,'y',t),285)
 def test_yarn_softmax_entropy_same_time(self):
  bars=elements('yarn-attention-temperature','rect');self.assertEqual(len(bars),5)
  for k in range(1001):
   t=k/1000;lam=.5+1.5*t/.4 if t<=.4 else 2 if t<=.6 else 2-1.5*(t-.6)/.4;ps=soft([lam*c for c in [2,1,0,-1]])
   for e,p in zip(bars[:4],ps):self.assertLess(abs(value(e,'height',t)-170*p),.009);self.assertAlmostEqual(value(e,'height',t)+value(e,'y',t),277,places=3)
   h=-sum(p*math.log(p) for p in ps);self.assertLess(abs(value(bars[4],'width',t)-170*h/math.log(4)),.009)
 def test_cache_reveal(self):
  gs=elements('rope-cache-reindex','g');self.assertEqual(len(gs),5)
  for t in [.1,.34,.36,.49,.51,.9]:
   vs=[value(g,'opacity',t) for g in gs];self.assertEqual(vs[:3],[int(t>=.35)]*3);self.assertEqual(vs[3:],[int(t>=.5)]*2)
  self.assertAlmostEqual(math.cos(math.pi/6*(6-2)),-.5);self.assertAlmostEqual(math.cos(math.pi/6*(3-1)),.5)
 def test_bilingual_hooks_and_math(self):
  for suffix in ['', '.zh-TW']:
   s=(ROOT/f'docs/theory/models/transformer/positional-encodings/index{suffix}.md').read_text()
   self.assertEqual(s.count('class="concept-motion-scroll" tabindex="0"'),12);self.assertEqual(s.count('style="width:640px;min-width:640px"'),12)
   self.assertNotIn('\\(',s);self.assertNotIn('\\)',s)
   for formula in re.findall(r'\$([^$\n]+)\$',s):self.assertNotIn(' The ',formula);self.assertNotIn(' with ',formula)
   for stem in STEMS:self.assertIn(stem+'-motion.svg',s);self.assertIn(stem+'-still.svg',s)
   self.assertIn('\\omega(p/s)=(\\omega/s)p',s);self.assertIn('0.06+0.9p',s)
if __name__=='__main__':unittest.main()
