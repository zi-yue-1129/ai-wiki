"""Actual-SVG regressions: a shared reverse-time axis and a common epsilon endpoint."""
from pathlib import Path
import re, unittest, subprocess, xml.etree.ElementTree as E
ROOT=Path(__file__).resolve().parents[1]; A=ROOT/'docs/assets/concept-animations'; N='{http://www.w3.org/2000/svg}'
def cubic_segments(d):
    tokens=re.findall(r'[MCS]|-?\d+(?:\.\d+)?',d);i=0;segments=[];p=0j;last=0j
    while i<len(tokens):
        cmd=tokens[i];i+=1
        count={'M':2,'C':6,'S':4}[cmd];v=list(map(float,tokens[i:i+count]));i+=count
        q=[complex(*v[j:j+2]) for j in range(0,count,2)]
        if cmd=='M':p=q[0];continue
        if cmd=='S':q.insert(0,2*p-last)
        segments.append([p,*q]);p=q[-1];last=q[-2]
    return segments
def cubic(c,t):return sum(c[k]*[1,3,3,1][k]*(1-t)**(3-k)*t**k for k in range(4))
def y_for_x(segments,x):
    c=next((c for c in segments if c[-1].real>=x),segments[-1]);lo,hi=0,1
    for _ in range(40):
        t=(lo+hi)/2
        if cubic(c,t).real<x:lo=t
        else:hi=t
    return cubic(c,(lo+hi)/2).imag
def value(a,t):
    v=list(map(float,a.get('values').split(';')));times=list(map(float,a.get('keyTimes').split(';'))) if a.get('keyTimes') else [i/(len(v)-1) for i in range(len(v))]
    i=min(next((i-1 for i,x in enumerate(times) if x>t),len(v)-1),len(v)-2);i=max(0,i)
    return v[i] if a.get('calcMode')=='discrete' else v[i]+(v[i+1]-v[i])*(t-times[i])/(times[i+1]-times[i])
class DiffusionMotion(unittest.TestCase):
    def test_shared_reverse_time_and_actual_curves(self):
        r=E.parse(A/'score-sde-flow-motion.svg').getroot();paths={p.get('stroke'):p.get('d') for p in r.iter(N+'path') if p.get('d','').startswith('M 200')}
        circles=[c for c in r.iter(N+'circle') if c.find(N+'animate') is not None]
        self.assertEqual(len(circles),3)
        for c in circles:
            anim={a.get('attributeName'):a for a in c};cs=cubic_segments(paths[c.get('fill')])
            for i in range(10001):
                t=i/10000;x=value(anim['cx'],t);y=value(anim['cy'],t)
                self.assertAlmostEqual(x,200+494*t,places=6)
                self.assertLess(abs(y-y_for_x(cs,x)),.03)
        ode1=cubic_segments(paths['#087F8C']);ode2=cubic_segments(paths['#80B7BB'])
        for i in range(1001):
            x=200+494*i/1000
            self.assertGreater(y_for_x(ode2,x)-y_for_x(ode1,x),0,'deterministic trajectories must not cross')
        for mode in ['motion','still']:
            r=E.parse(A/f'score-sde-flow-{mode}.svg').getroot();ells=list(r.iter(N+'ellipse'));self.assertEqual(len(ells),6)
            if mode=='still':
                for c in r.iter(N+'circle'):
                    if c.get('fill') in paths:self.assertEqual(c.get('cx'),'452')
            for a,b in zip(ells[:3],ells[3:]):
                self.assertEqual([a.get(k) for k in ('cx','rx','ry')],[b.get(k) for k in ('cx','rx','ry')])
    def test_consistency_common_endpoint_and_sequential_arrivals(self):
        for mode in ['motion','still']:
            r=E.parse(A/f'consistency-trajectory-map-{mode}.svg').getroot()
            paths=[p for p in r.iter(N+'path') if p.get('stroke') in ('#3268D9','#D67E36','#087F8C')]
            for p in paths:self.assertEqual(cubic_segments(p.get('d'))[-1][-1],650+230j)
            labels=' '.join(t.text or '' for t in r.iter(N+'text'));self.assertIn('T > t₂ > t₁ > ε',labels);self.assertNotIn('x₀',labels)
            if mode=='still':continue
            dots=[c for c in r.iter(N+'circle') if c.find(N+'animateMotion') is not None];self.assertEqual(len(dots),3)
            for j,c in enumerate(dots):
                m=c.find(N+'animateMotion');op=c.find(N+'animate');kt=list(map(float,m.get('keyTimes').split(';')))
                self.assertEqual(cubic_segments(m.get('path'))[-1][-1],650+230j)
                self.assertAlmostEqual(kt[2],(j+.85)/3,places=10)
                self.assertEqual(value(op,(j+.95)/3),1,'visible arrival hold')
                for k in range(10000):
                    t=(k+.5)/10000
                    self.assertEqual(value(op,t),int(j/3<=t<(j+1)/3))
                for a in c:self.assertEqual(a.get('repeatCount'),'indefinite')
    def test_bilingual_sources_and_scoped_actual_controller(self):
        for topic,stem in [('score-sde','score-sde-flow'),('consistency-models','consistency-trajectory-map')]:
            for lang in ['', '.zh-TW']:
                s=(ROOT/f'docs/theory/paradigms/unsupervised/density-and-generative-models/diffusion/{topic}{lang}.md').read_text()
                for text in ['data-source-asset-urls',f'{stem}-motion.svg',f'{stem}-still.svg','800','CC BY-SA 4.0']:self.assertIn(text,s)
                if topic=='consistency-models':self.assertIn('f(x_\\epsilon,\\epsilon)=x_\\epsilon',s)
            for mode in ['motion','still']:
                r=E.parse(A/f'{stem}-{mode}.svg').getroot()
                for t in r.iter(N+'text'):self.assertGreaterEqual(float(t.get('font-size','12')),12)
        subprocess.run(['node','scripts/test_diffusion_player.cjs'],cwd=ROOT,check=True)
if __name__=='__main__':unittest.main()
