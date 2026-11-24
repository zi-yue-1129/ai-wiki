"""Whole synthetic support evidence, run-attempt provenance and workflow wiring."""
import copy,hashlib,json,unittest
from pathlib import Path
from motion_shard_contract import *
from policy_glyph_contract import EXPECTED_LABELS
from test_motion_shard_contract import IDENT,V,canary_fixture,scroll_fixture,lazy_fixture
ROOT=Path(__file__).resolve().parents[1]

def support_fixture():
    pages=[{'source':f'theory/{t}{lang}.md','url':t,'images':[{'src':'still.svg'}]} for t in sorted(PREFLIGHT_TOPICS) for lang in ('','.zh-TW')]
    m=manifest(pages,V,IDENT);cases=[]
    for p in pages:
        for mode in MODES:
            vp=V['mobile'];cases.append({'case_id':case_id(p['source'],vp,mode),'source':p['source'],'viewport':vp,'reduced_motion':mode,'status':'passed','artifact_directory':str(len(cases)),'keyboard_scroll':scroll_fixture(),'images':[{'states':{s:{'screenshot':s+'.png'} for s in ('initial','paused','replayed')}}]})
    reports={'keyboard-scroll-preflight':{'status':'passed','scope':'keyboard-preflight','identity':IDENT,'manifest_sha256':m['sha256'],'cases':cases,'math_renderer_canary':canary_fixture(),'lazy_image_canary':lazy_fixture()}}
    prose={'vi-prose':['docs/vi.md','docs/vi.zh-TW.md'],'embedding-pages':['docs/emb.md','docs/emb.zh-TW.md'],'ddim-prose':['docs/ddim.md','docs/ddim.zh-TW.md']}
    for suite,sources in prose.items():reports[suite]={'status':'passed','cases':[{'source':s,'width':w,'status':'passed','errors':[]} for s in sources for w in (390,1280)]}
    for suite in support_registry()['suites']:
        if suite['id'] in {'time-series-prose','causal-prose'}:
            sources=json.loads((ROOT/suite['sources_manifest']).read_text());prose[suite['id']]=sources
            reports[suite['id']]={'status':'passed','cases':[dict(source=s,lang='zh-TW' if s.endswith('.zh-TW.md') else 'en',width=w,status='passed',errors=[],screenshots=['top.png']) for s in sources for w in suite['widths']]}
    for case in reports['ddim-prose']['cases']:case['required_screenshots']=['schedule.png']
    for suite in support_registry()['suites']:
        if suite['type']=='report-cases':
            reports[suite['id']]={'status':'passed','cases':[dict(zip(suite['case_fields'],v),status='passed') for v in suite['expected_cases']]}
    original=next(s for s in support_registry()['suites'] if s['id']=='policy-gradient-motion')
    reports['policy-gradient-motion']['cases']=[dict(c,status='passed',page_errors=[],failed_requests=[],screenshots=[p for p in original['expected_pngs'] if p.startswith(c['id']+'/')],**({'samples':[dict(time=t,canvas=[0,0,760,400],boxes=[dict(label=label,x=10+(i%10)*60,y=10+(i//10)*30,w=10,h=10) for i,label in enumerate(EXPECTED_LABELS[c['stem']+':'+c['kind']])]) for t in c['times']]} if c['test']=='svg' else {})) for c in original['expected_case_specs']]
    policy=next(c for c in reports['policy-credit-labs']['cases'] if (c['topic'],c['lang'],c['width'],c['reduced'])==('reinforce','en',320,False))
    policy['update_320_negative_canary']={'status':'passed','original_inline_rejected':{'inner':320,'width':369}}
    execution={'identity':IDENT,'registry_sha256':sha(support_registry()),'status':'passed','suites':[{'suite':s,'status':'passed','returncode':0} for s in SUPPORT_SUITES]}
    prefix='motion-123-2-support';artifact=prefix+'-01';files=[]
    for suite,r in reports.items():
        raw=json.dumps(r,ensure_ascii=False,indent=2)+ ('\n' if suite=='keyboard-scroll-preflight' else '')
        files.append({'path':suite+'/report.json','size':len(raw.encode()),'sha256':hashlib.sha256(raw.encode()).hexdigest()})
    files.append({'path':'keyboard-scroll-preflight/discovery-manifest.json','size':1,'sha256':report_digest(m)})
    files.append({'path':'keyboard-scroll-preflight/math-renderer-canary/report.json','size':1,'sha256':report_digest(canary_fixture())})
    files.append({'path':'keyboard-scroll-preflight/lazy-image-canary/report.json','size':1,'sha256':report_digest(lazy_fixture())})
    files.append({'path':'support-execution/report.json','size':12,'sha256':report_digest(execution)})
    files.extend({'path':s+'/figure.png','size':1,'sha256':'d'*64} for s in SUPPORT_SUITES)
    pngs=[f'keyboard-scroll-preflight/{c["artifact_directory"]}/{stage}.png' for c in cases for stage in ('initial','paused','replayed')]
    pngs += ['keyboard-scroll-preflight/lazy-image-canary/loaded-after-scroll.png','keyboard-scroll-preflight/math-renderer-canary/invalid-rendered-error.png'] + [f'keyboard-scroll-preflight/{c["artifact_directory"]}/scroll-region-1-right.png' for c in cases]
    pngs += [suite+'/'+source.replace('/','__').removesuffix('.md')+f'-{width}/top.png' for suite,sources in prose.items() for source in sources for width in next(x['widths'] for x in support_registry()['suites'] if x['id']==suite)]
    pngs += ['ddim-prose/'+source.replace('/','__').removesuffix('.md')+f'-{width}/schedule.png' for source in prose['ddim-prose'] for width in (390,1280)]
    pngs += [f'sharpness-labs/{lang}-{width}.png' for lang in ('en','zh') for width in (320,390,768,1024)]
    pngs += [f'sharpness-labs/built-{lang}-{width}.png' for lang in ('en','zh-TW') for width in (390,1280)]
    pngs += [f'adaptive-optimiser-labs/{mode}-{lang}-{width}.png' for mode in ('adagrad','adafactor') for lang in ('en','zh') for width in (320,720)]
    pngs += [f'adaptive-optimiser-labs/built-{mode}-{lang}-{width}.png' for mode in ('adagrad','adafactor') for lang in ('en','zh-TW') for width in (390,1280)]
    pngs += [suite['id']+'/'+png for suite in support_registry()['suites'] if suite['type']=='report-cases' for png in suite['expected_pngs']]
    files.extend({'path':p,'size':1,'sha256':'d'*64} for p in pngs)
    for f in files:f.update(artifact=artifact,artifact_path=f['path'])
    total=sum(f['size'] for f in files);pack={'status':'passed','artifact_prefix':prefix,'missing_roots':[],'files':files,'file_count':len(files),'raw_bytes':total,'groups':[{'artifact':artifact,'directory':'group-01','file_count':len(files),'raw_bytes':total}]}
    r={'manifest':m,'identity':IDENT,'execution':execution,'reports':reports,'pack':pack}
    return m,r,[{'name':artifact,'id':1,'size_in_bytes':100,'expired':False}],prose

def inventory():
    jobs=[{'name':name,'run_id':123,'status':'completed','conclusion':'success'} for name in ['Support browser suites',*(f'Full motion shard {i}' for i in range(4))]]
    names=[f'motion-123-2-shard-{i}-receipt' for i in range(4)]+['motion-123-2-support-receipt']
    return {'run_id':123,'run_attempt':2,'jobs_attempt':2,'jobs':jobs,'artifacts':[{'name':n,'size_in_bytes':100,'expired':False} for n in names]}
class SupportGate(unittest.TestCase):
    def test_policy_320_canary_missing_failed_or_nonoverflow_rejected(self):
        for kind in ('missing','failed','nonoverflow','wrong-viewport','nan','infinite','boolean'):
            m,r,a,p=support_fixture()
            report=r['reports']['policy-credit-labs']
            case=next(c for c in report['cases'] if (c['topic'],c['lang'],c['width'],c['reduced'])==('reinforce','en',320,False))
            canary=case['update_320_negative_canary']
            if kind=='missing':case.pop('update_320_negative_canary')
            elif kind=='failed':canary['status']='failed'
            elif kind=='wrong-viewport':canary['original_inline_rejected']['inner']=390
            else:canary['original_inline_rejected']['width']={'nonoverflow':320,'nan':float('nan'),'infinite':float('inf'),'boolean':True}[kind]
            # Re-sign changed synthetic report so failure is the actual canary
            # contract, not merely the report-integrity guard.
            for f in r['pack']['files']:
                if f['path']=='policy-credit-labs/report.json':f['sha256']=hashlib.sha256(json.dumps(report,ensure_ascii=False,indent=2).encode()).hexdigest()
            with self.subTest(kind=kind),self.assertRaisesRegex(ValueError,'Policy 320'):
                validate_support(m,r,a,p)

    def test_complete_support(self):
        self.assertEqual(validate_support(*support_fixture())['suite_count'],11)
    def rejected(self,mutation):
        m,r,a,p=support_fixture();mutation(m,r,a,p)
        with self.assertRaises((ValueError,KeyError)):validate_support(m,r,a,p)
    def test_ddim_registry_and_real_source_sections(self):
        suite=next(s for s in support_registry()['suites'] if s['id']=='ddim-prose')
        self.assertEqual(suite['type'],'prose');self.assertEqual(suite['widths'],[390,1280])
        self.assertEqual(suite['required_case_pngs'],['schedule.png'])
        entries=json.loads((ROOT/suite['sources_manifest']).read_text())
        base='docs/theory/paradigms/unsupervised/density-and-generative-models/diffusion/ddim'
        self.assertEqual([e['source'] for e in entries],[base+'.md',base+'.zh-TW.md'])
        for entry,title in zip(entries,['Stochasticity is schedule-dependent','隨機程度取決於時間排程']):
            self.assertEqual(entry['screenshots'],{'schedule':'.md-content__inner h3:has-text("'+title+'")'})
            self.assertIn('### '+title,(ROOT/entry['source']).read_text())

    def test_ddim_missing_suite_page_schedule_or_capture_claim_rejected(self):
        for kind in ('suite','page','schedule','capture-claim'):
            m,r,a,p=support_fixture();report=r['reports']['ddim-prose'];pack=r['pack']
            if kind=='suite':
                r['execution']['suites']=[x for x in r['execution']['suites'] if x['suite']!='ddim-prose']
            elif kind=='page':report['cases'].pop()
            elif kind=='capture-claim':report['cases'][0]['required_screenshots']=[]
            else:
                victim=next(f for f in pack['files'] if f['path'].startswith('ddim-prose/') and f['path'].endswith('/schedule.png'))
                pack['files'].remove(victim)
            for f in pack['files']:
                if f['path']=='ddim-prose/report.json':f['sha256']=hashlib.sha256(json.dumps(report,ensure_ascii=False,indent=2).encode()).hexdigest()
                if f['path']=='support-execution/report.json':f['sha256']=report_digest(r['execution'])
            pack['file_count']=len(pack['files']);pack['raw_bytes']=sum(f['size'] for f in pack['files'])
            pack['groups'][0].update(file_count=pack['file_count'],raw_bytes=pack['raw_bytes'])
            with self.subTest(kind=kind),self.assertRaises(ValueError):validate_support(m,r,a,p)

    def test_required_prose_section_capture_is_not_optional(self):
        from unittest.mock import Mock
        from test_built_prose_browser import capture_required_views
        entry={'screenshots':{'schedule':'h3'}};page=Mock();element=page.locator.return_value
        element.count.return_value=1;element.is_visible.return_value=True
        self.assertEqual(capture_required_views(page,entry,Path('/tmp')),['schedule.png'])
        element.scroll_into_view_if_needed.assert_called_once()
        page.screenshot.assert_called_once_with(path='/tmp/schedule.png')
        for count,visible in ((0,True),(2,True),(1,False)):
            page=Mock();element=page.locator.return_value;element.count.return_value=count;element.is_visible.return_value=visible
            with self.subTest(count=count,visible=visible),self.assertRaises(AssertionError):capture_required_views(page,entry,Path('/tmp'))
            page.screenshot.assert_not_called()

    def test_preflight_topics_match_actual_harness_ast(self):
        import ast
        tree=ast.parse((ROOT/'scripts/test_built_motion_browser.py').read_text())
        assignment=next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='MOBILE_PREFLIGHT_NAMES' for t in n.targets))
        names=ast.literal_eval(assignment.value.args[0])
        self.assertEqual(names,PREFLIGHT_TOPICS)
        suite=support_registry()['suites'][0]
        self.assertEqual(suite['expected_source_count'],2*len(names))
        self.assertEqual(len(support_fixture()[1]['reports'][suite['id']]['cases']),28)
    def test_support_missing_canary_and_right_edge_evidence(self):
        for suffix in ('lazy-image-canary/report.json','lazy-image-canary/loaded-after-scroll.png','math-renderer-canary/report.json','math-renderer-canary/invalid-rendered-error.png','0/scroll-region-1-right.png'):
            m,r,a,p=support_fixture();pack=r['pack']
            pack['files']=[f for f in pack['files'] if not f['path'].endswith(suffix)]
            pack['file_count']=len(pack['files']);pack['raw_bytes']=sum(f['size'] for f in pack['files'])
            pack['groups'][0].update(file_count=pack['file_count'],raw_bytes=pack['raw_bytes'])
            with self.subTest(suffix=suffix),self.assertRaises(ValueError):validate_support(m,r,a,p)
    def test_support_rejects_missing_or_invalid_lazy_canary(self):
        for kind in ('missing','failed','early','undecoded','broken-accepted'):
            m,r,a,p=support_fixture();report=r['reports']['keyboard-scroll-preflight'];canary=report['lazy_image_canary']
            if kind=='missing':report.pop('lazy_image_canary')
            elif kind=='failed':canary['status']='failed'
            elif kind=='early':canary['before_scroll']['naturalWidth']=640
            elif kind=='undecoded':canary['after_scroll']['complete']=False
            else:canary['broken_rejected']=False
            # Coherent hashes ensure this tests semantics, not a stale report digest.
            for f in r['pack']['files']:
                if f['path']=='keyboard-scroll-preflight/report.json':f['sha256']=report_digest(report)
                if f['path']=='keyboard-scroll-preflight/lazy-image-canary/report.json':f['sha256']=report_digest(report.get('lazy_image_canary',{}))
            with self.subTest(kind=kind),self.assertRaisesRegex(ValueError,'lazy|Broken'):
                validate_support(m,r,a,p)
    def test_missing_support_suite(self):self.rejected(lambda m,r,a,p:r['execution']['suites'].pop())
    def test_failed_support_suite(self):self.rejected(lambda m,r,a,p:r['execution']['suites'][0].__setitem__('returncode',1))
    def test_wrong_support_tree(self):self.rejected(lambda m,r,a,p:r.__setitem__('identity',{**IDENT,'tree':'e'*40}))
    def test_missing_preflight_case(self):self.rejected(lambda m,r,a,p:r['reports']['keyboard-scroll-preflight']['cases'].pop())
    def test_missing_prose_case(self):self.rejected(lambda m,r,a,p:r['reports']['vi-prose']['cases'].pop())
    def test_failed_prose_case(self):self.rejected(lambda m,r,a,p:r['reports']['embedding-pages']['cases'][0].__setitem__('status','failed'))
    def test_missing_support_group(self):self.rejected(lambda m,r,a,p:a.clear())
    def test_missing_support_report(self):self.rejected(lambda m,r,a,p:r['reports'].pop('vi-prose'))
    def test_forged_execution(self):self.rejected(lambda m,r,a,p:r['execution'].__setitem__('status','incomplete'))
    def test_real_new_suite_contracts_match_source_loops_and_screenshots(self):
        import ast,itertools
        registry=support_registry()
        for name,script,count,stages in [
            ('policy-credit-labs','test_policy_credit_labs_browser.py',48,['boundary']),
            ('built-planning-evolution-labs','test_built_planning_evolution_labs_browser.py',32,['initial','numeric-final'])]:
            suite=next(x for x in registry['suites'] if x['id']==name)
            tree=ast.parse((ROOT/'scripts'/script).read_text());loops={}
            topics=None
            for node in ast.walk(tree):
                if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='TOPICS' for t in node.targets):topics=list(ast.literal_eval(node.value))
                if isinstance(node,ast.For) and isinstance(node.target,ast.Name) and node.target.id in ('topic','lang','width','reduced'):
                    if isinstance(node.iter,(ast.Tuple,ast.List)):loops[node.target.id]=list(ast.literal_eval(node.iter))
                    elif isinstance(node.iter,ast.Name) and node.iter.id=='TOPICS':loops['topic']=topics
            expected=[list(x) for x in itertools.product(*(loops[k] for k in ('topic','lang','width','reduced')))]
            self.assertEqual(len(expected),count);self.assertEqual(suite['expected_cases'],expected)
            self.assertFalse(suite['require_identity']);self.assertFalse(suite['report_trailing_newline'])
            self.assertEqual(suite['expected_pngs'],[f'{t}-{l}-{w}-{r}/{stage}.png' for t,l,w,r in expected for stage in stages])
            source=(ROOT/'scripts'/script).read_text()
            for env in suite['env']:self.assertIn(env,source)
            for stage in stages:self.assertIn(stage+'.png',source)

    def test_missing_true_policy_case_is_rejected(self):
        self.rejected(lambda m,r,a,p:r['reports']['policy-credit-labs']['cases'].pop())
    def test_failed_true_planning_case_is_rejected(self):
        self.rejected(lambda m,r,a,p:r['reports']['built-planning-evolution-labs']['cases'][0].__setitem__('status','failed'))

    def test_two_new_registry_suites_keep_all_existing_coverage(self):
        m,r,a,prose=support_fixture();registry=copy.deepcopy(support_registry())
        for name in ('additional-lab-a','additional-lab-b'):
            tuples=[[lang,width,mode,kind] for lang in ('en','zh-TW') for width in (390,1280) for mode in ('reduce','no-preference') for kind in range(4)]
            pngs=[f'case-{i}.png' for i in range(32)]
            suite={'id':name,'type':'report-cases','command':['scripts/example_existing_suite.py'],'case_fields':['lang','width','mode','kind'],'expected_cases':tuples,'expected_pngs':pngs,'report_trailing_newline':True}
            registry['suites'].append(suite)
            report={'status':'passed','identity':IDENT,'cases':[dict(zip(suite['case_fields'],values),status='passed') for values in tuples]}
            r['reports'][name]=report;r['execution']['suites'].append({'suite':name,'status':'passed','returncode':0})
            files=r['pack']['files'];artifact=r['pack']['groups'][0]['artifact']
            files.append({'path':name+'/report.json','artifact_path':name+'/report.json','artifact':artifact,'size':1,'sha256':report_digest(report)})
            files.extend({'path':name+'/'+png,'artifact_path':name+'/'+png,'artifact':artifact,'size':1,'sha256':'d'*64} for png in pngs)
        r['execution']['registry_sha256']=sha(registry)
        next(f for f in files if f['path']=='support-execution/report.json')['sha256']=report_digest(r['execution'])
        r['pack']['file_count']=len(files);r['pack']['raw_bytes']=sum(f['size'] for f in files)
        r['pack']['groups'][0].update(file_count=len(files),raw_bytes=r['pack']['raw_bytes'])
        self.assertEqual(validate_support(m,r,a,prose,registry)['suite_count'],13)
        # Merely passing the existing suites cannot satisfy the expanded registry.
        r['reports']['additional-lab-b']['cases'].pop()
        with self.assertRaises(ValueError):validate_support(m,r,a,prose,registry)

    def test_attempt_api_without_optional_run_attempt_field(self):validate_run_inventory(inventory(),IDENT,4)
    def test_run_inventory_negatives(self):
        edits=[lambda x:x.__setitem__('run_id',122),lambda x:x.__setitem__('run_attempt',1),lambda x:x.__setitem__('jobs_attempt',1),lambda x:x['jobs'].pop(),lambda x:x['jobs'].append(copy.deepcopy(x['jobs'][0])),lambda x:x['jobs'][0].__setitem__('conclusion','cancelled'),lambda x:x['jobs'][0].__setitem__('run_attempt',1),lambda x:x['artifacts'].pop(),lambda x:x['artifacts'][0].__setitem__('expired',True)]
        for edit in edits:
            with self.subTest(edit=edit):
                data=inventory();edit(data)
                with self.assertRaises(ValueError):validate_run_inventory(data,IDENT,4)
    def test_complete_gate_with_synthetic_downloaded_receipts(self):
        import tempfile
        from types import SimpleNamespace
        from unittest.mock import patch
        import motion_shard_ci as ci
        from test_motion_shard_contract import fixture
        m,support,group_rows,prose=support_fixture()
        m,shards,rows=fixture(m['pages']);rows+=group_rows
        registry=copy.deepcopy(support_registry())
        for suite in registry['suites']:
            if suite['type']=='prose':
                suite.pop('sources_manifest',None);suite['sources']=prose[suite['id']]
        support['execution']['registry_sha256']=sha(registry)
        next(f for f in support['pack']['files'] if f['path']=='support-execution/report.json')['sha256']=report_digest(support['execution'])
        metadata=inventory();metadata['artifacts']+=rows
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);receipts=root/'receipts';receipts.mkdir()
            for index,r in enumerate(shards):
                d=receipts/f'motion-123-2-shard-{index}-receipt';d.mkdir();(d/'receipt.json').write_text(json.dumps(r))
            d=receipts/'motion-123-2-support-receipt';d.mkdir();(d/'receipt.json').write_text(json.dumps(support))
            inv=root/'inventory.json';inv.write_text(json.dumps(metadata));out=root/'gate.json'
            config=SimpleNamespace(site_dir=str(root/'site'),site_url='https://example.test/')
            with patch.object(ci,'identity',return_value=IDENT),patch.object(ci,'support_registry',return_value=registry),patch('mkdocs.config.load_config',return_value=config),patch('test_built_motion_browser.discover_pages',return_value=m['pages']),patch('test_built_motion_browser.check_built_page') as checked:
                ci.gate(receipts,inv,4,out)
                self.assertEqual(checked.call_count,14,'Gate independently validates every built mapping')
                self.assertEqual(json.loads(out.read_text())['case_count'],56)
                # A green needs state plus a missing upload still cannot pass.
                metadata['artifacts'].pop();inv.write_text(json.dumps(metadata))
                with self.assertRaises(ValueError):ci.gate(receipts,inv,4,out)

    def test_workflow_preserves_full_scope_and_bounded_groups(self):
        import yaml
        text=(ROOT/'.github/workflows/built-motion-browser.yml').read_text();w=yaml.safe_load(text);jobs=w['jobs'];self.assertEqual(set(jobs),{'full-motion','support-browser','built-motion-browser'})
        self.assertEqual(jobs['full-motion']['strategy']['matrix']['shard'],[0,1,2,3]);self.assertFalse(jobs['full-motion']['strategy']['fail-fast'])
        self.assertEqual(jobs['built-motion-browser']['if'],'always()');self.assertEqual(set(jobs['built-motion-browser']['needs']),{'full-motion','support-browser'})
        self.assertIn('mkdocs build --strict',str(jobs['built-motion-browser']))
        self.assertIn('test_*motion_semantics.py',str(jobs['support-browser']));self.assertNotIn('continue-on-error',text)
        action=yaml.safe_load((ROOT/'.github/actions/upload-browser-parts/action.yml').read_text());self.assertEqual(len(action['runs']['steps']),24)
        for step in action['runs']['steps']:self.assertEqual(step['with']['if-no-files-found'],'error')
        from run_motion_shard_support import commands
        self.assertEqual([s for s,_ in commands()],list(SUPPORT_SUITES))
        reference=(ROOT/'scripts/fixtures/built-motion-browser-unsharded-reference.yml').read_text()
        for _,cmd in commands():self.assertIn(cmd[0],reference)
class SharpnessScreenshotContract(unittest.TestCase):
    def test_writer_matches_registry_without_dropping_execution_cases(self):
        import ast,itertools
        tree=ast.parse((ROOT/'scripts/test_sharpness_geometry_labs_browser.py').read_text())
        loops=[n for n in ast.walk(tree) if isinstance(n,ast.For)]
        def loop_values(name):
            return [ast.literal_eval(n.iter) for n in loops if isinstance(n.target,ast.Name) and n.target.id==name]
        # All 16 standalone language/viewport/motion cases remain; only eight screenshots are written.
        self.assertEqual(loop_values('language'),[('en','zh')])
        self.assertEqual(loop_values('motion'),[('reduce','no-preference')])
        self.assertEqual(loop_values('width'),[(320,390,768,1024),(390,1280)])
        self.assertEqual(loop_values('locale'),[('','zh-TW/')])
        shots=[n for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='screenshot']
        self.assertEqual(len(shots),2)
        paths=[]
        for shot in shots:
            kw=next(k.value for k in shot.keywords if k.arg=='path')
            scope=next(n for n in ast.walk(tree) if isinstance(n,ast.If) and shot in list(ast.walk(n)) and 'width in' in ast.unparse(n.test)) if 'language' in ast.unparse(kw) else None
            if scope:
                self.assertEqual(ast.unparse(scope.test),"width in (320, 1024) and motion == 'no-preference'")
                for language,width,motion in itertools.product(('en','zh'),(320,390,768,1024),('reduce','no-preference')):
                    env=dict(language=language,width=width,motion=motion,OUT=Path('.'))
                    if eval(compile(ast.Expression(scope.test),'<writer predicate>','eval'),{},env):paths.append(eval(compile(ast.Expression(kw),'<writer filename>','eval'),{},env))
            else:
                for locale,width in itertools.product(('','zh-TW/'),(390,1280)):
                    paths.append(eval(compile(ast.Expression(kw),'<writer filename>','eval'),{},dict(locale=locale,width=width,OUT=Path('.'))))
        suite=next(s for s in support_registry()['suites'] if s['id']=='sharpness-labs')
        self.assertEqual(len(paths),8);self.assertEqual(len(set(paths)),8)
        self.assertEqual(set(paths),set(suite['expected_pngs']))
    def test_each_missing_sharpness_png_and_duplicate_registry_rejected(self):
        suite=next(s for s in support_registry()['suites'] if s['id']=='sharpness-labs')
        paths={suite['id']+'/'+p for p in suite['expected_pngs']}
        validate_registered_pngs(suite,paths)
        for p in sorted(paths):
            with self.subTest(path=p),self.assertRaisesRegex(ValueError,p):validate_registered_pngs(suite,paths-{p})
        empty=copy.deepcopy(suite);empty['expected_pngs']=[]
        with self.assertRaisesRegex(ValueError,'Empty registered'):validate_registered_pngs(empty,paths)
        suite=copy.deepcopy(suite);suite['expected_pngs'].append(suite['expected_pngs'][0])
        with self.assertRaisesRegex(ValueError,'Duplicate registered'):validate_registered_pngs(suite,paths)
    def test_duplicate_packed_png_rejected(self):
        m,r,a,p=support_fixture()
        item=next(f for f in r['pack']['files'] if f['path']=='sharpness-labs/en-320.png')
        r['pack']['files'].append(copy.deepcopy(item))
        with self.assertRaisesRegex(ValueError,'Duplicate packed file'):validate_support(m,r,a,p)

class GateRuntimeDependencies(unittest.TestCase):
    def test_gate_explicitly_installs_prose_import_dependency_before_tests(self):
        import yaml
        w=yaml.safe_load((ROOT/'.github/workflows/built-motion-browser.yml').read_text())
        def verify(w):
            job=w['jobs']['built-motion-browser'];steps=job['steps'];installs=[];tests=[]
            for i,s in enumerate(steps):
                lines=[line.strip()for line in s.get('run','').splitlines()]
                if 'python -m pip install -r requirements.txt "playwright==1.55.0"' in lines:
                    assert 'if' not in s and (s.get('continue-on-error') is None or s.get('continue-on-error') is False)
                    installs.append(i)
                if 'python scripts/test_motion_shard_ci.py' in lines:tests.append(i)
            assert len(installs)==len(tests)==1 and installs[0]<tests[0]
        verify(w)
        for value in ('python -m pip install -r requirements.txt','# python -m pip install -r requirements.txt "playwright==1.55.0"','python -m pip install -r requirements.txt "playwright==1.55.0" || true'):
            bad=copy.deepcopy(w)
            for step in bad['jobs']['built-motion-browser']['steps']:
                if step.get('name')=='Install independent discovery and build dependencies':step['run']=value
            with self.assertRaises(AssertionError):verify(bad)
        for condition in (False,None,'always()'):
            bad=copy.deepcopy(w)
            for step in bad['jobs']['built-motion-browser']['steps']:
                if step.get('name')=='Install independent discovery and build dependencies':step['if']=condition
            with self.assertRaises(AssertionError):verify(bad)
    def test_missing_playwright_fails_actual_capture_negative_not_skipped(self):
        import sys,subprocess
        program=r'''
import sys,importlib.abc,unittest
sys.path.insert(0,sys.argv[1])
class NoPlaywright(importlib.abc.MetaPathFinder):
 def find_spec(self,fullname,path=None,target=None):
  if fullname=='playwright' or fullname.startswith('playwright.'):
   raise ModuleNotFoundError("No module named 'playwright' (intentional dependency negative)")
sys.meta_path.insert(0,NoPlaywright())
from test_motion_shard_ci import SupportGate
result=unittest.TextTestRunner().run(unittest.TestSuite([SupportGate('test_required_prose_section_capture_is_not_optional')]))
sys.exit(0 if result.wasSuccessful() else 1)
'''
        result=subprocess.run([sys.executable,'-I','-c',program,str(ROOT/'scripts')],text=True,capture_output=True)
        self.assertEqual(result.returncode,1)
        self.assertIn("No module named 'playwright' (intentional dependency negative)",result.stderr)
        self.assertIn('FAILED (errors=1)',result.stderr)
        self.assertNotIn('skipped=',result.stderr)


if __name__=='__main__':unittest.main()
