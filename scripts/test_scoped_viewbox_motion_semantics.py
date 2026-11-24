"""Keep original ECE/ensemble and flow-specific canvas contracts fail-closed."""
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET
import verify_concept_motion as validator

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'docs/assets/concept-animations'
EXPECTED = {
    'ece-binned-calibration': '0 0 720 400',
    'deep-ensemble-spread': '0 0 720 400',
    'cfm-conditional-bridge': '0 0 760 410',
    'rectified-reflow-coupling': '0 0 760 410',
}
PREVIOUS_GLOBAL = {'0 0 640 360', '0 0 720 400', '0 0 720 460', '0 0 760 410', '0 0 800 420'}

class Scope(unittest.TestCase):
    def test_eight_correct_source_assets(self):
        for stem, expected in EXPECTED.items():
            for kind in ('motion', 'still'):
                path = ASSETS / f'{stem}-{kind}.svg'
                with self.subTest(path=path.name):
                    self.assertEqual(ET.parse(path).getroot().get('viewBox'), expected)
                    self.assertEqual(validator.verify_svg(path, kind == 'motion'), [])

    def test_all_32_formerly_allowed_wrong_canvas_mutations(self):
        count = 0
        with tempfile.TemporaryDirectory() as directory:
            for stem, expected in EXPECTED.items():
                for kind in ('motion', 'still'):
                    for wrong in PREVIOUS_GLOBAL - {expected}:
                        with self.subTest(stem=stem, kind=kind, wrong=wrong):
                            root = ET.parse(ASSETS / f'{stem}-{kind}.svg').getroot()
                            root.set('viewBox', wrong)
                            path = Path(directory) / f'{stem}-{kind}.svg'
                            ET.ElementTree(root).write(path, encoding='unicode')
                            errors = validator.verify_svg(path, kind == 'motion')
                            self.assertTrue(any('invalid SVG root/viewBox' in error for error in errors), errors)
                            count += 1
        self.assertEqual(count, 32)

    def test_original_prefix_scope_includes_related_named_variants(self):
        with tempfile.TemporaryDirectory() as directory:
            for stem in EXPECTED:
                root = ET.parse(ASSETS / f'{stem}-still.svg').getroot()
                root.set('viewBox', '0 0 640 360')
                path = Path(directory) / f'{stem}-variant-still.svg'
                ET.ElementTree(root).write(path, encoding='unicode')
                self.assertTrue(any('invalid SVG root/viewBox' in error for error in validator.verify_svg(path, False)))

    def test_every_other_registered_source_remains_valid(self):
        for stem in validator.TOPICS:
            if stem in EXPECTED:
                continue
            for kind in ('motion', 'still'):
                path = ASSETS / f'{stem}-{kind}.svg'
                with self.subTest(path=path.name):
                    self.assertEqual(validator.verify_svg(path, kind == 'motion'), [])

if __name__ == '__main__':
    unittest.main()
