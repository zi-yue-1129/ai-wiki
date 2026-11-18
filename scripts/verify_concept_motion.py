#!/usr/bin/env python3
"""Validate SVG teaching assets and accessible bilingual GIF/static fallbacks.

stdlib-only check; rendered/browser validation is performed separately.
"""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from xml.etree import ElementTree as ET

DOCS = Path("docs")
ASSETS = DOCS / "assets" / "concept-animations"
NS = "{http://www.w3.org/2000/svg}"
TOPICS = {
    "ucb1-optimism-switch": "theory/paradigms/online/stochastic-bandits/index",
    "ucb1-bonus-sensitivity": "theory/paradigms/online/stochastic-bandits/index",
    "thompson-beta-posterior-draws": "theory/paradigms/online/stochastic-bandits/index",
    "thompson-evidence-concentration": "theory/paradigms/online/stochastic-bandits/index",

    "ece-binned-calibration": "theory/paradigms/probabilistic/uncertainty-calibration/expected-calibration-error",
    "deep-ensemble-spread": "theory/paradigms/probabilistic/uncertainty-calibration/deep-ensembles",
    "tsne-kl-embedding": "theory/paradigms/unsupervised/dimensionality-reduction/t-sne",
    "umap-fuzzy-union": "theory/paradigms/unsupervised/dimensionality-reduction/umap",
    "minhash-lsh-band-collision": "engineering/data/minhash-deduplication",
    "weak-supervision-vote-fusion": "engineering/data/data-programming",
    "cfm-conditional-bridge": "theory/paradigms/unsupervised/density-and-generative-models/flow/flow-matching/conditional-flow-matching",
    "rectified-reflow-coupling": "theory/paradigms/unsupervised/density-and-generative-models/flow/flow-matching/rectified-flow",
    "clr-triangular2-sweep": "theory/optimization/cyclical-learning-rates",
    "lion-sign-momentum": "theory/optimization/adaptive/lion",
    "muon-spectral-balancing": "theory/optimization/adaptive/muon",
    "lars-layer-trust-scaling": "theory/optimization/lars",
    "lamb-adam-layer-trust": "theory/optimization/lamb",
    "checkpoint-recompute": "engineering/hardware/co-design/gradient-checkpointing",
    "fp16-loss-scaling": "engineering/hardware/co-design/mixed-precision",
    "effective-number-growth": "theory/paradigms/supervised/loss-functions-and-optimization/class-balanced-loss",
    "logit-prior-decision": "theory/paradigms/supervised/loss-functions-and-optimization/logit-adjustment",
    "roofline-ridge-sweep": "engineering/hardware/memory-hierarchy/roofline",
    "fp8-scale-range": "engineering/hardware/co-design/fp8",
    "roc-threshold-sweep": "theory/evaluation/metrics/classification/roc-auc",
    "pr-threshold-sweep": "theory/evaluation/metrics/classification/pr-auc",
    "dpr-dot-product-sweep": "engineering/vector-databases/dense-passage-retrieval",
    "colbert-maxsim-switch": "engineering/vector-databases/colbert",
    "paired-bootstrap-resampling": "theory/evaluation/protocols/methods/paired-bootstrap",
    "elo-online-update": "theory/evaluation/protocols/methods/elo-rating",
    "grid-search-x-coverage": "theory/optimization/hyperparameter-optimisation/grid-search",
    "random-search-x-coverage": "theory/optimization/hyperparameter-optimisation/random-search",
    "group-norm-statistics": "theory/deep-learning/normalisation/group-normalisation",
    "rmsnorm-shift-response": "theory/deep-learning/normalisation/rms-normalisation",
    "svm-margin-hinge": "theory/paradigms/supervised/kernel-methods-svm/svm",
    "cv-fold-rotation": "theory/evaluation/protocols/methods/cross-validation",
    "ndcg-position-discount": "theory/evaluation/metrics/ranking/ndcg",
    "map-precision-at-hits": "theory/evaluation/metrics/ranking/map",
    "heavy-ball-overshoot": "theory/optimization/sgd-and-momentum/heavy-ball",
    "sgd-noise-batch": "theory/optimization/sgd-noise-scale",
    "adagrad-coordinate-gain": "theory/optimization/adaptive/adagrad",
    "adafactor-factored-moments": "theory/optimization/adaptive/adafactor",
    "sharpness-reparam-curvature": "theory/optimization/sharp-minima",
    "sharpness-radius-loss": "theory/optimization/sharp-minima",
    "itemcf-weighted-neighbors": "theory/models/recommender/item-based-cf",
    "neumf-dual-path": "theory/models/recommender/neural-cf",
    "resnet-identity-gradient": "theory/models/cnn/backbones-and-scaling/resnet/index",
    "resnet-projection-shortcut": "theory/models/cnn/backbones-and-scaling/resnet/index",
    "resnet-postrelu-gate": "theory/models/cnn/backbones-and-scaling/resnet/index",
    "resnet-depth-gradient-factors": "theory/models/cnn/backbones-and-scaling/resnet/index",
    "mixup-paired-interpolation": "theory/deep-learning/dropout/mixup",
    "mixup-beta-strength": "theory/deep-learning/dropout/mixup",
    "mixup-loss-decomposition": "theory/deep-learning/dropout/mixup",
    "mixup-cutmix-area": "theory/deep-learning/dropout/mixup",
    "outlier-mae-rmse": "theory/evaluation/metrics/regression/mae",
    "r2-mean-baseline": "theory/evaluation/metrics/regression/r-squared",
    "ar-score-vs-sample": "theory/paradigms/unsupervised/density-and-generative-models/autoregressive/index",
    "ar-likelihood-accumulation": "theory/paradigms/unsupervised/density-and-generative-models/autoregressive/index",
    "ar-context-drift": "theory/paradigms/unsupervised/density-and-generative-models/autoregressive/index",
    "ar-eos-survival": "theory/paradigms/unsupervised/density-and-generative-models/autoregressive/index",
    "svd-unit-circle": "theory/math/linear-algebra/svd",
    "svd-rank-accumulation": "theory/math/linear-algebra/svd",
    "svd-noise-amplification": "theory/math/linear-algebra/svd",
    "svd-ls-orthogonal-residual": "theory/math/linear-algebra/svd",
    "svd-degenerate-bases": "theory/math/linear-algebra/svd",
    "power-iteration-convergence": "theory/math/linear-algebra/eigendecomposition",
    "eigen-linear-map": "theory/math/linear-algebra/eigendecomposition",
    "eigen-rotation-no-real": "theory/math/linear-algebra/eigendecomposition",
    "eigen-zero-eigenvalue": "theory/math/linear-algebra/eigendecomposition",
    "eigen-jordan-shear": "theory/math/linear-algebra/eigendecomposition",
    "mae-visible-patch-reconstruction": "theory/paradigms/self-supervised/masked-prediction/mae",
    "dinov2-dual-objective-ema": "theory/paradigms/self-supervised/non-contrastive-methods/dinov2",
    "moco-dictionary-cycle": "theory/paradigms/self-supervised/contrastive-learning/moco",
    "byol-online-target": "theory/paradigms/self-supervised/non-contrastive-methods/byol",
    "gibbs-coordinate-sweeps": "theory/paradigms/probabilistic/mcmc/gibbs-sampling",
    "mean-field-coordinate-ascent": "theory/paradigms/probabilistic/variational-inference/mean-field",
    "moe-top2-routing": "theory/models/mixture-of-experts/index",
    "cfg-extrapolation": "theory/paradigms/unsupervised/density-and-generative-models/diffusion/classifier-free-guidance",
    "gradient-norm-clipping": "theory/optimization/norm-clipping",
    "swin-shifted-windows": "theory/models/transformer/vision-transformer/swin/index",
    "deformable-sampling": "theory/models/cnn/convolution-variants/deformable-convolution/index",
    "speculative-decoding": "engineering/inference-optimization/speculative-decoding",
    "orca-continuous-batching": "engineering/inference-optimization/orca",
    "disaggregated-handoff": "engineering/inference-optimization/disaggregated-serving",
    "streaming-kv-eviction": "engineering/inference-optimization/kv-cache-compression",
    "mcts-search-cycle": "theory/paradigms/reinforcement-learning/mcts-and-self-play/index",
    "dqn-target-sync": "theory/paradigms/reinforcement-learning/deep-q-networks/index",
    "adamw-decoupled-paths": "theory/optimization/adaptive/adamw",
    "adam-bias-correction": "theory/optimization/adaptive/adam",
    "adam-scale-invariance": "theory/optimization/adaptive/adam",
    "adam-sign-reversal": "theory/optimization/adaptive/adam",
    "adam-epsilon-threshold": "theory/optimization/adaptive/adam",
    "td3-delayed-twin-critics": "theory/paradigms/reinforcement-learning/policy-gradient-and-actor-critic/td3/index",
    "ppo-clipped-objective": "theory/paradigms/reinforcement-learning/proximal-policy-optimisation/index",
    "prioritized-replay-cycle": "theory/paradigms/reinforcement-learning/experience-replay/index",
    "sam-two-gradient": "theory/optimization/sharpness-aware-minimisation",
    "lbfgs-two-loop": "theory/optimization/lbfgs",
    "nesterov-lookahead": "theory/optimization/sgd-and-momentum/nesterov",
    "hyperband-budget": "theory/optimization/hyperparameter-optimisation/hyperband",
    "bo-gp-conditioning": "theory/optimization/hyperparameter-optimisation/bayesian-optimisation",
    "bo-expected-improvement": "theory/optimization/hyperparameter-optimisation/bayesian-optimisation",
    "qmix-monotonic-greedy": "theory/paradigms/reinforcement-learning/multi-agent-rl/qmix/index",
    "muzero-latent-planning": "theory/paradigms/reinforcement-learning/model-based-rl/muzero/index",
    "gru-gate-flow": "theory/models/rnn/gated-cells/gru/index",
    "kfac-factor-preconditioning": "theory/optimization/kfac/index",
    "maml-inner-outer-loop": "theory/paradigms/meta-learning/optimisation-based/maml",
    "alpha-beta-cutoff": "theory/paradigms/symbolic-ai/search/alpha-beta-pruning",
    "cmaes-distribution-adaptation": "theory/optimization/cma-es",
    "spsa-two-evaluations": "theory/optimization/spsa",
    "batch-norm-train-infer": "theory/deep-learning/normalisation/batch-normalisation",
    "stochastic-depth-paths": "theory/deep-learning/dropout/stochastic-depth",
    "dropout-inverted-sampling": "theory/deep-learning/dropout/dropout-method",
    "dropout-variance-tradeoff": "theory/deep-learning/dropout/dropout-method",
    "dropblock-spatial-masking": "theory/deep-learning/dropout/dropout-method",
    "mc-dropout-repeated-passes": "theory/deep-learning/dropout/index",
    "stochastic-depth-survival-samples": "theory/deep-learning/dropout/stochastic-depth",
    "stochastic-depth-scaling-conventions": "theory/deep-learning/dropout/stochastic-depth",
    "vae-reparameterisation": "theory/paradigms/unsupervised/density-and-generative-models/vae/index",
    "realnvp-affine-coupling": "theory/paradigms/unsupervised/density-and-generative-models/flow/normalising-flows/realnvp",
    "mh-accept-reject": "theory/paradigms/probabilistic/mcmc/metropolis-hastings",
    "hmc-leapfrog-trajectory": "theory/paradigms/probabilistic/mcmc/hamiltonian-monte-carlo",
    "astar-frontier": "theory/paradigms/symbolic-ai/search/a-star",
    "dpll-backtrack": "theory/paradigms/symbolic-ai/theorem-proving/dpll",
    "hmm-forward-sum-product": "theory/paradigms/probabilistic/graphical-models/hidden-markov-models",
    "hmm-filter-smooth": "theory/paradigms/probabilistic/graphical-models/hidden-markov-models",
    "hmm-pairwise-posterior": "theory/paradigms/probabilistic/graphical-models/hidden-markov-models",
    "hmm-baum-welch-transition": "theory/paradigms/probabilistic/graphical-models/hidden-markov-models",
    "viterbi-trellis": "theory/paradigms/probabilistic/graphical-models/hidden-markov-models",
    "tree-belief-propagation": "theory/paradigms/probabilistic/graphical-models/belief-propagation",
    "3d-unet-depth-kernel": "theory/models/cnn/unet/3d-unet",
    "3d-unet-skip-concat": "theory/models/cnn/unet/3d-unet",
    "3d-unet-orthogonal-slices": "theory/models/cnn/unet/3d-unet",
    "3d-unet-sparse-context-gradient": "theory/models/cnn/unet/3d-unet",
    "3d-unet-context-tiling": "theory/models/cnn/unet/3d-unet",
    "3d-unet-paired-warp": "theory/models/cnn/unet/3d-unet",
    "3d-unet-sparse-loss": "theory/models/cnn/unet/3d-unet",
    "3d-unet-evaluation-holdout": "theory/models/cnn/unet/3d-unet",
    "forward-ad-jvp": "theory/math/automatic-differentiation/forward-mode",
    "reverse-ad-vjp": "theory/math/automatic-differentiation/reverse-mode",
    "gcn-aggregation": "theory/models/gnn/message-passing/gcn/index",
    "gat-aggregation": "theory/models/gnn/message-passing/gat/index",
    "gin-multiset-counts": "theory/models/gnn/message-passing/gin/index",
    "graphsage-sample-aggregate": "theory/models/gnn/message-passing/graphsage/index",
    "kmeans-lloyd": "theory/paradigms/unsupervised/clustering/k-means",
    "qk-norm-scale-sweep": "theory/models/transformer/qk-norm",
    "sigma-reparam-spectral-gain": "theory/models/transformer/sigma-reparam",
    "kmeans-plusplus-d2": "theory/paradigms/unsupervised/clustering/k-means",
    "kmeans-outlier-leverage": "theory/paradigms/unsupervised/clustering/k-means",
    "kmeans-feature-scale": "theory/paradigms/unsupervised/clustering/k-means",
    "kmeans-elbow-inertia": "theory/paradigms/unsupervised/clustering/k-means",
    "pca-variance-axis": "theory/paradigms/unsupervised/dimensionality-reduction/pca",
    "pca-rank1-reconstruction": "theory/paradigms/unsupervised/dimensionality-reduction/pca",
    "rmsprop-adaptive-memory": "theory/optimization/adaptive/rmsprop",
    "mf-coupled-sgd": "theory/models/recommender/matrix-factorization",
    "bpr-pairwise-ranking": "theory/models/recommender/bpr",
    "mf-als-alternating": "theory/models/recommender/matrix-factorization",
    "bpr-gradient-saturation": "theory/models/recommender/bpr",
    "bpe-ordered-merges": "theory/models/llm/tokenisation/byte-pair-encoding",
    "mle-bernoulli-likelihood": "theory/math/probability-statistics/maximum-likelihood",
    "map-beta-posterior": "theory/math/probability-statistics/maximum-a-posteriori",
    "nerf-volume-rendering": "theory/models/computer-vision/3d-and-neural-rendering/nerf",
    "iou-overlap-sweep": "theory/evaluation/metrics/segmentation/iou",
    "dice-overlap-response": "theory/evaluation/metrics/segmentation/dice",
}
GITHUB_GIF_PREVIEWS = {
    "moco-dictionary-cycle": "moco-momentum-preview.gif",
    "byol-online-target": "byol-momentum-preview.gif",
}
FORBIDDEN = {"script", "foreignObject", "iframe", "image"}
LIMIT = 50 * 1024


class MotionImages(HTMLParser):
    def __init__(self, text: str):
        super().__init__()
        self.images: list[dict[str, str | None]] = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            attributes = {}
            for name, value in attrs:
                attributes.setdefault(name, value)
            self.images.append(attributes)


def verify_source_pair(page: Path, text: str, stem: str) -> list[str]:
    """Check raw opt-in images in source coordinates, never built URL depths."""
    images = [attrs for attrs in MotionImages(text).images
              if "data-source-asset-urls" in attrs
              and stem in (attrs.get("src") or "")]
    if len(images) != 1:
        return [f"{page}: expected one source-relative raw image for {stem}"]
    errors = []
    for attribute, kind in (("src", "still"), ("data-motion-src", "motion"),
                            ("data-still-src", "still")):
        value = images[0].get(attribute)
        expected = (ASSETS / f"{stem}-{kind}.svg").resolve()
        if not value or (page.parent / value).resolve() != expected:
            errors.append(f"{page}: {attribute} must reference the source-relative {kind} asset")
    return errors


def verify_svg(path: Path, animated: bool) -> list[str]:
    errors = []
    if not path.is_file():
        return [f"{path}: missing"]
    if path.stat().st_size > LIMIT:
        errors.append(f"{path}: exceeds {LIMIT} bytes")
    try:
        root = ET.parse(path).getroot()
    except (ET.ParseError, OSError) as exc:
        return [f"{path}: invalid XML: {exc}"]
    if root.tag != NS + "svg" or root.get("viewBox") not in {"0 0 860 464", "0 0 640 360", "0 0 720 400", "0 0 720 460", "0 0 760 410", "0 0 800 420"}:
        errors.append(f"{path}: invalid SVG root/viewBox")
    for label in ("title", "desc"):
        if root.find(NS + label) is None:
            errors.append(f"{path}: missing accessible {label}")
    motions = []
    for element in root.iter():
        name = element.tag.split("}")[-1]
        if name in FORBIDDEN:
            errors.append(f"{path}: prohibited {name}")
        if name in ("animate", "animateMotion", "animateTransform"):
            motions.append(element)
            if element.get("repeatCount") != "indefinite":
                errors.append(f"{path}: animation must loop indefinitely")
            if not element.get("dur", "").endswith("s"):
                errors.append(f"{path}: animation requires a duration in seconds")
        for key, value in element.attrib.items():
            local_key = key.split("}")[-1]
            if local_key.startswith("on"):
                errors.append(f"{path}: event handler prohibited")
            if local_key == "href" and (
                "://" in value or value.startswith(("data:", "javascript:"))
            ):
                errors.append(f"{path}: external or active asset reference")
    if animated and not motions:
        errors.append(f"{path}: no animation found")
    if not animated and motions:
        errors.append(f"{path}: still fallback contains animation")
    return errors


def main() -> int:
    errors = []
    for stem, page_stem in TOPICS.items():
        animated_path = ASSETS / f"{stem}-motion.svg"
        static_path = ASSETS / f"{stem}-still.svg"
        errors.extend(verify_svg(animated_path, True))
        errors.extend(verify_svg(static_path, False))
        if stem == "moe-top2-routing":
            errors.extend(verify_svg(ASSETS / "moe-top2-routing-token-b.svg", False))
        for suffix in (".md", ".zh-TW.md"):
            page = DOCS / (page_stem + suffix)
            if not page.is_file():
                errors.append(f"{page}: missing translation")
                continue
            text = page.read_text(encoding="utf-8")
            links = re.findall(r"!\[[^]]+\]\(([^)]+\.svg)\)", text)
            linked_images = {(page.parent / link).resolve() for link in links}
            if stem in {"iou-overlap-sweep", "dice-overlap-response"}:
                # GitHub gets the static image; MkDocs enhances it via data-motion-src.
                match = re.search(r'<img\s+data-source-asset-urls\s+[^>]*src="([^"]+)"\s+data-motion-src="([^"]+)"', text)
                if not match:
                    errors.append(f"{page}: missing source-relative HTML static/motion pair")
                else:
                    still_link, motion_link = match.groups()
                    if (page.parent / still_link).resolve() != static_path.resolve():
                        errors.append(f"{page}: invalid GitHub static fallback")
                    if (page.parent / motion_link).resolve() != animated_path.resolve():
                        errors.append(f"{page}: invalid MkDocs motion link")
            elif stem in {"cfm-conditional-bridge", "deep-ensemble-spread", "ece-binned-calibration", "hmm-baum-welch-transition", "hmm-filter-smooth", "hmm-forward-sum-product", "hmm-pairwise-posterior", "lion-sign-momentum", "muon-spectral-balancing", "qk-norm-scale-sweep", "rectified-reflow-coupling", "sigma-reparam-spectral-gain", "tsne-kl-embedding", "umap-fuzzy-union"}:
                errors.extend(verify_source_pair(page, text, stem))
            elif stem in {"itemcf-weighted-neighbors", "neumf-dual-path"}:
                errors.extend(verify_source_pair(page, text, stem))
                static_links = re.findall(r"\[[^]]+\]\(([^)]+\.svg)\)", text)
                if static_path.resolve() not in {
                    (page.parent / link).resolve() for link in static_links
                }:
                    errors.append(f"{page}: missing GitHub-readable fallback link for {stem}")
            elif stem in GITHUB_GIF_PREVIEWS:
                # These topics now teach via a controllable JS lab, not the
                # legacy four-stage SVG. GitHub shows the static overview and
                # links to the reviewed, continuously animated GIF preview.
                if static_path.resolve() not in linked_images:
                    errors.append(f"{page}: missing static overview image")
                gif_path = ASSETS / GITHUB_GIF_PREVIEWS[stem]
                gif_links = re.findall(r"\[[^]]+\]\(([^)]+\.gif)\)", text)
                if gif_path.resolve() not in {
                    (page.parent / link).resolve() for link in gif_links
                }:
                    errors.append(f"{page}: missing linked continuous GIF preview")
            elif stem in {"ucb1-optimism-switch", "ucb1-bonus-sensitivity", "thompson-beta-posterior-draws", "thompson-evidence-concentration", "adafactor-factored-moments", "adagrad-coordinate-gain", "adam-bias-correction", "adam-epsilon-threshold", "adam-scale-invariance", "adam-sign-reversal", "bo-expected-improvement", "bo-gp-conditioning", "bpr-gradient-saturation", "bpr-pairwise-ranking", "checkpoint-recompute", "clr-triangular2-sweep", "colbert-maxsim-switch", "cv-fold-rotation", "dpr-dot-product-sweep", "dropblock-spatial-masking", "dropout-inverted-sampling", "dropout-variance-tradeoff", "effective-number-growth", "eigen-jordan-shear", "eigen-linear-map", "eigen-rotation-no-real", "eigen-zero-eigenvalue", "elo-online-update", "fp16-loss-scaling", "fp8-scale-range", "gin-multiset-counts", "graphsage-sample-aggregate", "grid-search-x-coverage", "group-norm-statistics", "heavy-ball-overshoot", "lamb-adam-layer-trust", "lars-layer-trust-scaling", "logit-prior-decision", "map-beta-posterior", "map-precision-at-hits", "mc-dropout-repeated-passes", "mf-als-alternating", "mf-coupled-sgd", "minhash-lsh-band-collision", "mixup-beta-strength", "mixup-cutmix-area", "mixup-loss-decomposition", "mixup-paired-interpolation", "mle-bernoulli-likelihood", "ndcg-position-discount", "outlier-mae-rmse", "paired-bootstrap-resampling", "pr-threshold-sweep", "r2-mean-baseline", "random-search-x-coverage", "resnet-depth-gradient-factors", "resnet-identity-gradient", "resnet-postrelu-gate", "resnet-projection-shortcut", "rmsnorm-shift-response", "roc-threshold-sweep", "roofline-ridge-sweep", "sgd-noise-batch", "sharpness-radius-loss", "sharpness-reparam-curvature", "stochastic-depth-scaling-conventions", "stochastic-depth-survival-samples", "svm-margin-hinge", "weak-supervision-vote-fusion",
                          "svd-unit-circle", "svd-rank-accumulation", "svd-noise-amplification", "svd-ls-orthogonal-residual", "svd-degenerate-bases", "power-iteration-convergence",
                          "kmeans-plusplus-d2", "kmeans-outlier-leverage", "kmeans-feature-scale", "kmeans-elbow-inertia",
                          "ar-score-vs-sample", "ar-likelihood-accumulation", "ar-context-drift", "ar-eos-survival",
                          "3d-unet-depth-kernel", "3d-unet-paired-warp", "3d-unet-sparse-loss", "3d-unet-evaluation-holdout", "3d-unet-skip-concat", "3d-unet-context-tiling", "3d-unet-orthogonal-slices", "3d-unet-sparse-context-gradient"}:
                # GitHub uses the raw static image; the opt-in hook rewrites
                # all three source-relative attributes for each built locale.
                errors.extend(verify_source_pair(page, text, stem))
                if stem in {"adam-bias-correction", "adam-scale-invariance", "adam-sign-reversal", "adam-epsilon-threshold", "mf-coupled-sgd", "bpr-pairwise-ranking", "mf-als-alternating", "bpr-gradient-saturation", "resnet-identity-gradient", "resnet-projection-shortcut", "resnet-postrelu-gate", "resnet-depth-gradient-factors", "eigen-linear-map", "eigen-rotation-no-real", "svd-unit-circle", "svd-rank-accumulation", "svd-noise-amplification", "svd-ls-orthogonal-residual", "svd-degenerate-bases", "power-iteration-convergence"}:
                    static_links = re.findall(r"\[[^]]+\]\(([^)]+\.svg)\)", text)
                    if static_path.resolve() not in {
                        (page.parent / link).resolve() for link in static_links
                    }:
                        errors.append(f"{page}: missing GitHub-readable static link")
            elif animated_path.resolve() not in linked_images:
                errors.append(f"{page}: missing or incorrect animated SVG link")
            if stem in {'3d-unet-context-tiling', '3d-unet-depth-kernel', '3d-unet-evaluation-holdout', '3d-unet-orthogonal-slices', '3d-unet-paired-warp', '3d-unet-skip-concat', '3d-unet-sparse-context-gradient', '3d-unet-sparse-loss', 'adamw-decoupled-paths', 'alpha-beta-cutoff', 'astar-frontier', 'batch-norm-train-infer', 'bpe-ordered-merges', 'byol-online-target', 'cmaes-distribution-adaptation', 'deformable-sampling', 'dinov2-dual-objective-ema', 'disaggregated-handoff', 'dpll-backtrack', 'dqn-target-sync', 'forward-ad-jvp', 'gat-aggregation', 'gcn-aggregation', 'gibbs-coordinate-sweeps', 'gru-gate-flow', 'hmc-leapfrog-trajectory', 'hyperband-budget', 'kfac-factor-preconditioning', 'kmeans-lloyd', 'lbfgs-two-loop', 'lion-sign-momentum', 'mae-visible-patch-reconstruction', 'maml-inner-outer-loop', 'mcts-search-cycle', 'mean-field-coordinate-ascent', 'mh-accept-reject', 'moco-dictionary-cycle', 'moe-top2-routing', 'muon-spectral-balancing', 'muzero-latent-planning', 'nerf-volume-rendering', 'nesterov-lookahead', 'orca-continuous-batching', 'ppo-clipped-objective', 'prioritized-replay-cycle', 'qk-norm-scale-sweep', 'qmix-monotonic-greedy', 'realnvp-affine-coupling', 'reverse-ad-vjp', 'rmsprop-adaptive-memory', 'sam-two-gradient', 'sigma-reparam-spectral-gain', 'speculative-decoding', 'spsa-two-evaluations', 'stochastic-depth-paths', 'streaming-kv-eviction', 'swin-shifted-windows', 'td3-delayed-twin-critics', 'tree-belief-propagation', 'tsne-kl-embedding', 'umap-fuzzy-union', 'vae-reparameterisation', 'viterbi-trellis'}:
                static_links = re.findall(r"\[[^]]+\]\(([^)]+\.svg)\)", text)
                linked = {(page.parent / link).resolve() for link in static_links}
                fallbacks = (static_path, ASSETS / "moe-top2-routing-token-b.svg") if stem == "moe-top2-routing" else (static_path,)
                for fallback in fallbacks:
                    if fallback.resolve() not in linked:
                        errors.append(f"{page}: missing GitHub-readable fallback link {fallback.name}")
            if stem in {"dropout-inverted-sampling", "stochastic-depth-survival-samples", "dropout-variance-tradeoff", "stochastic-depth-scaling-conventions", "dropblock-spatial-masking", "mc-dropout-repeated-passes"}:
                # Both languages must expose a GitHub-safe static fallback.
                static_links = re.findall(r"\[[^]]+\]\(([^)]+\.svg)\)", text)
                if static_path.resolve() not in {
                    (page.parent / link).resolve() for link in static_links
                }:
                    errors.append(f"{page}: missing GitHub static fallback for {stem}")
            if "CC BY-SA 4.0" not in text:
                errors.append(f"{page}: missing original-diagram attribution")
        print(
            f"Motion pair {stem}: "
            f"{animated_path.stat().st_size if animated_path.exists() else '-'} / "
            f"{static_path.stat().st_size if static_path.exists() else '-'} bytes"
        )
    # GitHub's static previews and MkDocs's bilingual motion enhancement.
    for stem, page in {
        "brier-expected-risk": "brier-score",
        "log-loss-tail-penalty": "log-loss",
    }.items():
        moving = ASSETS / f"{stem}-motion.svg"
        still = ASSETS / f"{stem}-still.svg"
        errors.extend(verify_svg(moving, True))
        errors.extend(verify_svg(still, False))
        for locale in (".md", ".zh-TW.md"):
            doc = DOCS / "theory/evaluation/metrics/probabilistic" / (page + locale)
            if not doc.is_file():
                errors.append(f"{doc}: missing translation")
                continue
            body = doc.read_text(encoding="utf-8")
            errors.extend(verify_source_pair(doc, body, stem))
            relative = "../../../../assets/concept-animations/"
            if f'src="{relative}{still.name}"' not in body:
                errors.append(f"{doc}: missing actual GitHub static image src")
            if f'data-motion-src="{relative}{moving.name}"' not in body:
                errors.append(f"{doc}: missing animated source")
            if f'data-still-src="{relative}{still.name}"' not in body:
                errors.append(f"{doc}: missing reduced-motion fallback")
            if "CC BY-SA 4.0" not in body:
                errors.append(f"{doc}: missing original-art attribution")
    # MAE and RMSE share one source-relative visual in both languages.
    for suffix in (".md", ".zh-TW.md"):
        page = DOCS / ("theory/evaluation/metrics/regression/rmse" + suffix)
        errors.extend(verify_source_pair(page, page.read_text(encoding="utf-8"), "outlier-mae-rmse"))

    # The two reviewed process animations must show interpolated intermediate states,
    # not four discrete slides masquerading as motion.
    for stem in ("mae-visible-patch-reconstruction", "dinov2-dual-objective-ema"):
        root = ET.parse(ASSETS / f"{stem}-motion.svg").getroot()
        animations = [node for node in root.iter() if node.tag == NS + "animate"]
        if len(animations) < 10 or any(node.get("calcMode") == "discrete" for node in animations):
            errors.append(f"{stem}: continuous interpolation required; discrete slides are not sufficient")

    config = Path("mkdocs.yml").read_text(encoding="utf-8")
    for path in (
        "javascripts/concept-motion.js",
        "stylesheets/concept-motion.css",
        "javascripts/concept-motion-detailed.js",
        "stylesheets/concept-motion-detailed.css",
    ):
        if path not in config or not (DOCS / path).exists():
            errors.append(f"Missing registered player asset: {path}")
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    print(f"Checked {len(TOPICS)} motion/still pairs and bilingual pages: {len(errors)} error(s)")
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
