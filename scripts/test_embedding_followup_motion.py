from pathlib import Path
from fractions import Fraction
from xml.etree import ElementTree as ET
import unittest
A=Path(__file__).resolve().parents[1]/'docs/assets/concept-animations'
if not A.is_dir(): A=Path(__file__).resolve().parent
NS='{http://www.w3.org/2000/svg}'

def node(stem, ident):
    root=ET.parse(A/(stem+'-motion.svg')).getroot()
    return next(x for x in root.iter() if x.get('id')==ident)

class EmbeddingFollowup(unittest.TestCase):
    def test_counts(self):
        a=node('glove-window-accumulation','total').find(NS+'animate')
        self.assertEqual(a.get('calcMode'),'discrete')
        self.assertEqual([Fraction(v)/540 for v in a.get('values').split(';')],[0,Fraction(1,2),Fraction(1,2)+Fraction(1,3),0])
        self.assertEqual(a.get('keyTimes'),'0;0.25;0.625;1')
    def test_threshold(self):
        for ident,distances in [('tar',[.1,.3,.5,.7]),('far',[.4,.6,.8,.9])]:
            a=node('facenet-verification-sweep',ident).find(NS+'animate')
            self.assertEqual(a.get('calcMode'),'discrete')
            self.assertEqual([int(v) for v in a.get('values').split(';')],[0,110,220,330,440,0])
            for t,d in zip(a.get('keyTimes').split(';')[1:-1],distances): self.assertAlmostEqual(float(t)*12/10,d)
        self.assertEqual(sum(d<=.65 for d in [.1,.3,.5,.7]),3)
        self.assertEqual(sum(d<=.65 for d in [.4,.6,.8,.9]),2)
    def test_assets(self):
        for stem in ['glove-window-accumulation','facenet-verification-sweep']:
            for kind in ['motion','still']:
                f=A/(stem+'-'+kind+'.svg'); root=ET.parse(f).getroot()
                self.assertEqual(root.get('viewBox'),'0 0 640 360')
                self.assertTrue(root.find(NS+'title').text and root.find(NS+'desc').text)
                self.assertLess(f.stat().st_size,500000)
                for x in root.iter():
                    self.assertNotIn(x.tag,[NS+'script',NS+'foreignObject',NS+'image'])
                    self.assertFalse(any(k.startswith('on') or k.endswith('href') for k in x.attrib))
                nodes=list(root.iter(NS+'animate')); self.assertEqual(bool(nodes),kind=='motion')
                for a in nodes:
                    self.assertEqual(a.get('dur'),'12s'); self.assertEqual(a.get('repeatCount'),'indefinite')
                    values=a.get('values').split(';'); self.assertEqual(values[0],values[-1])
                    times=list(map(float,a.get('keyTimes').split(';')))
                    self.assertEqual(len(times),len(values)); self.assertEqual((times[0],times[-1]),(0,1)); self.assertTrue(all(x<y for x,y in zip(times,times[1:])))

if __name__=='__main__': unittest.main()
