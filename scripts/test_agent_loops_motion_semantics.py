"""Causal stage arrival, continuous axis-aligned guides, and readable source hooks."""
from pathlib import Path
import unittest,xml.etree.ElementTree as E,re,math
N='{http://www.w3.org/2000/svg}';P=Path(__file__).resolve().parents[1];A=P/'docs/assets/concept-animations'
CASES={'react-evidence-loop':([0,.15,.3,.5,.65,.8,.92],[(116,153),(319,153),(524,153),(116,285),(319,285),(524,285),(564,327)]),'reflexion-memory-feedback':([0,.14,.28,.43,.56,.70,.82,.94],[(114,159),(318,159),(524,159),(580,236),(318,236),(114,300),(318,300),(524,300)])}
def root(stem):return E.parse(A/f'{stem}-motion.svg').getroot()
def value(a,t):
 ts=list(map(float,a.get('keyTimes').split(';')));vs=list(map(float,a.get('values').split(';')));i=max(i for i,x in enumerate(ts) if x<=t)
 if i==len(ts)-1 or a.get('calcMode')=='discrete':return vs[i]
 return vs[i]+(vs[i+1]-vs[i])*(t-ts[i])/(ts[i+1]-ts[i])
class AgentLoops(unittest.TestCase):
 def test_arrivals_and_causal_highlights_dense(self):
  for stem,(arrivals,anchors) in CASES.items():
   r=root(stem);m=next(e for e in r.iter() if e.get('id')=='progress-marker');ax,ay=m.findall(N+'animate');stages={int(e.get('id').split('-')[1]):e.find(N+'animate') for e in r.iter() if (e.get('id') or '').startswith('stage-')}
   self.assertEqual(len(stages),len(arrivals));self.assertEqual(ax.get('keyTimes'),ay.get('keyTimes'));self.assertFalse(list(r.iter(N+'animateMotion')))
   for t,(x,y) in zip(arrivals,anchors):self.assertAlmostEqual(value(ax,t),x);self.assertAlmostEqual(value(ay,t),y)
   for j in range(10001):
    t=j/10001;active=[i for i,a in stages.items() if value(a,t)==1];self.assertEqual(active,[max(i for i,a in enumerate(arrivals) if a<=t)])
   xs=list(map(float,ax.get('values').split(';')));ys=list(map(float,ay.get('values').split(';')))
   self.assertTrue(all(x0==x1 or y0==y1 for x0,x1,y0,y1 in zip(xs,xs[1:],ys,ys[1:])))
   self.assertEqual((xs[-1],ys[-1]),anchors[-1])
 def test_dense_marker_text_clearance(self):
  for stem in CASES:
   r=root(stem);m=next(e for e in r.iter() if e.get('id')=='progress-marker');ax,ay=m.findall(N+'animate');radius=float(m.get('r'))+float(m.get('stroke-width'))/2;boxes=[]
   for e in r.iter(N+'text'):
    txt=''.join(e.itertext());x,y=float(e.get('x')),float(e.get('y'));fs=float(e.get('font-size'));width=len(txt)*fs*.62
    if e.get('text-anchor')=='middle':x-=width/2
    boxes.append((x,x+width,y-.8*fs,y+(.2*fs if any(c in txt for c in 'gjpqy') else 0),txt))
   for j in range(10001):
    t=j/10001;x,y=value(ax,t),value(ay,t);self.assertTrue(radius<=x<=640-radius and radius<=y<=360-radius)
    for l,rr,top,bottom,txt in boxes:
     dx=max(l-x,0,x-rr);dy=max(top-y,0,y-bottom)
     self.assertGreaterEqual(math.hypot(dx,dy),radius,msg=f'{stem} t={t} touches {txt}')
 def test_static_markers_use_readable_route_anchors(self):
  for stem,xy in [('react-evidence-loop',(524,153)),('reflexion-memory-feedback',(318,236))]:
   r=E.parse(A/f'{stem}-still.svg').getroot();m=list(r.iter(N+'circle'))[-1]
   self.assertEqual((float(m.get('cx')),float(m.get('cy'))),xy)
 def test_bilingual_source_and_no_trace_claim(self):
  for topic,stem in [('react','react-evidence-loop'),('reflexion','reflexion-memory-feedback')]:
   for lang in ['', '.zh-TW']:
    s=(P/f'docs/engineering/agents/{topic}{lang}.md').read_text()
    for token in ['data-source-asset-urls','tabindex="0"','overflow-x:auto','width:640px;min-width:640px',f'{stem}-still.svg',f'{stem}-motion.svg']:self.assertIn(token,s)
    self.assertIn('循環重設' if lang else 'loop reset',s)
    if topic=='reflexion':self.assertIn('不保證' if lang else 'does not guarantee',s)
if __name__=='__main__':unittest.main()
