"""Review dates must not be inferred from git modification or page length."""
import datetime as dt
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import wiki_status as ws


class ReviewStatusTests(unittest.TestCase):
    def load(self, front='', words=450, commit=dt.date(2026, 11, 16)):
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp)
            path = docs / 'topic.md'
            path.write_text(f'---\n{front}\n---\n# Topic\n' + 'word ' * words)
            with patch.object(ws, 'DOCS', docs), patch.object(ws, 'git_date', return_value=commit):
                return ws.load_page(path)

    def test_complete_does_not_mean_reviewed(self):
        page = self.load()
        self.assertEqual(page.status, 'complete')
        self.assertIsNone(page.last_reviewed)
        self.assertFalse(page.stale)  # unknown is distinct from stale

    def test_typo_commit_cannot_refresh_review(self):
        page = self.load('last_reviewed: 2024-01-01')
        self.assertEqual(page.last_commit, dt.date(2026, 11, 16))
        self.assertEqual(page.last_reviewed, dt.date(2024, 1, 1))
        with patch.object(ws, 'TODAY', dt.date(2026, 11, 16)):
            self.assertTrue(page.stale)

    def test_shorter_review_interval(self):
        page = self.load('last_reviewed: 2026-10-01\nreview_interval_days: 30')
        with patch.object(ws, 'TODAY', dt.date(2026, 11, 16)):
            self.assertTrue(page.stale)
        default = self.load('last_reviewed: 2026-10-01')
        with patch.object(ws, 'TODAY', dt.date(2026, 11, 16)):
            self.assertFalse(default.stale)

    def test_interval_boundary(self):
        page = self.load('last_reviewed: 2026-10-01\nreview_interval_days: 30')
        with patch.object(ws, 'TODAY', dt.date(2026, 10, 31)):
            self.assertFalse(page.stale)

    def test_invalid_date_not_inferred(self):
        self.assertIsNone(self.load('last_reviewed: nonsense').last_reviewed)

    def test_date_requires_date_not_timestamp_or_compact_form(self):
        self.assertIsNone(ws.as_date(dt.datetime(2026, 1, 1)))
        self.assertIsNone(ws.as_date('20260101'))
        self.assertIsNone(ws.as_date('2026-W01-1'))
        self.assertEqual(ws.as_date('2026-01-01'), dt.date(2026, 1, 1))

    def test_report_distinguishes_unknown_and_reviewed(self):
        report = ws.render([self.load(), self.load('last_reviewed: 2024-01-01')], '', '##')
        self.assertIn('**1** pages have no explicit review date', report)
        self.assertIn('not factual verification', report)
        self.assertIn('last reviewed 2024-01-01', report)
        self.assertNotIn('last reviewed 2026-11-16', report)


if __name__ == '__main__':
    unittest.main()
