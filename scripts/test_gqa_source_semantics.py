"""Verify authored grouping, separate K/V arithmetic and conversion phase order."""
import unittest,re,bisect,xml.etree.ElementTree as E
from pathlib import Path
from verify_concept_motion import verify_source_pair
R=Path(__file__).resolve().parents[1];A=R/'docs/assets/concept-animations';N='{http://www.w3.org/2000/svg}'
def value(a,t):
 v=list(map(float,a.get('values').split(';')));ts=list(map(float,a.get('keyTimes').split(';')));i=min(len(v)-2,max(0,bisect.bisect_right(ts,t)-1));return v[i] if a.get('calcMode')=='discrete' else v[i]+(v[i+1]-v[i])*(t-ts[i])/(ts[i+1]-ts[i])
class GQA(unittest.TestCase):
 def test_grouping_paths(self):
  r=E.parse(A/'gqa-head-sharing-motion.svg').getroot();motion=list(r.iter(N+'animateMotion'));self.assertEqual(len(motion),8)
  for i,a in enumerate(motion):
   n=list(map(float,re.findall(r'[\d.]+',a.get('path'))));self.assertEqual(n[-2:], [205.,218.] if i<4 else [436.,218.]);self.assertEqual(n[1],134)
  # Timed group emphasis: not pooled queries or an execution order requirement.
  gs=[e for e in r.iter(N+'g') if e.find(N+'animate') is not None];self.assertEqual(len(gs),2);self.assertGreater(value(gs[0].find(N+'animate'),.2),.9);self.assertEqual(value(gs[1].find(N+'animate'),.2),0);self.assertGreater(value(gs[1].find(N+'animate'),.7),.9)
 def test_separate_projection_means(self):
  for kind in ['motion','still']:
   r=E.parse(A/f'gqa-uptraining-pooling-{kind}.svg').getroot();text=[e.text for e in r.iter(N+'text')];K=[.2,.6,.3,.7];V=[.8,.4,.5,.9]
   for g in range(2):
    k=sum(K[2*g:2*g+2])/2;v=sum(V[2*g:2*g+2])/2;label=f'K {k:.1f} / V {v:.1f}'.replace('0.','.');self.assertIn(label,text)
 def test_pool_before_uptraining(self):
  r=E.parse(A/'gqa-uptraining-pooling-motion.svg').getroot();c=[e for e in r.iter(N+'circle') if e.find(N+'animate') is not None];self.assertEqual(len(c),7)
  self.assertEqual(value(c[-1].find(N+'animate'),.5),0);self.assertGreater(value(c[-1].find(N+'animate'),.75),0)
  for e in c[:4]:self.assertGreater(value(e.find(N+'animate'),.25),.9);self.assertEqual(value(e.find(N+'animate'),.7),0)
  for e in c[4:6]:self.assertEqual(value(e.find(N+'animate'),.25),0);self.assertGreater(value(e.find(N+'animate'),.5),.9)
 def test_sources_and_safe_motion(self):
  for stem in ['gqa-head-sharing','gqa-uptraining-pooling']:
   for suffix in ['.md','.zh-TW.md']:
    p=R/f'docs/engineering/inference-optimization/grouped-query-attention{suffix}';self.assertEqual(verify_source_pair(p,p.read_text(),stem),[]);self.assertIn('tabindex="0"',p.read_text())
   for kind in ['motion','still']:
    r=E.parse(A/f'{stem}-{kind}.svg').getroot();self.assertEqual(r.get('viewBox'),'0 0 640 360')
    for e in r.iter():
     if e.find(N+'animateMotion') is not None:self.assertEqual(float(e.get('cx',0))+float(e.get('cy',0)),0)
    self.assertEqual(bool(list(r.iter(N+'animateMotion'))),kind=='motion')
class NativeFixtureContract(unittest.TestCase):
 def test_fixture_matches_actual_source_asset_paths_and_old_path_is_rejected(self):
  import ast
  from html.parser import HTMLParser
  class Images(HTMLParser):
   def __init__(self,html):super().__init__();self.images=[];self.feed(html)
   def handle_starttag(self,tag,attrs):
    if tag=='img':self.images.append(dict(attrs))
  def check(source):
   tree=ast.parse(source)
   calls=[n for n in ast.walk(tree)if isinstance(n,ast.Call)and isinstance(n.func,ast.Attribute)]
   htmlarg=next(n.args[0]for n in calls if n.func.attr=='set_content')
   route=next(n.args[0].value for n in calls if n.func.attr=='route')
   assert route=='**/assets/concept-animations/*.svg'
   for stem in ['gqa-head-sharing','gqa-uptraining-pooling']:
    html=eval(compile(ast.Expression(htmlarg),'<actual native fixture>','eval'),{'css':'','stem':stem,'alt':'test','size':640})
    image=Images(html).images[0]
    assert image['src']==f'https://wiki.example/assets/concept-animations/{stem}-still.svg'
    assert image['data-motion-src']==f'https://wiki.example/assets/concept-animations/{stem}-motion.svg'
    for suffix in ('.md','.zh-TW.md'):
     doc=(R/f'docs/engineering/inference-optimization/grouped-query-attention{suffix}').read_text()
     assert any(i.get('src','').endswith('assets/concept-animations/'+stem+'-still.svg')for i in Images(doc).images)
  source=(R/'scripts/test_gqa_source_browser.py').read_text();check(source)
  for bad in (source.replace('https://wiki.example/assets/concept-animations/','https://wiki.example/assets/'),source.replace('**/assets/concept-animations/*.svg','**/assets/*.svg')):
   with self.assertRaises(AssertionError):check(bad)
 def test_real_producer_failure_records_diagnostics_and_reraises(self):
  import tempfile,json
  from unittest.mock import MagicMock,patch
  import test_gqa_source_browser as b
  manager=MagicMock();browser=manager.__enter__.return_value.chromium.launch.return_value;page=browser.new_page.return_value
  page.evaluate.side_effect=[320,{'readyState':'complete','eligible':0,'buttons':0}]
  page.locator.return_value.count.return_value=0;page.content.return_value='<html>old fixture diagnostic</html>'
  with tempfile.TemporaryDirectory()as directory,patch.object(b,'OUT',Path(directory)),patch.object(b,'sync_playwright',return_value=manager):
   with self.assertRaises(AssertionError):b.main()
   report=json.loads((Path(directory)/'report.json').read_text())
   self.assertEqual(report['status'],'failed');self.assertEqual(report['cases'][0]['status'],'failed')
   self.assertEqual(report['cases'][0]['dom']['eligible'],0)
   self.assertTrue(list(Path(directory).glob('*-failure.html')));page.screenshot.assert_called_once();page.close.assert_called_once()
 def test_actual_js_selector_rejects_original_fixture(self):
  import subprocess
  result=subprocess.run(['node','scripts/test_gqa_player.cjs'],cwd=R,capture_output=True,text=True)
  self.assertEqual(result.returncode,0,result.stderr)
  self.assertIn('8 wrong-path selector negatives plus 8 actual GQA player',result.stdout)

 def test_future_only_changed_test_files_reach_native_and_semantic_steps(self):
  import yaml,fnmatch,copy
  w=yaml.safe_load((R/'.github/workflows/concept-animation-validation.yml').read_text())
  paths=['scripts/test_gradient_source_player.cjs', 'scripts/test_diffusion_schedule_player.cjs', 'scripts/test_diffusion_player.cjs', 'scripts/test_inference_player.cjs', 'scripts/test_motor_player.cjs', 'scripts/test_navigation_player.cjs', 'scripts/test_reviewed_scroll_player.cjs', 'scripts/concept_motion_fixture_selector.cjs', 'scripts/test_concept_motion_fixture_selector.cjs', 'scripts/test_gqa_source_browser.py', 'scripts/test_gqa_player.cjs', 'scripts/test_gqa_source_semantics.py', 'scripts/test_diffusion_policy_player.cjs', 'scripts/test_act_source_player.cjs', 'scripts/test_federated_source_player.cjs', 'scripts/test_grounded_action_source_player.cjs', 'scripts/test_openvla_source_player.cjs', 'scripts/test_distillation_player.cjs', 'scripts/test_sac_source_player.cjs', 'scripts/test_marl_source_player.cjs', 'scripts/test_population_source_player.cjs']
  commands=['node scripts/test_concept_motion_fixture_selector.cjs','python scripts/test_gqa_source_browser.py','node scripts/test_gqa_player.cjs','python -m unittest discover -s scripts -p "test_gqa_source_semantics.py"']
  def verify(w):
   patterns=w.get('on',w.get(True))['pull_request']['paths']
   assert all(any(fnmatch.fnmatchcase(p,g)for g in patterns)for p in paths)
   job=w['jobs']['validate-motion'];assert 'if' not in job
   runs=[]
   for step in job['steps']:
    if 'if' not in step and (step.get('continue-on-error') is None or step.get('continue-on-error') is False):runs.extend(line.strip()for line in step.get('run','').splitlines())
   assert all(c in runs for c in commands)
  verify(w)
  for path in paths:
   bad=copy.deepcopy(w);bad.get('on',bad.get(True))['pull_request']['paths'].remove(path)
   with self.assertRaises(AssertionError):verify(bad)
  for condition in (False,None,'always()'):
   bad=copy.deepcopy(w)
   for step in bad['jobs']['validate-motion']['steps']:
    if 'python scripts/test_gqa_source_browser.py' in step.get('run',''):step['if']=condition
   with self.assertRaises(AssertionError):verify(bad)

 def test_replacing_selector_filter_with_always_return_images_is_rejected(self):
  import subprocess
  program="const h=require.resolve('./scripts/concept_motion_fixture_selector.cjs');require(h);require.cache[h].exports=(selector,images)=>images;require('./scripts/test_gqa_player.cjs');"
  result=subprocess.run(['node','-e',program],cwd=R,capture_output=True,text=True)
  self.assertNotEqual(result.returncode,0)
  self.assertIn('AssertionError',result.stderr)

 def test_shared_helper_cannot_drop_existing_eighth_mock_scope(self):
  import json,re
  required={'test_act_source_player.cjs', 'test_inference_player.cjs', 'test_distillation_player.cjs', 'test_marl_source_player.cjs', 'test_diffusion_policy_player.cjs', 'test_diffusion_schedule_player.cjs', 'test_navigation_player.cjs', 'test_diffusion_player.cjs', 'test_federated_source_player.cjs', 'test_sac_source_player.cjs', 'test_openvla_source_player.cjs', 'test_reviewed_scroll_player.cjs', 'test_grounded_action_source_player.cjs', 'test_motor_player.cjs', 'test_gradient_source_player.cjs', 'test_population_source_player.cjs', 'test_gqa_player.cjs'}
  text=(R/'scripts/test_concept_motion_fixture_selector.cjs').read_text()
  def verify(source):
   match=re.search(r'^const requiredPlayers=(\[.*\]);$',source,re.M);assert match
   actual=json.loads(match[1]);assert len(actual)==len(set(actual))and required<=set(actual)
   return match,actual
  match,actual=verify(text)
  for name in required:
   with self.subTest(name=name),self.assertRaises(AssertionError):verify(text[:match.start(1)]+json.dumps([p for p in actual if p!=name])+text[match.end(1):])

if __name__=='__main__':unittest.main()
