"""Independent schedule, shared-clock and curve-geometry checks; not browser QA."""
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as E
A=Path(__file__).resolve().parents[1]/'docs/assets/concept-animations'
N='{http://www.w3.org/2000/svg}'

def schedule(step, decay):
    cycle=min(int(step//4),2)
    phase=(step-4*cycle)/4
    return .1+.9*(1-abs(2*phase-1))/(2**cycle if decay else 1)

def sample(anim,t):
    ts=list(map(float,anim.get('keyTimes').split(';')))
    vs=list(map(float,anim.get('values').split(';')))
    for i in range(1,len(ts)):
        if t<=ts[i]:
            f=(t-ts[i-1])/(ts[i]-ts[i-1]);return vs[i-1]+f*(vs[i]-vs[i-1])
    return vs[-1]

class CLRComparison(unittest.TestCase):
    def test_shared_time_and_exact_schedule_at_1201_intermediate_times(self):
        r=E.parse(A/'clr-triangular2-sweep-motion.svg').getroot()
        markers=list(r.iter(N+'circle'));self.assertEqual(len(markers),2)
        scan=next(e for e in r.iter(N+'line') if e.find(N+'animate') is not None)
        for j in range(1201):
            t=j/1200
            for decay,c in enumerate(markers):
                a={x.get('attributeName'):x for x in c.findall(N+'animate')}
                x=sample(a['cx'],t);y=sample(a['cy'],t)
                self.assertAlmostEqual(x,68+532*t,delta=.006)
                self.assertAlmostEqual(y,270-(schedule(12*t,decay)-.1)*168/.9,delta=.001)
                self.assertAlmostEqual(x,sample(scan.find(N+'animate'),t),places=7)
            # All markers, cursor and reveal are driven by the same twelve-second clock.
        for a in r.iter(N+'animate'):
            self.assertEqual(a.get('dur'),'12s');self.assertEqual(a.get('repeatCount'),'indefinite')
        reveal=next(r.iter(N+'clipPath')).find(N+'rect').find(N+'animate')
        self.assertEqual((reveal.get('from'),reveal.get('to')),('0','532'))
    def test_visible_curves_and_static_fallback(self):
        for kind in ['motion','still']:
            r=E.parse(A/f'clr-triangular2-sweep-{kind}.svg').getroot()
            for decay,color in enumerate(['#087F82','#CB6C35']):
                paths=[p for p in r.iter(N+'path') if p.get('stroke')==color and len(p.get('d',''))>100]
                self.assertTrue(paths)
                for p in paths:
                    pts=[tuple(map(float,v)) for v in re.findall(r'[ML]([\d.]+),([\d.]+)',p.get('d'))]
                    self.assertEqual(len(pts),121)
                    for j,(x,y) in enumerate(pts):
                        self.assertAlmostEqual(x,68+532*j/120,delta=.006)
                        self.assertAlmostEqual(y,270-(schedule(j/10,decay)-.1)*168/.9,delta=.006)
            if kind=='still':self.assertFalse(list(r.iter(N+'animate')))
    def test_consolidated_bilingual_embed_and_sgdr_unchanged(self):
        for suffix in ['', '.zh-TW']:
            t=(A.parents[1]/f'theory/optimization/cyclical-learning-rates{suffix}.md').read_text()
            self.assertEqual(t.count('<img '),1)
            self.assertIn('<img data-source-asset-urls',t)
            for attr in ['src','data-motion-src','data-still-src']:
                self.assertRegex(t,attr+r'="[^\"]*clr-triangular2-sweep-(?:motion|still).svg"')
            self.assertIn('0.325',t)
        self.assertFalse((A/'sgdr-cosine-restart-motion.svg').exists())
if __name__=='__main__':unittest.main()
