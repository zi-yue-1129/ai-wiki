"""Read actual communication SVGs: numerical examples, path causality and negative controls."""
from pathlib import Path
import unittest,xml.etree.ElementTree as E,math
R=Path(__file__).resolve().parents[1];A=R/'docs/assets/concept-animations';N='{http://www.w3.org/2000/svg}'
STEMS=['rial-dial-credit-path','dial-dru-train-execute','commnet-leave-one-out','commnet-layer-iterations']
def root(stem,kind='motion'):return E.parse(A/f'{stem}-{kind}.svg').getroot()
def sample(a,t):
 v=list(map(float,a.get('values').split(';')));k=list(map(float,a.get('keyTimes').split(';')))
 for i in range(len(k)-1):
  if t<k[i+1]:return v[i] if a.get('calcMode')=='discrete' else v[i]+(v[i+1]-v[i])*(t-k[i])/(k[i+1]-k[i])
 return v[-1]
def anim(e,n):return e.find(N+f"animate[@attributeName='{n}']")
def packets(r):return [e for e in r.findall(N+'circle') if e.get('id')]
def check_layers(r):
 groups=[e for e in r.findall(N+'g') if anim(e,'opacity') is not None];assert len(groups)==2
 h=[.2,.8,.6];layers=[]
 for _ in range(2):h=[.5*x+.5*(sum(h)-x)/2 for x in h];layers.append(h)
 for g,vals in zip(groups,layers):
  texts=[t.text for t in g.iter(N+'text')]
  for v in vals:assert f'{v:.2f}'.removeprefix('0') in texts
 for t,expected in [(.2/12,[0,0]),(6.7/12,[1,0]),(9.5/12,[1,1])]:assert [sample(anim(g,'opacity'),t) for g in groups]==expected
 assert sample(anim(groups[0],'opacity'),.34)==0 and sample(anim(groups[1],'opacity'),.71)==0
class CommSource(unittest.TestCase):
 def test_dru_actual_values_modes_and_gradient(self):
  for kind in ['motion','still']:
   r=root(STEMS[1],kind);texts=[e.text for e in r.iter(N+'text')]
   self.assertIn(f'{1/(1+math.exp(-(.4-.1))):.3f}',texts);self.assertIn('1',texts);self.assertIn('m > 0',texts);self.assertIn('training only',texts);self.assertIn('no cross-agent gradient',texts)
  r=root(STEMS[1]);p=packets(r)[3];self.assertGreater(sample(anim(p,'cx'),.58),sample(anim(p,'cx'),.88));self.assertEqual(sample(anim(p,'opacity'),.46),0)
 def test_static_gradient_arrow_direction(self):
  for kind in ['motion','still']:
   r=root(STEMS[0],kind);points=[p.get('points') for p in r.findall(N+'polyline')]
   for expected in ['71,199 77,192 83,199','390,200 396,193 402,200','551,233 557,226 563,233']:self.assertIn(expected,points)
   r=root(STEMS[1],kind);self.assertEqual(r.find(N+"polyline[@id='receiver-gradient-arrival']").get('points'),'66,214 72,207 78,214')
 def test_actual_leave_one_out_mean(self):
  for kind in ['motion','still']:
   ts=[e.text for e in root(STEMS[2],kind).iter(N+'text')];self.assertIn(f'c_B = {(.2+.6)/2:.2f}',ts);self.assertIn('excluded',ts)
  self.assertNotEqual((.2+.8+.6)/3,(.2+.6)/2)
 def test_layer_values_reveals_and_negative(self):
  r=root(STEMS[3]);check_layers(r)
  next(e for e in r.iter(N+'text') if e.text=='.45').text='.46'
  with self.assertRaises(AssertionError):check_layers(r)
  r=root(STEMS[3]);anim(r.find(N+'g'),'opacity').set('keyTimes','0;0.1;0.2;0.96;1')
  with self.assertRaises(AssertionError):check_layers(r)
 def test_actual_visible_arrivals(self):
  bounds=[[(.08,.34,(208,151)),(.08,.34,(517,151)),(.48,.82,(396,194))],[(.06,.2,(126,167)),(.3,.46,(232,167)),(.3,.46,(591,167)),(.58,.88,(72,207))],[(.08,.34,(255,233)),(.08,.34,(385,233)),(.48,.62,(320,282))],[(.06,.22,(211,190)),(.06,.22,(211,190)),(.26,.34,(259,190)),(.43,.59,(429,190)),(.43,.59,(429,190)),(.63,.71,(477,190))]]
  for stem,entries in zip(STEMS,bounds):
   r=root(stem);self.assertEqual(len(r.findall('.//'+N+'animateMotion')),0);self.assertEqual(len(packets(r)),len(entries))
   for p,(start,end,xy) in zip(packets(r),entries):
    self.assertEqual(sample(anim(p,'opacity'),start-.001),0);self.assertEqual(sample(anim(p,'opacity'),end),1)
    for attr,v in zip(['cx','cy'],xy):self.assertAlmostEqual(sample(anim(p,attr),end),v)
    for j in range(1001):self.assertTrue(0<=sample(anim(p,'cx'),j/1000)<=640);self.assertTrue(0<=sample(anim(p,'cy'),j/1000)<=360)
   for a in r.findall('.//'+N+'animate'):self.assertEqual(a.get('begin'),'0s');self.assertEqual(a.get('dur'),'12s')
 def test_bilingual_source_contract_and_fallback(self):
  for topic in ['rial-dial','commnet']:
   for lang in ['', '.zh-TW']:
    s=(R/f'docs/theory/paradigms/reinforcement-learning/multi-agent-rl/emergent-communication/{topic}/index{lang}.md').read_text();self.assertEqual(s.count('class="comm-source-scroll" tabindex="0"'),2);self.assertEqual(s.count('data-source-asset-urls'),2)
    if topic=='rial-dial':self.assertIn('Q_u',s);self.assertIn('Q_m',s);self.assertIn(r'\mathcal N(0,\sigma^2)',s)
  for stem in STEMS:
   self.assertIn('prefers-reduced-motion',(A/f'{stem}-motion.svg').read_text());r=root(stem,'still');self.assertEqual(r.get('width'),'640');self.assertFalse(any('animate' in e.tag for e in r.iter()))
if __name__=='__main__':unittest.main()
