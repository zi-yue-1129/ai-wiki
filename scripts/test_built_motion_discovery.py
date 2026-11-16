#!/usr/bin/env python3
"""Browser-free regression tests for the built-motion browser harness."""
from pathlib import Path
import json
import tempfile
from types import SimpleNamespace
import unittest

from test_built_motion_browser import (
    Images, MotionPage, assert_document_fits, check_built_page, check_math_rendering, discover_pages,
    record_failure_diagnostics, source_asset_url,
)

BASE = "https://example.test/ai-wiki/"
IMAGE = ('<img data-source-asset-urls src="../assets/plot-still.svg" '
         'data-motion-src="../assets/plot-motion.svg" alt="Example plot">')


class DiscoveryTests(unittest.TestCase):
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
                 "nestedAssistive": 0, "assistiveMathML": 1, "trackedItems": 1}
        page = SimpleNamespace(evaluate=lambda _js: valid)
        self.assertEqual(check_math_rendering(page), valid)
        for changes, message in [({"nestedAssistive": 1}, "typeset again"),
                                 ({"unrendered": 1}, "unrendered math"),
                                 ({"assistiveMathML": 0}, "missing assistive"),
                                 ({"trackedItems": 0}, "forgotten")]:
            page.evaluate = lambda _js: {**valid, **changes}
            with self.assertRaisesRegex(AssertionError, message):
                check_math_rendering(page)

    def test_diagnostics_error_does_not_replace_original_failure(self):
        def fail(_js):
            raise RuntimeError("page unavailable")
        result = {"status": "failed", "error": "original failure"}
        record_failure_diagnostics(SimpleNamespace(evaluate=fail), self.site, result)
        self.assertEqual(result, {"status": "failed", "error": "original failure",
                                  "overflow_diagnostics_error": "page unavailable"})


if __name__ == "__main__":
    unittest.main()
