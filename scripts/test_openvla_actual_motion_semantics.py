"""Source-geometry checks; distinguish paper-style bins from released tokenizer edges."""
from pathlib import Path
import unittest,xml.etree.ElementTree as ET,math
import numpy as np
R=Path(__file__).resolve().parents[1];A=R/'docs/assets/concept-animations';N='{http://www.w3.org/2000/svg}'
STEMS=['openvla-dual-encoder-fusion','openvla-percentile-action-bins']
def sample(a,t):
 v=list(map(float,a.get('values').split(';')));k=list(map(float,a.get('keyTimes').split(';')))
 for i in range(len(k)-1):
  if t<k[i+1]:return v[i] if a.get('calcMode')=='discrete' else v[i]+(v[i+1]-v[i])*(t-k[i])/(k[i+1]-k[i])
 return v[-1]
def root(stem,kind='motion'):return ET.parse(A/f'{stem}-{kind}.svg').getroot()
def anim(el,name):return el.find(N+f"animate[@attributeName='{name}']")
class OpenVLAMotion(unittest.TestCase):
 def test_paper_toy_vs_official_index_convention(self):
  a=np.array([-1.4,.4,1.6]);clip=np.clip(a,-1,1);toy=np.minimum(255,np.floor(256*(clip+1)/2)).astype(int)
  np.testing.assert_array_equal(toy,[0,179,255]);edges=np.linspace(-1,1,256);idx=np.digitize(clip,edges)
  np.testing.assert_array_equal(idx,[1,179,256]);np.testing.assert_array_equal(idx-1,[0,178,255])
  centres=(edges[:-1]+edges[1:])/2;decoded=centres[np.clip(idx-1,0,254)];self.assertAlmostEqual(decoded[1],.4);self.assertEqual(centres[np.clip(255,0,254)],centres[254])
 def test_fusion_input_follows_actual_paths(self):
  cs=root(STEMS[0]).find(N+"g[@class='motion-overlay']").findall(N+'circle')
  for c,end in [(cs[0],145),(cs[2],243)]:
   for i in range(251):
    t=i/1000;x=sample(anim(c,'cx'),t);y=sample(anim(c,'cy'),t)
    if t<=.06:self.assertAlmostEqual(y,197)
    elif t<=.18:self.assertAlmostEqual(x,160)
    else:self.assertAlmostEqual(y,end)
   self.assertEqual(sample(anim(c,'cx'),.25),176)
 def test_fusion_temporal_dependencies(self):
  g=root(STEMS[0]).find(N+"g[@class='motion-overlay']");cs=g.findall(N+'circle')
  for c in [cs[1],cs[3]]:
   self.assertEqual(sample(anim(c,'opacity'),.25),0);self.assertEqual(sample(anim(c,'cx'),.30),284);self.assertEqual(sample(anim(c,'cx'),.45),320)
  for e in g.findall(N+'rect'):
   self.assertEqual(sample(anim(e,'opacity'),.45),0);self.assertEqual(sample(anim(e,'x'),.65),401)
  self.assertEqual(sample(anim(cs[4],'opacity'),.65),0);self.assertEqual(sample(anim(cs[4],'cx'),.90),548)
  for e in g:self.assertEqual(sample(anim(e,'opacity'),.97),0)
 def test_scalar_geometry_and_discrete_highlights(self):
  r=root(STEMS[1]);base=r.findall(N+'circle');self.assertEqual(len(base),3)
  for c,a in zip(base,[-1.4,.4,1.6]):self.assertAlmostEqual(float(c.get('cx')),143+176*(a+1))
  g=r.find(N+"g[@class='motion-overlay']");h=g.find(N+'rect');self.assertEqual(anim(h,'x').get('calcMode'),'discrete')
  for t,b in [(.25,0),(.50,179),(.80,255)]:self.assertAlmostEqual(sample(anim(h,'x'),t)+1.5,143+(b+.5)*352/256)
  for i in range(1001):self.assertIn(sample(anim(h,'x'),i/1000),[142.1875,388.3125,492.8125])
  for c,t,target in zip(g.findall(N+'circle'),[.24,.48,.75],[143,389.4,495]):self.assertAlmostEqual(sample(anim(c,'cx'),t),target)
 def test_static_reduced_and_source_math_scope(self):
  for stem in STEMS:
   self.assertFalse(root(stem,'still').findall('.//'+N+'animate'));css=root(stem).find(N+'style').text;self.assertIn('.motion-overlay{display:none!important}',css);self.assertIn('.static-overlay{display:inline!important}',css)
  for lang in ['', '.zh-TW']:
   s=(R/f'docs/applications/robotics/openvla/index{lang}.md').read_text()
   self.assertEqual(s.count('class="openvla-source-scroll" tabindex="0" role="region"'),2)
   for stem in STEMS:self.assertIn(f'{stem}-still.svg" data-motion-src=',s)
   for text in ['[0, 178, 255]','action_tokenizer.py','data_utils.py','linspace(-1, 1, 256)']:self.assertIn(text,s)
class NumpyRuntimeDependency(unittest.TestCase):
 def test_exact_pinned_install_precedes_unchanged_source_test(self):
  import re
  workflow=(R/'.github/workflows/concept-animation-validation.yml').read_text()
  def verify(text):
   step=re.search(r'^      - name: Validate OpenVLA source geometry and player\n        run: \|\n((?:          .*\n)+)',text,re.M)
   assert step
   assert [line.strip()for line in step[1].splitlines()]==['python -m pip install "numpy==2.5.5"','python scripts/test_openvla_actual_motion_semantics.py','node scripts/test_openvla_source_player.cjs']
  verify(workflow)
  for install in ('','# python -m pip install "numpy==2.5.5"','python -m pip install "numpy==2.5.5" || true','python -m pip install numpy'):
   with self.assertRaises(AssertionError):verify(workflow.replace('python -m pip install "numpy==2.5.5"',install))
  with self.assertRaises(AssertionError):verify(workflow.replace('      - name: Validate OpenVLA source geometry and player\n','      - name: Validate OpenVLA source geometry and player\n        if: false\n'))
 def test_original_numeric_module_fails_without_numpy(self):
  import subprocess,sys
  program=r'''
import sys,importlib.abc
sys.path.insert(0,sys.argv[1])
class NoNumpy(importlib.abc.MetaPathFinder):
 def find_spec(self,fullname,path=None,target=None):
  if fullname=='numpy' or fullname.startswith('numpy.'):
   raise ModuleNotFoundError("No module named 'numpy' (intentional dependency negative)")
sys.meta_path.insert(0,NoNumpy())
import test_openvla_actual_motion_semantics
'''
  result=subprocess.run([sys.executable,'-I','-c',program,str(R/'scripts')],text=True,capture_output=True)
  self.assertNotEqual(result.returncode,0)
  self.assertIn("No module named 'numpy' (intentional dependency negative)",result.stderr)

if __name__=='__main__':unittest.main()
