"""LARS/LAMB common-scale vectors, ratios and causal reveal sequencing."""
import math
import re
import unittest
import xml.etree.ElementTree as E
from pathlib import Path

N='{http://www.w3.org/2000/svg}'
A=Path(__file__).resolve().parents[1]/'docs/assets/concept-animations'
def nums(s): return list(map(float,re.findall(r'-?\d+(?:\.\d+)?',s)))
def sample(a,t):
    ts=list(map(float,a.get('keyTimes').split(';')))
    vs=[nums(v) for v in a.get('values').split(';')]
    for i in range(len(ts)-1):
        if t<=ts[i+1]:
            q=(t-ts[i])/(ts[i+1]-ts[i])
            return [x+(y-x)*q for x,y in zip(vs[i],vs[i+1])]
    return vs[-1]
def motion(stem):
    r=E.parse(A/f'{stem}-motion.svg').getroot()
    return next(n for n in r if n.get('class')=='motion')

class LayerTrust(unittest.TestCase):
    def test_lars_ratios_and_relative_steps(self):
        for w,g,rho,step in [(2,8,.025,.2),(6,3,.2,.6)]:
            self.assertAlmostEqual(.1*w/g,rho)
            self.assertAlmostEqual(rho*g,step)
            self.assertAlmostEqual(step/w,.1)
        g=motion('lars-layer-trust-scaling')
        bars=[n for n in g.iter(N+'rect') if n.find(N+'animate') is not None]
        for t in [i/1000 for i in range(1001)]:
            for x,ratio in [(168,3),(294,.375),(516,3)]:
                pair=[n for n in bars if float(n.get('x'))==x]
                a,b=[sample(n.find(N+'animate'),t)[0] for n in pair]
                self.assertAlmostEqual(b,a*ratio)
        for n in bars:
            if n.get('x')=='516':
                self.assertGreaterEqual(float(n.find(N+'animate').get('keyTimes').split(';')[1]),.58)

    def test_lamb_direction_scale_and_marker_attachment(self):
        for mode in ['still','motion']:
            r=E.parse(A/f'lamb-adam-layer-trust-{mode}.svg').getroot()
            groups=[r] if mode=='still' else [n for n in r if n.tag==N+'g']
            ids=[n.get('id') for n in r.iter() if n.get('id')]
            self.assertEqual(len(ids),len(set(ids)))
            for g in groups:
                paths=[n for n in g.iter(N+'path') if n.get('marker-end')]
                self.assertEqual(len(paths),4)
                for layer,factor in enumerate([.2,.5]):
                    blue,teal=paths[2*layer:2*layer+2]
                    a,b=nums(blue.get('d')),nums(teal.get('d'))
                    dx,dy=a[2]-a[0],a[3]-a[1]
                    self.assertAlmostEqual(b[2]-b[0],factor*dx)
                    self.assertAlmostEqual(b[3]-b[1],factor*dy)
                    self.assertAlmostEqual(math.hypot(b[2]-b[0],b[3]-b[1])/math.hypot(dx,dy),factor)
                    # ρ=||w||/||r||, s=ηρr, Δw=-s.
                    self.assertAlmostEqual(.1*[2,5][layer]/1,factor)
                for path in paths:
                    self.assertNotIn('stroke-dashoffset',path.attrib)
                    if g.get('class')=='motion':
                        anim=next(a for a in path if a.get('attributeName')=='d')
                        end=nums(path.get('d'));dx,dy=end[2]-end[0],end[3]-end[1]
                        for i in range(1001):
                            xy=sample(anim,i/1000)
                            self.assertAlmostEqual((xy[2]-xy[0])*dy,(xy[3]-xy[1])*dx)
                            self.assertLessEqual(math.hypot(xy[2]-xy[0],xy[3]-xy[1]),math.hypot(dx,dy)+1e-9)
                        # Marker-end follows the interpolated path endpoint, not a fixed dash-hidden endpoint.
                        self.assertEqual(sample(anim,0),[end[0],end[1],end[0],end[1]])
                        self.assertEqual(sample(anim,1),end)

if __name__=='__main__':unittest.main()
