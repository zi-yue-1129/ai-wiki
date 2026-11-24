"""Original-source and native-fixture contracts for marl; run after browser dependencies."""
import ast,copy,fnmatch,json,subprocess,tempfile,unittest
from pathlib import Path
from html.parser import HTMLParser
from unittest.mock import MagicMock,patch
R=Path(__file__).resolve().parents[1]
STEMS=['maddpg-actor-gradient', 'maddpg-joint-bootstrap', 'mappo-shared-advantage', 'mappo-backward-gae']
SOURCES={'maddpg-actor-gradient': ['docs/theory/paradigms/reinforcement-learning/multi-agent-rl/maddpg/index.md', 'docs/theory/paradigms/reinforcement-learning/multi-agent-rl/maddpg/index.zh-TW.md'], 'maddpg-joint-bootstrap': ['docs/theory/paradigms/reinforcement-learning/multi-agent-rl/maddpg/index.md', 'docs/theory/paradigms/reinforcement-learning/multi-agent-rl/maddpg/index.zh-TW.md'], 'mappo-shared-advantage': ['docs/theory/paradigms/reinforcement-learning/multi-agent-rl/mappo/index.md', 'docs/theory/paradigms/reinforcement-learning/multi-agent-rl/mappo/index.zh-TW.md'], 'mappo-backward-gae': ['docs/theory/paradigms/reinforcement-learning/multi-agent-rl/mappo/index.md', 'docs/theory/paradigms/reinforcement-learning/multi-agent-rl/mappo/index.zh-TW.md']}
CASES=48
class Images(HTMLParser):
 def __init__(self,html):super().__init__();self.images=[];self.feed(html)
 def handle_starttag(self,tag,attrs):
  if tag=='img':self.images.append(dict(attrs))
def check_fixture(source):
 tree=ast.parse(source);calls=[n for n in ast.walk(tree)if isinstance(n,ast.Call)and isinstance(n.func,ast.Attribute)]
 htmlarg=next(n.args[0]for n in calls if n.func.attr=='set_content');route=next(n.args[0].value for n in calls if n.func.attr=='route')
 assert route=='**/assets/concept-animations/*.svg'
 loops=[ast.literal_eval(n.iter)for n in ast.walk(tree)if isinstance(n,ast.For)]
 assert loops==[STEMS,['en','zh'],[320,390,1024],['reduce','no-preference']], 'Original native matrix drift'
 assert len(STEMS)*2*3*2==CASES
 for stem in STEMS:
  html=eval(compile(ast.Expression(htmlarg),'<actual native fixture>','eval'),{'css':'','stem':stem,'alt':'test','size':640})
  image=Images(html).images[0]
  for attr,kind in [('src','still'),('data-motion-src','motion'),('data-still-src','still')]:
   expected=f'assets/concept-animations/{stem}-{kind}.svg'
   assert image[attr]=='https://wiki.example/'+expected
   for path in SOURCES[stem]:
    matching=[i for i in Images((R/path).read_text()).images if i.get('src','').endswith(f'assets/concept-animations/{stem}-still.svg')]
    assert len(matching)==1,(path,stem)
    assert matching[0].get(attr,'').endswith(expected),(path,attr)
    assert (R/'docs'/expected).is_file()
 return True
class NativeFixtureContract(unittest.TestCase):
 def test_actual_fixture_source_paths_all_locales_and_original_matrix(self):
  source=(R/'scripts/test_marl_source_browser.py').read_text();self.assertTrue(check_fixture(source))
  variants=[source.replace('https://wiki.example/assets/concept-animations/','https://wiki.example/assets/'),source.replace('**/assets/concept-animations/*.svg','**/assets/*.svg'),source.replace("['en','zh']","['en']")]
  for variant in variants:
   with self.assertRaises(AssertionError):check_fixture(variant)
 def test_actual_producer_failure_records_diagnostics_and_reraises(self):
  import test_marl_source_browser as b
  manager=MagicMock();browser=manager.__enter__.return_value.chromium.launch.return_value;page=browser.new_page.return_value
  page.evaluate.side_effect=[320,{'readyState':'complete','eligible':0,'buttons':0}];page.locator.return_value.count.return_value=0;page.content.return_value='<html>old fixture diagnostic</html>'
  with tempfile.TemporaryDirectory()as directory,patch.object(b,'OUT',Path(directory)),patch.object(b,'sync_playwright',return_value=manager):
   with self.assertRaises(AssertionError):b.main()
   report=json.loads((Path(directory)/'report.json').read_text());self.assertEqual(report['status'],'failed');self.assertEqual(len(report['cases']),1);self.assertEqual(report['cases'][0]['status'],'failed');self.assertEqual(report['cases'][0]['dom']['eligible'],0)
   self.assertTrue(list(Path(directory).glob('*-failure.html')));page.screenshot.assert_called_once();page.close.assert_called_once()
 def test_actual_js_positives_wrong_path_negatives_and_false_mock_rejection(self):
  result=subprocess.run(['node','scripts/test_marl_source_player.cjs'],cwd=R,capture_output=True,text=True)
  self.assertEqual(result.returncode,0,result.stderr);self.assertIn('16 wrong-path selector negatives plus 16 actual',result.stdout)
  program="const h=require.resolve('./scripts/concept_motion_fixture_selector.cjs');require(h);require.cache[h].exports=(selector,images)=>images;require('./scripts/test_marl_source_player.cjs');"
  bad=subprocess.run(['node','-e',program],cwd=R,capture_output=True,text=True);self.assertNotEqual(bad.returncode,0);self.assertIn('AssertionError',bad.stderr)
 def test_future_only_file_routes_and_dependency_order_fail_closed(self):
  import yaml
  workflow=yaml.safe_load((R/'.github/workflows/concept-animation-validation.yml').read_text())
  paths=['scripts/test_marl_source_semantics.py','scripts/concept_motion_fixture_selector.cjs','scripts/test_concept_motion_fixture_selector.cjs','scripts/test_marl_source_browser.py','scripts/test_marl_source_player.cjs','scripts/test_marl_fixture_motion_semantics.py']
  commands=['python scripts/test_marl_source_semantics.py','node scripts/test_concept_motion_fixture_selector.cjs','python scripts/test_marl_source_browser.py','node scripts/test_marl_source_player.cjs','python scripts/test_marl_fixture_motion_semantics.py']
  def verify(w):
   patterns=w.get('on',w.get(True))['pull_request']['paths'];assert all(any(fnmatch.fnmatchcase(path,pattern)for pattern in patterns)for path in paths)
   job=w['jobs']['validate-motion'];assert 'if'not in job and (job.get('continue-on-error')is None or job.get('continue-on-error')is False)
   command_steps={}
   for index,step in enumerate(job['steps']):
    if 'if'not in step and (step.get('continue-on-error')is None or step.get('continue-on-error')is False):
     for line in step.get('run','').splitlines():command_steps[line.strip()]=index
   assert all(command in command_steps for command in commands)
   uploads=[step for step in job['steps']if str(step.get('uses','')).startswith('actions/upload-artifact@')and step.get('if')=='always()']
   patterns=[line.strip()for step in uploads for line in step.get('with',{}).get('path','').splitlines()]
   for name in ['report.json','example-failure.png','example-failure.html']:
    path='artifacts/marl-source/'+name
    assert any((pattern.endswith('/')and path.startswith(pattern))or fnmatch.fnmatchcase(path,pattern)for pattern in patterns), 'Failure evidence not uploaded'
   fixture=command_steps['python scripts/test_marl_fixture_motion_semantics.py'];native=command_steps['python scripts/test_marl_source_browser.py']
   for dependency in ['python -m pip install "playwright==1.55.0"','python -m pip install "PyYAML==6.0.3"']:
    assert dependency in command_steps and command_steps[dependency]<fixture and command_steps[dependency]<native
  verify(workflow)
  for path in paths:
   bad=copy.deepcopy(workflow);event=bad.get('on',bad.get(True));event['pull_request']['paths']=[x for x in event['pull_request']['paths']if not fnmatch.fnmatchcase(path,x)]
   with self.subTest(path=path),self.assertRaises(AssertionError):verify(bad)
  bad=copy.deepcopy(workflow)
  for step in bad['jobs']['validate-motion']['steps']:
   if 'path'in step.get('with',{}):step['with']['path']='\n'.join(line for line in step['with']['path'].splitlines()if 'artifacts/marl-source/'not in line)
  with self.assertRaises(AssertionError):verify(bad)
  for mode in ['if-false','if-null','if-always','soft-true','soft-zero','soft-string','job-false','delete-playwright','delete-yaml']:
   bad=copy.deepcopy(workflow);job=bad['jobs']['validate-motion'];step=next(x for x in job['steps']if 'python scripts/test_marl_fixture_motion_semantics.py'in x.get('run','').splitlines())
   if mode.startswith('if-'):step['if']={'if-false':False,'if-null':None,'if-always':'always()'}[mode]
   elif mode.startswith('soft-'):step['continue-on-error']={'soft-true':True,'soft-zero':0,'soft-string':'false'}[mode]
   elif mode=='job-false':job['if']=False
   else:
    token='playwright==1.55.0'if mode=='delete-playwright'else'PyYAML==6.0.3'
    for s in job['steps']:
     if 'run'in s:s['run']='\n'.join(line for line in s['run'].splitlines()if token not in line)
   with self.subTest(mode=mode),self.assertRaises(AssertionError):verify(bad)
if __name__=='__main__':unittest.main()
