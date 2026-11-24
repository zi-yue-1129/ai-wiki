"""Support's dynamic source discovery must have its own numerical runtime."""
import ast,contextlib,copy,fnmatch,io,subprocess,sys,unittest
from pathlib import Path
from unittest.mock import patch
import yaml
R=Path(__file__).resolve().parents[1]
PIN='python -m pip install "numpy==2.5.5"'
OPENVLA='scripts/test_openvla_actual_motion_semantics.py'
SELF='scripts/test_support_numpy_motion_semantics.py'
def code_of(step):
 run=step.get('run','');assert "python - <<'PYTHON'\n" in run
 return run.split("python - <<'PYTHON'\n",1)[1].rsplit('\nPYTHON',1)[0]
def replay(code,runner=None):
 calls=[]
 def run(args,**kw):
  assert kw.get('check') is True,'Discovery cannot mask failed source tests'
  assert len(args)==2 and args[0]==sys.executable,args
  calls.append(str(args[1]))
  if runner:runner(args,kw)
 with patch('subprocess.run',side_effect=run),contextlib.redirect_stdout(io.StringIO()):exec(compile(code,'<actual support discovery>','exec'),{})
 return calls

def valid(step):return 'if'not in step and(step.get('continue-on-error')is None or step.get('continue-on-error')is False)
def verify(w):
 job=w['jobs']['support-browser'];assert valid(job)
 steps=job['steps'];discovery=[(i,s)for i,s in enumerate(steps)if 'Path("scripts").glob("test_*motion_semantics.py")'in s.get('run','')];assert len(discovery)==1
 index,consumer=discovery[0];assert valid(consumer)
 suppliers=[i for i,s in enumerate(steps)if valid(s)and PIN in [x.strip()for x in s.get('run','').splitlines()]]
 assert suppliers and min(suppliers)<index,'Support cannot inherit NumPy from another job'
 calls=replay(code_of(consumer));expected=[str(p)for p in sorted(Path('scripts').glob('test_*motion_semantics.py'))]
 assert calls==expected and OPENVLA in calls and SELF in calls,'Original dynamic source coverage must remain complete'
 paths=w.get('on',w.get(True))['pull_request']['paths']
 for path in [SELF,OPENVLA]:assert any(fnmatch.fnmatchcase(path,p)for p in paths)
 return code_of(consumer)
class SupportNumpy(unittest.TestCase):
 def setUp(self):self.w=yaml.safe_load((R/'.github/workflows/built-motion-browser.yml').read_text())
 def test_actual_job_dynamic_discovery_has_own_pinned_dependency(self):verify(self.w)
 def test_missing_late_masked_or_other_job_only_install_is_rejected(self):
  for mode in ['delete','comment','unpin','or-true','if-false','if-null','soft-true','soft-zero','late','other-job']:
   w=copy.deepcopy(self.w);steps=w['jobs']['support-browser']['steps'];providers=[s for s in steps if PIN in s.get('run','').splitlines()];assert providers
   for s in providers:
    if mode.startswith('if-'):s['if']=False if mode=='if-false'else None
    elif mode.startswith('soft-'):s['continue-on-error']=True if mode=='soft-true'else 0
    else:s['run']=s['run'].replace(PIN,{'delete':'','comment':'# '+PIN,'unpin':'python -m pip install numpy','or-true':PIN+' || true','late':'','other-job':''}[mode])
   if mode=='late':steps.append({'run':PIN})
   if mode=='other-job':w['jobs']['unrelated']={'steps':[{'run':PIN}]}
   with self.subTest(mode=mode),self.assertRaises(AssertionError):verify(w)
 def test_discovery_cannot_drop_openvla_or_ignore_subprocess_failure(self):
  code=verify(self.w)
  for bad in [code.replace('check=True','check=False'),code.replace('print(f"Running {test}", flush=True)','if test.name=="test_openvla_actual_motion_semantics.py":continue')]:
   with self.assertRaises(AssertionError):
    calls=replay(bad);assert OPENVLA in calls
  for mode in ['if','softfail','route']:
   w=copy.deepcopy(self.w)
   if mode=='route':
    event=w.get('on',w.get(True));event['pull_request']['paths']=[p for p in event['pull_request']['paths']if not fnmatch.fnmatchcase(SELF,p)]
   else:
    s=next(s for s in w['jobs']['support-browser']['steps']if 'test_*motion_semantics.py'in s.get('run',''));s['if'if mode=='if'else'continue-on-error']=False if mode=='if'else True
   with self.assertRaises(AssertionError):verify(w)
 def test_actual_discovery_propagates_real_missing_numpy_import(self):
  code=verify(self.w);realrun=subprocess.run
  program="import sys,importlib.abc;sys.path.insert(0,sys.argv[1])\nclass Missing(importlib.abc.MetaPathFinder):\n def find_spec(self,fullname,path=None,target=None):\n  if fullname.split('.')[0]=='numpy':raise ModuleNotFoundError('intentional support missing numpy')\nsys.meta_path.insert(0,Missing())\nimport test_openvla_actual_motion_semantics\n"
  def runner(args,kw):
   if str(args[1])==OPENVLA:
    result=realrun([sys.executable,'-I','-c',program,str(R/'scripts')],capture_output=True,text=True)
    self.assertNotEqual(result.returncode,0);self.assertIn('intentional support missing numpy',result.stderr)
    raise subprocess.CalledProcessError(result.returncode,args,stderr=result.stderr)
  with self.assertRaises(subprocess.CalledProcessError):replay(code,runner)
if __name__=='__main__':unittest.main()
