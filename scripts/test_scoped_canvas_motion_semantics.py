"""Execute SVG guard positives/mutations; never infer expected geometry from input."""
from copy import deepcopy
from pathlib import Path
import tempfile
import json
import unittest
from unittest.mock import patch
from xml.etree import ElementTree as ET
import verify_concept_motion as v

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'docs/assets/concept-animations'
# Frozen original git-blob geometry evidence, not derived from the input SVGs.
CONTRACTS = json.loads((ROOT / 'scripts/fixtures/deployed-motion-contracts.json').read_text())
EXPECTED_CANVASES = {stem: entry['viewBox'] for stem, entry in CONTRACTS['canonical'].items()}
EXPECTED_EXTRAS = {name: entry['viewBox'] for name, entry in CONTRACTS['extra'].items()}
EXPECTED_PREFIXES = {name: entry['viewBox'] for name, entry in CONTRACTS['prefix'].items()}
assert len(EXPECTED_CANVASES) == 429 and len(EXPECTED_EXTRAS) == 9 and len(EXPECTED_PREFIXES) == 28

EXPECTED_EXCLUSIONS = {name: tuple(entry['excluded_prefixes']) for name, entry in CONTRACTS['prefix'].items() if entry.get('excluded_prefixes')}



assert EXPECTED_EXCLUSIONS == {'forward-ad-': ('forward-ad-jvp-',)}

# These are candidates, NOT an allowance: only a stem's literal registry value passes.
CANDIDATES = {'0 0 640 360', '0 0 720 400', '0 0 720 460', '0 0 760 410', '0 0 800 420', '0 0 641 361', '0 0 1 1'} | set(EXPECTED_CANVASES.values()) | set(EXPECTED_EXTRAS.values())

class ScopedCanvas(unittest.TestCase):
    def assert_reviewed_registry(self):
        self.assertEqual(v.CANONICAL_VIEWBOXES, EXPECTED_CANVASES)
        self.assertEqual(v.EXTRA_CANONICAL_FILENAMES, EXPECTED_EXTRAS)
        self.assertEqual(v.PREFIX_VIEWBOXES, EXPECTED_PREFIXES)
        self.assertEqual(v.PREFIX_EXCLUSIONS, EXPECTED_EXCLUSIONS)
        self.assertEqual(set(v.TOPICS), set(EXPECTED_CANVASES))

    def test_reviewed_registry_cannot_shrink_clear_or_substitute(self):
        for attribute, expected in [('CANONICAL_VIEWBOXES', EXPECTED_CANVASES), ('EXTRA_CANONICAL_FILENAMES', EXPECTED_EXTRAS), ('PREFIX_VIEWBOXES', EXPECTED_PREFIXES)]:
            mutations = [('empty', {})]
            for name in expected:
                without = {key: value for key, value in expected.items() if key != name}
                mutations += [('delete:' + name, without), ('replace:' + name, {**without, 'unreviewed-substitute': expected[name]})]
            for label, mutation in mutations:
                with self.subTest(attribute=attribute, mutation=label):
                    with patch.object(v, attribute, mutation):
                        with self.assertRaises(AssertionError):
                            self.assert_reviewed_registry()
        # Deleting matching entries in BOTH production sets is not preservation.
        for stem in EXPECTED_CANVASES:
            with patch.dict(v.TOPICS, {k: x for k, x in v.TOPICS.items() if k != stem}, clear=True), patch.dict(v.CANONICAL_VIEWBOXES, {k: x for k, x in v.CANONICAL_VIEWBOXES.items() if k != stem}, clear=True):
                with self.assertRaises(AssertionError):
                    self.assert_reviewed_registry()

    def test_registry_is_complete_and_each_registered_asset_has_one_literal_canvas(self):
        self.assert_reviewed_registry()
        for stem, box in EXPECTED_CANVASES.items():
            self.assertIsInstance(box, str)
            for kind in ('motion', 'still'):
                path = ASSETS / f'{stem}-{kind}.svg'
                with self.subTest(path=path.name):
                    self.assertEqual(v.expected_viewbox(path), box)
                    self.assertEqual(v.verify_svg(path, kind == 'motion'), [])

    def test_every_actual_main_validation_call_is_explicitly_covered(self):
        import contextlib
        import io
        import os
        called = set()
        real = v.verify_svg
        def record(path, animated):
            called.add(path.name)
            return real(path, animated)
        previous = Path.cwd()
        try:
            os.chdir(ROOT)
            with patch.object(v, 'verify_svg', side_effect=record), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(v.main(), 0)
        finally:
            os.chdir(previous)
        expected = {f'{stem}-{kind}.svg' for stem in EXPECTED_CANVASES for kind in ('motion', 'still')}
        self.assertEqual(called, expected | set(EXPECTED_EXTRAS))

    def test_explicit_non_topic_variants_keep_valid_canvas_and_reject_others(self):
        with tempfile.TemporaryDirectory() as td:
            for filename, correct in EXPECTED_EXTRAS.items():
                source = ASSETS / filename
                animated = filename.endswith('-motion.svg')
                self.assertEqual(v.verify_svg(source, animated), [])
                root = ET.parse(source).getroot()
                for box in CANDIDATES - {correct}:
                    root.set('viewBox', box)
                    path = Path(td) / filename
                    path.write_bytes(ET.tostring(root))
                    self.assertTrue(any('viewBox' in e for e in v.verify_svg(path, animated)))

    def test_all_other_global_shapes_are_rejected_for_every_registered_asset(self):
        with tempfile.TemporaryDirectory() as td:
            for stem, correct in EXPECTED_CANVASES.items():
                for kind in ('motion', 'still'):
                    root = ET.parse(ASSETS / f'{stem}-{kind}.svg').getroot()
                    path = Path(td) / f'{stem}-{kind}.svg'
                    for box in CANDIDATES - {correct}:
                        root.set('viewBox', box)
                        path.write_bytes(ET.tostring(root))
                        with self.subTest(stem=stem, kind=kind, box=box):
                            self.assertTrue(any('viewBox' in e for e in v.verify_svg(path, kind == 'motion')))

    def test_unknown_name_and_new_registered_stem_fail_closed(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / 'unreviewed-topic-motion.svg'
            path.write_bytes((ASSETS / 'ece-binned-calibration-motion.svg').read_bytes())
            with patch.dict(v.TOPICS, {'unreviewed-topic': 'some/page'}):
                self.assertIsNone(v.expected_viewbox(path))
                self.assertTrue(any('viewBox' in e for e in v.verify_svg(path, True)))

    def test_preserved_prefix_contracts_accept_valid_variants_and_reject_wrong_canvas(self):
        with tempfile.TemporaryDirectory() as td:
            for prefix, box in EXPECTED_PREFIXES.items():
                for variant in ('-reviewed-variant-motion', '-reviewed-variant-still'):
                    kind = 'motion' if variant.endswith('motion') else 'still'
                    path = Path(td) / f'{prefix}{variant}.svg'
                    sample = CONTRACTS['prefix'][prefix].get('sample_stem', prefix)
                    root = ET.parse(ASSETS / f'{sample}-{kind}.svg').getroot()
                    path.write_bytes(ET.tostring(root))
                    self.assertEqual(v.expected_viewbox(path), box)
                    self.assertEqual(v.verify_svg(path, kind == 'motion'), [])
                    root.set('viewBox', '0 0 1 1'); path.write_bytes(ET.tostring(root))
                    self.assertTrue(any('viewBox' in e for e in v.verify_svg(path, kind == 'motion')))

    def test_original_prefix_exclusions_are_not_broadened(self):
        for prefix, excluded in EXPECTED_EXCLUSIONS.items():
            with patch.object(v, 'PREFIX_EXCLUSIONS', {}):
                with self.assertRaises(AssertionError):self.assert_reviewed_registry()
            for exception in excluded:
                self.assertIsNone(v.expected_viewbox(Path(exception + 'unregistered-variant-motion.svg')))

    def test_longest_explicit_prefix_wins_and_registered_topics_never_inherit(self):
        with patch.dict(v.PREFIX_VIEWBOXES, {'ece-binned-calibration-special': '0 0 800 420'}):
            self.assertEqual(v.expected_viewbox(Path('ece-binned-calibration-special-preview.svg')), '0 0 800 420')
            with patch.dict(v.TOPICS, {'ece-binned-calibration-special-preview': 'page'}):
                self.assertIsNone(v.expected_viewbox(Path('ece-binned-calibration-special-preview-motion.svg')))

    def test_original_xml_accessibility_security_and_animation_guards_remain(self):
        source = ET.parse(ASSETS / 'ece-binned-calibration-motion.svg').getroot()
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / 'ece-binned-calibration-motion.svg'
            for label in ('title', 'desc'):
                root = deepcopy(source); root.remove(root.find(v.NS + label))
                path.write_bytes(ET.tostring(root))
                self.assertTrue(any('accessible ' + label in e for e in v.verify_svg(path, True)))
            # Original safety contract, independent of the production set.
            forbidden = {'script', 'foreignObject', 'iframe', 'image'}
            self.assertEqual(v.FORBIDDEN, forbidden)
            for tag in forbidden:
                root = deepcopy(source); ET.SubElement(root, v.NS + tag)
                path.write_bytes(ET.tostring(root))
                self.assertTrue(any('prohibited ' + tag in e for e in v.verify_svg(path, True)))
            for attribute, value, error in [('onclick', 'x()', 'event handler'), ('href', 'https://example.test/a', 'external or active')]:
                root = deepcopy(source); root.set(attribute, value); path.write_bytes(ET.tostring(root))
                self.assertTrue(any(error in e for e in v.verify_svg(path, True)))
            for attribute, value, error in [('repeatCount', '1', 'loop indefinitely'), ('dur', '500', 'duration in seconds')]:
                root = deepcopy(source)
                animation = next(e for e in root.iter() if e.tag.split('}')[-1] in ('animate', 'animateMotion', 'animateTransform'))
                animation.set(attribute, value); path.write_bytes(ET.tostring(root))
                self.assertTrue(any(error in e for e in v.verify_svg(path, True)))
            path.write_bytes(ET.tostring(source))
            self.assertTrue(any('still fallback contains animation' in e for e in v.verify_svg(path, False)))
            path.write_bytes((ASSETS / 'ece-binned-calibration-still.svg').read_bytes())
            self.assertTrue(any('no animation' in e for e in v.verify_svg(path, True)))
            path.write_text('<svg>')
            self.assertTrue(any('invalid XML' in e for e in v.verify_svg(path, True)))


class InterconnectTiming(unittest.TestCase):
    def test_ring_delivery_before_state_transition(self):
        from fractions import Fraction
        root = ET.parse(ASSETS / 'interconnect-ring-reduction-motion.svg').getroot()
        n = 3
        rounds = 2 * (n - 1)
        duration = 2 * (rounds + 1)
        ns = v.NS
        groups = {g.get('id'): g for g in root.iter(ns + 'g') if (g.get('id') or '').startswith('round-')}
        self.assertEqual(len(groups), rounds + 1)
        state = [list(range(1 + n*r, 1 + n*(r+1))) for r in range(n)]
        for step in range(rounds + 1):
            group = groups[f'round-{step}']
            track = group.find(ns + 'animate')
            self.assertEqual(track.get('calcMode'), 'discrete')
            self.assertEqual(track.get('dur'), f'{duration}s')
            times = list(map(Fraction, track.get('keyTimes').split(';')))
            self.assertEqual(times, [Fraction(i, rounds + 1) for i in range(rounds + 2)])
            values = list(map(int, track.get('values').split(';')))
            self.assertEqual(values, [int(min(i, rounds) == step) for i in range(rounds + 2)])
            labels = [t.text for t in group.iter(ns + 'text') if t.get('y') == '150']
            self.assertEqual(labels, [str(x) if x is not None else '–' for row in state for x in row])
            if step == rounds:
                self.assertEqual(state, [[sum(range(c+1, n*n+1, n)) for c in range(n)]] * n)
                self.assertEqual(list(group.iter(ns + 'circle')), [])
                break
            chunks = [(rank - step) % n for rank in range(n)]
            expected_packets = [f'{chr(65+c)}: {state[r][c]}' for r, c in enumerate(chunks)]
            self.assertEqual([t.text for t in group.iter(ns + 'text') if t.get('y') == '235'], expected_packets)
            circles = list(group.iter(ns + 'circle'))
            self.assertEqual(len(circles), n)
            for rank, circle in enumerate(circles):
                packet = circle.find(ns + 'animate')
                self.assertEqual(packet.get('dur'), f'{duration}s')
                self.assertEqual(packet.get('attributeName'), 'cx')
                begin, arrival = Fraction(2*step, duration), Fraction(20*step+18, 10*duration)
                times = list(map(Fraction, packet.get('keyTimes').split(';')))
                self.assertEqual(times, [Fraction(0)] + ([begin] if step else []) + [arrival, Fraction(1)])
                x0 = 22 + 120*rank
                self.assertEqual(list(map(int, packet.get('values').split(';'))), [x0] + ([x0] if step else []) + [x0+76, x0+76])
                self.assertLess(arrival, Fraction(2*(step+1), duration))
            previous = [row[:] for row in state]
            if step < n-1:
                for r, c in enumerate(chunks):
                    state[r][c] = None
                for r, c in enumerate(chunks):
                    receiver = (r+1) % n
                    state[receiver][c] = previous[receiver][c] + previous[r][c]
            else:
                for r, c in enumerate(chunks):
                    state[(r+1) % n][c] = previous[r][c]

    def test_overlap_activity_matches_common_cursor(self):
        from fractions import Fraction
        ns = v.NS
        root = ET.parse(ASSETS / 'interconnect-bucket-overlap-motion.svg').getroot()
        cursor = next(root.iter(ns + 'animateTransform'))
        end = Fraction(cursor.get('keyTimes').split(';')[1])
        # C1, C2 serial; N1, N2 serial; C1, C2 overlap; N1, N2 overlap.
        schedules = [(0,3), (3,6), (6,8), (8,10), (0,3), (3,6), (3,5), (6,8)]
        tracks = [a for a in root.iter(ns + 'animate') if a.get('attributeName') == 'fill-opacity']
        self.assertEqual(len(tracks), len(schedules))
        for a, (start, stop) in zip(tracks, schedules):
            self.assertEqual(a.get('dur'), cursor.get('dur'))
            times = list(map(Fraction, a.get('keyTimes').split(';')))
            values = list(map(Fraction, a.get('values').split(';')))
            self.assertEqual(times, [Fraction(0)] + ([end*start/10] if start else []) + [end*stop/10, Fraction(1)])
            self.assertEqual(values, ([Fraction(28,100)] if start else []) + [Fraction(1), Fraction(65,100), Fraction(65,100)])

if __name__ == '__main__':
    unittest.main()
