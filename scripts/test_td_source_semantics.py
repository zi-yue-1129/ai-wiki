"""Actual TD source assets: targets, geometry, route arrival, trace cut and negative controls."""
from pathlib import Path
import unittest,xml.etree.ElementTree as E,math,re
R=Path(__file__).resolve().parents[1];A=R/'docs/assets/concept-animations';N='{http://www.w3.org/2000/svg}'
STEMS=['q-sarsa-backup','q-sarsa-noisy-backups','q-sarsa-epsilon','double-dqn-selector','td-terminal-truncation','cliff-walking','eligibility-trace-cut','nstep-lambda-forward']
def root(s,k='motion'):return E.parse(A/f'{s}-{k}.svg').getroot()
def byid(r,i):return r.find(".//*[@id='"+i+"']")
def sample(a,t):
 v=list(map(float,a.get('values',a.get('keyPoints','0;1')).split(';')));k=list(map(float,a.get('keyTimes',';'.join(str(i/(len(v)-1)) for i in range(len(v)))).split(';')))
 for i in range(len(k)-1):
  if t<k[i+1]:return v[i] if a.get('calcMode')=='discrete' else v[i]+(v[i+1]-v[i])*(t-k[i])/(k[i+1]-k[i])
 return v[-1]
def attr(e,n,t):
 a=e.find(N+f"animate[@attributeName='{n}']");return float(e.get(n)) if a is None else sample(a,t)
def pts(s):
 tok=re.findall(r'[MLQHV]|-?\d+(?:\.\d+)?',s);out=[];i=0
 while i<len(tok):
  op=tok[i];i+=1
  if op in 'ML':out.append((float(tok[i]),float(tok[i+1])));i+=2
  elif op=='H':out.append((float(tok[i]),out[-1][1]));i+=1
  elif op=='V':out.append((out[-1][0],float(tok[i])));i+=1
  elif op=='Q':
   p=out[-1];q=(float(tok[i]),float(tok[i+1]));r=(float(tok[i+2]),float(tok[i+3]));i+=4
   for j in range(1,65):
    u=j/64;out.append(tuple((1-u)**2*p[k]+2*(1-u)*u*q[k]+u*u*r[k] for k in [0,1]))
  else:raise ValueError(op)
 return out
def point(a,t):
 ps=pts(a.get('path'));ds=[math.dist(p,q) for p,q in zip(ps,ps[1:])];wanted=sample(a,t)*sum(ds)
 for i,d in enumerate(ds):
  if wanted<=d:return tuple(ps[i][k]+(ps[i+1][k]-ps[i][k])*wanted/d for k in [0,1])
  wanted-=d
 return ps[-1]
def text(r):return [''.join(e.itertext()).strip() for e in r.iter(N+'text')]
def bar(r,y,c):return next(e for e in r.iter(N+'rect') if e.get('y')==str(y) and e.get('fill')==c)
def check_backup(r):
 for id_,target in [('q',3.75),('s',2.4)]:
  for i in range(1000):
   t=i/1000
   if attr(byid(r,id_+'-updated'),'opacity',t)>.9:assert abs(attr(byid(r,id_+'-updated-bar'),'width',t)/(59.3/2)-target)<.003
class TDSource(unittest.TestCase):
 def test_backup_actual_geometry_labels_negative(self):
  self.assertEqual(2+.5*(1+.9*5-2),3.75);self.assertAlmostEqual(2+.5*(1+.9*2-2),2.4);r=root(STEMS[0]);check_backup(r)
  byid(r,'q-updated').find(N+'animate').set('keyTimes','0;.60;.61;.96;1')
  with self.assertRaises(AssertionError):check_backup(r)
 def test_noisy_cases_and_means(self):
  cases=[(5,5),(5,3),(3,5),(3,3)];r=root(STEMS[1]);mx=[];sm=[]
  for i,(a,b) in enumerate(cases,1):
   x=float(''.join(byid(r,f'case-{i}-max').itertext()).strip());y=float(''.join(byid(r,f'case-{i}-sample').itertext()).strip());self.assertEqual(x,max(a,b));self.assertEqual(y,b);mx.append(x);sm.append(y)
  self.assertEqual(sum(mx)/4,4.5);self.assertEqual(sum(sm)/4,4);self.assertIn('4.5',text(root(STEMS[1],'still')))
 def test_epsilon_and_double_selection(self):
  ts=text(root(STEMS[2]));self.assertIn('90%',ts);self.assertIn('10%',ts);self.assertIn(f'{(.8+.2/2)*5.5+.2/2*2.8:.2f}',ts)
  for k in ['motion','still']:
   r=root(STEMS[3],k);self.assertEqual(''.join(byid(r,'dqn-target').itertext()).strip(),f'{1+.9*7:.2f}');self.assertEqual(''.join(byid(r,'double-target').itertext()).strip(),f'{1+.9*3:.2f}')
 def test_termination_and_packet_arrivals(self):
  for k in ['motion','still']:
   ts=text(root(STEMS[4],k));self.assertEqual(ts.count('1.00'),2);self.assertIn(f'{1+.9*4:.2f}',ts);self.assertIn(f'{1+.9*2:.2f}',ts)
  r=root(STEMS[4])
  for i,end,dst in [('q-pulse',.46,(120,479)),('s-pulse',.70,(323,479))]:
   e=byid(r,i);m=e.find(N+'animateMotion');self.assertEqual(m.get('dur'),'10s');self.assertTrue(all(abs(x-y)<1e-9 for x,y in zip(point(m,end),dst)));self.assertEqual(attr(e,'opacity',end),1)
 def test_cliff_routes_start_at_start_and_reach_goal(self):
  r=root(STEMS[5]);ends=[]
  for i,start,end in [('q-agent',.02,.30),('s-agent',.54,.90)]:
   e=byid(r,i);m=e.find(N+'animateMotion');self.assertEqual(m.get('dur'),'12s');self.assertEqual(m.get('begin'),'0s');self.assertEqual(point(m,start),(65,305));self.assertEqual(point(m,end),(377,305));self.assertEqual(attr(e,'opacity',start-.001),0);self.assertEqual(attr(e,'opacity',end),1);ends.append(pts(m.get('path')))
  self.assertEqual(min(y for x,y in ends[0]),253);self.assertEqual(min(y for x,y in ends[1]),201)
  self.assertEqual(attr(byid(r,'slip-agent'),'cy',.47),305);self.assertEqual(attr(byid(r,'slip-agent'),'opacity',.47),1)
 def test_trace_cut_discrete_and_decay(self):
  r=root(STEMS[6]);self.assertAlmostEqual(attr(bar(r,229,'#159f89'),'width',.8)/254,.72**2);self.assertAlmostEqual(attr(bar(r,270,'#159f89'),'width',.8)/254,.72);self.assertEqual(attr(bar(r,311,'#159f89'),'width',.8),254)
  for y,prior in [(429,254*.72),(470,254)]:
   b=bar(r,y,'#e49a39');self.assertAlmostEqual(attr(b,'width',.6799),prior);self.assertEqual(attr(b,'width',.68),0);self.assertEqual(b.find(N+'animate').get('calcMode'),'discrete')
  self.assertEqual(attr(bar(r,511,'#e49a39'),'width',.68),254)
 def test_nstep_returns_horizon_timing(self):
  vals=[1+.9*3,1-.9+.9**2,1-.9+.9**2*4+.9**3*2];r=root(STEMS[7]);ts=text(r)
  for v in vals:self.assertIn(f'{v:.3f}',ts)
  self.assertIn('Gλ = '+f'{sum(w*v for w,v in zip([.2,.16,.64],vals)):.5f}',ts)
  self.assertEqual(attr(byid(r,'nstep-lambda-forward-animated-25'),'cx',.97),449)
  for y,c,t in [(266,'#3285c5',.30),(346,'#7765c6',.51),(426,'#259985',.72)]:self.assertEqual(attr(bar(r,y,c),'width',t-.001),0)
 def test_all_bilingual_sourcehooks_and_svg_contract(self):
  for topic in ['q-learning','sarsa','double-dqn']:
   for lang in ['', '.zh-TW']:
    s=(R/f'docs/theory/paradigms/reinforcement-learning/value-based-methods/{topic}/index{lang}.md').read_text();n=1 if topic=='double-dqn' else 7;self.assertEqual(s.count('class="td-source-scroll" tabindex="0"'),n);self.assertEqual(s.count('data-source-asset-urls'),n)
  for st in STEMS:
   a=root(st);b=root(st,'still');self.assertEqual(a.get('viewBox'),b.get('viewBox'));self.assertFalse(any('animate' in x.tag for x in b.iter()));self.assertIn('prefers-reduced-motion',(A/f'{st}-motion.svg').read_text())
if __name__=='__main__':unittest.main()
