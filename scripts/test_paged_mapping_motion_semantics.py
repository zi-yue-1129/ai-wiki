import bisect,re,subprocess,unittest,xml.etree.ElementTree as E
from pathlib import Path
R=Path(__file__).resolve().parents[1];N='{http://www.w3.org/2000/svg}'
def val(a,t):
 k=list(map(float,a.get('keyTimes').split(';')));v=list(map(float,a.get('values').split(';')));i=min(bisect.bisect_right(k,t)-1,len(k)-2)
 if a.get('calcMode')=='discrete':return v[i] if t<1 else v[-1]
 f=(t-k[i])/(k[i+1]-k[i]);return v[i]*(1-f)+v[i+1]*f
class Paged(unittest.TestCase):
 def test_actual_mapping_geometry_tokens_and_visibility(self):
  for kind in ['motion','still']:
   r=E.parse(R/f'docs/assets/concept-animations/paged-block-mapping-{kind}.svg').getroot();groups={}
   for g in r.findall(N+'g'):
    texts=[t.text for t in g.findall(N+'text')]
    if texts:groups[texts[0]]=(g,texts)
   for logical,physical,tokens in [('L0','P2','0 1'),('L1','P0','2 3'),('L2','P3','4 5')]:
    self.assertEqual(groups[logical][1][1],tokens);self.assertEqual(groups[physical][1][1],tokens)
   self.assertEqual(groups['P1'][1][1],'free');self.assertIsNone(groups['P1'][0].find(N+'animate'))
   paths=[g.find(N+'path') for g in r.findall(N+'g') if g.find(N+'path') is not None];self.assertEqual(len(paths),3)
   for j,(l,p) in enumerate([('L0','P2'),('L1','P0'),('L2','P3')]):
    nums=list(map(float,re.findall(r'-?\d+(?:\.\d+)?',paths[j].get('d'))));lr=groups[l][0].find(N+'rect');pr=groups[p][0].find(N+'rect')
    self.assertEqual(nums[:2],[float(lr.get('x'))+38,143]);self.assertEqual(nums[-2:],[float(pr.get('x'))+38,230])
   if kind=='still':continue
   particles=r.findall("./"+N+"circle[@class='particle']");self.assertEqual(len(particles),3)
   for i in range(10001):
    t=i/10000
    for j,(l,p) in enumerate([('L0','P2'),('L1','P0'),('L2','P3')]):
     def opacity(g):
      a=g.find(N+'animate');return val(a,t) if a is not None else float(g.get('opacity','1'))
     self.assertEqual(opacity(groups[l][0]),opacity(groups[p][0]));expected=1 if t>=j*.25 and (j==0 or t<1) else 0
     self.assertEqual(opacity(groups[l][0]),expected)
     particle=particles[j];a=particle.find(N+'animate');motion=particle.find(N+'animateMotion');self.assertEqual(motion.get('path'),paths[j].get('d'))
     if val(a,t)>0:self.assertEqual(opacity(groups[l][0]),1)
 def test_player_scope_and_source_registration(self):
  subprocess.run(['node','scripts/test_inference_player.cjs'],cwd=R,check=True)
  css=(R/'docs/stylesheets/concept-motion.css').read_text();self.assertIn('.concept-motion-player.concept-motion-inference img',css);self.assertIn('min-width:640px',css)
  for name in ['paged-attention','expert-offloading']:
   for suffix in ['', '.zh-TW']:
    s=(R/f'docs/engineering/inference-optimization/{name}{suffix}.md').read_text();self.assertIn('<img data-source-asset-urls',s);self.assertIn('data-motion-src=',s);self.assertIn('data-still-src=',s)
if __name__=='__main__':unittest.main()
