#!/usr/bin/env python3
"""Exercise the actual shared JS arithmetic without a browser or installed model."""
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[1]
subprocess.run(['node', '-e', r'''
const assert=require('node:assert/strict');
const M=require('./docs/javascripts/policy-credit-math.js');
const near=(a,b)=>assert(Math.abs(a-b)<1e-10,`${a} != ${b}`);
const vec=(a,b)=>a.forEach((v,i)=>near(v,b[i]));
vec(M.returns([1,0,2],.9),[2.62,1.8,2]);
vec(M.returns([0,0,4],.8),[2.56,3.2,4]);
vec(M.returns([1,2,3],0),[1,2,3]);
vec(M.returns([1,2,3],1),[6,5,3]);
vec(M.returns([0,0,0],.5),[0,0,0]);
for(const r of [[1,3,0,2],[1,2,4,5],[0,6,0,0],[0,0,0,6]]) {
  const g=M.group(r);near(g.advantages.reduce((a,b)=>a+b,0),0);
  near(g.advantages.reduce((a,b)=>a+b*b,0)/r.length,1);
}
const equal=M.group([3,3,3,3]);assert.equal(equal.defined,false);assert.equal(equal.sigma,0);vec(equal.advantages,[0,0,0,0]);
// Shared per-frame scale: no saturation, exactly proportional lengths.
for(const values of [[4.75,5,0],[-4,0,5],[15,10,5],[1,6,4,5]]) {
  const s=M.scale(values);for(const v of values)assert(Math.abs(v)*s<=104+1e-10);
  if(values[0]>0&&values[1]>0)near(values[0]*s/(values[1]*s),values[0]/values[1]);
}
console.log('Policy credit numerical/geometry model: passed');
'''], cwd=root, check=True)

# Tie the retained instructional SVG endpoints to their two source examples.
import math
import xml.etree.ElementTree as ET
assets = root / 'docs/assets/concept-animations'
ns = '{http://www.w3.org/2000/svg}'
for stem, labels in {
    'reinforce-reward-to-go': ['G0 = 2.62', 'G1 = 1.80', 'G2 = 2.00', 'A0  +0.72', 'A1  -0.10', 'A2  +0.10'],
    'reinforce-return-credit': ['G0 = 2.56', 'G1 = 3.2', 'G2 = 4.0', 'A0 = +0.56', 'A1 = +1.20', 'A2 = +2.00'],
    'grpo-group-advantages': ['r = 1', 'r = 2', 'r = 4', 'r = 5', 'mean = 3', 'σ = √2.5', '-1.26', '-0.63', '+0.63', '+1.26'],
}.items():
    for kind in ('motion', 'still'):
        svg = ET.parse(assets / f'{stem}-{kind}.svg').getroot()
        texts = [''.join(t.itertext()) for t in svg.iter(ns+'text')]
        assert all(label in texts for label in labels), (stem,kind,texts)
        animations = list(svg.iter(ns+'animate'))
        assert bool(animations) == (kind == 'motion'), (stem,kind)
        if stem == 'reinforce-return-credit':
            bars=[node for node in svg.iter(ns+'rect') if node.get('width')=='38']
            assert len(bars)==3
            for bar,value in zip(bars,[.56,1.2,2]):
                assert math.isclose(float(bar.get('height')),value*42,abs_tol=1e-10)
                assert math.isclose(float(bar.get('y'))+float(bar.get('height')),340,abs_tol=1e-10)
            if kind == 'motion':
                for bar in bars:
                    for animation in bar:
                        assert animation.get('keyTimes') == '0;0.62;0.80;0.91;1'
print('Policy credit SVG labels, endpoints and stage timing: passed')


# Positive labels must clear the tallest actual bar at every linear SMIL knot.
# A conservative 0.25em descent plus 2px gap keeps same-colour text off fill.
def check_grpo_positive_label_clearance(svg):
    for text in svg.iter(ns+'text'):
        if ''.join(text.itertext()) not in ('+0.63', '+1.26'):
            continue
        x = float(text.get('x'))
        bars = [bar for bar in svg.iter(ns+'rect')
                if bar.get('width') == '42'
                and math.isclose(float(bar.get('x')) + 21, x)]
        assert len(bars) == 1
        bar = bars[0]
        ys = [float(bar.get('y'))]
        for anim in bar.findall(ns+'animate'):
            if anim.get('attributeName') == 'y':
                assert anim.get('calcMode') == 'linear'
                ys.extend(map(float, anim.get('values').split(';')))
        # Linear interpolation cannot overshoot the endpoint extrema.
        bottom = float(text.get('y')) + .25 * float(text.get('font-size'))
        assert bottom + 2 <= min(ys), (text.text, bottom, min(ys))

for kind in ('motion', 'still'):
    svg = ET.parse(assets / f'grpo-group-advantages-{kind}.svg').getroot()
    check_grpo_positive_label_clearance(svg)
    # Real regression: restore the former y=278, which hid +1.26 in green fill.
    label = next(t for t in svg.iter(ns+'text') if t.text == '+1.26')
    label.set('y', '278')
    try:
        check_grpo_positive_label_clearance(svg)
    except AssertionError:
        pass
    else:
        raise AssertionError('The former same-colour label/bar overlap was accepted')
print('GRPO actual SVG label clearance and old-coordinate negative cases: passed')
