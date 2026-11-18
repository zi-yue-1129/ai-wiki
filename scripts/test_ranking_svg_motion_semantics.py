import xml.etree.ElementTree as E, math, pathlib, re, subprocess, copy

B=pathlib.Path(__file__).resolve().parents[1]/'docs/assets/concept-animations'
names=['roc-pairwise-auc','pr-ap-rectangles','roc-partial-area','pr-ap-trapezoid-gap','roc-rank-transform','auc-ap-ranking-contrast']; ns='{http://www.w3.org/2000/svg}'
def parse(n):return E.parse(B/(n+'-motion.svg')).getroot()
def val(a,t):
 k=list(map(float,a.get('keyTimes').split(';')));v=[list(map(float,re.split('[, ]+',s))) for s in a.get('values').split(';')];i=max(j for j in range(len(k)-1) if k[j]<=t); u=0 if a.get('calcMode')=='discrete' else (t-k[i])/(k[i+1]-k[i]);return [x+(y-x)*u for x,y in zip(v[i],v[i+1])]
# Dense scan actual animated attributes, not author helper formula.
r=parse('roc-rank-transform'); aa=list(r.iter(ns+'animate')); scores=[.9,.8,.6,.3]
for i in range(10001):
 t=i/10001; xs=[val(a,t)[0] for a in aa];u=2*t if t<=.5 else 2*(1-t)
 assert all(abs(x-(170+244*((1-u)*math.sqrt(s)+u*s**3)))<.006 for x,s in zip(xs,scores));assert xs[0]>xs[1]>xs[2]>xs[3]
r=parse('roc-partial-area');aa=list(r.iter(ns+'animate'))
for i in range(10001):
 t=i/10001; w,x1,x2,bar=[val(a,t)[0] for a in aa]; c=w/300; assert abs(x1-130-w)<1e-9 and x1==x2; area=c-.125;assert abs(bar/130*.875-area)<.000011
# Actual rectangle dimensions normalized by plot size for every discrete state.
r=parse('pr-ap-rectangles');groups=[g for g in r.iter(ns+'g') if g.find(ns+'animate') is not None]
for g,expected in zip(groups,[0,.5,.5,5/6,5/6]):
 rects=[x for x in g.findall(ns+'rect') if float(x.get('x'))>=350];area=sum(float(x.get('width'))*float(x.get('height'))/(210*120) for x in rects);assert abs(area-expected)<1e-9
r=parse('roc-pairwise-auc');groups=[g for g in r.iter(ns+'g') if g.find(ns+'animate') is not None]
for g,wins in zip(groups,[0,1,2,2,3]):
 bars=[x for x in g.findall(ns+'rect') if x.get('fill')=='#258f93']; assert abs(sum(float(x.get('width')) for x in bars)/260-wins/4)<1e-10
# Polygon shoelace, independently reconstructed from literal SVG path coordinates.
r=parse('pr-ap-trapezoid-gap');p=next(p for p in r.iter(ns+'path') if p.get('fill')=='#f2b881');assert p.get('d')=='M367 270V134H469V202L571 179.33333333333334V270Z'
pts=[(367,270),(367,134),(469,134),(469,202),(571,179.33333333333334),(571,270)];area=abs(sum(x*yy-xx*y for (x,y),(xx,yy) in zip(pts,pts[1:]+pts[:1])))/2/(204*136);assert abs(area-19/24)<1e-12

# Verify actual contrast scan marker reaches each row as contributions begin.
r=parse('auc-ap-ranking-contrast');a=next(r.iter(ns+'animateTransform'))
for t,y in zip([.2,.4,.6,.8],[152,190,228,266]):
 assert abs(133+val(a,t)[1]-y)<1e-8, f'scan sync t={t}'
for g in r.iter(ns+'g'):
 a=g.find(ns+'animate')
 if a is None:continue
 rect=g.find(ns+'rect');text=g.find(ns+'text');area=float(text.text[1:]);assert abs(float(rect.get('width'))/180-area)<.00034
 row=(float(rect.get('y'))-145)/38+1;assert abs(float(a.get('keyTimes').split(';')[1])-.2*row)<1e-9
for suffix in ['motion','still']:
 r=E.parse(B/f'pr-ap-trapezoid-gap-{suffix}.svg').getroot();p=next(p for p in r.iter(ns+'path') if p.get('stroke')=='#b86d3b');assert p.get('d').endswith('V202'), 'final negative threshold vertex missing'
print('Ranking SVG actual geometry and 10,001-time-point regression checks PASS')
