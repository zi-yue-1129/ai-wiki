"""Check rendered schedule labels and saved-activation history against dependencies."""
from pathlib import Path
import re
import unittest
from xml.etree import ElementTree as ET

ASSETS = Path(__file__).resolve().parents[1] / 'docs/assets/concept-animations'
NS = '{http://www.w3.org/2000/svg}'


class PipelineSchedule(unittest.TestCase):
    def test_schedule_dependencies_and_memory_trace(self):
        for kind in ('motion', 'still'):
            schedule = ET.parse(ASSETS / f'gpipe-1f1b-schedule-{kind}.svg').getroot()
            trace = ET.parse(ASSETS / f'gpipe-activation-liveness-{kind}.svg').getroot()
            by_id = {e.get('id'): e for e in schedule.iter() if e.get('id')}
            curves = {e.get('id'): e for e in trace.iter() if e.get('id')}
            for policy in range(2):
                done = set()
                saved = [set() for _ in range(3)]
                histories = [[0] for _ in range(3)]
                idle = 0
                local = [[] for _ in range(3)]
                completed_at = {}
                for t in range(12):
                    pending = []
                    for stage in range(3):
                        op = by_id[f'op-{policy}-{stage}-{t}'].find(NS+'text').text
                        if op == '·':
                            idle += 1
                            continue
                        direction, batch = op[0], int(op[1:])
                        self.assertIn(direction, ('F', 'B'))
                        self.assertIn(batch, range(1,5))
                        key = (stage, direction, batch)
                        self.assertNotIn(key, done)
                        if direction == 'F':
                            if stage:
                                self.assertIn((stage-1, 'F', batch), done)
                            saved[stage].add(batch)
                        else:
                            self.assertIn((stage, 'F', batch), done)
                            if stage < 2:
                                self.assertIn((stage+1, 'B', batch), done)
                            saved[stage].remove(batch)
                        local[stage].append(op)
                        pending.append(key)
                        completed_at[key] = t + 1
                    done.update(pending)
                    for stage in range(3):
                        histories[stage].append(len(saved[stage]))
                aggregate = [sum(values) for values in zip(*histories)]
                self.assertEqual(aggregate[3], 6)
                self.assertEqual([row[6] for row in histories], [4, 4, 4] if policy == 0 else [2, 2, 0])
                self.assertEqual(max(aggregate), 12 if policy == 0 else 6)
                # Weight each stage's boundary counts by its saved-set size (MiB).
                weighted = [sum(n * size for n, size in zip(values, (2, 4, 8)))
                            for values in zip(*histories)]
                self.assertEqual(max(weighted), 56 if policy == 0 else 22)
                self.assertEqual(weighted.index(max(weighted)), 6 if policy == 0 else 3)
                self.assertEqual(sum(weighted[:-1]), 288 if policy == 0 else 130)
                # Double-count the saved-set area using each micro-batch's lifetime.
                durations = [[completed_at[(s, 'B', b)] - completed_at[(s, 'F', b)]
                              for b in range(1, 5)] for s in range(3)]
                expected_durations = ([[11, 9, 7, 5], [9, 7, 5, 3], [7, 5, 3, 1]]
                                      if policy == 0 else [[5, 6, 7, 5], [3, 4, 3, 3], [1, 1, 1, 1]])
                self.assertEqual(durations, expected_durations)
                stage_areas = [sum(row) for row in durations]
                self.assertEqual(stage_areas, [sum(row[:-1]) for row in histories])
                self.assertEqual(stage_areas, [32, 24, 16] if policy == 0 else [23, 13, 4])
                self.assertEqual(sum(area * size for area, size in zip(stage_areas, (2, 4, 8))),
                                 sum(weighted[:-1]))
                self.assertEqual(len(done), 24)
                self.assertEqual(idle, 12)
                self.assertTrue(all(not s for s in saved))
                for stage in range(3):
                    if policy == 0:
                        expected = [f'F{i}' for i in range(1,5)] + [f'B{i}' for i in range(4,0,-1)]
                    else:
                        warmup = 2-stage
                        expected = [f'F{i}' for i in range(1,warmup+1)]
                        for i in range(1,5-warmup):
                            expected += [f'F{i+warmup}', f'B{i}']
                        expected += [f'B{i}' for i in range(5-warmup,5)]
                    self.assertEqual(local[stage], expected)
                    self.assertEqual(max(histories[stage]), 4 if policy == 0 else 3-stage)
                    path = curves[f'count-{policy}-{stage}'].get('d')
                    base = 110+89*stage
                    self.assertTrue(path.startswith(f'M106 {base}'))
                    samples = [(int(x), int(y)) for x,y in re.findall(r'H(\d+)V(\d+)', path)]
                    self.assertEqual(samples, [(106+42*t, base-14*histories[stage][t]) for t in range(1,13)])

    def test_weighted_microbatch_gradient_is_schedule_independent(self):
        from fractions import Fraction
        sizes, means = (2, 2, 1, 1), (1, 3, 5, 7)
        full = Fraction(sum(n * g for n, g in zip(sizes, means)), sum(sizes))
        self.assertEqual(full, Fraction(10, 3))
        self.assertNotEqual(full, Fraction(sum(means), len(means)))
        for kind in ('motion', 'still'):
            root = ET.parse(ASSETS / f'gpipe-1f1b-schedule-{kind}.svg').getroot()
            by_id = {e.get('id'): e for e in root.iter() if e.get('id')}
            for policy in range(2):
                for stage in range(3):
                    order = []
                    for t in range(12):
                        label = by_id[f'op-{policy}-{stage}-{t}'].find(NS+'text').text
                        if label.startswith('B'):
                            order.append(int(label[1:]) - 1)
                    self.assertEqual(order, [3, 2, 1, 0] if policy == 0 else [0, 1, 2, 3])
                    self.assertEqual(sum(Fraction(sizes[i] * means[i], sum(sizes)) for i in order), full)

    def test_masked_token_gradient_with_empty_microbatch(self):
        from fractions import Fraction
        # Sum-reduced token gradients: one micro-batch has no valid targets.
        counts = (3, 0, 1, 2)
        numerators = (9, 0, -2, 8)
        expected = Fraction(15, 6)
        for kind in ('motion', 'still'):
            root = ET.parse(ASSETS / f'gpipe-1f1b-schedule-{kind}.svg').getroot()
            by_id = {e.get('id'): e for e in root.iter() if e.get('id')}
            for policy in range(2):
                for stage in range(3):
                    order = [int(label[1:]) - 1 for t in range(12)
                             if (label := by_id[f'op-{policy}-{stage}-{t}'].find(NS+'text').text).startswith('B')]
                    self.assertEqual(sorted(order), list(range(4)))
                    total = sum(counts[i] for i in order)
                    self.assertEqual(Fraction(sum(numerators[i] for i in order), total), expected)
                    self.assertEqual(sum(Fraction(numerators[i], counts[i]) * Fraction(counts[i], total)
                                         for i in order if counts[i]), expected)

    def test_reveal_boundaries(self):
        schedule = ET.parse(ASSETS / 'gpipe-1f1b-schedule-motion.svg').getroot()
        trace = ET.parse(ASSETS / 'gpipe-activation-liveness-motion.svg').getroot()
        a = schedule.find('.//'+NS+'clipPath/'+NS+'rect/'+NS+'animate')
        self.assertEqual(a.get('calcMode'), 'discrete')
        self.assertEqual(a.get('values').split(';'), [str(min(i,12)*42) for i in range(14)])
        self.assertEqual(a.get('dur'), '14s')
        for i,t in enumerate(a.get('keyTimes').split(';')):
            self.assertAlmostEqual(float(t), i/14 if i < 13 else 1, places=7)
        b = trace.find('.//'+NS+'clipPath/'+NS+'rect/'+NS+'animate')
        self.assertEqual(b.get('values'), '0;504;504')
        for root in (schedule, trace):
            c = root.find('.//'+NS+'animateTransform')
            self.assertEqual(c.get('dur'), '14s')
            self.assertEqual(c.get('values'), '0 0;504 0;504 0')
            self.assertAlmostEqual(float(c.get('keyTimes').split(';')[1]), 12/14, places=7)


if __name__ == '__main__':
    unittest.main()
