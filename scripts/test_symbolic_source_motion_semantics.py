"""Source fallback and repaired mathematical notation contracts."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class SymbolicSource(unittest.TestCase):
    def test_bilingual_assets_and_negated_literals(self):
        for topic in ['search/ida-star', 'theorem-proving/resolution']:
            for lang in ['', '.zh-TW']:
                source = (ROOT / f'docs/theory/paradigms/symbolic-ai/{topic}{lang}.md').read_text()
                self.assertIn('<img data-source-asset-urls', source)
                self.assertIn('data-still-src=', source)
                self.assertIn('data-motion-src=', source)
                self.assertIn('tabindex="0"', source)
                self.assertNotIn('\neg ', source)  # Accidental newline + 'eg'.
                if topic.endswith('resolution'):
                    self.assertIn(r'\neg p\lor q', source)
                    self.assertIn(r'\neg q', source)


if __name__ == '__main__':
    unittest.main()
