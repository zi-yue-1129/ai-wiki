"""Check the toy examples and their SVG labels, not measured performance."""
from itertools import combinations
from math import log, hypot
from pathlib import Path
from xml.etree import ElementTree as ET
import unittest

ASSETS = Path(__file__).resolve().parents[1] / 'docs/assets/concept-animations'
NS = '{http://www.w3.org/2000/svg}'


class SparseDistilMotion(unittest.TestCase):
    def labels(self, stem, kind):
        root = ET.parse(ASSETS / f'{stem}-{kind}.svg').getroot()
        self.assertEqual(root.get('viewBox'), '0 0 640 360')
        for node in root.iter():
            self.assertNotIn(node.tag, {NS + 'script', NS + 'foreignObject', NS + 'image'})
            self.assertFalse(any(key.startswith('on') or key.endswith('href') for key in node.attrib))
        return {e.text for e in root.iter(NS + 'text')}

    def test_sparse_metadata(self):
        x = (2, -3, 1, 4)
        w = (0, -2, 0, 3)
        packed = [(v, k) for k, v in enumerate(w, 1) if v]
        self.assertEqual(packed, [(-2, 2), (3, 4)])
        self.assertEqual(sum(v * x[k-1] for v, k in packed), 18)
        for pair in combinations(range(4), 2):
            masked = [w[i] if i in pair else 0 for i in range(4)]
            self.assertEqual(sum(masked[i] * x[i] for i in range(4)),
                             sum(w[i] * x[i] for i in pair))
        for kind in ('motion', 'still'):
            self.assertTrue({'(−2, 2)', '(3, 4)', '−2 × −3 = 6', '3 × 4 = 12', '6 + 12 = 18'} <= self.labels('sparse-metadata-gather', kind))

    def test_triple_loss(self):
        teacher, student = (.6, .3, .1), (.5, .25, .25)
        soft = -sum(p * log(q) for p, q in zip(teacher, student))
        mlm = -log(student[1])
        cosine = 1 - 3 / hypot(3, 4)
        total = soft + mlm + cosine
        self.assertEqual([f'{v:.3f}' for v in (soft, mlm, cosine, total)],
                         ['0.970', '1.386', '0.400', '2.757'])
        for kind in ('motion', 'still'):
            self.assertTrue({'0.970', '1.386', '0.400', 'Total = 2.757', 'Update student only'} <= self.labels('distilbert-triple-loss', kind))


if __name__ == '__main__':
    unittest.main()
