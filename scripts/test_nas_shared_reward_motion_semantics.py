"""Regression for actual ENAS timeline and MnasNet plotted reward coordinates."""
from pathlib import Path
import bisect
import unittest
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'docs/assets/concept-animations'
NS='{http://www.w3.org/2000/svg}'


def at(a,t):
    values=list(map(float,a.get('values',a.get('keyPoints')).split(';')))
    times=list(map(float,a.get('keyTimes').split(';')))
    i=min(len(times)-2,max(0,bisect.bisect_right(times,t)-1))
    q=(t-times[i])/(times[i+1]-times[i])
    return values[i]*(1-q)+values[i+1]*q


class NasSharedRewardTests(unittest.TestCase):
    def test_shared_gradient_and_forward_only_update(self):
        shared,private_a,private_b=.4,.2,-.3
        grad=(shared+private_a)-1
        self.assertAlmostEqual(grad,-.4)
        self.assertAlmostEqual(shared-.5*grad,.6)
        self.assertAlmostEqual(private_a-.5*grad,.4)
        self.assertAlmostEqual(shared-.5*grad+private_b,.3)
        r=ET.parse(ASSETS/'enas-shared-weight-transfer-motion.svg').getroot()
        width=next(a for a in r.iter(NS+'animate') if a.get('attributeName')=='width')
        marker=next(r.iter(NS+'animateMotion'))
        self.assertEqual(marker.get('calcMode'),'linear')
        previous=.4
        for i in range(1001):
            t=i/1000; value=at(width,t)/360
            self.assertGreaterEqual(value+1e-12,previous)
            self.assertAlmostEqual(value,.4+.2*min(1,max(0,(t-.25)/.25)))
            if at(marker,t)>=.5:self.assertAlmostEqual(value,.6)
            previous=value
        self.assertEqual(at(marker,0),0)
        self.assertEqual(at(marker,1),1)

    def test_mnasnet_actual_reward_geometry(self):
        r=ET.parse(ASSETS/'mnasnet-latency-tradeoff-motion.svg').getroot()
        a={e.get('attributeName'):e for e in r.iter(NS+'animate')}
        self.assertAlmostEqual(.74/.8,.925)
        crossing=.8/.925
        self.assertTrue(.7<crossing<1.3)
        for i in range(10001):
            t=i/10000; x=at(a['cx'],t);y=at(a['cy'],t);width=at(a['width'],t)
            latency=.7+(x-77)*.6/376
            reward=.8/latency
            # Piecewise-linear SVG sampling approximates the analytic curve.
            self.assertAlmostEqual(y,120+(1.2-reward)*224/.65,delta=.16)
            self.assertAlmostEqual(width,159*reward,delta=.074)
            self.assertAlmostEqual(width/159,1.2-(y-120)*.65/224,delta=.00001)

    def test_all_bilingual_nas_figures_are_source_relative_and_scrollable(self):
        for name in ['darts','regularized-evolution','efficient-neural-architecture-search','mnasnet']:
            for suffix in ['.md','.zh-TW.md']:
                text=(ROOT/'docs/theory/deep-learning/nas-automl'/(name+suffix)).read_text()
                self.assertIn('data-source-asset-urls',text)
                self.assertIn('width:100%;overflow-x:auto',text)
                self.assertIn('tabindex="0"',text)
                self.assertIn('min-width:800px;max-width:none',text)
                self.assertNotIn('src="../../../../assets',text)


if __name__=='__main__':unittest.main()
