"""Exact toy interpolation, bounding-box rule, and animation causality."""
from pathlib import Path
import unittest,xml.etree.ElementTree as E,subprocess,json,math
P=Path(__file__).resolve().parents[1];N='{http://www.w3.org/2000/svg}'
def sample(a,t):
 ts=list(map(float,a.get('keyTimes').split(';')));vs=list(map(float,a.get('values').split(';')));i=max(i for i,x in enumerate(ts[:-1]) if x<=t)
 return vs[i] if a.get('calcMode')=='discrete' else vs[i]+(vs[i+1]-vs[i])*(t-ts[i])/(ts[i+1]-ts[i])
class SegmentationSemantics(unittest.TestCase):
 def test_roi_shared_geometry_and_scale(self):
  r=E.parse(P/'docs/assets/concept-animations/roi-align-sampling-motion.svg').getroot()
  target=next(e.find(N+'animate') for e in r.iter(N+'circle') if e.get('r')=='11')
  snap=next(e.find(N+'animate') for e in r.iter(N+'circle') if e.get('r')=='7.5')
  bars=[e.find(N+'animate') for e in r.iter(N+'rect') if e.get('y')=='372' and e.get('fill')=='#0f9689']
  for i in range(10000):
   t=i/10000;x=sample(target,t);self.assertAlmostEqual(x,185.5+40*min(t/.8,1))
   self.assertEqual(sample(snap,t),185.5 if x<205.5 else 225.5)
   self.assertEqual(sample(bars[0],t),68 if x<205.5 else 118)
   self.assertAlmostEqual(sample(bars[1],t),68+50*(x-185.5)/40)
 def test_sam_valid_attributes_and_simultaneous_box_selection(self):
  r=E.parse(P/'docs/assets/concept-animations/sam-prompt-ambiguity-motion.svg').getroot()
  for a in r.iter(N+'animate'):self.assertEqual(len(a.get('values').split(';')),len(a.get('keyTimes').split(';')))
  box=next(e.find(N+'animate') for e in r.iter(N+'g') if e.get('opacity')=='0')
  whole=next(e.find(N+'animate') for e in r.iter(N+'rect') if e.get('x')=='436' and e.get('stroke')=='#e5813b')
  masks=[e.find(N+'animate') for e in r.iter(N+'rect') if e.get('x')=='436' and e.get('fill')=='#ffffff']
  for i in range(10000):
   t=i/10000;on=int(t>=.55);self.assertEqual(sample(box,t),on);self.assertEqual(sample(whole,t),on)
   for a in masks:self.assertEqual(sample(a,t),.86*on)
 def test_live_js_helpers_all_grid_samples_and_masks(self):
  src=(P/'docs/javascripts/segmentation-labs.js').read_text()
  code="global.window={};global.document={readyState:'complete',querySelectorAll:()=>[]};"+src+";const m=window.SegmentationTeachingMath;console.log(JSON.stringify({grid:m.grid,r:Array.from({length:29},(_,i)=>(i+1)/10).flatMap(x=>Array.from({length:29},(_,i)=>(i+1)/10).map(y=>m.roiState(x,y))),b:[0,1,2].map(i=>m.maskBox(i)),s:[0,1,2].flatMap(i=>[false,true].flatMap(b=>[0,1,2,3].map(t=>[i,b,t,m.samMatches(i,b,t)])))}));"
  d=json.loads(subprocess.check_output(['node','-e',code],text=True));grid=d['grid']
  for r in d['r']:
   x,y=r['x'],r['y'];x0,y0=math.floor(x),math.floor(y);u,v=x-x0,y-y0
   expected=(1-v)*((1-u)*grid[y0][x0]+u*grid[y0][x0+1])+v*((1-u)*grid[y0+1][x0]+u*grid[y0+1][x0+1])
   self.assertAlmostEqual(r['bi'],expected,places=14);self.assertAlmostEqual(sum(c[2] for c in r['corners']),1)
   self.assertEqual(r['near'],grid[math.floor(y+.5)][math.floor(x+.5)])
  self.assertEqual(d['b'],[[0,0,8,8],[1,1,7,7],[2,2,6,6]])
  for i,b,t,matches in d['s']:self.assertEqual(matches,[i] if b and t>=2 else [0,1,2])
 def test_source_hooks_and_fallbacks(self):
  for topic in ['mask-r-cnn','segment-anything']:
   for suffix in ['', '.zh-TW']:
    s=(P/f'docs/theory/models/computer-vision/segmentation/{topic}{suffix}.md').read_text()
    for token in ['data-source-asset-urls','concept-motion-scroll','tabindex="0"','width:800px','data-still-src']:self.assertIn(token,s)
if __name__=='__main__':unittest.main()
