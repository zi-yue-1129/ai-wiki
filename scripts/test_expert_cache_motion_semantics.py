"""Actual SVG event ordering: miss, eviction, transfer, residency, later hit."""
import bisect
from functools import lru_cache
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as E
B=Path(__file__).resolve().parents[1]/'docs/assets/concept-animations';N='{http://www.w3.org/2000/svg}'
@lru_cache(None)
def data(a):
    ts=tuple(map(float,a.get('keyTimes').split(';')))
    vs=tuple(map(float,a.get('values',a.get('keyPoints','')).split(';')))
    assert len(ts)==len(vs) and ts[0]==0 and ts[-1]==1
    assert all(x<y for x,y in zip(ts,ts[1:]))
    return ts,vs

def value(a,t):
    ts,vs=data(a);i=min(bisect.bisect_right(ts,t)-1,len(ts)-1)
    if a.get('calcMode')=='discrete' or i==len(ts)-1:return vs[i]
    u=(t-ts[i])/(ts[i+1]-ts[i]);return vs[i]+u*(vs[i+1]-vs[i])

def opacity(e,t):return value(e.find(N+'animate'),t)

class ExpertCacheCausality(unittest.TestCase):
    def test_all_time_states_and_loop(self):
        root=E.parse(B/'expert-cache-miss-motion.svg').getroot()
        get=lambda name:next(e for e in root if e.get('class')==name)
        old,new=get('cache-old'),get('cache-new');particle=get('particle')
        miss,loaded,hit=map(get,('status-miss','status-loaded','status-hit'))
        phases=[e for e in root if e.get('class') in ('phase','phase-final')]
        self.assertEqual(len(phases),5)
        motion=particle.find(N+'animateMotion')
        self.assertEqual(motion.get('path'),'M243 190 Q345 247 556 190')
        self.assertEqual(motion.get('keyPoints'),'0;0;1;1')
        self.assertEqual([float(v) for v in motion.get('keyTimes').split(';')],[0,.28,.62,1])
        for i in range(10001):
            t=i/10000
            # t=1 explicitly resets to the same state as t=0 for replay.
            period=0 if t==1 else t
            old_on=int(period<.22);new_on=int(period>=.62);moving=int(.28<=period<.62)
            self.assertEqual(opacity(old,t),old_on);self.assertEqual(opacity(new,t),new_on)
            self.assertLessEqual(old_on+new_on,1)
            self.assertEqual(opacity(particle,t),moving)
            self.assertFalse(moving and (old_on or new_on))
            self.assertEqual(opacity(miss,t),int(period<.62))
            self.assertEqual(opacity(loaded,t),int(.62<=period<.78))
            self.assertEqual(opacity(hit,t),int(period>=.78))
            self.assertEqual(sum(opacity(e,t) for e in phases),1)
            if period>=.78:self.assertTrue(new_on and not moving)
            if .28<=t<=.62:self.assertAlmostEqual(value(motion,t),(t-.28)/.34,delta=1e-12)
        # Host E1 remains throughout; eviction is of the GPU copy only.
        self.assertTrue(any(e.tag==N+'text' and e.text=='E1' and e.get('x')=='157' for e in root))
        self.assertTrue(any(e.tag==N+'text' and e.text=='E0' and e.get('x')=='474' for e in root))

    def test_still_and_readability(self):
        for kind in ('motion','still'):
            p=B/f'expert-cache-miss-{kind}.svg';root=E.parse(p).getroot();self.assertLess(p.stat().st_size,51200)
            style=root.find(N+'style').text
            self.assertNotRegex(style,r'font-size:\s*(?:10|11)px')
            self.assertRegex(style,r'\.small\{font-size:12px')
            if kind=='still':
                self.assertFalse(list(root.iter(N+'animate'))+list(root.iter(N+'animateMotion')))
                def visible(e, parent_opacity=1):
                    alpha=parent_opacity*float(e.get('opacity','1'))
                    return ([e] if alpha>0 else []) + [x for child in e for x in visible(child,alpha)]
                gpu=[e.text for e in visible(root) if e.tag==N+'text' and e.get('x') in ('474','560')]
                self.assertEqual(gpu,['E0','E2'])
                self.assertIn('HIT · GPU REUSE',[e.text for e in root.iter(N+'text')])

if __name__=='__main__':unittest.main()
