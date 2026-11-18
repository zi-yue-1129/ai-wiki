"""Independent numerical and geometry checks for the two didactic examples."""
import math,re,unittest,xml.etree.ElementTree as E
from markdown import Markdown
from pathlib import Path
from tsne_motion_example import X,Y0,affinities,trajectory,loss,gradient
ROOT=Path(__file__).resolve().parents[1];NS={'s':'http://www.w3.org/2000/svg'}
def svg(stem,kind='motion'):return E.parse(ROOT/f'docs/assets/concept-animations/{stem}-{kind}.svg').getroot()
def vals(a):return list(map(float,a.get('values').split(';')))
def lerp(v,t):
 x=t*(len(v)-1);i=min(int(x),len(v)-2);return v[i]*(1-x+i)+v[i+1]*(x-i)
class Semantics(unittest.TestCase):
 def test_mobile_figures_preserve_readable_width_and_local_scroll(self):
  from html.parser import HTMLParser
  class Tags(HTMLParser):
   def __init__(self): super().__init__(); self.tags=[]
   def handle_starttag(self,tag,attrs): self.tags.append((tag,dict(attrs)))
  for name in ['t-sne','umap']:
   for lang in ['', '.zh-TW']:
    text=(ROOT/f'docs/theory/paradigms/unsupervised/dimensionality-reduction/{name}{lang}.md').read_text()
    parser=Tags();parser.feed(Markdown().convert(text))
    i=next(i for i,(tag,a) in enumerate(parser.tags) if tag=='img' and 'data-motion-src' in a)
    outer,inner,img=parser.tags[i-2:i+1]
    self.assertEqual((outer[0],inner[0],img[0]),('div','div','img'))
    self.assertEqual(outer[1]['tabindex'],'0');self.assertEqual(outer[1]['role'],'group')
    self.assertIn('overflow-x:auto',outer[1]['style']);self.assertIn('max-width:100%',outer[1]['style'])
    self.assertIn('min-width:640px',inner[1]['style'])
    for rule in ['width:640px','min-width:640px','max-width:none','height:auto']:
     self.assertIn(rule,img[1]['style'])
    self.assertIn('左右捲動' if lang else 'scroll horizontally',outer[1]['aria-label'])
    self.assertIn('左右方向鍵' if lang else 'Left and Right arrow keys',text)
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
 def test_coordinate_lists_are_display_matrices_with_unchanged_values(self):
  for lang in ['', '.zh-TW']:
   source=(ROOT/f'docs/theory/paradigms/unsupervised/dimensionality-reduction/t-sne{lang}.md').read_text()
   blocks=re.findall(r'^\$\$\n(.*?)\n\$\$$',source,re.M|re.S)
   for name,expected in [('X',X),('Y_0',Y0)]:
    matches=[b for b in blocks if b.startswith(name+'=')]
    self.assertEqual(len(matches),1)
    block=matches[0]
    matrix=block.split(r'\begin{pmatrix}')[1].split(r'\end{pmatrix}')[0]
    rows=[tuple(float(x.strip()) for x in row.split('&')) for row in matrix.strip().split(r'\\')]
    self.assertEqual(tuple(rows),expected)
    html=Markdown(extensions=['pymdownx.arithmatex'],extension_configs={'pymdownx.arithmatex':{'generic':True}}).convert('$$\n'+block+'\n$$')
    self.assertIn('<div class="arithmatex">',html)
    self.assertNotIn('<span class="arithmatex">',html)
 def test_static_and_language_hooks(self):
  for topic,stem in [('t-sne','tsne-kl-embedding'),('umap','umap-fuzzy-union')]:
   self.assertFalse(svg(stem,'still').findall('.//s:animate',NS))
   for lang in ['', '.zh-TW']:
    s=(ROOT/f'docs/theory/paradigms/unsupervised/dimensionality-reduction/{topic}{lang}.md').read_text();self.assertIn('data-source-asset-urls',s);self.assertIn(f'{stem}-still.svg',s)
if __name__=='__main__':unittest.main()
