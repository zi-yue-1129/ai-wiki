"""Check actual shipped Gaussian curves, ancestry, and all bilingual asset hooks."""
import math,re,unittest,xml.etree.ElementTree as ET
import subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'docs/assets/concept-animations';N='{http://www.w3.org/2000/svg}'
class BayesianSvgTests(unittest.TestCase):
 def test_gaussian_curve_endpoints(self):
  r=ET.parse(A/'kalman-gain-fusion-motion.svg').getroot();p=next(e for e in r.iter(N+'polyline') if e.find(N+'animate') is not None);a=p.find(N+'animate');values=a.get('values').split(';')
  for value,mean,var in [(values[0],3,1.44),(values[-1],3+1.44/2.08*4,1.44*.64/2.08)]:
   for pair in value.split():
    x,y=map(float,pair.split(','));state=(x-74)/50;expected=252-122*math.exp(-.5*(state-mean)**2/var);self.assertAlmostEqual(y,expected,delta=.16)
  self.assertEqual(values[-1],values[-2])
 def test_actual_ancestor_geometry(self):
  r=ET.parse(A/'particle-weight-resampling-motion.svg').getroot();cs=[e for e in r.iter(N+'circle') if e.find(N+'animate') is not None];self.assertEqual(len(cs),10)
  xs=[1,2.1,2.9,3.7,4.4,5.3,6.1,6.6,7.4,8.8];w=[math.exp(-.5*((x-6.6)/1.3)**2) for x in xs];total=sum(w);cdf=[];s=0
  for x in w:s+=x/total;cdf.append(s)
  for j,c in enumerate(cs):
   idx=next(i for i,f in enumerate(cdf) if f>.045+j/10);self.assertAlmostEqual(float(c.get('cx')),74+50*xs[idx]);an={a.get('attributeName'):a for a in c.findall(N+'animate')};self.assertEqual(an['cy'].get('values').split(';')[-2:],['302','302']);self.assertEqual(an['opacity'].get('calcMode'),'discrete');self.assertTrue(all(float(v) in [0,1] for v in an['opacity'].get('values').split(';')))
 def test_bilingual_hooks_and_shared_scope(self):
  for name in ['kalman','particle']:
   for lang in ['', '.zh-TW']:
    s=(ROOT/f'docs/theory/paradigms/probabilistic/graphical-models/{name}-filter{lang}.md').read_text();self.assertEqual(s.count('data-source-asset-urls'),6);self.assertIn('width:640px;min-width:640px',s);self.assertNotRegex(s,r'(?m)^\$$');self.assertNotIn('![' ,s)
 def test_shared_player_scope_behavior(self):
  player=(ROOT/'docs/javascripts/concept-motion.js').read_text()
  harness=r"""
const fs=require('fs'),vm=require('vm'),assert=require('assert/strict');
const src=fs.readFileSync(0,'utf8');
for(const stem of ['kalman-gain-fusion','particle-weight-resampling','unrelated-topic','paged-block-mapping','expert-cache-miss','strips-state-effects','graphplan-layer-extraction'])for(const reduced of [true,false]){
 class El{constructor(tag){this.tag=tag;this.attrs={};this.dataset={};this.children=[];this.events={};this.className='';this.classList={add:n=>this.className+=' '+n}}setAttribute(k,v){this.attrs[k]=v}getAttribute(k){return this.attrs[k]??null}append(x){this.children.push(x)}before(x){this.host=x}addEventListener(k,f){this.events[k]=f}}
 const img=new El('img'),inference=['paged-block-mapping','expert-cache-miss'].includes(stem),planning=['strips-state-effects','graphplan-layer-extraction'].includes(stem);
 img.attrs.src=`/assets/concept-animations/${stem}-${inference?'still':'motion'}.svg`;img.alt='Teaching diagram';
 const document={readyState:'complete',querySelectorAll:()=>[img],createElement:t=>new El(t)};
 vm.runInNewContext(src,{document,window:{matchMedia:()=>({matches:reduced,addEventListener(){}})}});
 assert.equal(img.dataset.conceptMotionEnhanced,'yes');
 assert.equal(img.host.tabIndex,inference||planning?0:undefined,stem+' host focus scope');
 assert.equal(img.host.attrs.role,inference||planning?'region':undefined,stem+' region scope');
 assert.equal(img.host.children.includes(img),true);
 assert.match(img.attrs.src,reduced?/-still\.svg$/:/-motion\.svg$/);
}
"""
  run=lambda source:subprocess.run(['node','-e',harness],input=source,text=True,capture_output=True,cwd=ROOT)
  result=run(player);self.assertEqual(result.returncode,0,result.stderr)
  # Mutation control: a real global host-focus assignment must fail the same behavior check.
  marker="host.className = 'concept-motion-player';"
  self.assertEqual(player.count(marker),1)
  bad=run(player.replace(marker,marker+' host.tabIndex = 0;'))
  self.assertNotEqual(bad.returncode,0);self.assertIn('host focus scope',bad.stderr)
if __name__=='__main__':unittest.main()
