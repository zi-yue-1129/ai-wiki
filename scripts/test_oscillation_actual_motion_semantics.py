"""Check animated rounding against actual markers, not just endpoint arithmetic."""
import bisect
import math
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'docs/assets/concept-animations'
NS='{http://www.w3.org/2000/svg}'

def read(stem,kind='motion'):return ET.parse(ASSETS/f'{stem}-{kind}.svg').getroot()

def at(e,attr,t):
    a=next((a for a in e.findall(NS+'animate') if a.get('attributeName')==attr),None)
    if a is None:return float(e.get(attr,'1' if attr=='opacity' else '0'))
    v=list(map(float,a.get('values').split(';')));k=list(map(float,a.get('keyTimes').split(';'))) if a.get('keyTimes') else [i/(len(v)-1) for i in range(len(v))]
    i=min(len(k)-1,max(0,bisect.bisect_right(k,t)-1))
    if a.get('calcMode')=='discrete' or i==len(k)-1:return v[i]
    q=(t-k[i])/(k[i+1]-k[i]);return v[i]*(1-q)+v[i+1]*q

def points(path):
    import re
    n=list(map(float,re.findall(r'-?\d+(?:\.\d+)?',path)));return list(zip(n[::2],n[1::2]))
def height_at(pts,x):
    xs=[p[0] for p in pts];i=max(0,min(len(pts)-2,bisect.bisect_right(xs,x)-1));q=(x-xs[i])/(xs[i+1]-xs[i]);return pts[i][1]*(1-q)+pts[i+1][1]*q
class OscillationSvgTests(unittest.TestCase):
    def test_theta_phase_cursor_and_markers_remain_synchronized(self):
        r=read('theta-gamma-phase-amplitude');circles=list(r.iter(NS+'circle'));line=next(e for e in r.iter(NS+'line') if e.find(NS+'animate') is not None)
        self.assertFalse(list(r.iter(NS+'animateMotion')))
        for i in range(10001):
            t=i/10000;theta=math.sin(2*math.pi*t-math.pi/2)
            for c in circles:
                self.assertLess(abs(at(c,'cx',t)-at(line,'x1',t)),.00001)
                expected=136-30*theta if c.get('fill')=='#2778a8' else 235-(8+13*(1+theta))
                self.assertLess(abs(at(c,'cy',t)-expected),.017)
    def test_receiver_is_translated_without_amplitude_morphing(self):
        r=read('coherence-phase-gating');g=next(e for e in r.iter(NS+'g') if e.get('data-phase-period'));p=g.find(NS+'path');pts=points(p.get('d'));a=g.find(NS+'animateTransform')
        self.assertIsNone(p.find(NS+'animate'));self.assertEqual(a.get('keyTimes'),'0;0.5;1');self.assertEqual(a.get('values'),'0 0;-63.666666667 0;0 0')
        for t in [0,.0625,.125,.2,.25,.437,.5,.75,.937]:
            phi=2*math.pi*min(t,1-t);shift=phi*(382/3)/(2*math.pi)
            for i in range(77):
                x=120+382*i/76;expected=230-25*math.sin(2*math.pi*(x-120)/(382/3)+phi)
                self.assertLess(abs(height_at(pts,x+shift)-expected),.008)
    def test_gain_and_phase_marker_agree_at_all_intermediate_times(self):
        r=read('coherence-phase-gating');bar=next(e for e in r.iter(NS+'rect') if e.get('fill')=='#16aaa0');marker=next(r.iter(NS+'circle'))
        for i in range(10001):
            t=i/10000;phi=(at(marker,'cx',t)-153)/333*math.pi;gain=(1+math.cos(phi))/2
            self.assertLess(abs(at(bar,'height',t)-156*gain),.06)
            self.assertAlmostEqual(at(bar,'y',t)+at(bar,'height',t),280,places=5)

if __name__=='__main__':unittest.main()
