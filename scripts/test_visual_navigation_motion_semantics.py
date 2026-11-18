"""Independent actual-SVG navigation geometry, timing, routing and source contracts."""
import math,re,unittest,xml.etree.ElementTree as E
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];ASSETS=ROOT/'docs/assets/concept-animations';N='{http://www.w3.org/2000/svg}'
STEMS={'vint':'vint-goal-waypoint-flow','nomad':'nomad-goal-mask-routing','gnm':'gnm-speed-normalization','ving':'ving-learned-graph-routing'}
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

def route_check(test,root):
    paths=[n for n in root.iter(N+'path') if n.find(N+'animate') is not None]
    markers=[n for n in root.iter(N+'circle') if n.find(N+'animateMotion') is not None]
    test.assertEqual(len(paths),len(markers))
    for path,marker in zip(paths,markers):
        test.assertEqual(path.get('pathLength'),'100');test.assertEqual(path.get('stroke-dasharray'),'100')
        a=path.find(N+'animate');b=marker.find(N+'animateMotion');op=marker.find(N+'animate')
        test.assertEqual(path.get('d'),b.get('path'))
        for k in range(9900):
            t=k/10000
            if progress(op,t)>0:test.assertAlmostEqual(1-progress(a,t)/100,progress(b,t,'keyPoints'),places=9)

def gnm_check(test,root):
    moving=[n for n in root.iter(N+'path') if n.find(N+'animate') is not None]
    lengths=[math.dist(points(n.get('d'))[0],points(n.get('d'))[-1]) for n in moving]
    test.assertAlmostEqual(lengths[1]/lengths[0],2)
    bars=[n for n in root.iter(N+'rect') if n.find(N+'animate') is not None]
    for n,length in zip(moving,lengths):
        test.assertAlmostEqual(float(n.get('stroke-dasharray')),length)
        test.assertEqual(list(map(float,n.find(N+'animate').get('values').split(';')))[:2],[length,length])
    for bar in bars:
        anim=bar.find(N+'animate');test.assertGreater(float(anim.get('keyTimes').split(';')[1]),.58)
        for k in range(10001):test.assertTrue(0<=progress(anim,k/10000)/170<=.5)
    texts=' '.join(root.itertext());test.assertEqual(texts.count('target 0.50'),2);test.assertIn('Δx / (vmax · Δt)',texts)

def ving_label_layer_check(test,root):
    # SVG paints in document order: opaque node disks and labels must cover all route strokes.
    sequence=list(root.iter());routes=[n for n in sequence if n.tag==N+'path' and n.get('stroke')=='#079e94']
    test.assertTrue(routes)
    expected={'S':('112','247'),'A':('254','144'),'B':('254','309'),'C':('464','144'),'D':('464','309'),'G':('679','247')}
    for label,(cx,cy) in expected.items():
        texts=[n for n in sequence if n.tag==N+'text' and n.text==label];test.assertEqual(len(texts),1)
        circles=[n for n in sequence if n.tag==N+'circle' and n.get('cx')==cx and n.get('cy')==cy and n.get('r')=='25'];test.assertEqual(len(circles),1)
        disk=circles[0];text=texts[0];test.assertNotIn(disk.get('fill'),[None,'none','transparent']);test.assertEqual(disk.get('opacity','1'),'1')
        for route in routes:test.assertLess(sequence.index(route),sequence.index(disk))
        test.assertLess(sequence.index(disk),sequence.index(text))

class VisualNavigationTests(unittest.TestCase):
    def test_ving_labels_above_static_fallback_and_animated_route(self):
        import copy
        for mode in ['motion','still']:
            root=E.parse(ASSETS/f'{STEMS["ving"]}-{mode}.svg').getroot();ving_label_layer_check(self,root)
            routes=[n for n in root.iter(N+'path') if n.get('stroke')=='#079e94']
            for index in range(len(routes)):
                bad=copy.deepcopy(root);route=[n for n in bad.iter(N+'path') if n.get('stroke')=='#079e94'][index]
                parent=next(n for n in bad.iter() if route in list(n));parent.remove(route)
                group=bad.find(N+'g');group.append(route)
                with self.assertRaises(AssertionError):ving_label_layer_check(self,bad)

    def test_actual_curves_markers_and_causal_waypoints(self):
        for topic in ['vint','nomad']:
            root=E.parse(ASSETS/f'{STEMS[topic]}-motion.svg').getroot();route_check(self,root)
            if topic=='vint':
                path=next(n for n in root.iter(N+'path') if n.find(N+'animate') is not None);ps=points(path.get('d'))
                waypoints=[n for n in root.iter(N+'circle') if n.get('data-waypoint') and n.find(N+'animate') is not None];self.assertEqual(len(waypoints),5)
                for j,n in enumerate(waypoints):
                    self.assertLess(math.dist((float(n.get('cx')),float(n.get('cy'))),point_at(ps,(j+1)/5)),1e-6)
                    a=n.find(N+'animate');self.assertAlmostEqual(float(a.get('keyTimes').split(';')[1]),.30+.55*(j+1)/5)
                pulse=next(a for a in root.iter(N+'animate') if a.get('attributeName')=='cx');self.assertLess(float(pulse.get('keyTimes').split(';')[1]),.30)
                distance=next(n for n in root if n.get('id')=='distance-output');self.assertEqual(progress(distance.find(N+'animate'),.29),0);self.assertEqual(progress(distance.find(N+'animate'),.31),1)

    def test_gnm_physical_scale_and_normalized_targets(self):
        root=E.parse(ASSETS/f'{STEMS["gnm"]}-motion.svg').getroot();gnm_check(self,root)
        self.assertEqual(.5/(1*1),1/(2*1))
        static=E.parse(ASSETS/f'{STEMS["gnm"]}-still.svg').getroot();displacements=[n for n in static.iter(N+'path') if n.get('stroke') in ['#157c8b','#ad6b1a'] and n.get('stroke-width')=='6'];lengths=[math.dist(points(n.get('d'))[0],points(n.get('d'))[-1]) for n in displacements];self.assertEqual(lengths,[181,362])

    def test_ving_actual_graph_weighted_shortest_route(self):
        import heapq
        root=E.parse(ASSETS/f'{STEMS["ving"]}-motion.svg').getroot();edges=[n for n in root.iter(N+'path') if n.get('stroke')=='#d5e0e9'];weights=[int(n.text) for n in root.iter(N+'text') if n.text in ['2','3','5']];self.assertEqual(len(edges),8);self.assertEqual(len(weights),8)
        coords={n.text:(float(n.get('x')),float(n.get('y'))-6) for n in root.iter(N+'text') if n.text in 'SABCDG' and len(n.text)==1};self.assertEqual(len(coords),6)
        lookup={v:k for k,v in coords.items()};graph={k:[] for k in coords}
        for path,w in zip(edges,weights):
            ps=points(path.get('d'),steps=1);u,v=lookup[ps[0]],lookup[ps[-1]];graph[u].append((v,w));graph[v].append((u,w))
        queue=[(0,'S',['S'])];seen=set()
        while queue:
            cost,u,route=heapq.heappop(queue)
            if u in seen:continue
            seen.add(u)
            if u=='G':break
            for v,w in graph[u]:heapq.heappush(queue,(cost+w,v,route+[v]))
        selected=next(n for n in root.iter(N+'path') if n.get('id')=='selected-route');self.assertEqual([lookup[x] for x in points(selected.get('d'),1)],route);self.assertEqual((cost,route),(6,['S','B','D','G']));self.assertIn('Cost = 6',''.join(root.itertext()));self.assertEqual(selected.get('pathLength'),'100')
        for g in root.iter(N+'g'):
            a=g.find(N+'animate')
            if a is not None:self.assertGreaterEqual(float(a.get('keyTimes').split(';')[1]),.79)

    def test_goal_attention_modes_and_bilingual_mobile_contract(self):
        root=E.parse(ASSETS/f'{STEMS["nomad"]}-motion.svg').getroot()
        labels={n.text:float(n.get('x')) for n in root.iter(N+'text')}
        self.assertLess(labels['m = 1'],320);self.assertLess(labels['EXPLORE'],320);self.assertGreater(labels['m = 0'],320);self.assertGreater(labels['NAVIGATE'],320)
        paths={n.get('d'):n for n in root.iter(N+'path')};self.assertEqual(paths['M177 134 L194 134'].get('stroke-dasharray'),'3 5');self.assertIsNone(paths['M481 134 L498 134'].get('stroke-dasharray'));self.assertIn('M123 122 L168 146',paths)
        for topic,stem in STEMS.items():
            for lang in ['', '.zh-TW']:
                text=(ROOT/f'docs/applications/robotics/navigation/{topic}{lang}.md').read_text()
                for word in ['tabindex="0"','role="region"','concept-motion-scroll','width:640px;max-width:none','data-source-asset-urls',stem+'-motion.svg',stem+'-still.svg','CC BY-SA']:self.assertIn(word,text)
            static=E.parse(ASSETS/f'{stem}-still.svg').getroot();self.assertFalse(any(n.tag in [N+'animate',N+'animateMotion'] for n in static.iter()))

    def test_negative_wrong_dash_and_physical_scale(self):
        root=E.parse(ASSETS/f'{STEMS["vint"]}-motion.svg').getroot();path=next(n for n in root.iter(N+'path') if n.find(N+'animate') is not None);path.attrib.pop('pathLength')
        with self.assertRaises(AssertionError):route_check(self,root)
        root=E.parse(ASSETS/f'{STEMS["gnm"]}-motion.svg').getroot();path=[n for n in root.iter(N+'path') if n.find(N+'animate') is not None][1];path.set('d','M84 298 L399 298')
        with self.assertRaises(AssertionError):gnm_check(self,root)

if __name__=='__main__':unittest.main()
