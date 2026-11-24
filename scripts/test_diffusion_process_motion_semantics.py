"""Independent numerical contracts for deterministic diffusion teaching visuals."""
import unittest,math,json,subprocess,xml.etree.ElementTree as E
from pathlib import Path
P=Path(__file__).resolve().parents[1];N='{http://www.w3.org/2000/svg}'
def sample(a,t):
 ts=list(map(float,a.get('keyTimes').split(';')));vs=list(map(float,a.get('values').split(';')));i=max(i for i,x in enumerate(ts[:-1]) if x<=t)
 return vs[i] if a.get('calcMode')=='discrete' else vs[i]+(vs[i+1]-vs[i])*(t-ts[i])/(ts[i+1]-ts[i])
class DiffusionSemantics(unittest.TestCase):
 def test_no_early_decoding(self):
  r=E.parse(P/'docs/assets/concept-animations/latent-space-denoise-motion.svg').getroot();a=next(a for a in r.iter(N+'animate') if a.get('attributeName')=='opacity')
  for i in range(10000):self.assertEqual(sample(a,i/10000),int(i/10000>=.8))
  for a in r.iter(N+'animate'):
   if a.get('attributeName')=='fill':self.assertEqual(a.get('keyTimes'),'0;0.08;0.8;1')
 def test_all_video_frames_share_noise_clock(self):
  r=E.parse(P/'docs/assets/concept-animations/video-joint-denoising-motion.svg').getroot()
  tiles=[e for e in r.iter(N+'rect') if e.get('width')=='27'];self.assertEqual(len(tiles),100)
  for e in tiles:
   a=e.find(N+'animate');self.assertEqual(a.get('keyTimes'),'0;.12;.84;1');self.assertEqual(a.get('values').split(';')[-1],'0.07')
  labels=[e.text for e in r.iter(N+'text')];self.assertTrue(all(f'frame index = {i}' in labels for i in range(1,5)))
 def test_actual_js_rms_compression_decode_and_mse(self):
  src=(P/'docs/javascripts/diffusion-process-labs.js').read_text()
  code="global.window={};global.document={readyState:'complete',querySelectorAll:()=>[]};"+src+";const m=window.DiffusionTeachingMath;console.log(JSON.stringify({noise:m.videoNoise,source:m.source,v:m.alphas.map((_,i)=>m.videoRender({},i,m.translations.en,{})),z:[1,2,4,8].map(f=>[f,m.compress(f),m.decode(m.compress(f),f),Array.from({length:9},(_,i)=>m.latentRender({},i,f,m.translations.en,{}))])}));"
  d=json.loads(subprocess.check_output(['node','-e',code],text=True));power=sum(v*v for f in d['noise'] for v in f)/384
  for r in d['v']:self.assertAlmostEqual(r['rms'],math.sqrt((1-r['a'])*power),places=14)
  self.assertEqual(d['v'][-1]['rms'],0)
  source=d['source']
  for f,z,decoded,steps in d['z']:
   expected=[sum(source[(y+dy)*16+x+dx] for dy in range(f) for dx in range(f))/(f*f) for y in range(0,16,f) for x in range(0,16,f)]
   self.assertEqual(len(z),256//(f*f))
   for a,b in zip(z,expected):self.assertAlmostEqual(a,b,places=14)
   for i,a in enumerate(decoded):self.assertAlmostEqual(a,expected[(i//16//f)*(16//f)+(i%16//f)],places=14)
   for r in steps[:-1]:self.assertIsNone(r['mse'])
   self.assertAlmostEqual(steps[-1]['mse'],sum((a-b)**2 for a,b in zip(source,decoded))/256,places=14)
 def test_scoped_layout_and_bilingual_source(self):
  css=(P/'docs/stylesheets/concept-motion.css').read_text();self.assertNotIn('.concept-motion-scroll img,',css);self.assertIn('.diffusion-motion-scroll img,',css)
  for topic in ['theory/models/computer-vision/video/video-diffusion','theory/paradigms/unsupervised/density-and-generative-models/diffusion/latent-diffusion']:
   for suffix in ['', '.zh-TW']:
    s=(P/f'docs/{topic}{suffix}.md').read_text()
    for token in ['data-source-asset-urls','concept-motion-scroll diffusion-motion-scroll','tabindex="0"','data-still-src']:self.assertIn(token,s)
if __name__=='__main__':unittest.main()
