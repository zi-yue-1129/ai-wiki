"""Numerical regression checks for the XNOR and spatial-energy teaching assets."""
from pathlib import Path
from math import sqrt
import unittest
from xml.etree import ElementTree as ET

ASSETS = Path(__file__).resolve().parents[1] / 'docs/assets/concept-animations'
NS = '{http://www.w3.org/2000/svg}'


def labels(stem):
    return [e.text for e in ET.parse(ASSETS / f'{stem}-still.svg').iter(NS + 'text')]


class XnorAttentionMotion(unittest.TestCase):
    def test_xnor_popcount(self):
        w = [2, -1, 3, -2, 1, -3]
        x = [2, -1, -1, -2, 4, 2]
        bits = [int((a >= 0) == (b >= 0)) for a, b in zip(w, x)]
        self.assertEqual(bits, [1, 1, 0, 1, 1, 0])
        self.assertEqual([sum(bits[:i]) for i in range(7)], [0, 1, 2, 2, 3, 4, 4])
        dot = 2 * sum(bits) - len(bits)
        alpha = sum(map(abs, w)) / len(w)
        beta = sum(map(abs, x)) / len(x)
        self.assertEqual((dot, alpha, beta, alpha * beta * dot), (2, 2, 2, 8))
        self.assertEqual(sum(a * b for a, b in zip(w, x)), 4)
        self.assertIn('2 × 4 − 6 = 2', labels('xnor-popcount-dot'))
        self.assertIn('Scaled: 2 × 2 × 2 = 8', labels('xnor-popcount-dot'))

    def test_attention_spatial_energy(self):
        teacher = [[2, 0, 0, 1], [0, 1, 0, 0]]
        student = [[4, 2, 0, 2]]
        energy = lambda channels: [sum(v*v for v in col) for col in zip(*channels)]
        t, s = energy(teacher), energy(student)
        self.assertEqual(t, [4, 1, 0, 1])
        self.assertEqual(s, [16, 4, 0, 4])
        normalize = lambda a: [v / sqrt(sum(x*x for x in a)) for v in a]
        self.assertEqual(normalize(t), normalize(s))
        text = labels('attention-transfer-spatial-energy')
        for v in normalize(t):
            self.assertIn(str(round(v, 3)).removesuffix('.0'), text)
        self.assertIn('Same spatial pattern · distance = 0', text)


    def test_partial_word_mask(self):
        for w in range(64):
            for x in range(64):
                matches = ~(w ^ x) & 0xff
                valid = (matches & 0x3f).bit_count()
                expected = sum(1 if (w >> i & 1) == (x >> i & 1) else -1 for i in range(6))
                self.assertEqual(2 * valid - 6, expected)
                self.assertEqual(matches.bit_count(), valid + 2)

    def test_attention_normalized_geometry(self):
        t, s = [4, 1, 0, 1], [16, 4, 4, 4]
        normalize = lambda a: [v / sqrt(sum(x*x for x in a)) for v in a]
        u, v = normalize(t), normalize(s)
        self.assertAlmostEqual(sum(a*b for a, b in zip(u, v)), sqrt(18/19))
        self.assertAlmostEqual(sum((a-b)**2 for a, b in zip(u, v)), 2-2*sqrt(18/19))
        self.assertIn('÷ √18', labels('attention-transfer-spatial-energy'))
        self.assertIn('÷ 4√18', labels('attention-transfer-spatial-energy'))


if __name__ == '__main__':
    unittest.main()
