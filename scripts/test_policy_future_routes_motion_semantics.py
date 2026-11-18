"""Only-file-change CI routing for restored policy suites, units and evidence contracts."""
import copy,fnmatch,json,re,unittest
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1]
COMMON=['scripts/policy_line_clearance.py','scripts/policy_glyph_contract.py','scripts/test_policy_glyph_contract_motion_semantics.py','scripts/test_policy_gradient_motion_browser.py','scripts/test_policy_gradient_restore.py','scripts/test_policy_credit_labs_browser.py','scripts/test_policy_union_motion_semantics.py','scripts/test_policy_history_motion_semantics.py','scripts/test_policy_future_routes_motion_semantics.py','.github/workflows/built-motion-browser.yml']
SHARD=['scripts/fixtures/browser-support-suites.json','scripts/fixtures/built-motion-browser-unsharded-reference.yml','scripts/motion_shard_contract.py','scripts/test_motion_shard_ci.py','scripts/run_motion_shard_support.py','scripts/motion_shard_ci.py','scripts/prepare_browser_artifacts.py','scripts/test_prepare_browser_artifacts.py','scripts/test_ci_font_archive.py','scripts/test_policy_original_gate_motion_semantics.py']
def executable(job,command,allow_always=False):
 assert ('if' not in job or (allow_always and job['if']=='always()')) and (job.get('continue-on-error') is None or job.get('continue-on-error') is False),'Disabled job'
 matches=[s for s in job['steps'] if any(line.strip()==command for line in s.get('run','').splitlines())]
 assert len(matches)==1,'Missing executable '+command
 assert 'if' not in matches[0] and (matches[0].get('continue-on-error') is None or matches[0].get('continue-on-error') is False),'Disabled command'
def validate(workflow,registry=None):
 event=workflow.get('on',workflow.get(True));patterns=event['pull_request']['paths'];shard='support-browser'in workflow['jobs']
 for file in COMMON+(SHARD if shard else []):
  assert any(fnmatch.fnmatchcase(file,p)for p in patterns),'Missing only-change route: '+file
 if shard:
  job=workflow['jobs']['support-browser'];assert 'if' not in job
  executable(job,'python scripts/run_motion_shard_support.py')
  executable(job,'python scripts/test_policy_glyph_contract_motion_semantics.py');executable(job,'python scripts/test_policy_gradient_restore.py');executable(job,'python scripts/test_policy_future_routes_motion_semantics.py')
  executable(job,'python scripts/test_policy_original_gate_motion_semantics.py')
  gate=workflow['jobs']['built-motion-browser'];executable(gate,'python scripts/motion_shard_ci.py gate --receipts shard-receipts --inventory run-inventory.json --shard-count 4',allow_always=True)
  assert 'support-browser' in gate['needs']
  for name,script in [('policy-gradient-motion','test_policy_gradient_motion_browser.py'),('policy-credit-labs','test_policy_credit_labs_browser.py')]:
   entries=[x for x in registry['suites']if x['id']==name];assert len(entries)==1
   assert entries[0]['command']==['scripts/'+script]
   if name=='policy-gradient-motion':assert set(entries[0].get('source_dependencies',[]))=={'scripts/policy_glyph_contract.py','scripts/policy_line_clearance.py'}
 else:
  job=workflow['jobs']['built-motion-browser'];assert 'if' not in job
  for script in ['test_policy_glyph_contract_motion_semantics.py','test_policy_gradient_restore.py','test_policy_gradient_motion_browser.py','test_policy_future_routes_motion_semantics.py']:
   executable(job,'python scripts/'+script)
  executable(job,'POLICY_CREDIT_SITE_DIR=site python scripts/test_policy_credit_labs_browser.py')
  upload=next(s for s in job['steps']if s.get('with',{}).get('name')=='policy-gradient-motion-review')
  assert upload['if']=='always()' and upload['with']['path']=='artifacts/policy-gradient-motion/' and upload['with']['if-no-files-found']=='error'
 return COMMON+(SHARD if shard else [])
class FutureRoutes(unittest.TestCase):
 def data(self):
  workflow=yaml.safe_load((ROOT/'.github/workflows/built-motion-browser.yml').read_text());p=ROOT/'scripts/fixtures/browser-support-suites.json';return workflow,json.loads(p.read_text())if p.exists()else None
 def test_all_only_change_events_reach_real_runner_and_gate(self):validate(*self.data())
 def test_policy_dependency_removal_rejected(self):
  w,r=self.data()
  if r is None:self.skipTest('unsharded workflow has no support registry')
  for dependency in ['scripts/policy_glyph_contract.py','scripts/policy_line_clearance.py']:
   bad=copy.deepcopy(r);entry=next(x for x in bad['suites']if x['id']=='policy-gradient-motion');entry['source_dependencies'].remove(dependency)
   with self.subTest(dependency=dependency),self.assertRaises(AssertionError):validate(w,bad)
 def test_each_missing_trigger_rejected(self):
  w,r=self.data();files=validate(w,r)
  for file in files:
   bad=copy.deepcopy(w);event=bad.get('on',bad.get(True));event['pull_request']['paths']=[p for p in event['pull_request']['paths']if not fnmatch.fnmatchcase(file,p)]
   with self.subTest(file=file),self.assertRaises(AssertionError):validate(bad,r)
 def test_comment_or_disable_actual_commands_rejected(self):
  w,r=self.data();job='support-browser'if 'support-browser'in w['jobs']else'built-motion-browser'
  commands=['python scripts/test_policy_glyph_contract_motion_semantics.py','python scripts/test_policy_gradient_restore.py','python scripts/test_policy_future_routes_motion_semantics.py']
  commands.append('python scripts/run_motion_shard_support.py'if job=='support-browser'else'python scripts/test_policy_gradient_motion_browser.py')
  for command in commands:
   for mode in ['comment','conditional','boolean_false','null','always','continue','continue_zero','continue_expression','job_false','job_null','job_always']:
    bad=copy.deepcopy(w);step=next(s for s in bad['jobs'][job]['steps']if command in s.get('run','').splitlines())
    if mode=='comment':step['run']=step['run'].replace(command,'# '+command)
    elif mode=='conditional':step['if']='false'
    elif mode=='boolean_false':step['if']=False
    elif mode=='null':step['if']=None
    elif mode=='always':step['if']='always()'
    elif mode=='continue':step['continue-on-error']=True
    elif mode=='continue_zero':step['continue-on-error']=0
    elif mode=='continue_expression':step['continue-on-error']='${{ true }}'
    elif mode=='job_null':bad['jobs'][job]['if']=None
    elif mode=='job_always':bad['jobs'][job]['if']='always()'
    else:bad['jobs'][job]['if']=False
    with self.subTest(command=command,mode=mode),self.assertRaises(AssertionError):validate(bad,r)
if __name__=='__main__':unittest.main()
