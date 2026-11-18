"""CF consumer wiring contracts; real cache modes and browser run in CI."""
from pathlib import Path
import unittest
import yaml
ROOT=Path(__file__).resolve().parents[1]
def read(path):return yaml.load((ROOT/path).read_text(),Loader=yaml.BaseLoader)
class CFWorkflowTests(unittest.TestCase):
 def setUp(self):
  self.workflow=read('.github/workflows/item-cf-browser.yml')
  self.job=self.workflow['jobs']['item-cf-browser'];self.steps=self.job['steps']
 def test_original_build_browser_and_upload_retained_without_cache_bypass(self):
  commands=[s.get('run','') for s in self.steps]
  self.assertIn('mkdocs build --strict',commands)
  self.assertIn('python scripts/test_item_cf_browser.py',commands)
  self.assertTrue(any('playwright install --with-deps chromium' in c for c in commands))
  for s in self.steps:
   if 'run' in s:self.assertNotIn('if',s)
   self.assertNotEqual(s.get('continue-on-error'),'true')
  upload=next(s for s in self.steps if s.get('with',{}).get('name')=='item-cf-browser-review')
  self.assertEqual(upload['if'],'always()');self.assertEqual(upload['with']['path'],'artifacts/item-cf-browser/')
  self.assertEqual(self.workflow['permissions'],{'contents':'read'})
 def test_unchanged_verified_helper_mandatory_before_build(self):
  index=next(i for i,s in enumerate(self.steps) if s.get('uses')=='./.github/actions/install-cjk-font')
  font=self.steps[index];self.assertNotIn('if',font);self.assertNotIn('with',font)
  build=next(i for i,s in enumerate(self.steps) if s.get('run')=='mkdocs build --strict')
  self.assertLess(index,build)
  all_text=str(self.steps)
  for forbidden in ['cache-hit','actions/cache/save','allow-unauthenticated','trusted=yes']:
   self.assertNotIn(forbidden,all_text)
  self.assertFalse(any('apt-get' in s.get('run','') for s in self.steps))
 def test_safety_and_consumer_regressions_execute(self):
  command=next(s['run'] for s in self.steps if s.get('name')=='Verify dependency safety and CF workflow contracts')
  self.assertIn('python scripts/test_ci_font_archive.py',command)
  self.assertIn('python scripts/test_ci_item_cf_workflow.py',command)
  self.assertEqual(self.job['runs-on'],'ubuntu-24.04')
  self.assertGreaterEqual(int(self.job['timeout-minutes']),35)
 def test_all_dependency_changes_trigger_real_consumer_and_matrix(self):
  paths=self.workflow['on']['pull_request']['paths']
  for path in ['.github/actions/install-cjk-font/**','scripts/ci_font_archive.py','scripts/test_ci_font_archive.py','scripts/test_ci_item_cf_workflow.py','requirements.txt']:
   self.assertIn(path,paths)
  safety=read('.github/workflows/font-archive-cache.yml')
  for path in ['.github/workflows/item-cf-browser.yml','scripts/test_ci_item_cf_workflow.py']:
   self.assertIn(path,safety['on']['pull_request']['paths'])
  self.assertEqual(set(safety['jobs']['verify']['strategy']['matrix']['mode']),{'auto','miss','disabled','corrupt','fallback'})
  self.assertEqual(safety['jobs']['verify']['strategy']['fail-fast'],'false')
  guard=safety['jobs']['seed-main']['if']
  self.assertIn("github.ref == 'refs/heads/main'",guard)
  self.assertIn("github.event_name == 'push'",guard)
 def test_font_report_survives_failure_without_greenwashing(self):
  s=next(s for s in self.steps if s.get('with',{}).get('name')=='item-cf-font-dependency-report')
  self.assertEqual(s['if'],'always()');self.assertEqual(s['with']['path'],'${{ steps.font.outputs.report }}')
  self.assertNotEqual(s.get('continue-on-error'),'true')
if __name__=='__main__':unittest.main()
