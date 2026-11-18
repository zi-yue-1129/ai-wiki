"""Mutate actual bilingual source in memory; execute the unchanged real main loop."""
import contextlib
import io
import json
import os
from pathlib import Path
import re
import unittest
from unittest.mock import patch
import verify_concept_motion as v
ROOT = Path(__file__).resolve().parents[1]
# Reviewed original PR/head/page evidence, independent of the validator under test.
CONTRACTS = json.loads((ROOT / 'scripts/fixtures/deployed-motion-contracts.json').read_text())
EXPECTED_ALT = CONTRACTS['alt']
EXPECTED_PREVIEWS = CONTRACTS['static_preview']
assert len(EXPECTED_ALT) == 26 and len(EXPECTED_PREVIEWS) == 39


class PageContracts(unittest.TestCase):
    def assert_reviewed_scopes(self):
        self.assertEqual(set(v.SOURCE_ALT_CONTRACT_STEMS), set(EXPECTED_ALT))
        self.assertEqual(set(v.STATIC_PREVIEW_LINK_STEMS), set(EXPECTED_PREVIEWS))
        for stem, source in {**EXPECTED_ALT, **EXPECTED_PREVIEWS}.items():
            self.assertEqual('docs/' + v.TOPICS.get(stem, '') + '.md', source['page'])

    @classmethod
    def setUpClass(cls):
        cls().assert_reviewed_scopes()
        previous = Path.cwd()
        try:
            os.chdir(ROOT)
            with contextlib.redirect_stdout(io.StringIO()):
                if v.main() != 0:
                    raise AssertionError('Unmodified actual main must pass before mutation checks')
        finally:
            os.chdir(previous)

    def test_reviewed_scope_cannot_shrink_clear_or_substitute(self):
        for attribute, expected in [('SOURCE_ALT_CONTRACT_STEMS', EXPECTED_ALT), ('STATIC_PREVIEW_LINK_STEMS', EXPECTED_PREVIEWS)]:
            original = set(expected)
            mutations = [('empty', set())]
            for stem in original:
                mutations.append(('delete:' + stem, original - {stem}))
                mutations.append(('replace:' + stem, (original - {stem}) | {'unreviewed-substitute'}))
            for label, mutation in mutations:
                with self.subTest(attribute=attribute, mutation=label):
                    with patch.object(v, attribute, mutation):
                        with self.assertRaises(AssertionError):
                            self.assert_reviewed_scopes()

    def run_main_with_page(self, page, replacement):
        original = Path.read_text
        wanted = page.resolve()
        def read(path, *args, **kwargs):
            return replacement if path.resolve() == wanted else original(path, *args, **kwargs)
        previous = Path.cwd()
        try:
            os.chdir(ROOT)
            with patch.object(Path, 'read_text', read), contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                return v.main()
        finally:
            os.chdir(previous)

    def test_original_empty_and_whitespace_alt_guards_cover_all_bilingual_main_branches(self):
        for stem in EXPECTED_ALT:
            for suffix in ('.md', '.zh-TW.md'):
                page = ROOT / (EXPECTED_ALT[stem]['page'][:-3] + suffix)
                text = page.read_text()
                tags = list(re.finditer(r'<img\b[^>]*>', text))
                target = next(m for m in tags if f'{stem}-still.svg' in m.group())
                for alt in ('', '   ', '\t'):
                    modified, count = re.subn(r'alt="[^"]*"', f'alt="{alt}"', target.group())
                    self.assertEqual(count, 1)
                    mutation = text[:target.start()] + modified + text[target.end():]
                    with self.subTest(stem=stem, locale=suffix, alt=alt):
                        self.assertNotEqual(self.run_main_with_page(page, mutation), 0)

    def test_independent_preview_links_cannot_be_replaced_by_image_or_attributes(self):
        for stem in EXPECTED_PREVIEWS:
            for suffix in ('.md', '.zh-TW.md'):
                page = ROOT / (EXPECTED_PREVIEWS[stem]['page'][:-3] + suffix)
                text = page.read_text()
                pattern = r'(?<!!)\[[^]]+\]\(([^)]+/' + re.escape(stem) + r'-still\.svg)\)'
                matches = list(re.finditer(pattern, text))
                self.assertTrue(matches, (stem, page))
                for replacement in ('', lambda m: '!' + m.group()):
                    mutation = re.sub(pattern, replacement, text)
                    # Keep real still image and both source URLs; deleting the
                    # separately clickable preview must still fail.
                    self.assertIn(f'{stem}-still.svg', mutation)
                    self.assertIn('data-still-src=', mutation)
                    with self.subTest(stem=stem, locale=suffix, replacement=str(replacement)):
                        self.assertNotEqual(self.run_main_with_page(page, mutation), 0)

    def test_clr_original_complete_animation_link_is_independent(self):
        for suffix in ('.md', '.zh-TW.md'):
            page = ROOT / 'docs/theory/optimization' / ('cyclical-learning-rates' + suffix)
            text = page.read_text()
            pattern = r'(?<!!)\[[^]]+\]\(([^)]+/clr-triangular2-sweep-motion\.svg)\)'
            mutation, count = re.subn(pattern, '', text)
            self.assertEqual(count, 1)
            self.assertIn('clr-triangular2-still.svg)', mutation)
            self.assertIn('clr-triangular2-motion.svg)', mutation)
            self.assertNotEqual(self.run_main_with_page(page, mutation), 0)

if __name__ == '__main__':
    unittest.main()
