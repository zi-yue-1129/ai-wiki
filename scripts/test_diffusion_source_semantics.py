"""Validate the authored SVG numerical schedule and the qualitative time direction."""
import unittest,bisect,xml.etree.ElementTree as E
from pathlib import Path
from verify_concept_motion import verify_source_pair
R=Path(__file__).resolve().parents[1];A=R/'docs/assets/concept-animations';N='{http://www.w3.org/2000/svg}'
def value(a,t):
 v=list(map(float,a.get('values').split(';')));ts=list(map(float,a.get('keyTimes').split(';')));i=min(len(v)-2,max(0,bisect.bisect_right(ts,t)-1));return v[i] if a.get('calcMode')=='discrete' else v[i]+(v[i+1]-v[i])*(t-ts[i])/(ts[i+1]-ts[i])
class Diffusion(unittest.TestCase):
 def test_eta_squared_budget_at_every_displayed_time(self):
  r=E.parse(A/'ddim-eta-coefficients-motion.svg').getroot();an={(a.get('href'),a.get('attributeName')):a for a in r.iter(N+'animate')}
  for t in [i/1000 for i in range(1000)]:
   eta=(value(an['#knob','cx'],t)-144)/448;fresh=value(an['#fresh','width'],t);pred=value(an['#pred','width'],t);x=value(an['#fresh','x'],t)
   self.assertAlmostEqual(fresh/448,.24609375*eta**2,12);self.assertAlmostEqual(.64+(pred+fresh)/448,1,12);self.assertAlmostEqual(x+fresh,592,12)
 def test_still_eta_exact(self):
  r=E.parse(A/'ddim-eta-coefficients-still.svg').getroot();ids={e.get('id'):e for e in r.iter() if e.get('id')};eta=(float(ids['knob'].get('cx'))-144)/448
  self.assertAlmostEqual(eta,.65);self.assertAlmostEqual(float(ids['fresh'].get('width'))/448,.24609375*eta**2,12);self.assertAlmostEqual((float(ids['pred'].get('width'))+float(ids['fresh'].get('width')))/448,.36)
 def test_forward_qualitative_monotone_before_loop_reset(self):
  r=E.parse(A/'ddpm-progressive-noising-motion.svg').getroot();a=list(r.iter(N+'animate'));self.assertEqual(len(a),3)
  signal=list(map(float,a[1].get('values').split(';')))[:-1];noise=list(map(float,a[2].get('values').split(';')))[:-1]
  self.assertEqual(signal,sorted(signal,reverse=True));self.assertEqual(noise,sorted(noise));self.assertTrue(all(x+y==425 for x,y in zip(signal,noise)))
 def test_sampling_indices_decrease(self):
  r=E.parse(A/'ddim-strided-sampling-motion.svg').getroot();texts=list(r.iter(N+'text'))
  self.assertEqual([e.text for e in texts if e.get('y')=='143'],list(map(str,range(8,-1,-1))));self.assertEqual([e.text for e in texts if e.get('y')=='253'],list(map(str,range(8,-1,-2))))
  for a in r.iter(N+'animate'):
   xs=list(map(float,a.get('values').split(';')));self.assertEqual(xs[:-1],sorted(xs[:-1]));self.assertEqual(xs[0],xs[-1]);self.assertEqual(a.get('calcMode'),'discrete')
 def test_bilingual_sources(self):
  for stem,page in [('ddpm-progressive-noising','ddpm'),('ddim-strided-sampling','ddim'),('ddim-eta-coefficients','ddim')]:
   for suffix in ['.md','.zh-TW.md']:
    p=R/f'docs/theory/paradigms/unsupervised/density-and-generative-models/diffusion/{page}{suffix}';self.assertEqual(verify_source_pair(p,p.read_text(),stem),[]);self.assertIn('tabindex="0"',p.read_text())
class NativeDiffusionFixtureContract(unittest.TestCase):
 def test_fixture_paths_match_each_real_bilingual_source(self):
  import ast
  from html.parser import HTMLParser
  class Images(HTMLParser):
   def __init__(self,html):super().__init__();self.images=[];self.feed(html)
   def handle_starttag(self,tag,attrs):
    if tag=='img':self.images.append(dict(attrs))
  def check(source):
   tree=ast.parse(source);calls=[n for n in ast.walk(tree)if isinstance(n,ast.Call)and isinstance(n.func,ast.Attribute)]
   htmlarg=next(n.args[0]for n in calls if n.func.attr=='set_content');route=next(n.args[0].value for n in calls if n.func.attr=='route');assert route=='**/assets/concept-animations/*.svg'
   loops={n.target.id:ast.literal_eval(n.iter)for n in ast.walk(tree)if isinstance(n,ast.For)and isinstance(n.target,ast.Name)and isinstance(n.iter,ast.List)}
   assert loops=={'stem':['ddpm-progressive-noising','ddim-strided-sampling','ddim-eta-coefficients'],'lang':['en','zh'],'width':[320,390,1024],'reduced':['reduce','no-preference']}
   for stem,page in [('ddpm-progressive-noising','ddpm'),('ddim-strided-sampling','ddim'),('ddim-eta-coefficients','ddim')]:
    size=800 if stem=='ddim-eta-coefficients'else 640
    html=eval(compile(ast.Expression(htmlarg),'<actual diffusion fixture>','eval'),{'css':'','stem':stem,'alt':'test','size':size});image=Images(html).images[0]
    assert image['src']==f'https://wiki.example/assets/concept-animations/{stem}-still.svg'
    assert image['data-still-src']==image['src'] and image['data-motion-src']==image['src'].replace('-still.svg','-motion.svg')
    for suffix in ('.md','.zh-TW.md'):
     doc=(R/f'docs/theory/paradigms/unsupervised/density-and-generative-models/diffusion/{page}{suffix}').read_text()
     actual=next(i for i in Images(doc).images if i.get('src','').endswith('assets/concept-animations/'+stem+'-still.svg'))
     assert actual['data-motion-src'].endswith('assets/concept-animations/'+stem+'-motion.svg')
     assert actual['data-still-src'].endswith('assets/concept-animations/'+stem+'-still.svg')
  source=(R/'scripts/test_diffusion_source_browser.py').read_text();check(source)
  for bad in [source.replace('https://wiki.example/assets/concept-animations/','https://wiki.example/assets/'),source.replace('**/assets/concept-animations/*.svg','**/assets/*.svg'),source.replace('data-still-src=','data-wrong-still='),source.replace('[320,390,1024]','[390,1024]'),source.replace("['reduce','no-preference']","['no-preference']")]:
   with self.assertRaises((AssertionError,KeyError)):check(bad)
 def test_failure_capture_closes_and_reraises_actual_producer(self):
  import tempfile,json
  from unittest.mock import MagicMock,patch
  import test_diffusion_source_browser as b
  manager=MagicMock();browser=manager.__enter__.return_value.chromium.launch.return_value;page=browser.new_page.return_value
  page.evaluate.side_effect=[320,{'readyState':'complete','eligible':0,'buttons':0}];page.locator.return_value.count.return_value=0;page.content.return_value='<html>old diffusion path diagnostic</html>'
  with tempfile.TemporaryDirectory()as directory,patch.object(b,'OUT',Path(directory)),patch.object(b,'sync_playwright',return_value=manager):
   with self.assertRaises(AssertionError):b.main()
   report=json.loads((Path(directory)/'report.json').read_text());self.assertEqual(report['status'],'failed');self.assertEqual(report['cases'][0]['dom']['eligible'],0);self.assertEqual(report['cases'][0]['status'],'failed')
   self.assertTrue(list(Path(directory).glob('*-failure.html')));page.screenshot.assert_called_once();page.close.assert_called_once()
 def test_true_selector_and_rejecting_always_return_mock(self):
  import subprocess
  result=subprocess.run(['node','scripts/test_diffusion_schedule_player.cjs'],cwd=R,capture_output=True,text=True);self.assertEqual(result.returncode,0,result.stderr);self.assertIn('12 wrong-path selector negatives plus 12 actual diffusion',result.stdout)
  program="const h=require.resolve('./scripts/concept_motion_fixture_selector.cjs');require(h);require.cache[h].exports=(selector,images)=>images;require('./scripts/test_diffusion_schedule_player.cjs');"
  bad=subprocess.run(['node','-e',program],cwd=R,capture_output=True,text=True);self.assertNotEqual(bad.returncode,0);self.assertIn('AssertionError',bad.stderr)
 def test_actual_ci_routes_and_transitive_dependencies_precede_contract(self):
  import yaml,fnmatch,copy
  w=yaml.safe_load((R/'.github/workflows/concept-animation-validation.yml').read_text())
  paths=['scripts/concept_motion_fixture_selector.cjs','scripts/test_concept_motion_fixture_selector.cjs','scripts/test_diffusion_source_browser.py','scripts/test_diffusion_source_semantics.py','scripts/test_diffusion_schedule_player.cjs']
  commands=['node scripts/test_concept_motion_fixture_selector.cjs','python -m unittest discover -s scripts -p "test_*diffusion*semantics.py"','node scripts/test_diffusion_schedule_player.cjs','python scripts/test_diffusion_source_browser.py']
  def check(w):
   patterns=w.get('on',w.get(True))['pull_request']['paths'];assert all(any(fnmatch.fnmatchcase(p,g)for g in patterns)for p in paths)
   job=w['jobs']['validate-motion'];assert 'if'not in job and (job.get('continue-on-error')is None or job.get('continue-on-error')is False)
   lines=[]
   for step in job['steps']:
    if 'if'not in step and (step.get('continue-on-error')is None or step.get('continue-on-error')is False):lines.extend(line.strip()for line in step.get('run','').splitlines())
   assert all(command in lines for command in commands)
   consumer=lines.index(commands[1])
   for dependency in ['python -m pip install "playwright==1.55.0"','python -m pip install "PyYAML==6.0.3"']:
    assert dependency in lines and lines.index(dependency)<consumer,'Fixture imports require same-job earlier dependencies'
  check(w)
  for path in paths:
   bad=copy.deepcopy(w);event=bad.get('on',bad.get(True));event['pull_request']['paths']=[pattern for pattern in event['pull_request']['paths']if not fnmatch.fnmatchcase(path,pattern)]
   with self.assertRaises(AssertionError):check(bad)
  for condition in [False,None,'always()']:
   bad=copy.deepcopy(w)
   for step in bad['jobs']['validate-motion']['steps']:
    if commands[1]in step.get('run',''):step['if']=condition
   with self.assertRaises(AssertionError):check(bad)
  for dependency in ['python -m pip install "playwright==1.55.0"','python -m pip install "PyYAML==6.0.3"']:
   for mode in ['delete','late','softfail','zero']:
    bad=copy.deepcopy(w);steps=bad['jobs']['validate-motion']['steps'];installations=[s for s in steps if dependency in s.get('run','').splitlines()]
    assert installations
    for installation in installations:
     if mode in ['softfail','zero']:installation['continue-on-error']=True if mode=='softfail' else 0
     else:installation['run']=installation['run'].replace(dependency,'')
    if mode=='late':steps.append({'run':dependency})
    with self.assertRaises(AssertionError):check(bad)

if __name__=='__main__':unittest.main()
