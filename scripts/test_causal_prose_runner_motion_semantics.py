"""Keep the pinned causal-prose Chromium environment on its supported OS."""
import copy
from pathlib import Path
import unittest
import yaml
ROOT=Path(__file__).resolve().parents[1]
WORKFLOW=ROOT/'.github/workflows/concept-animation-validation.yml'
TEST='scripts/test_causal_prose_runner_motion_semantics.py'

def check(workflow):
    job=workflow['jobs']['build-docs']
    assert job['runs-on']=='ubuntu-24.04'
    assert 'if' not in job and (job.get('continue-on-error') is None or job.get('continue-on-error') is False)
    steps=job['steps']
    def require(command):
        matches=[(i,s) for i,s in enumerate(steps) if command in [x.strip() for x in s.get('run','').splitlines()]]
        assert len(matches)==1,command
        i,s=matches[0];assert 'if' not in s and (s.get('continue-on-error') is None or s.get('continue-on-error') is False)
        return i
    dependencies=require('pip install -r requirements.txt')
    guard=require('python '+TEST)
    pip=require('python -m pip install "playwright==1.55.0"')
    browser=require('python -m playwright install --with-deps chromium')
    run=require('python scripts/test_causal_inference_prose_browser.py --site-dir site')
    assert dependencies<guard<pip<=browser<run
    uploads=[s for s in steps if s.get('uses','').startswith('actions/upload-artifact@') and s.get('with',{}).get('name')=='causal-prose-browser']
    assert len(uploads)==1
    u=uploads[0];assert u.get('if')=='always()' and u['with']['path']=='artifacts/causal-prose/' and u['with']['if-no-files-found']=='error'
    paths=workflow.get('on',workflow.get(True))['pull_request']['paths'];assert TEST in paths

class RunnerContract(unittest.TestCase):
    def setUp(self):self.w=yaml.safe_load(WORKFLOW.read_text())
    def test_actual_job(self):check(self.w)
    def test_unsupported_or_floating_runners_rejected(self):
        for value in ['ubuntu-latest','ubuntu-26.04','${{ matrix.os }}',None]:
            w=copy.deepcopy(self.w);w['jobs']['build-docs']['runs-on']=value
            with self.assertRaises(AssertionError):check(w)
    def test_original_browser_install_execution_and_artifact_required(self):
        for needle in ['playwright==1.55.0','playwright install --with-deps','test_causal_inference_prose_browser.py','python '+TEST]:
            w=copy.deepcopy(self.w);steps=w['jobs']['build-docs']['steps'];s=next(s for s in steps if needle in s.get('run',''));s['run']='\n'.join(x for x in s['run'].splitlines() if needle not in x)
            with self.assertRaises(AssertionError):check(w)
        w=copy.deepcopy(self.w);w['jobs']['build-docs']['steps']=[s for s in w['jobs']['build-docs']['steps'] if s.get('with',{}).get('name')!='causal-prose-browser']
        with self.assertRaises(AssertionError):check(w)
    def test_conditional_soft_failure_and_only_file_trigger_rejected(self):
        for key,value in [('if',False),('if',None),('continue-on-error',0),('continue-on-error',True),('continue-on-error','${{ true }}')]:
            w=copy.deepcopy(self.w);s=next(s for s in w['jobs']['build-docs']['steps'] if 'python '+TEST in s.get('run',''));s[key]=value
            with self.assertRaises(AssertionError):check(w)
        w=copy.deepcopy(self.w);w.get('on',w.get(True))['pull_request']['paths'].remove(TEST)
        with self.assertRaises(AssertionError):check(w)

if __name__=='__main__':unittest.main()
