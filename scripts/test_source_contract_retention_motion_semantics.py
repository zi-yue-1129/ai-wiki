"""Mutate actual bilingual source in memory; execute the unchanged real main loop."""
import contextlib
import io
import os
from pathlib import Path
import re
import unittest
from unittest.mock import patch
import verify_concept_motion as v
ROOT = Path(__file__).resolve().parents[1]

class PageContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        previous = Path.cwd()
        try:
            os.chdir(ROOT)
            with contextlib.redirect_stdout(io.StringIO()):
                if v.main() != 0:
                    raise AssertionError('Unmodified actual main must pass before mutation checks')
        finally:
            os.chdir(previous)

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
        for stem in v.SOURCE_ALT_CONTRACT_STEMS:
            for suffix in ('.md', '.zh-TW.md'):
                page = ROOT / 'docs' / (v.TOPICS[stem] + suffix)
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
        for stem in v.STATIC_PREVIEW_LINK_STEMS:
            for suffix in ('.md', '.zh-TW.md'):
                page = ROOT / 'docs' / (v.TOPICS[stem] + suffix)
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
