"""Unit and workflow contract tests for lossless artifact packaging, not browser mocks."""
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch
import prepare_browser_artifacts as pack


class Packaging(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.source=self.root/'artifacts';self.source.mkdir()
        self.output=self.root/'parts'

    def file(self,path,data=b'abc'):
        p=self.source/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data);return p

    def run_pack(self,**kwargs):
        return pack.prepare(self.source,self.output,roots=['suite'],**kwargs)

    def test_exact_boundary_and_roundtrip(self):
        self.file('suite/a',b'a'*6);self.file('suite/b',b'b'*4);self.file('suite/c',b'c')
        self.file('suite/.hidden',b'')
        r=self.run_pack(limit=10);self.assertEqual([g['raw_bytes'] for g in r['groups']],[10,1])
        self.assertEqual(r['file_count'],4)
        for f in r['files']:
            group='group-'+f['artifact'].rsplit('-',1)[1]
            self.assertEqual((self.output/group/f['artifact_path']).read_bytes(),(self.source/f['path']).read_bytes())
        self.assertEqual(json.loads((self.output/'manifest.json').read_text()),r)

    def test_deterministic_order(self):
        self.file('suite/z',b'zz');self.file('suite/a',b'aa')
        r=self.run_pack(limit=2)
        second=pack.prepare(self.source,self.root/'second',['suite'],limit=2)
        self.assertEqual(r,second)
        self.assertEqual([x['path'] for x in r['files']],['suite/a','suite/z'])

    def test_missing_root_strict(self):
        with self.assertRaisesRegex(ValueError,'Missing root'):self.run_pack()
        self.assertEqual(json.loads((self.output/'manifest.json').read_text())['status'],'failed')

    def test_missing_roots_explicit_manifest(self):
        r=self.run_pack(allow_missing=True)
        self.assertEqual(r['missing_roots'],['suite']);self.assertEqual(r['groups'],[])
        self.assertTrue((self.output/'manifest.json').exists())

    def test_empty_existing_directory(self):
        (self.source/'suite').mkdir();r=self.run_pack()
        self.assertEqual(r['file_count'],0);self.assertEqual(r['missing_roots'],[])

    def test_duplicate_roots(self):
        with self.assertRaisesRegex(ValueError,'Duplicate'):
            pack.inventory(self.source,['suite','suite'],True)

    def test_overlapping_roots(self):
        with self.assertRaisesRegex(ValueError,'overlapping'):
            pack.inventory(self.source,['suite','suite/nested'],True)

    def test_unsafe_root(self):
        for path in ('../elsewhere','/absolute','suite/../other','suite//nested'):
            with self.subTest(path=path),self.assertRaises(ValueError):pack.inventory(self.source,[path],True)

    def test_single_file_over_limit(self):
        self.file('suite/big',b'123')
        with self.assertRaisesRegex(ValueError,'Single file'):self.run_pack(limit=2)
        self.assertFalse(list(self.output.glob('group-*')))

    def test_slot_limit(self):
        self.file('suite/a',b'12');self.file('suite/b',b'34')
        with self.assertRaisesRegex(ValueError,'slots'):self.run_pack(limit=2,max_groups=1)
        self.assertFalse(list(self.output.glob('group-*')))

    def test_exact_slot_count_succeeds(self):
        for i in range(24):self.file(f'suite/{i:02d}',b'x')
        result=self.run_pack(limit=1,max_groups=24)
        self.assertEqual(len(result['groups']),24)
        self.assertEqual(result['file_count'],24)

    def test_source_disappearance_rejected(self):
        self.file('suite/a')
        def remove(src,dst):
            shutil.copyfile(src,dst);src.unlink()
        with self.assertRaisesRegex(ValueError,'Source inventory'):self.run_pack(copy_file=remove)

    def test_bad_limits(self):
        for limit,slots in [(0,24),(10,0),(-1,2)]:
            with self.assertRaises(ValueError):pack.plan({},limit,slots)

    def test_no_mixing_existing_output(self):
        self.output.mkdir();(self.output/'keep').write_text('original')
        with self.assertRaisesRegex(ValueError,'already exists'):self.run_pack()
        self.assertEqual((self.output/'keep').read_text(),'original')

    def test_source_output_overlap(self):
        with self.assertRaisesRegex(ValueError,'overlap'):
            pack.prepare(self.source,self.source/'parts',['suite'])

    def test_file_and_parent_symlinks(self):
        real=self.file('real/file');(self.source/'suite').symlink_to(real.parent,target_is_directory=True)
        with self.assertRaisesRegex(ValueError,'Symlink'):self.run_pack()
        (self.source/'suite').unlink();(self.source/'suite').mkdir();(self.source/'suite/link').symlink_to(real)
        with self.assertRaisesRegex(ValueError,'Symlink'):pack.inventory(self.source,['suite'])

    def test_missing_copy_rejected(self):
        self.file('suite/a')
        with self.assertRaisesRegex(ValueError,'Output inventory'):
            self.run_pack(copy_file=lambda src,dst:None)
        self.assertFalse(list(self.output.glob('group-*')))

    def test_corrupt_copy_rejected(self):
        self.file('suite/a')
        with self.assertRaisesRegex(ValueError,'SHA mismatch'):
            self.run_pack(copy_file=lambda src,dst:dst.write_bytes(b'xyz'))

    def test_source_mutation_rejected(self):
        self.file('suite/a')
        def mutate(src,dst):
            shutil.copyfile(src,dst);src.write_bytes(b'xyz')
        with self.assertRaisesRegex(ValueError,'Source inventory'):self.run_pack(copy_file=mutate)

    def test_duplicate_output_mapping(self):
        self.file('suite/a');files,_=pack.inventory(self.source,['suite'])
        with self.assertRaisesRegex(ValueError,'Duplicate output'):
            pack.verify_outputs(self.output,files,[['suite/a'],['suite/a']])

    def test_omitted_output_mapping(self):
        self.file('suite/a');files,_=pack.inventory(self.source,['suite'])
        with self.assertRaisesRegex(ValueError,'omitted'):
            pack.verify_outputs(self.output,files,[])

    def test_extra_output_rejected(self):
        self.file('suite/a');files,_=pack.inventory(self.source,['suite'])
        (self.output/'group-01/suite').mkdir(parents=True)
        (self.output/'group-01/suite/a').write_bytes(b'abc');(self.output/'extra').write_text('extra')
        with self.assertRaisesRegex(ValueError,'Output inventory'):
            pack.verify_outputs(self.output,files,[['suite/a']])

    def test_workflow_preserves_coverage_and_uploads(self):
        import yaml
        self.assertIn('policy-credit-labs',pack.DEFAULT_ROOTS)
        self.assertIn('built-planning-evolution-labs',pack.DEFAULT_ROOTS)
        self.assertEqual(len(pack.DEFAULT_ROOTS),12)
        root=Path(__file__).resolve().parents[1]
        data=yaml.safe_load((root/'.github/workflows/built-motion-browser.yml').read_text())
        for key in ('full-motion','support-browser'):
            job=data['jobs'][key];self.assertIsInstance(job['timeout-minutes'],int);self.assertGreaterEqual(job['timeout-minutes'],50)
            steps=job['steps']
            if key == 'support-browser':
                # Keep all required numerical motion tests. A 50-min cancellation
                # previously truncated browser support and its evidence manifest.
                self.assertGreaterEqual(job['timeout-minutes'], 90)
                self.assertNotIn('continue-on-error', job)
                numerical=next(s for s in steps if s.get('name') ==
                               'Check available motion numerical semantics')
                self.assertIn('test_*motion_semantics.py', numerical['run'])
            prep=next(s for s in steps if s.get('name')=='Package bounded lossless evidence, including failed cases')
            self.assertEqual(prep['if'],'always()');self.assertNotIn('continue-on-error',prep)
            self.assertIn('--allow-missing-roots',prep['run']);self.assertIn('--artifact-prefix',prep['run'])
            upload=next(s for s in steps if s.get('uses')=='./.github/actions/upload-browser-parts')
            self.assertEqual(upload['if'],'always()')
            receipt=next(s for s in steps if s.get('name')=='Upload small exact-attempt receipt')
            self.assertEqual(receipt['if'],'always()');self.assertEqual(receipt['with']['if-no-files-found'],'error')
        uploads=yaml.safe_load((root/'.github/actions/upload-browser-parts/action.yml').read_text())['runs']['steps']
        self.assertEqual(len(uploads),pack.MAX_GROUPS)
        self.assertEqual(len({s['with']['name'] for s in uploads}),len(uploads))
        for index,s in enumerate(uploads,1):
            self.assertIn('always()',s['if']);self.assertIn('hashFiles(',s['if'])
            self.assertEqual(s['with']['if-no-files-found'],'error')
            self.assertTrue(s['with']['include-hidden-files']);self.assertNotIn('continue-on-error',s)
            self.assertEqual(s['with']['path'],f'browser-artifact-parts/group-{index:02d}/')
        from run_motion_shard_support import commands
        from motion_shard_contract import SUPPORT_SUITES
        self.assertEqual([s for s,_ in commands()],list(SUPPORT_SUITES))
        self.assertIn('--shard-count 4',str(data['jobs']['full-motion']))

    def test_custom_attempt_prefix_is_lossless(self):
        self.file('suite/a')
        result=pack.prepare(self.source,self.output,['suite'],artifact_prefix='motion-123-2-shard-0')
        self.assertEqual(result['artifact_prefix'],'motion-123-2-shard-0')
        self.assertEqual(result['groups'][0]['artifact'],'motion-123-2-shard-0-01')
        self.assertEqual(result['files'][0]['artifact'],'motion-123-2-shard-0-01')


if __name__=='__main__':unittest.main()
