"""History contract tests; actual same-document/full-page browser runs remain CI."""
import unittest
from unittest.mock import Mock, patch
import test_built_planning_evolution_labs_browser as harness

class HistoryTests(unittest.TestCase):
    def fixture(self):
        page=Mock();host=Mock();group=Mock();page.locator.return_value=host;host.locator.return_value=group
        widgets={name:Mock() for name in ('prev','play','next','seek','speed','reset')}
        widgets['seek'].input_value.return_value='0'
        events=[]
        page.evaluate.side_effect=lambda js:events.append(js)
        def wait(url, *, wait_until):
            self.assertEqual(wait_until,'commit', 'SPA history must not await a nonexistent load event')
            self.assertEqual(len(events),1);self.assertTrue(callable(url));self.assertTrue(url('https://example.test/strips/#restored-section'));events.append('https://example.test/strips/')
        page.wait_for_url.side_effect=wait
        assertions=Mock()
        return page,host,widgets,events,assertions

    def test_same_document_back_and_forward_without_load_event(self):
        for forward in (False,True):
            with self.subTest(forward=forward):
                page,host,widgets,events,checks=self.fixture()
                with patch.object(harness,'controls',return_value=widgets),patch.object(harness,'expect',return_value=checks):
                    self.assertIs(harness.history_lab(page,'https://example.test/strips/','strips',forward=forward),host)
                self.assertEqual(events,['history.forward()' if forward else 'history.back()','https://example.test/strips/'])
                page.go_back.assert_not_called();page.go_forward.assert_not_called()
                widgets['reset'].click.assert_called_once();checks.to_have_value.assert_called_once_with('0')
                self.assertEqual(checks.to_have_count.call_count,8) # host, group, six controls
                page.wait_for_timeout.assert_called_once_with(1100)

    def test_only_fragment_may_differ(self):
        expected='https://example.test/strips/?view=1'
        for actual in (expected,expected+'#section',expected+'#繁體中文'):
            self.assertTrue(harness.same_document_url(actual,expected))
        for actual in ('https://example.test/graphplan/?view=1#section',
                       'https://example.test/strips/?view=2#section',
                       'https://evil.test/strips/?view=1#section',
                       'http://example.test/strips/?view=1#section',
                       'https://example.test:444/strips/?view=1#section',
                       'https://example.test/strips/#section'):
            self.assertFalse(harness.same_document_url(actual,expected),actual)

    def test_real_predicate_rejects_wrong_page_before_controls(self):
        page,host,widgets,events,checks=self.fixture()
        def wait(predicate,**kwargs):
            if not predicate('https://example.test/graphplan/#same-anchor'):
                raise TimeoutError('different document')
        page.wait_for_url.side_effect=wait
        with patch.object(harness,'controls',return_value=widgets),patch.object(harness,'expect',return_value=checks):
            with self.assertRaisesRegex(TimeoutError,'different document'):
                harness.history_lab(page,'https://example.test/strips/','strips')
        widgets['reset'].click.assert_not_called()

    def test_wrong_destination_does_not_validate_stale_controls(self):
        page,host,widgets,events,checks=self.fixture();page.wait_for_url.side_effect=TimeoutError('wrong history destination')
        with patch.object(harness,'controls',return_value=widgets),patch.object(harness,'expect',return_value=checks):
            with self.assertRaisesRegex(TimeoutError,'wrong history destination'):harness.history_lab(page,'expected','strips')
        widgets['reset'].click.assert_not_called()

    def test_duplicate_initialization_is_rejected(self):
        page,host,widgets,events,checks=self.fixture();checks.to_have_count.side_effect=AssertionError('duplicate lab')
        with patch.object(harness,'controls',return_value=widgets),patch.object(harness,'expect',return_value=checks):
            with self.assertRaisesRegex(AssertionError,'duplicate lab'):harness.history_lab(page,'https://example.test/strips/','ga')
        widgets['reset'].click.assert_not_called()

    def test_reset_failure_is_rejected(self):
        page,host,widgets,events,checks=self.fixture();checks.to_have_value.side_effect=AssertionError('reset failed')
        with patch.object(harness,'controls',return_value=widgets),patch.object(harness,'expect',return_value=checks):
            with self.assertRaisesRegex(AssertionError,'reset failed'):harness.history_lab(page,'https://example.test/strips/','ga')

    def test_timer_surviving_history_reset_is_rejected(self):
        page,host,widgets,events,checks=self.fixture();widgets['seek'].input_value.side_effect=['0','1']
        with patch.object(harness,'controls',return_value=widgets),patch.object(harness,'expect',return_value=checks):
            with self.assertRaisesRegex(AssertionError,'kept moving'):harness.history_lab(page,'https://example.test/strips/','ga')

class PipelineTests(unittest.TestCase):
    def validate(self, text):
        import yaml
        data = yaml.load(text, Loader=yaml.BaseLoader)
        commands = [line.strip() for job in data['jobs'].values() for step in job.get('steps', []) for line in step.get('run', '').splitlines()]
        self.assertIn('python scripts/test_planning_evolution_history.py', commands)
        paths = data['on']['pull_request']['paths']
        for filename in ('test_planning_evolution_history.py', 'test_built_planning_evolution_labs_browser.py'):
            self.assertIn('scripts/' + filename, paths)
    def source(self):
        from pathlib import Path
        return (Path(__file__).resolve().parents[1] / '.github/workflows/built-motion-browser.yml').read_text()
    def test_executable_ci_registration(self):
        self.validate(self.source())
    def test_comment_or_missing_command_does_not_count(self):
        with self.assertRaises(AssertionError):
            self.validate(self.source().replace('          python scripts/test_planning_evolution_history.py', '          # python scripts/test_planning_evolution_history.py'))
    def test_missing_path_trigger_is_rejected(self):
        with self.assertRaises(AssertionError):
            self.validate(self.source().replace('      - "scripts/test_planning_evolution_history.py"', ''))

if __name__=='__main__':unittest.main()
