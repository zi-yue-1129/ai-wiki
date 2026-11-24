"""Independent equations against actual SVG SMIL attributes, including intermediate times."""
from pathlib import Path
import math,re,unittest,xml.etree.ElementTree as E
N='{http://www.w3.org/2000/svg}'
ASSETS=Path(__file__).resolve().parents[1]/'docs/assets/concept-animations'
STEMS=['conformal-'+s for s in ['subgroup-coverage','shift-coverage','cqr-expansion','weighted-quantile','aps-cumulative','alpha-staircase','mondrian-groups','raps-penalty']]
NUM=r'-?(?:\d+(?:\.\d*)?|\.\d+)'
def root(s):return E.parse(ASSETS/(s+'-motion.svg')).getroot()
def value(e,attr,t):
 a=next((a for a in e if a.get('attributeName')==attr),None)
 if a is None:return e.get(attr)
 vs=a.get('values').split(';');ts=list(map(float,a.get('keyTimes').split(';')));i=max(i for i,k in enumerate(ts) if k<=t+1e-13)
 if a.get('calcMode')=='discrete' or i==len(vs)-1:return vs[i]
 u=(t-ts[i])/(ts[i+1]-ts[i]);xs=list(map(float,re.findall(NUM,vs[i])));ys=list(map(float,re.findall(NUM,vs[i+1])));it=iter(x+u*(y-x) for x,y in zip(xs,ys))
 return re.sub(NUM,lambda _:str(next(it)),vs[i])
def num(e,a,t):return float(value(e,a,t))
class Review(unittest.TestCase):
 def test_shift_boolean_colours(self):
  r=root('conformal-shift-coverage');cs=list(r.iter(N+'circle'))
  for t in [i/4000 for i in range(4000)]:
   for c in cs:
    if abs(num(c,'cx',t)-336.62)<1e-9:continue # right-hand state at a measure-zero SMIL switch
    self.assertEqual(value(c,'fill',t),'#168575' if num(c,'cx',t)<=336.62 else '#cf795a')
 def test_mondrian_membership(self):
  r=root('conformal-mondrian-groups');line=next(e for e in r.iter(N+'line') if e.find(N+'animate') is not None);texts=[e for e in r.iter(N+'text') if e.get('y')=='255' and e.find(N+'animate') is not None]
  for t in [i/4000 for i in range(4000)]:
   included=(num(line,'x1',t)-132)/402>=.72
   if abs((num(line,'x1',t)-132)/402-.72)<1e-10:continue # one-sided transition rendering at exact crossing
   for e in texts:self.assertEqual(num(e,'opacity',t),int((e.text=='IN')==included))
 def test_raps_path_marker_membership(self):
  r=root('conformal-raps-penalty');path=next(e for e in r.iter(N+'path') if e.find(N+'animate') is not None);cs=[e for e in r.iter(N+'circle') if e.get('r')=='5.5'];texts=[e for e in r.iter(N+'text') if e.get('x')=='448']
  for t in [i/4000 for i in range(4000)]:
   frac=0 if t<.18 else (t-.18)/.3 if t<.48 else 1 if t<.65 else ( .86-t)/.21 if t<.86 else 0
   scores=[.45,.75,.9+.1*frac,1+.2*frac];pts=list(map(float,re.findall(NUM,value(path,'d',t))))
   for i,(c,score) in enumerate(zip(cs,scores)):
    self.assertAlmostEqual(num(c,'cy',t),276-125*score,7);self.assertAlmostEqual(pts[2*i+1],num(c,'cy',t),7)
   if abs(scores[2]-.95)<1e-10:continue
   for e in texts:self.assertEqual(num(e,'opacity',t),int((e.text=='A B C')==(scores[2]<=.95)))
 def test_weighted_quantile_from_bar_mass(self):
  r=root('conformal-weighted-quantile');bars=[e for e in r.iter(N+'rect') if e.find(N+'animate') is not None];indicator=next(e for e in r.iter(N+'g') if e.find(N+'animateTransform') is not None)
  for t in [i/5000 for i in range(5000)]:
   weights=[num(e,'height',t)/28 for e in bars];cum=0
   for i,w in enumerate(weights):
    cum+=w
    if cum>=.7*sum(weights)-1e-12:break
   if abs(cum-.7*sum(weights))<1e-10:continue # reverse crossing uses its right-hand state
   self.assertAlmostEqual(float(value(indicator,'transform',t).split()[0]),[116,185,254,323,392,514][i])
 def test_alpha_ceiling(self):
  r=root('conformal-alpha-staircase');c=next(e for e in r.iter(N+'circle') if e.find(N+'animate') is not None)
  for t in [i/5000 for i in range(5000)]:
   alpha=.08+.42*min(t/.85,1);k=math.ceil(9*(1-alpha)-1e-11)
   self.assertAlmostEqual(num(c,'cx',t),105+(alpha-.06)*425/.48,7);self.assertEqual(num(c,'cy',t),125+38*(9-k))
 def test_cqr_interval_geometry(self):
  r=root('conformal-cqr-expansion');rects=[e for e in r.iter(N+'rect') if e.find(N+'animate') is not None]
  for t in [i/1000 for i in range(1000)]:
   q=.35*(0 if t<.16 else (t-.16)/.44 if t<.60 else 1 if t<.84 else (1-t)/.16)
   for e,(lo,hi) in zip(rects,[(1,2),(3,4.7)]):
    self.assertAlmostEqual(num(e,'x',t),90+85*(lo-q));self.assertAlmostEqual(num(e,'width',t),85*(hi-lo+2*q))
 def test_aps_decisions_after_mass(self):
  r=root('conformal-aps-cumulative');groups=[e for e in r.iter(N+'g') if e.find(N+'animate') is not None];cover=next(e for e in r.iter(N+'rect') if e.find(N+'animate') is not None)
  for t in [i/5000 for i in range(5000)]:
   mass=(num(cover,'x',t)-115)/400
   for e,score,completion in zip(groups,[.45,.75,.9,1],[.27,.46,.65,.78]):
    self.assertEqual(num(e,'opacity',t),int(completion<=t<.94))
    if num(e,'opacity',t):self.assertGreaterEqual(mass+1e-10,score)
 def test_subgroup_counts(self):
  r=root('conformal-subgroup-coverage');cs=[e for e in r.iter(N+'circle') if e.get('r')=='14']
  self.assertEqual([sum(c.get('fill')=='#168575' for c in cs[i:i+10]) for i in [0,10]],[9,7])
 def test_near_discrete_boundaries(self):
  r=root('conformal-shift-coverage')
  for c in r.iter(N+'circle'):
   a=next(e for e in c if e.get('attributeName')=='fill');ts=list(map(float,a.get('keyTimes').split(';')))
   if len(ts)!=2 or ts[1]==1:continue
   for t in [ts[1]-1e-8,ts[1]+1e-8]:self.assertEqual(value(c,'fill',t),'#168575' if num(c,'cx',t)<=336.62 else '#cf795a')
  r=root('conformal-alpha-staircase');c=next(e for e in r.iter(N+'circle') if e.find(N+'animate') is not None)
  for j in range(1,5):
   boundary=.85*(j/9-.08)/.42
   for t in [boundary-1e-8,boundary+1e-8]:
    alpha=.08+.42*t/.85;self.assertEqual(num(c,'cy',t),125+38*(9-math.ceil(9*(1-alpha))))
 def test_mobile_sources_and_no_animation_in_stills(self):
  from html.parser import HTMLParser
  class Wrappers(HTMLParser):
   def __init__(self):super().__init__();self.stack=[];self.images=[]
   def handle_starttag(self,tag,attrs):
    d=dict(attrs)
    if tag=='div':self.stack.append(d)
    if tag=='img' and 'data-motion-src' in d:self.images.append(self.stack[-2:])
   def handle_endtag(self,tag):
    if tag=='div':self.stack.pop()
  for lang in ['', '.zh-TW']:
   p=ASSETS.parents[1]/('theory/paradigms/probabilistic/uncertainty-calibration/conformal-prediction'+lang+'.md');s=p.read_text();parser=Wrappers();parser.feed(s)
   self.assertNotIn('\\(',s)
   self.assertEqual(len(parser.images),9)
   for outer,inner in parser.images:
    self.assertEqual(outer.get('tabindex'),'0');self.assertEqual(outer.get('role'),'region');self.assertIn('reviewed-motion-scroll',outer.get('class',''));self.assertIn('640px',inner['style'])
  for stem in STEMS:
   r=E.parse(ASSETS/(stem+'-still.svg')).getroot();self.assertFalse(any(e.tag.split('}')[-1].startswith('animate') for e in r.iter()))
if __name__=='__main__':unittest.main()
