"""Check the constructed wav2vec objective examples and their SVG encodings."""
import math
from pathlib import Path
import unittest
from xml.etree import ElementTree as ET

ASSETS = Path(__file__).resolve().parent
if not (ASSETS / 'wav2vec-diversity-mean-still.svg').exists():
    ASSETS = ASSETS.parent / 'docs/assets/concept-animations'
NS = '{http://www.w3.org/2000/svg}'
STEMS = ('wav2vec-contrastive-normalization', 'wav2vec-diversity-mean')


def root(stem, kind='still'):
    return ET.parse(ASSETS / f'{stem}-{kind}.svg').getroot()


class Wav2vecObjectiveMotion(unittest.TestCase):
    def test_contrastive(self):
        svg = root(STEMS[0])
        labels = {e.text for e in svg.iter(NS + 'text')}
        weights = [math.exp(x / .3) for x in (.6, .3, 0)]
        total = sum(weights)
        self.assertIn(f'Sum = {total:.3f}', labels)
        self.assertIn(f'Loss = {-math.log(weights[0] / total):.3f}', labels)
        for i, w in enumerate(weights):
            self.assertIn(f'{w:.3f}', labels)
            self.assertIn(f'{100*w/total:.1f}%', labels)
            bars = [e for e in svg.iter(NS + 'rect') if e.get('x') == '431' and e.get('y') == str(117 + 60*i)]
            self.assertEqual(len(bars), 2)
            self.assertAlmostEqual(float(bars[-1].get('width')), 120*w/total, places=2)

    def test_diversity(self):
        svg = root(STEMS[1])
        labels = {e.text for e in svg.iter(NS + 'text')}
        for i, batch in enumerate(((.9, .9), (.9, .1))):
            p = sum(batch)/2
            entropy = -p*math.log(p)-(1-p)*math.log(1-p)
            self.assertIn(f'Entropy = {entropy:.3f}', labels)
            bars = [e for e in svg.iter(NS + 'rect') if e.get('x') == '441' and e.get('y') == str(118+128*i)]
            self.assertEqual(len(bars), 2)
            self.assertAlmostEqual(float(bars[-1].get('width')), 120*p)

    def test_assets(self):
        for stem in STEMS:
            for kind in ('motion', 'still'):
                svg = root(stem, kind)
                self.assertEqual(svg.get('viewBox'), '0 0 640 360')
                ids = [e.get('id') for e in svg.iter() if e.get('id')]
                self.assertEqual(len(ids), len(set(ids)))
                self.assertTrue(set(svg.get('aria-labelledby').split()) <= set(ids))
                self.assertFalse(any(e.tag.split('}')[-1] in {'script', 'foreignObject', 'iframe', 'image'} for e in svg.iter()))
                animations = [e for e in svg.iter() if e.tag.split('}')[-1].startswith('animate')]
                self.assertEqual(bool(animations), kind == 'motion')
                for e in animations:
                    self.assertEqual(e.get('dur'), '12s')
                    self.assertEqual(e.get('repeatCount'), 'indefinite')
                    times = [float(x) for x in e.get('keyTimes').split(';')]
                    self.assertEqual(times, sorted(set(times)))
                    self.assertEqual((times[0], times[-1]), (0, 1))


if __name__ == '__main__':
    unittest.main()
