"""Independent arithmetic/geometry and dense actual-SMIL timeline regression; not a browser."""
from pathlib import Path
import math,re,unittest,xml.etree.ElementTree as E
from html.parser import HTMLParser
R=Path(__file__).resolve().parents[1];A=R/'docs/assets/concept-animations';N='{http://www.w3.org/2000/svg}';STEMS=['diffusion-policy-'+s for s in ['noise-training','denoising','receding-horizon','multimodal-actions']]
def root(s):return E.parse(A/(s+'-motion.svg')).getroot()
def nums(s):return list(map(float,re.findall(r'-?(?:\d+(?:\.\d*)?|\.\d+)',s)))
def value(e,attr,t):
 a=next((x for x in e if x.get('attributeName')==attr),None)
 if a is None:return nums(e.get(attr))
 ts=nums(a.get('keyTimes'));vs=a.get('values').split(';');i=max(i for i,k in enumerate(ts) if k<=t)
 if a.get('calcMode')=='discrete' or i==len(ts)-1:return nums(vs[i])
 u=(t-ts[i])/(ts[i+1]-ts[i]);return [x+(y-x)*u for x,y in zip(nums(vs[i]),nums(vs[i+1]))]
def bez(p,t):return tuple(sum((1-t)**3*p[k]+3*(1-t)**2*t*p[k+2]+3*(1-t)*t*t*p[k+4]+t**3*p[k+6] for _ in [0]) for k in [0,1])
def timeline_check(r):
 marker=r.find('.//*[@id="completed-action-marker"]');cells=[e for e in r.iter(N+'rect') if e.get('data-completion-index')]
 ends=[(row*4+.9+j*1.15)/12 for row in range(3) for j in range(3)]
 for t in [i/4000 for i in range(4000)]:
  n=sum(t>=k for k in ends);shown=sum(value(e,'opacity',t)[0] for e in cells)
  assert shown==n,(t,shown,n)
  # Compare independent completion count to both actual coordinate timelines.
  for attr in ['cx','cy']:
   ani=next(e for e in marker if e.get('attributeName')==attr);assert ani.get('calcMode')=='discrete';expected=nums(ani.get('values'))[n]
   assert abs(value(marker,attr,t)[0]-expected)<1e-9
LABEL_PANELS = {'denoising': ('DENOISER', '#EDF6F7'), 'noise-training': ('PREDICT NOISE', '#EAF5F4')}
def check_marker_label_paint(r, stem):
 label, panel = LABEL_PANELS[stem]
 text = next(e for e in r if e.tag == N+'text' and e.text == label)
 # A top-level label must paint after every moving marker group, not merely
 # after an unrelated path within that group. No claim of native pixel QA.
 children = list(r)
 groups = [g for g in r if g.get('class') == 'motion' and any(e.tag == N+'circle' for e in g.iter())]
 assert groups
 assert all(children.index(text) > children.index(g) for g in groups)
 # The panel-coloured outline isolates glyph edges from the coloured marker.
 assert text.get('stroke') == panel
 assert text.get('stroke-width') == '1.5'
 assert text.get('paint-order') == 'stroke fill'
 assert text.get('stroke-linejoin') == 'round'

class Semantics(unittest.TestCase):
 def test_marker_labels_paint_above_motion_with_panel_contrast(self):
  for stem in LABEL_PANELS:check_marker_label_paint(root('diffusion-policy-'+stem),stem)
 def test_negative_marker_group_repainted_above_label(self):
  for stem,(label,_) in LABEL_PANELS.items():
   r=root('diffusion-policy-'+stem);text=next(e for e in r if e.text==label)
   r.remove(text);r.insert(0,text)
   with self.assertRaises(AssertionError):check_marker_label_paint(r,stem)
 def test_negative_missing_label_contrast(self):
  for stem,(label,_) in LABEL_PANELS.items():
   for attr in ['stroke','stroke-width','paint-order','stroke-linejoin']:
    r=root('diffusion-policy-'+stem);text=next(e for e in r if e.text==label);text.attrib.pop(attr)
    with self.assertRaises(AssertionError):check_marker_label_paint(r,stem)

 def test_dense_horizon_causality(self):timeline_check(root(STEMS[2]))
 def test_negative_early_completion(self):
  r=root(STEMS[2]);e=next(e for e in r.iter(N+'rect') if e.get('data-completion-index')=='1');e.find(N+'animate').set('keyTimes','0;.001;1')
  with self.assertRaises(AssertionError):timeline_check(r)
 def test_marker_positions_lie_on_illustrative_curve(self):
  r=root(STEMS[2]);marker=r.find('.//*[@id="completed-action-marker"]');xs=nums(next(e for e in marker if e.get('attributeName')=='cx').get('values'));ys=nums(next(e for e in marker if e.get('attributeName')=='cy').get('values'))
  curve=[bez(p,i/4000) for p in [[65,157,165,102,242,168,332,135],[332,135,422,102,499,110,575,111]] for i in range(4001)]
  for pt in zip(xs,ys):self.assertLess(min(math.dist(pt,q) for q in curve),.1)
  self.assertEqual((xs[0],ys[0]),(65,157));self.assertEqual((xs[-1],ys[-1]),(575,111))
 def test_rows_share_action_axis(self):
  r=root(STEMS[2]);rows=[]
  for y in ['223','260','297']:
   es=[e for e in r.iter(N+'rect') if e.get('y')==y and e.get('fill')=='#DDE5ED'];rows.append([float(e.get('x')) for e in es]);self.assertEqual(len(es),8)
  self.assertEqual(rows,[[96+99*i+33*j for j in range(8)] for i in range(3)])
 def test_denoising_holds_never_reverses(self):
  r=root(STEMS[1]);e=r.find('.//*[@id="candidate"]');target=value(e,'d',.99);last=float('inf')
  for i in range(4001):
   t=i/4001;dist=sum((x-y)**2 for x,y in zip(value(e,'d',t),target));self.assertLessEqual(dist,last+1e-8);last=dist
  self.assertEqual(value(e,'d',.85),value(e,'d',.9999))
 def test_training_holds_and_is_explicitly_schematic(self):
  r=root(STEMS[0]);e=next(e for e in r.iter(N+'path') if e.find(N+'animate') is not None);base=value(e,'d',0);last=0
  for i in range(4001):
   dist=sum((x-y)**2 for x,y in zip(value(e,'d',i/4001),base));self.assertGreaterEqual(dist+1e-8,last);last=dist
  for lang in ['', '.zh-TW']:
   s=(R/f'docs/applications/robotics/diffusion-policy/index{lang}.md').read_text();self.assertIn('arxiv.org/abs/2303.04137v5',s);self.assertIn('\\sqrt{\\bar{\\alpha}_k}',s);self.assertIn('\\end{gathered}',s)
 def test_multimodal_mean_and_exact_dash_lengths(self):
  r=root(STEMS[3]);paths=list(r.iter(N+'path'));upper,lower,mean=[nums(e.get('d')) for e in paths[:3]]
  self.assertEqual(mean,[(x+y)/2 for x,y in zip(upper,lower)])
  # Both modes avoid the obstacle bounding box; the constructed mean enters its solid interior.
  for p in [upper,lower]:self.assertFalse(any(172<x<215 and 180<y<219 for x,y in [bez(p,i/5000) for i in range(5001)]))
  self.assertTrue(any(179<x<208 and 187<y<212 for x,y in [bez(mean,i/5000) for i in range(5001)]))
  for e in [e for e in paths if e.find(N+'animate') is not None]:
   p=nums(e.get('d'));ps=[bez(p,i/10000) for i in range(10001)];length=sum(math.dist(x,y) for x,y in zip(ps,ps[1:]));self.assertAlmostEqual(float(e.get('stroke-dasharray')),length,places=5)
   last=float('inf')
   for i in range(4001):
    offset=value(e,'stroke-dashoffset',i/4001)[0];self.assertLessEqual(offset,last+1e-8);last=offset
   self.assertEqual(value(e,'stroke-dashoffset',.999),[0])
 def test_all_bilingual_static_first_focusable_regions(self):
  class P(HTMLParser):
   def __init__(self):super().__init__();self.divs=[];self.images=[]
   def handle_starttag(self,t,a):
    a=dict(a)
    if t=='div':self.divs.append(a)
    if t=='img' and 'data-motion-src' in a:self.images.append((a,self.divs[-2:]))
  for lang in ['', '.zh-TW']:
   p=P();s=(R/f'docs/applications/robotics/diffusion-policy/index{lang}.md').read_text();p.feed(s);self.assertEqual(len(p.images),4);self.assertNotIn('\n$\n',s)
   for a,ds in p.images:
    self.assertTrue(a['src'].endswith('-still.svg'));self.assertIn('data-source-asset-urls',a);self.assertEqual(ds[0]['tabindex'],'0');self.assertEqual(ds[0]['role'],'region');self.assertIn('640px',ds[1]['style'])
 def test_static_assets_have_no_animation(self):
  for s in STEMS:
   r=E.parse(A/(s+'-still.svg')).getroot();self.assertFalse(any(e.tag.split('}')[-1].startswith('animate') for e in r.iter()))
if __name__=='__main__':unittest.main()
