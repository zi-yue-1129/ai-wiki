"""Guard shared-validator contracts preserved while merging classification work."""
import ast
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ValidatorPreservation(unittest.TestCase):
    def test_existing_canvas_and_static_fallback_contracts_remain(self):
        tree = ast.parse((ROOT / "scripts/verify_concept_motion.py").read_text())
        comparisons = [
            node for node in ast.walk(tree)
            if isinstance(node, ast.Compare)
            and len(node.comparators) == 1
            and isinstance(node.comparators[0], ast.Set)
        ]
        viewboxes = [
            set(ast.literal_eval(node.comparators[0]))
            for node in comparisons
            if isinstance(node.left, ast.Call)
            and any(isinstance(arg, ast.Constant) and arg.value == "viewBox"
                    for arg in node.left.args)
        ]
        self.assertEqual(len(viewboxes), 1)
        self.assertTrue({"0 0 640 360", "0 0 720 460", "0 0 800 420",
                         "0 0 720 400"} <= viewboxes[0])
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
