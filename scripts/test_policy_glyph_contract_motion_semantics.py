"""Real receipt-gate mutations and original producer arithmetic equivalence."""
import ast,copy,hashlib,json,math,unittest
from pathlib import Path
from xml.etree import ElementTree as ET
import policy_glyph_contract as g
ROOT=Path(__file__).resolve().parents[1]

def sample(stem='reinforce-return-credit',kind='motion',time=0):
    return dict(time=time,canvas=[0,0,760,400],boxes=[dict(label=label,x=10+(i%10)*60,y=10+(i//10)*30,w=10,h=10) for i,label in enumerate(g.EXPECTED_LABELS[stem+':'+kind])])

def mutations():
    out=[]
    def add(name,fn):
        s=sample();fn(s);out.append((name,s))
    add('empty_object',lambda s:s.update(boxes=[{}]))
    for k in ['label','x','y','w','h']:
        add('missing_'+k,lambda s,k=k:s['boxes'][0].pop(k))
    add('extra_box_field',lambda s:s['boxes'][0].update(extra=1))
    for k in ['x','y','w','h']:
        for value in [float('nan'),float('inf'),float('-inf'),True,False,'1',None]:
            add(k+'_'+repr(value),lambda s,k=k,v=value:s['boxes'][0].update({k:v}))
    for k in ['w','h']:add('negative_'+k,lambda s,k=k:s['boxes'][0].update({k:-1}))
    for k,value in [('x',9999),('y',-3),('w',800),('h',500)]:add('bounds_'+k,lambda s,k=k,v=value:s['boxes'][0].update({k:v}))
    add('overlap',lambda s:s['boxes'][1].update(x=10,y=10,w=10,h=10))
    for val in ['', ' ', None, 1, 'wrong']:
        add('label_'+repr(val),lambda s,v=val:s['boxes'][0].update(label=v))
    add('missing_glyph',lambda s:s['boxes'].pop())
    add('extra_glyph',lambda s:s['boxes'].append(dict(label='extra',x=600,y=300,w=1,h=1)))
    for val in [None,{},[0,0,640,360],[False,0,760,400],[0,0,760,float('nan')],[0,0,760,400,0]]:
        add('canvas_'+repr(val),lambda s,v=val:s.update(canvas=v))
    for val in [None,True,float('nan'),float('inf'),2,'0']:
        add('time_'+repr(val),lambda s,v=val:s.update(time=v))
    for k in ['time','canvas','boxes']:add('missing_sample_'+k,lambda s,k=k:s.pop(k))
    add('extra_sample_field',lambda s:s.update(extra=True))
    return out

class Glyphs(unittest.TestCase):
    def test_literals_match_reviewed_svg_all_labels_in_dom_order(self):
        for key,labels in g.EXPECTED_LABELS.items():
            stem,kind=key.split(':');root=ET.parse(ROOT/f'docs/assets/concept-animations/{stem}-{kind}.svg').getroot()
            self.assertEqual([''.join(e.itertext()) for e in root.iter() if e.tag.endswith('}text')],labels)
            self.assertEqual(root.get('viewBox'),'0 0 760 400')
    def test_all_fourteen_original_sample_positives(self):
        for key in g.EXPECTED_LABELS:
            stem,kind=key.split(':')
            for t in g.TIMES if kind=='motion' else [0]:g.validate_glyph_sample(sample(stem,kind,t),stem,kind,t)
    def test_all_malformed_measurements_fail_producer(self):
        for name,s in mutations():
            with self.subTest(name=name),self.assertRaises(AssertionError):g.validate_glyph_sample(s,'reinforce-return-credit','motion',0)
    def test_exact_original_tolerances_including_three_pixel_overlap(self):
        g.check_boxes([dict(label='edge',x=-2,y=-2,w=764,h=404)],'s','still',0)
        boxes=[dict(label='a',x=20,y=20,w=20,h=20),dict(label='b',x=37,y=20,w=20,h=20)]
        g.check_boxes(boxes,'s','motion',0)
        boxes[1]['x']=36.999
        with self.assertRaises(AssertionError):g.check_boxes(boxes,'s','motion',0)
    def test_new_helper_and_negative_suite_have_future_actual_ci_routes(self):
        import yaml
        from test_policy_future_routes_motion_semantics import validate
        w=yaml.safe_load((ROOT/'.github/workflows/built-motion-browser.yml').read_text())
        path=ROOT/'scripts/fixtures/browser-support-suites.json'
        registry=json.loads(path.read_text()) if path.exists() else None
        validate(w,registry)
        for bad_value in [False,'false']:
            bad=copy.deepcopy(w)
            job='support-browser' if 'support-browser' in bad['jobs'] else 'built-motion-browser'
            step=next(s for s in bad['jobs'][job]['steps'] if 'python scripts/test_policy_glyph_contract_motion_semantics.py' in s.get('run','').splitlines())
            step['if']=bad_value
            with self.subTest(condition=bad_value),self.assertRaises(AssertionError):validate(bad,registry)
        bad=copy.deepcopy(w)
        job='support-browser' if 'support-browser' in bad['jobs'] else 'built-motion-browser'
        step=next(s for s in bad['jobs'][job]['steps'] if 'python scripts/test_policy_glyph_contract_motion_semantics.py' in s.get('run','').splitlines())
        step['continue-on-error']=True
        with self.assertRaises(AssertionError):validate(bad,registry)
    def test_producer_and_gate_use_same_pure_contract(self):
        src=(ROOT/'scripts/test_policy_gradient_motion_browser.py').read_text()
        self.assertIn('validate_glyph_sample(sample, stem, kind, t)',src)
        self.assertIn("document.querySelector('svg').viewBox.baseVal",src)
        self.assertIn('getBBox()',src)
        if (ROOT/'scripts/motion_shard_contract.py').exists():
            self.assertIn("validate_glyph_sample(sample, spec['stem'], spec['kind'], expected_time)",(ROOT/'scripts/motion_shard_contract.py').read_text())

@unittest.skipUnless((ROOT/'scripts/motion_shard_contract.py').exists(),'Fifth is unsharded: same pure producer contract enforced above')
class Receipt(unittest.TestCase):
    def test_real_all_suite_fixture_and_every_mutation_with_rehashed_receipt(self):
        from test_motion_shard_ci import support_fixture
        from motion_shard_contract import validate_support
        m,r,a,p=support_fixture();self.assertEqual(validate_support(m,r,a,p)['status'],'passed')
        for name,sample_data in mutations():
            m,r,a,p=support_fixture();report=r['reports']['policy-gradient-motion'];report['cases'][0]['samples'][0]=sample_data
            raw=json.dumps(report,ensure_ascii=False,indent=2).encode();entry=next(f for f in r['pack']['files'] if f['path']=='policy-gradient-motion/report.json');entry.update(sha256=hashlib.sha256(raw).hexdigest(),size=len(raw))
            pack=r['pack'];pack['raw_bytes']=sum(f['size'] for f in pack['files']);pack['groups'][0]['raw_bytes']=pack['raw_bytes']
            with self.subTest(name=name),self.assertRaises(ValueError):validate_support(m,r,a,p)
if __name__=='__main__':unittest.main()
