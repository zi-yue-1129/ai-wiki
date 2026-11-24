"""The actual policy-layout/canary regression must execute in CI, not a comment."""
import fnmatch
import unittest
from pathlib import Path
import yaml
ROOT = Path(__file__).resolve().parents[1]
def validate(text):
    data=yaml.load(text, Loader=yaml.BaseLoader)
    lines=[line.strip() for job in data['jobs'].values() for step in job.get('steps',[]) for line in step.get('run','').splitlines()]
    for script in ('test_reinforce_layout_motion_semantics.py','test_policy_history_motion_semantics.py','test_policy_layout_ci_motion_semantics.py'):
        assert 'python scripts/'+script in lines, 'missing executable policy regression'
    for script in ('test_reinforce_layout_motion_semantics.py','test_policy_history_motion_semantics.py','test_policy_layout_ci_motion_semantics.py','test_policy_credit_labs_browser.py'):
        assert any(fnmatch.fnmatch('scripts/'+script,p) for p in data['on']['pull_request']['paths']), 'missing trigger'
class PolicyLayoutCI(unittest.TestCase):
    def source(self):return (ROOT/'.github/workflows/built-motion-browser.yml').read_text()
    def test_registered(self):validate(self.source())
    def test_commented_command_rejected(self):
        with self.assertRaises(AssertionError):validate(self.source().replace('          python scripts/test_reinforce_layout_motion_semantics.py','          # python scripts/test_reinforce_layout_motion_semantics.py'))
    def test_missing_browser_trigger_rejected(self):
        with self.assertRaises(AssertionError):validate(self.source().replace('      - "scripts/test_policy_credit_labs_browser.py"',''))
if __name__=='__main__':unittest.main()
