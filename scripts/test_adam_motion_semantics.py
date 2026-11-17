#!/usr/bin/env python3
"""Check illustrative numerical values underlying bilingual Adam motion figures."""
import math
import unittest

class TestAdamMotionSemantics(unittest.TestCase):
    def test_sign_reversal(self):
        m = v = 0.0
        moments = []
        for t in range(1, 11):
            g = 1.0 if t <= 4 else -1.0
            m = 0.8 * m + 0.2 * g
            v = 0.5 * v + 0.5 * (g * g)
            mhat, vhat = m / (1 - 0.8**t), v / (1 - 0.5**t)
            self.assertAlmostEqual(vhat, 1.0)
            moments.append(mhat / math.sqrt(vhat))
        self.assertAlmostEqual(moments[4], 0.4050, delta=0.001)
        self.assertAlmostEqual(moments[5], 0.0242, delta=0.001)
        self.assertAlmostEqual(moments[6], -0.2350, delta=0.001)
        self.assertGreater(moments[5], 0)
        self.assertLess(moments[6], 0)

    def test_epsilon_regularizes_scale(self):
        for c in (0.02, 0.05, 0.1, 0.15, 0.25, 0.35, 0.5):
            self.assertAlmostEqual(c / math.sqrt(c*c), 1.0)
            self.assertAlmostEqual(c / (math.sqrt(c*c) + 0.1), c/(c+0.1))
        self.assertAlmostEqual(0.1/(0.1+0.1), 0.5)
        self.assertAlmostEqual(0.5/(0.5+0.1), 5/6)

    def test_shipped_svg_timelines(self):
        from pathlib import Path
        import xml.etree.ElementTree as ET
        ns = '{http://www.w3.org/2000/svg}'
        assets = Path(__file__).resolve().parents[1] / 'docs/assets/concept-animations'
        def root(stem, kind='motion'):
            return ET.parse(assets / f'{stem}-{kind}.svg').getroot()
        def values(a):
            return list(map(float, a.get('values').split(';')))
        def near(actual, expected, tol=.06):
            self.assertEqual(len(actual), len(expected))
            for a,b in zip(actual,expected):self.assertAlmostEqual(a,b,delta=tol)
        # Raw zero-start bias and corresponding corrected estimates.
        r=root('adam-bias-correction')
        ys=[values(a) for a in r.iter(ns+'animate') if a.get('attributeName')=='cy']
        self.assertEqual(len(ys),2)
        for ys,beta in zip(ys,(.8,.5)):
            near(ys,[325-205*(1-beta**t) for t in range(1,7)])
        self.assertEqual(len(ys),6)
        # Every keyframe in the sign-flip chart follows the recomputed first moment.
        r=root('adam-sign-reversal');m=0;expected=[]
        for t in range(1,11):
            m=.8*m+.2*(1 if t<=4 else -1)
            expected.append(297-51*m/(1-.8**t))
        y=next(a for a in r.iter(ns+'animate') if a.get('attributeName')=='cy')
        near(values(y),expected,.011)
        # No full-size duplicate coloured bars can occlude the moving scale bars.
        r=root('adam-scale-invariance')
        bars=[e for e in r.iter(ns+'rect') if e.get('x')=='444' and e.get('y') in ('165','225') and e.get('fill') in ('#2876b5','#dc8740')]
        self.assertEqual(len(bars),2)
        for b in bars:
            a=b.find(ns+'animate');self.assertIsNotNone(a)
            near(values(a),[31.25,250,31.25],.001)
        # The marker, vertical guide and magnitude bar share the same analytic sweep.
        r=root('adam-epsilon-threshold');anims=list(r.iter(ns+'animate'))
        self.assertEqual(len({a.get('keyTimes') for a in anims}),1)
        tracks={a.get('attributeName'):values(a) for a in anims}
        xs=tracks['cx'];ys=tracks['cy'];ws=tracks['width']
        self.assertEqual(len(xs),241)
        near(tracks['x1'],xs,.001);near(tracks['x2'],xs,.001)
        for x,y,w in zip(xs,ys,ws):
            c=(x-77)/820;u=c/(c+.1)
            self.assertAlmostEqual(y,328-184*u,delta=.001)
            self.assertAlmostEqual(w,188*u,delta=.001)
        # Numerical error between adjacent linear SMIL keyframes stays below .05px.
        for i in range(len(xs)-1):
            for f in (.25,.5,.75):
                x=xs[i]*(1-f)+xs[i+1]*f;y=ys[i]*(1-f)+ys[i+1]*f
                c=(x-77)/820
                self.assertAlmostEqual(y,328-184*c/(c+.1),delta=.05)
        for stem in ('adam-bias-correction','adam-scale-invariance','adam-sign-reversal','adam-epsilon-threshold'):
            self.assertFalse(list(root(stem,'still').iter(ns+'animate')))
        for suffix in ('','.zh-TW'):
            s=(assets.parents[1]/f'theory/optimization/adaptive/adam{suffix}.md').read_text()
            self.assertEqual(s.count('width:640px;min-width:640px;max-width:none;height:auto'),4)

if __name__ == "__main__":
    unittest.main()
