"""Exact finite-ranking metrics and synchronized discrete SVG operating points."""
import math
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import unittest
import xml.etree.ElementTree as E

ASSETS=Path(__file__).resolve().parents[1]/'docs/assets/concept-animations'
NS='{http://www.w3.org/2000/svg}'
LABELS=[1,0,1,0,0,1,0,0,0,0]
def ap(positions):
    return sum(F(j,k) for j,k in enumerate(positions,1))/len(positions)
def value(node,attr,frame):
    a=next((a for a in node if a.get('attributeName')==attr),None)
    return a.get('values').split(';')[frame] if a is not None and frame is not None else node.get(attr)
class RankingMotion(unittest.TestCase):
    def test_exact_metrics_and_finite_random_baselines(self):
        wins=sum(LABELS[i] and not LABELS[j] for i in range(10) for j in range(i+1,10))
        self.assertEqual(F(wins,21),F(17,21));self.assertEqual(ap([1,3,6]),F(13,18))
        for n,p,expected in [(4,2,F(49,72)),(10,3,F(14581,32400))]:
            vals=[ap(pos) for pos in combinations(range(1,n+1),p)]
            self.assertEqual(sum(vals)/len(vals),expected)
    def test_svg_operating_points_highlights_labels_and_revealed_paths(self):
        for topic in ('roc','pr'):
            coords=[]
            for k in range(11):
                tp=sum(LABELS[:k]);fp=k-tp
                x=fp/7 if topic=='roc' else tp/3
                y=tp/3 if topic=='roc' else tp/k if k else 1
                coords.append((356+221*x,269-141*y))
            for mode in ('motion','still'):
                root=E.parse(ASSETS/f'{topic}-threshold-sweep-{mode}.svg').getroot()
                circles=root.findall(NS+'circle');self.assertEqual(len(circles),1);dot=circles[0]
                lines=root.findall(NS+'polyline');self.assertEqual(len(lines),2)
                plotted=[tuple(map(float,p.split(','))) for p in lines[0].get('points').split()]
                for got,expected in zip(plotted,coords):
                    for a,b in zip(got,expected):self.assertAlmostEqual(a,b,delta=.006)
                highlights=[x for x in root.findall(NS+'rect') if x.get('fill')=='#dbedf1']
                labels=[x for x in root.findall(NS+'text') if x.get('y')=='329']
                self.assertEqual(len(highlights),10)
                if mode=='motion':
                    animations=root.findall('.//'+NS+'animate')
                    for a in animations:
                        self.assertEqual(a.get('calcMode'),'discrete');self.assertEqual(a.get('dur'),'11s')
                        self.assertEqual(len(a.get('values').split(';')),12)
                        for i,t in enumerate(map(float,a.get('keyTimes').split(';'))):self.assertAlmostEqual(t,i/11,delta=.000006)
                else:self.assertFalse(root.findall('.//'+NS+'animate'))
                for frame in range(12) if mode=='motion' else [None]:
                    k=min(frame,10) if frame is not None else 6
                    for attr,expected in zip(('cx','cy'),coords[k]):self.assertAlmostEqual(float(value(dot,attr,frame)),expected,delta=.006)
                    for i,h in enumerate(highlights):self.assertEqual(float(value(h,'opacity',frame)),int(i<k))
                    active=[x for x in labels if float(value(x,'opacity',frame))==1];self.assertEqual(len(active),1)
                    tp=sum(LABELS[:k]);fp=k-tp
                    expected=f'TP {tp}   FP {fp}    '+(f'TPR {tp/3:.2f}  FPR {fp/7:.2f}' if topic=='roc' else f'P {tp/k if k else 1:.2f}  R {tp/3:.2f}')
                    self.assertEqual(active[0].text,expected)
                    length=sum(math.dist(a,b) for a,b in zip(coords[:k],coords[1:k+1]))
                    self.assertAlmostEqual(float(value(lines[1],'stroke-dasharray',frame).split()[0]),length,delta=.001)
    def test_bilingual_baseline_correction(self):
        for suffix in ('','.zh-TW'):
            s=(ASSETS.parents[1]/f'theory/evaluation/metrics/classification/pr-auc{suffix}.md').read_text()
            self.assertIn('49/72',s);self.assertIn('0.450',s);self.assertIn('(R,P)=(0,1)',s)
if __name__=='__main__':unittest.main()
