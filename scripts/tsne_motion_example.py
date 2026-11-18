"""Reproducible six-point t-SNE teaching example (not paper measurements)."""
import math
X=((0,0,0),(1.7,.2,0),(.2,1.7,.1),(4,4,4),(5.7,4.1,4),(4.1,5.7,4.2))
Y0=((-0.4,.2),(.5,-.3),(.4,.3),(-.5,-.4),(.1,.5),(0,-.4))
RATE=3
STEPS=120
def affinities():
    a=[[0 if i==j else math.exp(-sum((u-v)**2 for u,v in zip(x,z))/2) for j,z in enumerate(X)] for i,x in enumerate(X)]
    rows=[[v/sum(row) for v in row] for row in a]
    return [[(rows[i][j]+rows[j][i])/12 for j in range(6)] for i in range(6)]
def kernel(y):
    n=[[0 if i==j else 1/(1+sum((u-v)**2 for u,v in zip(x,z))) for j,z in enumerate(y)] for i,x in enumerate(y)]
    total=sum(map(sum,n));return n,[[v/total for v in row] for row in n]
def loss(p,y):
    _,q=kernel(y)
    return sum(p[i][j]*math.log(p[i][j]/q[i][j]) for i in range(6) for j in range(6) if i!=j)
def gradient(p,y):
    n,q=kernel(y)
    return [[4*sum((p[i][j]-q[i][j])*n[i][j]*(y[i][d]-y[j][d]) for j in range(6)) for d in range(2)] for i in range(6)]
def trajectory():
    p=affinities();mean=[sum(x[d] for x in Y0)/6 for d in range(2)]
    y=[[x[d]-mean[d] for d in range(2)] for x in Y0];frames=[y]
    for _ in range(STEPS):
        g=gradient(p,y);y=[[y[i][d]-RATE*g[i][d] for d in range(2)] for i in range(6)];frames.append(y)
    return p,frames
def samples():
    p,frames=trajectory();result=[]
    for k in range(STEPS*5+1):
        i=min(k//5,STEPS-1);a=k/5-i
        y=[[frames[i][j][d]*(1-a)+frames[i+1][j][d]*a for d in range(2)] for j in range(6)]
        result.append((y,loss(p,y)))
    return result
