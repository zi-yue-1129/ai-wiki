"""Check convolutional support and mask-union examples against SVG geometry."""
from pathlib import Path
import unittest
from xml.etree import ElementTree as ET

ASSETS = Path(__file__).resolve().parent
if not (ASSETS / 'wav2vec-window-hop-still.svg').exists():
    ASSETS = ASSETS.parent / 'docs/assets/concept-animations'
NS = '{http://www.w3.org/2000/svg}'
STEMS = ('wav2vec-window-hop', 'wav2vec-mask-overlap')


def root(stem, kind='still'):
    return ET.parse(ASSETS / f'{stem}-{kind}.svg').getroot()


class Wav2vecSpanMotion(unittest.TestCase):
    def test_window_hop(self):
        stride, field = 1, 1
        for k, s in zip((10, 3, 3, 3, 3, 2, 2), (5, 2, 2, 2, 2, 2, 2)):
            field += (k - 1) * stride
            stride *= s
        self.assertEqual((field, stride), (400, 320))
        self.assertEqual(1 + (1040 - field) // stride, 3)
        svg = root(STEMS[0])
        windows = [e for e in svg.iter(NS+'rect') if e.get('fill') == '#d4e8f3']
        self.assertEqual([(int(e.get('x')), int(e.get('width'))) for e in windows],
                         [(60+i*stride//2, field//2) for i in range(3)])
        self.assertIn(f'{field-stride} samples overlap', {e.text for e in svg.iter(NS+'text')})

    def test_mask_union(self):
        a, b = set(range(2, 6)), set(range(4, 8))
        svg = root(STEMS[1])
        for y, color, expected in ((96, '#21678d', a), (158, '#a95516', b), (240, '#087d70', a|b)):
            cells = [e for e in svg.iter(NS+'rect') if e.get('y') == str(y) and e.get('fill') == color]
            self.assertEqual({1+(int(e.get('x'))-166)//52 for e in cells}, expected)
        self.assertIn(f'Overlap: {len(a&b)}', {e.text for e in svg.iter(NS+'text')})
        self.assertIn(f'4 + 4 − 2 = {len(a|b)} / 8 masked', {e.text for e in svg.iter(NS+'text')})

    def test_assets(self):
        for stem in STEMS:
            for kind in ('motion', 'still'):
                svg = root(stem, kind)
                self.assertEqual(svg.get('viewBox'), '0 0 640 360')
                ids = [e.get('id') for e in svg.iter() if e.get('id')]
                self.assertEqual(len(ids), len(set(ids)))
                self.assertTrue(set(svg.get('aria-labelledby').split()) <= set(ids))
                self.assertFalse(any(e.tag.split('}')[-1] in {'script', 'foreignObject', 'iframe', 'image'} for e in svg.iter()))
                animations = list(svg.iter(NS+'animate'))
                self.assertEqual(bool(animations), kind == 'motion')
                for e in animations:
                    self.assertEqual(e.get('dur'), '12s')
                    self.assertEqual(e.get('repeatCount'), 'indefinite')
                    times = list(map(float, e.get('keyTimes').split(';')))
                    self.assertEqual(times, sorted(set(times)))
                    self.assertEqual((times[0], times[-1]), (0, 1))


if __name__ == '__main__':
    unittest.main()
