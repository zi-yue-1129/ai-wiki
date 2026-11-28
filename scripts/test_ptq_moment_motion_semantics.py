"""Check exact toy arithmetic and matching SVG keyframe geometry."""
import unittest
from fractions import Fraction as F
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'docs/assets/concept-animations'
if not ASSETS.is_dir():  # standalone local QA, same assets beside this test
    ASSETS = Path(__file__).resolve().parent
NS = '{http://www.w3.org/2000/svg}'


def read(stem, kind):
    return ET.parse(ASSETS / f'{stem}-{kind}.svg').getroot()


def values(element):
    return list(map(float, element.get('values').split(';')))


class PTQMomentMotion(unittest.TestCase):
    def test_group_rounding(self):
        small = [F(1), F(3, 2), F(3), F(4)]
        large = [F(8), F(16), F(24), F(28)]
        sse = lambda ws, s: sum((w - round(w / s) * s) ** 2 for w in ws)
        self.assertEqual(sse(small + large, F(4)), F(17, 4))
        self.assertEqual(sse(small, F(4, 7)) + sse(large, F(4)), F(17, 196))
        root = read('ptq-group-scale-grid', 'motion')
        still = read('ptq-group-scale-grid', 'still')
        nodes = {n.get('id'): n for n in root.iter() if n.get('id')}
        still_nodes = {n.get('id'): n for n in still.iter() if n.get('id')}
        ends = [0.19, 0.34, 0.49, 0.64]
        self.assertEqual(len(root.findall('.//' + NS + 'animate')), 18)
        for key, left, scale in [('shared', 12, F(4)), ('local', 328, F(4, 7))]:
            errors = [(w - round(w / scale) * scale) ** 2 for w in small]
            for i, w in enumerate(small):
                dot = nodes[f'{key}-dot-{i}'].find(NS+'animate')
                bar = nodes[f'{key}-error-{i}'].find(NS+'animate')
                v = values(dot)
                self.assertAlmostEqual(v[0], float(left+44+38*w), places=3)
                self.assertAlmostEqual(v[2], float(left+44+38*round(w/scale)*scale), places=3)
                self.assertEqual(v[0], v[-1])
                self.assertEqual(float(dot.get('keyTimes').split(';')[2]), ends[i])
                self.assertEqual(float(bar.get('keyTimes').split(';')[1]), ends[i])
                self.assertEqual(bar.get('calcMode'), 'discrete')
                self.assertAlmostEqual(values(bar)[1], float(74*errors[i]/F(9,4)), places=3)
                self.assertAlmostEqual(float(still_nodes[f'{key}-error-{i}'].get('width')), values(bar)[1], places=3)
                self.assertAlmostEqual(float(still_nodes[f'{key}-dot-{i}'].get('cx')), v[2], places=3)
            total = nodes[f'{key}-total'].find(NS+'animate')
            self.assertEqual(list(map(float,total.get('keyTimes').split(';')))[1:5], ends)
            for i in range(4):
                self.assertAlmostEqual(values(total)[i+1], float(272*sum(errors[:i+1])/F(17,4)), places=3)
            self.assertAlmostEqual(float(still_nodes[f'{key}-total'].get('width')), values(total)[4], places=3)

    def test_moment_nonidentifiability(self):
        a = [(F(1), F(1,2)), (F(3), F(1,2))]
        b = [(F(0), F(1,8)), (F(2), F(3,4)), (F(4), F(1,8))]
        for dist in (a,b):
            self.assertEqual(sum(p for _,p in dist),1)
            self.assertEqual(sum(x*p for x,p in dist),2)
            self.assertEqual(sum((x-2)**2*p for x,p in dist),1)
        self.assertEqual(sum((x-2)**4*p for x,p in a),1)
        self.assertEqual(sum((x-2)**4*p for x,p in b),4)

    def test_moment_descent(self):
        root = read('data-free-moment-descent', 'motion')
        motions = root.findall('.//' + NS + 'animate')
        self.assertEqual(len(motions), 8)
        self.assertEqual([a.get('calcMode') for a in motions[5:]], ['discrete'] * 3)
        steps = [0, 0, 1, 2, 3, 4, 5, 5, 0]
        m, s = F(-1), F(1, 4)
        states = [(m, s)]
        for _ in range(5):
            m -= F(1, 4)*2*(m-2)
            s -= F(1, 4)*2*(s-1)
            states.append((m, s))
        for i, k in enumerate(steps):
            m, s = states[k]
            loss = (m-2)**2 + (s-1)**2
            self.assertEqual(loss, F(153, 16)/4**k)
            a, b = 80+80*(m-s+2), 80+80*(m+s+2)
            expected = [a, b, 80+80*(m+2)-2, a, b, 220*loss/F(153,16), 69+46*k, 235+16*k]
            for motion, val in zip(motions, expected):
                self.assertAlmostEqual(values(motion)[i], float(val), places=3)

    def test_calibration_output_error(self):
        w = [F(11,10), F(17,20)]
        results = []
        for scale in [F(1), F(3,5)]:
            self.assertTrue(all((v/scale) % 1 != F(1,2) for v in w))
            codes = [round(v/scale) for v in w]
            self.assertTrue(all(-7 <= q <= 7 for q in codes))
            d = [v-q*scale for v,q in zip(w,codes)]
            results.append((sum(v*v for v in d), *(sum(v*x for v,x in zip(d,inp))**2 for inp in [(5,2),(3,2)])))
        self.assertEqual(results, [(F(13,400), F(1,25), F(0)), (F(29,400), F(0), F(1,25))])
        for p in [F(0), F(1,2), F(1)]:
            losses = [p*a+(1-p)*b for _,a,b in results]
            self.assertEqual(losses[0]-losses[1], (2*p-1)/25)

    def test_asset_contracts(self):
        for stem in ('ptq-group-scale-grid', 'data-free-moment-descent'):
            for kind in ('motion', 'still'):
                root = read(stem, kind)
                self.assertEqual(root.get('viewBox'), '0 0 640 360')
                self.assertIsNotNone(root.find(NS+'title'))
                self.assertIsNotNone(root.find(NS+'desc'))
                self.assertFalse(any(e.tag.split('}')[-1] in ('script','foreignObject','image') for e in root.iter()))
                animations = root.findall('.//' + NS + 'animate')
                self.assertEqual(bool(animations), kind=='motion')
                for a in animations:
                    self.assertEqual(a.get('repeatCount'), 'indefinite')
                    self.assertEqual(a.get('dur'), '12s')
                    times = list(map(float, a.get('keyTimes').split(';')))
                    self.assertEqual(len(times), len(values(a)))
                    self.assertEqual(times, sorted(set(times)))
                    self.assertEqual((times[0],times[-1]),(0,1))


if __name__ == '__main__':
    unittest.main()
