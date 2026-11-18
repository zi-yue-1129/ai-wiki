#!/usr/bin/env python3
"""Regression checks for the Mondrian and RAPS toy visualizations."""
from math import ceil, isclose

def q(scores, alpha):
    k = ceil((len(scores)+1)*(1-alpha))
    return sorted(scores)[k-1] if k <= len(scores) else float("inf")

def main():
    a = [0.10,0.20,0.30,0.40,0.50,0.60]
    b = [0.15,0.25,0.35,0.55,0.65,0.85]
    assert isclose(q(a,.25),.60) and isclose(q(b,.25),.85)
    assert isclose(q(a+b,.25),.60) and q(a,.25)<.72<=q(b,.25)
    p = [.45,.30,.15,.10]
    aps = [sum(p[:r]) for r in range(1,5)]
    raps = [s+.10*max(0,r-2) for r,s in enumerate(aps,1)]
    assert all(isclose(x,y) for x,y in zip(aps,[.45,.75,.90,1.]))
    assert all(isclose(x,y) for x,y in zip(raps,[.45,.75,1.,1.20]))
    assert [i for i,s in enumerate(aps) if s<=.95]==[0,1,2]
    assert [i for i,s in enumerate(raps) if s<=.95]==[0,1]
    print("Mondrian/RAPS toy calculations: PASS")

if __name__ == "__main__":
    main()
