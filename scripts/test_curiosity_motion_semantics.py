"""Curiosity actual-SMIL geometry, counterfactual transitions, and actual lab JS."""
import unittest,math,copy,re,subprocess,xml.etree.ElementTree as E
from pathlib import Path
from curiosity_svg_math import N,value
R=Path(__file__).resolve().parents[1];A=R/'docs/assets/concept-animations'
def root(s):return E.parse(A/(s+'-motion.svg')).getroot()
def ident(r,i):return r.find(".//*[@id='"+i+"']")
def circle(r,x,y,moving=False):return next(e for e in r.iter(N+'circle')if e.get('cx')==str(x)and e.get('cy')==str(y)and(not moving or e.find(N+'animate')is not None))
def check_novelty(r,mobile):
 tx,ty,px,py,scale=(291,379,72,496,240)if mobile else(589,145,470,235,390);target=circle(r,tx,ty,True);pred=circle(r,px,py,True);bar=next(e for e in r.iter(N+'rect')if e.get('class')=='animated'and e.get('width')==str(scale));base=(tx-px)**2+(ty-py)**2
 for t in [i/4000 for i in range(4000)]+[.711,.7115,.711999999,.712,.712000001]:
  want=(tx,ty)if t<.712 else((230,467)if mobile else(550,202));assert (value(target,'cx',t),value(target,'cy',t))==want
  err=((value(target,'cx',t)-value(pred,'cx',t))**2+(value(target,'cy',t)-value(pred,'cy',t))**2)*scale/base
  assert abs(value(bar,'width',t)-err)<.08,(t,value(bar,'width',t),err)
def check_predictor_clearance(r):
 # Conservative Arial 16px label envelope, independently checked with real
 # Inkscape glyph bounds. Include descenders and all SMIL interpolated bars.
 labels=[e for e in r.iter(N+'text') if e.text=='Predictor']
 assert len(labels)==1
 label=labels[0]; x=float(label.get('x')); y=float(label.get('y'))
 assert label.get('class')=='small' and label.get('text-anchor')=='middle'
 assert re.search(r'\.small\s*\{[^}]*font-size:16px',r.find(N+'style').text)
 assert y-16>=194, 'label must remain inside predictor panel'
 bars=[e for g in r.iter(N+'g') if g.get('fill')=='#d27b3f' for e in g if e.tag==N+'rect']
 assert len(bars)==(8 if any(g.get('class')=='resting' for g in r.iter(N+'g')) else 4)
 for bar in bars:
  bx=float(bar.get('x'));bw=float(bar.get('width'))
  for j in range(4001):
   t=j/4001;by=value(bar,'y',t)
   if bx<x+45 and bx+bw>x-45:
    assert by-(y+4)>=3, ('Predictor glyph/bar clearance',t,by,y)
class Tests(unittest.TestCase):
 def test_predictor_label_clearance_motion_and_still(self):
  for mode in ('motion','still'):
   check_predictor_clearance(E.parse(A/('rnd-prediction-error-'+mode+'.svg')).getroot())
 def test_predictor_original_overlap_is_rejected(self):
  for mode in ('motion','still'):
   r=E.parse(A/('rnd-prediction-error-'+mode+'.svg')).getroot()
   next(e for e in r.iter(N+'text') if e.text=='Predictor').set('y','225')
   with self.assertRaises(AssertionError):check_predictor_clearance(r)

 def test_novelty_desktop(self):check_novelty(root('rnd-state-novelty'),False)
 def test_novelty_mobile(self):check_novelty(root('rnd-state-novelty-mobile'),True)
 def test_mobile_line_attached(self):
  r=root('rnd-state-novelty-mobile');line=next(e for e in r.iter(N+'line')if e.find(N+'animate')is not None);cs=[e for e in r.iter(N+'circle')if any(a.get('attributeName')=='cx' for a in e)]
  for t in [j/4000 for j in range(4000)]+[.7115,.712,.9995]:
   for k,c in [('x1',cs[0]),('y1',cs[0]),('x2',cs[1]),('y2',cs[1])]:self.assertAlmostEqual(value(line,k,t),value(c,'cx'if k[0]=='x'else'cy',t))
 def test_negative_invented_observation(self):
  r=root('rnd-state-novelty');a=circle(r,589,145,True).find(N+'animate');a.set('keyTimes',a.get('keyTimes').replace('0.712;0.712','0.711;0.712'))
  with self.assertRaises(AssertionError):check_novelty(r,False)
 def test_negative_wrong_bonus(self):
  r=root('rnd-state-novelty');a=next(e for e in r.iter(N+'rect')if e.get('class')=='animated').find(N+'animate');a.set('values',';'.join(str(float(v)*.8)for v in a.get('values').split(';')))
  with self.assertRaises(AssertionError):check_novelty(r,False)
 def test_primary_squared_bars(self):
  for stem,tx,ty,px,py,scale in [('rnd-prediction-error',581,138,479,233,406),('icm-forward-inverse',604,143,550,229,132)]:
   r=root(stem);pred=circle(r,px,py,True);bar=next(e for e in r.iter(N+'rect')if e.get('class')=='animated');base=(tx-px)**2+(ty-py)**2
   for j in range(2000):
    t=j/2000;expected=scale*((tx-value(pred,'cx',t))**2+(ty-value(pred,'cy',t))**2)/base;self.assertLess(abs(value(bar,'width',t)-expected),.04)
 def test_return_scale(self):
  r=root('rnd-return-scale');bar=next(e for e in r.iter(N+'rect')if e.get('x')=='38'and e.get('y')=='339'and e.get('fill')=='#168a7d')
  for j in range(1000):
   t=j/1000;sd=1 if t<.32 else 2 if t<.65 else 4;self.assertAlmostEqual(value(bar,'width',t),60*4/sd)
 def test_weighted_gradient(self):
  r=root('icm-loss-blend');lines=[e for e in r.iter(N+'line')if e.get('stroke')in ['#8564b4','#d5893e','#168a7d']and e.find(N+'animate')is not None];inv,fwd,mix=lines
  for j in range(1000):
   t=j/1000;b=0 if t<.34 else .5 if t<.67 else 1
   self.assertAlmostEqual(value(mix,'x2',t),188+(1-b)*95+b*(-60));self.assertAlmostEqual(value(mix,'y2',t),253+(1-b)*(-30)+b*(-88));self.assertAlmostEqual(value(inv,'x2',t),value(fwd,'x1',t))
 def test_weighted_outcomes(self):
  r=root('icm-weighted-outcomes');points=[(365,101),(310,174),(255,115)]
  for j in range(1000):
   t=j/1000;s=-60+240*t if t<=.5 else 180-240*t;ps=[(100+s)/300,1/3,(100-s)/300];mx=sum(p*x for p,(x,y)in zip(ps,points));my=sum(p*y for p,(x,y)in zip(ps,points));var=sum(p*((x-mx)**2+(y-my)**2)for p,(x,y)in zip(ps,points))
   for i,p in enumerate(ps):self.assertLess(abs(value(ident(r,'icm-weight-'+str(i+1)),'width',t)-352*p),.02)
   self.assertLess(abs(value(ident(r,'icm-weighted-mean'),'cx',t)-(70+1.9*(mx-245))),.02);self.assertLess(abs(value(ident(r,'icm-weighted-variance'),'width',t)-326*var/4000),.2)
 def test_all_assets_and_hooks(self):
  files=[p for p in A.glob('*.svg')if p.name.startswith(('rnd-','icm-'))];self.assertEqual(len(files),42)
  for p in files:
   r=E.parse(p).getroot();self.assertIsNotNone(r.find(N+'title'));self.assertIsNotNone(r.find(N+'desc'));self.assertLess(p.stat().st_size,51200)
   for e in r.iter():
    self.assertNotIn(e.tag.split('}')[-1],['script','foreignObject','image'])
    if e.tag in [N+'animate',N+'animateMotion']:
     self.assertNotIn('-still',p.name);self.assertEqual(e.get('repeatCount'),'indefinite');self.assertIn(e.get('begin','0s'),['0s'])
     ts=list(map(float,e.get('keyTimes').split(';')));self.assertEqual(ts,sorted(ts));self.assertEqual(ts[0],0);self.assertEqual(ts[-1],1)
  for kind in ['rnd','icm']:
   for loc in ['', '.zh-TW']:
    s=(R/f'docs/theory/paradigms/reinforcement-learning/exploration/{kind}/index{loc}.md').read_text();imgs=re.findall(r'<img\b[^>]*data-motion-src[^>]*>',s)
    self.assertTrue(imgs);self.assertEqual(s.count('tabindex="0"'),len(imgs));self.assertTrue(all('data-source-asset-urls'in x for x in imgs))
 def test_sampling_band_actual_geometry(self):
  losses=[3.866,1.936,3.250];mean=sum(losses)/3;sd=math.sqrt(sum((x-mean)**2 for x in losses)/3)
  for suffix,count in [('motion',2),('still',1)]:
   r=E.parse(A/('icm-sampling-frequency-'+suffix+'.svg')).getroot();bands=[e for e in r.iter(N+'polygon')if 'data-analytic-se-band'in e.attrib];self.assertEqual(len(bands),count)
   for band in bands:
    points=[tuple(map(float,p.split(',')))for p in band.get('points').split()];self.assertEqual(len(points),40)
    for n in range(1,21):
     x=62+(n-1)*316/19
     for i,y in [(n-1,381-(mean+sd/math.sqrt(n)-2)*52),(40-n,381-(mean-sd/math.sqrt(n)-2)*52)]:self.assertLess(math.dist(points[i],(x,y)),.03)
 def test_normalisation_and_math_markup(self):
  for loc in ['','.zh-TW']:
   rnd=(R/f'docs/theory/paradigms/reinforcement-learning/exploration/rnd/index{loc}.md').read_text();icm=(R/f'docs/theory/paradigms/reinforcement-learning/exploration/icm/index{loc}.md').read_text()
   self.assertIn('fixed observation-normalisation statistics'if not loc else '觀測正規化統計量也固定',rnd)
   self.assertNotIn('(p(a_t=',icm);self.assertNotIn('(ln 2)',icm)
 def test_actual_js(self):
  for script in ['scripts/test_curiosity_math.cjs','scripts/test_curiosity_player.cjs']:subprocess.run(['node',script],cwd=R,check=True)
if __name__=='__main__':unittest.main()
