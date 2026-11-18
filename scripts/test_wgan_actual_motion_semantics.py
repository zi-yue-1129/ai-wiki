"""Verify actual clipping and sampled input-gradient SVG geometry and timelines."""
import bisect
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'docs/assets/concept-animations'
NS='{http://www.w3.org/2000/svg}'

def read(stem,kind='motion'):
    return ET.parse(ASSETS/f'{stem}-{kind}.svg').getroot()

def at(e,attr,t):
    a=next((a for a in e.findall(NS+'animate') if a.get('attributeName')==attr),None)
    if a is None:return float(e.get(attr))
    v=list(map(float,a.get('values').split(';')))
    k=list(map(float,a.get('keyTimes',';'.join(str(i/(len(v)-1)) for i in range(len(v)))).split(';')))
    i=min(len(k)-2,max(0,bisect.bisect_right(k,t)-1));q=(t-k[i])/(k[i+1]-k[i])
    return v[i]*(1-q)+v[i+1]*q

class WganActualSvgTests(unittest.TestCase):
    def test_clip_exact_positions_and_no_reverse_update(self):
        weights=[-.055,-.041,-.012,.046,.057]
        r=read('wgan-weight-clip');dots=[c for c in r.iter(NS+'circle') if c.get('fill')=='#008f86']
        for dot,w in zip(dots,weights):
            target=max(-.03,min(.03,w));previous=abs(w-target)
            for i in range(1001):
                t=i/1000;value=(at(dot,'cx',t)-220)*.03/65
                expected=w+(target-w)*min(1,max(0,(t-.15)/.33))
                self.assertAlmostEqual(value,expected,places=10)
                self.assertLessEqual(abs(value-target),previous+1e-10);previous=abs(value-target)
            self.assertAlmostEqual(value,target)
        r=read('wgan-weight-clip','still')
        for dot,w in zip([c for c in r.iter(NS+'circle') if c.get('fill')=='#008f86'],weights):
            self.assertAlmostEqual((float(dot.get('cx'))-220)*.03/65,max(-.03,min(.03,w)))

    def test_gp_actual_interpolation_norm_and_penalty(self):
        r=read('wgan-gp-interpolation');dots=[c for c in r.iter(NS+'circle') if c.find(NS+'animate') is not None]
        self.assertEqual(len(dots),3)
        for i in range(10001):
            t=i/10000;s=(at(dots[0],'cx',t)-94)/236
            gradient=.6+.8*s;penalty=10*(gradient-1)**2
            self.assertAlmostEqual(at(dots[1],'cx',t),438+161*s)
            self.assertAlmostEqual(at(dots[1],'cy',t),207-(gradient-.6)*87/.8)
            self.assertAlmostEqual(at(dots[2],'cx',t),438+161*s)
            self.assertAlmostEqual(at(dots[2],'cy',t),312-63*penalty/1.6,delta=.159)
        # Tick baseline offset is 5px: it must describe actual plotted values.
        for text in r.iter(NS+'text'):
            if text.text in ['0.6','1.0','1.4']:
                self.assertAlmostEqual(float(text.get('y'))-5,207-(float(text.text)-.6)*87/.8)
        unit=next(e for e in r.iter(NS+'line') if e.get('x1')=='438' and e.get('stroke-dasharray')=='5 5')
        self.assertAlmostEqual(float(unit.get('y1')),163.5)
        self.assertAlmostEqual(at(dots[2],'cy',.25),312)

    def test_bilingual_hooks_and_no_global_gp_claim(self):
        for name in ['wgan','wgan-gp']:
            for lang in ['', '.zh-TW']:
                text=(ROOT/f'docs/theory/paradigms/unsupervised/density-and-generative-models/gan/{name}{lang}.md').read_text()
                self.assertIn('data-source-asset-urls',text)
                self.assertIn('width:100%;overflow-x:auto',text)
                self.assertIn('min-width:640px;max-width:none',text)
                self.assertNotIn('constraint holds approximately everywhere',text)
                self.assertNotIn('限制只能近似地在各處成立',text)

if __name__=='__main__':unittest.main()
