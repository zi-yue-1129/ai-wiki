#!/usr/bin/env python3
"""Browser-free regression tests for the built-motion browser harness."""
from pathlib import Path
import json
import tempfile
import subprocess
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

from test_built_motion_browser import (
    Images, MotionPage, assert_document_fits, check_built_page, check_math_rendering, discover_pages,
    record_failure_diagnostics, source_asset_url, check_keyboard_scrollers,
    check_math_renderer_canary, MOBILE_PREFLIGHT_NAMES,
)

BASE = "https://example.test/ai-wiki/"
IMAGE = ('<img data-source-asset-urls src="../assets/plot-still.svg" '
         'data-motion-src="../assets/plot-motion.svg" alt="Example plot">')


class DiscoveryTests(unittest.TestCase):
    def test_real_parser_rejects_blank_alt_in_source_and_built_page(self):
        # Source and built values are obtained through actual HTML parsers.
        # Whitespace is not trimmed for matching valid accessible names.
        from markdown import Markdown
        for alt in (None, "", "   ", "\t", "&#32;&#9;", "&nbsp;"):
            with self.subTest(alt=alt):
                attr = "" if alt is None else f' alt="{alt}"'
                html = '<img data-source-asset-urls src="../assets/plot-still.svg" data-motion-src="../assets/plot-motion.svg"' + attr + '>'
                rendered = Markdown().convert(html)
                target = MotionPage("topic/page.md", "en", "topic/page/", "page.html", Images(rendered).images)
                (self.site / "page.html").write_text(rendered.replace("data-source-asset-urls", "").replace('../assets/', '/ai-wiki/assets/'))
                with self.assertRaisesRegex(AssertionError, "non-whitespace alt"):
                    check_built_page(self.site, target, BASE)
        for alt in ("Descriptive name", "  保留完整名稱  "):
            html = f'<img data-source-asset-urls src="../assets/plot-still.svg" data-motion-src="../assets/plot-motion.svg" alt="{alt}">'
            target = MotionPage("topic/page.md", "en", "topic/page/", "page.html", Images(Markdown().convert(html)).images)
            (self.site / "page.html").write_text(html.replace("data-source-asset-urls", "").replace('../assets/', '/ai-wiki/assets/'))
            self.assertEqual(check_built_page(self.site, target, BASE)[0]["alt"], alt)

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.docs, self.site = root / "docs", root / "site"
        self.docs.mkdir()
        self.site.mkdir()
        i18n = SimpleNamespace(docs_structure="suffix", languages=[
            {"locale": "en", "default": True, "build": True},
            {"locale": "zh-TW", "default": False, "build": True},
        ])
        self.config = SimpleNamespace(docs_dir=str(self.docs), site_dir=str(self.site),
                                      use_directory_urls=True,
                                      markdown_extensions=["fenced_code"], mdx_configs={},
                                      plugins={"i18n": SimpleNamespace(config=i18n)})

    def write(self, root, name, text):
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def test_directory_pages_and_translations(self):
        for name in ("chapter/topic.md", "chapter/topic.zh-TW.md"):
            self.write(self.docs, name, IMAGE)
        pages = discover_pages(self.config)
        self.assertEqual([(p.locale, p.url, p.output) for p in pages], [
            ("en", "chapter/topic/", "chapter/topic/index.html"),
            ("zh-TW", "zh-TW/chapter/topic/", "zh-TW/chapter/topic/index.html"),
        ])

    def test_index_and_explicit_default_suffix(self):
        for name in ("deep/chapter/index.en.md", "deep/chapter/index.zh-TW.md"):
            self.write(self.docs, name, IMAGE)
        self.assertEqual([p.url for p in discover_pages(self.config)],
                         ["deep/chapter/", "zh-TW/deep/chapter/"])

    def test_flat_output_uses_configuration(self):
        self.config.use_directory_urls = False
        for name in ("chapter/topic.md", "chapter/topic.zh-TW.md", "index.zh-TW.md"):
            self.write(self.docs, name, IMAGE)
        self.assertEqual([p.output for p in discover_pages(self.config)],
                         ["chapter/topic.html", "zh-TW/chapter/topic.html", "zh-TW/index.html"])

    def test_new_marked_pages_join_without_allowlist(self):
        self.write(self.docs, "chapter/first.md", IMAGE)
        self.assertEqual(len(discover_pages(self.config)), 1)
        self.write(self.docs, "another/new.zh-TW.md", IMAGE + "\n\n" + IMAGE.replace("plot", "other"))
        pages = discover_pages(self.config)
        self.assertEqual(len(pages), 2)
        self.assertEqual(sum(len(page.images) for page in pages), 3)

    def test_comments_code_and_unmarked_images_are_not_discovered(self):
        self.write(self.docs, "chapter/actual.md", IMAGE)
        self.write(self.docs, "chapter/examples.md",
                   f"<!-- {IMAGE} -->\n\n```html\n{IMAGE}\n```\n\n" +
                   IMAGE.replace("data-source-asset-urls ", "") +
                   '\n\n<img data-source-asset-urls src="../assets/static.svg">')
        self.assertEqual([p.source for p in discover_pages(self.config)], ["chapter/actual.md"])

    def test_no_marked_pages_fails_instead_of_passing_zero_cases(self):
        self.write(self.docs, "chapter/unmarked.md", IMAGE.replace("data-source-asset-urls ", ""))
        with self.assertRaisesRegex(AssertionError, "vacuous"):
            discover_pages(self.config)

    def test_disabled_language_is_not_browsed(self):
        self.config.plugins["i18n"].config.languages[1]["build"] = False
        self.write(self.docs, "chapter/topic.md", IMAGE)
        self.write(self.docs, "chapter/topic.zh-TW.md", IMAGE)
        self.assertEqual([p.locale for p in discover_pages(self.config)], ["en"])

    def target(self):
        return MotionPage("chapter/topic.zh-TW.md", "zh-TW", "zh-TW/chapter/topic/",
                          "zh-TW/chapter/topic/index.html", Images(IMAGE).images)

    def test_removed_marker_still_has_a_built_page_target(self):
        target = self.target()
        self.write(self.site, target.output,
                   IMAGE.replace("data-source-asset-urls ", "").replace("../assets/", "../../../assets/"))
        self.assertEqual(check_built_page(self.site, target, BASE), [{
            "alt": "Example plot", "motion": BASE + "assets/plot-motion.svg",
            "still": BASE + "assets/plot-still.svg",
        }])

    def test_unrewritten_translated_data_attribute_is_rejected(self):
        target = self.target()
        html = IMAGE.replace("data-source-asset-urls ", "").replace(
            'src="../assets/plot-still.svg"', 'src="../../../assets/plot-still.svg"')
        self.write(self.site, target.output, html)
        with self.assertRaisesRegex(AssertionError, "data-motion-src"):
            check_built_page(self.site, target, BASE)

    def test_unrewritten_explicit_still_attribute_is_rejected(self):
        target = self.target()
        target.images[0]["data-still-src"] = "../assets/plot-still.svg"
        html = IMAGE.replace("data-source-asset-urls ", "").replace("../assets/", "../../../assets/")
        self.write(self.site, target.output, html.replace("<img", '<img data-still-src="../assets/plot-still.svg"'))
        with self.assertRaisesRegex(AssertionError, "data-still-src"):
            check_built_page(self.site, target, BASE)

    def test_missing_built_output_or_image_fails(self):
        target = self.target()
        with self.assertRaisesRegex(AssertionError, "Missing built page"):
            check_built_page(self.site, target, BASE)
        self.write(self.site, target.output, "<p>Image disappeared</p>")
        with self.assertRaisesRegex(AssertionError, "expected one built image"):
            check_built_page(self.site, target, BASE)

    def test_source_urls_keep_mount_and_encoded_query_fragment(self):
        self.assertEqual(source_asset_url(BASE, "deep/chapter/page.md",
                                         "../../assets/a%20b.svg?v=2#view"),
                         BASE + "assets/a%20b.svg?v=2#view")

    def test_document_overflow_checks_real_viewport_not_figure_width(self):
        page = SimpleNamespace(evaluate=lambda _js: {"inner": 390, "client": 390, "width": 390})
        assert_document_fits(page, {"width": 390})
        page.evaluate = lambda _js: {"inner": 980, "client": 980, "width": 980}
        with self.assertRaisesRegex(AssertionError, "actual viewport mismatch"):
            assert_document_fits(page, {"width": 390})
        page.evaluate = lambda _js: {"inner": 391, "client": 390, "width": 391}
        with self.assertRaisesRegex(AssertionError, "actual viewport mismatch"):
            assert_document_fits(page, {"width": 390})
        page.evaluate = lambda _js: {"inner": 390, "client": 390, "width": 640}
        with self.assertRaisesRegex(AssertionError, "whole-document horizontal overflow"):
            assert_document_fits(page, {"width": 390})

    def test_failure_diagnostics_keep_fractional_bounds_in_artifact(self):
        diagnostic = {"innerWidth": 391, "overflowingTextRanges": [
            {"text": "文字", "rect": {"right": 390.625}}]}
        page = SimpleNamespace(evaluate=lambda _js: diagnostic)
        result = {"status": "failed", "error": "original failure"}
        record_failure_diagnostics(page, self.site, result)
        self.assertEqual(result["error"], "original failure")
        self.assertEqual(result["status"], "failed")
        self.assertEqual(json.loads((self.site / result["overflow_diagnostics"]).read_text()), diagnostic)

    def test_math_rendering_rejects_nested_or_forgotten_assistive_output(self):
        valid = {"sourceRoots": 1, "unrendered": 0, "containers": 1,
                 "nestedAssistive": 0, "assistiveMathML": 1, "trackedItems": 1, "renderedErrors": []}
        page = SimpleNamespace(evaluate=lambda _js: valid)
        self.assertEqual(check_math_rendering(page), valid)
        for changes, message in [({"nestedAssistive": 1}, "typeset again"),
                                 ({"unrendered": 1}, "unrendered math"),
                                 ({"assistiveMathML": 0}, "missing assistive"),
                                 ({"trackedItems": 0}, "forgotten")]:
            page.evaluate = lambda _js: {**valid, **changes}
            with self.assertRaisesRegex(AssertionError, message):
                check_math_rendering(page)

    def test_rendered_errors_rejected_even_when_every_container_count_matches(self):
        valid = {"sourceRoots": 1, "unrendered": 0, "containers": 1,
                 "nestedAssistive": 0, "assistiveMathML": 1, "trackedItems": 1,
                 "renderedErrors": []}
        for tag in ('mjx-merror', 'merror', 'g[data-mml-node=merror]', 'span[data-mjx-error]'):
            state = {**valid, "renderedErrors": [{"tag": tag, "message": "Unknown environment"}]}
            with self.subTest(tag=tag), self.assertRaisesRegex(AssertionError, 'rendered MathJax error'):
                check_math_rendering(SimpleNamespace(evaluate=lambda _: state))

    def test_math_error_guard_inspects_nodes_not_prose_strings(self):
        expressions = []
        valid = {"sourceRoots": 0, "unrendered": 0, "containers": 0,
                 "nestedAssistive": 0, "assistiveMathML": 0, "trackedItems": 0,
                 "renderedErrors": []}
        def evaluate(js):
            expressions.append(js); return valid
        self.assertEqual(check_math_rendering(SimpleNamespace(evaluate=evaluate)), valid)
        rendered_query = expressions[-1]
        for selector in ('mjx-merror', '[data-mjx-error]', 'merror', '[data-mml-node="merror"]'):
            self.assertIn(selector, rendered_query)
        self.assertNotIn('article.textContent', rendered_query)

    def test_renderer_canary_requires_actual_rejection_and_closes_context(self):
        browser = Mock(); context = browser.new_context.return_value
        page = context.new_page.return_value; page.goto.return_value.ok = True
        valid = {"containers": 1, "renderedErrors": []}
        invalid = {"containers": 1, "renderedErrors": [{"tag": "mjx-merror"}]}
        with patch('test_built_motion_browser.check_math_rendering', side_effect=[
                valid, valid, AssertionError(('rendered MathJax error', invalid)), valid]):
            result = check_math_renderer_canary(browser, BASE, self.site)
        self.assertEqual(result['status'], 'passed')
        self.assertEqual(result['invalid_rejected']['containers'], 1)
        context.close.assert_called_once()
        self.assertEqual(page.evaluate.call_count, 3)  # valid -> invalid -> cleared

    def test_renderer_canary_fails_if_invalid_tex_is_accepted(self):
        browser = Mock(); page = browser.new_context.return_value.new_page.return_value
        page.goto.return_value.ok = True
        with patch('test_built_motion_browser.check_math_rendering', return_value={"containers": 1}):
            with self.assertRaisesRegex(AssertionError, 'incorrectly accepted'):
                check_math_renderer_canary(browser, BASE, self.site)
        browser.new_context.return_value.close.assert_called_once()
        report = json.loads((self.site/'math-renderer-canary/report.json').read_text())
        self.assertEqual(report['status'], 'failed')

    def test_mobile_preflight_retains_original_topics_and_adds_shampoo(self):
        self.assertEqual(MOBILE_PREFLIGHT_NAMES, {'t-sne', 'umap', 'minhash-deduplication',
            'data-programming', 'regularized-evolution', 'asam', 'shampoo'})
        self.assertEqual(len(MOBILE_PREFLIGHT_NAMES)*2*2, 28)

    def test_actual_scroll_discovery_javascript(self):
        # Execute the actual Python-embedded JS in Node's DOM-stub contract tests.
        # Real native focus/keyboard/renderer assertions still run separately in CI Chromium.
        subprocess.run(['node', str(Path(__file__).with_name('test_motion_scroll_discovery.cjs'))], check=True)

    def test_diagnostics_error_does_not_replace_original_failure(self):
        def fail(_js):
            raise RuntimeError("page unavailable")
        result = {"status": "failed", "error": "original failure"}
        record_failure_diagnostics(SimpleNamespace(evaluate=fail), self.site, result)
        self.assertEqual(result, {"status": "failed", "error": "original failure",
                                  "overflow_diagnostics_error": "page unavailable"})


class KeyboardScrollTests(unittest.TestCase):
    def fixture(self, width=640):
        region = Mock()
        region.is_visible.return_value = True
        region.evaluate.side_effect = [
            {'clientWidth': 358, 'scrollWidth': width}, None, True, 40, None, 0,
        ]
        page = Mock()
        region.get_attribute.return_value = '0'
        handle = Mock(); handle.as_element.return_value = region
        page.evaluate_handle.return_value.get_properties.return_value = {'0': handle}
        return page, region

    def test_keyboard_scroll_is_measured_and_reset(self):
        page, region = self.fixture()
        result = check_keyboard_scrollers(page)
        self.assertEqual(result, [{'clientWidth': 358, 'scrollWidth': 640, 'afterArrowRight': 40}])
        region.focus.assert_called_once()
        region.press.assert_called_once_with('ArrowRight')
        page.wait_for_function.assert_called_once()
        self.assertIn('scrollLeft > 0', page.wait_for_function.call_args.args[0])

    def test_missing_tabindex_is_a_failure_not_a_filtered_region(self):
        page, region = self.fixture(); region.get_attribute.return_value = None
        with self.assertRaisesRegex(AssertionError, 'lacks tabindex=0'):
            check_keyboard_scrollers(page)
        region.press.assert_not_called()
        page.evaluate_handle.return_value.dispose.assert_called_once()

    def test_unfocusable_region_fails(self):
        page, region = self.fixture()
        region.evaluate.side_effect = [{'clientWidth': 358, 'scrollWidth': 640}, None, False]
        with self.assertRaisesRegex(AssertionError, 'cannot receive focus'):
            check_keyboard_scrollers(page)

    def test_right_edge_screenshot_and_reset_are_both_retained(self):
        page, region = self.fixture()
        region.evaluate.side_effect = [
            {'clientWidth': 358, 'scrollWidth': 640}, None, True, 40, None, 282, None, 0]
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp); result = check_keyboard_scrollers(page, out)
            page.screenshot.assert_called_once_with(path=str(out/'scroll-region-1-right.png'))
        self.assertEqual(result[0]['rightEdge'], 282)
        self.assertEqual(result[0]['rightEdgeScreenshot'], 'scroll-region-1-right.png')

    def test_scroll_settling_and_blur_are_not_skipped(self):
        page, region = self.fixture()
        check_keyboard_scrollers(page)
        calls = [c.args[0] for c in region.evaluate.call_args_list]
        self.assertEqual(sum('stableSince' in js for js in calls), 2)
        self.assertTrue(any('e.blur()' in js and 'scrollTo' in js for js in calls))

    def test_reset_failure_is_not_swallowed(self):
        page, region = self.fixture()
        region.evaluate.side_effect = [
            {'clientWidth': 358, 'scrollWidth': 640}, None, True, 40, None, 2,
        ]
        with self.assertRaisesRegex(AssertionError, 'Scroll region did not reset'):
            check_keyboard_scrollers(page)

    def test_non_overflowing_region_is_not_falsely_reported(self):
        page, region = self.fixture(width=358)
        self.assertEqual(check_keyboard_scrollers(page), [])
        region.press.assert_not_called()

    def test_failed_native_scrolling_is_not_swallowed(self):
        page, _ = self.fixture()
        page.wait_for_function.side_effect = TimeoutError('No native scrolling')
        with self.assertRaisesRegex(TimeoutError, 'No native scrolling'):
            check_keyboard_scrollers(page)


if __name__ == "__main__":
    unittest.main()
