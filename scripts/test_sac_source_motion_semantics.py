from pathlib import Path
import bisect,math,re,unittest,xml.etree.ElementTree as E
from html.parser import HTMLParser
R=Path(__file__).resolve().parents[1];A=R/'docs/assets/concept-animations';N='{http://www.w3.org/2000/svg}'
def value(a,t):
 v=list(map(float,a.get('values').split(';')));k=list(map(float,a.get('keyTimes').split(';')));assert len(k)==len(v) and k[0]==0 and k[-1]==1 and all(x<y for x,y in zip(k,k[1:]));i=min(len(v)-2,max(0,bisect.bisect_right(k,t)-1))
 return v[min(len(v)-1,bisect.bisect_right(k,t)-1)] if a.get('calcMode')=='discrete' else v[i]+(v[i+1]-v[i])*(t-k[i])/(k[i+1]-k[i])
def check(r,stem):
 for a in r.iter(N+'animate'):value(a,.5)
 packets=r.findall(N+'circle');assert len(packets)==2
 for c in packets:
  a=c.find(N+'animateMotion');assert a.get('begin')=='0s' and a.get('dur')=='10s' and a.get('calcMode')=='linear';assert a.get('keyPoints')=='0;0;1;1'
 if stem=='sac-soft-target':
  bars=[e for e in r.findall(N+'rect') if e.get('x')=='92' and e.get('fill') in ['#3269ad','#078f91']];assert [float(e.get('width')) for e in bars]==[4.2*35,3.8*35]
  out=next(e for e in r.findall(N+'text') if e.text=='1 + 0.9 × 3.94 = 4.546').find(N+'animate')
  for i in range(1001):
   t=i/1000
   if value(out,t)>0:assert all(t>=float(c.find(N+'animateMotion').get('keyTimes').split(';')[2]) for c in packets)
 else:
  bars=[e for e in r.findall(N+'rect') if e.get('class')=='moving'];assert len(bars)==2
  for c,b,vals in zip(packets,bars,[[100,100,135,135,100],[135,135,110,110,135]]):
   a=b.find(N+'animate');assert list(map(float,a.get('values').split(';')))==vals
   path=c.find(N+'animateMotion').get('path');assert any(p.get('d')==path for p in r.findall(N+'path'))
   end=float(c.find(N+'animateMotion').get('keyTimes').split(';')[2])
   for i in range(1001):
    t=i/1000
    if abs(value(a,t)-vals[0])>1e-8:assert t>=end
def check_wrappers(s):
 class Regions(HTMLParser):
  def __init__(self):super().__init__();self.stack=[];self.images=[]
  def handle_starttag(self,tag,attrs):
   a=dict(attrs)
   if tag=='div':self.stack.append(a)
   if tag=='img':self.images.append((a,list(self.stack)))
  def handle_endtag(self,tag):
   if tag=='div':self.stack.pop()
 parser=Regions();parser.feed(s)
 for stem in ['sac-soft-target','sac-temperature-feedback']:
  found=[(a,regions) for a,regions in parser.images if a.get('src','').endswith(stem+'-still.svg')]
  assert len(found)==1
  a,regions=found[0]
  assert 'data-source-asset-urls' in a
  assert a.get('data-motion-src','').endswith(stem+'-motion.svg')
  assert a.get('data-still-src','').endswith(stem+'-still.svg')
  assert any(r.get('tabindex')=='0' and r.get('role')=='region' and 'overflow-x:auto' in r.get('style','') for r in regions)
 assert r'\begin{gathered}' in s and '\n$\n' not in s
class Sac(unittest.TestCase):
 def test_actual_geometry_causality(self):
  for s in ['sac-soft-target','sac-temperature-feedback']:check(E.parse(A/(s+'-motion.svg')).getroot(),s)
 def test_numeric_target_terminal_and_dual_sign(self):
  for d in [0,1]:self.assertAlmostEqual(1+.9*(1-d)*(min(4.2,3.8)-.2*(-.7)),4.546 if not d else 1)
  # J(alpha)=alpha*(H-H*) with detached entropy; descent gives stated directions.
  for h,sign in [(.5,1),(1.4,-1)]:self.assertEqual(math.copysign(1,-(h-1)),sign)
 def test_early_target_negative(self):
  r=E.parse(A/'sac-soft-target-motion.svg').getroot();next(e for e in r.findall(N+'text') if e.text.startswith('1 +')).find(N+'animate').set('keyTimes','0;.1;.2;.96;1')
  with self.assertRaises(AssertionError):check(r,'sac-soft-target')
 def test_early_feedback_negative(self):
  r=E.parse(A/'sac-temperature-feedback-motion.svg').getroot();next(e for e in r.findall(N+'rect') if e.get('class')=='moving').find(N+'animate').set('keyTimes','0;.1;.2;.95;1')
  with self.assertRaises(AssertionError):check(r,'sac-temperature-feedback')
 def test_bilingual_wrappers(self):
  for p in (R/'docs/theory/paradigms/reinforcement-learning/policy-gradient-and-actor-critic/sac').glob('index*.md'):
   check_wrappers(p.read_text())
 def test_missing_source_focus_negative(self):
  s=(R/'docs/theory/paradigms/reinforcement-learning/policy-gradient-and-actor-critic/sac/index.md').read_text()
  # An unrelated focusable diagram must not mask missing focus on either SAC source.
  bad=s.replace('<div tabindex="0" role="region" aria-label="Horizontally scrollable SAC diagram"','<div role="region" aria-label="Horizontally scrollable SAC diagram"',1)
  with self.assertRaises(AssertionError):check_wrappers(bad)
if __name__=='__main__':unittest.main()
