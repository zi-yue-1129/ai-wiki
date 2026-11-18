"""Check rendered resolution dependency order and the actual JS lab controller."""
from pathlib import Path
import bisect
import subprocess
import unittest
import xml.etree.ElementTree as E
ROOT=Path(__file__).resolve().parents[1];N='{http://www.w3.org/2000/svg}'

def sample(e, attr, t):
    a=next((a for a in e.findall(N+'animate') if a.get('attributeName')==attr),None)
    if a is None:return float(e.get(attr,'1'))
    times=list(map(float,a.get('keyTimes').split(';')));values=list(map(float,a.get('values').split(';')))
    assert len(times)==len(values) and times[0]==0 and times[-1]==1
    i=min(bisect.bisect_right(times,t)-1,len(times)-1)
    if a.get('calcMode')=='discrete' or i==len(times)-1:return values[i]
    u=(t-times[i])/(times[i+1]-times[i]);return values[i]+u*(values[i+1]-values[i])

class ResolutionProof(unittest.TestCase):
    def test_svg_inference_dependencies_and_cursor_arrival(self):
        root=E.parse(ROOT/'docs/assets/concept-animations/resolution-refutation-chain-motion.svg').getroot()
        outputs=[e for e in root if e.get('class','').startswith('resolution-output-')]
        parents=[e for e in root if e.get('class')=='resolution-derived-parent']
        cursors=[e for e in root if e.get('class')=='motion']
        status=next(e for e in root if e.get('class')=='resolution-status')
        self.assertEqual([e.find(N+'text').text for e in outputs],['Q ∨ R','R','□'])
        def at(x,y):
            return next(e.text for e in root.iter(N+'text')
                        if e.get('x')==str(x) and e.get('y')==str(y))
        for i,pivot in enumerate(('P','Q','R')):
            left=set(at(102,100+100*i).split(' ∨ '))
            right=set(at(278,100+100*i).split(' ∨ '))
            self.assertEqual(at(387,83+100*i),f'/{pivot}/')
            self.assertIn(pivot,left);self.assertIn('¬'+pivot,right)
            actual=(left-{pivot})|(right-{'¬'+pivot})
            output=outputs[i].find(N+'text').text
            expected=set() if output=='□' else set(output.split(' ∨ '))
            self.assertEqual(actual,expected)
            if i:self.assertEqual(left,set(outputs[i-1].find(N+'text').text.split(' ∨ ')))
        self.assertEqual([e.find(N+'text').text for e in parents],['Q ∨ R','R'])
        for t in (i/10000 for i in range(10001)):
            for i,g in enumerate(outputs):self.assertEqual(sample(g,'opacity',t),int(t>=(i+1)/4))
            for i,g in enumerate(parents):self.assertEqual(sample(g,'opacity',t),int(t>=(i+1)/4))
            self.assertEqual(sample(status,'opacity',t),int(t>=.75))
            for i,g in enumerate(cursors):
                self.assertEqual(sample(g,'opacity',t),int(i/4<=t<(i+1)/4))
                c=g.find(N+'circle');self.assertEqual(float(c.get('cy')),95+100*i)
                want=357+68*min(1,max(0,(t-i/4)*4))
                self.assertAlmostEqual(sample(c,'cx',t),want,delta=1e-8)
        still=E.parse(ROOT/'docs/assets/concept-animations/resolution-refutation-chain-still.svg').getroot()
        self.assertFalse(list(still.iter(N+'animate')))
        self.assertIn('□',[e.text for e in still.iter(N+'text')]);self.assertIn('UNSAT',[e.text for e in still.iter(N+'text')])

    def test_actual_js_resolution_and_repeated_controls(self):
        subprocess.run(['node',str(ROOT/'scripts/test_resolution_lab.cjs')],check=True)

if __name__=='__main__':unittest.main()
