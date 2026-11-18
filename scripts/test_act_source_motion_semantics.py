from pathlib import Path
import bisect,math,copy,unittest,xml.etree.ElementTree as E
R=Path(__file__).resolve().parents[1];A=R/'docs/assets/concept-animations';N='{http://www.w3.org/2000/svg}'
def value(a,t):
 vals=[float(x) for x in a.get('values').split(';')];ks=[float(x) for x in a.get('keyTimes').split(';')];i=min(len(vals)-2,max(0,bisect.bisect_right(ks,t)-1))
 if a.get('calcMode')=='discrete':return vals[min(len(vals)-1,bisect.bisect_right(ks,t)-1)]
 return vals[i]+(vals[i+1]-vals[i])*(t-ks[i])/(ks[i+1]-ks[i])
def check(root,stem):
 if stem=='act-temporal-ensemble':
  bars=[x for x in root.iter(N+'rect') if x.get('y')=='278' and x.get('fill')=='#087f83'];assert len(bars)==4
  for i,b in enumerate(bars):assert abs(float(b.get('width'))-56*math.exp(-.5*i))<1e-8
  for i in range(4):
   c=root.find(f".//*[@id='query-{i}-same-time']");a=c.find(N+'animateMotion');assert a.get('dur')=='10s' and a.get('begin')=='0s' and a.get('path').endswith('H384');end=float(a.get('keyTimes').split(';')[2]);b=bars[i].find(N+'animate')
   for j in range(1001):
    t=j/1000
    if value(b,t)>0:assert t>=end
  weights=[math.exp(-.5*i) for i in range(4)];x=sum(a*b for a,b in zip([.7,1,.8,1.2],weights))/sum(weights)
  assert f'{x:.3f}'=='0.850'
  outputs=[g for g in root.findall(N+'g') if any(t.text=='0.850' for t in g.iter(N+'text'))];assert len(outputs)==1
  a=outputs[0].find(N+'animate')
  for j in range(1001):
   t=j/1000
   if value(a,t)>0:assert all(value(b.find(N+'animate'),t)==1 for b in bars)
 else:
  ids={c.get('id'):c for c in root.findall(N+'circle') if c.get('id')};assert len(ids)==9
  windows={k:tuple(map(float,c.find(N+'animateMotion').get('keyTimes').split(';')[1:3])) for k,c in ids.items()}
  for out,ins in [('encoder-to-latent',['demo-to-encoder','joint-to-encoder']),('latent-to-decoder',['encoder-to-latent']),('train-chunk',['latent-to-decoder','train-observation']),('deploy-chunk',['deploy-observation','zero-to-decoder'])]:assert windows[out][0]>=max(windows[x][1] for x in ins)
  for name,c in ids.items():
   a=c.find(N+'animateMotion');assert a.get('dur')=='10s' and a.get('begin')=='0s'
   for j in range(1001):
    t=j/1000
    if t<windows[name][0]:assert value(c.find(N+'animate'),t)==0
  assert any(x.text=='q only' for x in root.iter(N+'text'))
class Act(unittest.TestCase):
 def test_actual_geometry_timing_and_weights(self):
  for s in ['act-temporal-ensemble','act-cvae-train-deploy']:check(E.parse(A/(s+'-motion.svg')).getroot(),s)
 def test_old_independent_clock_rejected(self):
  r=E.parse(A/'act-temporal-ensemble-motion.svg').getroot();r.find(".//*[@id='query-1-same-time']/"+N+'animateMotion').set('dur','5s')
  with self.assertRaises(AssertionError):check(r,'act-temporal-ensemble')
 def test_early_decoder_output_rejected(self):
  r=E.parse(A/'act-cvae-train-deploy-motion.svg').getroot();r.find(".//*[@id='train-chunk']/"+N+'animateMotion').set('keyTimes','0;.1;.2;1')
  with self.assertRaises(AssertionError):check(r,'act-cvae-train-deploy')
 def test_bilingual_display_hooks_and_scope(self):
  for lang in ['', '.zh-TW']:
   s=(R/f'docs/applications/robotics/aloha/index{lang}.md').read_text();assert s.count('data-source-asset-urls')==2 and s.count('tabindex="0"')==2 and '\\begin{gathered}' in s and '\\end{gathered}' in s and '\n$\n' not in s
if __name__=='__main__':unittest.main()
