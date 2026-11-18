"""Real suite inventory, collision negatives, failure reports and CI wiring."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch, Mock
import yaml

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('policy_svg_browser',ROOT/'scripts/test_policy_gradient_motion_browser.py')
suite=importlib.util.module_from_spec(spec);spec.loader.exec_module(suite)

def validate_player_barriers(source):
    import ast
    tree=ast.parse(source);player=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='check_player')
    waits=[n for n in ast.walk(player)if isinstance(n,ast.Call)and isinstance(n.func,ast.Name)and n.func.id=='ready_image']
    expected=[('initial-still-before-enhancement',"base+stem+'-still.svg'"),('enhanced',"base+stem+('-still.svg' if reduced else '-motion.svg')"),('clicked',"base+stem+('-motion.svg' if reduced else '-still.svg')"),('entered',"base+stem+('-still.svg' if reduced else '-motion.svg')"),('spaced',"base+stem+('-motion.svg' if reduced else '-still.svg')"),('final-still',"base+stem+'-still.svg'")]
    assert [n.args[-1].value for n in waits]==[x[0]for x in expected]
    for call,(_,expression)in zip(waits,expected):assert ast.dump(call.args[2])==ast.dump(ast.parse(expression,mode='eval').body)
    top=[ast.unparse(n)for n in player.body]
    assert next(i for i,x in enumerate(top)if 'initial-still-before-enhancement'in x)<next(i for i,x in enumerate(top)if 'page.add_script_tag'in x)
    for stage,shot in [('clicked','clicked'),('entered','entered'),('spaced','spaced'),('final-still','final-still')]:
        assert next(i for i,x in enumerate(top)if x.startswith('ready_image(')and repr(stage)in x)<next(i for i,x in enumerate(top)if x.startswith('shot(')and repr(shot)in x)
    return tree,player,waits

class Coverage(unittest.TestCase):
    def test_original_24_cases_and_every_time(self):
        cases=suite.cases();self.assertEqual(len(cases),24)
        for stem in suite.STEMS:
            own=[x for x in cases if x['stem']==stem]
            svg=[x for x in own if x['test']=='svg'];self.assertEqual(len(svg),2)
            self.assertEqual(next(x['times']for x in svg if x['kind']=='motion'),[0,2,4,6,9,11])
            self.assertEqual(next(x['times']for x in svg if x['kind']=='still'),[0])
            for lang in ['en','zh']:
                players=[x for x in own if x.get('lang')==lang]
                self.assertEqual({(x['width'],x['reduced'])for x in players},{(320,False),(360,False),(720,False),(1024,False),(320,True)})
    def test_collision_negative(self):
        with self.assertRaises(AssertionError):suite.check_boxes([dict(label='a',x=20,y=20,w=20,h=20),dict(label='b',x=25,y=25,w=20,h=20)],'s','motion',6)
    def test_bound_negative(self):
        for box in [dict(x=-3,y=10,w=1,h=1),dict(x=10,y=-3,w=1,h=1),dict(x=760,y=10,w=3,h=1),dict(x=10,y=400,w=1,h=3)]:
            with self.assertRaises(AssertionError):suite.check_boxes([dict(label='bad',**box)],'s','still',0)
    def test_original_tolerance(self):
        suite.check_boxes([dict(label='a',x=20,y=20,w=20,h=20),dict(label='b',x=37,y=20,w=20,h=20)],'s','motion',0)
    def test_launch_failure_retains_all_cases(self):
        with tempfile.TemporaryDirectory() as d,patch.object(suite,'OUT',Path(d)),patch.object(suite,'sync_playwright',side_effect=RuntimeError('launch blocked canary')):
            self.assertEqual(suite.main(),1);r=json.loads((Path(d)/'report.json').read_text());self.assertEqual(r['status'],'failed');self.assertEqual(len(r['cases']),24);self.assertTrue(all(x['status']=='blocked'for x in r['cases']));self.assertIn('launch blocked canary',r['error'])
    def test_native_sample_path_measures_line_and_rejects_original_crossing(self):
        from test_policy_glyph_contract_motion_semantics import sample
        for y, valid in [(185., True), (170., False)]:
            page = Mock()
            page.evaluate.side_effect = [sample(kind='still')['boxes'], [0,0,760,400],
                dict(text=dict(x=369.5546875,y=y,w=71.1630859375,h=12.),
                     line=dict(x=141.,y=179.,w=541.,h=0.),stroke=3.)]
            record = {}
            with patch.object(suite, 'shot'):
                if valid:
                    suite.check_svg(page, 'reinforce-return-credit', 'still', record)
                    self.assertEqual(record['line_clearance'][0]['gap'], 4.5)
                else:
                    with self.assertRaisesRegex(AssertionError, 'glyph/line clearance'):
                        suite.check_svg(page, 'reinforce-return-credit', 'still', record)
                    self.assertEqual(record['line_clearance'][0]['geometry']['text']['y'], 170.)
            self.assertEqual(page.evaluate.call_count, 3)
            self.assertIn('getBBox()', page.evaluate.call_args_list[2].args[0])
            self.assertIn('getComputedStyle', page.evaluate.call_args_list[2].args[0])

    def test_actual_readiness_javascript_controlled_delay_and_wrong_resource_negatives(self):
        import subprocess
        harness=r"""
const ready=eval('('+PREDICATE+')');const expected='https://aiwiki.test/assets/concept-animations/reinforce-return-credit-motion.svg';
const img={src:expected,currentSrc:expected,complete:false,naturalWidth:0,naturalHeight:0,isConnected:true,getAttribute(k){return this[k]}};
global.document={querySelector:()=>img};
(async()=>{
 if(ready(expected))throw Error('Incomplete resource accepted');
 setTimeout(()=>Object.assign(img,{complete:true,naturalWidth:760,naturalHeight:400}),25);
 const end=Date.now()+1000;while(!ready(expected)&&Date.now()<end)await new Promise(r=>setTimeout(r,2));
 if(!ready(expected))throw Error('Delayed valid image not accepted');
 for(const [key,value]of [['src',expected.replace('motion','still')],['currentSrc',expected.replace('motion','still')],['complete',false],['naturalWidth',759],['naturalHeight',399],['isConnected',false]]){
   const old=img[key];img[key]=value;if(ready(expected))throw Error('Wrong state accepted '+key);img[key]=old;
 }
 document.querySelector=()=>null;if(ready(expected))throw Error('Missing image accepted');
})().catch(e=>{console.error(e);process.exitCode=1});
""".replace('PREDICATE',json.dumps(suite.IMAGE_READY))
        subprocess.run(['node','-e',harness],check=True,capture_output=True,text=True)

    def test_actual_decode_promise_has_deadline_and_cleans_every_timer(self):
        import subprocess
        harness=r"""
const decode=eval('('+DECODE+')');const assert=require('node:assert/strict');
const originalSet=setTimeout,originalClear=clearTimeout,active=new Set();
global.setTimeout=(f,ms)=>{let id;id=originalSet(()=>{active.delete(id);f()},ms);active.add(id);return id};
global.clearTimeout=id=>{active.delete(id);return originalClear(id)};
(async()=>{
 await decode({decode:()=>Promise.resolve()},40);assert.equal(active.size,0);
 await assert.rejects(decode({decode:()=>Promise.reject(Error('bad image'))},40),/bad image/);assert.equal(active.size,0);
 await assert.rejects(decode({decode:()=>{throw Error('synchronous decode error')}},40),/synchronous decode/);assert.equal(active.size,0);
 const start=Date.now();await assert.rejects(decode({decode:()=>new Promise(()=>{})},20),/Image decode timeout/);
 assert.ok(Date.now()-start<1000);assert.equal(active.size,0);
})().catch(e=>{console.error(e);process.exitCode=1});
""".replace('DECODE',json.dumps(suite.IMAGE_DECODE))
        subprocess.run(['node','-e',harness],check=True,capture_output=True,text=True,timeout=3)

    def test_readiness_helper_decode_failures_and_state_diagnostics(self):
        expected='https://aiwiki.test/assets/concept-animations/reinforce-return-credit-motion.svg'
        valid=dict(src=expected,currentSrc=expected,complete=True,width=760,height=400,connected=True)
        for variant in [None,('src','wrong'),('currentSrc','wrong'),('complete',False),('width',759),('height',399),('decode','rejected'),('wait','timeout')]:
            page=Mock();img=Mock();img.count.return_value=1;record={};state=dict(valid)
            if variant and variant[0]not in ['decode','wait']:state[variant[0]]=variant[1]
            before=dict(valid,complete=False,width=0,height=0)
            if variant and variant[0]=='decode':img.evaluate.side_effect=[before,RuntimeError('decode rejected'),state]
            elif variant and variant[0]=='wait':
                page.wait_for_function.side_effect=TimeoutError('image stayed incomplete');img.evaluate.side_effect=[before,before]
            else:img.evaluate.side_effect=[before,None,state,state]
            if variant:
                with self.assertRaises((AssertionError,RuntimeError,TimeoutError)):suite.ready_image(page,img,expected,record,'controlled')
                self.assertEqual(record['image_states'][0]['status'],'failed');self.assertIn('failure_state',record['image_states'][0])
            else:
                suite.ready_image(page,img,expected,record,'controlled');self.assertEqual(record['image_states'][0]['status'],'passed')
            page.wait_for_function.assert_called_once_with(suite.IMAGE_READY,arg=expected,timeout=5000)
            if not variant or variant[0]!='wait':self.assertEqual(img.evaluate.call_args_list[1].args,(suite.IMAGE_DECODE,5000))

    def test_every_original_player_transition_has_exact_readiness_barrier(self):
        import ast
        source=(ROOT/'scripts/test_policy_gradient_motion_browser.py').read_text()
        tree,player,waits=validate_player_barriers(source)
        for index in range(6):
            changed=ast.parse(source);function=next(n for n in changed.body if isinstance(n,ast.FunctionDef)and n.name=='check_player')
            calls=[n for n in ast.walk(function)if isinstance(n,ast.Call)and isinstance(n.func,ast.Name)and n.func.id=='ready_image']
            calls[index].args[2]=ast.Constant(value='https://wrong.test/same-suffix-motion.svg')
            with self.assertRaises(AssertionError):validate_player_barriers(ast.unparse(changed))
            changed=ast.parse(source);function=next(n for n in changed.body if isinstance(n,ast.FunctionDef)and n.name=='check_player')
            statements=[n for n in function.body if isinstance(n,ast.Expr)and isinstance(n.value,ast.Call)and isinstance(n.value.func,ast.Name)and n.value.func.id=='ready_image']
            function.body.remove(statements[index])
            with self.assertRaises(AssertionError):validate_player_barriers(ast.unparse(changed))
        main=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='main')
        self.assertTrue(any(isinstance(n,ast.Assert)and ast.unparse(n.test)=="not record['failed_requests']"for n in ast.walk(main)))
        source=ast.unparse(player);self.assertIn('request.failure',source);self.assertIn("record['failed_requests'].append(request.url)",source)

    def test_ci_execution_and_evidence(self):
        d=yaml.safe_load((ROOT/'.github/workflows/built-motion-browser.yml').read_text())
        if 'support-browser' in d['jobs']:
            steps=d['jobs']['support-browser']['steps'];run=next(x for x in steps if x.get('run')=='python scripts/run_motion_shard_support.py')
            self.assertNotIn('if',run);self.assertNotIn('continue-on-error',run)
            registry=json.loads((ROOT/'scripts/fixtures/browser-support-suites.json').read_text());entry=next(x for x in registry['suites'] if x['id']=='policy-gradient-motion')
            self.assertEqual(entry['command'],['scripts/test_policy_gradient_motion_browser.py']);self.assertEqual(len(entry['expected_cases']),24);self.assertEqual(len(entry['expected_pngs']),114)
            runs=[x.get('run','')for j in d['jobs'].values()for x in j['steps']]
            self.assertTrue(any('python scripts/test_policy_gradient_restore.py' in x.splitlines() for x in runs))
            self.assertTrue(any(x.get('uses','').startswith('actions/upload-artifact@') for x in steps))
        else:
            steps=d['jobs']['built-motion-browser']['steps'];self.assertTrue(any(x.get('run')=='python scripts/test_policy_gradient_motion_browser.py'for x in steps));self.assertTrue(any(x.get('run')=='python scripts/test_policy_gradient_restore.py'for x in steps));upload=next(x for x in steps if x.get('with',{}).get('name')=='policy-gradient-motion-review');self.assertEqual(upload['if'],'always()');self.assertEqual(upload['with']['path'],'artifacts/policy-gradient-motion/');self.assertEqual(upload['with']['if-no-files-found'],'error')

    def test_controls_and_native_glyph_contract_retained(self):
        src=(ROOT/'scripts/test_policy_gradient_motion_browser.py').read_text()
        for token in ['getBBox()','page.keyboard.press("Enter")','page.keyboard.press("Space")','i.naturalWidth===760','dimensions["scroll"]>=760','region.focus()','s.pauseAnimations(); s.setCurrentTime(t)']:self.assertIn(token,src)

if __name__=='__main__':unittest.main()
