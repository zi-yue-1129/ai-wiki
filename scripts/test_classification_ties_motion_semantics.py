"""Read actual tied-score SVG stages: credits, active pairs and grouped AP areas."""
from pathlib import Path
import xml.etree.ElementTree as ET
import unittest

ASSETS=Path(__file__).resolve().parents[1]/'docs/assets/concept-animations'
NS='{http://www.w3.org/2000/svg}'

def stages(stem):
    r=ET.parse(ASSETS/(stem+'-motion.svg')).getroot()
    return [g for g in r.findall(NS+'g') if g.get('class')=='moving']

class TiedScoreSvgTests(unittest.TestCase):
    def test_roc_active_pair_and_cumulative_credit(self):
        gs=stages('roc-tie-half-credit');pairs=[(.9,.8),(.9,.2),(.8,.8),(.8,.2)]
        total=0
        for i,(g,(pos,neg)) in enumerate(zip(gs[1:],pairs),1):
            txt=[e.text for e in g.iter(NS+'text')]
            self.assertIn(f'P   {pos:.2f}',txt);self.assertIn(f'N   {neg:.2f}',txt)
            dots=g.findall(NS+'circle')
            self.assertAlmostEqual(float(dots[0].get('cx')),62+208*pos)
            self.assertAlmostEqual(float(dots[1].get('cx')),62+208*neg)
            total+=(pos>neg)+.5*(pos==neg)
            vals=[e.text for e in g.findall(NS+'text') if e.get('class')=='num']
            numeric={'–':0,'½':.5,'1':1}
            self.assertEqual(sum(numeric[v] for v in vals),total)
            current=g.findall(NS+'animate')[0]
            self.assertEqual(current.get('values').split(';')[i],'1')
        self.assertEqual(total/4,.875)
        self.assertIn('PAIR 4 OF 4',[e.text for e in gs[-1].iter(NS+'text')])

    def test_ap_ties_enter_atomically_and_area_matches(self):
        gs=stages('pr-ap-tied-threshold');scores=[.9,.7,.7,.2];labels=[1,1,0,0]
        total=0;last_recall=0
        for i,threshold in enumerate([1,.9,.7,.2]):
            selected=[j for j,s in enumerate(scores) if s>=threshold]
            tp=sum(labels[j] for j in selected);recall=tp/2
            precision=tp/len(selected) if selected else 0
            total+=(recall-last_recall)*precision;last_recall=recall
            g=gs[i];txt=[e.text for e in g.iter(NS+'text')]
            self.assertIn('SELECT  3 (TIE)' if i==2 else f'SELECT  {len(selected)}',txt)
            self.assertIn(f'AP  {total:.3f}',txt)
            rects=[e for e in g.findall(NS+'rect') if e.get('x') in ['359','464']]
            area=sum(float(e.get('width'))*float(e.get('height')) for e in rects)/(210*126)
            self.assertAlmostEqual(area,total)
        self.assertAlmostEqual(total,5/6)

if __name__=='__main__':unittest.main()
