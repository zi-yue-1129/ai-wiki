"""Independent numerical and geometry checks for the two didactic examples."""
import math,unittest,xml.etree.ElementTree as E
from pathlib import Path
from tsne_motion_example import affinities,trajectory,loss,gradient
ROOT=Path(__file__).resolve().parents[1];NS={'s':'http://www.w3.org/2000/svg'}
def svg(stem,kind='motion'):return E.parse(ROOT/f'docs/assets/concept-animations/{stem}-{kind}.svg').getroot()
def vals(a):return list(map(float,a.get('values').split(';')))
def lerp(v,t):
 x=t*(len(v)-1);i=min(int(x),len(v)-2);return v[i]*(1-x+i)+v[i+1]*(x-i)
class Semantics(unittest.TestCase):
 def test_affinities_and_gradient_by_finite_differences(self):
  p,ys=trajectory();self.assertAlmostEqual(sum(map(sum,p)),1)
  for i in range(6):
   self.assertEqual(p[i][i],0)
   for j in range(6):self.assertEqual(p[i][j],p[j][i])
  for y in [ys[0],ys[1],ys[60],ys[-1]]:
   g=gradient(p,y)
   for i in range(6):
    for d in range(2):
     a=[x[:] for x in y];b=[x[:] for x in y];a[i][d]+=1e-5;b[i][d]-=1e-5
     self.assertAlmostEqual(g[i][d],(loss(p,a)-loss(p,b))/2e-5,places=7)
  self.assertAlmostEqual(loss(p,ys[0]),1.0523044235012489)
  self.assertAlmostEqual(loss(p,ys[-1]),.042910145319812215)
 def test_svg_retains_every_actual_update_and_loss_at_samples(self):
  p,ys=trajectory();r=svg('tsne-kl-embedding');circles=r.findall(".//s:g[@class='moving']/s:circle",NS)
  axes=[[vals(a) for a in c.findall('s:animate',NS)] for c in circles];self.assertEqual(len(axes),6)
  for j in range(6):
   for d in range(2):
    self.assertEqual(len(axes[j][d]),121)
    for k,y in enumerate(ys):self.assertAlmostEqual(axes[j][d][k],[446,184][d]+40*y[j][d],delta=.000051)
  bar=vals(r.find(".//s:animate[@attributeName='width']",NS));self.assertEqual(len(bar),601)
  for k,width in enumerate(bar):
   t=k/600;y=[[(lerp(axes[j][d],t)-[446,184][d])/40 for d in range(2)] for j in range(6)]
   self.assertAlmostEqual(width/266*loss(p,ys[0]),loss(p,y),delta=3e-6)
 def test_umap_union_scale_and_one_way_guides(self):
  for kind in ['motion','still']:
   r=svg('umap-fuzzy-union',kind)
   edges=[e for e in r.findall('.//s:line',NS) if e.get('x1')=='409']
   for e in edges:
    a,b=(.35,.7) if e.get('y1')=='125' else (.2,.5)
    self.assertAlmostEqual(float(e.get('stroke-width')),10*(a+b-a*b));self.assertFalse(list(e))
   for c in r.findall('.//s:circle',NS):
    for a in c.findall('s:animate',NS):
     v=vals(a);self.assertEqual(len(v),2)
     self.assertEqual(v,[94,230] if c.get('cy') in ['113','226'] else [230,94])
 def test_static_and_language_hooks(self):
  for topic,stem in [('t-sne','tsne-kl-embedding'),('umap','umap-fuzzy-union')]:
   self.assertFalse(svg(stem,'still').findall('.//s:animate',NS))
   for lang in ['', '.zh-TW']:
    s=(ROOT/f'docs/theory/paradigms/unsupervised/dimensionality-reduction/{topic}{lang}.md').read_text();self.assertIn('data-source-asset-urls',s);self.assertIn(f'{stem}-still.svg',s)
if __name__=='__main__':unittest.main()
