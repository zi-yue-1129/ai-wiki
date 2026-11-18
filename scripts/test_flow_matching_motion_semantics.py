"""Independent interpolation/Bezier checks; toy paths are not learned ODE samples."""
from pathlib import Path
import unittest,re,xml.etree.ElementTree as E
N='{http://www.w3.org/2000/svg}';A=Path(__file__).resolve().parents[1]/'docs/assets/concept-animations'
def root(stem,kind='motion'):return E.parse(A/f'{stem}-{kind}.svg').getroot()
def point(poly,t):
 ps=list(poly)
 while len(ps)>1:ps=[tuple((1-t)*a+t*b for a,b in zip(p,q)) for p,q in zip(ps,ps[1:])]
 return ps[0]
class Flow(unittest.TestCase):
 def test_cfm_cursor_and_constant_velocity(self):
  r=root('cfm-conditional-bridge');markers=[e for e in r.iter(N+'circle') if e.get('class')=='moving']
  for circle,(x0,x1) in zip(markers,[(2.05,2.30),(1.29,.72),(.33,1.59)]):
   anims={a.get('attributeName'):a for a in circle};self.assertEqual(set(anims),{'cx','cy'})
   for k in range(1001):
    t=k/1000;xs=list(map(float,anims['cx'].get('values').split(';')));ys=list(map(float,anims['cy'].get('values').split(';')))
    self.assertAlmostEqual(xs[0]*(1-t)+xs[1]*t,90+385*t)
    self.assertAlmostEqual((350-(ys[0]*(1-t)+ys[1]*t))/100,(1-t)*x0+t*x1)
   for a in anims.values():self.assertEqual(a.get('keyTimes'),'0;1');self.assertEqual(a.get('dur'),'9s')
  for a in r.iter(N+'animate'):
   if a.get('attributeName') in ['x1','x2']:self.assertEqual(a.get('values'),'90;475');self.assertEqual(a.get('keyTimes'),'0;1')
 def test_cfm_still_at_shared_time(self):
  r=root('cfm-conditional-bridge','still');cs=[e for e in r.iter(N+'circle') if e.get('r')=='10']
  for e,(a,b) in zip(cs,[(145,120),(221,278),(317,191)]):
   self.assertAlmostEqual(float(e.get('cx')),90+385*.575,delta=.0051);self.assertAlmostEqual(float(e.get('cy')),a+(.575)*(b-a),delta=.0051)
 def test_reflow_exact_time_coordinates_and_midpoint(self):
  curves=[[(66,190),(135,100),(243,256),(330,173)],[(66,295),(139,222),(244,357),(330,280)]]
  r=root('rectified-reflow-coupling');cs=[e for e in r.iter(N+'circle') if e.get('class')=='moving']
  for i,e in enumerate(cs):
   p=curves[i//2]
   for j,a in enumerate(e):
    vals=list(map(float,a.get('values').split(';')));ts=list(map(float,a.get('keyTimes').split(';')));self.assertEqual(len(vals),201)
    for t,v in zip(ts,vals):
     expected=point(p,t)[j] if i%2==0 else (1-t)*p[0][j]+t*p[-1][j]+(366 if j==0 else 0)
     self.assertAlmostEqual(v,expected,delta=.00000051)
    for k in range(1000):
     t=k/1000;seg=min(int(t*200),199);f=t*200-seg;rendered=vals[seg]*(1-f)+vals[seg+1]*f
     expected=point(p,t)[j] if e in cs[::2] else (1-t)*p[0][j]+t*p[-1][j]+(366 if j==0 else 0)
     self.assertAlmostEqual(rendered,expected,delta=.005)
  for kind in ['motion','still']:
   rr=root('rectified-reflow-coupling',kind);rest=[e for e in rr.iter(N+'circle') if e.get('class')=='rest'] if kind=='motion' else [e for e in rr.iter(N+'circle') if e.get('r')=='10']
   self.assertEqual(len(rest),4)
   for i,e in enumerate(rest):
    p=curves[i//2];expected=point(p,.5) if i%2==0 else ((p[0][0]+p[-1][0])/2+366,(p[0][1]+p[-1][1])/2)
    self.assertAlmostEqual(float(e.get('cx')),expected[0]);self.assertAlmostEqual(float(e.get('cy')),expected[1])
 def test_bilingual_source_hooks_and_time_caveats(self):
  d=A.parents[1]/'theory/paradigms/unsupervised/density-and-generative-models/flow/flow-matching'
  for topic in ['conditional-flow-matching','rectified-flow']:
   for suffix in ['', '.zh-TW']:
    s=(d/f'{topic}{suffix}.md').read_text();self.assertIn('<img data-source-asset-urls',s);self.assertIn('data-still-src=',s);self.assertIn('tabindex="0"',s);self.assertIn('$t=0.5',s)
 def test_long_equations_use_bilingual_display_blocks(self):
  d=A.parents[1]/'theory/paradigms/unsupervised/density-and-generative-models/flow/flow-matching'
  for topic in ['conditional-flow-matching','rectified-flow']:
   texts=[(d/f'{topic}{suffix}.md').read_text() for suffix in ['', '.zh-TW']]
   for s in texts:
    inline=re.findall(r'\\\((.*?)\\\)',s)
    self.assertFalse(any(len(x)>55 for x in inline))
    self.assertFalse(any('RectFlow' in x or '\\mathbb E' in x for x in inline))
   normalize=lambda s: re.sub(r'\s+','',s)
   self.assertEqual([normalize(x) for x in re.findall(r'\$\$(.*?)\$\$',texts[0],re.S)], [normalize(x) for x in re.findall(r'\$\$(.*?)\$\$',texts[1],re.S)])
if __name__=='__main__':unittest.main()
