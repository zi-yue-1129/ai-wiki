"""Actual-SVG motor-state geometry and minimal-intervention causal ordering."""
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
class Motor(unittest.TestCase):
 def test_actual_forward_coordinates_and_causal_order(self):
  r=root('forward-prediction-correction');get=lambda k:r.find('.//*[@id="'+k+'"]');pred,sense,corr=map(get,['prediction','sensation','correction'])
  for i in range(10000):
   t=i/10000
   p=.2+.4*min(1,max(0,(t-.12)/.18));c=.6+.15*min(1,max(0,(t-.5)/.2))
   self.assertAlmostEqual((attr(pred,'cx',t)-96)/445,p,places=10)
   self.assertAlmostEqual((attr(corr,'cx',t)-96)/445,c,places=10)
   self.assertAlmostEqual((attr(sense,'cx',t)-96)/445,.9,places=10)
   self.assertEqual(attr(sense,'opacity',t),int(t>=.5));self.assertEqual(attr(corr,'opacity',t),int(t>=.5))
  r=root('forward-prediction-correction','still')
  for ident,x in [('prediction',.6),('sensation',.9),('correction',.75)]:self.assertAlmostEqual((float(r.find('.//*[@id="'+ident+'"]').get('cx'))-96)/445,x)
  self.assertEqual(.6+.5*(.9-.6),.75)
 def test_actual_selective_correction_never_reverses_irrelevant_shift(self):
  r=root('ofc-selective-feedback');a=r.find('.//*[@id="relevant"]');b=r.find('.//*[@id="irrelevant"]')
  for i in range(10000):
   t=i/10000;perturb=min(1,max(0,(t-.12)/.18));correct=min(1,max(0,(t-.5)/.2))
   self.assertAlmostEqual(attr(a,'cy',t),240-94*perturb+94*correct)
   self.assertAlmostEqual(attr(b,'cx',t),469-78*perturb)
   self.assertEqual(float(b.get('cy')),240)
  self.assertEqual(float(root('ofc-selective-feedback','still').find('.//*[@id="relevant"]').get('cy')),240)
  self.assertEqual(float(root('ofc-selective-feedback','still').find('.//*[@id="irrelevant"]').get('cx')),391)
 def test_actual_player_and_source_hooks(self):
  subprocess.run(['node','scripts/test_motor_player.cjs'],cwd=R,check=True)
  for topic in ['internal-forward-models','optimal-feedback-control']:
   for lang in ['', '.zh-TW']:
    s=(R/f'docs/brain-mind/motor-control/{topic}/index{lang}.md').read_text()
    for mark in ['data-source-asset-urls','data-motion-src','data-still-src','Tab']:self.assertIn(mark,s)
  css=(R/'docs/stylesheets/concept-motion.css').read_text();self.assertIn('min-width:640px',css);self.assertIn('.concept-motion-motor .concept-motion-viewport',css)
if __name__=='__main__':unittest.main()
