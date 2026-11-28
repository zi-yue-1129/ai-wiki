"""Check the exact toy distributions, skipped-output errors and animation tracks."""
from fractions import Fraction as F
from pathlib import Path
from xml.etree import ElementTree as ET
import unittest

ASSETS = Path(__file__).resolve().parents[1] / 'docs/assets/concept-animations'
if not ASSETS.is_dir():
    ASSETS = Path(__file__).resolve().parent
NS = {'s': 'http://www.w3.org/2000/svg'}


class CouplingValueMotionTests(unittest.TestCase):
    def root(self, stem, mode='motion'):
        return ET.parse(ASSETS / f'{stem}-{mode}.svg').getroot()

    def test_coupling(self):
        joint = [[F(1,4), F(1,4), 0], [0, F(1,4), F(1,4)]]
        independent = [[F(1,8), F(1,4), F(1,8)]] * 2
        for k in range(17):
            t = F(k,16)
            p = [[(1-t)*a+t*b for a,b in zip(j,i)] for j,i in zip(joint,independent)]
            self.assertEqual(list(map(sum,p)), [F(1,2)]*2)
            self.assertEqual([sum(col) for col in zip(*p)], [F(1,4),F(1,2),F(1,4)])
            pmf = {s: sum(p[i][j] for i,a in enumerate((2,4)) for j,b in enumerate((1,3,5)) if a+b==s) for s in (3,5,7,9)}
            self.assertEqual(list(pmf.values()), [F(1,4)-t/8,F(1,4)+t/8,F(1,4)+t/8,F(1,4)-t/8])
            self.assertEqual(sum(s*v for s,v in pmf.items()),6)
            self.assertEqual(sum((s-6)**2*v for s,v in pmf.items()),5-2*t)
        tracks = self.root('deepar-coupling-totals').findall('.//s:animate',NS)
        self.assertEqual([a.get('values') for a in tracks if a.get('attributeName')=='height'], ['50;50;25;25;50','50;50;75;75;50','50;50;75;75;50','50;50;25;25;50'])
        self.assertEqual([a.get('values') for a in tracks if a.get('attributeName')=='width'], ['150;150;90;90;150'])

    def test_value_errors(self):
        for v in [F(k,9) for k in range(36,109)]:
            values = [0,4,8,v]
            mean = sum(values)/4
            errors = [abs(sum(w*x for w,x in zip(row,values))/sum(row)-mean) for row in ([1,1,1,9],[2,1,1,1])]
            self.assertEqual(errors,[v/2-2,(12+v)/20])
            self.assertEqual(errors[0]>errors[1],v>F(52,9))
        tracks = self.root('informer-value-error').findall('.//s:animate',NS)
        self.assertEqual([a.get('values') for a in tracks if a.get('attributeName')=='cy'], ['158;158;286;286;158','247.6;247.6;260.4;260.4;247.6'])

    def test_assets(self):
        for stem in ('deepar-coupling-totals','informer-value-error'):
            for mode in ('motion','still'):
                root=self.root(stem,mode)
                self.assertEqual(root.get('viewBox'),'0 0 640 360')
                self.assertIsNotNone(root.find('s:title',NS))
                self.assertIsNotNone(root.find('s:desc',NS))
                tracks=root.findall('.//s:animate',NS)
                self.assertEqual(bool(tracks),mode=='motion')
                for a in tracks:
                    self.assertEqual(a.get('dur'),'12s')
                    self.assertEqual(a.get('repeatCount'),'indefinite')
                    self.assertEqual(a.get('keyTimes'),'0;0.15;0.55;0.75;1')
                    self.assertEqual(len(a.get('values').split(';')),5)
                for e in root.iter():
                    self.assertNotIn(e.tag.split('}')[-1],{'script','foreignObject','image','iframe'})
                    self.assertFalse(any(k.startswith('on') or k.endswith('href') for k in e.attrib))


if __name__=='__main__':
    unittest.main()
