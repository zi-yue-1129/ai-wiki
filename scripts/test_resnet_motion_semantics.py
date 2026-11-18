"""Source-based checks for the synthetic ResNet diagrams (no browser required)."""
import math
import re
from pathlib import Path
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'docs/assets/concept-animations'
NS='{http://www.w3.org/2000/svg}'
def load(name,kind='motion'):
    return ET.parse(ASSETS/f'resnet-{name}-{kind}.svg').getroot()
def points(path):
    nums=list(map(float,re.findall(r'[-+]?[0-9]*\.?[0-9]+',path)))
    return list(zip(nums[::2],nums[1::2]))
def values(e,name):return list(map(float,e.get(name).split(';')))
def position(e,t):
    pts=points(e.get('path'));lens=[0]
    for a,b in zip(pts,pts[1:]):lens.append(lens[-1]+math.dist(a,b))
    times=values(e,'keyTimes');ks=values(e,'keyPoints')
    i=min(len(times)-2,max(k for k,v in enumerate(times) if v<=t))
    f=(t-times[i])/(times[i+1]-times[i]);d=(ks[i]+f*(ks[i+1]-ks[i]))*lens[-1]
    i=min(len(lens)-2,max(k for k,v in enumerate(lens) if v<=d+1e-8))
    f=(d-lens[i])/(lens[i+1]-lens[i]);return tuple(a+f*(b-a) for a,b in zip(pts[i],pts[i+1]))
for kind in ('motion','still'):
    r=load('depth-gradient-factors',kind)
    for line,base in zip(r.iter(NS+'polyline'),(.9,.1)):
        for d,(x,y) in enumerate(points(line.get('points'))):
            assert abs(x-(90+67*d))<.001
            assert abs(y-(312-160*base**d))<.0051
    text=' '.join(e.text or '' for e in r.iter(NS+'text'))
    assert f'{.9**6:.6f}' in text and f'{.1**6:.6f}' in text
r=load('depth-gradient-factors')
motions=list(r.iter(NS+'animateMotion'))
assert len(motions)==2
for d in range(61):
    t=d/60
    for m in motions:assert abs(position(m,t)[0]-(90+402*t))<1e-6
r=load('postrelu-gate');m=next(r.iter(NS+'animateMotion'))
gate=next(e for e in r.iter(NS+'animate') if e.get('attributeName')=='width')
assert gate.get('calcMode')=='discrete'
for i in range(1001):
    t=i/1000
    if min(abs(t-.22),abs(t-.78))<1e-7:continue # classical derivative undefined exactly at kink
    x,y=position(m,t)
    times=values(gate,'keyTimes');k=max(k for k,v in enumerate(times) if v<=t)
    width=values(gate,'values')[k]
    assert width==(152 if x>290 else 0),(t,x,width)
    assert abs(y-(296 if x<=290 else 296-(x-290)*133/150))<1e-7
assert (4+2*1-3)//2+1 == (4-1)//2+1 == 2
assert 2-.5*2==1 and 1-.5==.5
for kind in ('motion','still'):
    text=' '.join(e.text or '' for e in load('identity-gradient',kind).iter(NS+'text'))
    for token in ('x = 2','y = 1','gₓ = 0.5','F′ = −0.5','gᵧ = 1'):assert token in text
    text=' '.join(e.text or '' for e in load('projection-shortcut',kind).iter(NS+'text'))
    assert '4 × 4 × 1' in text and text.count('2 × 2 × 2')==3
for p in (ROOT/'docs/theory/models/cnn/backbones-and-scaling/resnet').glob('index*.md'):
    s=p.read_text()
    assert not re.search(r'^\s*\$\s*$',s,re.M),p
    assert 'width:800px' not in s
    assert s.count('width:640px;min-width:640px;max-width:none;height:auto')==4
    assert s.count('\\[')==s.count('\\]')
    for token in ('0.531441','0.8','-0.5x','padding 1'):assert token in s
print('ResNet: SVG gradient values, shapes, 61 synchronized depths, 999 gate states, bilingual math/layout passed')
