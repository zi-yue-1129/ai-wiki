from pathlib import Path
from fractions import Fraction
import unittest
import xml.etree.ElementTree as ET

ASSETS = Path(__file__).resolve().parents[1] / 'docs/assets/concept-animations'
if not ASSETS.is_dir():
    ASSETS = Path(__file__).resolve().parent
NS = '{http://www.w3.org/2000/svg}'

class WhisperTimingMotion(unittest.TestCase):
    def root(self, stem, kind):
        return ET.parse(ASSETS / f'whisper-{stem}-{kind}.svg').getroot()

    def test_timestamp_grid(self):
        times = ['0.80', '4.20', '6.00', '9.60']
        self.assertEqual([Fraction(t) / Fraction('0.02') for t in times], [40, 210, 300, 480])
        root = self.root('timestamp-interleave', 'still')
        cells = [e.text for e in root.iter(NS+'text') if e.get('y') == '255']
        self.assertEqual(cells, ['0.80', 'A', '4.20', '6.00', 'B', '9.60'])

    def test_window_shift(self):
        start, end, new_start, caption_end = 0, 30, 24, 34
        self.assertEqual(end-new_start, 6)
        self.assertEqual((new_start, new_start+end-start), (24, 54))
        self.assertEqual((0, caption_end-new_start), (0, 10))
        root = self.root('window-seek', 'motion')
        shift = [e for e in root.iter(NS+'animate') if e.get('attributeName') == 'x']
        self.assertEqual(len(shift), 1)
        self.assertEqual(shift[0].get('values'), '48;48;264;264')
        self.assertEqual((264-48)/9, new_start)

    def test_assets(self):
        for stem in ['timestamp-interleave', 'window-seek']:
            for kind in ['motion', 'still']:
                root = self.root(stem, kind)
                self.assertEqual(root.get('viewBox'), '0 0 640 360')
                ids = [e.get('id') for e in root.iter() if e.get('id')]
                self.assertEqual(len(ids), len(set(ids)))
                motions = list(root.iter(NS+'animate'))
                self.assertEqual(bool(motions), kind == 'motion')
                for e in motions:
                    self.assertEqual(e.get('repeatCount'), 'indefinite')
                    self.assertEqual(e.get('dur'), '12s')
                    ts = [float(t) for t in e.get('keyTimes').split(';')]
                    self.assertEqual(ts, sorted(ts))
                    self.assertEqual((ts[0], ts[-1]), (0, 1))
                for e in root.iter():
                    self.assertNotIn(e.tag.split('}')[-1], ('script', 'foreignObject', 'image'))
                    self.assertFalse(any(k.startswith('on') or k.endswith('href') for k in e.attrib))

if __name__ == '__main__':
    unittest.main()
