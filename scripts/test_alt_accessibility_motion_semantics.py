"""Restore original non-whitespace accessible names through the real source parser."""
from pathlib import Path
import unittest
import verify_concept_motion as validator

class AltContract(unittest.TestCase):
    def test_source_parser_rejects_all_blank_names_without_weakening_urls(self):
        page = Path('docs/page.md')
        stem = 'wgan-weight-clip'
        template = ('<img data-source-asset-urls src="assets/concept-animations/{s}-still.svg" '
                    'data-still-src="assets/concept-animations/{s}-still.svg" '
                    'data-motion-src="assets/concept-animations/{s}-motion.svg"{alt}>')
        for alt in (None, '', ' ', '\t', '&#32;&#9;', '&nbsp;'):
            attr = '' if alt is None else f' alt="{alt}"'
            with self.subTest(alt=alt):
                errors = validator.verify_source_pair(page, template.format(s=stem, alt=attr), stem)
                self.assertTrue(any('non-whitespace alt' in e for e in errors), errors)
        for alt in ('Explanation', '  雙語說明  '):
            html = template.format(s=stem, alt=f' alt="{alt}"')
            self.assertEqual(validator.verify_source_pair(page, html, stem), [])
            self.assertTrue(validator.verify_source_pair(page, html.replace('-motion.svg', '-WRONG.svg'), stem))

if __name__ == '__main__':
    unittest.main()
