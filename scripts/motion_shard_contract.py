"""Deterministic full-coverage partition and fail-closed browser evidence contract."""
from policy_glyph_contract import validate_glyph_sample
from dataclasses import asdict
import hashlib
import json
import os
from pathlib import PurePosixPath
import subprocess

SCHEMA = 1
MODES = ('no-preference', 'reduce')

def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))

def sha(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()

def identity():
    checkout = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
    return {'checkout': checkout,
            'tree': subprocess.check_output(['git', 'rev-parse', 'HEAD^{tree}'], text=True).strip(),
            'event_head': os.environ.get('PR_HEAD_SHA') or checkout,
            'run_id': os.environ.get('GITHUB_RUN_ID', 'local'),
            'run_attempt': os.environ.get('GITHUB_RUN_ATTEMPT', 'local')}

def case_id(source, viewport, mode):
    return canonical([source, viewport['width'], viewport['height'], mode])

def manifest(pages, viewports, provenance):
    pages = sorted([asdict(p) if not isinstance(p, dict) else p for p in pages], key=lambda p: p['source'])
    if not pages or len({p['source'] for p in pages}) != len(pages):
        raise ValueError('Empty or duplicate page discovery')
    cases = sorted(case_id(p['source'], v, m) for p in pages for v in viewports.values() for m in MODES)
    if len(set(cases)) != len(cases):
        raise ValueError('Duplicate expected case IDs')
    data = {'schema': SCHEMA, 'identity': provenance, 'pages': pages,
            'viewports': viewports, 'expected_case_ids': cases}
    return {**data, 'sha256': sha(data)}

def partition(expected, index, count):
    if type(count) is not int or type(index) is not int or count < 1 or not 0 <= index < count:
        raise ValueError('Invalid shard index/count')
    if len(expected) != len(set(expected)) or not expected:
        raise ValueError('Empty/duplicate full expected coverage')
    selected = sorted(expected)[index::count]
    if not selected:
        raise ValueError('Empty shard is not a passing browser run')
    return selected

def require(condition, message):
    if not condition:
        raise ValueError(message)

def validate_manifest(actual, expected):
    require(actual == expected, 'Different identity, discovery manifest or expected cases')
    require(actual.get('sha256') == sha({k:v for k,v in actual.items() if k != 'sha256'}), 'Invalid manifest digest')

def validate_canary(report, files, root):
    canary = report.get('math_renderer_canary', {})
    require(canary.get('status') == 'passed', 'Missing/failed actual renderer canary')
    require(canary.get('scope') == 'isolated actual MathJax renderer canary', 'Wrong canary scope')
    for name in ('valid', 'cleared'):
        state = canary.get(name, {})
        require(state.get('containers') == 1 and state.get('unrendered') == 0
                and state.get('nestedAssistive') == 0 and state.get('renderedErrors') == [],
                'Valid/cleared canary render not proven')
    invalid = canary.get('invalid_rejected', {})
    require(invalid.get('containers', 0) > 0 and bool(invalid.get('renderedErrors')),
            'Invalid renderer output was not rejected')
    path = root + '/math-renderer-canary/report.json'
    require(path in files and files[path]['sha256'] == report_digest(canary), 'Missing/mismatched canary report')
    require(root + '/math-renderer-canary/invalid-rendered-error.png' in files, 'Missing canary screenshot')


def validate_lazy_canary(report, files, root):
    canary = report.get('lazy_image_canary', {})
    require(canary.get('status') == 'passed' and canary.get('scope') == 'isolated native lazy image canary',
            'Missing/failed native lazy image canary')
    before, after = canary.get('before_scroll', {}), canary.get('after_scroll', {})
    require(before.get('top', 0) > 10000 and before.get('naturalWidth') == 0,
            'Native lazy image was not deferred before scroll')
    require(after.get('complete') is True and after.get('naturalWidth') == 640
            and after.get('naturalHeight') == 360, 'Native lazy image not decoded after scroll')
    require(canary.get('broken_rejected') is True, 'Broken image was not rejected')
    path = root + '/lazy-image-canary/report.json'
    require(path in files and files[path]['sha256'] == report_digest(canary), 'Missing/mismatched lazy canary report')
    require(root + '/lazy-image-canary/loaded-after-scroll.png' in files, 'Missing lazy canary screenshot')


def validate_scroll_evidence(case, files, root, used):
    require('keyboard_scroll' in case, 'Missing scroll discovery evidence')
    for bounds in case['keyboard_scroll']:
        require(bounds['scrollWidth'] > bounds['clientWidth'] + 2 and bounds['afterArrowRight'] > 0,
                'Unproven overflowing-region keyboard movement')
        require(bounds.get('rightEdge', -1) >= bounds['scrollWidth'] - bounds['clientWidth'] - 1,
                'Right edge not reached')
        filename = bounds.get('rightEdgeScreenshot', '')
        require(filename and PurePosixPath(filename).name == filename, 'Missing/unsafe right-edge screenshot')
        path = root + '/' + case['artifact_directory'] + '/' + filename
        require(path in files and path not in used, 'Missing/reused right-edge screenshot')
        used.add(path)

def validate_cases(report, expected, scope='full'):
    require(report.get('status') == 'passed' and report.get('scope') == scope, 'Suite not passed/full browser execution')
    observed = []
    for case in report.get('cases', []):
        derived = case_id(case['source'], case['viewport'], case['reduced_motion'])
        require(case.get('case_id') == derived, 'Case ID does not match observed dimensions/motion/source')
        require(case.get('status') == 'passed' and not case.get('errors') and not case.get('page_errors') and not case.get('failed_requests'), 'Failed browser case')
        require(case.get('images'), 'Case has no tested images')
        for image in case['images']:
            require(set(image.get('states', {})) == {'initial', 'paused', 'replayed'}, 'Missing image-state screenshots')
            for state in image['states'].values():
                require(bool(state.get('screenshot')), 'Missing screenshot reference')
        observed.append(derived)
    require(len(observed) == len(set(observed)), 'Duplicate case')
    require(set(observed) == set(expected), 'Missing or extra cases')
    return observed

def validate_pack(pack, artifact_rows, prefix):
    require(pack.get('status') == 'passed' and not pack.get('missing_roots'), 'Incomplete lossless packaging')
    require(pack.get('artifact_prefix') == prefix, 'Wrong artifact prefix/run attempt')
    groups = pack.get('groups', []);files = pack.get('files', [])
    require(groups and files and len(groups)<=24, 'Empty/oversized artifact inventory')
    for i,g in enumerate(groups,1):
        require(g['artifact']==f'{prefix}-{i:02d}' and g['directory']==f'group-{i:02d}','Noncanonical group mapping')
    require(len({g['artifact'] for g in groups}) == len(groups), 'Duplicate artifact groups')
    require(len({f['path'] for f in files}) == len(files), 'Duplicate packed file')
    expected_names = {g['artifact'] for g in groups}
    rows = [a for a in artifact_rows if a['name'].startswith(prefix + '-') and not a['name'].endswith('-receipt')]
    require(len(rows) == len(expected_names) and {a['name'] for a in rows} == expected_names, 'Missing, duplicate or extra group artifacts')
    for a in rows:
        require(not a.get('expired') and a.get('size_in_bytes', 0) > 0 and a.get('id'), 'Expired/empty artifact')
    for f in files:
        p=PurePosixPath(f['path'])
        require(not p.is_absolute() and '..' not in p.parts and f['artifact_path'] == f['path'], 'Unsafe packed path')
        require(f['artifact'] in expected_names and f['size'] >= 0 and len(f['sha256']) == 64 and all(c in '0123456789abcdef' for c in f['sha256']), 'Invalid packed file')
    for g in groups:
        selected = [f for f in files if f['artifact'] == g['artifact']]
        require(g['raw_bytes'] == sum(f['size'] for f in selected) <= 100*1024*1024, 'Artifact bound/size mismatch')
        require(g['file_count'] == len(selected) > 0, 'Artifact file-count mismatch')
    require(pack['file_count'] == len(files) and pack['raw_bytes'] == sum(f['size'] for f in files), 'Pack totals mismatch')
    return {f['path']: f for f in files}

def validate_shards(expected, receipts, count, artifact_rows):
    require(len(receipts) == count, 'Missing or extra shard receipts')
    seen_indices = set();observed = []
    for receipt in receipts:
        validate_manifest(receipt['manifest'], expected)
        report=receipt['report'];index=report.get('shard_index')
        require(report_digest(report)==receipt['report_file_sha256'],'Report receipt digest mismatch')
        require(type(index) is int and index not in seen_indices, 'Duplicate/invalid shard index')
        require(report.get('shard_count') == count, 'Wrong shard count')
        seen_indices.add(index)
        require(report.get('identity') == expected['identity'] and report.get('manifest_sha256') == expected['sha256'], 'Wrong report head/tree/run/attempt/discovery')
        observed += validate_cases(report, partition(expected['expected_case_ids'], index, count))
        ident=expected['identity'];prefix=f"motion-{ident['run_id']}-{ident['run_attempt']}-shard-{index}"
        files=validate_pack(receipt['pack'],artifact_rows,prefix)
        require('built-motion-browser/report.json' in files,'Missing packed report')
        require('built-motion-browser/discovery-manifest.json' in files and files['built-motion-browser/discovery-manifest.json']['sha256']==report_digest(receipt['manifest']),'Packed discovery manifest mismatch')
        require(files['built-motion-browser/report.json']['sha256'] == receipt['report_file_sha256'], 'Receipt differs from packaged report')
        validate_canary(report, files, 'built-motion-browser')
        validate_lazy_canary(report, files, 'built-motion-browser')
        discovered={p['source']:p['images'] for p in expected['pages']}
        screenshot_paths=set()
        for c in report['cases']:
            validate_scroll_evidence(c, files, 'built-motion-browser', screenshot_paths)
            require([i.get('alt') for i in c['images']]==[i.get('alt') for i in discovered[c['source']]],'Missing/extra/disordered discovered image coverage')
            for image in c['images']:
                for state in image['states'].values():
                    path='built-motion-browser/'+c['artifact_directory']+'/'+state['screenshot']
                    require(path in files, 'Case screenshot missing from uploaded groups')
                    require(path not in screenshot_paths,'Duplicate per-case/image/state screenshot reference')
                    screenshot_paths.add(path)
    require(seen_indices == set(range(count)), 'Missing shard index')
    require(len(observed)==len(set(observed)) and set(observed)==set(expected['expected_case_ids']), 'Global coverage gap or overlap')
    return {'status':'passed','case_count':len(observed),'shard_count':count,'identity':expected['identity'],'manifest_sha256':expected['sha256']}

def support_registry(path=None):
    from pathlib import Path
    path=Path(path) if path else Path(__file__).resolve().parent/'fixtures/browser-support-suites.json'
    registry=json.loads(path.read_text())
    require(registry.get('schema')==1 and registry.get('suites'),'Invalid support registry')
    ids=[s['id'] for s in registry['suites']]
    require(len(ids)==len(set(ids)),'Duplicate support registry ID')
    for suite in registry['suites']:
        require(suite['id'] and '/' not in suite['id'] and suite['id'] not in {'.','..'},'Unsafe support root')
        require(suite['type'] in {'motion-preflight','prose','legacy-lab','report-cases'},'Unsupported suite type; define coverage contract first')
        require(suite.get('command'),'Support command missing')
    return registry

PREFLIGHT_TOPICS={topic for suite in support_registry()['suites'] if suite['type']=='motion-preflight' for topic in suite['topics']}
SUPPORT_SUITES=tuple(s['id'] for s in support_registry()['suites'])

def report_digest(report):
    return hashlib.sha256((json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode()).hexdigest()

def validate_registered_pngs(suite, files):
    """Require every registered screenshot once; retain concrete paths in gate errors."""
    name = suite['id']
    pngs = suite.get('expected_pngs', [])
    if suite['type'] in {'legacy-lab', 'report-cases'}:
        require(bool(pngs), f'Empty registered lab screenshot contract: {name}')
    require(len(pngs) == len(set(pngs)), f'Duplicate registered lab screenshot: {name}')
    require(all(isinstance(p, str) and not PurePosixPath(p).is_absolute() and '..' not in PurePosixPath(p).parts and p.endswith('.png') for p in pngs),
            f'Unsafe registered lab screenshot: {name}')
    missing = [name + '/' + p for p in pngs if name + '/' + p not in files]
    require(not missing, 'Missing registered lab screenshots: ' + ', '.join(missing))

def validate_support(expected, receipt, artifact_rows, prose_sources=None, registry=None):
    registry=registry or support_registry();suites=registry['suites'];suite_ids=[s['id'] for s in suites]
    validate_manifest(receipt['manifest'],expected)
    ident=expected['identity'];require(receipt['identity']==ident,'Support run/head/tree mismatch')
    execution=receipt['execution']
    require(execution.get('identity')==ident and execution.get('status')=='passed','Support suites incomplete')
    require(execution.get('registry_sha256')==sha(registry),'Different support registry')
    require([x['suite'] for x in execution['suites']]==suite_ids,'Skipped/extra support suite')
    require(all(x.get('returncode')==0 and x.get('status')=='passed' for x in execution['suites']),'Support suite failed')
    prefix=f"motion-{ident['run_id']}-{ident['run_attempt']}-support"
    files=validate_pack(receipt['pack'],artifact_rows,prefix)
    require('support-execution/report.json' in files,'Missing support execution receipt')
    require(files['support-execution/report.json']['sha256']==report_digest(execution),'Execution receipt differs from pack')
    reports=receipt['reports']
    require(set(reports)=={s['id'] for s in suites if s['type']!='legacy-lab'},'Missing/extra support report')
    discovered={p['source']:p['images'] for p in expected['pages']}
    for suite in suites:
        name=suite['id'];kind=suite['type']
        if kind!='legacy-lab':
            report=reports[name];require(report['status']=='passed','Support report not passed')
            raw=json.dumps(report,ensure_ascii=False,indent=2)+ ('\n' if suite.get('report_trailing_newline') else '')
            path=name+'/report.json';require(path in files,'Missing packed support report')
            require(files[path]['sha256']==hashlib.sha256(raw.encode()).hexdigest(),'Support report/pack mismatch')
        if kind=='motion-preflight':
            require(name+'/discovery-manifest.json' in files and files[name+'/discovery-manifest.json']['sha256']==report_digest(expected),'Packed preflight discovery mismatch')
            require(report['identity']==ident and report['manifest_sha256']==expected['sha256'],'Preflight head/manifest mismatch')
            sources=[p['source'] for p in expected['pages'] if p['source'].rsplit('/',1)[-1].removesuffix('.md').removesuffix('.zh-TW') in suite['topics']]
            require(len(sources)==suite['expected_source_count'],'Preflight lost a bilingual topic')
            ids=[case_id(s,v,m) for s in sources for v in expected['viewports'].values() if v['width']<=suite['maximum_viewport_width'] for m in MODES]
            validate_cases(report,ids,'keyboard-preflight')
            validate_canary(report, files, name)
            validate_lazy_canary(report, files, name)
            screenshot_paths=set()
            for c in report['cases']:
                validate_scroll_evidence(c, files, name, screenshot_paths)
                require([i.get('alt') for i in c['images']]==[i.get('alt') for i in discovered[c['source']]],'Missing preflight discovered images')
                for image in c['images']:
                    for state in image['states'].values():
                        path=name+'/'+c['artifact_directory']+'/'+state['screenshot']
                        require(path in files,'Missing preflight screenshot')
                        require(path not in screenshot_paths,'Duplicate preflight screenshot reference')
                        screenshot_paths.add(path)
        elif kind=='prose':
            require(prose_sources is not None and name in prose_sources,'Missing expected prose source contract')
            wanted={(s,w) for s in prose_sources[name] for w in suite['widths']}
            cases=report['cases'];observed=[(c['source'],c['width']) for c in cases]
            require(len(observed)==len(set(observed)) and set(observed)==wanted,'Prose coverage gap/overlap')
            require(all(c['status']=='passed' and not c.get('errors') for c in cases),'Prose case failed')
            for source,width in wanted:
                folder=source.replace('/','__').removesuffix('.md')+f'-{width}'
                require(name+'/'+folder+'/top.png' in files,'Missing prose-case screenshot')
        elif kind=='report-cases':
            # Extensible lab reports: registry specifies exact tuple keys and expected tuples.
            fields=suite['case_fields'];wanted=[canonical(x) for x in suite['expected_cases']]
            require(wanted and len(wanted)==len(set(wanted)),'Empty/duplicate lab expected cases')
            observed=[canonical([c[k] for k in fields]) for c in report['cases']]
            require(len(observed)==len(set(observed)) and set(observed)==set(wanted),'Lab case coverage gap/overlap')
            require(all(c['status']=='passed' and not c.get('errors') and not c.get('page_errors') for c in report['cases']),'Lab case failed')
            if name == 'policy-gradient-motion':
                specs=suite['expected_case_specs']
                require(len(specs)==24 and len({c['id'] for c in specs})==24,'Original policy 24-case contract lost')
                by_id={c['id']:c for c in report['cases']}
                for spec in specs:
                    c=by_id[spec['id']]
                    require(all(c.get(k)==v for k,v in spec.items()), 'Original policy case matrix differs')
                    require(not c.get('failed_requests') and not c.get('page_errors'), 'Original policy browser errors')
                    wanted_shots=[p for p in suite['expected_pngs'] if p.startswith(c['id']+'/')]
                    require(c.get('screenshots')==wanted_shots,'Original policy screenshot sequence incomplete')
                    if spec['test']=='svg':
                        samples=c.get('samples',[])
                        require(type(samples) is list and all(type(sample) is dict for sample in samples), 'Original policy samples schema malformed')
                        require([x.get('time') for x in samples]==spec['times'], 'Original policy sample times incomplete')
                        for sample, expected_time in zip(samples, spec['times']):
                            try:
                                validate_glyph_sample(sample, spec['stem'], spec['kind'], expected_time)
                            except (AssertionError, TypeError, KeyError) as error:
                                raise ValueError('Original policy glyph measurement contract failed') from error
            if name == 'policy-credit-labs':
                candidates=[c for c in report['cases'] if c.get('topic')=='reinforce' and c.get('lang')=='en' and c.get('width')==320 and c.get('reduced') is False]
                require(len(candidates)==1,'Policy 320 canary case missing or duplicated')
                canary=candidates[0].get('update_320_negative_canary',{})
                require(canary.get('status')=='passed','Policy 320 negative canary missing/failed')
                measurement=canary.get('original_inline_rejected',{})
                width=measurement.get('width')
                require(measurement.get('inner')==320 and isinstance(width,(int,float)) and not isinstance(width,bool) and 320 < width < float('inf'),'Policy 320 canary did not reject original inline overflow')
            if suite.get('require_identity',True):require(report.get('identity')==ident,'Lab identity mismatch')
            require(suite.get('expected_pngs'),'Lab screenshot coverage contract required')
        validate_registered_pngs(suite, files)
        require(any(p.startswith(name+'/') and p.endswith('.png') for p in files),'Missing support screenshots')
    return {'status':'passed','suite_count':len(suites),'registry_sha256':sha(registry)}


def validate_run_inventory(metadata,provenance,count):
    require(str(metadata['run_id'])==provenance['run_id'] and str(metadata['run_attempt'])==provenance['run_attempt'],'Wrong API run/attempt inventory')
    wanted={'Support browser suites',*(f'Full motion shard {i}' for i in range(count))}
    jobs=[j for j in metadata['jobs'] if j['name'] in wanted]
    require(len(jobs)==len(wanted) and {j['name'] for j in jobs}==wanted,'Missing/duplicate exact-attempt producer job')
    require(all(j['status']=='completed' and j['conclusion']=='success' for j in jobs),'Cancelled/skipped/failed producer job')
    require(str(metadata['jobs_attempt'])==provenance['run_attempt'],'Wrong jobs API attempt endpoint')
    require(all(str(j.get('run_attempt',metadata['jobs_attempt']))==provenance['run_attempt'] and str(j['run_id'])==provenance['run_id'] for j in jobs),'Prior-attempt job contamination')
    prefix=f"motion-{provenance['run_id']}-{provenance['run_attempt']}-"
    names={prefix+f'shard-{i}-receipt' for i in range(count)}|{prefix+'support-receipt'}
    artifacts=metadata['artifacts'];actual=[a for a in artifacts if a['name'].startswith(prefix) and a['name'].endswith('-receipt')]
    require(len(actual)==len(names) and {a['name'] for a in actual}==names,'Missing/extra/duplicate receipt artifacts')
    require(all(not a.get('expired') and a.get('size_in_bytes',0)>0 for a in actual),'Expired/empty receipt artifact')
    return names
