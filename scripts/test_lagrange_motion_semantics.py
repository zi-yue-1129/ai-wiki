"""Actual rendered-SMIL geometry, including active-set and dual-curve transitions."""
import bisect
import math
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'docs/assets/concept-animations'
NS = '{http://www.w3.org/2000/svg}'

def load(name, kind='motion'):
    return ET.parse(ASSETS / f'{name}-{kind}.svg').getroot()

def value(element, attr, time):
    animations = [a for a in element.findall(NS+'animate') if a.get('attributeName') == attr]
    if not animations:
        return float(element.get(attr))
    a = animations[0]
    times = list(map(float, a.get('keyTimes').split(';')))
    vals = list(map(float, a.get('values').split(';')))
    assert len(times) == len(vals) and times[0] == 0 and times[-1] == 1
    i = min(bisect.bisect_right(times, time)-1, len(times)-2)
    f = (time-times[i])/(times[i+1]-times[i])
    return vals[i] + f*(vals[i+1]-vals[i])

class LagrangeGeometry(unittest.TestCase):
    def test_feasible_circle_and_contour_gradient_directions(self):
        r = load('lagrange-tangency')
        point = next(e for e in r.iter(NS+'circle') if e.get('fill') == '#148b87')
        contour = next(e for e in r.iter(NS+'circle') if e.get('stroke') == '#e39b42')
        arrows = [e for e in r.iter(NS+'line') if e.find(NS+'animate') is not None]
        for t in (i/10000 for i in range(10001)):
            x,y=value(point,'cx',t),value(point,'cy',t)
            self.assertAlmostEqual(math.hypot(x-225,y-201),80,delta=.002)
            self.assertAlmostEqual(value(contour,'r',t),math.hypot(x-385,y-121),delta=.004)
            for e in arrows:
                self.assertAlmostEqual(value(e,'x1',t),x,delta=1e-8)
                self.assertAlmostEqual(value(e,'y1',t),y,delta=1e-8)
                dx,dy=value(e,'x2',t)-x,value(e,'y2',t)-y
                if e.get('stroke')=='#148b87':
                    self.assertAlmostEqual(dx,(x-225)*28/80,delta=.00002)
                    self.assertAlmostEqual(dy,(y-201)*28/80,delta=.00002)
                else:
                    d=math.hypot(x-385,y-121)
                    self.assertAlmostEqual(dx,32*(x-385)/d,delta=.004)
                    self.assertAlmostEqual(dy,32*(y-121)/d,delta=.004)
        self.assertAlmostEqual((value(point,'cx',1)-225)/80,2/math.sqrt(5),delta=1e-7)
        self.assertAlmostEqual((201-value(point,'cy',1))/80,1/math.sqrt(5),delta=1e-7)

    def test_kkt_complementarity_at_every_intermediate_time(self):
        r=load('lagrange-kkt-active-set')
        target=next(e for e in r.iter(NS+'circle') if e.get('cy')=='151')
        point=next(e for e in r.iter(NS+'circle') if e.get('cy')=='229')
        bar=next(e for e in r.iter(NS+'rect') if e.find(NS+'animate') is not None)
        scale=258/1.75
        for t in (i/10000 for i in range(10001)):
            a=(value(target,'cx',t)-54)/scale
            x=(value(point,'cx',t)-54)/scale
            mu=value(bar,'height',t)/100
            self.assertAlmostEqual(x,min(a,1),delta=1e-7)
            self.assertAlmostEqual(mu,2*max(a-1,0),delta=1e-7)
            self.assertAlmostEqual(2*(x-a)+mu,0,delta=2e-7)
            self.assertAlmostEqual(mu*(x-1),0,delta=1e-7)
            self.assertAlmostEqual(value(bar,'y',t)+100*mu,270,delta=1e-8)

    def test_dual_gap_and_lagrangian_minimizer_share_lambda(self):
        r=load('lagrange-dual-gap')
        points=[e for e in r.iter(NS+'circle') if e.find(NS+'animate') is not None]
        point=next(e for e in points if e.get('cy')!='200')
        minimizer=next(e for e in points if e.get('cy')=='200')
        gap=next(e for e in r.iter(NS+'line') if e.find(NS+'animate') is not None)
        for t in (i/10000 for i in range(10001)):
            px,py=value(point,'cx',t),value(point,'cy',t)
            lam=(px-79)/94.375
            d=(269-py)/147.5
            self.assertAlmostEqual(d,lam-lam*lam/4,delta=.00015)
            self.assertLessEqual(d,1.0000001)
            self.assertAlmostEqual((value(minimizer,'cx',t)-452)/(148/2.2),2-lam/2,delta=1e-7)
            for attr in ('x1','x2'):self.assertAlmostEqual(value(gap,attr,t),px,delta=1e-8)
            self.assertAlmostEqual(value(gap,'y2',t),py,delta=1e-8)
        self.assertAlmostEqual(value(point,'cy',.48),121.5,delta=1e-8)
        self.assertAlmostEqual(value(minimizer,'cx',.48),452+148/2.2,delta=.00001)

if __name__=='__main__':unittest.main()
