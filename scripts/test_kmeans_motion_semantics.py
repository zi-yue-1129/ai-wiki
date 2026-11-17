#!/usr/bin/env python3
"""Numerically verify the synthetic k-means teaching diagrams."""
from pathlib import Path
import itertools
import math
import xml.etree.ElementTree as ET
A = Path(__file__).resolve().parents[1] / 'docs/assets/concept-animations'
N = {'s':'http://www.w3.org/2000/svg'}
def root(name): return ET.parse(A / (name+'.svg')).getroot()
def vals(e,attr):
    return [float(x) for x in next(a for a in e.findall('s:animate',N) if a.get('attributeName')==attr).get('values').split(';')]
def test_d2():
    xs=[0,1,2,3,8,9,10,11]
    ws=[[min((x-c)**2 for c in cs) for x in xs] for cs in [[1],[1,10]]]
    assert list(map(sum,ws))==[300,12]
    bars=[e for e in root('kmeans-plusplus-d2-motion').iter() if e.tag.endswith('rect') and any(a.get('attributeName')=='height' for a in e)]
    assert len(bars)==8
    for i,b in enumerate(bars):
        hs,ys=vals(b,'height'),vals(b,'y')
        for k,w in [(0,ws[0]),(2,ws[1])]:
            assert abs(hs[k]-324*w[i]/sum(w))<=.51
        assert all(abs(h+y-286)<1e-9 for h,y in zip(hs,ys))
def test_outlier():
    r=root('kmeans-outlier-leverage-motion')
    seq=[a.get('values') for a in r.iter() if a.tag.endswith('animateTransform')]
    x,mu=[[float(v.split()[0]) for v in a.split(';')] for a in seq]
    for px,pm in zip(x,mu): assert math.isclose((pm-112)/48,(10+(px-112)/48)/6)
def test_scaling():
    # Static Euclidean segments use isotropic 40px per unit.
    lines=[e for e in root('kmeans-feature-scale-still').findall('s:line',N)]
    for line,expected in zip(lines,[5.3525,3.4525,6.29,11.89]):
        d=sum((float(line.get(a))-float(line.get(b)))**2 for a,b in [('x1','x2'),('y1','y2')])/40**2
        assert math.isclose(d,expected,abs_tol=1e-8)
    r=root('kmeans-feature-scale-motion')
    lines=r.findall('s:line',N)
    for l in lines:
        ys1,ys2=vals(l,'y1'),vals(l,'y2')
        dx=float(l.get('x1'))-float(l.get('x2'))
        bars=[e for e in r.findall('s:rect',N) if e.get('class')=='animated']
        bar=bars[lines.index(l)];widths=vals(bar,'width')
        for y1,y2,w in zip(ys1,ys2,widths):
            d=(dx**2+(y1-y2)**2)/55**2
            assert abs(w-d*17.75)<.015
    assert math.isclose(math.sqrt(1.2),1.0954451150103321)
def test_elbow():
    xs=[0,1,2,8,9,10]
    def cost(group):
        mu=sum(group)/len(group);return sum((x-mu)**2 for x in group)
    best=[]
    for k in range(1,5):
        best.append(min(sum(cost(xs[a:b]) for a,b in zip((0,)+cuts,cuts+(6,))) for cuts in itertools.combinations(range(1,6),k-1)))
    assert best==[100,4,2.5,1]
    r=root('kmeans-elbow-inertia-motion')
    marker=next(e for e in r.findall('.//s:circle',N) if e.findall('s:animate',N))
    for actual,sse in zip(vals(marker,'cy'),[100,100,4,2.5,1,100]): assert abs(actual-(324-95*math.log10(sse)))<.06
if __name__=='__main__':
    test_d2();test_outlier();test_scaling();test_elbow()
    print('k-means D² probabilities, centroid motion, equal-scale distances and optimal inertia passed')
