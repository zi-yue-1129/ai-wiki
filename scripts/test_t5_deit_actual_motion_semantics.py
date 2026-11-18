"""Actual T5 reveal and DeiT forward-flow ordering."""
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
class T5DeitSvgTests(unittest.TestCase):
 def test_t5_target_order_and_final_hold(self):
  r=read('t5-span-corruption');groups=r.findall(NS+'g');self.assertEqual([g.find(NS+'text').text for g in groups],['S0','B','C','S1','H','I','S2'])
  for i in range(1001):
   t=i/1000;op=[at(g.findall(NS+'rect')[-1],'opacity',t) for g in groups];self.assertEqual(op,sorted(op));
   if t<.45:self.assertEqual(op,[1]*7)
   if t>.77:self.assertEqual(op,[0]*7)
  circles=r.findall(NS+'circle');ends=[float(c.find(NS+'animateMotion').get('keyTimes').split(';')[2]) for c in circles];self.assertLess(ends[0],.28);self.assertLess(ends[1],.45)
 def test_deit_causal_routes_synchronized(self):
  r=read('deit-dual-head-distillation');circles=r.findall(NS+'circle');intervals=[]
  for c in circles:
   a=c.find(NS+'animateMotion');self.assertEqual(a.get('begin'),'0s');self.assertEqual(a.get('dur'),'12s');k=list(map(float,a.get('keyTimes').split(';')));intervals.append(k[1:3]);self.assertEqual(at(c,'opacity',0),0);self.assertEqual(at(c,'opacity',.999),0)
  self.assertLessEqual(intervals[0][1],intervals[1][0]);self.assertLessEqual(intervals[4][1],intervals[3][0]);self.assertLessEqual(intervals[3][1],intervals[6][0]);self.assertLessEqual(intervals[2][1],intervals[6][0]);self.assertLessEqual(intervals[1][1],intervals[5][0])
 def test_source_scopes(self):
  for stem in ['architecture-families/t5','vision-transformer/deit']:
   for lang in ['', '.zh-TW']:
    s=(ROOT/f'docs/theory/models/transformer/{stem}/index{lang}.md').read_text()
    for token in ['data-source-asset-urls','data-still-src','overflow-x:auto','width:640px','tabindex="0"','t5-deit-lab']:self.assertIn(token,s)
if __name__=='__main__':unittest.main()
