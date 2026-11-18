"""Actual Dreamer SVG arrival causality and independently expanded return targets."""
import math,re,unittest,xml.etree.ElementTree as E
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];ASSETS=ROOT/'docs/assets/concept-animations';N='{http://www.w3.org/2000/svg}'
STEMS=['dreamer-posterior-prior','dreamer-lambda-bootstrap']
def points(path,steps=1000):
    tokens=re.findall(r'[MCLSQ]|[-+]?(?:\d*\.\d+|\d+)',path);i=0;pos=(0.,0.);prev=None;out=[]
    while i<len(tokens):
        cmd=tokens[i];i+=1;count={'M':2,'L':2,'C':6,'S':4,'Q':4}[cmd]
        nums=list(map(float,tokens[i:i+count]));i+=count;pairs=list(zip(nums[::2],nums[1::2]))
        if cmd=='M':pos=pairs[0];out.append(pos);prev=None;continue
        controls=[pos]+pairs
        if cmd=='S':controls=[pos,tuple(2*pos[k]-prev[k] for k in (0,1))]+pairs
        degree=len(controls)-1
        for j in range(1,steps+1):
            t=j/steps
            out.append(tuple(sum(math.comb(degree,k)*(1-t)**(degree-k)*t**k*controls[k][axis] for k in range(degree+1)) for axis in (0,1)))
        pos=pairs[-1];prev=controls[-2] if degree>1 else None
    return out

def progress(a,t,field='values'):
    ts=list(map(float,a.get('keyTimes','0;1').split(';')));vs=list(map(float,a.get(field).split(';')))
    for i in range(len(ts)-1):
        if ts[i]<=t<ts[i+1]:
            return vs[i] if a.get('calcMode')=='discrete' else vs[i]+(vs[i+1]-vs[i])*(t-ts[i])/(ts[i+1]-ts[i])
    return vs[-1]

def point_at(ps,f):
    lengths=[0.]
    for a,b in zip(ps,ps[1:]):lengths.append(lengths[-1]+math.dist(a,b))
    target=f*lengths[-1]
    import bisect
    i=min(max(bisect.bisect_right(lengths,target)-1,0),len(ps)-2)
    frac=(target-lengths[i])/(lengths[i+1]-lengths[i])
    return tuple(ps[i][k]+frac*(ps[i+1][k]-ps[i][k]) for k in (0,1))


def causality(case,root,is_lambda):
    g=root.find(f"{N}g[@class='motion-only']")
    packets=[x for x in g if x.find(N+'animateMotion') is not None]
    arrivals=[float(x.find(N+'animateMotion').get('keyTimes').split(';')[-2]) for x in packets]
    rings=[x for x in g if x.tag==N+'circle' and x.get('cx')]
    relevant=arrivals if is_lambda else [arrivals[i] for i in [0,2,3,4]]
    for ring,arrival in zip(rings,relevant):
        opacity=ring.find(N+'animate')
        for i in range(10001):
            t=i/10000
            if t<arrival:case.assertAlmostEqual(progress(opacity,t),0)
    if is_lambda:
        masks=sorted([x for x in g if x.tag==N+'rect' and x.get('height')=='55'],key=lambda x:-float(x.get('x')))
        for mask,arrival in zip(masks,arrivals):
            a=mask.find(N+'animate');reveal=float(a.get('keyTimes','0;1').split(';')[2])
            case.assertGreaterEqual(float(a.get('keyTimes','0;1').split(';')[1]),arrival)
            for i in range(10001):
                t=i/10000
                if t<arrival:case.assertAlmostEqual(progress(a,t),1)
            case.assertEqual(progress(a,reveal+.001),0)
        for prev,nxt in zip(masks,packets[1:]):case.assertLess(float(prev.find(N+'animate').get('keyTimes').split(';')[2]),float(nxt.find(N+'animateMotion').get('keyTimes').split(';')[1]))
    else:
        case.assertEqual(len(packets),5);case.assertLessEqual(arrivals[0],float(packets[1].find(N+'animateMotion').get('keyTimes').split(';')[1]))
        for p,q in zip(packets[1:],packets[2:]):case.assertLessEqual(float(p.find(N+'animateMotion').get('keyTimes').split(';')[-2]),float(q.find(N+'animateMotion').get('keyTimes').split(';')[1]))
        case.assertEqual(packets[1].find(N+'animateMotion').get('path'),'M274 177 C274 218 109 188 109 251')
        heading=next(x for x in root.iter(N+'text') if x.text=='MODEL IMAGINATION');case.assertGreater(float(heading.get('x')),max(x for x,y in points(packets[1].find(N+'animateMotion').get('path'))))
        for p in packets[2:]:case.assertTrue(all(abs(y-285)<1e-9 for x,y in points(p.find(N+'animateMotion').get('path'),1)))

def returns(r,v,d,lam):
    g=[0]*len(r)+[v[-1]]
    for t in reversed(range(len(r))):g[t]=r[t]+d[t]*((1-lam)*v[t]+lam*g[t+1])
    return g
class DreamerTests(unittest.TestCase):
    def test_actual_svg_arrival_causality(self):
        for stem in STEMS:causality(self,E.parse(ASSETS/(stem+'-motion.svg')).getroot(),'lambda' in stem)
    def test_actual_rewards_targets_and_independent_nstep(self):
        root=E.parse(ASSETS/(STEMS[1]+'-still.svg')).getroot();texts=[x.text for x in root.iter(N+'text')];r=[float(re.fullmatch(r'r[123]=([0-9.]+)',x).group(1)) for x in texts if re.fullmatch(r'r[123]=([0-9.]+)',x)]
        self.assertEqual(r,[1,0,2]);v=[.8,1.1,1.5];gamma=.9;lam=.8;g=returns(r,v,[gamma]*3,lam)
        for t in range(3):
            n=3-t;ns=[sum(gamma**j*r[t+j] for j in range(k))+gamma**k*v[t+k-1] for k in range(1,n+1)];expanded=sum((1-lam)*lam**j*ns[j] for j in range(n-1))+lam**(n-1)*ns[-1];self.assertAlmostEqual(g[t],expanded);self.assertIn(f'{g[t]:.3f}',texts)
        self.assertAlmostEqual(g[0],3.0232)
        self.assertEqual(returns(r,v,[.9,0,.9],lam)[1],0)
        self.assertEqual(returns(r,[.8,1e6,1e9],[.9,0,.9],lam)[1],0)
        self.assertEqual(returns(r,v,[.9]*3,0)[:3],[r[i]+.9*v[i] for i in range(3)])
        self.assertAlmostEqual(returns(r,v,[.9]*3,1)[0],1+.9**2*2+.9**3*1.5)
    def test_source_layout_and_original_browser_coverage(self):
        for lang in ['','.zh-TW']:
            s=(ROOT/f'docs/theory/models/world-models/dreamer{lang}.md').read_text()
            self.assertEqual(s.count('tabindex="0"'),2);self.assertEqual(s.count('data-source-asset-urls'),2);self.assertEqual(s.count('width:640px;max-width:none'),2)
            for x in [r'p_t&=p(s_t\mid s_{t-1},a_{t-1},o_t)',r'q_t&=q(s_t\mid s_{t-1},a_{t-1})',r'd_{t+1}&=\gamma c_{t+1}',r'\gamma=0.9',r'\lambda=0.8','3.0232','CC BY-SA']:self.assertIn(x,s)
        b=(ROOT/'scripts/test_dreamer_motion_browser.py').read_text();self.assertIn('WIDTHS = (320, 360, 720, 1024)',b);self.assertIn('reduced_png == still_png',b);self.assertIn('TIMES = (0, 2, 2.5, 2.9, 5, 5.5, 8, 8.1, 10.6)',b);self.assertIn('getComputedStyle(e).opacity',b)
        for stem in STEMS:
            s=E.parse(ASSETS/(stem+'-still.svg')).getroot();self.assertFalse(any('animate' in x.tag for x in s.iter()))
    def test_negative_early_mask_and_ring_are_rejected(self):
        r=E.parse(ASSETS/(STEMS[1]+'-motion.svg')).getroot();m=r.find(f"{N}g[@class='motion-only']").find(N+'rect').find(N+'animate');m.set('keyTimes','0;.63;.69;.91;1')
        with self.assertRaises(AssertionError):causality(self,r,True)
        r=E.parse(ASSETS/(STEMS[0]+'-motion.svg')).getroot();ring=next(x for x in r.iter(N+'circle') if x.get('data-arrival'));ring.find(N+'animate').set('keyTimes','0;.15;.18;.25;1')
        with self.assertRaises(AssertionError):causality(self,r,False)
class DreamerXMLMount(unittest.TestCase):
    def test_actual_mount_parser_namespace_and_old_prefix_negative(self):
        import subprocess,json
        import test_dreamer_motion_browser as browser
        program = r"""
const vm=require('vm'),assert=require('assert');const source=JSON.parse(process.argv[1]);
for(const kind of ['valid','parsererror','wrong-root','wrong-namespace']){
 let parsed=0,imported=0,mounted=0;
 const root={localName:kind==='wrong-root'?'html':'svg',namespaceURI:kind==='wrong-namespace'?'bad':'http://www.w3.org/2000/svg'};
 const document={importNode:(r,deep)=>{assert.equal(r,root);assert.equal(deep,true);imported++;return r},body:{replaceChildren:r=>{assert.equal(r,root);mounted++}}};
 class DOMParser{parseFromString(xml,type){assert.equal(type,'image/svg+xml');assert.equal(xml,'<ns0:svg/>');parsed++;return {documentElement:root,querySelector:s=>{assert.equal(s,'parsererror');return kind==='parsererror'?{}:null}}}}
 const fn=vm.runInNewContext('('+source+')',{DOMParser,document});
 if(kind==='valid'){fn('<ns0:svg/>');assert.equal(imported,1);assert.equal(mounted,1)}
 else {assert.throws(()=>fn('<ns0:svg/>'));assert.equal(imported,0);assert.equal(mounted,0)}
 assert.equal(parsed,1);
}
"""
        subprocess.run(['node','-e',program,json.dumps(browser.MOUNT_SVG_JS)],check=True)
    def test_prefix_normalization_preserves_all_expanded_XML(self):
        import test_dreamer_motion_browser as browser
        def model(e):return (e.tag,dict(e.attrib),e.text,e.tail,[model(c) for c in e])
        for stem in STEMS:
            for mode in ['motion','still']:
                source=(ASSETS/f'{stem}-{mode}.svg').read_text()
                normalized=browser.inline_svg(source)
                prefixes=re.findall(r'xmlns:([\w-]+)=',source)
                tree=E.fromstring(source)
                for element in tree.iter():
                    for value in element.attrib.values():
                        for prefix in prefixes:self.assertNotRegex(value,rf'(?<![\w-]){re.escape(prefix)}[:|]')
                    if element.tag==N+'style':
                        self.assertNotIn('@namespace',element.text or '')
                        for prefix in prefixes:self.assertNotRegex(element.text or '',rf'(?<![\w-]){re.escape(prefix)}[:|]')
                self.assertTrue(normalized.startswith('<svg '))
                self.assertEqual(model(E.fromstring(source)),model(E.fromstring(normalized)))
        for bad in ['<svg','<svg/>','<svg xmlns="bad"/>']:
            with self.assertRaises((ValueError,E.ParseError)):browser.inline_svg(bad)

    def test_mount_failure_saves_and_rethrows(self):
        import tempfile
        from unittest.mock import Mock,patch
        import test_dreamer_motion_browser as browser
        page=Mock();page.evaluate.side_effect=RuntimeError('bad XML');page.content.return_value='<body>failure</body>';page.viewport_size={'width':320,'height':188}
        with tempfile.TemporaryDirectory() as d,patch.object(browser,'ARTIFACTS',Path(d)):
            with self.assertRaisesRegex(RuntimeError,'bad XML'):browser.mount(page,'<svg xmlns="http://www.w3.org/2000/svg"/>')
            self.assertEqual(__import__('json').loads((Path(d)/'mount-failure.json').read_text())['status'],'failed')
            self.assertTrue((Path(d)/'mount-failure.html').exists());page.screenshot.assert_called_once()
    def test_true_native_canary_and_all_case_constants(self):
        import ast
        import test_dreamer_motion_browser as browser
        self.assertEqual(browser.WIDTHS,(320,360,720,1024));self.assertEqual(browser.TIMES,(0,2,2.5,2.9,5,5.5,8,8.1,10.6))
        tree=ast.parse((ROOT/'scripts/test_dreamer_motion_browser.py').read_text())
        fn=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='namespace_canary')
        tests=[ast.unparse(x.test) for x in ast.walk(fn) if isinstance(x,ast.Assert)]
        self.assertTrue(any("count() == 0" in x for x in tests));self.assertTrue(any("count() == 1" in x for x in tests));self.assertTrue(any("setCurrentTime" in x for x in tests))
        workflow=(ROOT/'.github/workflows/concept-animation-validation.yml').read_text()
        self.assertIn('artifacts/dreamer-motion/**',workflow)

if __name__=='__main__':unittest.main()
