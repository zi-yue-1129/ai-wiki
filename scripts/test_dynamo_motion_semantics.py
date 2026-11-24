from pathlib import Path
from xml.etree import ElementTree as ET
import unittest

ASSETS = Path(__file__).resolve().parents[1] / 'docs/assets/concept-animations'
NS = '{http://www.w3.org/2000/svg}'

class DynamoMotion(unittest.TestCase):
    def check_reveal(self, stem, prefix, expected, times):
        for kind in ('motion', 'still'):
            root = ET.parse(ASSETS / f'{stem}-{kind}.svg').getroot()
            groups = [g for g in root.iter(NS+'g') if g.get('id', '').startswith(prefix)]
            self.assertEqual(len(groups), len(expected))
            for group, labels, time in zip(groups, expected, times):
                self.assertEqual([t.text for t in group.findall(NS+'text')], labels)
                anim = group.find(NS+'animate')
                if kind == 'motion':
                    self.assertEqual(anim.get('values'), '0;1;1')
                    self.assertEqual(anim.get('calcMode'), 'discrete')
                    self.assertEqual(anim.get('dur'), '12s')
                    self.assertEqual(anim.get('repeatCount'), 'indefinite')
                    self.assertAlmostEqual(float(anim.get('keyTimes').split(';')[1])*12, time, places=4)
                else:
                    self.assertIsNone(anim)
                    self.assertEqual(group.get('opacity'), '1')

    def test_guard_cache_history(self):
        cache = {}
        rows = []
        for n in (4, 4, 6, 4):
            hit = n in cache
            if not hit:
                cache[n] = chr(65 + len(cache))
            variant = cache[n]
            rows.append(['Hit '+variant if hit else 'Miss',
                         ('Reuse ' if hit else 'Compile ')+variant,
                         ' '.join(cache.values())])
        self.check_reveal('dynamo-shape-guard-cache', 'row-', rows,
                          [1.55 + 2.5*i for i in range(4)])

    def test_graph_break_values(self):
        x = 2
        y = x + 1
        printed = y
        result = y * 2
        self.check_reveal('dynamo-graph-break-resume', 'value-',
                          [[str(v)] for v in (y, printed, result)], [3, 6, 9])

if __name__ == '__main__':
    unittest.main()
