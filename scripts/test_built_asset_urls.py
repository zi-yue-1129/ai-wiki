#!/usr/bin/env python3
"""Dependency-free tests: python scripts/test_built_asset_urls.py."""
from contextlib import redirect_stderr, redirect_stdout
import io
from pathlib import Path
import tempfile
import unittest

from verify_built_asset_urls import check_site, document_url, main


SITE_URL = "https://zi-yue-1129.github.io/ai-wiki/"
FIXTURES = Path(__file__).parent / "fixtures" / "built_asset_urls"


class BuiltAssetURLTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.site = Path(self.temp.name) / "site"
        self.site.mkdir()

    def write(self, path, text="fixture"):
        target = self.site / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
        return target

    def check(self, site_url=SITE_URL):
        return check_site(self.site, site_url)

    def test_directory_and_flat_document_urls(self):
        self.assertEqual(document_url(SITE_URL, Path("index.html")), SITE_URL)
        self.assertEqual(document_url(SITE_URL, Path("chapter/index.html")), SITE_URL + "chapter/")
        self.assertEqual(document_url(SITE_URL, Path("chapter.html")), SITE_URL + "chapter.html")
        self.write("chapter/index.html", '<img src="../assets/figure.svg">')
        self.write("flat.html", '<img src="assets/figure.svg">')
        self.write("assets/figure.svg")
        self.assertEqual(self.check().violations, [])

    def test_pr1031_raw_html_uses_built_page_not_markdown_directory(self):
        page = "theory/math/linear-algebra/svd/index.html"
        html = (FIXTURES / "pr1031-raw-html.html").read_text()
        self.write(page, html)
        for suffix in ("motion", "still"):
            self.write(f"assets/concept-animations/svd-unit-circle-{suffix}.svg")
        failures = self.check().violations
        self.assertEqual(len(failures), 3)
        self.assertEqual({v.reference.attribute for v in failures},
                         {"src", "data-motion-src", "data-still-src"})
        self.assertTrue(all("/ai-wiki/theory/assets/" in v.resolved_url for v in failures))
        self.assertTrue(all("missing built file theory/assets/" in v.reason for v in failures))
        self.write(page, html.replace("../../../assets/", "../../../../assets/"))
        self.assertEqual(self.check().violations, [])

    def test_pr1035_translated_src_passes_but_unrewritten_data_attributes_fail(self):
        page = "zh-TW/theory/math/probability-statistics/maximum-a-posteriori/index.html"
        html = (FIXTURES / "pr1035-translated-attributes.html").read_text()
        self.write(page, html)
        for suffix in ("motion", "still"):
            self.write(f"assets/concept-animations/map-beta-posterior-{suffix}.svg")
        result = self.check()
        self.assertEqual(result.local_references, 3)
        self.assertEqual(len(result.violations), 2)
        self.assertEqual({v.reference.attribute for v in result.violations},
                         {"data-motion-src", "data-still-src"})
        self.assertTrue(all("/ai-wiki/zh-TW/assets/" in v.resolved_url for v in result.violations))
        self.write(page, html.replace('="../../../../assets/', '="../../../../../assets/'))
        self.assertEqual(self.check().violations, [])

    def test_initial_uncertainty_calibration_baseline_both_languages(self):
        # The source-relative raw HTML is valid in GitHub, but not after build.
        chapter = "theory/paradigms/probabilistic/uncertainty-calibration"
        for prefix, parents, bad_target in (("", 5, "theory/assets/"),
                                            ("zh-TW/", 6, "zh-TW/theory/assets/")):
            page = f"{prefix}{chapter}/temperature-scaling/index.html"
            html = ('<img src="../../../../assets/temperature-still.svg" '
                    'data-motion-src="../../../../assets/temperature-motion.svg">')
            self.write(page, html)
            for suffix in ("still", "motion"):
                self.write(f"assets/temperature-{suffix}.svg")
            failures = self.check().violations
            self.assertEqual(len(failures), 2)
            self.assertTrue(all(SITE_URL + bad_target in v.resolved_url for v in failures))
            self.write(page, html.replace("../../../../assets/", "../" * parents + "assets/"))
            self.assertEqual(self.check().violations, [])

    def test_root_relative_same_origin_absolute_and_protocol_relative_urls(self):
        self.write("index.html", '''
<img src="/ai-wiki/assets/figure.svg">
<img src="https://zi-yue-1129.github.io:443/ai-wiki/assets/figure.svg">
<img src="//zi-yue-1129.github.io/ai-wiki/assets/figure.svg">
<img src="/assets/figure.svg">
<img src="/ai-wiki-other/assets/figure.svg">''')
        self.write("assets/figure.svg")
        result = self.check()
        self.assertEqual(result.local_references, 5)
        self.assertEqual(len(result.violations), 2)
        self.assertTrue(all("outside deployment path" in v.reason for v in result.violations))

    def test_site_can_be_deployed_at_origin_root(self):
        self.write("zh-TW/chapter/index.html", '<img src="/assets/figure.svg">')
        self.write("assets/figure.svg")
        self.assertEqual(self.check("https://example.org/").violations, [])

    def test_external_inline_and_non_http_urls_are_not_fetched(self):
        self.write("index.html", '''
<img src="https://cdn.example.org/missing.svg">
<img src="//cdn.example.org/missing.svg">
<img src="data:image/svg+xml,%3Csvg%3E%3C/svg%3E">
<img src="blob:https://zi-yue-1129.github.io/example">
<img src="https://zi-yue-1129.github.io:8443/missing.svg">
<img src="http://zi-yue-1129.github.io/missing.svg">''')
        result = self.check()
        self.assertEqual(result.skipped_references, 6)
        self.assertEqual(result.local_references, 0)
        self.assertEqual(result.violations, [])

    def test_queries_fragments_entities_and_encoded_filenames(self):
        self.write("章節/index.html", '''
<img src="../assets/figure.svg?version=2&amp;mode=light#panel">
<img src="../assets/a%20b%23c%3Fd.svg#part">
<img src="../assets/圖.svg">
<img src="?version=2#same-document">
<img src="#same-document">''')
        for name in ("figure.svg", "a b#c?d.svg", "圖.svg"):
            self.write("assets/" + name)
        self.assertEqual(self.check().violations, [])

    def test_first_base_href_controls_resolution_even_after_image(self):
        self.write("nested/index.html", '''<img src="figure.svg">
<base href="/ai-wiki/assets/"><base href="/wrong/">''')
        self.write("assets/figure.svg")
        self.assertEqual(self.check().violations, [])
        self.write("nested/index.html", '<base href="https://cdn.example.org/"><img src="figure.svg">')
        self.assertEqual(self.check().skipped_references, 1)

    def test_missing_empty_and_malformed_urls_are_actionable(self):
        self.write("index.html", '''<img src="assets/missing.svg?v=1#part">
<img src="">
<img src>
<img src="https://[invalid/image.svg">''')
        failures = self.check().violations
        self.assertEqual(len(failures), 4)
        self.assertEqual(failures[0].reference.line, 1)
        self.assertIn("missing built file assets/missing.svg", str(failures[0]))
        self.assertIn("index.html:1: src=", str(failures[0]))
        self.assertEqual(failures[1].reason, "empty asset URL")
        self.assertEqual(failures[2].reason, "empty asset URL")

    def test_parser_scope_and_first_duplicate_attribute(self):
        self.write("index.html", '''<!-- <img src="missing.svg"> -->
<script>const example = '<img src="missing.svg">';</script>
<a href="missing.html">Ignored link</a><script src="missing.js"></script>
<img srcset="not-checked.svg 1x">
<IMG SRC="assets/figure.svg" SRC="missing.svg"/>
<button data-motion-src="assets/figure.svg" data-still-src="missing.svg"></button>''')
        self.write("assets/figure.svg")
        result = self.check()
        self.assertEqual(result.local_references, 3)
        self.assertEqual(len(result.violations), 1)
        self.assertEqual(result.violations[0].reference.attribute, "data-still-src")

    def test_dot_segments_and_browser_backslashes(self):
        self.write("nested/index.html", r'''<img src="../assets/./figure.svg">
<img src="%2e%2e/assets/figure.svg">
<img src="..\assets\figure.svg">
<img src="https://zi-yue-1129.github.io/ai-wiki/nested/../assets/figure.svg">''')
        self.write("assets/figure.svg")
        self.assertEqual(self.check().violations, [])

    def test_outside_mount_and_symlink_escape_are_not_local_files(self):
        outside = self.site.parent / "outside.svg"
        outside.write_text("fixture")
        (self.site / "escape.svg").symlink_to(outside)
        self.write("index.html", '''<img src="../outside.svg">
<img src="%2e%2e/outside.svg"><img src="escape.svg">''')
        failures = self.check().violations
        self.assertEqual(len(failures), 3)
        self.assertIn("escapes the built site", failures[2].reason)

    def test_empty_or_missing_build_fails_instead_of_passing(self):
        with self.assertRaisesRegex(ValueError, "no built HTML"):
            self.check()
        with self.assertRaisesRegex(ValueError, "does not exist"):
            check_site(self.site / "missing", SITE_URL)

    def test_invalid_deployment_url_fails(self):
        for url in ("/ai-wiki/", "file:///site/", "https://example.org/?q=1",
                    "https://user:pass@example.org/", "https://example.org:bad/"):
            with self.subTest(url=url), self.assertRaises(ValueError):
                self.check(url)

    def test_cli_exit_codes_and_summary(self):
        for html, expected in (("<p>No assets</p>", 0), ('<img src="missing.svg">', 1)):
            self.write("index.html", html)
            stdout, stderr = io.StringIO(), io.StringIO()
            with redirect_stdout(stdout), redirect_stderr(stderr):
                actual = main(["--site-dir", str(self.site), "--site-url", SITE_URL])
            self.assertEqual(actual, expected)
            self.assertIn("Checked 1 HTML files", stdout.getvalue())
            if expected:
                self.assertIn("missing built file missing.svg", stderr.getvalue())
        with redirect_stderr(io.StringIO()):
            self.assertEqual(main(["--site-dir", str(self.site / "absent"),
                                   "--site-url", SITE_URL]), 2)


if __name__ == "__main__":
    unittest.main()
