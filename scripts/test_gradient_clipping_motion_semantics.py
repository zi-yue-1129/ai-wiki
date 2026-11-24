#!/usr/bin/env python3
"""Numerical regression for four synthetic gradient-clipping teaching examples."""
import math

def norm(x): return math.sqrt(sum(t*t for t in x))
def clip(x,cap):
    z=norm(x)
    a=min(1.0,cap/z) if z else 1.0
    return tuple(a*t for t in x)
def same(x,y): return len(x)==len(y) and all(math.isclose(a,b,abs_tol=1e-10,rel_tol=1e-10) for a,b in zip(x,y))
def validate():
    e=[]
    def check(label,x,y):
        if not same(x,y): e.append(f"{label}: {x} != {y}")
    # Global norm/coordinate clipping: direction is retained only in the first.
    g=(4.,2.)
    check("norm clipping",clip(g,2),(4/math.sqrt(5),2/math.sqrt(5)))
    check("coordinate clipping",tuple(min(1.5,max(-1.5,x)) for x in g),(1.5,1.5))
    for z in (0.35,0.5,0.75,1):
        v=tuple(z*x for x in g); out=clip(v,2)
        if norm(out)>2+1e-10 or not math.isclose(out[0]*v[1],out[1]*v[0],abs_tol=1e-10):
            e.append(f"direction/budget at s={z}")
    # Per-microbatch clipping and averaging are non-commutative.
    a,b=(4.,0.),(0.,2.)
    first=tuple((x+y)/2 for x,y in zip(clip(a,2),clip(b,2)))
    second=clip(tuple((x+y)/2 for x,y in zip(a,b)),2)
    check("clip then mean",first,(1.,1.))
    check("mean then clip",second,(4/math.sqrt(5),2/math.sqrt(5)))
    if same(first,second): e.append("unexpected commutativity")
    # Shared global budget induces cross-layer coupling.
    for z in (0,0.25,0.5,0.75,1):
        grp=(4.,3*z)
        if norm(clip(grp,4))>4+1e-10: e.append(f"global norm at s={z}")
        check(f"per-layer budget at s={z}",tuple(min(t,4) for t in grp),grp)
    check("global endpoint",clip((4.,3.),4),(3.2,2.4))
    check("per-layer endpoint",(4.,3.),(4.,3.))
    # AMP loss scaling: unscale first, THEN apply norm clipping.
    v=(3.,4.); S=4.; scaled=tuple(S*t for t in v)
    good=clip(tuple(t/S for t in scaled),2)
    bad=tuple(t/S for t in clip(scaled,2))
    check("AMP correct",good,(1.2,1.6))
    check("AMP incorrect",bad,(0.3,0.4))
    if not math.isclose(norm(good),2,abs_tol=1e-10) or not math.isclose(norm(bad),0.5,abs_tol=1e-10):
        e.append("AMP norm mismatch")

    # Unit-wise adaptive clipping with weight-norm-relative budgets.
    for s in (0.4, 0.75, 1.0, 2.0, 3.0):
        for w in (1.0, 4.0):
            cap = 0.5 * w
            out = min(s, cap)
            if out > cap + 1e-10 or not math.isclose(out, norm(clip((s, 0.0), cap)), rel_tol=1e-10):
                e.append(f"AGC relative cap at gradient {s}, weight {w}")
    check("AGC small-weight endpoint", clip((3.,0.),0.5), (0.5,0.))
    check("AGC large-weight endpoint", clip((3.,0.),2.), (2.,0.))
    # Decoupled weight decay is outside the loss-gradient norm clipping budget.
    grad=clip((4.,0.),2.)
    grad_step=tuple(-0.2*x for x in grad)
    decay_step=tuple(-0.2*0.5*x for x in (3.,4.))
    total_step=tuple(a+b for a,b in zip(grad_step,decay_step))
    check("decoupled gradient displacement",grad_step,(-0.4,0.))
    check("decoupled decay displacement",decay_step,(-0.3,-0.4))
    check("total displacement",total_step,(-0.7,-0.4))
    if not math.isclose(norm(total_step),math.sqrt(0.65),rel_tol=1e-10) or norm(total_step)<=0.4:
        e.append("decoupled decay must exceed pure gradient step in this toy case")
    return e

if __name__=="__main__":
    errors=validate()
    for error in errors: print("ERROR",error)
    print(f"Gradient-clipping examples: {len(errors)} error(s)")
    raise SystemExit(bool(errors))
