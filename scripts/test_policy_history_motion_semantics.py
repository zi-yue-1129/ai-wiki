"""Mocked history failures plus source matrix; actual 24 browser cases remain CI."""
import ast
from pathlib import Path
import unittest
from unittest.mock import Mock,patch
import test_policy_credit_labs_browser as harness

class PolicyHistoryTests(unittest.TestCase):
    def fixture(self):
        page=Mock();host=Mock();page.locator.return_value=host
        widgets={s:Mock() for s in ('.pcl-panel','.pcl-controls','.pcl-controls button','.pcl-seek','.pcl-rate','.pcl-preset')}
        host.locator.side_effect=lambda s:widgets[s]
        buttons=[Mock() for _ in range(4)]
        widgets['.pcl-controls button'].nth.side_effect=lambda i:buttons[i]
        widgets['.pcl-seek'].input_value.return_value='0'
        assertions=Mock();events=[]
        page.evaluate.side_effect=lambda js:events.append(js)
        def wait(url,*,wait_until):
            self.assertEqual(wait_until,'commit');self.assertEqual(events,['history.back()']);self.assertTrue(callable(url));self.assertTrue(url('https://example.test/reinforce/#restored-section'));events.append('https://example.test/reinforce/')
        page.wait_for_url.side_effect=wait
        return page,host,widgets,buttons,assertions,events

    def run_helper(self,page,checks):
        with patch.object(harness,'expect',return_value=checks),patch.object(harness,'check_math_rendering') as math,patch.object(harness,'assert_document_fits') as fits:
            host=harness.history_policy_lab(page,'https://example.test/reinforce/','reinforce',320)
            math.assert_called_once_with(page);fits.assert_called_once_with(page,{'width':320})
            return host

    def test_same_document_no_load_but_strict_dom_reset_and_geometry(self):
        page,host,w,b,checks,events=self.fixture()
        self.assertIs(self.run_helper(page,checks),host)
        self.assertEqual(events,['history.back()','https://example.test/reinforce/']);page.go_back.assert_not_called()
        b[3].click.assert_called_once();page.wait_for_timeout.assert_called_once_with(1100)
        self.assertEqual(checks.to_have_count.call_count,11) # host, panel, group, button set, seven controls
        self.assertEqual(checks.to_be_visible.call_count,8)
        checks.to_have_attribute.assert_called_once_with('aria-pressed','false')

    def test_fragment_only_matching_preserves_origin_path_query(self):
        expected='https://example.test/reinforce/?view=1'
        for actual in (expected,expected+'#policy',expected+'#繁體'):
            self.assertTrue(harness.same_document_url(actual,expected))
        for actual in ('https://example.test/grpo/?view=1#policy',
                       'https://example.test/reinforce/?view=2#policy',
                       'https://evil.test/reinforce/?view=1#policy',
                       'http://example.test/reinforce/?view=1#policy',
                       'https://example.test:444/reinforce/?view=1#policy',
                       'https://example.test/reinforce/#policy'):
            self.assertFalse(harness.same_document_url(actual,expected),actual)

    def test_actual_predicate_rejects_stale_topic_before_controls(self):
        p,h,w,b,c,e=self.fixture()
        def wait(predicate,**kwargs):
            if not predicate('https://example.test/grpo/#same-anchor'):
                raise TimeoutError('different document')
        p.wait_for_url.side_effect=wait
        with self.assertRaisesRegex(TimeoutError,'different document'):self.run_helper(p,c)
        b[3].click.assert_not_called()

    def test_wrong_url_rejects_stale_dom(self):
        p,h,w,b,c,e=self.fixture();p.wait_for_url.side_effect=TimeoutError('wrong URL')
        with self.assertRaisesRegex(TimeoutError,'wrong URL'):self.run_helper(p,c)
        b[3].click.assert_not_called()

    def test_duplicate_missing_or_hidden_controls_rejected(self):
        for method in ('to_have_count','to_be_visible'):
            p,h,w,b,c,e=self.fixture();getattr(c,method).side_effect=AssertionError('invalid controls')
            with self.assertRaisesRegex(AssertionError,'invalid controls'):self.run_helper(p,c)
            b[3].click.assert_not_called()

    def test_reset_value_and_timer_negative_cases(self):
        p,h,w,b,c,e=self.fixture();c.to_have_value.side_effect=AssertionError('not reset')
        with self.assertRaisesRegex(AssertionError,'not reset'):self.run_helper(p,c)
        p,h,w,b,c,e=self.fixture();w['.pcl-seek'].input_value.side_effect=['0','1']
        with self.assertRaisesRegex(AssertionError,'kept moving'):self.run_helper(p,c)

    def test_48_union_cases_and_live_timer_navigation_not_replaced(self):
        source=Path(harness.__file__).read_text();tree=ast.parse(source)
        loops=[ast.literal_eval(n.iter) for n in ast.walk(tree) if isinstance(n,ast.For) and isinstance(n.iter,ast.Tuple)]
        for values in [('reinforce','grpo'),('en','zh-TW'),(320,360,390,720,1024,1280),(False,True)]:self.assertIn(values,loops)
        self.assertNotIn('page.go_back(',source)
        self.assertIn("expect(play).to_have_attribute('aria-pressed', 'true')",source)
        self.assertIn('history_policy_lab(page, url, topic, width)',source)
        self.assertIn('check_320_update_negative(page)',source)

if __name__=='__main__':unittest.main()
