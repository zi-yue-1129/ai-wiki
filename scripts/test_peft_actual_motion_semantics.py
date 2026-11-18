"""Actual IA3 gain geometry and prefix softmax, including interpolated frames."""
import bisect,math,unittest
from pathlib import Path
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1];ASSETS=ROOT/'docs/assets/concept-animations';NS='{http://www.w3.org/2000/svg}'
def read(stem,kind='motion'):return ET.parse(ASSETS/f'{stem}-{kind}.svg').getroot()
def at(e,attr,t):
 a=next((a for a in e.findall(NS+'animate') if a.get('attributeName')==attr),None)
 if a is None:return float(e.get(attr,'1' if attr=='opacity' else '0'))
 v=list(map(float,a.get('values').split(';')));k=list(map(float,a.get('keyTimes').split(';'))) if a.get('keyTimes') else [i/(len(v)-1) for i in range(len(v))];i=min(len(k)-1,max(0,bisect.bisect_right(k,t)-1))
 if a.get('calcMode')=='discrete' or i==len(k)-1:return v[i]
 q=(t-k[i])/(k[i+1]-k[i]);return v[i]*(1-q)+v[i+1]*q
class PeftSvgTests(unittest.TestCase):
 def test_actual_gain_axis_and_output_product(self):
  for kind in ['motion','still']:
   r=read('ia3-channel-gates',kind);markers=list(r.iter(NS+'circle'));inputs=[e for e in r.iter(NS+'rect') if e.get('fill')=='#28799B'];outputs=[e for e in r.iter(NS+'rect') if e.get('fill')=='#148A83']
   for e in r.iter(NS+'text'):
    if e.text in ['0.4','1.0','1.4']:self.assertEqual(float(e.get('x')),246+100*float(e.text))
   for j in range(1001):
    t=j/1000;u=1 if kind=='still' else 2*min(t,1-t)
    for h,g,m,inp,out in zip([.7,.9,.5,.8],[1.3,.6,1.1,.4],markers,inputs,outputs):
     actual=(at(m,'cx',t)-246)/100;self.assertAlmostEqual(actual,1+u*(g-1),places=5);self.assertAlmostEqual(float(inp.get('width')),104*h);self.assertAlmostEqual(at(out,'width',t),104*h*actual,places=3)
 def test_softmax_mass_axis_and_visual_channels(self):
  for kind in ['motion','still']:
   r=read('prefix-kv-attention',kind);bars=[e for e in r.iter(NS+'rect') if e.get('x')=='434' and e.get('fill')!='#E9F0F4'];edges=[e for e in r.iter(NS+'path') if e.get('d','').startswith('M 170')]
   ticks={e.text:float(e.get('x')) for e in r.iter(NS+'text') if e.text in ['0','0.75']};self.assertEqual(ticks,{'0':434,'0.75':598})
   for j in range(10001):
    t=j/10000;u=1 if kind=='still' else 2*min(t,1-t);ss=[-1.8+4.8*u,-1.4+2.6*u,1.2,.4];v=[math.exp(s-max(ss)) for s in ss];w=[a/sum(v) for a in v];actual=[at(b,'width',t)/(164/.75) for b in bars];self.assertAlmostEqual(sum(actual),1,places=7)
    for expected,a,e in zip(w,actual,edges):
     self.assertLess(abs(a-expected)*164/.75,.03);self.assertLess(abs(at(e,'stroke-width',t)-(1+7*a)),.000002);self.assertLess(abs(at(e,'opacity',t)-(.3+.68*a)),.000002)
 def test_bilingual_local_source_hooks(self):
  for topic in ['ia3','prefix-tuning']:
   for lang in ['', '.zh-TW']:
    s=(ROOT/f'docs/theory/paradigms/transfer/fine-tuning-and-adaptation/{topic}{lang}.md').read_text()
    for token in ['data-source-asset-urls','width:100%;overflow-x:auto','width:640px','tabindex="0"']:self.assertIn(token,s)
if __name__=='__main__':unittest.main()
