"""Check the actual intervention geometry and demonstration-history timeline."""
from pathlib import Path
import bisect,unittest,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1];ASSETS=ROOT/'docs/assets/concept-animations';NS='{http://www.w3.org/2000/svg}'
def read(stem,kind='motion'):return ET.parse(ASSETS/f'{stem}-{kind}.svg').getroot()
def at(e,attr,t):
 a=next((a for a in e.findall(NS+'animate') if a.get('attributeName')==attr),None)
 if a is None:return float(e.get(attr,'1' if attr=='opacity' else '0'))
 v=list(map(float,a.get('values').split(';')));k=list(map(float,a.get('keyTimes').split(';')));i=min(len(k)-1,max(0,bisect.bisect_right(k,t)-1))
 if a.get('calcMode')=='discrete' or i==len(k)-1:return v[i]
 q=(t-k[i])/(k[i+1]-k[i]);return v[i]*(1-q)+v[i+1]*q
class CausalImitationTests(unittest.TestCase):
 def test_actual_lamp_geometry_matches_defined_signal(self):
  r=read('causal-lamp-intervention');lamp=next(e for e in r.iter() if e.get('class')=='lamp');bar=next(e for e in r.iter() if e.get('class')=='shortcut')
  for i in range(10001):
   t=i/10000;l=(at(lamp,'opacity',t)-.08)/.92
   self.assertGreaterEqual(l,-1e-12);self.assertLessEqual(l,1+1e-12);self.assertAlmostEqual(at(bar,'width',t)/376,l,places=12)
  for e in r.iter():
   if e.get('class')=='fixed':self.assertEqual(e.get('width'),'376');self.assertFalse(list(e))
  self.assertTrue(any(e.get('d')=='M414 108 L424 124 M421 108 L431 124' for e in r.iter(NS+'path')))
  for kind in ['motion','still']:
   rr=read('causal-lamp-intervention',kind);self.assertIn('width:0px',rr.find(NS+'style').text)
  still=read('causal-lamp-intervention','still');self.assertEqual(next(e for e in still.iter() if e.get('class')=='shortcut').get('width'),'0')
 def test_copycat_sequence_errors_and_forward_only_cursor(self):
  for kind in ['motion','still']:
   r=read('copycat-action-lag',kind);expert=[e.text for e in r.iter(NS+'text') if e.get('y')=='137'];copy=[e.text for e in r.iter(NS+'text') if e.get('y')=='214'];self.assertEqual(expert,['GO']*3+['STOP']*3+['GO']*2);self.assertEqual(copy,['GO']+expert[:-1]);self.assertEqual([i for i,(a,b) in enumerate(zip(expert,copy)) if a!=b],[3,6])
   boxes=[e for e in r.iter(NS+'rect') if e.get('stroke-dasharray')=='5 3'];self.assertEqual([float(e.get('x'))+26 for e in boxes],[343,505])
  r=read('copycat-action-lag');cursor=next(e for e in r.iter() if e.get('class')=='moving');xs=[at(cursor,'x',i/10000) for i in range(10001)];self.assertEqual(xs,sorted(xs));self.assertEqual(xs[0],154);self.assertEqual(xs[-1],532)
 def test_bilingual_hooks_and_no_global_special_case(self):
  for lang in ['', '.zh-TW']:
   s=(ROOT/f'docs/theory/paradigms/imitation/behavioural-cloning/causal-confusion{lang}.md').read_text();self.assertEqual(s.count('data-source-asset-urls'),2);self.assertEqual(s.count('tabindex="0"'),2);self.assertEqual(s.count('width:100%;overflow-x:auto'),2);self.assertIn('75%',s)
  self.assertNotIn('causal-imitation-motion',(ROOT/'docs/javascripts/concept-motion.js').read_text())
if __name__=='__main__':unittest.main()
