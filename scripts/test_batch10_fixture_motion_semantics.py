"""Actual source/native fixture routing, original matrices and failure evidence."""
import ast,copy,fnmatch,importlib,json,subprocess,tempfile,unittest
from pathlib import Path
from html.parser import HTMLParser
from unittest.mock import MagicMock,patch
import yaml
R=Path(__file__).resolve().parents[1]
SPECS={'federated': {'stems': ['fedavg-weighted-round', 'secagg-mask-cancellation'], 'docs': {'fedavg-weighted-round': ['docs/theory/paradigms/federated/federated-averaging/index.md', 'docs/theory/paradigms/federated/federated-averaging/index.zh-TW.md'], 'secagg-mask-cancellation': ['docs/theory/paradigms/federated/privacy-and-secure-aggregation/index.md', 'docs/theory/paradigms/federated/privacy-and-secure-aggregation/index.zh-TW.md']}}, 'grounded_action': {'stems': ['saycan-skill-grounding', 'rt2-action-token-decoding'], 'docs': {'saycan-skill-grounding': ['docs/applications/robotics/saycan/index.md', 'docs/applications/robotics/saycan/index.zh-TW.md'], 'rt2-action-token-decoding': ['docs/applications/robotics/rt-2/index.md', 'docs/applications/robotics/rt-2/index.zh-TW.md']}}, 'openvla': {'stems': ['openvla-dual-encoder-fusion', 'openvla-percentile-action-bins'], 'docs': {'openvla-dual-encoder-fusion': ['docs/applications/robotics/openvla/index.md', 'docs/applications/robotics/openvla/index.zh-TW.md'], 'openvla-percentile-action-bins': ['docs/applications/robotics/openvla/index.md', 'docs/applications/robotics/openvla/index.zh-TW.md']}}}
class Images(HTMLParser):
 def __init__(self,text):super().__init__();self.images=[];self.feed(text)
 def handle_starttag(self,tag,attrs):
  if tag=='img':self.images.append(dict(attrs))

def check_fixture(topic,source):
 tree=ast.parse(source);calls=[n for n in ast.walk(tree)if isinstance(n,ast.Call)and isinstance(n.func,ast.Attribute)]
 htmlarg=next(n.args[0]for n in calls if n.func.attr=='set_content');route=next(n.args[0].value for n in calls if n.func.attr=='route')
 assert route=='**/assets/concept-animations/*.svg'
 loops={n.target.id:ast.literal_eval(n.iter)for n in ast.walk(tree)if isinstance(n,ast.For)and isinstance(n.target,ast.Name)and isinstance(n.iter,ast.List)}
 assert loops=={'stem':SPECS[topic]['stems'],'lang':['en','zh'],'width':[320,390,1024],'reduced':['reduce','no-preference']}
 for stem in SPECS[topic]['stems']:
  html=eval(compile(ast.Expression(htmlarg),'<actual source fixture>','eval'),{'css':'','stem':stem,'alt':'test','size':640});image=Images(html).images[0]
  for key,kind in [('src','still'),('data-still-src','still'),('data-motion-src','motion')]:assert image[key]==f'https://wiki.example/assets/concept-animations/{stem}-{kind}.svg'
  for doc in SPECS[topic]['docs'][stem]:
   images=Images((R/doc).read_text()).images
   assert any(i.get('src','').endswith(f'assets/concept-animations/{stem}-still.svg') and i.get('data-motion-src','').endswith(f'assets/concept-animations/{stem}-motion.svg') for i in images),(stem,doc)
 return loops

class Fixtures(unittest.TestCase):
 def test_real_source_paths_matrices_and_old_path_negatives(self):
  for topic in SPECS:
   source=(R/f'scripts/test_{topic}_source_browser.py').read_text();check_fixture(topic,source)
   for old,new in [('https://wiki.example/assets/concept-animations/','https://wiki.example/assets/'),('**/assets/concept-animations/*.svg','**/assets/*.svg'),("[320,390,1024]","[390,1024]"),("['reduce','no-preference']","['no-preference']")]:
    with self.subTest(topic=topic,mutation=old),self.assertRaises(AssertionError):check_fixture(topic,source.replace(old,new))
 def test_producer_failure_has_diagnostics_and_reraises(self):
  for topic in SPECS:
   module=importlib.import_module(f'test_{topic}_source_browser')
   for capture_fails in (False,True):
    manager=MagicMock();browser=manager.__enter__.return_value.chromium.launch.return_value;page=browser.new_page.return_value
    page.evaluate.side_effect=[320,{'readyState':'complete','eligible':0,'buttons':0}];page.locator.return_value.count.return_value=0;page.content.return_value='<html>old-path failure</html>'
    if capture_fails:page.screenshot.side_effect=RuntimeError('diagnostic screenshot failed')
    with tempfile.TemporaryDirectory()as directory,patch.object(module,'OUT',Path(directory)),patch.object(module,'sync_playwright',return_value=manager):
     with self.assertRaises(AssertionError):module.main()
     report=json.loads((Path(directory)/'report.json').read_text());self.assertEqual(report['status'],'failed');self.assertEqual(len(report['cases']),1);case=report['cases'][0];self.assertEqual(case['status'],'failed');self.assertEqual(case['dom']['eligible'],0)
     self.assertIn('AssertionError',report['error']);page.close.assert_called_once();page.screenshot.assert_called_once()
     if capture_fails:self.assertIn('diagnostic screenshot failed',case['capture_error'])
     else:self.assertTrue(list(Path(directory).glob('*-failure.html')))
 def test_true_selector_positive_negative_and_always_images_mutation(self):
  for topic in SPECS:
   script=f'scripts/test_{topic}_source_player.cjs';result=subprocess.run(['node',script],cwd=R,capture_output=True,text=True);self.assertEqual(result.returncode,0,result.stderr);self.assertIn('8 wrong-path selector negatives plus 8 actual',result.stdout)
   program="const h=require.resolve('./scripts/concept_motion_fixture_selector.cjs');require(h);require.cache[h].exports=(selector,images)=>images;require('./"+script+"');"
   bad=subprocess.run(['node','-e',program],cwd=R,capture_output=True,text=True);self.assertNotEqual(bad.returncode,0);self.assertIn('AssertionError',bad.stderr)
 def test_future_file_only_triggers_unconditional_native_and_negatives(self):
  workflow=yaml.safe_load((R/'.github/workflows/concept-animation-validation.yml').read_text())
  files=['scripts/concept_motion_fixture_selector.cjs','scripts/test_concept_motion_fixture_selector.cjs','scripts/test_batch10_fixture_motion_semantics.py']+[f'scripts/test_{t}_source_{suffix}'for t in SPECS for suffix in ['browser.py','player.cjs']]
  commands=['node scripts/test_concept_motion_fixture_selector.cjs','python scripts/test_batch10_fixture_motion_semantics.py']+[f'python scripts/test_{t}_source_browser.py'for t in SPECS]+[f'node scripts/test_{t}_source_player.cjs'for t in SPECS]
  def check(w):
   patterns=w.get('on',w.get(True))['pull_request']['paths'];assert all(any(fnmatch.fnmatchcase(f,p)for p in patterns)for f in files)
   job=w['jobs']['validate-motion'];assert 'if'not in job and (job.get('continue-on-error')is None or job.get('continue-on-error')is False)
   runs=[line.strip()for s in job['steps']if 'if'not in s and(s.get('continue-on-error')is None or s.get('continue-on-error')is False)for line in s.get('run','').splitlines()]
   assert all(c in runs for c in commands)
  check(workflow)
  for file in files:
   w=copy.deepcopy(workflow);event=w.get('on',w.get(True));event['pull_request']['paths']=[p for p in event['pull_request']['paths']if not fnmatch.fnmatchcase(file,p)]
   with self.subTest(file=file),self.assertRaises(AssertionError):check(w)
  for command in commands:
   for key,value in [('if',False),('if',None),('if','always()'),('continue-on-error',True),('continue-on-error',0)]:
    w=copy.deepcopy(workflow);step=next(s for s in w['jobs']['validate-motion']['steps']if command in [x.strip()for x in s.get('run','').splitlines()]);step[key]=value
    with self.subTest(command=command,key=key,value=value),self.assertRaises(AssertionError):check(w)
 def test_transitive_imports_are_installed_before_same_job_consumers(self):
  workflow=yaml.safe_load((R/'.github/workflows/concept-animation-validation.yml').read_text())
  consumers={'python -m pip install "playwright==1.55.0"':['python scripts/test_batch10_fixture_motion_semantics.py']+[f'python scripts/test_{t}_source_browser.py'for t in SPECS],
             'python -m pip install "PyYAML==6.0.3"':['python scripts/test_batch10_fixture_motion_semantics.py'],
             'python -m pip install "numpy==2.5.5"':['python scripts/test_openvla_actual_motion_semantics.py']}
  def check(w):
   job=w['jobs']['validate-motion'];assert 'if'not in job and(job.get('continue-on-error')is None or job.get('continue-on-error')is False)
   lines=[line.strip()for step in job['steps']if 'if'not in step and(step.get('continue-on-error')is None or step.get('continue-on-error')is False)for line in step.get('run','').splitlines()]
   for install,commands in consumers.items():
    assert install in lines
    assert all(c in lines and lines.index(install)<lines.index(c)for c in commands)
  check(workflow)
  for install,commands in consumers.items():
   for mode in ('remove','late','false','null','always','softfail','zero'):
    w=copy.deepcopy(workflow);steps=w['jobs']['validate-motion']['steps'];installations=[s for s in steps if install in s.get('run','').splitlines()]
    assert installations
    for step in installations:
     if mode in ('remove','late'):step['run']='\n'.join(line for line in step['run'].splitlines()if line!=install)
     elif mode=='false':step['if']=False
     elif mode=='null':step['if']=None
     elif mode=='always':step['if']='always()'
     elif mode=='softfail':step['continue-on-error']=True
     else:step['continue-on-error']=0
    if mode=='late':
     consumer=next(i for i,s in enumerate(steps)if commands[0]in s.get('run','').splitlines());steps.insert(consumer+1,{'name':'too late dependency','run':install})
    with self.subTest(install=install,mode=mode),self.assertRaises(AssertionError):check(w)
if __name__=='__main__':unittest.main()
