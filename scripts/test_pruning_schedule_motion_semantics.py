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
        trained = [0.9, -0.05, 0.7, 0.04, -0.8, 0.2]
        dropped = set(sorted(range(6), key=lambda i: abs(trained[i]))[:2])
        self.assertEqual(dropped, {1, 3})
        for kind in ('motion', 'still'):
            root = ET.parse(ASSETS / f'lottery-ticket-initial-reset-{kind}.svg').getroot()
            for i, v in enumerate(init):
                cell = next(e for e in root.iter(NS + 'text') if e.get('x') == str(501 + i % 3 * 48) and e.get('y') == str(86 + i // 3 * 48))
                self.assertEqual(cell.text, '0' if i in dropped else v)


if __name__ == '__main__':
    unittest.main()
