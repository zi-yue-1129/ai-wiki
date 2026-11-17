"""Recompute the recommender examples and check source SVG keyframes."""
from pathlib import Path
import math,re
import xml.etree.ElementTree as E
ROOT=Path(__file__).resolve().parents[1];ASSETS=ROOT/'docs/assets/concept-animations';NS='{http://www.w3.org/2000/svg}'
def svg(name,kind='motion'):return E.parse(ASSETS/f'{name}-{kind}.svg').getroot()
def animations(name):return list(svg(name).iter(NS+'animate'))
def vals(e):return list(map(float,e.get('values').split(';')))
def near(a,b,tol=.011):assert abs(a-b)<tol,(a,b)
def loop(states):return states+states[-2::-1]
def check(name,expected):
    aa=animations(name);assert len(aa)==len(expected)
    for e,seq in zip(aa,expected):
        vv=vals(e);assert len(vv)==len(seq)
        for a,b in zip(vv,seq):near(a,b)
    assert len({e.get('keyTimes') for e in aa})==1
# Joint SGD: both gradients use the same old vectors, not in-place updates.
p=[.4,.2];q=[.7,.3];states=[]
for k in range(5):
    score=sum(a*b for a,b in zip(p,q));states.append((p,q,score))
    e=1-score;p,q=([a+.2*e*b for a,b in zip(p,q)],[b+.2*e*a for a,b in zip(p,q)])
fns=[lambda p,q,s:195+160*p[0],lambda p,q,s:301-160*p[1]]
fns+=fns[:]
fns += [lambda p,q,s:195+160*q[0],lambda p,q,s:301-160*q[1]]*2
fns += [lambda p,q,s:268*s,lambda p,q,s:268*(1-s)]
check('mf-coupled-sgd',[loop([f(*s) for s in states]) for f in fns]+[loop([470+60*k for k in range(5)])])
near(states[-1][2],.7643,.00005)
# BPR ascent with fixed user and zero regularisation.
i,j=.5,1.3;rank=[]
for k in range(5):
    delta=i-j;loss=math.log1p(math.exp(-delta));rank.append((i,j,delta,loss))
    g=1/(1+math.exp(delta));i,j=i+.4*g,j-.4*g
fns=[lambda i,j,d,l:148.75*i,lambda i,j,d,l:148.75*j,lambda i,j,d,l:580.2+124*d,lambda i,j,d,l:580.2+124*d,lambda i,j,d,l:341-103*l,lambda i,j,d,l:580.2+124*d,lambda i,j,d,l:341-103*l]
check('bpr-pairwise-ranking',[loop([f(*s) for s in rank]) for f in fns])
near(rank[-1][2],.8518,.00005);near(rank[-1][3],.3553,.00005)
# Exact block solves for sum squared error + lambda * sum squared factors.
R=((1,.7),(.3,.9));p=[.4,.6];q=[.5,.9];states=[]
for k in range(7):
    obj=sum((R[u][i]-p[u]*q[i])**2 for u in range(2) for i in range(2))+.1*sum(v*v for v in p+q)
    states.append((p,q,obj))
    if k%2==0:p=[sum(R[u][i]*q[i] for i in range(2))/(.1+sum(v*v for v in q)) for u in range(2)]
    else:q=[sum(R[u][i]*p[u] for u in range(2))/(.1+sum(v*v for v in p)) for i in range(2)]
assert all(states[k+1][2]<states[k][2] for k in range(6))
near(states[0][2],1.0432,1e-10);near(states[-1][2],.5053,.00005)
fns=[lambda p,q,o:172.8*p[0],lambda p,q,o:172.8*p[1],lambda p,q,o:172.8*q[0],lambda p,q,o:172.8*q[1]]
check('mf-als-alternating',[loop([f(*s) for s in states]) for f in fns]+[loop([456+45*k for k in range(7)]),loop([170+270*(states[0][2]-s[2]) for s in states])])
# The nonlinear saturation markers and bar share one margin at every keyframe.
aa=animations('bpr-gradient-saturation');arrays=list(map(vals,aa));assert len(set(map(len,arrays)))==1
for x,y,x2,y2,w in zip(*arrays):
    delta=(x-259)/61;g=1/(1+math.exp(delta));near(x,x2,.0001)
    near(y,252-38*math.log1p(math.exp(-delta)),.0002);near(y2,339-74*g,.0002);near(w,213*g,.0002)
assert len(arrays[0])==121
# 10 interpolated states per interval stay close to the analytic curve as well.
for k in range(len(arrays[0])-1):
    for n in range(10):
        f=n/10;x,y,_,yg,w=[a[k]*(1-f)+a[k+1]*f for a in arrays]
        d=(x-259)/61;g=1/(1+math.exp(d))
        near(y,252-38*math.log1p(math.exp(-d)),.006);near(yg,339-74*g,.006);near(w,213*g,.02)
# Stills must preserve the represented endpoint (initial SGD/BPR, final ALS).
for name in ('mf-coupled-sgd','bpr-pairwise-ranking'):
    motion=svg(name);still=svg(name,'still')
    # SVG element order is identical apart from animation children.
    me=[e for e in motion.iter() if e.tag != NS+'animate']
    se=[e for e in still.iter() if e.tag != NS+'animate']
    assert len(me)==len(se)
    for m,e in zip(me,se):
        for a in m.findall(NS+'animate'):
            near(float(e.get(a.get('attributeName'))),vals(a)[0])
r=svg('mf-als-alternating','still')
rects=[e for e in r.iter(NS+'rect') if e.get('height')=='20' and e.get('fill') in ('#0b8d86','#dd8556')]
for e,v in zip(rects,states[-1][0]+states[-1][1]):near(float(e.get('width')),172.8*v)
for name in ('mf-coupled-sgd','mf-als-alternating','bpr-pairwise-ranking','bpr-gradient-saturation'):
    for kind in ('motion','still'):
        assert 'font-family:Arial,Helvetica,sans-serif' in (ASSETS/f'{name}-{kind}.svg').read_text()
for name in ('bpr','matrix-factorization'):
    for pth in (ROOT/'docs/theory/models/recommender').glob(name+'*.md'):
        s=pth.read_text();assert not re.search(r'^\s*\${1,2}\s*$',s,re.M)
        assert 'width:800px' not in s
        assert s.count('width:640px;min-width:640px;max-width:none;height:auto')==2
        assert s.count('\\[')==s.count('\\]')
print('Recommender SVGs: joint old-state SGD, BPR signs, ridge ALS, 121 saturation keyframes + interpolation, bilingual math/layout passed')
