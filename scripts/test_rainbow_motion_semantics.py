"""Independent arithmetic and actual SVG state/geometry invariants for Rainbow."""
import unittest,copy,math,hashlib
from pathlib import Path
from xml.etree import ElementTree as E
ROOT=Path(__file__).resolve().parents[1]; A=ROOT/'docs/assets/concept-animations';N='{http://www.w3.org/2000/svg}'
STEMS=['rainbow-c51-projection','rainbow-dueling-head','rainbow-nstep-returns','rainbow-noisynet-samples']
def root(s,k='motion'):return E.parse(A/f'{s}-{k}.svg').getroot()
def value(n,attr,t):
 a=next((a for a in n.findall(N+'animate') if a.get('attributeName')==attr),None)
 if a is None:return float(n.get(attr,'1' if attr=='opacity' else '0'))
 ts=list(map(float,a.get('keyTimes').split(';')));vs=list(map(float,a.get('values').split(';')))
 i=max(i for i,x in enumerate(ts) if x<=t)
 if a.get('calcMode')=='discrete' or i==len(ts)-1:return vs[i]
 return vs[i]+(vs[i+1]-vs[i])*(t-ts[i])/(ts[i+1]-ts[i])
def projection(z,p,reward,gamma):
 out=[0.]*len(z);step=z[1]-z[0]
 for x,m in zip(z,p):
  y=min(z[-1],max(z[0],reward+gamma*x));b=(y-z[0])/step;l=math.floor(b);u=math.ceil(b)
  if l==u:out[l]+=m
  else:out[l]+=m*(u-b);out[u]+=m*(b-l)
 return out

def check_bars(r,c51):
 bars=[n for n in r.iter(N+'rect') if n.find(N+'animate[@attributeName="height"]') is not None]
 nums=[n for n in r.iter(N+'text') if n.get('y')==('521' if c51 else '524')]
 target=projection([-10,-5,0,5,10],[.1,.2,.4,.2,.1],2,.5)[1:] if c51 else [3+a-1/3 for a in [2,0,-1]]
 scale=148 if c51 else 11.8;baseline=493 if c51 else 500;switch=.34 if c51 else .47
 assert len(bars)==len(target)
 for i in range(10001):
  t=i/10000
  for b,y in zip(bars,target):
   assert abs(value(b,'height',t)-(y*scale if t>=switch else 0))<1e-5
   assert abs(value(b,'y',t)+value(b,'height',t)-baseline)<1e-7
  assert all(value(n,'opacity',t)==int(t>=switch) for n in nums)
 if c51:
  assert [float(n.text) for n in nums]==[0,.08,.48,.4,.04]
 else:assert all(abs(float(n.text.split()[-1])-q)<.005 for n,q in zip(nums,target))

def check_nstep(r):
 groups=[n for n in r.iter(N+'g') if n.get('class')=='moving']
 boxes=[n for n in r.iter(N+'rect') if n.get('y')=='348']
 expected=[1,1+.9*2,1+.9*2-.9**2,1+.9*2-.9**2+.9**3*5]
 assert len(groups)==len(boxes)==4
 for g,v in zip(groups,expected):assert abs(float(g.find(N+'text').text)-v)<1e-10
 for i in range(10001):
  t=i/10000;stage=sum(t>=b for b in [.16,.32,.52,.72,.88])-1
  for j,(g,b) in enumerate(zip(groups,boxes)):
   assert value(b,'opacity',t)==int(j==stage)
   assert value(g,'opacity',t)==int(j==min(stage,3))

def check_shifted_labels(r):
 labels=[n for n in r.iter(N+'text') if n.get('x') in ['172','212','252','292','332'] and (n.text or '') in ['-3','-0.5','2','4.5','7']]
 assert len(labels)==5
 assert [n.text for n in labels]==['-3','-0.5','2','4.5','7']
 circles={n.get('cx'):n for n in r.iter(N+'circle') if n.get('cy')=='137'}
 for n in labels:
  # Conservative 15px Arial envelope: full em above baseline, 3px below.
  y=float(n.get('y')); c=circles[n.get('x')]
  assert n.get('font-size')=='15' and n.get('text-anchor')=='middle'
  assert y-15>=95  # below the subtitle's baseline92 +3px descent
  assert y+3+3 <= float(c.get('cy'))-float(c.get('r'))
  assert y+3+3 <= 150-1.5  # both projection curves start at150 and never rise

class RainbowTests(unittest.TestCase):
 def test_shifted_label_clearance(self):
  for kind in ['motion','still']:check_shifted_labels(root(STEMS[0],kind))
 def test_shifted_label_old_layout_rejected(self):
  for kind in ['motion','still']:
   for x in ['172','212','252','292','332']:
    r=root(STEMS[0],kind)
    next(n for n in r.iter(N+'text') if n.get('x')==x and n.get('y')=='115').set('y','173')
    with self.assertRaises(AssertionError):check_shifted_labels(r)
 def test_projection_product_body_preserved(self):
  expected={'motion': '430cf35bed6f9b03b84fca02ad880b655ee9775ccac8725c54c06d0a9dc0be7c', 'still': '3aadbe1f3052e3c4d3a68442124dd2af3e6e36e57bb6ceaa3786401c167a5e0b'}
  for kind,h in expected.items():
   s=(A/f'rainbow-c51-projection-{kind}.svg').read_text()
   self.assertEqual(s.count('y="115"'),5)
   self.assertEqual(hashlib.sha256(s.replace('y="115"','y="173"').encode()).hexdigest(),h)
 def test_projection_and_geometry(self):
  check_bars(root(STEMS[0]),True)
  for reward in [-100,-10,0,2,10,100]:
   p=projection([-10,-5,0,5,10],[.1,.2,.4,.2,.1],reward,.5);self.assertAlmostEqual(sum(p),1);self.assertTrue(all(x>=0 for x in p))
 def test_dueling(self):check_bars(root(STEMS[1]),False)
 def test_nstep(self):check_nstep(root(STEMS[2]))
 def test_noisy(self):
  for kind in ['motion','still']:
   r=root(STEMS[3],kind);bars=[x for x in r.iter(N+'rect') if x.get('x')=='72' and x.get('fill')!='#e8effa']
   self.assertEqual(len(bars),4)
   for b,v in zip(bars,[.7+.2,.6-.2,.7-.25,.6+.2]):self.assertAlmostEqual(float(b.get('width'))/255,v)
  r=root(STEMS[3]);boxes=[x for x in r.iter(N+'rect') if x.get('class')=='moving'];dots=list(r.iter(N+'circle'))
  for d,x in zip(dots,[72+255*.9,72+255*.8]):self.assertAlmostEqual(float(d.get('cx')),x)
  for i in range(1001):
   t=i/1000;expected=[int(.16<=t<.52),int(.52<=t<1)]
   self.assertEqual([value(x,'opacity',t) for x in boxes],expected);self.assertEqual([value(x,'opacity',t) for x in dots],expected)
 def test_negative_mutations(self):
  r=root(STEMS[0]);next(x for x in r.iter(N+'animate') if x.get('attributeName')=='height').set('values','0;22;22')
  with self.assertRaises(AssertionError):check_bars(r,True)
  r=root(STEMS[1]);next(x for x in r.iter(N+'animate') if x.get('attributeName')=='height').set('calcMode','linear')
  with self.assertRaises(AssertionError):check_bars(r,False)
  r=root(STEMS[2]);next(g for g in r.iter(N+'g') if any(x.text=='5.635' for x in g.findall(N+'text'))).find(N+'animate').set('values','0;0;0;0;1;0;0')
  with self.assertRaises(AssertionError):check_nstep(r)
 def test_bilingual_hooks(self):
  for p in (ROOT/'docs/theory/paradigms/reinforcement-learning/value-based-methods/rainbow').glob('index*.md'):
   s=p.read_text();self.assertEqual(s.count('class="concept-motion-scroll" tabindex="0"'),4);self.assertEqual(s.count('data-source-asset-urls'),4);self.assertEqual(s.count('min-width:640px'),4);self.assertIn('CC BY-SA 4.0',s)
if __name__=='__main__':unittest.main()
