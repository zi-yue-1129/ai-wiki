"""Fail closed on fresh-job imports, not packages left in a developer environment."""
import ast,copy,fnmatch,re,shlex,unittest
from pathlib import Path
import yaml
R=Path(__file__).resolve().parents[1]
COMMAND='python scripts/test_fixture_dependency_motion_semantics.py'
INSTALLS={'playwright':'python -m pip install "playwright==1.55.0"','yaml':'python -m pip install "PyYAML==6.0.3"','numpy':'python -m pip install "numpy==2.5.5"','markdown':'python -m pip install -r requirements.txt','mkdocs':'python -m pip install -r requirements.txt'}
def imports(path,seen=None,env=None):
 env={} if env is None else env
 seen=set() if seen is None else seen
 if path in seen:return set()
 seen.add(path);out=set()
 def eager(node):
  if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)):return
  if isinstance(node,ast.If) and isinstance(node.test,ast.Call) and ast.unparse(node.test.func)=='os.environ.get' and node.test.args and isinstance(node.test.args[0],ast.Constant):
   branch=node.body if env.get(node.test.args[0].value) else node.orelse
   for child in branch:yield from eager(child)
   return
  yield node
  for child in ast.iter_child_nodes(node):yield from eager(child)
 for n in eager(ast.parse(path.read_text())):
  names=[a.name for a in n.names] if isinstance(n,ast.Import) else [n.module] if isinstance(n,ast.ImportFrom) and n.module else []
  for name in names:
   module=name.split('.')[0]
   if module in INSTALLS:out.add(module)
   local=R/'scripts'/(module+'.py')
   if local.is_file():out|=imports(local,seen,env)
 return out

def audit(w):
 job=w['jobs']['validate-motion'];assert 'if' not in job
 assert job.get('continue-on-error') is None or job.get('continue-on-error') is False
 lines=[];environments=[]
 for step in job['steps']:
  if 'if' not in step and (step.get('continue-on-error') is None or step.get('continue-on-error') is False):
   for line in step.get('run','').splitlines():
    lines.append(line.strip());environments.append({**w.get('env',{}),**job.get('env',{}),**step.get('env',{})})
 assert COMMAND in lines
 paths=w.get('on',w.get(True))['pull_request']['paths'];assert any(fnmatch.fnmatchcase('scripts/test_fixture_dependency_motion_semantics.py',p)for p in paths)
 report=[]
 for index,line in enumerate(lines):
  match=re.fullmatch(r'python (scripts/[\w_]+\.py)(?: .*)?',line)
  if not match:continue
  path=R/match[1];assert path.is_file(),path
  # Both imports are required before every source test, including indirect/dynamic native imports.
  required={'playwright','yaml'}|imports(path,env=environments[index])
  for dep in required:
   assert INSTALLS[dep] in lines[:index],(match[1],dep,'not installed earlier in this job')
  report.append({'source':match[1],'required':sorted(required)})
 assert report
 return report
class Dependencies(unittest.TestCase):
 def setUp(self):self.w=yaml.safe_load((R/'.github/workflows/concept-animation-validation.yml').read_text())
 def test_all_actual_python_consumers_have_prior_same_job_dependencies(self):
  report=audit(self.w);self.assertTrue(any(x['source']=='scripts/test_gradient_actual_motion_semantics.py'for x in report))
 def test_removed_commented_conditional_and_softfailed_first_installs_rejected(self):
  for dep in ['playwright','yaml']:
   for mode in ['remove','comment','or-true','if-false','if-null','if-always','coe-true','coe-zero','late']:
    w=copy.deepcopy(self.w);steps=w['jobs']['validate-motion']['steps'];step=next(s for s in steps if INSTALLS[dep] in s.get('run','').splitlines())
    if mode.startswith('if-'):step['if']={'if-false':False,'if-null':None,'if-always':'always()'}[mode]
    elif mode.startswith('coe-'):step['continue-on-error']=True if mode=='coe-true' else 0
    else:
     replacement={'remove':'','comment':'# '+INSTALLS[dep],'or-true':INSTALLS[dep]+' || true','late':''}[mode]
     step['run']=step['run'].replace(INSTALLS[dep],replacement)
     if mode=='late':steps.append({'run':INSTALLS[dep]})
    with self.subTest(dep=dep,mode=mode),self.assertRaises(AssertionError):audit(w)
 def test_enabled_opt_in_built_mode_requires_its_real_transitive_packages(self):
  w=copy.deepcopy(self.w);step=next(s for s in w['jobs']['validate-motion']['steps']if 'python scripts/test_adaptive_optimiser_labs_browser.py' in s.get('run',''))
  step['env']={'ADAPTIVE_SITE_DIR':'site'}
  with self.assertRaises(AssertionError):audit(w)
 def test_own_route_and_unconditional_execution_cannot_disappear(self):
  for mode in ['route','command','if','softfail']:
   w=copy.deepcopy(self.w)
   if mode=='route':
    event=w.get('on',w.get(True));event['pull_request']['paths']=[p for p in event['pull_request']['paths']if not fnmatch.fnmatchcase('scripts/test_fixture_dependency_motion_semantics.py',p)]
   else:
    step=next(s for s in w['jobs']['validate-motion']['steps']if COMMAND in s.get('run','').splitlines())
    if mode=='command':step['run']=step['run'].replace(COMMAND,'# '+COMMAND)
    elif mode=='if':step['if']=False
    else:step['continue-on-error']=True
   with self.subTest(mode=mode),self.assertRaises(AssertionError):audit(w)
if __name__=='__main__':unittest.main()
