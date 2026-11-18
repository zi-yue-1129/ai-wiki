#!/usr/bin/env python3
"""Offline security regressions for untrusted font archive bytes."""
import hashlib
import re
from pathlib import Path
import tempfile
import unittest
from ci_font_archive import copy_verified, candidate_metadata, validate_cache_directory, install
from unittest.mock import patch
import os
import subprocess
from types import SimpleNamespace

class PayloadTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / 'font.deb'
        self.destination = self.root / 'verified.deb'
        self.content = b'authenticated font fixture\x00' * 100
        self.source.write_bytes(self.content)
        self.meta = dict(size=len(self.content), sha256=hashlib.sha256(self.content).hexdigest())

    def reject(self):
        with self.assertRaises((OSError, ValueError)):
            copy_verified(self.source, self.destination, self.meta)
        self.assertFalse(self.destination.exists())

    def test_valid_payload(self):
        copy_verified(self.source, self.destination, self.meta)
        self.assertEqual(self.destination.read_bytes(), self.content)

    def test_same_size_corruption(self):
        self.source.write_bytes(bytes([self.content[0] ^ 1]) + self.content[1:])
        self.reject()

    def test_truncation(self):
        self.source.write_bytes(self.content[:-1])
        self.reject()

    def test_oversize(self):
        self.source.write_bytes(self.content + b'x')
        self.reject()

    def test_missing(self):
        self.source.unlink()
        self.reject()

    def test_symlink(self):
        other = self.root / 'other'
        self.source.rename(other)
        self.source.symlink_to(other)
        self.reject()

    def test_hardlink(self):
        (self.root / 'other').hardlink_to(self.source)
        self.reject()

    def test_directory(self):
        self.source.unlink()
        self.source.mkdir()
        self.reject()

    def test_fifo(self):
        import os
        self.source.unlink()
        os.mkfifo(self.source)
        self.reject()

    def test_wrong_digest(self):
        self.meta['sha256'] = '0' * 64
        self.reject()

    def test_stale_metadata(self):
        self.meta = dict(size=self.meta['size'], sha256=hashlib.sha256(b'other').hexdigest())
        self.reject()

class CacheBoundaryTests(unittest.TestCase):
    def test_unexpected_entry(self):
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp)
            (p / 'font.deb').write_bytes(b'font')
            (p / 'manifest.json').write_text('{}')
            with self.assertRaises(ValueError):
                validate_cache_directory(p)

    def test_parent_symlink(self):
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp)
            (p / 'real').mkdir()
            (p / 'real' / 'font.deb').write_bytes(b'font')
            (p / 'restore').symlink_to(p / 'real', target_is_directory=True)
            with self.assertRaises(ValueError):
                validate_cache_directory(p / 'restore')

    def test_existing_destination_unchanged(self):
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp)
            (p / 'source').write_bytes(b'font')
            (p / 'destination').write_bytes(b'KEEP')
            with self.assertRaises(FileExistsError):
                copy_verified(p / 'source', p / 'destination', {'size':4, 'sha256':hashlib.sha256(b'font').hexdigest()})
            self.assertEqual((p / 'destination').read_bytes(), b'KEEP')

    def test_metadata_failure_never_installs_or_reads_cache(self):
        with patch('ci_font_archive.metadata', side_effect=RuntimeError('untrusted metadata')), \
             patch('ci_font_archive.run') as command, patch('ci_font_archive.copy_verified') as copy:
            with self.assertRaises(RuntimeError):
                install(Path('cache'), Path('export'), Path('report'))
            command.assert_not_called()
            copy.assert_not_called()

class MetadataTests(unittest.TestCase):
    def candidate(self, **changes):
        origin = SimpleNamespace(archive='noble', trusted=True, origin='Ubuntu', site='archive.ubuntu.com')
        values = dict(origins=[origin], record={'SHA256':'a'*64, 'Size':'123'}, version='1:1.0', architecture='all')
        values.update(changes)
        return SimpleNamespace(**values)

    def test_ubuntu(self):
        self.assertEqual(candidate_metadata(self.candidate())['sha256'], 'a'*64)

    def test_untrusted_duplicate(self):
        candidate = self.candidate()
        candidate.origins.append(SimpleNamespace(archive='noble', trusted=False, origin='Ubuntu', site='evil'))
        with self.assertRaises(RuntimeError):
            candidate_metadata(candidate)

    def test_other_origin(self):
        candidate = self.candidate()
        candidate.origins[0].origin = 'Other'
        with self.assertRaises(RuntimeError):
            candidate_metadata(candidate)

    def test_status_only(self):
        candidate = self.candidate()
        candidate.origins[0].archive = 'now'
        with self.assertRaises(RuntimeError):
            candidate_metadata(candidate)

    def test_missing_hash(self):
        with self.assertRaises(RuntimeError):
            candidate_metadata(self.candidate(record={'Size':'123'}))

    def test_invalid_hash(self):
        with self.assertRaises(RuntimeError):
            candidate_metadata(self.candidate(record={'Size':'123', 'SHA256':'not a hash'}))

    def test_missing_size(self):
        with self.assertRaises(RuntimeError):
            candidate_metadata(self.candidate(record={'SHA256':'a'*64}))

class WorkflowTests(unittest.TestCase):
    def test_original_browser_coverage_retained(self):
        root = Path(__file__).resolve().parents[1]
        workflow = (root / '.github/workflows/built-motion-browser.yml').read_text()
        for command in ['playwright install --with-deps chromium', 'mkdocs build --strict',
                        'test_built_motion_discovery.py', 'test_mathjax_lifecycle.cjs',
                        'test_*motion_semantics.py', 'test_built_motion_browser.py',
                        'test_built_prose_browser.py', 'test_sharpness_geometry_labs_browser.py',
                        'test_adaptive_optimiser_labs_browser.py']:
            self.assertIn(command, workflow)
        timeouts = [int(value) for value in re.findall(r'^    timeout-minutes: ([0-9]+)$', workflow, re.M)]
        self.assertTrue(timeouts, 'Browser job needs an explicit timeout budget')
        self.assertTrue(all(value >= 50 for value in timeouts), 'Full coverage budget must not shrink')
        self.assertNotIn('cache-hit', workflow)

    def test_production_save_guard(self):
        root = Path(__file__).resolve().parents[1]
        action = (root / '.github/actions/install-cjk-font/action.yml').read_text()
        save = action.split('    - name: Save verified archive for sibling pull requests')[1]
        self.assertIn("inputs.save == 'true'", save)
        self.assertIn("inputs.test-key == ''", save)
        self.assertIn("github.ref == 'refs/heads/main'", save)
        self.assertIn("github.event_name == 'push' || github.event_name == 'workflow_dispatch'", save)
        self.assertIn("default: 'false'", action)
        consumer = (root / '.github/workflows/built-motion-browser.yml').read_text()
        self.assertNotIn("save: 'true'", consumer)
        self.assertNotIn('actions/cache/save', consumer)

    def test_refresh_failure_stops_before_dependency_install(self):
        root = Path(__file__).resolve().parents[1]
        action = (root / '.github/actions/install-cjk-font/action.yml').read_text()
        commands = action.split('      run: |', 1)[1].split('    - name:', 1)[0]
        commands = '\n'.join(line[8:] for line in commands.splitlines() if line.strip())
        self.assertIn('APT::Update::Error-Mode=any', commands)
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp)
            sudo = p / 'sudo'
            sudo.write_text('#!/bin/sh\nprintf "%s\\n" "$*" >> "$CALL_LOG"\nexit 23\n')
            sudo.chmod(0o755)
            env = dict(os.environ, PATH=f'{p}:' + os.environ['PATH'], CALL_LOG=str(p / 'calls'))
            result = subprocess.run(['bash', '-e', '-c', commands], env=env)
            self.assertEqual(result.returncode, 23)
            calls = (p / 'calls').read_text().splitlines()
            self.assertEqual(len(calls), 1)
            self.assertIn('update -qq', calls[0])
            self.assertNotIn('install', calls[0])

if __name__ == '__main__':
    unittest.main()
