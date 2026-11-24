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
assert len(EXPECTED_CANVASES) == 431 and len(EXPECTED_EXTRAS) == 9 and len(EXPECTED_PREFIXES) == 28

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

# Independent arithmetic and state checks for DNN dataflow illustrations.
def dnn_dataflow_states(stem):
    root = ET.parse(ASSETS / f'{stem}-motion.svg').getroot()
    groups = [g for g in root.iter(v.NS + 'g') if g.get('id', '').startswith('state-')]
    assert len(groups) == 4
    for i, group in enumerate(groups):
        animation = group.find(v.NS + 'animate')
        assert group.get('opacity') == str(int(i == 0))
        assert animation.get('keyTimes') == '0;0.25;0.5;0.75;1'
        assert animation.get('values').split(';') == [str(int(i == j)) for j in (0, 1, 2, 3, 3)]
        assert animation.get('dur') == '12s'
        assert animation.get('repeatCount') == 'indefinite'
        assert animation.get('calcMode') == 'discrete'
    return groups


def dnn_dataflow_labels(node):
    return {(t.get('x'), t.get('y')): t.text for t in node.iter(v.NS + 'text')}


class DNNDataflowMotion(unittest.TestCase):
    def test_output_stationary_and_spill(self):
        stem = 'dnn-output-stationary-traffic'
        partial = 0
        for i, group in enumerate(dnn_dataflow_states(stem)):
            if i:
                partial += i * (i + 1)
            text = dnn_dataflow_labels(group)
            self.assertEqual(text['215', '159'], str(partial) if i < 3 else '—')
            self.assertEqual(text['485', '159'], str(partial) if i == 3 else '—')
            self.assertEqual(text['485', '257'], str(partial) if i else '—')
            self.assertEqual(text['270', '321'], f'Keep: {int(i == 3)}')
            self.assertEqual(text['480', '321'], f'Spill: {i + max(0, i - 1)}')
        still = dnn_dataflow_labels(ET.parse(ASSETS / f'{stem}-still.svg').getroot())
        self.assertEqual(still['485', '159'], str(partial))
        self.assertEqual(still['485', '257'], str(partial))
        self.assertEqual(still['480', '321'], 'Spill: 5')

    def test_overlapping_input_windows(self):
        stem = 'dnn-sliding-window-reuse'
        x, w = [1, 2, 3, 4, 5], [1, 2, 1]
        expected = [sum(a * b for a, b in zip(x[j:j+3], w)) for j in range(3)]
        prior = set()
        reads = 0
        for i, group in enumerate(dnn_dataflow_states(stem)):
            active = set(range(i - 1, i + 2)) if i else set()
            reads += len(active - prior)
            text = dnn_dataflow_labels(group)
            self.assertEqual(text['225', '302'], str(i * len(w)))
            self.assertEqual(text['515', '302'], str(reads))
            for j in range(3):
                self.assertEqual(text[str(219 + j * 98), '237'], str(expected[j]) if j < i else '—')
            cells = {int(r.get('x')): r for r in group.findall(v.NS + 'rect') if r.get('y') == '99'}
            for j in range(5):
                color = '#45DDC4' if j in active & prior else '#FFBD6A' if j in active else '#304361'
                self.assertEqual(cells[100 + j * 98].get('stroke'), color)
                cx = str(139 + j * 98)
                if j in active:
                    self.assertEqual(text[cx, '126'], str(x[j]))
                    self.assertEqual(text[cx, '152'], 'Keep' if j in prior else 'New')
                    self.assertEqual(text[cx, '194'], f'×{w[j - (i - 1)]}')
                else:
                    self.assertNotIn((cx, '152'), text)
                    self.assertNotIn((cx, '194'), text)
            prior = active
        still = dnn_dataflow_labels(ET.parse(ASSETS / f'{stem}-still.svg').getroot())
        self.assertEqual(still['225', '302'], '9')
        self.assertEqual(still['515', '302'], '5')
        for j in range(2, 5):
            cx = str(139 + j * 98)
            self.assertEqual(still[cx, '152'], 'Keep' if j < 4 else 'New')
            self.assertEqual(still[cx, '194'], f'×{w[j - 2]}')
        self.assertEqual([still[str(219 + j * 98), '237'] for j in range(3)], list(map(str, expected)))
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
