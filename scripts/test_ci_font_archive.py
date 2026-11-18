#!/usr/bin/env python3
"""Offline security regressions for untrusted font archive bytes."""
import hashlib
import contextlib
import copy
import io
import json
import re
import sys
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

def validate_support_execution_link(workflow, registry):
    """Stdlib-only: the font seed runs before pip/dependency installation.

    Trace an unconditional executable step in the support job, not mentions in
    comments/path filters. Its registry must retain every established suite.
    """
    match=re.search(r'^  support-browser:\s*\n(.*?)(?=^  [A-Za-z0-9_-]+:|\Z)',workflow,re.M|re.S)
    if not match:raise ValueError('Missing support job')
    body=match.group(1)
    if re.search(r'^    (?:if|continue-on-error):',body,re.M):raise ValueError('Conditional/optional support job')
    steps=re.split(r'^      - ',body,flags=re.M)[1:]
    executable=[step for step in steps if re.search(r'^        run: python scripts/run_motion_shard_support\.py\s*$',step,re.M)]
    if len(executable)!=1:raise ValueError('Workflow must execute the registry runner exactly once')
    if re.search(r'^        (?:if|continue-on-error):',executable[0],re.M):raise ValueError('Conditional/optional support execution')
    required={
      'keyboard-scroll-preflight':('test_built_motion_browser.py',None),
      'policy-gradient-motion':('test_policy_gradient_motion_browser.py',None),
      'vi-prose':('test_built_prose_browser.py',None),
      'ddim-prose':('test_built_prose_browser.py',None),
      'embedding-pages':('test_built_prose_browser.py',None),
      'sharpness-labs':('test_sharpness_geometry_labs_browser.py','SHARPNESS_SITE_DIR'),
      'adaptive-optimiser-labs':('test_adaptive_optimiser_labs_browser.py','ADAPTIVE_SITE_DIR'),
      'policy-credit-labs':('test_policy_credit_labs_browser.py','POLICY_CREDIT_SITE_DIR'),
      'built-planning-evolution-labs':('test_built_planning_evolution_labs_browser.py','PLANNING_EVOLUTION_SITE_DIR')}
    entries=registry.get('suites',[]);ids=[x['id'] for x in entries]
    if len(ids)!=len(set(ids)):raise ValueError('Duplicate suite')
    by_id={x['id']:x for x in entries}
    for name,(script,env) in required.items():
        if name not in by_id:raise ValueError('Missing required suite: '+name)
        entry=by_id[name];cmd=entry.get('command',[])
        if not cmd or cmd[0]!='scripts/'+script:raise ValueError('Wrong executable for '+name)
        if env and entry.get('env',{}).get(env)!='site':raise ValueError('Lab no longer tests built site: '+name)
    if '--keyboard-preflight' not in by_id['keyboard-scroll-preflight']['command']:raise ValueError('Missing complete preflight')
    for name in ('keyboard-scroll-preflight','vi-prose','embedding-pages','ddim-prose'):
        cmd=by_id[name]['command']
        if '--output' not in cmd or cmd[cmd.index('--output')+1]!='artifacts/'+name:raise ValueError('Wrong support output root')
    return entries

class WorkflowTests(unittest.TestCase):
    def test_original_browser_coverage_retained(self):
        root = Path(__file__).resolve().parents[1]
        workflow = (root / '.github/workflows/built-motion-browser.yml').read_text()
        for command in ['playwright install --with-deps chromium', 'mkdocs build --strict',
                        'test_built_motion_discovery.py', 'test_mathjax_lifecycle.cjs',
                        'test_*motion_semantics.py', 'test_built_motion_browser.py',
                        'test_built_prose_browser.py']:
            self.assertIn(command, workflow)
        jobs = dict(re.findall(r'^  ([a-z][a-z-]*):\n(.*?)(?=^  [a-z][a-z-]*:|\Z)', workflow.split('jobs:', 1)[1], re.M | re.S))
        for name, minimum in [('full-motion', 50), ('support-browser', 50), ('built-motion-browser', 30)]:
            timeout = re.search(r'^    timeout-minutes: ([0-9]+)$', jobs[name], re.M)
            self.assertIsNotNone(timeout, f'{name} needs an explicit timeout budget')
            self.assertGreaterEqual(int(timeout[1]), minimum, f'{name} budget must not shrink')
        self.assertNotIn('cache-hit', workflow)
        registry=json.loads((root/'scripts/fixtures/browser-support-suites.json').read_text())
        validate_support_execution_link(workflow,registry)

    def test_support_link_rejects_removed_runner_comment_or_conditional(self):
        root=Path(__file__).resolve().parents[1]
        workflow=(root/'.github/workflows/built-motion-browser.yml').read_text()
        registry=json.loads((root/'scripts/fixtures/browser-support-suites.json').read_text())
        command='        run: python scripts/run_motion_shard_support.py'
        mutations=[workflow.replace(command,'        # run: python scripts/run_motion_shard_support.py'),
                   workflow.replace(command,command+'\n        if: false'),
                   workflow.replace(command,command+'\n        continue-on-error: true'),
                   workflow.replace('  support-browser:', '  unrelated-job:'),
                   workflow.replace('  support-browser:', '  support-browser:\n    if: false')]
        for changed in mutations:
            with self.subTest(workflow=changed[-60:]):
                with self.assertRaises(ValueError):validate_support_execution_link(changed,registry)

    def test_support_link_rejects_each_missing_or_wrong_suite(self):
        root=Path(__file__).resolve().parents[1]
        workflow=(root/'.github/workflows/built-motion-browser.yml').read_text()
        registry=json.loads((root/'scripts/fixtures/browser-support-suites.json').read_text())
        for index in range(len(registry['suites'])):
            removed=copy.deepcopy(registry);removed['suites'].pop(index)
            with self.assertRaises(ValueError):validate_support_execution_link(workflow,removed)
            changed=copy.deepcopy(registry);changed['suites'][index]['command'][0]='scripts/unrelated.py'
            with self.assertRaises(ValueError):validate_support_execution_link(workflow,changed)
        for name in ('SHARPNESS_SITE_DIR','ADAPTIVE_SITE_DIR','POLICY_CREDIT_SITE_DIR','PLANNING_EVOLUTION_SITE_DIR'):
            changed=copy.deepcopy(registry)
            for entry in changed['suites']:entry.get('env',{}).pop(name,None)
            with self.assertRaises(ValueError):validate_support_execution_link(workflow,changed)

    def test_actual_runner_executes_every_registered_command_and_keeps_failure(self):
        import run_motion_shard_support as runner
        root=Path(__file__).resolve().parents[1]
        registry=json.loads((root/'scripts/fixtures/browser-support-suites.json').read_text())
        validate_support_execution_link((root/'.github/workflows/built-motion-browser.yml').read_text(),registry)
        # Run the real coordinator with only process launch replaced; no browser/deps
        # are required by this offline font safety job. A failing middle suite cannot
        # silently skip later suites or produce a passing execution receipt.
        for failed_index in (None,2):
            with tempfile.TemporaryDirectory() as directory:
                previous=Path.cwd();calls=[]
                def run(command,env):
                    calls.append((command,env));return SimpleNamespace(returncode=17 if len(calls)-1==failed_index else 0)
                try:
                    os.chdir(directory)
                    with patch.object(runner,'support_registry',return_value=registry),patch.object(runner,'identity',return_value={'test':'offline'}),patch.object(runner.subprocess,'run',side_effect=run),contextlib.redirect_stdout(io.StringIO()):
                        code=runner.main()
                    report=json.loads(Path('artifacts/support-execution/report.json').read_text())
                finally:os.chdir(previous)
                self.assertEqual(len(calls),len(registry['suites']))
                for entry,(command,env) in zip(registry['suites'],calls):
                    self.assertEqual(command,[sys.executable,*entry['command']])
                    for key,value in entry.get('env',{}).items():self.assertEqual(env[key],value)
                self.assertEqual([x['suite'] for x in report['suites']],[x['id'] for x in registry['suites']])
                self.assertEqual(code,0 if failed_index is None else 1)
                self.assertEqual(report['status'],'passed' if failed_index is None else 'failed')

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
