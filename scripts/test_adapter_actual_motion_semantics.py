"""Check animated rounding against actual markers, not just endpoint arithmetic."""
import bisect
import math
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'docs/assets/concept-animations'
NS='{http://www.w3.org/2000/svg}'

def read(stem,kind='motion'):return ET.parse(ASSETS/f'{stem}-{kind}.svg').getroot()

def at(e,attr,t):
    a=next((a for a in e.findall(NS+'animate') if a.get('attributeName')==attr),None)
    if a is None:return float(e.get(attr,'1' if attr=='opacity' else '0'))
    v=list(map(float,a.get('values').split(';')));k=list(map(float,a.get('keyTimes').split(';')))
    i=min(len(k)-1,max(0,bisect.bisect_right(k,t)-1))
    if a.get('calcMode')=='discrete' or i==len(k)-1:return v[i]
    q=(t-k[i])/(k[i+1]-k[i]);return v[i]*(1-q)+v[i+1]*q

class AdapterSvgTests(unittest.TestCase):
    def test_dora_analytic_endpoints_and_subpixel_norm_bound(self):
        r=read('dora-independent')
        v=next(e for e in r.iter(NS+'line') if e.find(NS+'animate') is not None)
        m=next(e for e in r.iter(NS+'rect') if e.find(NS+'animate') is not None)
        for i in range(10001):
            t=i/10000
            radius=math.hypot(at(v,'x2',t)-169,at(v,'y2',t)-203)
            expected=18*(3+at(m,'width',t)/50)
            self.assertLess(abs(radius-expected),.12)
        self.assertAlmostEqual((at(v,'x2',.59)-169)/18,4.8)
        self.assertAlmostEqual((203-at(v,'y2',.59))/18,3.6)
    def test_qlora_single_step_has_causal_phases(self):
        r=read('qlora-frozen-flow');motions=list(r.iter(NS+'animateMotion'))
        intervals=[]
        for a in motions:
            self.assertEqual(a.get('dur'),'10s');self.assertEqual(a.get('begin'),'0s')
            k=list(map(float,a.get('keyTimes').split(';')))
            self.assertEqual(a.get('keyPoints'),'0;0;1;1')
            intervals.append(k[1:3])
        read_,base,adapter,back,update=intervals
        self.assertLessEqual(read_[1],base[0])
        self.assertLessEqual(max(base[1],adapter[1]),back[0])
        self.assertLessEqual(back[1],update[0])
        self.assertLess(update[1],1)
        circles=[c for c in r.iter(NS+'circle') if c.find(NS+'animateMotion') is not None]
        for c,a in zip(circles,motions):
            opacity=c.find(NS+'animate');self.assertEqual(opacity.get('keyTimes'),a.get('keyTimes'))
            self.assertEqual(opacity.get('values'),'0;1;0;0')
    def test_bilingual_source_and_focusable_scroll(self):
        for topic,stem in [('dora','dora-independent'),('qlora','qlora-frozen-flow')]:
            for lang in ['', '.zh-TW']:
                p=ROOT/f'docs/theory/model-compression/low-rank-and-efficient-architectures/lora/{topic}{lang}.md';s=p.read_text()
                for token in ['data-source-asset-urls=', 'tabindex="0"', 'overflow-x:auto', 'min-width:640px', 'role="region"']:
                    self.assertIn(token,s)
                self.assertNotIn('../../../../../assets',s)

if __name__=='__main__':unittest.main()
