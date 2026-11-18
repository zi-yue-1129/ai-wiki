"""Test actual AdaGrad plotted gains and proportional accumulator bars."""
import math
from pathlib import Path
import unittest
import xml.etree.ElementTree as E
N='{http://www.w3.org/2000/svg}'
A=Path(__file__).resolve().parents[1]/'docs/assets/concept-animations'
class AdaptiveGeometry(unittest.TestCase):
    def test_adagrad_source_geometry(self):
        for kind in ('motion','still'):
            r=E.parse(A/f'adagrad-coordinate-gain-{kind}.svg').getroot()
            for points,Gs,base,color,linebase in zip(r.iter(N+'polyline'),(range(1,7),[1,1,1,1,2,2]),(199,385),('#487ac4','#0b858a'),(234,420)):
                coords=[list(map(float,p.split(','))) for p in points.get('points').split()]
                self.assertEqual(len(coords),6)
                bars=[e for e in r.iter(N+'rect') if e.get('width')=='26' and e.get('fill')==color]
                self.assertEqual(len(bars),6)
                for i,((x,y),g,b) in enumerate(zip(coords,Gs,bars)):
                    self.assertAlmostEqual(x,178+91*i)
                    self.assertAlmostEqual(y,linebase-19/math.sqrt(g),delta=.06)
                    self.assertAlmostEqual(float(b.get('height')),44*g/6,delta=.001)
                    self.assertAlmostEqual(float(b.get('y'))+float(b.get('height')),base,delta=.001)
    def test_static_fallbacks(self):
        for stem in ('adagrad-coordinate-gain','adafactor-factored-moments'):
            r=E.parse(A/f'{stem}-still.svg').getroot()
            self.assertEqual(len(list(r.iter(N+'animate'))),0)
if __name__=='__main__':unittest.main()
