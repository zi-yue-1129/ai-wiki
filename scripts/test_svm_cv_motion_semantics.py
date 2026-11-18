"""Check SVG coordinate coupling and independent held-out CV runs."""
import unittest
from pathlib import Path
from xml.etree import ElementTree as E
N='{http://www.w3.org/2000/svg}'
A=Path(__file__).resolve().parents[1]/'docs/assets/concept-animations'
def root(stem,kind='motion'):return E.parse(A/f'{stem}-{kind}.svg').getroot()
def sample(a,t):
 ts=list(map(float,a.get('keyTimes').split(';')));vs=list(map(float,a.get('values').split(';')))
 for i in range(len(ts)-1):
  if t<=ts[i+1]:return vs[i]+(vs[i+1]-vs[i])*(t-ts[i])/(ts[i+1]-ts[i])
 return vs[-1]
class Semantics(unittest.TestCase):
 def test_hinge_coordinate_coupling(self):
  r=root('svm-margin-hinge');a=list(r.iter(N+'animate'));self.assertEqual(len(a),3)
  for i in range(1001):
   t=i/1000;x=sample(a[0],t);margin=(x-164)/45
   self.assertAlmostEqual(sample(a[1],t),455+65*margin,places=5)
   self.assertAlmostEqual(sample(a[2],t),284-58*max(0,1-margin),places=5)
  for kind in ['motion','still']:
   r=root('svm-margin-hinge',kind);points=[c for c in r.iter(N+'circle') if c.get('fill')=='#e09d3a'];x=float(points[0].get('cx'));margin=(x-164)/45
   self.assertAlmostEqual(float(points[1].get('cx')),455+65*margin)
   self.assertAlmostEqual(float(points[1].get('cy')),284-58*max(0,1-margin))
 def test_cv_folds_scores_and_timing(self):
  scores=[.82,.85,.79,.88,.84];self.assertAlmostEqual(sum(scores)/5,.836)
  for kind in ['motion','still']:
   r=root('cv-fold-rotation',kind)
   for row in range(5):
    cells=[q for q in r.iter(N+'rect') if q.get('y')==str(106+41*row) and q.get('width')=='62']
    self.assertEqual(len(cells),5);self.assertEqual([i for i,c in enumerate(cells) if c.get('fill')=='#07998b'],[row])
    b=[q for q in r.iter(N+'rect') if q.get('x')=='479' and q.get('y')==str(115+41*row) and q.get('fill')=='#e09d3a'][0]
    if kind=='still':self.assertAlmostEqual(float(b.get('width')),90*scores[row])
    else:
     a=b.find(N+'animate');self.assertEqual(sample(a,row*.18),0);self.assertAlmostEqual(sample(a,row*.18+.14),90*scores[row]);self.assertAlmostEqual(sample(a,1),90*scores[row])
     cursor=[a for a in r.iter(N+'animate') if a.get('attributeName')=='y'][0]
     self.assertAlmostEqual(sample(cursor,row*.18+.08),102+41*row)
 def test_stills_static_and_duration(self):
  for stem in ['svm-margin-hinge','cv-fold-rotation']:
   self.assertFalse(list(root(stem,'still').iter(N+'animate')))
   for a in root(stem).iter(N+'animate'):self.assertEqual(a.get('dur'),'10s');self.assertEqual(a.get('repeatCount'),'indefinite')
if __name__=='__main__':unittest.main()
