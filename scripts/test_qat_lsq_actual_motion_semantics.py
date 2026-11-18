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

def quant(w,s):return s*max(-4,min(3,math.copysign(math.floor(abs(w/s)+.5),w)))

class QuantisationSvgTests(unittest.TestCase):
    def test_qat_rounding_and_connector_follow_true_crossings(self):
        r=read('qat-fake-quant-ste')
        raw=next(c for c in r.iter(NS+'circle') if c.get('cy')=='139')
        snapped=next(c for c in r.iter(NS+'circle') if c.get('cy')=='190')
        connector=next(e for e in r.iter(NS+'line') if e.get('y1')=='149')
        for i in range(10001):
            t=(i+.37)/10002;x=(at(raw,'cx',t)-145)/126;q=math.floor(x+.5)
            self.assertAlmostEqual(at(snapped,'cx',t),145+126*q)
            self.assertAlmostEqual(at(connector,'x1',t),at(raw,'cx',t))
            self.assertAlmostEqual(at(connector,'x2',t),at(snapped,'cx',t))
        packet=next(c for c in r.iter(NS+'circle') if c.get('cy')=='287' and c.find(NS+'animate') is not None)
        self.assertGreater(at(packet,'cx',0),at(packet,'cx',1))
        self.assertTrue(all(at(packet,'cx',(i+1)/100)<=at(packet,'cx',i/100)+1e-9 for i in range(100)))

    def test_lsq_active_marker_always_on_grid_even_during_code_change(self):
        r=read('lsq-step-size-sweep');groups=[g for g in r.iter(NS+'g') if g.get('data-row') is not None]
        weights=[-1.1,-.6,.7,1.7]
        for i in range(10001):
            t=(i+.27)/10002;s=1-.8*min(t,1-t)
            for row,w in enumerate(weights):
                active=[g for g in groups if g.get('data-row')==str(row) and at(g,'opacity',t)==1]
                self.assertEqual(len(active),1)
                group=active[0];dot=group.find(NS+'circle');line=group.find(NS+'line')
                q=quant(w,s);self.assertAlmostEqual((at(dot,'cx',t)-355)/67,q,places=8)
                self.assertAlmostEqual(at(line,'x2',t),at(dot,'cx',t))
                self.assertAlmostEqual((at(line,'x1',t)-355)/67,w)
        for s,want in [(1,.35),(.6,.03)]:self.assertAlmostEqual(sum((quant(w,s)-w)**2 for w in weights),want)
        # Saturation is part of the formula even though the pictured inputs avoid it.
        self.assertAlmostEqual(quant(99,.6),1.8)
        self.assertAlmostEqual(quant(-99,.6),-2.4)

    def test_lsq_all_eight_codes_and_static_endpoint(self):
        for kind,s in [('motion',1),('still',.6)]:
            r=read('lsq-step-size-sweep',kind);plot=next(g for g in r.findall(NS+'g') if g.get('clip-path'))
            lines=plot.findall(NS+'line')
            self.assertEqual(len(lines),8)
            self.assertEqual([round((float(e.get('x1'))-355)/(67*s)) for e in lines],list(range(-4,4)))
        r=read('lsq-step-size-sweep','still')
        gs=[g for g in r.iter(NS+'g') if g.get('data-row') is not None]
        self.assertEqual([int(g.get('data-code')) for g in gs],[-2,-1,1,3])

    def test_bilingual_source_hooks_scroll_and_display_equations(self):
        for path in ['index','lsq/index']:
            for lang in ['', '.zh-TW']:
                s=(ROOT/f'docs/theory/model-compression/quantisation/quantisation-aware-training/{path}{lang}.md').read_text()
                for text in ['data-source-asset-urls','data-still-src','width:100%;overflow-x:auto','min-width:640px']:self.assertIn(text,s)
                if path.startswith('lsq'):
                    self.assertIn('\\operatorname{round}(x/s)-x/s',s)
                    self.assertNotIn('moves to where the loss is lowest',s)
                    self.assertNotIn('損失最低的位置',s)

if __name__=='__main__':unittest.main()
