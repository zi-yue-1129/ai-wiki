"""Independently check visual probabilities and spectral gains, including between keys."""
import math
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
NS={'s':'http://www.w3.org/2000/svg'}
def svg(stem,kind='motion'):
    return ET.parse(ROOT/f'docs/assets/concept-animations/{stem}-{kind}.svg').getroot()
def interp(values,t):
    x=t*(len(values)-1);i=min(int(x),len(values)-2);a=x-i
    return values[i]*(1-a)+values[i+1]*a
def anims(root):
    return [[float(x) for x in a.attrib['values'].split(';')] for a in root.findall('.//s:animate',NS)]
def softmax(v):
    e=[math.exp(x-max(v)) for x in v];return [x/sum(e) for x in e]
class Semantics(unittest.TestCase):
    def test_qk_actual_vectors_and_interpolated_probability(self):
        q=[1,-1,0];ks=[[1,-1,0],[1,0,-1],[-1,1,0]]
        dots=[sum(a*b for a,b in zip(q,k))/math.sqrt(3) for k in ks]
        a=anims(svg('qk-norm-scale-sweep'))
        self.assertEqual(len(a),4)
        for j in range(2001):
            t=j/2000;s=1+3*(interp(a[-1],t)-173)/393
            expected=softmax([x*s*s for x in dots])
            actual=[interp(x,t)/170 for x in a[:3]]
            self.assertAlmostEqual(sum(actual),1,places=7)
            for x,y in zip(actual,expected):self.assertLess(abs(x-y),0.00005)
        normalized=softmax([x*1.5 for x in dots])
        for kind in ['motion','still']:
            bars=[r for r in svg('qk-norm-scale-sweep',kind).findall('.//s:rect',NS) if r.get('x')=='394' and r.get('fill')!='#e9f0f5']
            for i,r in enumerate(bars):self.assertLess(abs(float(r.get('width'))/170-normalized[i%3]),0.000004)
    def test_sigma_shared_scale_and_normalisation(self):
        a=anims(svg('sigma-reparam-spectral-gain'));self.assertEqual(len(a),3)
        for j in range(2001):
            t=j/2000;s=1+3*(interp(a[-1],t)-173)/393
            self.assertAlmostEqual(interp(a[0],t)/(190/8),2*s,places=6)
            self.assertAlmostEqual(interp(a[1],t)/(190/8),.5*s,places=6)
            self.assertAlmostEqual(1.2*(.5*s)/(2*s),.3)
        for kind in ['motion','still']:
            bars=[r for r in svg('sigma-reparam-spectral-gain',kind).findall('.//s:rect',NS) if r.get('x')=='395' and r.get('fill')!='#eaf1f6']
            for i,r in enumerate(bars):self.assertAlmostEqual(float(r.get('width'))/(190/8),[1.2,.3][i%2])
    def test_static_fallback_and_bilingual_hooks(self):
        for topic,stem in [('qk-norm','qk-norm-scale-sweep'),('sigma-reparam','sigma-reparam-spectral-gain')]:
            self.assertFalse(svg(stem,'still').findall('.//s:animate',NS))
            for lang in ['', '.zh-TW']:
                text=(ROOT/f'docs/theory/models/transformer/{topic}{lang}.md').read_text()
                self.assertIn('data-source-asset-urls',text)
                self.assertIn(f'data-motion-src="../../../assets/concept-animations/{stem}-motion.svg"',text)
if __name__=='__main__':unittest.main()
