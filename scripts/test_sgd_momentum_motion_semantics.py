"""Validate shipped momentum and minibatch-noise animation coordinates."""
import math
from pathlib import Path
import unittest
import xml.etree.ElementTree as E
N='{http://www.w3.org/2000/svg}';A=Path(__file__).resolve().parents[1]/'docs/assets/concept-animations'
def root(stem,kind='motion'):return E.parse(A/f'{stem}-{kind}.svg').getroot()
def vals(a):return list(map(float,a.get('values').split(';')))
def at(a,t):
    ts=list(map(float,a.get('keyTimes').split(';')));vs=vals(a)
    for i in range(1,len(ts)):
        if t<=ts[i]:return vs[i-1]+(vs[i]-vs[i-1])*(t-ts[i-1])/(ts[i]-ts[i-1])
    return vs[-1]
class MotionValues(unittest.TestCase):
    def test_momentum(self):
        v=0;x=3;hb=[x]
        for _ in range(12):v=.7*v+x;x-=.2*v;hb.append(x)
        self.assertGreater(hb[3],0);self.assertLess(hb[4],0)
        r=root('heavy-ball-overshoot')
        for color,states in [('#168f8b',[3*.8**i for i in range(13)]),('#7b67bc',hb)]:
            dot=next(e for e in r.iter(N+'circle') if e.get('fill')==color and e.find(N+'animate') is not None)
            cy=dot.find(N+'animate[@attributeName="cy"]')
            for y,x in zip(vals(cy),states):self.assertAlmostEqual(y,224-43*x,delta=.0001)
            bar=next(e.find(N+'animate') for e in r.iter(N+'rect') if e.get('fill')==color and e.find(N+'animate') is not None)
            # Includes between-step zero crossings, where abs(linear(theta)) is not linear(abs(theta)).
            for i in range(1201):
                t=i/1200;theta=(224-at(cy,t))/43
                self.assertAlmostEqual(at(bar,t),145*abs(theta)/3,delta=.001)
    def test_noise(self):
        r=root('sgd-noise-batch');circles=[e for e in r.iter(N+'circle') if e.find(N+'animate') is not None]
        cursor=circles[0];cx=cursor.find(N+'animate[@attributeName="cx"]');cy=cursor.find(N+'animate[@attributeName="cy"]')
        self.assertEqual(len(vals(cx)),65)
        for i in range(1025):
            t=i/1024;B=4*2**((at(cx,t)-67)/85.5)
            self.assertAlmostEqual(at(cy,t),260-54*.1*(128/B-1),delta=.041)
        for dot in circles[1:]:
            for attr,center in [('cx',532),('cy',170)]:
                a=dot.find(N+f'animate[@attributeName="{attr}"]');v=vals(a);d=v[0]-center
                for i,x in enumerate(v):self.assertAlmostEqual(x,center+d*math.sqrt(4/(4*2**(i/16))),delta=.0001)
        for stem in ('heavy-ball-overshoot','sgd-noise-batch'):
            self.assertFalse(list(root(stem,'still').iter(N+'animate')))
if __name__=='__main__':unittest.main()
