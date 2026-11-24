"""Independent timing and state checks for the illustrative working-memory demos."""
from pathlib import Path
import unittest,xml.etree.ElementTree as E,subprocess,json,math
ROOT=Path(__file__).resolve().parents[1];N='{http://www.w3.org/2000/svg}'
def sample(a,t):
 ts=list(map(float,a.get('keyTimes').split(';')));vs=list(map(float,a.get('values').split(';')))
 i=max(i for i,x in enumerate(ts[:-1]) if x<=t)
 return vs[i] if a.get('calcMode')=='discrete' else vs[i]+(vs[i+1]-vs[i])*(t-ts[i])/(ts[i+1]-ts[i])
class WorkingMemorySemantics(unittest.TestCase):
 def test_gate_arrival_and_complementary_phases(self):
  r=E.parse(ROOT/'docs/assets/concept-animations/pbwm-gate-motion.svg').getroot()
  gates=[e.find(N+'animate') for e in r.iter(N+'rect') if e.get('x')=='317']
  letters={e.text:e.find(N+'animate') for e in r.iter(N+'text') if e.text in ['A','B']}
  tokens={e.get('fill'):next(a for a in e if a.get('attributeName')=='cx') for e in r.iter(N+'circle') if e.get('r')=='12'}
  for i in range(10000):
   t=i/10000;self.assertEqual(sum(sample(a,t) for a in gates),1)
   self.assertEqual(sample(gates[0],t),int(not 1/3<=t<2/3))
   self.assertEqual(sample(letters['A'],t),int(.25<=t<11/12));self.assertEqual(sample(letters['B'],t),int(t>=11/12))
   if sample(letters['A'],t):self.assertEqual(sample(tokens['#3274e5'],t),480)
   if sample(letters['B'],t):self.assertEqual(sample(tokens['#009e9b'],t),480)
   self.assertLessEqual(sample(tokens['#e59a3b'],t)+12,317)
 def test_trace_does_not_anticipate_burst(self):
  for kind in ['motion','still']:
   s=(ROOT/f'docs/assets/concept-animations/activity-silent-trace-{kind}.svg').read_text()
   self.assertIn('133,333' if kind=='motion' else '133,332',s);self.assertIn('552,318 565,264' if kind=='motion' else '553,320 565,259',s)
 def test_actual_js_math_all_controls(self):
  js=(ROOT/'docs/javascripts/working-memory-labs.js').read_text()
  code="global.window={};global.document={readyState:'complete',querySelectorAll:()=>[]};"+js+";console.log(JSON.stringify({g:[false,true].flatMap(x=>[false,true].flatMap(b=>[0,1,2,3].map(t=>[x,b,t,window.WMTeachingMath.gateState(t,x,b)]))),s:Array.from({length:14},(_,i)=>1.5+i*.5).flatMap(k=>[false,true].map(r=>[k,r,window.WMTeachingMath.silentTrace(k,r)]))}));"
  data=json.loads(subprocess.check_output(['node','-e',code],text=True))
  for x,b,t,state in data['g']:
   memory='–'
   for j in range(1,t+1):
    if [False,True,x,b][j]:memory=['–','A','X','B'][j]
   self.assertEqual(state['memory'],memory)
  for k,r,state in data['s']:
   for t,value in enumerate(state['trace']):
    expected=math.exp(-t/k)+(.55*math.exp(-(t-4)/k) if r and t>=4 else 0)
    self.assertAlmostEqual(value,expected,places=14);self.assertEqual(state['spike'][t],int(t==0 or (r and t==4)))
    self.assertTrue(30<187-65*value<207)
 def test_bilingual_source_scroll_and_caveats(self):
  for topic,stem in [('pbwm','pbwm-gate'),('activity-silent-working-memory','activity-silent-trace')]:
   for suffix in ['', '.zh-TW']:
    s=(ROOT/f'docs/brain-mind/working-memory-executive-function/{topic}/index{suffix}.md').read_text()
    self.assertIn('wm-motion-pan concept-motion-scroll',s);self.assertIn('tabindex="0"',s);self.assertIn('data-source-asset-urls',s)
    self.assertIn(stem+'-still.svg',s);self.assertIn(stem+'-motion.svg',s);self.assertIn('重設' if suffix else 'resets',s)
if __name__=='__main__':unittest.main()
