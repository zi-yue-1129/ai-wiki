"""DPR scale and ColBERT exact MaxSim switch regression checks."""
from pathlib import Path
from xml.etree import ElementTree as E
import math,unittest
N='{http://www.w3.org/2000/svg}';A=Path(__file__).resolve().parents[1]/'docs/assets/concept-animations'
def root(stem,kind='motion'):return E.parse(A/f'{stem}-{kind}.svg').getroot()
def sample(e,attr,t):
 a=next((a for a in e if a.get('attributeName')==attr),None)
 if a is None:return float(e.get(attr))
 vs=list(map(float,a.get('values').split(';')));ts=list(map(float,a.get('keyTimes').split(';')))
 for i in range(len(ts)-1):
  if t<ts[i+1]:return vs[i] if a.get('calcMode')=='discrete' else vs[i]+(vs[i+1]-vs[i])*(t-ts[i])/(ts[i+1]-ts[i])
 return vs[-1]
def mat(t):return [[.88-.58*t,.22+.62*t,.12+.18*t],[.10+.12*t,.28+.52*t,.79-.40*t]]
class Retrieval(unittest.TestCase):
 def test_dpr_unit_query_and_score_scale(self):
  for kind in ['motion','still']:
   r=root('dpr-dot-product-sweep',kind);q=next(e for e in r.iter(N+'line') if e.get('stroke')=='#de8546');dot=next(e for e in r.iter(N+'circle') if e.get('fill')=='#de8546');bars=[e for e in r.iter(N+'rect') if e.get('x')=='398' and e.get('fill') in ['#087e99','#7565b9']]
   tracks=[e for e in r.iter(N+'rect') if e.get('fill')=='#eaf1f5'];self.assertEqual([float(e.get('width')) for e in tracks],[183,183])
   for i in range(1001 if kind=='motion' else 1):
    t=i/1000;a=math.radians(5+80*(1-abs(2*t-1)) if kind=='motion' else 62.6);x=(sample(q,'x2',t)-166)/96;y=(222-sample(q,'y2',t))/96
    self.assertAlmostEqual(x,math.cos(a),delta=.0001);self.assertAlmostEqual(y,math.sin(a),delta=.0001)
    self.assertAlmostEqual(sample(dot,'cx',t),sample(q,'x2',t));self.assertAlmostEqual(sample(dot,'cy',t),sample(q,'y2',t))
    self.assertAlmostEqual(sample(bars[0],'width',t)/183,x,delta=1e-7);self.assertAlmostEqual(sample(bars[1],'width',t)/183,y,delta=1e-7)
 def test_colbert_cells_argmax_and_sum(self):
  times=[i/1000 for i in range(1001)]+[x+d for x in [.55/2,1-.55/2,(.51/.92)/2,1-(.51/.92)/2] for d in [-1e-6,1e-6]]
  for kind in ['motion','still']:
   r=root('colbert-maxsim-switch',kind);cells=[e for e in r.iter(N+'rect') if e.get('fill-opacity')=='0.84'];outlines=[e for e in r.iter(N+'rect') if e.get('stroke')=='#f1a546'];maxbars=[e for e in r.iter(N+'rect') if e.get('x')=='466' and e.get('fill') in ['#087e99','#7565b9']];total=next(e for e in r.iter(N+'rect') if e.get('x')=='433' and e.get('fill')=='#de8546')
   for t in times if kind=='motion' else [0]:
    m=mat(1-abs(2*t-1) if kind=='motion' else .72)
    for row in range(2):
     for col in range(3):
      e=cells[3*row+col];h=sample(e,'height',t);self.assertAlmostEqual(h/36,m[row][col],delta=3e-8);self.assertAlmostEqual(sample(e,'y',t)+h,184+82*row,places=5)
     selected=round((sample(outlines[row],'x',t)-88)/79);self.assertAlmostEqual(m[row][selected],max(m[row]),delta=1e-9);self.assertAlmostEqual(sample(maxbars[row],'width',t)/128,max(m[row]),delta=1e-8)
    self.assertAlmostEqual(sample(total,'width',t)/80,sum(max(v) for v in m),delta=1e-8)
 def test_static(self):
  for stem in ['dpr-dot-product-sweep','colbert-maxsim-switch']:self.assertFalse(list(root(stem,'still').iter(N+'animate')))
if __name__=='__main__':unittest.main()
