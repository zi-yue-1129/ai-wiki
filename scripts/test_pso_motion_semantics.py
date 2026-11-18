"""Recompute synchronous PSO from old state; check actual SVG memory and motion."""
import bisect
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
B=Path(__file__).resolve().parents[1]/'docs/assets/concept-animations'
NS='{http://www.w3.org/2000/svg}'
COLORS=('#5c7fe7','#e6a33d','#996dc8')
TIMES=(0,.21,.42,.63,.84,1)

def objective(p):return (p[0]-4)**2+(p[1]-3)**2

def trajectory():
    x=[(1.2,5.2),(5.4,4.8),(2.3,1.2)]
    v=[(.6,-.1),(-.4,-.2),(.2,.4)]
    p=list(x);states=[]
    for k in range(5):
        g=min(p,key=objective)
        states.append((list(x),list(p),g,objective(g)))
        # Every velocity uses the same previous iteration's global best.
        new_v=[tuple(.6*v[i][j]+.7*(p[i][j]-x[i][j])+.7*(g[j]-x[i][j]) for j in range(2)) for i in range(3)]
        new_x=[tuple(x[i][j]+new_v[i][j] for j in range(2)) for i in range(3)]
        p=[new_x[i] if objective(new_x[i])<objective(p[i]) else p[i] for i in range(3)]
        x,v=new_x,new_v
    return states

def sample(e,attr,t):
    a=next((a for a in e.findall(NS+'animate') if a.get('attributeName')==attr),None)
    if a is None:return float(e.get(attr,'1'))
    times=list(map(float,a.get('keyTimes').split(';')))
    values=list(map(float,a.get('values').split(';')))
    assert tuple(times)==TIMES and len(values)==len(times)
    i=min(bisect.bisect_right(times,t)-1,len(times)-1)
    if a.get('calcMode')=='discrete' or i==len(times)-1:return values[i]
    f=(t-times[i])/(times[i+1]-times[i]);return values[i]+f*(values[i+1]-values[i])

def screen(p):return (60+52*p[0],294-32*p[1])

class ParticleSwarmGeometry(unittest.TestCase):
    def test_actual_svg_positions_memories_values_and_interpolation(self):
        root=ET.parse(B/'particle-swarm-best-motion.svg').getroot();states=trajectory()
        dots=[next(e for e in root.iter(NS+'circle') if e.get('fill')==c) for c in COLORS]
        rings=[next(e for e in root.iter(NS+'circle') if e.get('stroke')==c and e.get('fill')=='none') for c in COLORS]
        global_ring=next(e for e in root.iter(NS+'circle') if e.get('stroke')=='#159a90')
        readouts=[e for e in root.iter(NS+'text') if e.get('y')=='170']
        labels=[e for e in root.iter(NS+'text') if (e.text or '').startswith('ITERATION')]
        for n in range(10001):
            t=n/10000;k=min(bisect.bisect_right(TIMES,t)-1,4)
            f=0 if k==4 else (t-TIMES[k])/(TIMES[k+1]-TIMES[k])
            for i,(dot,ring) in enumerate(zip(dots,rings)):
                p0=states[k][0][i];p1=states[min(k+1,4)][0][i]
                expected=screen(tuple(p0[j]+f*(p1[j]-p0[j]) for j in range(2)))
                for attr,want in zip(('cx','cy'),expected):self.assertAlmostEqual(sample(dot,attr,t),want,delta=.0051)
                for attr,want in zip(('cx','cy'),screen(states[k][1][i])):self.assertAlmostEqual(sample(ring,attr,t),want,delta=.0051)
            for attr,want in zip(('cx','cy'),screen(states[k][2])):self.assertAlmostEqual(sample(global_ring,attr,t),want,delta=.0051)
            shown=[e for e in readouts if sample(e,'opacity',t)==1]
            self.assertEqual(len(shown),1);self.assertEqual(shown[0].text,f'{states[k][3]:.2f}')
            self.assertEqual([e.text for e in labels if sample(e,'opacity',t)==1],[f'ITERATION {k}'])
        self.assertEqual(states[2][1][0],states[1][1][0])  # overshoot retains pbest
        self.assertEqual(states[3][1][2],states[1][1][2])
        self.assertLess(states[4][3],states[3][3])

    def test_still_and_objective_contours_use_same_initial_state(self):
        root=ET.parse(B/'particle-swarm-best-still.svg').getroot();initial=trajectory()[0]
        self.assertFalse(list(root.iter(NS+'animate')))
        for i,c in enumerate(COLORS):
            dot=next(e for e in root.iter(NS+'circle') if e.get('fill')==c)
            for a,v in zip(('cx','cy'),screen(initial[0][i])):self.assertAlmostEqual(float(dot.get(a)),v,delta=.0051)
        for e in root.iter(NS+'ellipse'):
            self.assertEqual((float(e.get('cx')),float(e.get('cy'))),screen((4,3)))
            self.assertAlmostEqual(float(e.get('rx'))/52,float(e.get('ry'))/32,delta=.0002)
        self.assertIn('5.20',[e.text for e in root.iter(NS+'text')])

if __name__=='__main__':unittest.main()
