"""Guard shared-validator contracts preserved while merging classification work."""
import ast
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ValidatorPreservation(unittest.TestCase):
    def test_existing_canvas_and_static_fallback_contracts_remain(self):
        tree = ast.parse((ROOT / "scripts/verify_concept_motion.py").read_text())
        # Exercise the real guard on every formerly permitted canvas. A valid
        # canvas for one topic must not be accepted for unrelated geometry.
        import tempfile
        from xml.etree import ElementTree as ET
        import verify_concept_motion as validator
        representatives = {}
        for stem, box in validator.CANONICAL_VIEWBOXES.items():
            representatives.setdefault(box, stem)
        self.assertTrue({"0 0 640 360", "0 0 720 460", "0 0 800 420",
                         "0 0 720 400"} <= set(representatives))
        with tempfile.TemporaryDirectory() as td:
            for box, stem in representatives.items():
                source = ROOT / f"docs/assets/concept-animations/{stem}-still.svg"
                self.assertEqual(validator.verify_svg(source, False), [])
                root = ET.parse(source).getroot()
                for other in set(representatives) - {box}:
                    root.set("viewBox", other)
                    path = Path(td) / source.name
                    path.write_bytes(ET.tostring(root))
                    self.assertTrue(any("viewBox" in e for e in validator.verify_svg(path, False)))
        # The branch enforcing static preview links must retain both QK topics.
        checked = []
        for node in ast.walk(tree):
            if not isinstance(node, ast.If):
                continue
            body = ast.unparse(ast.Module(body=node.body, type_ignores=[]))
            if "missing GitHub-readable fallback link" not in body:
                continue
            test = node.test
            if (isinstance(test, ast.Compare) and isinstance(test.left, ast.Name)
                    and test.left.id == "stem"
                    and isinstance(test.comparators[0], ast.Set)):
                checked.append(set(ast.literal_eval(test.comparators[0])))
        self.assertTrue(any({"qk-norm-scale-sweep", "sigma-reparam-spectral-gain"}
                            <= group for group in checked))


if __name__ == "__main__":
    unittest.main()
