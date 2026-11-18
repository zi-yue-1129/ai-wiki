"""Actual SVG causal snapshots and local readable source contracts."""
import bisect, unittest
from pathlib import Path
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1];ASSETS=ROOT/'docs/assets/concept-animations';NS='{http://www.w3.org/2000/svg}'
def read(stem,kind='motion'):return ET.parse(ASSETS/f'{stem}-{kind}.svg').getroot()
def at(e,attr,t):
 a=next((a for a in e.findall(NS+'animate') if a.get('attributeName')==attr),None)
 if a is None:return e.get(attr,'1' if attr=='opacity' else '0')
 v=a.get('values').split(';');k=list(map(float,a.get('keyTimes').split(';')));i=min(len(k)-1,max(0,bisect.bisect_right(k,t)-1))
 if a.get('calcMode')=='discrete' or i==len(k)-1:return v[i]
 q=(t-k[i])/(k[i+1]-k[i]);return str(float(v[i])*(1-q)+float(v[i+1])*q)
def visible_rects(e,t,parent=1):
 visible=parent*float(at(e,'opacity',t))
 if e.tag==NS+'rect' and visible>.5:yield e
 for child in e:yield from visible_rects(child,t,visible)
class EvolutionSvgTests(unittest.TestCase):
 def test_genome_inheritance_and_mutation_causality(self):
  r=read('genetic-crossover-mutation')
  def bits(t,x):
   cells={float(e.get('x')):e for e in visible_rects(r,t) if e.get('width')=='16' and e.get('y')=='134' and x<=float(e.get('x'))<x+152}
   return ''.join('1' if cells[k].get('fill')=='#2563a6' else '0' for k in sorted(cells))
  for t in [0,.2,.249]:self.assertEqual(bits(t,244),'');self.assertEqual(bits(t,447),'')
  for t in [.438,.499]:self.assertEqual(bits(t,244),'11010101');self.assertEqual(bits(t,447),'')
  self.assertEqual(bits(.6,447),'11010101')
  for t in [.65,.8,.999]:self.assertEqual(bits(t,447),'11010111')
  cursor=next(r.iter(NS+'circle'));self.assertEqual(at(cursor,'cx',.999),'593.0')
 def test_archive_update_on_arrival_not_in_transit(self):
  r=read('map-elites-archive');cells=[e for e in r.iter(NS+'rect') if e.get('width')=='44'];self.assertEqual(len(cells),24)
  dot=next(r.iter(NS+'circle'))
  for t,n in [(0,3),(.17999,3),(.18,4),(.43,4),(.68,4),(.90999,4),(.91,5),(.999,5)]:
   self.assertEqual(sum(at(c,'fill',t)!='#f2f6fa' for c in cells),n)
  target=next(e for e in cells if e.get('x')=='206' and e.get('y')=='146')
  self.assertEqual(at(target,'fill',.67999),'#53b6a9');self.assertEqual(at(target,'fill',.68),'#138e82')
  for t,x,y in [(.18,228,167),(.43,228,167),(.68,228,167),(.91,179,261)]:
   self.assertAlmostEqual(float(at(dot,'cx',t)),x);self.assertAlmostEqual(float(at(dot,'cy',t)),y);self.assertEqual(at(dot,'opacity',t),'0')
  outcomes=[e for e in r.iter(NS+'text') if e.text in ('ADD','REJECT','REPLACE')]
  for e,t in zip(outcomes,[.18,.43,.68,.91]):self.assertEqual(at(e,'opacity',t-.000001),'0');self.assertEqual(at(e,'opacity',t),'1')
 def test_local_scroll_and_bilingual_hooks(self):
  for topic in ['genetic-algorithms','map-elites']:
   for lang in ['', '.zh-TW']:
    s=(ROOT/f'docs/theory/paradigms/evolutionary/{topic}{lang}.md').read_text()
    for token in ['data-source-asset-urls','width:100%;overflow-x:auto','width:640px','tabindex="0"','data-evolution-lab=']:self.assertIn(token,s)
if __name__=='__main__':unittest.main()
