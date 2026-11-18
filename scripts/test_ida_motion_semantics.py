"""Independently derive IDA* trace and verify actual SVG/JavaScript timelines."""
from pathlib import Path
import bisect
import json
import math
import subprocess
import unittest
import xml.etree.ElementTree as E

ROOT = Path(__file__).resolve().parents[1]
NS = "{http://www.w3.org/2000/svg}"
F = dict(S=4,A=6,B=8,C=7,D=10,E=9,G=8)
CHILDREN = dict(S=["A","B"],A=["C","D"],B=["E"],C=["G"],D=[],E=[],G=[])
POS = dict(S=(198,87),A=(100,157),B=(300,157),C=(71,228),D=(182,228),E=(329,228),G=(71,298))


def trace():
    output=[];seen=set();examined=revisits=0;bound=4;iteration=0
    while True:
        minimum=math.inf;found=False
        output.append(dict(kind="start",iteration=iteration,bound=bound,node=None,path=[],examined=examined,revisits=revisits,smallestCutoff=None))
        def visit(n,path):
            nonlocal minimum,found,examined,revisits
            if found:return
            examined+=1;revisits+=int(n in seen);seen.add(n)
            kind="cutoff" if F[n]>bound else "goal" if n=="G" else "expand"
            if kind=="cutoff":minimum=min(minimum,F[n])
            if kind=="goal":found=True
            output.append(dict(kind=kind,iteration=iteration,bound=bound,node=n,path=path+[n],examined=examined,revisits=revisits,smallestCutoff=None if math.isinf(minimum) else minimum))
            if kind=="expand":
                for c in CHILDREN[n]:visit(c,path+[n])
        visit("S",[])
        if found:return output
        output.append(dict(kind="nextBound",iteration=iteration,bound=bound,node=None,path=[],examined=examined,revisits=revisits,smallestCutoff=minimum))
        bound=minimum;iteration+=1


def value(a,t):
    times=list(map(float,a.get("keyTimes").split(";")))
    vals=list(map(float,a.get("values").split(";")))
    i=min(bisect.bisect_right(times,t)-1,len(times)-2)
    if a.get("calcMode")=="discrete":return vals[i]
    u=(t-times[i])/(times[i+1]-times[i])
    return vals[i]*(1-u)+vals[i+1]*u


class IdaSemantics(unittest.TestCase):
    def test_browser_model_matches_independent_recursive_search(self):
        path=ROOT/"docs/javascripts/symbolic-proof-labs.js"
        harness="""const fs=require('fs'),vm=require('vm');
let s=fs.readFileSync(process.argv[1],'utf8');
s=s.slice(0,s.indexOf('  const original ='))+'globalThis.result=idaSteps;})();';
const c={window:{matchMedia:()=>({matches:false})}};vm.createContext(c);vm.runInContext(s,c);
console.log(JSON.stringify(c.result));"""
        actual=json.loads(subprocess.check_output(["node","-e",harness,str(path)],text=True))
        self.assertEqual(actual,trace())
        self.assertEqual(actual[-1]["path"],["S","A","C","G"])
        self.assertEqual([s["bound"] for s in actual if s["kind"]=="start"],[4,6,7,8])

    def test_svg_labels_and_cursor_are_causally_synchronised(self):
        r=E.parse(ROOT/"docs/assets/concept-animations/ida-bound-reexpansion-motion.svg").getroot()
        groups=[g for g in r.iter(NS+"g") if g.get("data-kind")]
        circle=next(c for c in r.iter(NS+"circle") if c.get("class")=="motion")
        ax,ay=circle.findall(NS+"animate")
        visits=[s for s in trace() if s["node"]]
        dt=.9/len(visits)
        edges=[(POS[n],POS[c]) for n in CHILDREN for c in CHILDREN[n]]
        for j in range(10001):
            t=j/10001
            active=[g for g in groups if value(g.find(NS+"animate"),t)==1]
            self.assertEqual(len(active),1)
            g=active[0];i=min(int(t/dt),len(visits)-1);s=visits[i]
            moving=i<len(visits)-1 and t-i*dt>=dt/2
            self.assertEqual(g.get("data-kind"),"MOVE" if moving else s["kind"].upper())
            self.assertEqual(int(g.get("data-bound")),s["bound"])
            texts=[e.text for e in g.findall(NS+"text")]
            self.assertEqual(texts[0],str(s["bound"]))
            self.assertEqual(texts[2],"TRAVERSE" if moving else s["kind"].upper())
            x,y=value(ax,t),value(ay,t)
            if not moving:
                self.assertAlmostEqual(x,POS[s["node"]][0],delta=.0001)
                self.assertAlmostEqual(y,POS[s["node"]][1],delta=.0001)
            else:
                def distance(a,b):
                    vx,vy=b[0]-a[0],b[1]-a[1]
                    u=max(0,min(1,((x-a[0])*vx+(y-a[1])*vy)/(vx*vx+vy*vy)))
                    return math.hypot(x-a[0]-u*vx,y-a[1]-u*vy)
                self.assertLess(min(distance(a,b) for a,b in edges),.0001)
            if texts[2]=="GOAL":
                self.assertEqual(s["node"],"G");self.assertEqual(s["bound"],8)
        # No result is exposed before the last DFS visit.
        goal=next(p for p in r.iter(NS+"path") if p.get("class")=="motion")
        self.assertEqual(value(goal.find(NS+"animate"),.84),0)
        self.assertEqual(value(goal.find(NS+"animate"),.86),1)


if __name__=="__main__":
    unittest.main()
