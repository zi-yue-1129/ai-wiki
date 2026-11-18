import bisect,subprocess,unittest,xml.etree.ElementTree as E
from pathlib import Path
R=Path(__file__).resolve().parents[1];N='{http://www.w3.org/2000/svg}'
def val(a,t):
 v=list(map(float,a.get('values').split(';')));k=list(map(float,a.get('keyTimes',';'.join(str(i/(len(v)-1)) for i in range(len(v)))).split(';')));i=min(bisect.bisect_right(k,t)-1,len(k)-2)
 if a.get('calcMode')=='discrete':return v[-1] if t==1 else v[i]
 f=(t-k[i])/(k[i+1]-k[i]);return v[i]*(1-f)+v[i+1]*f
class Planning(unittest.TestCase):
 def test_actual_graph_layers_and_full_backtracking_causality(self):
  r=E.parse(R/'docs/assets/concept-animations/graphplan-layer-extraction-motion.svg').getroot()
  stages={e.get('id'):e for e in r.iter() if e.get('id')};starts={'action-A0':.14,'action-A1':.4,'F1-support-mutex':.4,'F2-support':.68,'persist-F1':.4,'persist-F2':.68,'backward-extraction':.72}
  starts.update({f'fact-F1-{i}':.4 for i in [18,19]});starts.update({f'fact-F2-{i}':.68 for i in [20,21,22]})
  trace=stages['backward-extraction'];self.assertEqual(trace.get('pathLength'),'1');self.assertEqual(trace.get('stroke-dasharray'),'1 1');dash=next(a for a in trace if a.get('attributeName')=='stroke-dashoffset')
  for i in range(10001):
   t=i/10000
   for id,start in starts.items():
    a=next(a for a in stages[id] if a.get('attributeName')=='opacity');self.assertEqual(val(a,t),1 if start<=t<1 else 0)
   self.assertGreaterEqual(val(dash,t),0);self.assertLessEqual(val(dash,t),1)
   if t>=.92:self.assertEqual(val(dash,t),0)
  facts=[{'A'}]
  for _ in range(2):facts.append(facts[-1]|{b for a,b in [('A','B'),('B','C')] if a in facts[-1]})
  self.assertEqual(facts,[{'A'},{'A','B'},{'A','B','C'}])
  # Independent reachability proves different location facts are mutex, despite layer union.
  states={frozenset({'A'})}
  for _ in range(2):states=states|{frozenset((set(s)-{a})|{b}) for s in states for a,b in [('A','B'),('B','C')] if a in s}
  self.assertTrue(all(len(s)==1 for s in states));self.assertIn(frozenset({'C'}),states)
 def test_actual_lab_computation_and_interrupted_controls(self):
  subprocess.run(['node','scripts/test_planning_lab_semantics.cjs'],cwd=R,check=True)
 def test_strips_atomic_effects_and_native_legibility(self):
  for stem in ['strips-state-effects','graphplan-layer-extraction']:
   for kind in ['motion','still']:
    r=E.parse(R/f'docs/assets/concept-animations/{stem}-{kind}.svg').getroot();self.assertTrue(all(float(t.get('font-size','12'))>=12 for t in r.iter(N+'text')))
  r=E.parse(R/'docs/assets/concept-animations/strips-state-effects-motion.svg').getroot();texts=[t.text for t in r.iter(N+'text')];self.assertEqual(texts.count('Charged'),2)
  a=next(a for a in r.iter(N+'animate') if a.get('attributeName')=='cx');self.assertEqual(val(a,0),280);self.assertEqual(val(a,.75),360)
if __name__=='__main__':unittest.main()
