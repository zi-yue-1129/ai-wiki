"""Actual SVG covariance geometry and synchronized minimum squared distance."""
import bisect
from functools import lru_cache
import math
from pathlib import Path
import unittest
import xml.etree.ElementTree as E
B=Path(__file__).resolve().parents[1]/'docs/assets/concept-animations';N='{http://www.w3.org/2000/svg}'
@lru_cache(None)
def animation(e,attr):
    a=next((a for a in e.findall(N+'animate') if a.get('attributeName')==attr),None)
    if a is None:return None
    times=tuple(map(float,a.get('keyTimes').split(';')));vals=tuple(map(float,a.get('values').split(';')))
    assert len(times)==len(vals) and times[0]==0 and times[-1]==1
    assert all(a<b for a,b in zip(times,times[1:]))
    return times,vals

def value(e,attr,t):
    data=animation(e,attr)
    if data is None:return float(e.get(attr))
    times,vals=data;i=min(bisect.bisect_right(times,t)-1,len(times)-2)
    u=(t-times[i])/(times[i+1]-times[i]);return vals[i]+u*(vals[i+1]-vals[i])

class MahalanobisGeometry(unittest.TestCase):
    def test_precision_contours_and_score_direction(self):
        for kind in ['motion','still']:
            root=E.parse(B/f'mahalanobis-ellipse-threshold-{kind}.svg').getroot()
            self.assertTrue(all(float(e.get('font-size', '12')) >= 12 for e in root.iter(N+'text')))
            ellipses=list(root.iter(N+'ellipse'))
            self.assertEqual(len(ellipses),2)
            self.assertEqual([float(e.get('cx')) for e in ellipses],[129,249])
            self.assertIn('Σ = diag(4, 1)',[e.text for e in root.iter(N+'text')])
            for e in ellipses:
                # Every covariance-shaped contour point has precision quadratic form 3.
                for i in range(361):
                    theta=i*math.pi/180
                    a=float(e.get('rx'))*math.cos(theta)/30
                    b=float(e.get('ry'))*math.sin(theta)/30
                    self.assertAlmostEqual(a*a/4+b*b,3,delta=.00007)
            threshold=next(e for e in root.iter(N+'line') if e.get('stroke')=='#ffca74')
            self.assertEqual(float(threshold.get('x1')),425+165*3/6)
            if kind=='still':self.assertFalse(list(root.iter(N+'animate')))

    def test_all_intermediate_coordinates_scores_and_crossings(self):
        root=E.parse(B/'mahalanobis-ellipse-threshold-motion.svg').getroot()
        point=next(e for e in root.iter(N+'circle') if e.get('fill')=='#53d6d0')
        readout=next(e for e in root.iter(N+'circle') if e.get('r')=='10')
        px=animation(point,'cx')[0];py=animation(point,'cy')[0];scoretimes=animation(readout,'cx')[0]
        self.assertEqual(px,py);self.assertEqual(px,scoretimes)
        for t in (i/10000 for i in range(10001)):
            a=(value(point,'cx',t)-129)/30;b=(218-value(point,'cy',t))/30
            u=(2-a)/2
            self.assertGreaterEqual(u,-1e-8);self.assertLessEqual(u,1+1e-8)
            self.assertAlmostEqual(b,1+u,delta=3e-8)
            d1=a*a/4+b*b;d2=(a-4)**2/4+b*b
            self.assertLessEqual(d1,d2+1e-8)
            self.assertAlmostEqual(d1,2+2*u*u,delta=2e-7)
            plotted=(value(readout,'cx',t)-425)/(165/6)
            self.assertAlmostEqual(plotted,min(d1,d2),delta=.00005)
        crossings=[t for t in px if abs(value(readout,'cx',t)-507.5)<1e-7]
        self.assertEqual(len(crossings),2)
        for t in crossings:
            u=(189-value(point,'cx',t))/60
            self.assertAlmostEqual(u,1/math.sqrt(2),delta=1e-8)
        for t,d in [(0,2),(.5,4),(1,2)]:self.assertAlmostEqual((value(readout,'cx',t)-425)/27.5,d,delta=1e-8)

if __name__=='__main__':unittest.main()
