"""Read actual authored SMIL coordinates, not merely a duplicate toy calculation."""
import bisect,math,re,unittest,xml.etree.ElementTree as E
from pathlib import Path
from test_gradient_clipping_motion_semantics import clip,validate
from verify_concept_motion import verify_source_pair
R=Path(__file__).resolve().parents[1];A=R/'docs/assets/concept-animations';N='{http://www.w3.org/2000/svg}'
STEMS=['gradient-clipping-comparison','gradient-accumulation-clipping-order','gradient-global-layer-budget','gradient-amp-unscale-order','gradient-agc-relative-cap','gradient-decoupled-decay']
def root(stem,kind='motion'):return E.parse(A/f'{stem}-{kind}.svg').getroot()
def sample(a,t):
 v=list(map(float,a.get('values').split(';')));ts=list(map(float,a.get('keyTimes').split(';'))) if a.get('keyTimes') else [i/(len(v)-1) for i in range(len(v))]
 if t>=1:return v[-1]
 i=max(0,min(len(v)-2,bisect.bisect_right(ts,t)-1));return v[i] if a.get('calcMode')=='discrete' else v[i]+(v[i+1]-v[i])*(t-ts[i])/(ts[i+1]-ts[i])
def attr(el,name,t):
 a=next((x for x in el.findall(N+'animate') if x.get('attributeName')==name),None);return sample(a,t) if a is not None else float(el.get(name))
def vector(el,t,scale):return ((attr(el,'x2',t)-float(el.get('x1')))/scale,(float(el.get('y1'))-attr(el,'y2',t))/scale)
def animated(r,tag):return [e for e in r.iter(N+tag) if e.find(N+'animate') is not None]
class ActualGradient(unittest.TestCase):
 def close(self,a,b,tol=.0005):
  for x,y in zip(a,b):self.assertAlmostEqual(x,y,delta=tol)
 def test_original_examples(self):self.assertEqual(validate(),[])
 def test_comparison_vectors_and_component_bars(self):
  r=root(STEMS[0]);lines=animated(r,'line');bars=animated(r,'rect');self.assertEqual(len(lines),3);self.assertEqual(len(bars),4)
  for i in range(1001):
   t=i/1000;s=.35+.65*(1-abs(2*t-1));raw=(4*s,2*s);norm=clip(raw,2);coord=tuple(min(x,1.5) for x in raw)
   self.close(vector(lines[0],t,50),raw);self.close(vector(lines[1],t,50),coord,.004);self.close(vector(lines[2],t,50),norm,.004)
   for e,x in zip(bars,[*norm,*coord]):self.assertAlmostEqual(attr(e,'width',t)/55.25,x,delta=.004)
 def test_accumulation_orders_actual_vectors(self):
  lines=animated(root(STEMS[1]),'line');self.assertEqual(len(lines),4)
  for i in range(1001):
   t=i/1000;s=1-abs(2*t-1);self.close(vector(lines[0],t,40),(2,s));self.close(vector(lines[1],t,40),(1,s));self.close(vector(lines[2],t,40),(2,s));self.close(vector(lines[3],t,40),clip((2,s),2),.001)
 def test_global_budget_actual_vectors_and_markers(self):
  r=root(STEMS[2]);lines=animated(r,'line');dots=animated(r,'circle')
  for i in range(1001):
   t=i/1000;s=1-abs(2*t-1);raw=(4,3*s);g=clip(raw,4)
   self.close(vector(lines[0],t,39),raw);self.close(vector(lines[1],t,39),g,.001);self.close(vector(lines[2],t,39),raw)
   for dot,line in zip(dots,lines[1:]):self.close((attr(dot,'cx',t),attr(dot,'cy',t)),(attr(line,'x2',t),attr(line,'y2',t)),1e-9)
 def test_agc_exact_piecewise_cap_crossings(self):
  bars=animated(root(STEMS[4]),'rect');self.assertEqual(len(bars),4)
  for i in range(10001):
   t=i/10000;s=.4+2.6*(1-abs(2*t-1))
   for e,v in zip(bars,[s,min(s,.5),s,min(s,2)]):self.assertAlmostEqual(attr(e,'width',t)/142,v,places=12)
 def test_amp_causal_highlights_and_labels(self):
  r=root(STEMS[3]);groups=animated(r,'g');self.assertEqual(len(groups),4)
  for t,expected in [(0,[.1,.1,.1,.1]),(.35,[1,.1,1,.1]),(.7,[1,1,1,1])]:self.close([attr(g,'opacity',t) for g in groups],expected,1e-12)
  texts=[e.text for e in r.iter(N+'text')];self.assertIn('Final norm: 2',texts);self.assertIn('Final norm: 0.5',texts)
  for group,label,value in zip(groups,['Unscale','Clip','Clip','Unscale'],['5','2','2','0.5']):self.assertEqual([e.text for e in group.iter(N+'text')],[label,value])
 def test_decay_geometry_scale_and_reveal(self):
  r=root(STEMS[5]);paths=list(r.iter(N+'path'));self.assertEqual([p.get('d') for p in paths],['M304 213 L192 213','M192 213 L108 325','M304 213 L108 325'])
  self.close(((-112-84)/280,-112/280),(-.7,-.4),1e-12)
  bars=[e for e in r.iter(N+'rect') if e.get('fill') in ['#6ed3ca','#f1b66e']];self.assertAlmostEqual(float(bars[1].get('width'))/float(bars[0].get('width')),math.sqrt(.65)/.4,delta=.001)
  for t,v in [(0,150),(.25,150),(.65,0),(.85,0),(1,150)]:self.assertEqual(attr(paths[1],'stroke-dashoffset',t),v)
  for t,v in [(0,0),(.25,0),(.65,1),(.85,1),(1,0)]:self.assertEqual(attr(bars[1],'opacity',t),v)
 def test_static_endpoints_and_no_active_motion(self):
  for stem in STEMS:self.assertFalse(list(root(stem,'still').iter(N+'animate')))
  r=root(STEMS[0],'still');ls=[e for e in r.iter(N+'line') if e.get('marker-end')];self.close(vector(ls[0],0,50),(4,2));self.close(vector(ls[1],0,50),(1.5,1.5));self.close(vector(ls[2],0,50),clip((4,2),2))
  r=root(STEMS[1],'still');ls=[e for e in r.iter(N+'line') if e.get('marker-end')];self.close(vector(ls[0],0,40),(1,1));self.close(vector(ls[1],0,40),clip((2,1),2))
  r=root(STEMS[2],'still');ls=[e for e in r.iter(N+'line') if e.get('stroke-width')=='5'];self.close(vector(ls[0],0,39),(3.2,2.4));self.close(vector(ls[1],0,39),(4,3))
  r=root(STEMS[4],'still');bars=[e for e in r.iter(N+'rect') if e.get('fill') in ['#e0a45d','#6ed3ca','#8da9f9']];self.close([float(e.get('width'))/142 for e in bars],[3,.5,3,2],1e-12)
 def test_bilingual_sources_focus_and_eight_hundred_canvas(self):
  for suffix in ['.md','.zh-TW.md']:
   p=R/f'docs/theory/optimization/gradient-clipping-and-normalisation{suffix}';s=p.read_text();self.assertEqual(s.count('class="gradient-source-scroll"'),6);self.assertEqual(s.count('tabindex="0"'),6);self.assertEqual(s.count('style="width:800px;min-width:800px;max-width:none;height:auto"'),6)
   for stem in STEMS:self.assertEqual(verify_source_pair(p,s,stem),[])
class NativeFixtureContract(unittest.TestCase):
 def test_fixture_matches_actual_source_asset_paths_and_old_path_is_rejected(self):
  import ast
  from html.parser import HTMLParser
  class Images(HTMLParser):
   def __init__(self,html):super().__init__();self.images=[];self.feed(html)
   def handle_starttag(self,tag,attrs):
    if tag=='img':self.images.append(dict(attrs))
  def check(source):
   tree=ast.parse(source)
   calls=[n for n in ast.walk(tree)if isinstance(n,ast.Call)and isinstance(n.func,ast.Attribute)]
   htmlarg=next(n.args[0]for n in calls if n.func.attr=='set_content')
   route=next(n.args[0].value for n in calls if n.func.attr=='route')
   assert route=='**/assets/concept-animations/*.svg'
   for stem in STEMS:
    html=eval(compile(ast.Expression(htmlarg),'<actual native fixture>','eval'),{'css':'','stem':stem,'alt':'test','size':800})
    image=Images(html).images[0]
    assert image['src']==f'https://wiki.example/assets/concept-animations/{stem}-still.svg'
    assert image['data-motion-src']==f'https://wiki.example/assets/concept-animations/{stem}-motion.svg'
    for suffix in ('.md','.zh-TW.md'):
     doc=(R/f'docs/theory/optimization/gradient-clipping-and-normalisation{suffix}').read_text()
     assert any(i.get('src','').endswith('assets/concept-animations/'+stem+'-still.svg')for i in Images(doc).images)
  source=(R/'scripts/test_gradient_source_browser.py').read_text();check(source)
  for bad in (source.replace('https://wiki.example/assets/concept-animations/','https://wiki.example/assets/'),source.replace('**/assets/concept-animations/*.svg','**/assets/*.svg')):
   with self.assertRaises(AssertionError):check(bad)
 def test_real_producer_failure_records_diagnostics_and_reraises(self):
  import tempfile,json
  from unittest.mock import MagicMock,patch
  import test_gradient_source_browser as b
  manager=MagicMock();browser=manager.__enter__.return_value.chromium.launch.return_value;page=browser.new_page.return_value
  page.evaluate.side_effect=[320,{'readyState':'complete','eligible':0,'buttons':0}]
  page.locator.return_value.count.return_value=0;page.content.return_value='<html>old fixture diagnostic</html>'
  with tempfile.TemporaryDirectory()as directory,patch.object(b,'OUT',Path(directory)),patch.object(b,'sync_playwright',return_value=manager):
   with self.assertRaises(AssertionError):b.main()
   report=json.loads((Path(directory)/'report.json').read_text())
   self.assertEqual(report['status'],'failed');self.assertEqual(report['cases'][0]['status'],'failed')
   self.assertEqual(report['cases'][0]['dom']['eligible'],0)
   self.assertTrue(list(Path(directory).glob('*-failure.html')));page.screenshot.assert_called_once();page.close.assert_called_once()
 def test_actual_js_selector_rejects_original_fixture(self):
  import subprocess
  result=subprocess.run(['node','scripts/test_gradient_source_player.cjs'],cwd=R,capture_output=True,text=True)
  self.assertEqual(result.returncode,0,result.stderr)
  self.assertIn('24 wrong-path selector negatives plus 24 actual gradient player',result.stdout)

 def test_future_only_changed_test_files_reach_native_and_semantic_steps(self):
  import yaml,fnmatch,copy
  w=yaml.safe_load((R/'.github/workflows/concept-animation-validation.yml').read_text())
  paths=['scripts/test_gradient_source_browser.py','scripts/test_gradient_source_player.cjs','scripts/test_gradient_actual_motion_semantics.py']
  commands=['python scripts/test_gradient_source_browser.py','node scripts/test_gradient_source_player.cjs','python scripts/test_gradient_actual_motion_semantics.py']
  def verify(w):
   patterns=w.get('on',w.get(True))['pull_request']['paths']
   assert all(any(fnmatch.fnmatchcase(p,g)for g in patterns)for p in paths)
   job=w['jobs']['validate-motion'];assert 'if' not in job
   runs=[]
   for step in job['steps']:
    if 'if' not in step and (step.get('continue-on-error') is None or step.get('continue-on-error') is False):runs.extend(line.strip()for line in step.get('run','').splitlines())
   assert all(c in runs for c in commands)
  verify(w)
  for path in paths:
   bad=copy.deepcopy(w);bad.get('on',bad.get(True))['pull_request']['paths'].remove(path)
   with self.assertRaises(AssertionError):verify(bad)
  for condition in (False,None,'always()'):
   bad=copy.deepcopy(w)
   for step in bad['jobs']['validate-motion']['steps']:
    if 'python scripts/test_gradient_source_browser.py' in step.get('run',''):step['if']=condition
   with self.assertRaises(AssertionError):verify(bad)

if __name__=='__main__':unittest.main()
