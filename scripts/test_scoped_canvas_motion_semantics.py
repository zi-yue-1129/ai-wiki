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
assert len(EXPECTED_CANVASES) == 429 and len(EXPECTED_EXTRAS) == 13 and len(EXPECTED_PREFIXES) == 28

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


    def assert_fp8_track(self, motion, still, tag, selector, attr, expected, duration):
        """Check actual SMIL values and the representative third-state fallback."""
        def select(root):
            matches = [node for node in root.iter(v.NS + tag)
                       if all(node.get(key) == value for key, value in selector.items())]
            self.assertEqual(len(matches), 1, (tag, selector))
            return matches[0]

        node = select(motion)
        tracks = [a for a in node.findall(v.NS + 'animate') if a.get('attributeName') == attr]
        self.assertEqual(len(tracks), 1, (selector, attr))
        track = tracks[0]
        self.assertEqual((track.get('dur'), track.get('calcMode'), track.get('repeatCount')),
                         (duration, 'discrete', 'indefinite'))
        self.assertIsNone(track.get('keyTimes'), 'These examples use equally spaced states')
        self.assertEqual([float(x) for x in track.get('values').split(';')], expected)
        self.assertEqual(float(select(still).get(attr)), expected[2])

    def test_fp8_rounding_tracks_follow_nearest_even_on_both_grids(self):
        stem = 'fp8-rounding-grid'
        motion, still = [ET.parse(ASSETS / f'{stem}-{kind}.svg').getroot()
                         for kind in ('motion', 'still')]
        inputs = [70 + 16 * i for i in range(17)]
        # i is an exact sixteenth; stride is the FP8 grid in sixteenths.
        # Python round uses ties-to-even and these binary fractions are exact.
        q4, q5 = [[70 + 16 * stride * round(i / stride) for i in range(17)]
                  for stride in (2, 4)]
        for y, expected in [(67, inputs), (131, q4), (195, q5)]:
            self.assert_fp8_track(motion, still, 'circle', {'cy': str(y)},
                                  'cx', expected, '8.5s')
        for y, output in [(117, q4), (181, q5)]:
            selector = {'y1': str(y), 'y2': str(y), 'stroke': '#ffbd6a'}
            self.assert_fp8_track(motion, still, 'line', selector, 'x1', inputs, '8.5s')
            self.assert_fp8_track(motion, still, 'line', selector, 'x2', output, '8.5s')
        guide = {'y1': '48', 'y2': '207', 'stroke-dasharray': '3 4'}
        for attr in ('x1', 'x2'):
            self.assert_fp8_track(motion, still, 'line', guide, attr, inputs, '8.5s')
        self.assertEqual([max(abs(x - y) for x, y in zip(inputs, q)) / 256
                          for q in (q4, q5)], [1/16, 1/8])

    def test_fp8_rounding_tie_candidates_follow_exact_midpoints(self):
        motion, still = [ET.parse(ASSETS / f'fp8-rounding-grid-{kind}.svg').getroot()
                         for kind in ('motion', 'still')]
        for stride, y in ((2, 131), (4, 195)):
            # Samples are exact sixteenths. Only half a grid step is a tie.
            visible = [int(i % stride == stride // 2) for i in range(17)]
            for side in (0, 1):
                selector = {'data-tie-grid': str(stride),
                            'data-tie-candidate': str(side)}
                candidates = [70 + 16 * min(16, stride * (i // stride + side)) - 9
                              for i in range(17)]
                self.assert_fp8_track(motion, still, 'rect', selector,
                                      'x', candidates, '8.5s')
                self.assert_fp8_track(motion, still, 'rect', selector,
                                      'opacity', visible, '8.5s')
                for root in (motion, still):
                    ring = next(n for n in root.iter(v.NS + 'rect')
                                if all(n.get(k) == val for k, val in selector.items()))
                    self.assertEqual((ring.get('y'), ring.get('width'), ring.get('height'),
                                      ring.get('fill'), ring.get('stroke-dasharray')),
                                     (str(y - 9), '18', '18', 'none', '3 2'))
            self.assert_fp8_track(motion, still, 'text', {'data-tie-label': str(stride)},
                                  'opacity', visible, '8.5s')

    def test_fp8_delayed_scaling_tracks_follow_the_previous_two_maxima(self):
        stem = 'fp8-delayed-amax'
        motion, still = [ET.parse(ASSETS / f'{stem}-{kind}.svg').getroot()
                         for kind in ('motion', 'still')]
        maxima = [1, 1, 4, 1, 1, 1]
        history = [1, 1] + maxima
        limits = [max(history[i:i+2]) for i in range(len(maxima))]
        self.assertEqual(limits, [1, 1, 1, 4, 4, 1])
        tracks = [
            ('rect', {'y': '43', 'stroke': '#fff'}, 'x',
             [58 + 47*i for i in range(len(maxima))]),
            ('rect', {'y': '129', 'fill': '#45ddc4'}, 'width', [60*a for a in maxima]),
            ('rect', {'y': '185', 'fill': '#45ddc4'}, 'width',
             [60*min(a, h) for a, h in zip(maxima, limits)]),
            ('rect', {'y': '185', 'fill': '#ffbd6a'}, 'width',
             [60*max(0, a-h) for a, h in zip(maxima, limits)]),
        ]
        for y, values in [(123, maxima), (179, limits)]:
            for attr in ('x1', 'x2'):
                tracks.append(('line', {'y1': str(y), 'stroke': '#fff'}, attr,
                               [82+60*a for a in values]))
        for tag, selector, attr, expected in tracks:
            self.assert_fp8_track(motion, still, tag, selector, attr, expected, '9s')

        # The purple history underlines must refer to the preceding two samples,
        # never the white-outlined current step. The first two bars are seeds.
        centers = [25, 43] + [74 + 47*i for i in range(len(maxima))]
        for offset in (0, 1):
            selected = centers[offset:offset+len(maxima)]
            selector = {'y1': '105', 'y2': '105', 'stroke': '#a993f9',
                        'x1': str(selected[2] - 6)}
            for attr, delta in [('x1', -6), ('x2', 6)]:
                self.assert_fp8_track(motion, still, 'line', selector, attr,
                                      [x+delta for x in selected], '9s')
        for root in (motion, still):
            for center in centers[:2]:
                seeds = [node for node in root.iter(v.NS + 'rect')
                         if node.get('x') == str(center-6) and node.get('y') == '71.5']
                self.assertEqual(len(seeds), 1)
                self.assertEqual((seeds[0].get('width'), seeds[0].get('height')), ('12', '7.5'))

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

class KernelTeachingStates(unittest.TestCase):
    def states(self, stem, n):
        root = ET.parse(ASSETS / f'{stem}-motion.svg').getroot()
        groups = root.findall(v.NS + 'g')
        self.assertEqual(len(groups), n)
        for i, group in enumerate(groups):
            self.assertEqual(group.get('id'), f'state-{i}')
            a = group.find(v.NS + 'animate')
            self.assertEqual(a.get('values').split(';'), [str(int(j % n == i)) for j in range(n + 1)])
            self.assertEqual(a.get('dur'), f'{2*n}s')
            for j, t in enumerate(a.get('keyTimes').split(';')):
                self.assertAlmostEqual(float(t), j/n, places=7)
        still = ET.parse(ASSETS / f'{stem}-still.svg').getroot()
        self.assertEqual([(e.get('x'), e.get('y'), e.text) for e in still.iter(v.NS + 'text')],
                         [(e.get('x'), e.get('y'), e.text) for e in groups[-1].iter(v.NS + 'text')])
        # The fallback must preserve shapes and styling as well as text.
        self.assertEqual([ET.tostring(e) for e in list(still)[3:]],
                         [ET.tostring(e) for e in list(groups[-1])[1:]])
        return groups

    def test_fusion_intermediate_traffic(self):
        groups = self.states('kernel-fusion-intermediate-traffic', 7)
        a, b = -3, 2
        tmp, out = a+b, max(a+b, 0)
        fmt = lambda value: str(value).replace('-', '−')
        for i, group in enumerate(groups):
            cells = {(float(e.get('x')), float(e.get('y'))): e.text for e in group.iter(v.NS + 'text')}
            for lane in (0, 1):
                x = 12 + 312*lane
                expected = sum(event <= i for event in ([1, 3, 4, 6] if lane == 0 else [1, 6]))
                self.assertEqual(cells[x+16,312], f'Transfers: {expected}')
                self.assertEqual(cells[x+56,161.5], fmt(a))
                self.assertEqual(cells[x+152,161.5], fmt(tmp) if lane == 0 and i>=3 else '–')
                self.assertEqual(cells[x+248,161.5], fmt(out) if i==6 else '–')
                local = '–' if i==0 or (lane==0 and i==3) else fmt(a if i==1 else tmp if i<5 else out)
                self.assertEqual(cells[x+152,248], local)

    def test_tail_tile_masks_and_outputs(self):
        groups = self.states('triton-tail-mask', 6)
        N, B = 6, 4
        for i, group in enumerate(groups):
            cells = {(float(e.get('x')), float(e.get('y'))): e.text for e in group.iter(v.NS + 'text')}
            pid, stage = divmod(i, 3)
            stored = 0
            for k in range(2*B):
                active = k//B == pid
                valid = k < N
                loaded = active and stage >= 1 and valid
                done = valid and (k//B < pid or (active and stage == 2))
                stored += done
                expected = [str(k), str(int(valid)) if k//B <= pid else '–', str(k+1) if loaded else '–', str(2*(k+1)) if loaded else '–', str(2*(k+1)) if done else '–']
                for row, value in enumerate(expected):
                    self.assertEqual(cells[152+k*63,95+row*47], value)
            self.assertEqual(cells[14,321], f'Valid stores: {stored} / {N}')


if __name__ == '__main__':
    unittest.main()
