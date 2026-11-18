"""Actual-SVG Gaussian tuning and discrete episodic successor accounting."""
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
 a=next((a for a in el.findall(N+'animate') if a.get('attributeName')==name),None);return value(a,t) if a is not None else float(el.get(name))
def root(stem,kind='motion'):return E.parse(R/f'docs/assets/concept-animations/{stem}-{kind}.svg').getroot()
class Navigation(unittest.TestCase):
 def test_actual_gaussian_bars_follow_actual_position(self):
  r=root('place-cell-firing');dots=[e for e in r.iter(N+'circle') if e.findall(N+'animate')];bars=[e for e in r.iter(N+'rect') if e.findall(N+'animate')];centers=[(389,182),(234,244),(79,182)]
  for i in range(10001):
   t=i/10000;x,y=[attr(dots[0],a,t) for a in ['cx','cy']]
   self.assertAlmostEqual(((x-234)/155)**2+((y-182)/62)**2,1,delta=.00007)
   for a in ['cx','cy']:self.assertEqual(attr(dots[0],a,t),attr(dots[1],a,t))
   for bar,(cx,cy) in zip(bars,centers):self.assertAlmostEqual(attr(bar,'width',t)/107,math.exp(-((x-cx)**2+(y-cy)**2)/(2*49**2)),delta=.00032)
 def test_visits_only_on_arrival_and_reward_revaluation_preserves_M(self):
  r=root('successor-occupancy');dot=next(c for c in r.iter(N+'circle') if c.find(N+'animate') is not None and c.find(N+'animate').get('attributeName')=='cx');bars=[e for e in r.iter(N+'rect') if e.findall(N+'animate')];rewards=[e for e in r.iter(N+'circle') if e.get('fill')=='#816ac1'];texts=[e for e in r.iter(N+'text') if (e.text or '').startswith('V=')]
  for i in range(10000):
   t=i/10000;x=attr(dot,'cx',t);self.assertAlmostEqual(x,90+460*min(t/.6,1),delta=1e-8)
   for j,b in enumerate(bars):
    expected=.7**j if t+1e-12>=j*.15 else 0
    self.assertAlmostEqual(attr(b,'height',t)/50,expected,places=10);self.assertAlmostEqual(attr(b,'y',t)+attr(b,'height',t),273,places=10)
   self.assertEqual([attr(c,'opacity',t) for c in rewards],[1,0] if t<.8 else [0,1])
   self.assertEqual([attr(e,'opacity',t) for e in texts],[0,0] if t<.6 else ([1,0] if t<.8 else [0,1]))
  self.assertAlmostEqual(.7**4,.2401);self.assertAlmostEqual(.7**2,.49)
 def test_actual_player_repeated_media_navigation(self):
  subprocess.run(['node','scripts/test_navigation_player.cjs'],cwd=R,check=True)
 def test_source_hooks_readability_and_scoped_shared_player(self):
  for topic in ['place-cells','successor-representation']:
   for lang in ['', '.zh-TW']:
    s=(R/f'docs/brain-mind/navigation-cognitive-maps/{topic}/index{lang}.md').read_text()
    for mark in ['data-source-asset-urls','data-motion-src','data-still-src','$$','Tab']:self.assertIn(mark,s)
  js=(R/'docs/javascripts/concept-motion.js').read_text();css=(R/'docs/stylesheets/concept-motion.css').read_text()
  self.assertIn('if (navigation)',js);self.assertIn('concept-motion-navigation',js);self.assertIn('.concept-motion-player.concept-motion-navigation img',css);self.assertIn('min-width:640px',css)
if __name__=='__main__':unittest.main()
