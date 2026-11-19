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
        matches=[(i,j,s) for i,s in enumerate(steps) for j,line in enumerate(s.get('run','').splitlines()) if command==line.strip()]
        assert len(matches)==1,command
        i,j,s=matches[0];assert 'if' not in s and (s.get('continue-on-error') is None or s.get('continue-on-error') is False)
        return (i,j)
    dependencies=require('pip install -r requirements.txt')
    guard=require('python '+TEST)
    run=require('python scripts/test_causal_inference_prose_browser.py --site-dir site')
    def suppliers(commands):
        return [(i,j) for i,s in enumerate(steps) if 'if' not in s and (s.get('continue-on-error') is None or s.get('continue-on-error') is False)
                for j,line in enumerate(s.get('run','').splitlines()) if line.strip() in commands]
    packages=suppliers(['python -m pip install "playwright==1.55.0"','pip install playwright==1.55.0 Pillow==13.0.0'])
    browsers=suppliers(['python -m playwright install --with-deps chromium'])
    assert dependencies<guard<run
    assert any(dependencies<pip<browser<run for pip in packages for browser in browsers), 'No effective ordered browser dependency supply'

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
            w=copy.deepcopy(self.w);steps=w['jobs']['build-docs']['steps'];
            for s in steps:
                if needle in s.get('run',''):s['run']='\n'.join(x for x in s['run'].splitlines() if needle not in x)
            with self.assertRaises(AssertionError):check(w)
        w=copy.deepcopy(self.w);w['jobs']['build-docs']['steps']=[s for s in w['jobs']['build-docs']['steps'] if s.get('with',{}).get('name')!='causal-prose-browser']
        with self.assertRaises(AssertionError):check(w)
    def test_redundant_suppliers_and_all_invalid_or_only_late_negatives(self):
        install='python -m playwright install --with-deps chromium'
        # An ineffective redundant supplier cannot invalidate a real earlier one.
        for key,value in [('if',False),('if',None),('continue-on-error',True),('continue-on-error',0)]:
            w=copy.deepcopy(self.w);w['jobs']['build-docs']['steps'].append(dict(run=install,**{key:value}));check(w)
            for needle in ['playwright==1.55.0','playwright install --with-deps']:
                w=copy.deepcopy(self.w)
                for step in w['jobs']['build-docs']['steps']:
                    if needle in step.get('run',''):step[key]=value
                with self.assertRaises(AssertionError):check(w)
        w=copy.deepcopy(self.w)
        for step in w['jobs']['build-docs']['steps']:
            if step.get('name') in ['Install built article browser package','Install built article Chromium dependencies']:step['if']=False
        check(w) # The original pip/browser/consumer block remains an effective chain.
        block=next(step for step in w['jobs']['build-docs']['steps'] if 'python -m pip install "playwright==1.55.0"' in step.get('run',''))
        lines=block['run'].splitlines();pi=next(i for i,x in enumerate(lines) if 'pip install "playwright' in x);bi=next(i for i,x in enumerate(lines) if 'playwright install --with-deps' in x)
        lines[pi],lines[bi]=lines[bi],lines[pi];block['run']='\n'.join(lines)
        with self.assertRaises(AssertionError):check(w)
        for transform in [lambda x:'# '+x,lambda x:x+' || true',lambda x:x.replace('1.55.0','1.54.0')]:
            w=copy.deepcopy(self.w)
            for step in w['jobs']['build-docs']['steps']:
                if 'playwright==1.55.0' in step.get('run',''):step['run']='\n'.join(transform(x) for x in step['run'].splitlines())
            with self.assertRaises(AssertionError):check(w)
        w=copy.deepcopy(self.w);steps=w['jobs']['build-docs']['steps']
        installs=[s for s in steps if 'playwright install --with-deps' in s.get('run','')]
        steps[:]=[s for s in steps if s not in installs]+installs
        with self.assertRaises(AssertionError):check(w)

    def test_conditional_soft_failure_and_only_file_trigger_rejected(self):
        for key,value in [('if',False),('if',None),('continue-on-error',0),('continue-on-error',True),('continue-on-error','${{ true }}')]:
            w=copy.deepcopy(self.w);s=next(s for s in w['jobs']['build-docs']['steps'] if 'python '+TEST in s.get('run',''));s[key]=value
            with self.assertRaises(AssertionError):check(w)
        w=copy.deepcopy(self.w);w.get('on',w.get(True))['pull_request']['paths'].remove(TEST)
        with self.assertRaises(AssertionError):check(w)

if __name__=='__main__':unittest.main()
