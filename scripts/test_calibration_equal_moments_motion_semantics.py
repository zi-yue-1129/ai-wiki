import unittest
from fractions import Fraction as F
from pathlib import Path
import xml.etree.ElementTree as ET
ASSETS=Path(__file__).resolve().parents[1]/'docs/assets/concept-animations'
NS={'s':'http://www.w3.org/2000/svg'}
P=[F(0),F(0),F(1,2),F(1,2),F(1),F(1),F(0)]
TIMES='0;0.12;0.43;0.58;0.85;0.95;1'
class MixtureMotionTests(unittest.TestCase):
    def tracks(self,stem,ident,attr,expected):
        root=ET.parse(ASSETS/f'{stem}-motion.svg').getroot()
        a=root.find(f'.//*[@id="{ident}"]/s:animate[@attributeName="{attr}"]',NS)
        self.assertIsNotNone(a)
        self.assertEqual(a.get('keyTimes'),TIMES)
        self.assertEqual(a.get('dur'),'12s')
        self.assertEqual(a.get('repeatCount'),'indefinite')
        self.assertEqual([float(v) for v in a.get('values').split(';')],[float(v) for v in expected])
        still=ET.parse(ASSETS/f'{stem}-still.svg').getroot().find(f'.//*[@id="{ident}"]')
        self.assertEqual(float(still.get(attr)),float(expected[4]))
    def test_calibration(self):
        w=[F(11,10),F(17,20)]
        ds=[[a-round(a/s)*s for a in w] for s in [F(1),F(3,5)]]
        self.assertEqual([sum(d*d for d in row) for row in ds],[F(13,400),F(29,400)])
        self.assertEqual([[sum(d*x for d,x in zip(row,v))**2 for v in [(5,2),(3,2)]] for row in ds],[[F(1,25),0],[0,F(1,25)]])
        stem='ptq-calibration-scale-choice'
        self.tracks(stem,'mse-one','width',[145*p for p in P])
        self.tracks(stem,'mse-local','width',[145*(1-p) for p in P])
        for ident,sign in [('curve-one',-1),('curve-local',1)]:
            self.tracks(stem,ident,'cx',[355+252*p for p in P])
            self.tracks(stem,ident,'cy',[(267 if sign==-1 else 87)+sign*180*p for p in P])
        for attr in ['x1','x2']:self.tracks(stem,'mix-cursor',attr,[355+252*p for p in P])
    def test_equal_moments(self):
        stem='data-free-equal-moments'
        for p in [F(i,16) for i in range(17)]:
            q=[p/8,(1-p)/2,3*p/4,(1-p)/2,p/8]
            self.assertEqual(sum(q),1)
            self.assertEqual(sum(i*v for i,v in enumerate(q)),2)
            self.assertEqual(sum((i-2)**2*v for i,v in enumerate(q)),1)
            self.assertEqual(sum((i-2)**4*v for i,v in enumerate(q)),1+3*p)
        for i in range(5):
            h=[208*[p/8,(1-p)/2,3*p/4,(1-p)/2,p/8][i] for p in P]
            self.tracks(stem,f'mass-{i}','height',h)
            self.tracks(stem,f'mass-{i}','y',[252-v for v in h])
        self.tracks(stem,'fourth-moment','width',[51*(1+3*p) for p in P])
    def test_assets(self):
        for stem in ['ptq-calibration-scale-choice','data-free-equal-moments']:
            for mode in ['motion','still']:
                f=ASSETS/f'{stem}-{mode}.svg';self.assertLess(f.stat().st_size,50000)
                root=ET.parse(f).getroot();self.assertEqual(root.get('viewBox'),'0 0 640 360')
                self.assertIsNotNone(root.find('s:title',NS));self.assertIsNotNone(root.find('s:desc',NS))
                self.assertEqual(bool(root.findall('.//s:animate',NS)),mode=='motion')
                for e in root.iter():
                    self.assertNotIn(e.tag.split('}')[-1],{'script','foreignObject','image','iframe'})
                    self.assertFalse(any(k.startswith('on') or k.endswith('href') for k in e.attrib))
if __name__=='__main__':unittest.main()
