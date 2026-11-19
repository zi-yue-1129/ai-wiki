"""Fail-closed coverage, source/render and actual CI routing for deployed math."""
import copy
import unittest
from pathlib import Path
import yaml
import test_deployed_math_browser as b

ROOT=Path(__file__).resolve().parents[1]
DEPENDENCIES=('scripts/test_built_motion_browser.py','scripts/test_built_prose_browser.py','scripts/motion_shard_contract.py','requirements.txt','mkdocs.yml')
def unconditional(step):
    return 'if' not in step and (step.get('continue-on-error') is None or step.get('continue-on-error') is False)
def verify_workflow(workflow):
    job=workflow['jobs']['build-docs'];assert job['runs-on']=='ubuntu-24.04' and unconditional(job)
    steps=job['steps'];commands=[x.get('run','') for x in steps]
    needed=['pip install -r requirements.txt','pip install playwright==1.55.0 Pillow==13.0.0','python -m playwright install --with-deps chromium','python scripts/test_deployed_math_contract.py','mkdocs build --strict','python scripts/test_deployed_math_browser.py']
    positions=[]
    for cmd in needed:
        valid=[i for i,x in enumerate(steps) if unconditional(x) and cmd in x.get('run','').splitlines()]
        assert valid,cmd
        positions.append(min(valid))
    assert positions[0]<positions[1]<positions[2]<positions[3]<positions[4]<positions[5]
    uploads=[x for x in steps if x.get('uses','').startswith('actions/upload-artifact@') and x.get('with',{}).get('name')=='deployed-math-browser']
    assert len(uploads)==1
    u=uploads[0];assert u.get('if')=='always()' and u['with']['path']=='artifacts/deployed-math/' and u['with']['if-no-files-found']=='error'
    triggers=workflow.get('on',workflow.get(True))
    for event in ('pull_request',):
        paths=triggers[event]['paths']
        for path in (*b.SOURCES,*DEPENDENCIES,'scripts/test_deployed_math_browser.py','scripts/test_deployed_math_contract.py','scripts/test_forward_math_markup.py'):
            assert path in paths,path

class DeployedMath(unittest.TestCase):
    def test_exact_sources_and_real_parser(self):
        self.assertEqual(b.SOURCES,('docs/theory/paradigms/reinforcement-learning/multi-agent-rl/mappo/index.md', 'docs/theory/paradigms/reinforcement-learning/multi-agent-rl/mappo/index.zh-TW.md', 'docs/theory/paradigms/reinforcement-learning/multi-agent-rl/maddpg/index.md', 'docs/theory/paradigms/reinforcement-learning/multi-agent-rl/maddpg/index.zh-TW.md', 'docs/theory/paradigms/unsupervised/density-and-generative-models/diffusion/score-sde.md', 'docs/theory/paradigms/unsupervised/density-and-generative-models/diffusion/score-sde.zh-TW.md', 'docs/theory/paradigms/reinforcement-learning/offline-rl/cql/index.md', 'docs/theory/paradigms/reinforcement-learning/offline-rl/cql/index.zh-TW.md', 'docs/theory/causal-inference/double-machine-learning.md', 'docs/theory/causal-inference/double-machine-learning.zh-TW.md'));self.assertEqual(b.WIDTHS,(320,390,1280))
        self.assertEqual(list(b.DISPLAY_COUNTS.values()),[2, 2, 2, 2, 3, 3, 2, 2, 6, 6])
        for source in b.SOURCES:
            displays=b.source_displays((ROOT/source).read_text())
            for body in b.required_bodies(source):self.assertEqual(displays.count(b.compact(body)),1)
    def test_source_to_native_snapshot_missing_duplicate_raw_and_list(self):
        for source in b.SOURCES:
            bodies=[b.compact(x) for x in b.required_bodies(source)]
            rows=[{'tex':x,'li':None}for x in bodies]
            if '/score-sde' in source:
                titles=['前向 SDE。','逆時 SDE。','機率流 ODE。'] if '.zh-TW.' in source else ['Forward SDE.','Reverse-time SDE.','Probability flow ODE.']
                for i,row in enumerate(rows):row['li']={'title':titles[i],'count':3,'index':i,'displays':1,'paragraphs':2}
            if '/double-machine-learning' in source:
                record=b.DmlLimitationsMarkupTests.RECORDS[1 if '.zh-TW.' in source else 0]
                rows[0]['li']=dict(title=record[3][1],count=5,index=1,displays=1,paragraphs=2);rows[0]['list_titles']=record[3]
            good={'displays':rows,'outside':'<p>Legal prose</p><code>\\sum_i</code>'};b.validate_snapshot(source,bodies,good)
            variants=[dict(good,displays=rows[:-1]),dict(good,displays=rows+rows[:1]),dict(good,outside='<p>\\sum_i x</p>')]
            if '/score-sde' in source:
                bad=copy.deepcopy(good);bad['displays'][0]['li']['count']=2;variants.append(bad)
            if '/double-machine-learning' in source:
                for key,value in [('count',2),('index',0),('title','Wrong heading'),('paragraphs',1)]:
                    bad=copy.deepcopy(good);bad['displays'][0]['li'][key]=value;variants.append(bad)
                bad=copy.deepcopy(good);bad['displays'][0]['list_titles']=bad['displays'][0]['list_titles'][:-1];variants.append(bad)
            for bad in variants:
                with self.assertRaises(AssertionError):b.validate_snapshot(source,bodies,bad)
    def test_geometry_true_overflow_rejected_local_scroll_accepted(self):
        g=dict(left=10,right=250,width=240,height=30,viewport=320,scroll=None);b.validate_geometry(g)
        for key,value in [('right',410),('left',-20),('height',0),('width',float('nan')),('viewport',True)]:
            bad=dict(g,**{key:value})
            with self.assertRaises(AssertionError):b.validate_geometry(bad)
        sc=dict(g,right=410,scroll=dict(left=10,right=300,client=290,width=400));b.validate_geometry(sc)
        for key,value in [('left',-10),('right',400),('client',0)]:
            bad=copy.deepcopy(sc);bad['scroll'][key]=value
            with self.assertRaises(AssertionError):b.validate_geometry(bad)
    def test_actual_browser_inspector_javascript_fail_closed(self):
        import subprocess,json
        harness=r"""
const inspect=eval('('+INPUT+')');
for(const mode of ['valid','missing-math','duplicate','error','zero-height','missing-article']) {
 const node={getBoundingClientRect:()=>({height:mode==='zero-height'?0:25}),querySelector:()=>mode==='error'?{}:null};
 const wrapper={contains:n=>n===node,querySelector:()=>node,closest:()=>null};
 const article={querySelectorAll:()=>[wrapper],cloneNode:()=>({querySelectorAll:()=>[],innerHTML:'<p>Plain prose</p>'})};
 global.document={querySelector:()=>mode==='missing-article'?null:article};
 global.window={MathJax:{startup:{document:{math:mode==='missing-math'?[]:Array.from({length:mode==='duplicate'?2:1},()=>({typesetRoot:node,math:'x=1'}))}}}};
 global.MathJax=window.MathJax;
 let failed=false;try{const result=inspect();if(result.displays[0].tex!=='x=1')throw Error('Wrong source')}catch(e){failed=true}
 if(failed!==(mode!=='valid'))throw Error('Inspector did not enforce '+mode);
}
""".replace('INPUT',json.dumps(b.INSPECT))
        subprocess.run(['node','-e',harness],check=True,capture_output=True,text=True)

    def test_exact_report_matrix_and_each_display_receipt(self):
        cases=[]
        for source in b.SOURCES:
            expected=b.source_displays((ROOT/source).read_text())
            rows=[dict(tex=x,li=None)for x in expected]
            if '/score-sde' in source:
                titles=['前向 SDE。','逆時 SDE。','機率流 ODE。'] if '.zh-TW.' in source else ['Forward SDE.','Reverse-time SDE.','Probability flow ODE.']
                for i,row in enumerate(rows):row['li']=dict(title=titles[i],count=3,index=i,displays=1,paragraphs=2)
            if '/double-machine-learning' in source:
                record=b.DmlLimitationsMarkupTests.RECORDS[1 if '.zh-TW.' in source else 0]
                row=rows[expected.index(b.compact(b.DmlLimitationsMarkupTests.BODY))]
                row['li']=dict(title=record[3][1],count=5,index=1,displays=1,paragraphs=2);row['list_titles']=record[3]
            for width in b.WIDTHS:
                cases.append(dict(source=source,width=width,status='passed',errors=[],expected_displays=len(expected),expected_tex=expected,
                    snapshot=dict(displays=rows,outside='<p>Prose</p>'),
                    displays=[dict(image=f'display-{i:03d}.png',geometry=dict(left=10,right=200,width=190,height=30,viewport=width,scroll=None))for i in range(len(expected))],screenshots=['top.png','core-list.png','limitations.png']))
        good=dict(status='passed',cases=cases);b.validate_report(good)
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for case in cases:
                folder=root/(case['source'].replace('/','__').removesuffix('.md')+f"-{case['width']}");folder.mkdir();case['image_receipts']={}
                for name in case['screenshots']+[row['image']for row in case['displays']]:
                    b.Image.new('RGB',(case['width'],900),(len(name)*7%255,len(case['source'])%255,len(case['image_receipts'])%255)).save(folder/name)
                    case['image_receipts'][name]=b.image_receipt(folder/name)
            b.validate_artifacts(good,root)
            victim=next(root.rglob('display-000.png'));data=victim.read_bytes();victim.unlink()
            with self.assertRaises(FileNotFoundError):b.validate_artifacts(good,root)
            victim.write_bytes(b'not a png')
            with self.assertRaises(Exception):b.validate_artifacts(good,root)
            victim.write_bytes(data)
            other=next(p for p in root.rglob('*.png') if p!=victim and p.read_bytes()!=data)
            victim.write_bytes(other.read_bytes())
            with self.assertRaises(AssertionError):b.validate_artifacts(good,root)
            victim.write_bytes(data[:-20])
            with self.assertRaises(Exception):b.validate_artifacts(good,root)
            victim.write_bytes(data)

        variants=[dict(good,cases=cases[:-1]),dict(good,cases=cases[:-1]+cases[:1]),dict(good,status='running')]
        for key,value in [('displays',[]),('errors',['MathJax error']),('status','failed'),('screenshots',[]),('expected_displays',1)]:
            bad=copy.deepcopy(good);bad['cases'][0][key]=value;variants.append(bad)
        bad=copy.deepcopy(good)
        for case in bad['cases']:case['expected_displays']=1;case['displays']=case['displays'][:1]
        variants.append(bad)
        bad=copy.deepcopy(good);bad['cases'][0]['displays'][0]['geometry']['scroll']=dict(left=10,right=300,client=290,width=500);variants.append(bad)
        bad=copy.deepcopy(good);bad['cases'][6]['expected_tex'][0]='forged';bad['cases'][6]['snapshot']['displays'][0]['tex']='forged';variants.append(bad)
        scrolled=copy.deepcopy(good);row=scrolled['cases'][0]['displays'][0]
        row['geometry']['scroll']=dict(left=10,right=300,client=290,width=500)
        row['right_image']='display-000-right.png';row['end']=dict(max=210,position=210,right=299,viewport_left=10,viewport_right=300)
        b.validate_report(scrolled)
        for key,value in [('position',1),('right',400),('max',0),('position',float('nan')),('right',float('inf')),('position',True)]:
            bad=copy.deepcopy(scrolled);bad['cases'][0]['displays'][0]['end'][key]=value;variants.append(bad)
        for bad in variants:
            with self.assertRaises((AssertionError,KeyError)):b.validate_report(bad)

    def test_future_ci_routes_and_dependencies(self):
        workflow=yaml.safe_load((ROOT/'.github/workflows/concept-animation-validation.yml').read_text());verify_workflow(workflow)
        for path in (*b.SOURCES,*DEPENDENCIES,'scripts/test_deployed_math_browser.py','scripts/test_deployed_math_contract.py','scripts/test_forward_math_markup.py'):
            bad=copy.deepcopy(workflow);bad[True]['pull_request']['paths'].remove(path)
            with self.assertRaises(AssertionError):verify_workflow(bad)
        for i,step in enumerate(workflow['jobs']['build-docs']['steps']):
            if step.get('run') in ['pip install -r requirements.txt','pip install playwright==1.55.0 Pillow==13.0.0','python -m playwright install --with-deps chromium','python scripts/test_deployed_math_contract.py','mkdocs build --strict','python scripts/test_deployed_math_browser.py']:
                for key,value in [('if',False),('if',None),('continue-on-error',True),('run','# '+step['run']),('run',step['run']+' || true')]:
                    bad=copy.deepcopy(workflow);bad['jobs']['build-docs']['steps'][i][key]=value
                    with self.assertRaises(AssertionError):verify_workflow(bad)
        bad=copy.deepcopy(workflow);bad['jobs']['build-docs']['runs-on']='ubuntu-latest'
        with self.assertRaises(AssertionError):verify_workflow(bad)

if __name__=='__main__':unittest.main()
