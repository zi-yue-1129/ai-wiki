"""Actual-SVG confidence gates and EMA arithmetic."""
import subprocess,math,bisect,unittest,xml.etree.ElementTree as E
from functools import lru_cache
from pathlib import Path
R=Path(__file__).resolve().parents[1];N='{http://www.w3.org/2000/svg}'
@lru_cache(None)
def spec(a):
 v=list(map(float,a.get('values').split(';')));k=list(map(float,a.get('keyTimes').split(';'))) if a.get('keyTimes') else [i/(len(v)-1) for i in range(len(v))];return v,k

def value(a,t):
 v,k=spec(a);i=min(bisect.bisect_right(k,t)-1,len(v)-2)
 if a.get('calcMode')=='discrete':return v[i]
 u=(t-k[i])/(k[i+1]-k[i]);return v[i]*(1-u)+v[i+1]*u

def attr(el,name,t):
 a=next((a for a in el.findall(N+'animate') if a.get('attributeName')==name),None);
 if a is None:return float(el.get(name))
 begin=float(a.get('begin','0s')[:-1])/12
 return float(el.get(name)) if t<begin else value(a,(t-begin)%1)
def root(stem,kind='motion'):return E.parse(R/f'docs/assets/concept-animations/{stem}-{kind}.svg').getroot()
class Semi(unittest.TestCase):
 def test_actual_fixmatch_highlights_follow_particle_arrival(self):
  r=root('fixmatch-confidence-gate');dots=[e for e in r.iter(N+'circle') if e.findall(N+'animate')];highlights=[e for e in r.iter(N+'rect') if e.findall(N+'animate')]
  for a in r.iter(N+'animate'):
   v,k=spec(a);self.assertEqual(k[0],0);self.assertEqual(k[-1],1);self.assertEqual(len(v),len(k))
  for i in range(20000):
   t=i/10000
   for dot,h,end in zip(dots,highlights,[538,332]):
    if attr(h,'opacity',t)>0:self.assertAlmostEqual(attr(dot,'cx',t),end)
   self.assertLessEqual(attr(dots[1],'cx',t),332+1e-9)
  for e in r.iter(N+'rect'):
   if e.get('x')=='161' and e.get('height')=='10':self.assertAlmostEqual(float(e.get('width'))/117,.97 if e.get('y')=='137' else .82)
 def test_actual_sampled_ema_paths_and_marker_interpolation(self):
  r=root('mean-teacher-ema-tracking');st=[.15,.85,.35,.95,.5];tea=[.15]
  for x in st[1:]:tea.append(.75*tea[-1]+.25*x)
  dots=[e for e in r.iter(N+'circle') if e.findall(N+'animate')]
  for i in range(10000):
   t=i/10000;j=min(int(t*4),3);u=t*4-j
   for e,vals in zip(dots,[st,tea]):
    self.assertAlmostEqual(attr(e,'cx',t),82+480*t)
    self.assertAlmostEqual((238-attr(e,'cy',t))/140,vals[j]*(1-u)+vals[j+1]*u)
  fixed=[e for e in r.iter(N+'circle') if e.get('fill')=='#169b86' and not e.findall(N+'animate')]
  for e,v in zip(fixed,tea):self.assertAlmostEqual((238-float(e.get('cy')))/140,v)
 def test_actual_lab_and_bilingual_source_readability(self):
  subprocess.run(['node','scripts/test_semi_process_lab_semantics.cjs'],cwd=R,check=True)
  for name in ['fixmatch','mean-teacher']:
   for lang in ['', '.zh-TW']:
    s=(R/f'docs/theory/paradigms/semi-supervised/consistency-regularisation/{name}{lang}.md').read_text()
    for mark in ['data-source-asset-urls','data-motion-src','data-still-src','concept-motion-scroll','min-width:640px','Tab','semi-process-lab']:self.assertIn(mark,s)
if __name__=='__main__':unittest.main()
