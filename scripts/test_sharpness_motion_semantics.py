"""Recompute coordinates and curvatures from the shipped sharpness SVG tracks."""
import re
import unittest
import xml.etree.ElementTree as E
from pathlib import Path

NS='{http://www.w3.org/2000/svg}'
ASSETS=Path(__file__).resolve().parents[1]/'docs/assets/concept-animations'
def root(stem,kind='motion'):
    return E.parse(ASSETS/f'sharpness-{stem}-{kind}.svg').getroot()
def values(el):
    return list(map(float,el.get('values').split(';')))

class SharpnessMotion(unittest.TestCase):
    def test_common_radius(self):
        r=root('radius-loss')
        circles=[e for e in r.iter(NS+'circle') if e.get('r')=='5.5']
        bars=[values(a) for a in r.iter(NS+'animate') if a.get('attributeName')=='width']
        self.assertEqual(len(circles),2)
        for e,k,x0,bar in zip(circles,(.5,2),(165,475),bars):
            ts={a.get('attributeName'):values(a) for a in e}
            for x,y,w in zip(ts['cx'],ts['cy'],bar):
                rho=(x-x0)/110
                loss=k*rho*rho/2
                self.assertAlmostEqual(y,235-115*loss,delta=.002)
                self.assertAlmostEqual(w,205*loss,delta=.002)
        for a,b in zip(*bars):self.assertAlmostEqual(b,4*a,delta=.003)

    def test_coordinate_curvature(self):
        r=root('reparam-curvature')
        curves=next(a for a in r.iter(NS+'animate') if a.get('attributeName')=='d').get('values').split(';')
        widths=values(next(a for a in r.iter(NS+'animate') if a.get('attributeName')=='width'))
        ys=values(next(a for a in r.iter(NS+'animate') if a.get('attributeName')=='cy'))
        self.assertEqual(len(curves),len(widths))
        for curve,w,y in zip(curves,widths,ys):
            a2=w/62
            self.assertAlmostEqual(y,235-120*a2*.5**2,delta=.002)
            points=list(map(float,re.findall(r'-?\d+(?:\.\d+)?',curve)))
            for x,cy in zip(points[::2],points[1::2]):
                u=(x-475)/(118/.72)
                self.assertAlmostEqual(cy,235-120*a2*u*u,delta=.003)
        for stem in ('radius-loss','reparam-curvature'):
            self.assertEqual(len(list(root(stem,'still').iter(NS+'animate'))),0)

if __name__=='__main__':unittest.main()
