"""Exact rendered SVG scalings, causal timing and loop-reset regressions."""
from pathlib import Path
import unittest,xml.etree.ElementTree as E,subprocess,copy
R=Path(__file__).resolve().parents[1];A=R/'docs/assets/concept-animations';N='{http://www.w3.org/2000/svg}'
def root(s):return E.parse(A/('alphazero-'+s+'-motion.svg')).getroot()
def el(r,i):return r.find(".//*[@id='"+i+"']")
def v(e,k,t):
 a=next((a for a in e.findall(N+'animate') if a.get('attributeName')==k),None)
 if a is None:return float(e.get(k,'1'))
 ts=list(map(float,a.get('keyTimes').split(';')));vs=list(map(float,a.get('values').split(';')));i=max(i for i,x in enumerate(ts) if x<=t)
 return vs[i] if a.get('calcMode')=='discrete' or i==len(vs)-1 else vs[i]+(vs[i+1]-vs[i])*(t-ts[i])/(ts[i+1]-ts[i])
def policy(r):
 for j in range(1000):
  t=j/1000;c=[(1,1,1),(4,8,3),(8,25,17),(12,54,34)][min(3,int(t*4))]
  for i in range(3):
   for prefix,h in [('prior',200*[.6,.3,.1][i]),('visits',2*c[i]),('target',200*c[i]/sum(c))]:
    e=el(r,f'{prefix}-{i}');assert abs(v(e,'height',t)-h)<1e-10;assert abs(v(e,'y',t)+h-275)<1e-10
class Tests(unittest.TestCase):
 def test_dense_policy(self):policy(root('policy-target'))
 def test_negative_wrong_interpolation(self):
  r=root('policy-target');el(r,'target-0').find(N+'animate').set('calcMode','linear')
  with self.assertRaises(AssertionError):policy(r)
 def test_puct_exact(self):
  r=root('puct-select')
  for i,(q,u) in enumerate(zip([.6,.48,.3],[.12,.78,.225])):
   self.assertAlmostEqual(v(el(r,f'q-{i}'),'width',.9),94*q);self.assertAlmostEqual(v(el(r,f'u-{i}'),'width',.9),94*u);self.assertAlmostEqual(v(el(r,f'u-{i}'),'x',.9),385+94*q)
   self.assertEqual(v(el(r,f'u-{i}'),'opacity',.349),0);self.assertEqual(v(el(r,f'u-{i}'),'opacity',.35),1)
 def test_backup_arrival(self):
  r=root('value-backup')
  for i,t in enumerate([.3,.54,.78]):
   self.assertEqual(v(el(r,f'backup-label-{i}'),'opacity',t-1e-6),0);self.assertEqual(v(el(r,f'backup-label-{i}'),'opacity',t),1);self.assertAlmostEqual(v(el(r,f'backup-token-{i}'),'cx',t),[431,274,117][i])
  self.assertEqual(v(el(r,'root-update'),'opacity',.819),0);self.assertEqual(v(el(r,'root-update'),'opacity',.82),1)
 def test_terminal_before_labels(self):
  r=root('selfplay-labels');self.assertEqual(v(el(r,'terminal-result'),'opacity',.599),0)
  for i,t in enumerate([.9,.8,.7]):self.assertEqual(v(el(r,f'outcome-{i}'),'opacity',t-1e-6),0);self.assertEqual(v(el(r,f'outcome-{i}'),'opacity',t),1)
 def test_assets_and_bilingual(self):
  for p in A.glob('alphazero-*.svg'):
   r=E.parse(p).getroot()
   for e in r.iter(N+'text'):self.assertIn(e.get('text-anchor','start'),['start','middle','end'])
   for a in r.iter(N+'animate'):self.assertIn(a.get('begin','0s'),['0s']);self.assertEqual(a.get('dur'),'12s')
   if '-still' in p.name:self.assertFalse(r.findall('.//'+N+'animate'))
  for p in (R/'docs/theory/paradigms/reinforcement-learning/alphazero').glob('index*.md'):
   s=p.read_text();self.assertEqual(s.count('tabindex="0"'),4);self.assertEqual(s.count('data-source-asset-urls'),4)
 def test_actual_player(self):subprocess.run(['node','scripts/test_alphazero_player.cjs'],cwd=R,check=True)
if __name__=='__main__':unittest.main()
