"""Actual SVG score widths, staged ranking and whole-field autoregression."""
from pathlib import Path
import unittest,xml.etree.ElementTree as ET,copy
R=Path(__file__).resolve().parents[1];A=R/'docs/assets/concept-animations';N='{http://www.w3.org/2000/svg}'
STEMS=['saycan-skill-grounding','rt2-action-token-decoding'];SCORES=[[.8,.2,.16],[.45,.5,.225],[.55,.85,.4675]]
def root(stem,kind='motion'):return ET.parse(A/f'{stem}-{kind}.svg').getroot()
def sample(a,t):
 v=list(map(float,a.get('values').split(';')));k=list(map(float,a.get('keyTimes').split(';')))
 for i in range(len(k)-1):
  if t<k[i+1]:return v[i] if a.get('calcMode')=='discrete' else v[i]+(v[i+1]-v[i])*(t-k[i])/(k[i+1]-k[i])
 return v[-1]
def assert_score_geometry(r):
 for el in r.iter(N+'rect'):
  if el.get('fill') not in ['#087f82','#c46a2b','#6857a5']:continue
  row=[149,227,305].index(int(el.get('y')));col=[221,352,482].index(int(el.get('x')));a=el.find(N+'animate');width=sample(a,.9) if a is not None else float(el.get('width'))
  assert abs(width/96-SCORES[row][col])<1e-12,(row,col,width)
class GroundedAction(unittest.TestCase):
 def test_scores_and_negative_mutation(self):
  for s in SCORES:self.assertAlmostEqual(s[0]*s[1],s[2])
  self.assertEqual(max(range(3),key=lambda i:SCORES[i][0]),0);self.assertEqual(max(range(3),key=lambda i:SCORES[i][2]),2)
  for kind in ['motion','still']:assert_score_geometry(root(STEMS[0],kind))
  bad=root(STEMS[0]);a=next(e for e in bad.iter(N+'animate') if e.get('attributeName')=='width');a.set('values','0;0;99;99;99;0')
  with self.assertRaises(AssertionError):assert_score_geometry(bad)
 def test_score_reveal_and_selection_order(self):
  r=root(STEMS[0]);labels=[e for e in r.findall(N+'text') if e.get('class')=='score-label'];self.assertEqual(len(labels),9)
  for e in labels:
   start={'269':.07,'400':.34,'530':.62}[e.get('x')];a=e.find(N+'animate');self.assertEqual(sample(a,start-.001),0);self.assertEqual(sample(a,start),1)
  select=next(g for g in r.findall(N+'g') if g.find(N+'animate') is not None).find(N+'animate');self.assertEqual(sample(select,.62),0);self.assertEqual(sample(select,.8),1)
 def test_rt2_whole_fields_and_no_premature_command(self):
  r=root(STEMS[1]);self.assertEqual(r.find(N+"path[@id='camera-to-vlm']").get('d'),'M199 154 L205 154 L205 174 L359 174 L359 141 L374 141');a=r.find('.//'+N+'clipPath/'+N+'rect/'+N+'animate');self.assertEqual(a.get('calcMode'),'discrete')
  expected=[0,67,141,215,289,363,437,511,585]
  for i in range(1001):self.assertIn(sample(a,i/1000),expected)
  for i in range(8):self.assertEqual(sample(a,.201+.08*i),expected[i+1])
  g=next(g for g in r.findall(N+'g') if g.find(N+'animate') is not None);out=g.find(N+'animate')
  self.assertEqual(sample(out,.76),0);self.assertEqual(sample(out,.82),0);self.assertEqual(sample(out,.9),1)
  texts=[t.text for t in r.find(N+"g[@clip-path='url(#token-window)']").findall(N+'text')];self.assertEqual(texts,['0','128','178','84','128','128','130','220'])
 def test_rt2_negative_partial_window(self):
  a=root(STEMS[1]).find('.//'+N+'clipPath/'+N+'rect/'+N+'animate');a.set('calcMode','linear');self.assertNotIn(sample(a,.10),[0,67,141,215,289,363,437,511,585])
 def test_bilingual_source_scope_and_reduced(self):
  for stem,topic in zip(STEMS,['saycan','rt-2']):
   self.assertFalse(root(stem,'still').findall('.//'+N+'animate'));self.assertIn('prefers-reduced-motion',root(stem).find(N+'style').text)
   for lang in ['', '.zh-TW']:
    s=(R/f'docs/applications/robotics/{topic}/index{lang}.md').read_text();self.assertIn('class="grounded-action-source-scroll" tabindex="0" role="region"',s);self.assertIn('data-source-asset-urls',s);self.assertIn(stem+'-still.svg" data-motion-src=',s)
    self.assertIn('VLA',s)
if __name__=='__main__':unittest.main()
