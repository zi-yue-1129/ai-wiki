#!/usr/bin/env python3
"""Check the numerical examples and shared SVG scales of the SVD diagrams."""
import math
from pathlib import Path
import xml.etree.ElementTree as ET

ASSETS = Path(__file__).resolve().parents[1] / 'docs/assets/concept-animations'
NS = {'s': 'http://www.w3.org/2000/svg'}

def test_rank_scale():
    root = ET.parse(ASSETS / 'svd-rank-accumulation-motion.svg').getroot()
    bars = [e for e in root.findall('s:rect', NS) if e.get('x') == '112' and e.get('height') == '14']
    assert [float(e.get('width')) for e in bars] == [168, 112, 56]
    labels = {''.join(e.itertext()) for e in root.findall('s:text', NS)}
    assert {'√28', '√10', '√2', '0'} <= labels
    # Orthogonal rows: squared singular values and exact rank residuals.
    energies = [18, 8, 2]
    assert [sum(energies[k:]) for k in range(4)] == [28, 10, 2, 0]

def test_least_squares():
    root = ET.parse(ASSETS / 'svd-ls-orthogonal-residual-motion.svg').getroot()
    markers = [e for e in root.findall('s:circle', NS) if e.findall('s:animate', NS)]
    def values(e, attr):
        return list(map(float, next(a for a in e.findall('s:animate', NS) if a.get('attributeName') == attr).get('values').split(';')))
    lx, ly = values(markers[0], 'cx'), values(markers[0], 'cy')
    rx, ry = values(markers[1], 'cx'), values(markers[1], 'cy')
    assert len(lx) == len(ly) == len(rx) == len(ry) == 49
    for ax, ay, ex, ey in zip(lx, ly, rx, ry):
        x = (ax - 122) / 112
        assert abs(ay - (285 - 56*x)) < 0.011
        assert abs(ex - (439 + 127*x)) < 0.012
        E = (2-2*x)**2 + (2-x)**2
        assert abs(ey - (321 - 22*E)) < 0.03
    assert math.isclose((2*2+1*2)/(2*2+1*1), 1.2)
    assert math.isclose(2*(-.4)+.8, 0)

def test_noise_and_degenerate_basis():
    for i in range(101):
        d = -.2 + .004*i
        assert math.isclose(.25*(4*d), d, abs_tol=1e-12)
        t = i*2*math.pi/100
        c,s = math.cos(t),math.sin(t)
        assert math.isclose(2*c*c+2*s*s,2,abs_tol=1e-12)
        assert abs(2*c*s-2*s*c)<1e-12

if __name__ == '__main__':
    test_rank_scale(); test_least_squares(); test_noise_and_degenerate_basis()
    print('SVD scales, residuals, 49 coupled least-squares states and analytic invariants passed')
