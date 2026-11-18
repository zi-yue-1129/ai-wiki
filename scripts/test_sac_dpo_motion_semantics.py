"""Numerical/temporal checks read committed SVG animation values."""
import bisect,math,unittest,xml.etree.ElementTree as E
from functools import lru_cache
from pathlib import Path
R=Path(__file__).resolve().parents[1];A=R/'docs/assets/concept-animations';N='{http://www.w3.org/2000/svg}'
@lru_cache(None)
def parsed(a):
 vs=list(map(float,a.get('values').split(';')));ts=list(map(float,a.get('keyTimes',';'.join(str(i/(len(vs)-1)) for i in range(len(vs)))).split(';')));return ts,vs

def value(a,t):
 ts,vs=parsed(a)
 if t==1:return vs[-1]
 i=min(len(vs)-2,max(0,bisect.bisect_right(ts,t)-1))
 return vs[i] if a.get('calcMode')=='discrete' else vs[i]+(vs[i+1]-vs[i])*(t-ts[i])/(ts[i+1]-ts[i])
class SacDpoMotion(unittest.TestCase):
 def test_sac_geometry(self):
  r=E.parse(A/'sac-entropy-temperature-motion.svg').getroot();an=list(r.iter(N+'animate'))
  for i in range(10001):
   t=i/10000;a=1.25+.75*math.cos(2*math.pi*t);p=[math.exp((q-2)/a) for q in [2,1,0]];z=sum(p);p=[v/z for v in p];H=-sum(v*math.log(v) for v in p)
   for k,v in enumerate(p):
    self.assertAlmostEqual(value(an[2*k],t),194*v,delta=.025);self.assertAlmostEqual(value(an[2*k],t)+value(an[2*k+1],t),330,delta=.00001)
   self.assertAlmostEqual(value(an[-2],t),522+(a-.5)/1.5*184,delta=.025);self.assertAlmostEqual(value(an[-1],t),320-147.32*H,delta=.03)
 def test_dpo_geometry(self):
  r=E.parse(A/'dpo-preference-margin-motion.svg').getroot();an=list(r.iter(N+'animate'))
  for i in range(10001):
   t=i/10000;d=-1.6*math.cos(2*math.pi*t);p=1/(1+math.exp(-d))
   self.assertAlmostEqual(value(an[0],t),198*p,delta=.025);self.assertAlmostEqual(value(an[0],t)+value(an[1],t),198,delta=.00001)
   self.assertAlmostEqual(value(an[2],t),403+(d+1.6)/3.2*296,delta=.025);self.assertAlmostEqual(value(an[3],t),322-87*math.log1p(math.exp(-d)),delta=.03)
 def test_source_hooks_and_math_blocks(self):
  for folder in ['learning-from-human-feedback/dpo','policy-gradient-and-actor-critic/sac']:
   for lang in ['', '.zh-TW']:
    text=(R/'docs/theory/paradigms/reinforcement-learning'/folder/('index'+lang+'.md')).read_text()
    for token in ['data-source-asset-urls','data-still-src','concept-motion-scroll','tabindex="0"','min-width:760px']:self.assertIn(token,text)
    self.assertNotIn('class="concept-motion-wide"',text)
    self.assertEqual(text.count(r'\begin{aligned}'),text.count(r'\end{aligned}'))


def check_dpo_reward_display(text):
 import re
 blocks=re.findall(r'\$\$(.*?)\$\$',text,re.S)
 expected=r'\begin{aligned}r(x,y)&=\beta\log\frac{\pi_r(y\mid x)}{\pi_{\mathrm{ref}}(y\mid x)}\\&\quad+\beta\log Z(x).\end{aligned}'
 compact=lambda x:re.sub(r'\s+','',x)
 matches=[b for b in blocks if 'r(x,y)' in compact(b)]
 assert len(matches)==1 and compact(matches[0])==compact(expected), 'Reward identity must retain all terms in the reviewed two-line display'
 assert not re.search(r'\\\(\s*r\(x,\s*y\)\s*=',text), 'Former overflowing inline reward identity'
 return matches[0]

class DpoRewardMobile(unittest.TestCase):
 def test_bilingual_two_line_identity_and_original_inline_negative(self):
  base=R/'docs/theory/paradigms/reinforcement-learning/learning-from-human-feedback/dpo'
  for name in ('index.md','index.zh-TW.md'):
   text=(base/name).read_text();block=check_dpo_reward_display(text)
   original=r'\(r(x, y) = \beta \log(\pi_r(y \mid x)/\pi_{\text{ref}}(y \mid x)) + \beta \log Z(x)\)'
   with self.assertRaises(AssertionError):check_dpo_reward_display(text.replace('$$'+block+'$$',original))
   for old,new in [(r'+\beta\log Z(x)',r'-\beta\log Z(x)'),(r'\beta\log\frac',r'\log\frac'),(r'\pi_{\mathrm{ref}}',r'\pi_r')]:
    with self.subTest(name=name,mutation=old),self.assertRaises(AssertionError):check_dpo_reward_display(text.replace(old,new,1))
 def test_reward_identity_and_partition_cancellation_numerically(self):
  # Recover rewards from the KL-optimal policy, not merely a formula snapshot.
  for beta in (.1,.3,1.,2.,5.):
   for ref in ((.1,.2,.7),(.6,.3,.1),(.01,.98,.01)):
    for rewards in ((-2.,0.,3.),(.5,-.7,1.2),(4.,4.,4.)):
     logits=[math.log(p)+r/beta for p,r in zip(ref,rewards)];m=max(logits);logZ=m+math.log(sum(math.exp(x-m)for x in logits));logpolicy=[x-logZ for x in logits]
     recovered=[beta*(lp-math.log(p))+beta*logZ for lp,p in zip(logpolicy,ref)]
     for actual,expected in zip(recovered,rewards):self.assertAlmostEqual(actual,expected,places=12)
     margin=beta*((logpolicy[0]-math.log(ref[0]))-(logpolicy[1]-math.log(ref[1])))
     self.assertAlmostEqual(margin,rewards[0]-rewards[1],places=12)

class ScopedLayoutRegression(unittest.TestCase):
 def test_geometry_boundary_rejects_old_host_without_weakening_mobile_scroll(self):
  from test_sac_dpo_motion_browser import assert_scroll_geometry
  for viewport in (320,360,760,1024):
   good={'innerWidth':viewport,'clientWidth':viewport,'documentWidth':viewport,'region':{'clientWidth':viewport,'scrollWidth':max(viewport,760)}}
   assert_scroll_geometry(good,viewport)
   bad={**good,'region':{'clientWidth':viewport,'scrollWidth':viewport if viewport<760 else viewport+60}}
   with self.assertRaises(AssertionError):assert_scroll_geometry(bad,viewport)
  with self.assertRaises(AssertionError):assert_scroll_geometry({'innerWidth':408,'clientWidth':390,'documentWidth':408,'region':{'clientWidth':358,'scrollWidth':760}},390)
 def test_four_pages_and_fixture_share_scoped_host_without_global_change(self):
  css=(R/'docs/stylesheets/concept-motion.css').read_text()
  self.assertIn('.sac-dpo-motion-frame > .concept-motion-player',css)
  self.assertIn('max-width: 640px',css)
  browser=(R/'scripts/test_sac_dpo_motion_browser.py').read_text()
  self.assertIn('for viewport in (320,360,760,1024)',browser)
  self.assertIn('for reduced in (False, True)',browser)
  self.assertIn('old_host_counterfactual(browser, html, js, handle, record)',browser)
  for folder in ('learning-from-human-feedback/dpo','policy-gradient-and-actor-critic/sac'):
   for suffix in ('.md','.zh-TW.md'):
    source=(R/'docs/theory/paradigms/reinforcement-learning'/folder/('index'+suffix)).read_text()
    self.assertIn('class="concept-motion-scroll sac-dpo-motion-scroll"',source)
    self.assertIn('class="sac-dpo-motion-frame"',source)
 def test_built_producer_and_gate_keep_original_states_and_explicit_formula_call(self):
  import ast
  tree=ast.parse((R/'scripts/test_built_motion_browser.py').read_text())
  exercise=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='exercise_page')
  calls=[n.func.id for n in ast.walk(exercise) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name)]
  self.assertIn('dpo_mobile',calls);self.assertIn('check_dpo_reward_identity',calls)
  gate=ast.parse((R/'scripts/motion_shard_contract.py').read_text())
  validate=next(n for n in gate.body if isinstance(n,ast.FunctionDef) and n.name=='validate_shards')
  self.assertTrue(any(isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='validate_dpo_reward_evidence' for n in ast.walk(validate)))

 def test_native_counterfactual_producer_path_and_cleanup_with_mock_browser(self):
  # Mock only browser transport: run the real producer and unchanged geometry assertion.
  # This is not native-renderer evidence; new CI must supply the real measurements.
  from unittest.mock import MagicMock,patch
  import test_sac_dpo_motion_browser as b
  for overflow in (True,False):
   page=MagicMock();browser=MagicMock();browser.new_page.return_value=page
   geometry={'innerWidth':760,'clientWidth':760,'documentWidth':760,
      'host':{'width':640},'img':{'width':760},'region':{'clientWidth':760,'scrollWidth':820 if overflow else 760}}
   record={'id':'mock-only'}
   with patch.object(b,'scroll_geometry',return_value=geometry):
    if overflow:b.old_host_counterfactual(browser,'<div class="sac-dpo-motion-frame">','js',lambda _:None,record)
    else:
     with self.assertRaises(AssertionError):b.old_host_counterfactual(browser,'<div class="sac-dpo-motion-frame">','js',lambda _:None,record)
   page.close.assert_called_once();page.add_script_tag.assert_called_once_with(content='js')
   self.assertIn('old-sac-dpo-motion-frame',page.set_content.call_args.args[0])
   self.assertEqual(record['old_host_counterfactual']['rejected'],overflow)

 def test_exact_original_32_case_matrix_missing_duplicate_failed_rejected(self):
  import copy
  from test_sac_dpo_motion_browser import TOPICS,validate_case_matrix
  rows=[dict(stem=s,lang=l,viewport=w,reduced=r,status='passed') for s in TOPICS for l in ('en','zh') for w in (320,360,760,1024) for r in (False,True)]
  validate_case_matrix(rows)
  variants=[rows[:-1],rows[:-1]+[rows[0]],copy.deepcopy(rows)]
  variants[-1][-1]['status']='failed'
  for variant in variants:
   with self.assertRaises(AssertionError):validate_case_matrix(variant)

 def test_actual_future_only_routes_and_required_unconditional_commands(self):
  import copy,fnmatch,yaml
  def verify(workflow,paths,commands):
   event=workflow.get('on',workflow.get(True));patterns=event['pull_request']['paths']
   assert all(any(fnmatch.fnmatchcase(path,pattern)for pattern in patterns)for path in paths)
   runs=[]
   for job in workflow['jobs'].values():
    if 'if' in job or job.get('continue-on-error') is not None and job.get('continue-on-error') is not False:continue
    for step in job.get('steps',[]):
     if 'if' not in step and (step.get('continue-on-error') is None or step.get('continue-on-error') is False):
      runs.extend(line.strip()for line in step.get('run','').splitlines())
   assert all(command in runs for command in commands)
  configurations=[('concept-animation-validation.yml',['scripts/test_sac_dpo_motion_browser.py','scripts/test_sac_dpo_motion_semantics.py','docs/stylesheets/concept-motion.css'],['python scripts/test_sac_dpo_motion_browser.py','python scripts/test_sac_dpo_motion_semantics.py']),
   ('built-motion-browser.yml',['scripts/motion_shard_contract.py','scripts/test_motion_shard_contract.py','scripts/test_built_motion_browser.py'],['python scripts/test_motion_shard_contract.py','python scripts/test_built_motion_browser.py --shard-index ${{ matrix.shard }} --shard-count 4'])]
  for filename,paths,commands in configurations:
   w=yaml.safe_load((R/'.github/workflows'/filename).read_text());verify(w,paths,commands)
   bad=copy.deepcopy(w);bad.get('on',bad.get(True))['pull_request']['paths']=[]
   with self.assertRaises(AssertionError):verify(bad,paths,commands)
   for flag in (False,None,'always()'):
    bad=copy.deepcopy(w)
    for job in bad['jobs'].values():
     for step in job.get('steps',[]):
      if any(command in step.get('run','').splitlines() for command in commands):step['if']=flag
    with self.assertRaises(AssertionError):verify(bad,paths,commands)

class RuntimeDependencyRegression(unittest.TestCase):
 def test_yaml_is_explicit_unconditional_and_before_consumer(self):
  import copy,yaml
  workflow=yaml.safe_load((R/'.github/workflows/concept-animation-validation.yml').read_text())
  def verify(w):
   job=w['jobs']['validate-motion'];assert 'if' not in job
   steps=job['steps'];install=[];consumer=[]
   for index,step in enumerate(steps):
    lines=[line.strip()for line in step.get('run','').splitlines()]
    valid='if' not in step and (step.get('continue-on-error') is None or step.get('continue-on-error') is False)
    if 'python -m pip install "PyYAML==6.0.3"' in lines and valid:install.append(index)
    if 'python scripts/test_sac_dpo_motion_semantics.py' in lines:
     assert valid, 'The consumer cannot be conditional or soft-failing'
     consumer.append(index)
   assert install and len(consumer)==1 and min(install)<consumer[0]
  verify(workflow)
  # An ineffective redundant provider cannot invalidate an effective earlier one.
  for field,value in [('if',False),('if',None),('if','always()'),('continue-on-error',True),('continue-on-error',0)]:
   good=copy.deepcopy(workflow);good['jobs']['validate-motion']['steps'].append({'run':'python -m pip install "PyYAML==6.0.3"',field:value});verify(good)
   # Also cover the actual retained later installation, not merely an added fake step.
   retained=copy.deepcopy(workflow);suppliers=[step for step in retained['jobs']['validate-motion']['steps']if 'python -m pip install "PyYAML==6.0.3"' in step.get('run','').splitlines()]
   if len(suppliers)>1:suppliers[-1][field]=value;verify(retained)
   bad=copy.deepcopy(workflow)
   for step in bad['jobs']['validate-motion']['steps']:
    if 'python -m pip install "PyYAML==6.0.3"' in step.get('run','').splitlines():step[field]=value
   with self.assertRaises(AssertionError):verify(bad)
   bad=copy.deepcopy(workflow)
   for step in bad['jobs']['validate-motion']['steps']:
    if 'python scripts/test_sac_dpo_motion_semantics.py' in step.get('run','').splitlines():step[field]=value
   with self.assertRaises(AssertionError):verify(bad)
  late=copy.deepcopy(workflow)
  for step in late['jobs']['validate-motion']['steps']:step['run']=step.get('run','').replace('python -m pip install "PyYAML==6.0.3"','')
  late['jobs']['validate-motion']['steps'].append({'run':'python -m pip install "PyYAML==6.0.3"'})
  with self.assertRaises(AssertionError):verify(late)
  for replacement in ('','# python -m pip install "PyYAML==6.0.3"','python -m pip install "PyYAML==6.0.3" || true'):
   bad=copy.deepcopy(workflow)
   for step in bad['jobs']['validate-motion']['steps']:step['run']=step.get('run','').replace('python -m pip install "PyYAML==6.0.3"',replacement)
   with self.assertRaises(AssertionError):verify(bad)
  for flag in (False,None,'always()'):
   bad=copy.deepcopy(workflow)
   for step in bad['jobs']['validate-motion']['steps']:
    if 'PyYAML==' in step.get('run',''):step['if']=flag
   with self.assertRaises(AssertionError):verify(bad)
 def test_svg_axis_text_api_preserves_assertion_and_rejects_missing_hidden_label(self):
  from unittest.mock import Mock
  from test_sac_dpo_labs_browser import assert_visible_loss_axis
  for text,count,visible in [('8.0',1,True),('7.0',1,True),('8.0',0,True),('8.0',1,False)]:
   svg=Mock();svg.text_content.return_value=text;svg.inner_text.side_effect=RuntimeError('Node is not an HTMLElement')
   label=svg.locator.return_value.filter.return_value;label.count.return_value=count;label.is_visible.return_value=visible
   if text=='8.0' and count==1 and visible:assert_visible_loss_axis(svg)
   else:
    with self.assertRaises(AssertionError):assert_visible_loss_axis(svg)
   svg.inner_text.assert_not_called()
  import ast
  tree=ast.parse((R/'scripts/test_sac_dpo_labs_browser.py').read_text())
  main=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='run')
  self.assertTrue(any(isinstance(n,ast.Call) and isinstance(n.func,ast.Name)and n.func.id=='assert_visible_loss_axis' for n in ast.walk(main)))

 def test_missing_yaml_dependency_fails_real_route_test_not_skipped(self):
  import subprocess,sys
  program=r'''
import sys,importlib.abc,unittest
sys.path.insert(0,sys.argv[1])
class NoYaml(importlib.abc.MetaPathFinder):
 def find_spec(self,fullname,path=None,target=None):
  if fullname=='yaml' or fullname.startswith('yaml.'):
   raise ModuleNotFoundError("No module named 'yaml' (intentional dependency negative)")
sys.meta_path.insert(0,NoYaml())
from test_sac_dpo_motion_semantics import ScopedLayoutRegression
suite=unittest.TestSuite([ScopedLayoutRegression('test_actual_future_only_routes_and_required_unconditional_commands')])
result=unittest.TextTestRunner().run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
'''
  result=subprocess.run([sys.executable,'-I','-c',program,str(R/'scripts')],text=True,capture_output=True)
  self.assertEqual(result.returncode,1)
  self.assertIn("No module named 'yaml' (intentional dependency negative)",result.stderr)
  self.assertIn('FAILED (errors=1)',result.stderr)
  self.assertNotIn('skipped=',result.stderr)

if __name__=='__main__':unittest.main()
