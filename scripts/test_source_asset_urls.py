#!/usr/bin/env python3
"""Unit tests for the explicit raw-image URL hook; no third-party dependencies."""
from html.parser import HTMLParser
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "hooks"))
from source_asset_urls import MARKER, on_page_content


class Files:
    def __init__(self, paths):
        self.paths = paths

    def get_file_from_path(self, path):
        return SimpleNamespace(url=self.paths[path]) if path in self.paths else None


class Images(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.images = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            self.images.append(dict(attrs))


class SourceAssetURLTests(unittest.TestCase):
    def setUp(self):
        self.chapter = "theory/paradigms/probabilistic/uncertainty-calibration"
        self.paths = {f"assets/figure-{kind}.svg": f"assets/figure-{kind}.svg"
                      for kind in ("motion", "still")}

    def rewrite(self, html, prefix="", suffix="", url=None):
        page = SimpleNamespace(
            file=SimpleNamespace(src_uri=f"{self.chapter}/temperature-scaling{suffix}.md"),
            url=url or f"{prefix}{self.chapter}/temperature-scaling/"
        )
        return on_page_content(html, page, {}, Files(self.paths))

    def test_source_relative_images_rewrite_for_both_languages(self):
        html = '''<img data-source-asset-urls
src="../../../../assets/figure-still.svg?v=1&amp;style=light#panel"
data-motion-src="../../../../assets/figure-motion.svg"
data-still-src="../../../../assets/figure-still.svg"
alt="校準 &amp; confidence &quot;example&quot;" width="640" height="360"/>'''
        for prefix, suffix, depth in (("", "", 5), ("zh-TW/", ".zh-TW", 6)):
            with self.subTest(locale=prefix):
                output = self.rewrite(html, prefix, suffix)
                attrs = Images(output).images[0]
                self.assertEqual(attrs["src"], "../" * depth + "assets/figure-still.svg?v=1&style=light#panel")
                self.assertEqual(attrs["data-motion-src"], "../" * depth + "assets/figure-motion.svg")
                self.assertEqual(attrs["data-still-src"], "../" * depth + "assets/figure-still.svg")
                self.assertEqual(attrs["alt"], '校準 & confidence "example"')
                self.assertEqual((attrs["width"], attrs["height"]), ("640", "360"))
                self.assertNotIn(MARKER, attrs)
                self.assertEqual(self.rewrite(output, prefix, suffix), output)

    def test_unmarked_elements_scripts_comments_and_surrounding_html_unchanged(self):
        untouched = '''<p>Original &amp; text</p>
<img src='../../../../assets/figure-still.svg' data-motion-src="already-built.svg">
<!-- <img data-source-asset-urls src="missing.svg"> -->
<script>const text = '<img data-source-asset-urls src="missing.svg">';</script>
<div data-source-asset-urls data-motion-src="missing.svg">Untouched</div>'''
        self.assertEqual(self.rewrite(untouched), untouched)
        marked = '<img data-source-asset-urls src="../../../../assets/figure-still.svg">'
        output = self.rewrite(untouched + marked + "\n<p>After</p>")
        self.assertTrue(output.startswith(untouched))
        self.assertTrue(output.endswith("\n<p>After</p>"))

    def test_multiple_marked_tags_and_quoted_greater_than(self):
        tag = '<img data-source-asset-urls alt="x > 1" src="../../../../assets/figure-still.svg">'
        output = self.rewrite(tag + "\n<p>middle</p>\n" + tag)
        self.assertEqual(output.count("../../../../../assets/figure-still.svg"), 2)
        self.assertEqual(len(Images(output).images), 2)
        self.assertTrue(all(attrs["alt"] == "x > 1" for attrs in Images(output).images))

    def test_tag_offsets_preserve_unicode_separators_and_crlf(self):
        before = "<p>First\u2028second</p>\r\n"
        tag = '<img data-source-asset-urls src="../../../../assets/figure-still.svg">'
        after = "\r\n<p>After</p>"
        output = self.rewrite(before + tag + after)
        self.assertEqual(output, before +
                         '<img src="../../../../../assets/figure-still.svg">' + after)

    def test_uses_actual_asset_destination_and_flat_page_url(self):
        self.paths["assets/figure-still.svg"] = "assets/renamed.svg"
        output = self.rewrite('<img data-source-asset-urls src="../../../../assets/figure-still.svg">',
                              url=f"zh-TW/{self.chapter}/temperature-scaling.html")
        self.assertEqual(Images(output).images[0]["src"], "../" * 5 + "assets/renamed.svg")

    def test_external_root_relative_inline_and_fragment_urls_unchanged(self):
        for value in ("https://cdn.example.org/image.svg?q=1#part", "/ai-wiki/assets/figure.svg",
                      "//cdn.example.org/image.svg", "data:image/png;base64,AA", "#part"):
            with self.subTest(value=value):
                output = self.rewrite(f'<img data-source-asset-urls src="{value}">')
                self.assertEqual(Images(output).images[0]["src"], value)

    def test_missing_outside_assets_and_empty_sources_fail_loudly(self):
        for value, message in (("../../../../assets/missing.svg", "no built asset"),
                               ("../../../../../outside.svg", "must resolve under docs/assets"),
                               ("", "empty src")):
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, message):
                self.rewrite(f'<img data-source-asset-urls src="{value}">')

    def test_encoded_filename_and_query_fragment(self):
        self.paths["assets/figure a#b.svg"] = "assets/figure%20a%23b.svg"
        output = self.rewrite('<img data-source-asset-urls src="../../../../assets/figure%20a%23b.svg?q=1#panel">')
        self.assertEqual(Images(output).images[0]["src"],
                         "../../../../../assets/figure%20a%23b.svg?q=1#panel")

    def test_repo_opt_ins_keep_github_source_paths_valid(self):
        # Original four uncertainty-calibration users plus the new bilingual
        # REINFORCE/GRPO visuals; future marked assets are allowed as well.
        expected = {f"{self.chapter}/{topic}{suffix}.md"
                    for topic in ("conformal-prediction", "temperature-scaling")
                    for suffix in ("", ".zh-TW")}
        policy = ("theory/paradigms/reinforcement-learning/"
                  "policy-gradient-and-actor-critic")
        expected.update(f"{policy}/{topic}/index{suffix}.md"
                        for topic in ("reinforce", "grpo")
                        for suffix in ("", ".zh-TW"))
        found = set()
        root_assets = (ROOT / "docs" / "assets").resolve()
        for path in (ROOT / "docs").rglob("*.md"):
            html = path.read_text(encoding="utf-8")
            if MARKER not in html:
                continue
            images = [attrs for attrs in Images(html).images if MARKER in attrs]
            if not images:
                continue
            found.add(path.relative_to(ROOT / "docs").as_posix())
            for attrs in images:
                self.assertIn("src", attrs)
                for attribute in ("src", "data-motion-src", "data-still-src"):
                    if attribute not in attrs:
                        continue
                    value = attrs[attribute]
                    parts = urlsplit(value)
                    with self.subTest(chapter=path.as_posix(), attribute=attribute):
                        self.assertFalse(parts.scheme or parts.netloc or parts.path.startswith("/"))
                        target = (path.parent / unquote(parts.path)).resolve()
                        self.assertTrue(target.is_relative_to(root_assets),
                                        f"{path}: {attribute} must remain under docs/assets/")
                        self.assertTrue(target.is_file(),
                                        f"{path}: {attribute} missing source asset {value}")
        self.assertTrue(expected.issubset(found),
                        f"Missing original/new opt-ins: {expected - found}")


if __name__ == "__main__":
    unittest.main()
