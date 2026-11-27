import unittest
from fractions import Fraction as F
from pathlib import Path
import xml.etree.ElementTree as ET

ASSETS = Path(__file__).resolve().parents[1] / 'docs/assets/concept-animations'
NS = '{http://www.w3.org/2000/svg}'

class SlimmingRewindSemantics(unittest.TestCase):
    def test_scale_shrink(self):
        gamma = list(map(F, ['0.9','-0.6','0.3','-0.2']))
        for _ in range(2):
            gamma = [g - F(1,10)*(int(g>0)-int(g<0)) for g in gamma]
        self.assertEqual(gamma, list(map(F,['0.7','-0.4','0.1','0'])))
        self.assertEqual([i for i,g in enumerate(gamma) if abs(g)>=F(3,20)], [0,1])
        root = ET.parse(ASSETS / 'network-slimming-scale-shrink-still.svg').getroot()
        self.assertEqual([int(e.get('width')) for e in root.iter(NS+'rect') if e.get('fill')=='#35678f'], [140,80,20,0])
    def test_early_checkpoint(self):
        initial,early,trained = [list(map(F,row)) for row in [['0.2','-0.4','0.6','-0.1'],['0.5','-0.2','0.4','0.3'],['0.9','0.05','-0.8','-0.04']]]
        drop = sorted(range(4),key=lambda i:abs(trained[i]))[:2]
        self.assertEqual(set(drop),{1,3})
        mask = [int(i not in drop) for i in range(4)]
        reset = lambda row: [m*w for m,w in zip(mask,row)]
        self.assertEqual(reset(early),list(map(F,['0.5','0','0.4','0'])))
        self.assertNotEqual(reset(early),reset(initial))
        self.assertNotEqual(reset(early),reset(trained))
        root = ET.parse(ASSETS / 'lottery-early-checkpoint-rewind-still.svg').getroot()
        self.assertEqual([e.text for e in root.iter(NS+'text') if e.get('y')=='292'],['0.5','0','0.4','0'])

if __name__ == '__main__':
    unittest.main()
