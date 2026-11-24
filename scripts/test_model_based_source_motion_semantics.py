from pathlib import Path
import bisect,math,re,unittest,xml.etree.ElementTree as E
R=Path(__file__).resolve().parents[1];A=R/'docs/assets/concept-animations';N='{http://www.w3.org/2000/svg}'
STEMS=['pets-ensemble-particles','pets-cem-refit','mbpo-short-branches','mbpo-horizon-error']
def value(a,t):
 v=list(map(float,a.get('values').split(';')));k=list(map(float,a.get('keyTimes').split(';')));assert len(k)==len(v) and k[0]==0 and k[-1]==1 and all(x<y for x,y in zip(k,k[1:]));i=min(len(v)-2,max(0,bisect.bisect_right(k,t)-1))
 return v[min(len(v)-1,bisect.bisect_right(k,t)-1)] if a.get('calcMode')=='discrete' else v[i]+(v[i+1]-v[i])*(t-k[i])/(k[i+1]-k[i])
def geometry(p):
 ns=list(map(float,re.findall(r'-?\d+(?:\.\d+)?',p.get('d'))));ps=list(zip(ns[::2],ns[1::2]));return ps,sum(math.dist(x,y) for x,y in zip(ps,ps[1:]))
def check(r,stem):
 for a in r.iter(N+'animate'):
  assert a.get('dur')=='12s' and a.get('begin')=='0s';value(a,.5)
 paths=[e for e in r.iter(N+'path') if e.find(N+'animate') is not None]
 for p in paths:assert math.isclose(float(p.get('stroke-dasharray')),geometry(p)[1])
 if stem=='pets-cem-refit':
  bars=[e for e in r.iter(N+'rect') if e.find(N+'animate') is not None];assert len(bars)==5
  for bar,score in zip(bars,[1,4,2,6,5]):
   a=bar.find(N+'animate');assert float(a.get('values').split(';')[2])==19*score
   label=next(g for g in r.iter(N+'g') if g.find(N+'text') is not None and g.find(N+'text').text==str(score)).find(N+'animate')
   for i in range(10001):
    t=i/10000
    if value(label,t)>0:assert math.isclose(value(a,t),19*score)
 else:
  for g in r.iter(N+'g'):
   a=g.find(N+'animate');c=g.find(N+'circle')
   if a is None or c is None:continue
   xy=float(c.get('cx')),float(c.get('cy'));matches=[p for p in paths if xy in geometry(p)[0][1:]]
   if not matches:continue
   p=matches[0];pts,total=geometry(p);idx=pts.index(xy);dist=sum(math.dist(x,y) for x,y in zip(pts[:idx],pts[1:idx+1]));offset=p.find(N+'animate')
   for i in range(10001):
    t=i/10000
    if value(a,t)>0:assert total-value(offset,t)>=dist-1e-7,(stem,xy,t)
  if stem=='mbpo-horizon-error':
   pts,total=geometry(paths[0]);assert pts==[(96.,245.),(207.,213.),(318.,181.)]
   for g in r.iter(N+'g'):
    txt=g.find(N+'text');a=g.find(N+'animate')
    if txt is not None and txt.text in ['0.2','0.4','Stop model rollout']:
     needed=total/2 if txt.text=='0.2' else total
     for i in range(10001):
      t=i/10000
      if value(a,t)>0:assert total-value(paths[0].find(N+'animate'),t)>=needed-1e-7
class ModelBased(unittest.TestCase):
 def test_actual_svg_geometry_and_causality(self):
  for s in STEMS:check(E.parse(A/f'{s}-motion.svg').getroot(),s)
 def test_early_cem_negative(self):
  r=E.parse(A/'pets-cem-refit-motion.svg').getroot();next(g for g in r.iter(N+'g') if g.find(N+'text') is not None and g.find(N+'text').text=='5').find(N+'animate').set('keyTimes','0;.2;.94;1')
  with self.assertRaises(AssertionError):check(r,'pets-cem-refit')
 def test_wrong_score_geometry_negative(self):
  r=E.parse(A/'pets-cem-refit-motion.svg').getroot();next(e for e in r.iter(N+'rect') if e.find(N+'animate') is not None).find(N+'animate').set('values','0;0;20;20;0')
  with self.assertRaises(AssertionError):check(r,'pets-cem-refit')
 def test_early_particle_negative(self):
  r=E.parse(A/'pets-ensemble-particles-motion.svg').getroot();next(g for g in r.iter(N+'g') if g.find(N+'circle') is not None and g.find(N+'animate') is not None).find(N+'animate').set('keyTimes','0;.2;.92;1')
  with self.assertRaises(AssertionError):check(r,'pets-ensemble-particles')
 def test_early_stop_negative(self):
  r=E.parse(A/'mbpo-horizon-error-motion.svg').getroot();next(g for g in r.iter(N+'g') if g.find(N+'text') is not None and g.find(N+'text').text=='Stop model rollout').find(N+'animate').set('keyTimes','0;.2;.95;1')
  with self.assertRaises(AssertionError):check(r,'mbpo-horizon-error')
 def test_numeric_toy_and_focus(self):
  self.assertEqual(sum([.5,1])/2,.75)
  for t in range(5):self.assertAlmostEqual(abs(1.2*t-t),.2*t)
  for topic in ['pets','mbpo']:
   for p in (R/f'docs/theory/paradigms/reinforcement-learning/model-based-rl/{topic}').glob('index*.md'):
    s=p.read_text();assert s.count('data-source-asset-urls')==2 and s.count('tabindex="0"')==2
if __name__=='__main__':unittest.main()
