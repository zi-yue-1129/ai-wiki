from fractions import Fraction
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

ASSETS = Path(__file__).resolve().parents[1] / 'docs/assets/concept-animations'
NS = '{http://www.w3.org/2000/svg}'


class PruningScheduleMotionTest(unittest.TestCase):
    def test_cubic_schedule_and_masks(self):
        order = [7, 2, 12, 0, 10, 5, 14, 3, 9, 15, 1, 6, 8, 4, 11, 13]
        counts = [int(16 * Fraction(3, 4) * (1 - (1 - Fraction(i, 4)) ** 3)) for i in range(5)]
        self.assertEqual(counts, [0, 6, 10, 11, 12])
        for kind in ('motion', 'still'):
            root = ET.parse(ASSETS / f'gradual-pruning-cubic-mask-{kind}.svg').getroot()
            for i, n in enumerate(counts):
                cells = [e for e in root.iter(NS + 'rect') if e.get('y') == str(62 + i * 50) and e.get('width') == '11']
                self.assertEqual(len(cells), 16)
                self.assertEqual([j for j, e in enumerate(cells) if e.get('fill') == '#dce4eb'], sorted(order[:n]))
                self.assertTrue(any(e.text == f'{n}/16' for e in root.iter(NS + 'text')))

    def test_ticket_mask_and_original_reset(self):
        init = ['0.2', '−0.4', '0.6', '−0.1', '0.3', '−0.5']
        trained = [[0.9, -0.05, 0.7, 0.04, -0.8, 0.2], [0.05, 0, 0.8, 0, -0.6, 0.3]]
        kept = set(range(6))
        for r, n in enumerate((2, 1)):
            kept -= set(sorted(kept, key=lambda i: abs(trained[r][i]))[:n])
            self.assertEqual(kept, ({0, 2, 4, 5}, {2, 4, 5})[r])
            for kind in ('motion', 'still'):
                root = ET.parse(ASSETS / f'lottery-ticket-initial-reset-{kind}.svg').getroot()
                for i, v in enumerate(init):
                    for prefix, expected in [('mask', str(int(i in kept))), ('reset', v if i in kept else '0')]:
                        cell = next(e for e in root.iter(NS + 'g') if e.get('id') == f'{prefix}-{r}-{i}')
                        self.assertEqual(cell.find(NS + 'text').text, expected)

    def test_rounding_and_mask_turnover(self):
        for N in range(1, 33):
            for j in range(101):
                target = Fraction(j, 100)
                actual = Fraction(int(N * target), N)
                self.assertTrue(0 <= target - actual < Fraction(1, N))
        a = [1, 3, 5, 7]
        b = [8, 1, 2, 7]
        first = set(sorted(range(4), key=lambda i: a[i])[:1])
        reselect = set(sorted(range(4), key=lambda i: b[i])[:2])
        nested = first | set(sorted(set(range(4)) - first, key=lambda i: b[i])[:1])
        self.assertEqual((first, reselect, nested), ({0}, {1, 2}, {0, 1}))
        self.assertFalse(first <= reselect)
        self.assertTrue(first <= nested)


if __name__ == '__main__':
    unittest.main()
