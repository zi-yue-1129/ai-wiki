"""Probe actual SVG paths, timeline causality, and accumulated label visibility."""
import math,re,unittest,xml.etree.ElementTree as E
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];ASSETS=ROOT/'docs/assets/concept-animations';N='{http://www.w3.org/2000/svg}'

def points(path,steps=1000):
    tokens=re.findall(r'[MCLSQ]|[-+]?(?:\d*\.\d+|\d+)',path);i=0;pos=(0.,0.);prev=None;out=[]
    while i<len(tokens):
        cmd=tokens[i];i+=1;count={'M':2,'L':2,'C':6,'S':4,'Q':4}[cmd]
        nums=list(map(float,tokens[i:i+count]));i+=count;pairs=list(zip(nums[::2],nums[1::2]))
        if cmd=='M':pos=pairs[0];out.append(pos);prev=None;continue
        controls=[pos]+pairs
        if cmd=='S':controls=[pos,tuple(2*pos[k]-prev[k] for k in (0,1))]+pairs
        degree=len(controls)-1
        for j in range(1,steps+1):
            t=j/steps
            out.append(tuple(sum(math.comb(degree,k)*(1-t)**(degree-k)*t**k*controls[k][axis] for k in range(degree+1)) for axis in (0,1)))
        pos=pairs[-1];prev=controls[-2] if degree>1 else None
    return out

def progress(a,t,field='values'):
    ts=list(map(float,a.get('keyTimes').split(';')));vs=list(map(float,a.get(field).split(';')))
    for i in range(len(ts)-1):
        if ts[i]<=t<ts[i+1]:
            return vs[i] if a.get('calcMode')=='discrete' else vs[i]+(vs[i+1]-vs[i])*(t-ts[i])/(ts[i+1]-ts[i])
    return vs[-1]

def point_at(ps,f):
    lengths=[0.]
    for a,b in zip(ps,ps[1:]):lengths.append(lengths[-1]+math.dist(a,b))
    target=f*lengths[-1]
    import bisect
    i=min(max(bisect.bisect_right(lengths,target)-1,0),len(ps)-2)
    frac=(target-lengths[i])/(lengths[i+1]-lengths[i])
    return tuple(ps[i][k]+frac*(ps[i+1][k]-ps[i][k]) for k in (0,1))

def geometry_and_causality(test,root,topic):
    ids={n.get('id'):n for n in root.iter() if n.get('id')}
    marker=ids['rollout-marker'];motion=marker.find(N+'animateMotion');route=points(motion.get('path'));lengths=[0.]
    for a,b in zip(route,route[1:]):lengths.append(lengths[-1]+math.dist(a,b))
    trail=ids['rollout-trail'].find(N+'animate');marker_opacity=marker.find(N+'animate')
    count=4 if topic=='dagger' else 2
    for t in [k/10000 for k in range(9900)]:
        if progress(marker_opacity,t)>0:
            test.assertAlmostEqual(1-progress(trail,t)/100,progress(motion,t,'keyPoints'),places=9)
    arrivals=[]
    for i in range(count):
        transfer=ids[f'transfer-{i}'];a=transfer.find(N+'animateMotion');op=transfer.find(N+'animate');path=points(a.get('path'));start,end=list(map(float,a.get('keyTimes').split(';')))[1:3];arrivals.append(end)
        nearest=min(range(len(route)),key=lambda j:math.dist(route[j],path[0]));test.assertLess(math.dist(route[nearest],path[0]),.25)
        visit=lengths[nearest]/lengths[-1]*float(motion.get('keyTimes').split(';')[1]);test.assertGreaterEqual(start,visit)
        query=ids[f'query-{i}'].find(N+'animate');test.assertEqual(query.get('calcMode'),'discrete')
        for k in range(10001):
            t=k/10000
            expected=float(start<=t<end)
            test.assertEqual(progress(op,t),expected)
            test.assertEqual(progress(query,t),expected)
            if topic=='dagger':
                row=ids[f'dataset-{i}'].find(N+'animate');test.assertEqual(progress(row,t),float(end<=t<1))
        if topic=='dagger':
            test.assertAlmostEqual(path[-1][0],460);test.assertAlmostEqual(path[-1][1],123+46*i)
    if topic=='dagger':
        green=ids['retrained-marker'].find(N+'animateMotion');test.assertGreater(float(green.get('keyTimes').split(';')[1]),max(arrivals))
        gt=ids['retrained-trail'].find(N+'animate')
        for k in range(9900):
            t=k/10000;test.assertAlmostEqual(1-progress(gt,t)/100,progress(green,t,'keyPoints'),places=9)
        test.assertIn('D₁ ∪ D₂ → π₃',''.join(root.itertext()))
    else:
        label=''.join(root.itertext());test.assertIn('u = π*(s) + ε',label);test.assertIn('(s, π*(s))',label);test.assertNotIn('(s, u)',label)
        hi=ids['saved-highlight'].find(N+'animate');test.assertGreaterEqual(float(hi.get('keyTimes').split(';')[1]),max(arrivals))

class DaggerDartTests(unittest.TestCase):
    def test_actual_geometry_and_timeline(self):
        for topic,stem in [('dagger','dagger-dataset-aggregation'),('dart','dart-noisy-expert-recovery')]:
            with self.subTest(topic=topic):geometry_and_causality(self,E.parse(ASSETS/f'{stem}-motion.svg').getroot(),topic)

    def test_early_packet_and_desynchronised_trail_negative(self):
        import copy
        root=E.parse(ASSETS/'dagger-dataset-aggregation-motion.svg').getroot()
        for mutation in ('early','trail'):
            bad=copy.deepcopy(root);ids={n.get('id'):n for n in bad.iter()}
            if mutation=='early':ids['transfer-0'].find(N+'animate').set('calcMode','linear')
            else:ids['rollout-trail'].find(N+'animate').set('keyTimes','0;.28;.99;1')
            with self.assertRaises(AssertionError):geometry_and_causality(self,bad,'dagger')

    def test_bilingual_sources_native_scroll_and_static(self):
        for topic,stem in [('dagger','dagger-dataset-aggregation'),('dart','dart-noisy-expert-recovery')]:
            for lang in ('','.zh-TW'):
                text=(ROOT/f'docs/theory/paradigms/imitation/interactive-imitation/{topic}{lang}.md').read_text()
                for token in ['tabindex="0"','role="region"','concept-motion-scroll','width:640px;max-width:none','data-source-asset-urls',stem+'-still.svg',stem+'-motion.svg','CC BY-SA']:self.assertIn(token,text)
            static=E.parse(ASSETS/f'{stem}-still.svg').getroot();self.assertFalse(any(n.tag in (N+'animate',N+'animateMotion') for n in static.iter()))
        en=(ROOT/'docs/theory/paradigms/imitation/interactive-imitation/dart.md').read_text()
        self.assertIn('not from executing learner rollouts',en);self.assertIn('without the demonstration-collection noise',en)

if __name__=='__main__':unittest.main()
