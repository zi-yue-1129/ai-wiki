"""Check actual SVG coordinates and SMIL state timing, not just example formulas."""
import bisect
import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / 'docs/assets/concept-animations'
NS = '{http://www.w3.org/2000/svg}'


def svg(topic):
    return ET.parse(ROOT / (topic + '-motion.svg')).getroot()


def moving(root, tag):
    return [e for e in root.iter(NS + tag) if e.find(NS + 'animate') is not None]


def sample(element, attr, t):
    a = next((a for a in element.findall(NS + 'animate') if a.get('attributeName') == attr), None)
    if a is None:
        return float(element.get(attr))
    values = a.get('values').split(';')
    times = list(map(float, a.get('keyTimes').split(';')))
    i = min(bisect.bisect_right(times, t) - 1, len(values) - 1)
    if a.get('calcMode') == 'discrete' or i == len(values) - 1:
        return float(values[i]) if attr != 'fill' else values[i]
    f = (t - times[i]) / (times[i + 1] - times[i])
    if attr == 'd':
        values = [re.search(r'M([\d.]+)', v).group(1) for v in values]
    return float(values[i]) * (1-f) + float(values[i+1]) * f


class ClassificationSvgMotionTests(unittest.TestCase):
    def test_threshold_dense_state_and_marker_agree(self):
        root = svg('precision-recall-threshold')
        marker = moving(root, 'path')[0]
        box = moving(root, 'rect')[0]
        groups = moving(root, 'g')
        labels = [1, 0, 1, 1, 0, 1, 0, 0]
        for k, g in enumerate(groups, 1):
            text = [e.text for e in g.iter(NS + 'text')]
            tp = sum(labels[:k])
            self.assertIn(f'{tp} / {k-tp} / {4-tp}', text)
            self.assertIn(f'{tp/k:.3f}', text)
            self.assertIn(f'{tp/4:.3f}', text)
        for i in range(10001):
            t = (i + .25) / 10002
            x = sample(marker, 'd', t)
            k = sum(91 + 64*j <= x for j in range(8))
            active = [j+1 for j,g in enumerate(groups) if sample(g, 'opacity', t) == 1]
            self.assertEqual(active, [k], (t, x, active, k))
            self.assertAlmostEqual(69 + sample(box, 'width', t), x, places=7)

    def test_accuracy_actual_geometry(self):
        r = svg('accuracy-prevalence'); bars = moving(r, 'rect'); dots = moving(r, 'circle')
        for i in range(101):
            t = i/100; p = sample(bars[0], 'width', t)/246
            accuracy = .8*p + .9*(1-p)
            self.assertAlmostEqual(sample(bars[1], 'width', t), 168*accuracy, places=6)
            self.assertAlmostEqual(sample(dots[0], 'cy', t), 270-1340*(accuracy-.8), places=6)
            self.assertEqual(sample(dots[1], 'cy', t), 203)

    def test_f1_harmonic_actual_geometry(self):
        dots = moving(svg('f1-harmonic-gap'), 'circle')
        for i in range(1001):
            t=i/1000; p=(sample(dots[0], 'cx', t)-85)/470
            self.assertAlmostEqual(sample(dots[0], 'cy', t), 293-192*(1.6*p/(p+.8)), delta=.07)
            self.assertAlmostEqual(sample(dots[1], 'cy', t), 293-192*(p+.8)/2, delta=.002)

    def test_fbeta_actual_geometry(self):
        r=svg('fbeta-recall-emphasis'); dot=moving(r,'circle')[0]; bar=moving(r,'rect')[0]
        for i in range(1001):
            t=i/1000; beta=.5+(sample(dot,'cx',t)-104)*1.5/230
            f=(1+beta*beta)*.45*.9/(beta*beta*.45+.9)
            self.assertAlmostEqual(sample(dot,'cy',t),249-355*(f-.5),delta=.36)
            self.assertAlmostEqual(sample(bar,'width',t),121*f,delta=.13)

    def test_precision_base_rate_actual_geometry(self):
        r=svg('precision-base-rate'); dot=moving(r,'circle')[0]; bars=moving(r,'rect')
        for i in range(1001):
            t=i/1000; p=.01+(sample(dot,'cx',t)-355)*.49/222
            ppv=.9*p/(.9*p+.05*(1-p))
            self.assertAlmostEqual(sample(dot,'cy',t),278-138*ppv,delta=.53)
            self.assertAlmostEqual(sample(bars[0],'width',t),245*p,delta=.006)
            self.assertAlmostEqual(sample(bars[1],'width',t),245*ppv,delta=.94)
            self.assertAlmostEqual(sample(bars[1],'width',t)+sample(bars[2],'width',t),245,places=6)
            self.assertAlmostEqual(sample(bars[2],'x',t),48+sample(bars[1],'width',t),places=6)

    def test_macro_micro_discrete_tiles_and_coordinates(self):
        r=svg('f1-macro-micro-imbalance'); dots=moving(r,'circle'); tiles=moving(r,'rect')
        for i in range(1001):
            t=i/1000; k=sum(sample(e,'fill',t)=='#168d80' for e in tiles)
            micro=(90+k)/100; macro=.5*(180/(190-k)+2*k/(10+k))
            for dot,value in zip(dots,[micro,macro]):
                self.assertAlmostEqual(sample(dot,'cx',t),356+22.4*k,places=6)
                self.assertAlmostEqual(sample(dot,'cy',t),276-135*value,delta=.006)


if __name__ == '__main__':
    unittest.main()
