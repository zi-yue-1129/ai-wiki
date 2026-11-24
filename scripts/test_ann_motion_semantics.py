"""Independent ANN geometry, causal reveal, and bilingual source regressions."""
from pathlib import Path
import unittest,re,xml.etree.ElementTree as E
N='{http://www.w3.org/2000/svg}';ROOT=Path(__file__).resolve().parents[1];A=ROOT/'docs/assets/concept-animations'
def root(stem):return E.parse(A/(stem+'-motion.svg')).getroot()
def value(a,t):
 ts=list(map(float,a.get('keyTimes').split(';')));v=list(map(float,a.get('values').split(';')))
 i=max(i for i,x in enumerate(ts) if x<=t)
 if i==len(ts)-1 or a.get('calcMode')=='discrete':return v[i]
 return v[i]+(v[i+1]-v[i])*(t-ts[i])/(ts[i+1]-ts[i])
class ANN(unittest.TestCase):
 def test_hnsw_connected_motion_and_causal_summary(self):
  r=root('hnsw-layer-descent');tokens=[e for e in r.iter(N+'circle') if e.find(N+'animate') is not None and e.get('r') in ['11','3.5']]
  edges=[tuple(float(e.get(k)) for k in ['x1','y1','x2','y2']) for e in r.iter(N+'line') if float(e.get('x1'))<400 and float(e.get('x2'))<400]
  for tok in tokens:
   ax,ay=tok.findall(N+'animate')
   for i in range(1001):
    t=i/1001;x,y=value(ax,t),value(ay,t)
    self.assertTrue(any(abs((x-x1)*(y2-y1)-(y-y1)*(x2-x1))<1e-6 and min(x1,x2)-1e-6<=x<=max(x1,x2)+1e-6 and min(y1,y2)-1e-6<=y<=max(y1,y2)+1e-6 for x1,y1,x2,y2 in edges))
  for e in r.iter(N+'circle'):
   if e.get('r')!='12' or e.find(N+'animate') is None:continue
   arrival={'141':.32,'207':.60,'273':.88}[e.get('cy')];a=e.find(N+'animate')
   for i in range(1001):self.assertEqual(value(a,i/1001),int(i/1001>=arrival))
 def test_toy_greedy_distances_and_coarse_selection(self):
  # This verifies the illustrated order only, not global HNSW recall.
  self.assertEqual(sorted([86,224,347],key=lambda x:abs(x-298)),[347,224,86])
  for start,end in [(347,315),(315,298)]:self.assertLess(abs(end-298),abs(start-298))
  q=(240,189);centroids=[(115,176),(270,143),(268,274)]
  ds=[sum((a-b)**2 for a,b in zip(q,c)) for c in centroids]
  self.assertEqual(sorted(range(3),key=lambda i:ds[i])[:2],[1,2])
 def test_pq_probe_then_terms_then_total(self):
  r=root('ivfpq-probe-pq-lookup');rects={e.get('y'):e.find(N+'animate') for e in r.iter(N+'rect') if e.find(N+'animate') is not None}
  for i in range(1001):
   t=i/1001;active=[y for y,a in rects.items() if value(a,t)]
   self.assertLessEqual(len(active),1)
   if active:self.assertGreaterEqual(t,.35)
   if '269' in active:self.assertGreaterEqual(t,.91)
  terms=[.3**2,.4**2,.2**2];self.assertAlmostEqual(sum(terms),.29)
  text=[''.join(e.itertext()) for e in r.iter(N+'text')]
  for x in ['0.09','0.16','0.04','0.29']:self.assertIn(x,text)
  circle=next(e for e in r.iter(N+'circle') if e.find(N+'animate') is not None)
  for a in circle.findall(N+'animate'):
   self.assertEqual(value(a,.9),float(a.get('values').split(';')[-1]))
 def test_bilingual_hooks_and_display_math(self):
  for topic,stem in [('hnsw','hnsw-layer-descent'),('ivf-pq-faiss','ivfpq-probe-pq-lookup')]:
   for lang in ['', '.zh-TW']:
    s=(ROOT/f'docs/engineering/vector-databases/{topic}{lang}.md').read_text()
    for token in ['data-source-asset-urls','tabindex="0"','overflow-x:auto',f'{stem}-still.svg',f'{stem}-motion.svg']:self.assertIn(token,s)
    self.assertNotRegex(s,r'(?m)^\$$')
    inline=re.findall(r'(?<!\$)\$([^$\n]+)\$(?!\$)',re.sub(r'\$\$.*?\$\$', '', s, flags=re.S))
    self.assertTrue(all(len(eq)<75 for eq in inline))
if __name__=='__main__':unittest.main()
