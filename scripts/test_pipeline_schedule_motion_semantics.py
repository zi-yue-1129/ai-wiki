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
                    done.update(pending)
                    for stage in range(3):
                        histories[stage].append(len(saved[stage]))
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
