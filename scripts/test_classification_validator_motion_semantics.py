"""Guard shared-validator contracts preserved while merging classification work."""
import ast
import tempfile
import xml.etree.ElementTree as ET
from verify_concept_motion import verify_svg, TOPICS, ASSETS
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ValidatorPreservation(unittest.TestCase):
    def test_existing_canvas_and_static_fallback_contracts_remain(self):
        tree = ast.parse((ROOT / "scripts/verify_concept_motion.py").read_text())
        # Fixed expected canvas inventory, not inferred from validator implementation.
        exceptions = {'0 0 860 440': ['s4d-diagonal-modes', 'mamba2-ssd-causal-map', 'layernorm-feature-shift', 'seq2seq-context-handoff'], '0 0 800 420': ['gradient-clipping-comparison', 'gradient-accumulation-clipping-order', 'gradient-global-layer-budget', 'gradient-amp-unscale-order', 'gradient-agc-relative-cap', 'gradient-decoupled-decay', 'ddim-eta-coefficients', 'rf-bootstrap-oob', 'rf-feature-subset', 'enas-shared-weight-transfer', 'mnasnet-latency-tradeoff', 'score-sde-flow', 'consistency-trajectory-map', 'itemcf-weighted-neighbors', 'neumf-dual-path', 'resnet-identity-gradient', 'resnet-projection-shortcut', 'resnet-postrelu-gate', 'resnet-depth-gradient-factors', 'ar-score-vs-sample', 'ar-likelihood-accumulation', 'ar-context-drift', 'ar-eos-survival', 'svd-rank-accumulation', 'svd-noise-amplification', 'svd-ls-orthogonal-residual', 'svd-degenerate-bases', 'eigen-linear-map', 'eigen-rotation-no-real', 'eigen-zero-eigenvalue', 'eigen-jordan-shear', 'adam-bias-correction', 'adam-scale-invariance', 'adam-sign-reversal', 'adam-epsilon-threshold', 'hmm-forward-sum-product', 'hmm-filter-smooth', 'hmm-pairwise-posterior', 'hmm-baum-welch-transition', '3d-unet-depth-kernel', '3d-unet-skip-concat', '3d-unet-context-tiling', '3d-unet-paired-warp', '3d-unet-sparse-loss', '3d-unet-evaluation-holdout', 'kmeans-plusplus-d2', 'kmeans-outlier-leverage', 'kmeans-feature-scale', 'kmeans-elbow-inertia', 'mf-coupled-sgd', 'bpr-pairwise-ranking', 'mf-als-alternating', 'bpr-gradient-saturation'], '0 0 760 400': ['reinforce-return-credit', 'grpo-group-advantages'], '0 0 760 420': ['sac-entropy-temperature', 'dpo-preference-margin'], '0 0 800 460': ['roi-align-sampling', 'sam-prompt-ambiguity'], '0 0 800 440': ['vivit-factorised-attention', 'i3d-filter-inflation'], '0 0 800 436': ['video-joint-denoising', 'latent-space-denoise'], '0 0 720 400': ['ece-binned-calibration', 'deep-ensemble-spread'], '0 0 760 410': ['cfm-conditional-bridge', 'rectified-reflow-coupling'], '0 0 720 460': ['adagrad-coordinate-gain', 'adafactor-factored-moments'], '0 0 860 464': ['ucb1-optimism-switch', 'ucb1-bonus-sensitivity', 'thompson-beta-posterior-draws', 'thompson-evidence-concentration'], '0 0 640 322': ['flashattention-online-rescale', 'flashattention-exact-merge'], '0 0 800 430': ['backdoor-standardisation', 'collider-selection']}
        expected = {stem: box for box, stems in exceptions.items() for stem in stems}
        with tempfile.TemporaryDirectory() as directory:
            for stem in TOPICS:
                box = expected.get(stem, "0 0 640 360")
                for suffix, animated in (("motion", True), ("still", False)):
                    path = ROOT / ASSETS / f"{stem}-{suffix}.svg"
                    root = ET.parse(path).getroot()
                    with self.subTest(stem=stem, suffix=suffix):
                        self.assertEqual(root.get("viewBox"), box)
                        self.assertEqual(verify_svg(path, animated), [])
                        root.set("viewBox", "0 0 641 361")
                        wrong = Path(directory) / path.name
                        ET.ElementTree(root).write(wrong)
                        self.assertTrue(any("invalid SVG root/viewBox" in e
                                            for e in verify_svg(wrong, animated)))
            # Special families must not accidentally accept a globally legal default size.
            for stem in ("sac-entropy-temperature", "dpo-preference-margin",
                         "vivit-factorised-attention", "i3d-filter-inflation",
                         "s4d-diagonal-modes", "mamba2-ssd-causal-map"):
                root = ET.parse(ROOT / ASSETS / f"{stem}-still.svg").getroot()
                root.set("viewBox", "0 0 640 360")
                wrong = Path(directory) / f"{stem}-still.svg"
                ET.ElementTree(root).write(wrong)
                self.assertTrue(any("invalid SVG root/viewBox" in e
                                    for e in verify_svg(wrong, False)), stem)
        # Exercise the real guard on every formerly permitted canvas. A valid
        # canvas for one topic must not be accepted for unrelated geometry.
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
