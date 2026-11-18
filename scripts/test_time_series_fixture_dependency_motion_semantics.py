"""The prose contract and subsequent MkDocs build need packages in this job."""
import copy,fnmatch,subprocess,sys,unittest
from test_fixture_dependency_motion_semantics import R,audit
import yaml
INSTALL='python -m pip install -r requirements.txt'
COMMAND='python scripts/test_time_series_fixture_dependency_motion_semantics.py'
def check(w):
 audit(w);job=w['jobs']['validate-motion'];lines=[l.strip()for s in job['steps']if 'if'not in s and(s.get('continue-on-error')is None or s.get('continue-on-error')is False)for l in s.get('run','').splitlines()]
 assert COMMAND in lines and INSTALL in lines
 for command in [COMMAND,'python scripts/test_time_series_prose_contract.py','mkdocs build --strict','python scripts/test_time_series_prose_browser.py']:
  assert command in lines and lines.index(INSTALL)<lines.index(command)
 paths=w.get('on',w.get(True))['pull_request']['paths'];assert any(fnmatch.fnmatchcase('scripts/test_time_series_fixture_dependency_motion_semantics.py',p)for p in paths)
class Requirements(unittest.TestCase):
 def test_same_job_requirements_and_original_all_prose_commands(self):check(yaml.safe_load((R/'.github/workflows/concept-animation-validation.yml').read_text()))
 def test_missing_late_commented_conditional_or_softfail_install_is_rejected(self):
  original=yaml.safe_load((R/'.github/workflows/concept-animation-validation.yml').read_text())
  for mode in ['remove','comment','late','or-true','if-false','if-null','coe-true','coe-zero','route','command']:
   w=copy.deepcopy(original);steps=w['jobs']['validate-motion']['steps'];step=next(s for s in steps if INSTALL in s.get('run','').splitlines())
   if mode=='route':
    event=w.get('on',w.get(True));event['pull_request']['paths']=[p for p in event['pull_request']['paths']if not fnmatch.fnmatchcase('scripts/test_time_series_fixture_dependency_motion_semantics.py',p)]
   elif mode=='command':step['run']=step['run'].replace(COMMAND,'# '+COMMAND)
   elif mode.startswith('if-'):step['if']=False if mode=='if-false'else None
   elif mode.startswith('coe-'):step['continue-on-error']=True if mode=='coe-true'else 0
   else:
    step['run']=step['run'].replace(INSTALL,{'remove':'','comment':'# '+INSTALL,'late':'','or-true':INSTALL+' || true'}[mode])
    if mode=='late':steps.append({'run':INSTALL})
   with self.subTest(mode=mode),self.assertRaises(AssertionError):check(w)
 def test_real_contract_import_fails_in_each_missing_package_environment(self):
  for package in ['markdown','mkdocs']:
   program="import sys,importlib.abc;sys.path.insert(0,'scripts')\nclass Missing(importlib.abc.MetaPathFinder):\n def find_spec(self,fullname,path=None,target=None):\n  if fullname.split('.')[0]=="+repr(package)+":raise ModuleNotFoundError('intentional missing '+fullname)\nsys.meta_path.insert(0,Missing())\nimport test_time_series_prose_contract\n"
   result=subprocess.run([sys.executable,'-c',program],cwd=R,capture_output=True,text=True)
   self.assertNotEqual(result.returncode,0);self.assertIn('intentional missing '+package,result.stderr)
if __name__=='__main__':unittest.main()
