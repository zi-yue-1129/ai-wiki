"""Independent GP/EI recomputation and x-synchronised acquisition scan regression."""
import math
import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ASSETS = Path(__file__).resolve().parents[1] / 'docs/assets/concept-animations'
NS = '{http://www.w3.org/2000/svg}'
X = [.8, 2.3, 4.7, 3.24]
# Rounded values documented by the original illustrative fixture, not measurements.
Y = [.0923, -.2694, .3036, -.8761]

def solve(matrix, rhs):
    rows = [list(a) + [b] for a, b in zip(matrix, rhs)]
    for j in range(len(rows)):
        pivot = rows[j][j]
        rows[j] = [x / pivot for x in rows[j]]
        for i in range(len(rows)):
            if i != j:
                factor = rows[i][j]
                rows[i] = [a-factor*b for a,b in zip(rows[i], rows[j])]
    return [r[-1] for r in rows]

def posterior(x, n):
    if n == 0:
        return 0., 1.
    kernel = lambda a,b: math.exp(-.5*((a-b)/.92)**2)
    k = [kernel(x,v) for v in X[:n]]
    matrix = [[kernel(a,b)+(.06**2 if i==j else 0) for j,b in enumerate(X[:n])] for i,a in enumerate(X[:n])]
    mean = sum(a*b for a,b in zip(k, solve(matrix, Y[:n])))
    var = 1-sum(a*b for a,b in zip(k, solve(matrix, k)))
    return mean, math.sqrt(max(0, var))

def points(d):
    return [tuple(map(float,p)) for p in re.findall(r'([-\d.]+),([-\d.]+)',d)]

def value(animation, t):
    ts = list(map(float,animation.get('keyTimes').split(';')))
    vs = list(map(float,animation.get('values').split(';')))
    for i in range(len(ts)-1):
        if t <= ts[i+1]:
            return vs[i]+(vs[i+1]-vs[i])*(t-ts[i])/(ts[i+1]-ts[i])
    return vs[-1]

class BayesianOptimisationMotion(unittest.TestCase):
    def test_gp_conditioning_grid(self):
        root = ET.parse(ASSETS/'bo-gp-conditioning-motion.svg').getroot()
        mean = next(p for p in root.iter(NS+'path') if p.get('stroke')=='#177f91')
        band = next(p for p in root.iter(NS+'path') if p.get('fill')=='#cbdcf1')
        mean_frames = mean.find(NS+'animate').get('values').split(';')
        bands = band.find(NS+'animate').get('values').split(';')
        for n in range(5):
            for i, (px,py) in enumerate(points(mean_frames[n])):
                m,s = posterior(i*.06,n)
                self.assertAlmostEqual(px,48+544*i/100,delta=.051)
                self.assertAlmostEqual(py,188.5-m*207/4.4,delta=.06)
                upper,lower = points(bands[n])[i],points(bands[n])[201-i]
                self.assertAlmostEqual(upper[1],188.5-(m+1.96*s)*207/4.4,delta=.06)
                self.assertAlmostEqual(lower[1],188.5-(m-1.96*s)*207/4.4,delta=.06)
        self.assertEqual(mean_frames[-1],mean_frames[-2])
        self.assertEqual(bands[-1],bands[-2])

    def test_ei_grid_and_candidate(self):
        root = ET.parse(ASSETS/'bo-expected-improvement-motion.svg').getroot()
        curve = next(p for p in root.iter(NS+'path') if p.get('stroke')=='#9072c4')
        ei = []
        for i,(px,py) in enumerate(points(curve.get('d'))):
            m,s = posterior(i*.06,3)
            delta = min(Y[:3])-m
            z=delta/s
            e = delta*.5*(1+math.erf(z/math.sqrt(2)))+s*math.exp(-z*z/2)/math.sqrt(2*math.pi)
            ei.append(e)
            # Original chart uses EI range 0..0.65 over a 70 px panel.
            self.assertAlmostEqual(py,310-e*70/.65,delta=.06)
        self.assertEqual(max(range(101),key=ei.__getitem__),54)
        self.assertAlmostEqual(ei[54],.22184,delta=.0001)

    def test_scan_dot_and_vertical_cursor_share_x(self):
        root = ET.parse(ASSETS/'bo-expected-improvement-motion.svg').getroot()
        dot = next(p for p in root.iter(NS+'circle') if p.get('fill')=='#9072c4')
        animations = {a.get('attributeName'): a for a in dot}
        curve = next(p for p in root.iter(NS+'path') if p.get('stroke')=='#9072c4')
        coords = points(curve.get('d'))
        for i in range(1001):
            t=i/1000
            x=value(animations['cx'],t)
            self.assertAlmostEqual(x,48+544*min(t/.78,1),delta=.000001)
            segment=next((j for j in range(100) if x<=coords[j+1][0]),99)
            (x0,y0),(x1,y1)=coords[segment:segment+2]
            self.assertAlmostEqual(value(animations['cy'],t),y0+(y1-y0)*(x-x0)/(x1-x0),delta=.000001)

if __name__ == '__main__':
    unittest.main()
