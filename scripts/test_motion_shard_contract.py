"""Offline, adversarial coverage and lossless-upload receipt tests (no Chromium)."""
import copy,hashlib,json,unittest
from motion_shard_contract import *

IDENT={'checkout':'a'*40,'tree':'b'*40,'event_head':'c'*40,'run_id':'123','run_attempt':'2'}
V={'desktop':{'width':1280,'height':900},'mobile':{'width':390,'height':844}}
def lazy_fixture():
    return {'status':'passed','scope':'isolated native lazy image canary',
            'before_scroll':{'top':20000,'complete':False,'naturalWidth':0},
            'after_scroll':{'complete':True,'naturalWidth':640,'naturalHeight':360},'broken_rejected':True}

def canary_fixture():
    good={'containers':1,'unrendered':0,'nestedAssistive':0,'renderedErrors':[]}
    return {'status':'passed','scope':'isolated actual MathJax renderer canary',
            'valid':good.copy(),'cleared':good.copy(),
            'invalid_rejected':{'containers':1,'renderedErrors':[{'message':'Unknown environment'}]}}

def scroll_fixture():
    return [{'clientWidth':358,'scrollWidth':640,'afterArrowRight':40,'rightEdge':282,
             'rightEdgeScreenshot':'scroll-region-1-right.png'}]

def fixture(pages=None):
    m=manifest(pages or [{'source':p,'url':p,'output':p+'.html','images':[{'src':p+'.svg'}]} for p in ['a.md','a.zh-TW.md']],V,IDENT)
    receipts=[];rows=[]
    for index in range(4):
        prefix=f'motion-123-2-shard-{index}';cases=[]
        for cid in partition(m['expected_case_ids'],index,4):
            src,w,h,mode=json.loads(cid)
            cases.append({'case_id':cid,'source':src,'viewport':{'width':w,'height':h},'reduced_motion':mode,'status':'passed','artifact_directory':str(len(cases)),
                          'keyboard_scroll':scroll_fixture(),'images':[{'states':{stage:{'screenshot':stage+'.png'} for stage in ('initial','paused','replayed')}}]})
        report={'status':'passed','scope':'full','identity':IDENT.copy(),'manifest_sha256':m['sha256'],'shard_index':index,'shard_count':4,'cases':cases,'math_renderer_canary':canary_fixture(),'lazy_image_canary':lazy_fixture()}
        raw=json.dumps(report,ensure_ascii=False,indent=2)+'\n';report_hash=hashlib.sha256(raw.encode()).hexdigest()
        name=prefix+'-01';paths=['built-motion-browser/report.json','built-motion-browser/discovery-manifest.json']+[f"built-motion-browser/{c['artifact_directory']}/{s}.png" for c in cases for s in ('initial','paused','replayed')]
        paths += ['built-motion-browser/lazy-image-canary/report.json','built-motion-browser/lazy-image-canary/loaded-after-scroll.png','built-motion-browser/math-renderer-canary/report.json','built-motion-browser/math-renderer-canary/invalid-rendered-error.png'] + [f"built-motion-browser/{c['artifact_directory']}/scroll-region-1-right.png" for c in cases]
        files=[{'path':p,'artifact_path':p,'artifact':name,'size':1,'sha256':report_digest(report['lazy_image_canary']) if p.endswith('lazy-image-canary/report.json') else report_digest(report['math_renderer_canary']) if p.endswith('math-renderer-canary/report.json') else report_hash if p.endswith('report.json') else report_digest(m) if p.endswith('discovery-manifest.json') else 'd'*64} for p in paths]
        pack={'status':'passed','missing_roots':[],'artifact_prefix':prefix,'file_count':len(files),'raw_bytes':len(files),'files':files,'groups':[{'artifact':name,'directory':'group-01','file_count':len(files),'raw_bytes':len(files)}]}
        receipts.append({'manifest':copy.deepcopy(m),'report':report,'report_file_sha256':report_hash,'pack':pack})
        rows.append({'name':name,'id':index+1,'size_in_bytes':99,'expired':False})
    return m,receipts,rows
class ShardContract(unittest.TestCase):
    def test_full_union_balanced_and_stable(self):
        m,r,a=fixture();self.assertEqual(validate_shards(m,r,4,a)['case_count'],8)
        for count in (2,3,4):
            parts=[partition(m['expected_case_ids'][::-1],i,count) for i in range(count)]
            self.assertEqual(sorted(sum(parts,[])),m['expected_case_ids']);self.assertLessEqual(max(map(len,parts))-min(map(len,parts)),1)
    def rejected(self,mutation):
        m,r,a=fixture();old=[x['report_file_sha256'] for x in r];mutation(m,r,a)
        # Re-sign coherent synthetic evidence so coverage negatives exercise coverage,
        # not merely the receipt-integrity guard. Explicit corrupt-hash tests stay corrupt.
        for receipt in r:
            if receipt['report_file_sha256'] in old:
                new=report_digest(receipt['report']);receipt['report_file_sha256']=new
                for f in receipt['pack']['files']:
                    if f['path']=='built-motion-browser/report.json':f['sha256']=new
                    if f['path']=='built-motion-browser/lazy-image-canary/report.json':f['sha256']=report_digest(receipt['report'].get('lazy_image_canary',{}))
                    if f['path']=='built-motion-browser/math-renderer-canary/report.json':f['sha256']=report_digest(receipt['report'].get('math_renderer_canary',{}))
        with self.assertRaises((ValueError,KeyError,TypeError)):validate_shards(m,r,4,a)
    def test_missing_lazy_canary(self):self.rejected(lambda m,r,a:r[0]['report'].pop('lazy_image_canary'))
    def test_failed_lazy_canary(self):self.rejected(lambda m,r,a:r[0]['report']['lazy_image_canary'].__setitem__('status','failed'))
    def test_lazy_loaded_before_scroll(self):self.rejected(lambda m,r,a:r[0]['report']['lazy_image_canary']['before_scroll'].__setitem__('naturalWidth',640))
    def test_lazy_not_decoded_after_scroll(self):self.rejected(lambda m,r,a:r[0]['report']['lazy_image_canary']['after_scroll'].__setitem__('complete',False))
    def test_broken_lazy_image_accepted(self):self.rejected(lambda m,r,a:r[0]['report']['lazy_image_canary'].__setitem__('broken_rejected',False))
    def test_missing_canary(self):self.rejected(lambda m,r,a:r[0]['report'].pop('math_renderer_canary'))
    def test_failed_canary(self):self.rejected(lambda m,r,a:r[0]['report']['math_renderer_canary'].__setitem__('status','failed'))
    def test_canary_invalid_not_rejected(self):self.rejected(lambda m,r,a:r[0]['report']['math_renderer_canary']['invalid_rejected'].__setitem__('renderedErrors',[]))
    def test_canary_not_cleared(self):self.rejected(lambda m,r,a:r[0]['report']['math_renderer_canary']['cleared'].__setitem__('renderedErrors',['error']))
    def test_missing_scroll_discovery(self):self.rejected(lambda m,r,a:r[0]['report']['cases'][0].pop('keyboard_scroll'))
    def test_missing_right_edge_reference(self):self.rejected(lambda m,r,a:r[0]['report']['cases'][0]['keyboard_scroll'][0].pop('rightEdgeScreenshot'))
    def test_right_edge_not_reached(self):self.rejected(lambda m,r,a:r[0]['report']['cases'][0]['keyboard_scroll'][0].__setitem__('rightEdge',40))
    def test_missing_extra_evidence(self):
        for suffix in ('lazy-image-canary/report.json','lazy-image-canary/loaded-after-scroll.png','math-renderer-canary/report.json','math-renderer-canary/invalid-rendered-error.png','0/scroll-region-1-right.png'):
            def mutation(m,r,a):
                pack=r[0]['pack'];pack['files']=[f for f in pack['files'] if not f['path'].endswith(suffix)]
                pack['file_count']=pack['raw_bytes']=len(pack['files'])
                pack['groups'][0]['file_count']=pack['groups'][0]['raw_bytes']=len(pack['files'])
            with self.subTest(suffix=suffix):self.rejected(mutation)
    def test_missing_receipt(self):self.rejected(lambda m,r,a:r.pop())
    def test_extra_receipt(self):self.rejected(lambda m,r,a:r.append(copy.deepcopy(r[0])))
    def test_duplicate_shard(self):self.rejected(lambda m,r,a:r.__setitem__(1,copy.deepcopy(r[0])))
    def test_wrong_shard_count(self):self.rejected(lambda m,r,a:r[0]['report'].__setitem__('shard_count',3))
    def test_wrong_checkout(self):self.rejected(lambda m,r,a:r[0]['report']['identity'].__setitem__('checkout','x'*40))
    def test_wrong_tree(self):self.rejected(lambda m,r,a:r[0]['report']['identity'].__setitem__('tree','x'*40))
    def test_wrong_event_head(self):self.rejected(lambda m,r,a:r[0]['report']['identity'].__setitem__('event_head','x'*40))
    def test_wrong_run(self):self.rejected(lambda m,r,a:r[0]['report']['identity'].__setitem__('run_id','122'))
    def test_wrong_attempt(self):self.rejected(lambda m,r,a:r[0]['report']['identity'].__setitem__('run_attempt','1'))
    def test_stale_manifest(self):self.rejected(lambda m,r,a:r[0]['manifest']['pages'][0].__setitem__('images',[]))
    def test_failed_case(self):self.rejected(lambda m,r,a:r[0]['report']['cases'][0].__setitem__('status','failed'))
    def test_missing_case(self):self.rejected(lambda m,r,a:r[0]['report']['cases'].pop())
    def test_duplicate_case(self):self.rejected(lambda m,r,a:r[0]['report']['cases'].append(copy.deepcopy(r[0]['report']['cases'][0])))
    def test_extra_case(self):self.rejected(lambda m,r,a:r[0]['report']['cases'].append(copy.deepcopy(r[1]['report']['cases'][0])))
    def test_wrong_actual_dimensions(self):self.rejected(lambda m,r,a:r[0]['report']['cases'][0]['viewport'].__setitem__('width',1))
    def test_forged_passed_discovery(self):self.rejected(lambda m,r,a:r[0]['report'].__setitem__('status','discovery-only; browser checks not run'))
    def test_missing_image_state(self):self.rejected(lambda m,r,a:r[0]['report']['cases'][0]['images'][0]['states'].pop('paused'))
    def test_reused_screenshot_cannot_cover_two_states(self):self.rejected(lambda m,r,a:r[0]['report']['cases'][0]['images'][0]['states']['paused'].__setitem__('screenshot','initial.png'))
    def test_missing_artifact(self):self.rejected(lambda m,r,a:a.pop())
    def test_extra_artifact(self):self.rejected(lambda m,r,a:a.append({**a[0],'name':a[0]['name'][:-2]+'02'}))
    def test_duplicate_artifact(self):self.rejected(lambda m,r,a:a.append(copy.deepcopy(a[0])))
    def test_expired_artifact(self):self.rejected(lambda m,r,a:a[0].__setitem__('expired',True))
    def test_missing_pack_root(self):self.rejected(lambda m,r,a:r[0]['pack'].__setitem__('missing_roots',['built-motion-browser']))
    def test_corrupt_receipt_hash(self):self.rejected(lambda m,r,a:r[0].__setitem__('report_file_sha256','e'*64))
    def test_missing_uploaded_png(self):self.rejected(lambda m,r,a:r[0]['pack']['files'].pop())
    def test_old_attempt_artifact_not_substitute(self):self.rejected(lambda m,r,a:a[0].__setitem__('name',a[0]['name'].replace('-123-2-','-123-1-')))
    def test_unrelated_prior_attempt_is_not_current_evidence(self):
        m,r,a=fixture();a.append({**a[0],'name':a[0]['name'].replace('-123-2-','-123-1-')});validate_shards(m,r,4,a)
    def test_empty_duplicate_invalid_partition(self):
        for args in [([],0,4),(['a','a'],0,2),(['a'],1,4),(['a'],-1,4),(['a'],0,0)]:
            with self.assertRaises(ValueError):partition(*args)
if __name__=='__main__':unittest.main()
