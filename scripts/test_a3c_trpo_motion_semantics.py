"""Actual SVG async states, backward returns and constrained signed contributions."""
import math,re,unittest,xml.etree.ElementTree as E
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];ASSETS=ROOT/'docs/assets/concept-animations';N='{http://www.w3.org/2000/svg}'
STEMS=['a3c-async-gradient','a3c-nstep-return','trpo-kl-backtracking','trpo-ratio-surrogate']
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
    ts=list(map(float,a.get('keyTimes','0;1').split(';')));vs=list(map(float,a.get(field).split(';')))
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



def animate(n,attr):return next(a for a in n.findall(N+'animate') if a.get('attributeName')==attr)
def async_check(case,r):
    workers=r.findall(f"{N}circle[@class='motion']");case.assertEqual(len(workers),2)
    groups=[g for g in r.findall(f"{N}g[@class='motion']") if g.find(N+'text') is not None];case.assertEqual(len(groups),3)
    arrivals=[]
    for i,w in enumerate(workers):
        a=w.find(N+'animateMotion');case.assertIsNotNone(a);end=float(a.get('keyTimes').split(';')[-2]);arrivals.append(end);ps=points(a.get('path'));case.assertEqual(ps[-1],(490.,142. if i==0 else 217.))
        stops=[0,.13,.25,.39,.43,.49,.51] if i==0 else [.35,.47,.60,.71,.75,.85,.87]
        expected=[(160,135),(216,135),(272,135),(377,135),(424,136),(480,130),(490,142)] if i==0 else [(160,239),(216,239),(272,239),(377,239),(424,240),(480,236),(490,217)]
        for t,xy in zip(stops,expected):case.assertLess(math.dist(point_at(ps,progress(a,t,'keyPoints')),xy),.005)
        case.assertEqual(progress(animate(w,'opacity'),end),1)
    for i in range(10000):
        t=i/10000;shown=[j for j,g in enumerate(groups) if progress(animate(g,'opacity'),t)>.5];case.assertEqual(shown,[sum(t>=x for x in arrivals)])
    labels=' '.join(r.itertext());case.assertIn('W1  θ₀',labels);case.assertIn('W2  θ₀',labels)

def nstep_check(case,r):
    marker=r.find(f"{N}circle[@class='motion']");cx=animate(marker,'cx');groups=[g for g in r.findall(f"{N}g[@class='motion']") if g.find(N+'text') is not None];rs={g.find(N+'text').text[:2]:g for g in groups}
    for label in ['R₀','R₁','R₂']:
        g=rs[label];a=animate(g,'opacity');t=float(a.get('keyTimes').split(';')[1]);case.assertAlmostEqual(progress(cx,t),float(g.find(N+'text').get('x')))
    advantage=next(g for g in groups if g.find(N+'text').text.startswith('A₀'));case.assertGreater(float(animate(advantage,'opacity').get('keyTimes').split(';')[1]),float(animate(rs['R₀'],'opacity').get('keyTimes').split(';')[1]))
    vals=[1,0,2];R=[0,0,0,1]
    for i in [2,1,0]:R[i]=vals[i]+.9*R[i+1]
    for i,label in enumerate(['R₀','R₁','R₂','R₃']):case.assertIn(f'{R[i]:.3f}',rs[label].find(N+'text').text)
    case.assertAlmostEqual(R[0],sum(.9**j*x for j,x in enumerate(vals))+.9**3);case.assertIn(f'{R[0]-2.5:.3f}',advantage.find(N+'text').text)
    terminal=sum(.9**j*x for j,x in enumerate(vals));case.assertAlmostEqual(terminal,2.62)

def ratio_check(case,r):
    adv=[float(n.text.replace('−','-')) for n in r.iter(N+'text') if n.get('x')=='204'];ratios=[float(n.text) for n in r.iter(N+'text') if n.get('x')=='340'];products=[a*b for a,b in zip(adv,ratios)];case.assertEqual(len(products),3);case.assertAlmostEqual(sum(products)/3,1.24/3);case.assertAlmostEqual(sum(adv)/3,.3)
    bars=[n for n in r.iter(N+'rect') if n.get('height')=='12'];case.assertGreaterEqual(len(bars),3)
    for n in bars:
        i={120:0,183:1,246:2}[int(n.get('y'))];v=products[i];case.assertAlmostEqual(float(n.get('width')),abs(v)*60);case.assertAlmostEqual(float(n.get('x')),480+min(v,0)*60)
        if n.find(N+'animate') is not None:
            w=animate(n,'width')
            for j in range(1001):
                t=j/1000;width=progress(w,t);case.assertGreaterEqual(width,0);case.assertLessEqual(width,abs(v)*60+1e-9)
                if v<0:case.assertAlmostEqual(progress(animate(n,'x'),t)+width,480)
    for g in r.findall(f"{N}g[@class='motion']"):
        text=g.find(N+'text').text
        if not text.startswith('Mean'):
            i=['+1.20','−0.40','+0.44'].index(text);start=float(animate(g,'opacity').get('keyTimes').split(';')[1]);b=next(n for n in bars if n.get('class')=='motion' and int(n.get('y'))==[120,183,246][i]);case.assertAlmostEqual(progress(animate(b,'width'),start),abs(products[i])*60)

class ActorCriticTests(unittest.TestCase):
    def test_async_exact_path_arrival_and_exclusive_global_state(self):async_check(self,E.parse(ASSETS/(STEMS[0]+'-motion.svg')).getroot())
    def test_nstep_numbers_terminal_and_arrival(self):nstep_check(self,E.parse(ASSETS/(STEMS[1]+'-motion.svg')).getroot())
    def test_trpo_kl_collinear_halving_and_surrogate_guard(self):
        for variant in ['motion','still']:
            r=E.parse(ASSETS/(STEMS[2]+'-'+variant+'.svg')).getroot();texts=' '.join(r.itertext());self.assertIn('surrogate improves',texts);self.assertIn('both checks required',texts)
            circles=[c for c in r.findall(N+'circle') if c.get('class')!='motion'];old,full,back=[(float(c.get('cx')),float(c.get('cy'))) for c in circles[:3]];self.assertEqual(back,tuple((x+y)/2 for x,y in zip(old,full)))
            e=r.find(N+'ellipse');ellipse=lambda p:((p[0]-float(e.get('cx')))/float(e.get('rx')))**2+((p[1]-float(e.get('cy')))/float(e.get('ry')))**2;self.assertGreater(ellipse(full),1);self.assertLess(ellipse(back),1)
            accept=lambda kl,gain:kl<=1 and gain>0;self.assertFalse(accept(1.8,.1));self.assertFalse(accept(.55,-.1));self.assertTrue(accept(.55,.1))
            if variant=='motion':
                marker=r.find(f"{N}circle[@class='motion']")
                for g in r.findall(f"{N}g[@class='motion']"):
                    label=g.find(N+'text').text;start=float(animate(g,'opacity').get('keyTimes').split(';')[1]);target=full if label=='rejected' else back;self.assertEqual((progress(animate(marker,'cx'),start),progress(animate(marker,'cy'),start)),target)
    def test_ratio_exact_signed_geometry_and_completion(self):
        for variant in ['motion','still']:ratio_check(self,E.parse(ASSETS/(STEMS[3]+'-'+variant+'.svg')).getroot())
    def test_bilingual_mobile_static_and_sources(self):
        base=ROOT/'docs/theory/paradigms/reinforcement-learning/policy-gradient-and-actor-critic'
        for topic in ['a3c','trpo']:
            for lang in ['','.zh-TW']:
                s=(base/topic/('index'+lang+'.md')).read_text();self.assertEqual(s.count('tabindex="0"'),2);self.assertEqual(s.count('data-source-asset-urls'),2);self.assertEqual(s.count('width:640px;max-width:none'),2);self.assertIn('CC BY-SA',s)
                if topic=='a3c':self.assertIn(r"V(s_t;\theta_v')",s)
        for stem in STEMS:self.assertFalse(any('animate' in n.tag for n in E.parse(ASSETS/(stem+'-still.svg')).getroot().iter()))
    def test_negative_early_return_and_unsigned_wrong_scale(self):
        r=E.parse(ASSETS/(STEMS[0]+'-motion.svg')).getroot();g=r.find(f"{N}g[@id='shared-0']");animate(g,'opacity').set('keyTimes','0;1')
        with self.assertRaises(AssertionError):async_check(self,r)
        r=E.parse(ASSETS/(STEMS[1]+'-motion.svg')).getroot();g=next(g for g in r.findall(f"{N}g[@class='motion']") if g.find(N+'text') is not None and g.find(N+'text').text.startswith('R₂'));animate(g,'opacity').set('keyTimes','0;.33;.96')
        with self.assertRaises(AssertionError):nstep_check(self,r)
        r=E.parse(ASSETS/(STEMS[3]+'-motion.svg')).getroot();bar=next(n for n in r.iter(N+'rect') if n.get('height')=='12');bar.set('width','75')
        with self.assertRaises(AssertionError):ratio_check(self,r)
if __name__=='__main__':unittest.main()
