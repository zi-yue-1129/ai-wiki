"""Read actual DT SVG values and sample native SMIL, not hard-coded example assertions."""
from pathlib import Path
import unittest
from xml.etree import ElementTree as E
ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'docs/assets/concept-animations'
NS='{http://www.w3.org/2000/svg}'
def svg(name,mode='motion'):
    return E.parse(ASSETS/f'dt-{name}-{mode}.svg').getroot()
def sample(a,t):
    keys=list(map(float,a.get('keyTimes').split(';')))
    vals=list(map(float,a.get('values').split(';')))
    i=max(i for i,k in enumerate(keys) if k<=t)
    if i==len(keys)-1 or a.get('calcMode')=='discrete':return vals[i]
    f=(t-keys[i])/(keys[i+1]-keys[i]);return vals[i]+f*(vals[i+1]-vals[i])
class Semantics(unittest.TestCase):
    def test_return_values_and_bars(self):
        r=svg('return-budget','still')
        values=[int(n.text) for n in r.iter(NS+'text') if n.get('font-size')=='29']
        rewards=[int(n.text.split('=')[1]) for n in r.iter(NS+'text') if (n.text or '').startswith(('r0','r1','r2'))]
        self.assertEqual(values,[6,4,3,0]);self.assertEqual(rewards,[2,1,3])
        for i,reward in enumerate(rewards):self.assertEqual(values[i]-reward,values[i+1])
        bars=[float(n.get('width')) for n in r.iter(NS+'rect') if n.get('height')=='7' and n.get('fill')=='#087f8c']
        self.assertEqual(len(bars),3)
        for width,value in zip(bars,values):self.assertAlmostEqual(width,86*value/6)
    def test_visible_reward_markers_do_not_reverse_or_leave_arrow(self):
        circles=[n for n in svg('return-budget').iter(NS+'circle') if n.get('r')=='7']
        self.assertEqual(len(circles),3)
        for c,(left,right) in zip(circles,[(120,193),(283,356),(446,519)]):
            animations={a.get('attributeName'):a for a in c.findall(NS+'animate')}
            seen=[sample(animations['cx'],t/10000) for t in range(10000) if sample(animations['opacity'],t/10000)>0]
            self.assertGreater(len(seen),100)
            self.assertGreaterEqual(min(seen),left);self.assertLessEqual(max(seen),right)
            self.assertTrue(all(b>=a for a,b in zip(seen,seen[1:])))
    def test_final_budget_appears_after_last_reward_flight(self):
        g=next(g for g in svg('return-budget').iter(NS+'g') if any(n.text=='G3' for n in g.iter(NS+'text')))
        a=g.find(NS+'animate')
        self.assertEqual(sample(a,.955),0)
        self.assertEqual(sample(a,.975),1)
    def test_prefix_marker_stays_in_allowed_row(self):
        c=next(n for n in svg('causal-prefix').iter(NS+'circle') if n.find(NS+'animate') is not None)
        a={x.get('attributeName'):x for x in c.findall(NS+'animate')}
        for t in range(10000):
            phase=t/10000;y=sample(a['cy'],phase);x=sample(a['cx'],phase)
            self.assertIn(y,[175,225,275]);self.assertGreaterEqual(x,158)
            self.assertLessEqual(x,{175:212,225:374,275:536}[y])
    def test_static_and_timing(self):
        for name in ['return-budget','causal-prefix']:
            self.assertFalse(svg(name,'still').findall('.//'+NS+'animate'))
            for a in svg(name).iter(NS+'animate'):
                self.assertEqual(a.get('dur'),'12s');self.assertEqual(a.get('repeatCount'),'indefinite')
                self.assertEqual(len(a.get('values').split(';')),len(a.get('keyTimes').split(';')))
    def test_bilingual_focusable_readable_regions(self):
        base=ROOT/'docs/theory/paradigms/reinforcement-learning/offline-rl/decision-transformer'
        for name in ['index.md','index.zh-TW.md']:
            text=(base/name).read_text()
            self.assertEqual(text.count('class="reviewed-motion-scroll" role="region" tabindex="0"'),2)
            self.assertEqual(text.count('<img class="concept-motion-wide"'),2)
if __name__=='__main__':unittest.main()
