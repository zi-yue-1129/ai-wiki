"""Actual EWC endpoint geometry and NEAT enabled/disabled ledger timelines."""
import bisect,math,unittest
from pathlib import Path
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1];ASSETS=ROOT/'docs/assets/concept-animations';NS='{http://www.w3.org/2000/svg}'
def read(stem,kind='motion'):return ET.parse(ASSETS/f'{stem}-{kind}.svg').getroot()
def at(e,attr,t):
 a=next((a for a in e.findall(NS+'animate') if a.get('attributeName')==attr),None)
 if a is None:return float(e.get(attr,'1' if attr=='opacity' else '0'))
 v=list(map(float,a.get('values').split(';')));k=list(map(float,a.get('keyTimes').split(';'))) if a.get('keyTimes') else [i/(len(v)-1) for i in range(len(v))];i=min(len(k)-1,max(0,bisect.bisect_right(k,t)-1))
 if a.get('calcMode')=='discrete' or i==len(k)-1:return v[i]
 q=(t-k[i])/(k[i+1]-k[i]);return v[i]*(1-q)+v[i+1]*q
class EwcNeatSvgTests(unittest.TestCase):
 def test_ewc_coordinate_geometry(self):
  r=read('ewc-fisher-springs');cs=[c for c in r.findall(NS+'circle') if c.find(NS+'animate') is not None];ls=[e for e in r.findall(NS+'line') if e.find(NS+'animate') is not None]
  for i in range(1001):
   t=i/1000
   for j,theta in enumerate([.2,.8]):
    expected=140+400*theta*min(t/.38,1);self.assertAlmostEqual(at(cs[j],'cx',t),expected);self.assertAlmostEqual(at(ls[j],'x2',t),expected)
  for s in [4,.25]:
   x=0
   for k in range(19):
    self.assertAlmostEqual(x,(1-(1-.024*(1+s))**k)/(1+s));x-=.024*((x-1)+s*x)
 def test_neat_discrete_genes_and_route(self):
  r=read('neat-add-node-innovation');gs=r.findall(NS+'g');marker=next(c for c in r.findall(NS+'circle') if c.find(NS+'animate') is not None)
  for i in range(1001):
   t=i/1000;op=[at(g,'opacity',t) for g in gs];self.assertTrue(all(v in [0,1] for v in op));self.assertEqual(op[0]+op[1],1);self.assertEqual(op[0],op[3]);self.assertEqual(op[1],op[4]);self.assertEqual(op[2],op[5]);self.assertFalse(op[0] and op[2]);
   if at(marker,'opacity',t)>0:self.assertEqual(op[2],1)
  self.assertEqual([at(g,'opacity',.999) for g in gs],[0,1,1,0,1,1])
 def test_bilingual_local_source_hooks(self):
  for stem in ['theory/paradigms/continual/regularisation-based/ewc','theory/paradigms/evolutionary/neat']:
   for lang in ['', '.zh-TW']:
    s=(ROOT/f'docs/{stem}{lang}.md').read_text()
    for token in ['data-source-asset-urls','data-still-src','width:640px','overflow-x:auto','tabindex="0"','data-ewc-neat-lab']:self.assertIn(token,s)
if __name__=='__main__':unittest.main()
