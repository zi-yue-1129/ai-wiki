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
    "hnsw-layer-descent": "engineering/vector-databases/hnsw",
    "ivfpq-probe-pq-lookup": "engineering/vector-databases/ivf-pq-faiss",
    "forest-bootstrap-vote": "theory/paradigms/supervised/trees-and-ensembles/random-forests",
    "boosting-residual-steps": "theory/paradigms/supervised/trees-and-ensembles/gradient-boosting",
    "rf-bootstrap-oob": "theory/paradigms/supervised/trees-and-ensembles/random-forests",
    "rf-feature-subset": "theory/paradigms/supervised/trees-and-ensembles/random-forests",
    "darts-soft-operations": "theory/deep-learning/nas-automl/darts",
    "aging-evolution-queue": "theory/deep-learning/nas-automl/regularized-evolution",
    "enas-shared-weight-transfer": "theory/deep-learning/nas-automl/efficient-neural-architecture-search",
    "mnasnet-latency-tradeoff": "theory/deep-learning/nas-automl/mnasnet",
    "newton-curvature-steps": "theory/math/calculus/newtons-method",
    "newton-indefinite-curvature": "theory/math/calculus/newtons-method",
    "newton-armijo-backtracking": "theory/math/calculus/newtons-method",
    "lagrange-tangency": "theory/math/calculus/lagrange-multipliers",
    "lagrange-dual-gap": "theory/math/calculus/lagrange-multipliers",
    "lagrange-kkt-active-set": "theory/math/calculus/lagrange-multipliers",
    "gated-sae-gate-magnitude": "society/interpretability/gated-sae",
    "jumprelu-threshold-jump": "society/interpretability/jumprelu-sae",
    "wgan-weight-clip": "theory/paradigms/unsupervised/density-and-generative-models/gan/wgan",
    "wgan-gp-interpolation": "theory/paradigms/unsupervised/density-and-generative-models/gan/wgan-gp",
    "ant-colony-pheromone": "theory/paradigms/evolutionary/ant-colony",
    "particle-swarm-best": "theory/paradigms/evolutionary/particle-swarm",
    "qat-fake-quant-ste": "theory/model-compression/quantisation/quantisation-aware-training/index",
    "lsq-step-size-sweep": "theory/model-compression/quantisation/quantisation-aware-training/lsq/index",
    "react-evidence-loop": "engineering/agents/react",
    "reflexion-memory-feedback": "engineering/agents/reflexion",
    "ida-bound-reexpansion": "theory/paradigms/symbolic-ai/search/ida-star",
    "resolution-refutation-chain": "theory/paradigms/symbolic-ai/theorem-proving/resolution",
    "dora-independent": "theory/model-compression/low-rank-and-efficient-architectures/lora/dora",
    "qlora-frozen-flow": "theory/model-compression/low-rank-and-efficient-architectures/lora/qlora",
    "unigram-viterbi-lattice": "theory/models/llm/tokenisation/sentencepiece",
    "unigram-sampling-alpha": "theory/models/llm/tokenisation/sentencepiece",
    "odin-gradient-perturbation": "theory/machine-learning/ood-detection/odin",
    "mahalanobis-ellipse-threshold": "theory/machine-learning/ood-detection/mahalanobis-distance",
    "asam-neighborhood": "theory/optimization/asam",
    "shampoo-eigenmode": "theory/optimization/shampoo",
    "glorot-alternating-width": "theory/deep-learning/initialisation/glorot-initialisation",
    "glorot-equal-variance-densities": "theory/deep-learning/initialisation/glorot-initialisation",
    "glorot-fan-tradeoff": "theory/deep-learning/initialisation/glorot-initialisation",
    "glorot-tanh-saturation": "theory/deep-learning/initialisation/glorot-initialisation",
    "he-fan-mode-tradeoff": "theory/deep-learning/initialisation/he-initialisation",
    "he-relu-mean-shift": "theory/deep-learning/initialisation/he-initialisation",
    "he-relu-second-moment": "theory/deep-learning/initialisation/he-initialisation",
    "mup-adam-sgd": "theory/deep-learning/initialisation/mup",
    "mup-readout-aggregation": "theory/deep-learning/initialisation/mup",
    "mup-readout-noise": "theory/deep-learning/initialisation/mup",
    "mup-transfer-protocol": "theory/deep-learning/initialisation/mup",
    "mup-transfer-validation": "theory/deep-learning/initialisation/mup",
    "mup-update-budget": "theory/deep-learning/initialisation/mup",
    "mup-width-multipliers": "theory/deep-learning/initialisation/mup",
    "prelu-slope-gain": "theory/deep-learning/initialisation/he-initialisation",
    "rotational-norm-balance": "theory/optimization/weight-norm-dynamics/rotational-equilibrium",
    "adamw-epoch-timescale": "theory/optimization/weight-norm-dynamics/adamw-weight-decay-scaling",
    "paged-block-mapping": "engineering/inference-optimization/paged-attention",
    "expert-cache-miss": "engineering/inference-optimization/expert-offloading",
    "ece-binned-calibration": "theory/paradigms/probabilistic/uncertainty-calibration/expected-calibration-error",
    "deep-ensemble-spread": "theory/paradigms/probabilistic/uncertainty-calibration/deep-ensembles",
    "tsne-kl-embedding": "theory/paradigms/unsupervised/dimensionality-reduction/t-sne",
    "umap-fuzzy-union": "theory/paradigms/unsupervised/dimensionality-reduction/umap",
    "minhash-lsh-band-collision": "engineering/data/minhash-deduplication",
    "weak-supervision-vote-fusion": "engineering/data/data-programming",
    "cfm-conditional-bridge": "theory/paradigms/unsupervised/density-and-generative-models/flow/flow-matching/conditional-flow-matching",
    "rectified-reflow-coupling": "theory/paradigms/unsupervised/density-and-generative-models/flow/flow-matching/rectified-flow",
    "clr-triangular2-sweep": "theory/optimization/cyclical-learning-rates",
    "gin-multiset-counts": "theory/models/gnn/message-passing/gin/index",
    "graphsage-sample-aggregate": "theory/models/gnn/message-passing/graphsage/index",
    "qk-norm-scale-sweep": "theory/models/transformer/qk-norm",
    "sigma-reparam-spectral-gain": "theory/models/transformer/sigma-reparam",
    "roc-pr-shift": "theory/evaluation/metrics/classification/roc-auc",
    "roc-youden-cost": "theory/evaluation/metrics/classification/roc-auc",
    "roc-cost-operating-point": "theory/evaluation/metrics/classification/roc-auc",
    "pr-random-ap-expectation": "theory/evaluation/metrics/classification/pr-auc",
    "roc-tie-half-credit": "theory/evaluation/metrics/classification/roc-auc",
    "f1-threshold-topk": "theory/evaluation/metrics/classification/f1",
    "roc-randomized-operating-mix": "theory/evaluation/metrics/classification/roc-auc",
    "pr-ap-tied-threshold": "theory/evaluation/metrics/classification/pr-auc",
    "roc-pairwise-auc": "theory/evaluation/metrics/classification/roc-auc",
    "pr-ap-rectangles": "theory/evaluation/metrics/classification/pr-auc",
    "precision-recall-threshold": "theory/evaluation/metrics/classification/precision",
    "f1-harmonic-gap": "theory/evaluation/metrics/classification/f1",
    "accuracy-prevalence": "theory/evaluation/metrics/classification/accuracy",
    "fbeta-recall-emphasis": "theory/evaluation/metrics/classification/f1",
    "precision-base-rate": "theory/evaluation/metrics/classification/precision",
    "f1-macro-micro-imbalance": "theory/evaluation/metrics/classification/f1",
    "roc-partial-area": "theory/evaluation/metrics/classification/roc-auc",
    "roc-rank-transform": "theory/evaluation/metrics/classification/roc-auc",
    "auc-ap-ranking-contrast": "theory/evaluation/metrics/classification/pr-auc",
    "pr-ap-trapezoid-gap": "theory/evaluation/metrics/classification/pr-auc",
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
    "kmeans-lloyd": "theory/paradigms/unsupervised/clustering/k-means",
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
# Canvas contracts are review-time literals, never inferred from the SVG under test.
# Every new TOPICS entry must explicitly declare its reviewed geometry here.
CANONICAL_VIEWBOXES = {
    '3d-unet-context-tiling': '0 0 800 420',  # origin 9ab22a24338e92717d61e54e33f9c8b04b588033
    '3d-unet-depth-kernel': '0 0 800 420',  # origin 9ab22a24338e92717d61e54e33f9c8b04b588033
    '3d-unet-evaluation-holdout': '0 0 800 420',  # origin 9ab22a24338e92717d61e54e33f9c8b04b588033
    '3d-unet-orthogonal-slices': '0 0 640 360',  # origin 9ab22a24338e92717d61e54e33f9c8b04b588033
    '3d-unet-paired-warp': '0 0 800 420',  # origin 9ab22a24338e92717d61e54e33f9c8b04b588033
    '3d-unet-skip-concat': '0 0 800 420',  # origin 9ab22a24338e92717d61e54e33f9c8b04b588033
    '3d-unet-sparse-context-gradient': '0 0 640 360',  # origin 9ab22a24338e92717d61e54e33f9c8b04b588033
    '3d-unet-sparse-loss': '0 0 800 420',  # origin 9ab22a24338e92717d61e54e33f9c8b04b588033
    'accuracy-prevalence': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'adafactor-factored-moments': '0 0 720 460',  # origin 43a57b80f5174aacd6c7675d51ec77c353a06fa2
    'adagrad-coordinate-gain': '0 0 720 460',  # origin 43a57b80f5174aacd6c7675d51ec77c353a06fa2
    'adam-bias-correction': '0 0 800 420',  # origin fd91f1c27f1427dac41731911fb93f5f4612388c
    'adam-epsilon-threshold': '0 0 800 420',  # origin 019e0d1b66d382cbe33d5d6a7b396ce0c3fdedba
    'adam-scale-invariance': '0 0 800 420',  # origin fd91f1c27f1427dac41731911fb93f5f4612388c
    'adam-sign-reversal': '0 0 800 420',  # origin 019e0d1b66d382cbe33d5d6a7b396ce0c3fdedba
    'adamw-decoupled-paths': '0 0 640 360',  # origin 5378eb9fe6f826d1f15ce934e7589b2facb915ed
    'adamw-epoch-timescale': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'aging-evolution-queue': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'alpha-beta-cutoff': '0 0 640 360',  # origin 4c4bfba7df3919ca11f77d9aa766be434878bdf0
    'ant-colony-pheromone': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'ar-context-drift': '0 0 800 420',  # origin a3fc0fb64052cd9c9a08039f59cfae0858b9e6ec,4e8feb76eda11c3e6d15a935f1a40b7de47fa7a6
    'ar-eos-survival': '0 0 800 420',  # origin 1f77bd440fbe818a9f0c5469ee8d489a3d65b291,39bec660675136ecc45e2c1654e258457cfb4aa0
    'ar-likelihood-accumulation': '0 0 800 420',  # origin e21d44e6af6e7776c8219ad0106d6ee23a95c5a5
    'ar-score-vs-sample': '0 0 800 420',  # origin e21d44e6af6e7776c8219ad0106d6ee23a95c5a5
    'asam-neighborhood': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'astar-frontier': '0 0 640 360',  # origin f7337cf2638f3c1ff1532e7f718aabac0865d28b
    'auc-ap-ranking-contrast': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'batch-norm-train-infer': '0 0 640 360',  # origin 255f92a3054b761cd178a1ec18a8d9e50d602d37
    'bo-expected-improvement': '0 0 640 360',  # origin 740965999012f3cd02c0b99ab0433fe165d23b4e
    'bo-gp-conditioning': '0 0 640 360',  # origin 740965999012f3cd02c0b99ab0433fe165d23b4e
    'boosting-residual-steps': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'bpe-ordered-merges': '0 0 640 360',  # origin b6f21f5f932d3eda532f7e743af087c20ead0870
    'bpr-gradient-saturation': '0 0 800 420',  # origin d63a71d59848759b91a71fe36ad6b96f764a9dc6
    'bpr-pairwise-ranking': '0 0 800 420',  # origin d1919fd73d05deb6f56ee7676fbdd63e658af355
    'byol-online-target': '0 0 640 360',  # origin 331d15f34b9f6772d986afeec1e928819f1b1f97
    'cfg-extrapolation': '0 0 640 360',  # origin 5875288b4c31f3ceb3fde5beaa67e1c4e07a6090
    'cfm-conditional-bridge': '0 0 760 410',  # origin c028c848a3e1e3d7013ae6ca35aaa9f9e2ced3d8
    'checkpoint-recompute': '0 0 640 360',  # origin c0924f0d4a260fdf4922a36c83ccb6c7c24990f2
    'clr-triangular2-sweep': '0 0 640 360',  # origin 4b9f79e116755c0070af9e803fcb0bb62f67bbb0
    'cmaes-distribution-adaptation': '0 0 640 360',  # origin d2c84dd00777ae7d0eea3ea38a13012146a4b1a5
    'colbert-maxsim-switch': '0 0 640 360',  # origin 25770e6b084eaeba6998b658780caa03c96b2c48
    'cv-fold-rotation': '0 0 640 360',  # origin 6695c6a7b352d64f98f511d2aa3fcf6edcf867bc
    'darts-soft-operations': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'deep-ensemble-spread': '0 0 720 400',  # origin 4a611378445ea5c5396a3488f71c4e374b2c939e
    'deformable-sampling': '0 0 640 360',  # origin e00a7dd21eca5336c9865027674000f7578521dc
    'dice-overlap-response': '0 0 640 360',  # origin 7c472a8dba6dd3a39ac74d438840ca27e1d8be3a
    'dinov2-dual-objective-ema': '0 0 640 360',  # origin dec6fcf99253875a1a6ff8508acf458c2d0b5085
    'disaggregated-handoff': '0 0 640 360',  # origin 1d54c4ae36eff5a4df7bb9587a2e0580ff5636ee
    'dora-independent': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'dpll-backtrack': '0 0 640 360',  # origin f7337cf2638f3c1ff1532e7f718aabac0865d28b
    'dpr-dot-product-sweep': '0 0 640 360',  # origin 25770e6b084eaeba6998b658780caa03c96b2c48
    'dqn-target-sync': '0 0 640 360',  # origin 0f1ccb332c13f2d7d72faaf2394d9d173d8f665a
    'dropblock-spatial-masking': '0 0 640 360',  # origin e434dff16b781d0facc56afa5840a4681dfedfd8
    'dropout-inverted-sampling': '0 0 640 360',  # origin eee699618afdae1909247586f288d49418006b66
    'dropout-variance-tradeoff': '0 0 640 360',  # origin b193cbd6879d351863724768390f9fadbc29d0c3,e450f3aeae496a8012a8e8e3b3bc5e8a348257fd
    'ece-binned-calibration': '0 0 720 400',  # origin 4a611378445ea5c5396a3488f71c4e374b2c939e
    'effective-number-growth': '0 0 640 360',  # origin 4fada4af8d68a02c30cfa9ddbd51d3d393a11f89
    'eigen-jordan-shear': '0 0 800 420',  # origin 15bdb38e1c312b578f4e4e41a4b96f483433e989
    'eigen-linear-map': '0 0 800 420',  # origin 19e3913d7aba853b2f10d1652ff6b6c1e1f6117f
    'eigen-rotation-no-real': '0 0 800 420',  # origin 19e3913d7aba853b2f10d1652ff6b6c1e1f6117f
    'eigen-zero-eigenvalue': '0 0 800 420',  # origin 15bdb38e1c312b578f4e4e41a4b96f483433e989
    'elo-online-update': '0 0 640 360',  # origin f7aefbad4b5af2090a85c4100e96326b34f25056
    'enas-shared-weight-transfer': '0 0 800 420',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'expert-cache-miss': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'f1-harmonic-gap': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'f1-macro-micro-imbalance': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'f1-threshold-topk': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'fbeta-recall-emphasis': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'forest-bootstrap-vote': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'forward-ad-jvp': '0 0 640 360',  # origin a8432b46ebe9a070935048402bdfcb6cb1442809
    'fp16-loss-scaling': '0 0 640 360',  # origin c0924f0d4a260fdf4922a36c83ccb6c7c24990f2
    'fp8-scale-range': '0 0 640 360',  # origin 67e4091c01b3f94b8e6fbfbeb4511d0a93971f39
    'gat-aggregation': '0 0 640 360',  # origin e2a78cc8d9c9e4f41393adecadc968c50e2a2912
    'gated-sae-gate-magnitude': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'gcn-aggregation': '0 0 640 360',  # origin e2a78cc8d9c9e4f41393adecadc968c50e2a2912
    'gibbs-coordinate-sweeps': '0 0 640 360',  # origin 39a25d3105b805ff71c44932982e0d5b5e5a3dba
    'gin-multiset-counts': '0 0 640 360',  # origin 4a611378445ea5c5396a3488f71c4e374b2c939e
    'glorot-alternating-width': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'glorot-equal-variance-densities': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'glorot-fan-tradeoff': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'glorot-tanh-saturation': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'gradient-norm-clipping': '0 0 640 360',  # origin 5875288b4c31f3ceb3fde5beaa67e1c4e07a6090
    'graphsage-sample-aggregate': '0 0 640 360',  # origin 4a611378445ea5c5396a3488f71c4e374b2c939e
    'grid-search-x-coverage': '0 0 640 360',  # origin 75080f86df360900362cc3c04fa2680194e1d0cf
    'group-norm-statistics': '0 0 640 360',  # origin 1b96705ef3e52dcad0fc061c8660305102de904d
    'gru-gate-flow': '0 0 640 360',  # origin 269c6767663de40b11c8bad3c9ebd40fb8bd8ca3
    'he-fan-mode-tradeoff': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'he-relu-mean-shift': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'he-relu-second-moment': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'heavy-ball-overshoot': '0 0 640 360',  # origin 20ab47cef45a7a5895987dc456f51c4d437912a5
    'hmc-leapfrog-trajectory': '0 0 640 360',  # origin b3f965ab18f3cb57c91a8d488857581d0e544748
    'hmm-baum-welch-transition': '0 0 800 420',  # origin 326513cb81d57184e3857da9a83017bc75f37039
    'hmm-filter-smooth': '0 0 800 420',  # origin 620ee6d9d94415967d694b0e87c284b1223e5ebb
    'hmm-forward-sum-product': '0 0 800 420',  # origin 620ee6d9d94415967d694b0e87c284b1223e5ebb
    'hmm-pairwise-posterior': '0 0 800 420',  # origin 326513cb81d57184e3857da9a83017bc75f37039
    'hnsw-layer-descent': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'hyperband-budget': '0 0 640 360',  # origin 0ca80d62237ba8063b37f07eff2648e545af5387
    'ida-bound-reexpansion': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'iou-overlap-sweep': '0 0 640 360',  # origin 7c472a8dba6dd3a39ac74d438840ca27e1d8be3a
    'itemcf-weighted-neighbors': '0 0 800 420',  # origin 12577fa11e8638d3ae3a26a74656dc162f8190c5
    'ivfpq-probe-pq-lookup': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'jumprelu-threshold-jump': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'kfac-factor-preconditioning': '0 0 640 360',  # origin 269c6767663de40b11c8bad3c9ebd40fb8bd8ca3
    'kmeans-elbow-inertia': '0 0 800 420',  # origin 53d6c5d17c6102c294ca716a345bebdfd379d455
    'kmeans-feature-scale': '0 0 800 420',  # origin 53d6c5d17c6102c294ca716a345bebdfd379d455
    'kmeans-lloyd': '0 0 640 360',  # origin b6f21f5f932d3eda532f7e743af087c20ead0870
    'kmeans-outlier-leverage': '0 0 800 420',  # origin 743cc54ed4de3af9bef0a06fa1e020aced6337eb
    'kmeans-plusplus-d2': '0 0 800 420',  # origin 743cc54ed4de3af9bef0a06fa1e020aced6337eb
    'lagrange-dual-gap': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'lagrange-kkt-active-set': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'lagrange-tangency': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'lamb-adam-layer-trust': '0 0 640 360',  # origin a11018eea3dad5a2a5623b263e4db13859719341
    'lars-layer-trust-scaling': '0 0 640 360',  # origin a11018eea3dad5a2a5623b263e4db13859719341
    'lbfgs-two-loop': '0 0 640 360',  # origin 7b8fd624643589fcf0ccca7f08706f06e7cb5b39
    'lion-sign-momentum': '0 0 640 360',  # origin 1083b195b9f48a497775b45c1de11e5104082001
    'logit-prior-decision': '0 0 640 360',  # origin 4fada4af8d68a02c30cfa9ddbd51d3d393a11f89
    'lsq-step-size-sweep': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'mae-visible-patch-reconstruction': '0 0 640 360',  # origin dec6fcf99253875a1a6ff8508acf458c2d0b5085
    'mahalanobis-ellipse-threshold': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'maml-inner-outer-loop': '0 0 640 360',  # origin 4c4bfba7df3919ca11f77d9aa766be434878bdf0
    'map-beta-posterior': '0 0 640 360',  # origin 1790e581b761fe90871b4e590328b5e004a14e3e
    'map-precision-at-hits': '0 0 640 360',  # origin 7b8d8d6ecbdf8057cba16b1f27fee9ddee61dda9
    'mc-dropout-repeated-passes': '0 0 640 360',  # origin e434dff16b781d0facc56afa5840a4681dfedfd8
    'mcts-search-cycle': '0 0 640 360',  # origin 0f1ccb332c13f2d7d72faaf2394d9d173d8f665a
    'mean-field-coordinate-ascent': '0 0 640 360',  # origin 39a25d3105b805ff71c44932982e0d5b5e5a3dba
    'mf-als-alternating': '0 0 800 420',  # origin d63a71d59848759b91a71fe36ad6b96f764a9dc6
    'mf-coupled-sgd': '0 0 800 420',  # origin d1919fd73d05deb6f56ee7676fbdd63e658af355
    'mh-accept-reject': '0 0 640 360',  # origin b3f965ab18f3cb57c91a8d488857581d0e544748
    'minhash-lsh-band-collision': '0 0 640 360',  # origin c028c848a3e1e3d7013ae6ca35aaa9f9e2ced3d8
    'mixup-beta-strength': '0 0 640 360',  # origin 197cb82e931330a8ecbc918601ff5cabb4953314
    'mixup-cutmix-area': '0 0 640 360',  # origin 155c657a631dd76ed375778d19e556ba8a68efb1
    'mixup-loss-decomposition': '0 0 640 360',  # origin 155c657a631dd76ed375778d19e556ba8a68efb1
    'mixup-paired-interpolation': '0 0 640 360',  # origin 197cb82e931330a8ecbc918601ff5cabb4953314
    'mle-bernoulli-likelihood': '0 0 640 360',  # origin 1790e581b761fe90871b4e590328b5e004a14e3e
    'mnasnet-latency-tradeoff': '0 0 800 420',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'moco-dictionary-cycle': '0 0 640 360',  # origin 331d15f34b9f6772d986afeec1e928819f1b1f97
    'moe-top2-routing': '0 0 640 360',  # origin 5875288b4c31f3ceb3fde5beaa67e1c4e07a6090
    'muon-spectral-balancing': '0 0 640 360',  # origin 1083b195b9f48a497775b45c1de11e5104082001
    'mup-adam-sgd': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'mup-readout-aggregation': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'mup-readout-noise': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'mup-transfer-protocol': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'mup-transfer-validation': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'mup-update-budget': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'mup-width-multipliers': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'muzero-latent-planning': '0 0 640 360',  # origin c1057975ae7734354fa2e335b1ea0dea67fbb356
    'ndcg-position-discount': '0 0 640 360',  # origin 7b8d8d6ecbdf8057cba16b1f27fee9ddee61dda9
    'nerf-volume-rendering': '0 0 640 360',  # origin b6f21f5f932d3eda532f7e743af087c20ead0870
    'nesterov-lookahead': '0 0 640 360',  # origin 0ca80d62237ba8063b37f07eff2648e545af5387
    'neumf-dual-path': '0 0 800 420',  # origin 12577fa11e8638d3ae3a26a74656dc162f8190c5
    'newton-armijo-backtracking': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'newton-curvature-steps': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'newton-indefinite-curvature': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'odin-gradient-perturbation': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'orca-continuous-batching': '0 0 640 360',  # origin af2ed229649acd6e2699911860c52a161fcc304b
    'outlier-mae-rmse': '0 0 640 360',  # origin 3f85643dd79a62b8b104350a41b9a2ea77262d88
    'paged-block-mapping': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'paired-bootstrap-resampling': '0 0 640 360',  # origin f7aefbad4b5af2090a85c4100e96326b34f25056
    'particle-swarm-best': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'pca-rank1-reconstruction': '0 0 640 360',  # origin 38f8a0ffdaba8ee78383cf1b5d8671507e971d44
    'pca-variance-axis': '0 0 640 360',  # origin 38f8a0ffdaba8ee78383cf1b5d8671507e971d44
    'power-iteration-convergence': '0 0 640 360',  # origin e2abf17856e1fd83746aaf12f8fd5119d6f0d40e
    'ppo-clipped-objective': '0 0 640 360',  # origin 69563b42b0f35762ff2500253396ddef91064993
    'pr-ap-rectangles': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'pr-ap-tied-threshold': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'pr-ap-trapezoid-gap': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'pr-random-ap-expectation': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'pr-threshold-sweep': '0 0 640 360',  # origin a8dae56d1f71737396ac4be1836092be8c8d5393
    'precision-base-rate': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'precision-recall-threshold': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'prelu-slope-gain': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'prioritized-replay-cycle': '0 0 640 360',  # origin 69563b42b0f35762ff2500253396ddef91064993
    'qat-fake-quant-ste': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'qk-norm-scale-sweep': '0 0 640 360',  # origin 4a611378445ea5c5396a3488f71c4e374b2c939e
    'qlora-frozen-flow': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'qmix-monotonic-greedy': '0 0 640 360',  # origin c1057975ae7734354fa2e335b1ea0dea67fbb356
    'r2-mean-baseline': '0 0 640 360',  # origin 3f85643dd79a62b8b104350a41b9a2ea77262d88
    'random-search-x-coverage': '0 0 640 360',  # origin 75080f86df360900362cc3c04fa2680194e1d0cf
    'react-evidence-loop': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'realnvp-affine-coupling': '0 0 640 360',  # origin 83c4115c9a0a88e9659169d136db7107410f4b66
    'rectified-reflow-coupling': '0 0 760 410',  # origin c028c848a3e1e3d7013ae6ca35aaa9f9e2ced3d8
    'reflexion-memory-feedback': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'resnet-depth-gradient-factors': '0 0 800 420',  # origin 262db96efe99958dda65bb7e3a320ef6fe38430e
    'resnet-identity-gradient': '0 0 800 420',  # origin 72e0b1a5550f470df4fbce109dce8094a5e4e109
    'resnet-postrelu-gate': '0 0 800 420',  # origin 262db96efe99958dda65bb7e3a320ef6fe38430e
    'resnet-projection-shortcut': '0 0 800 420',  # origin 72e0b1a5550f470df4fbce109dce8094a5e4e109
    'resolution-refutation-chain': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'reverse-ad-vjp': '0 0 640 360',  # origin a8432b46ebe9a070935048402bdfcb6cb1442809
    'rf-bootstrap-oob': '0 0 800 420',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'rf-feature-subset': '0 0 800 420',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'rmsnorm-shift-response': '0 0 640 360',  # origin 1b96705ef3e52dcad0fc061c8660305102de904d
    'rmsprop-adaptive-memory': '0 0 640 360',  # origin b6f21f5f932d3eda532f7e743af087c20ead0870
    'roc-pr-shift': '0 0 640 360',  # reviewed original prevalence-shift motion and still
    'roc-youden-cost': '0 0 640 360',  # reviewed original cost-sweep motion and still
    'roc-cost-operating-point': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'roc-pairwise-auc': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'roc-partial-area': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'roc-randomized-operating-mix': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'roc-rank-transform': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'roc-threshold-sweep': '0 0 640 360',  # origin a8dae56d1f71737396ac4be1836092be8c8d5393
    'roc-tie-half-credit': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'roofline-ridge-sweep': '0 0 640 360',  # origin 67e4091c01b3f94b8e6fbfbeb4511d0a93971f39
    'rotational-norm-balance': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'sam-two-gradient': '0 0 640 360',  # origin 7b8fd624643589fcf0ccca7f08706f06e7cb5b39
    'sgd-noise-batch': '0 0 640 360',  # origin 20ab47cef45a7a5895987dc456f51c4d437912a5
    'shampoo-eigenmode': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'sharpness-radius-loss': '0 0 640 360',  # origin 469ccacaea8b418e2e0a5078fd790ccfed00dc43
    'sharpness-reparam-curvature': '0 0 640 360',  # origin 469ccacaea8b418e2e0a5078fd790ccfed00dc43
    'sigma-reparam-spectral-gain': '0 0 640 360',  # origin 4a611378445ea5c5396a3488f71c4e374b2c939e
    'speculative-decoding': '0 0 640 360',  # origin af2ed229649acd6e2699911860c52a161fcc304b
    'spsa-two-evaluations': '0 0 640 360',  # origin d2c84dd00777ae7d0eea3ea38a13012146a4b1a5
    'stochastic-depth-paths': '0 0 640 360',  # origin 255f92a3054b761cd178a1ec18a8d9e50d602d37
    'stochastic-depth-scaling-conventions': '0 0 640 360',  # origin cf135da6a3c3514a791ac9fef8d2c911ad5b067c,ad0d9a902490f60136e5f15ea4481b1208d4bc14
    'stochastic-depth-survival-samples': '0 0 640 360',  # origin eee699618afdae1909247586f288d49418006b66
    'streaming-kv-eviction': '0 0 640 360',  # origin 1d54c4ae36eff5a4df7bb9587a2e0580ff5636ee
    'svd-degenerate-bases': '0 0 800 420',  # origin 4e9273d5f125f417ff90d9a72fdaec328b37ad2c
    'svd-ls-orthogonal-residual': '0 0 800 420',  # origin 4e9273d5f125f417ff90d9a72fdaec328b37ad2c
    'svd-noise-amplification': '0 0 800 420',  # origin 15ee47cca1facbe271d07664928f3cba3b6d5cd9
    'svd-rank-accumulation': '0 0 800 420',  # origin 15ee47cca1facbe271d07664928f3cba3b6d5cd9
    'svd-unit-circle': '0 0 640 360',  # origin e2abf17856e1fd83746aaf12f8fd5119d6f0d40e
    'svm-margin-hinge': '0 0 640 360',  # origin 6695c6a7b352d64f98f511d2aa3fcf6edcf867bc
    'swin-shifted-windows': '0 0 640 360',  # origin e00a7dd21eca5336c9865027674000f7578521dc
    'td3-delayed-twin-critics': '0 0 640 360',  # origin 5378eb9fe6f826d1f15ce934e7589b2facb915ed
    'tree-belief-propagation': '0 0 640 360',  # origin 273a612a84ccbe0748594ed51a27b63256af321a
    'tsne-kl-embedding': '0 0 640 360',  # origin c028c848a3e1e3d7013ae6ca35aaa9f9e2ced3d8
    'umap-fuzzy-union': '0 0 640 360',  # origin c028c848a3e1e3d7013ae6ca35aaa9f9e2ced3d8
    'unigram-sampling-alpha': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'unigram-viterbi-lattice': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'vae-reparameterisation': '0 0 640 360',  # origin 83c4115c9a0a88e9659169d136db7107410f4b66
    'viterbi-trellis': '0 0 640 360',  # origin 273a612a84ccbe0748594ed51a27b63256af321a
    'weak-supervision-vote-fusion': '0 0 640 360',  # origin c028c848a3e1e3d7013ae6ca35aaa9f9e2ced3d8
    'wgan-gp-interpolation': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
    'wgan-weight-clip': '0 0 640 360',  # origin 15c481b6e404a995701352554969476d4bf66fc8
}
# Explicit non-TOPICS assets validated by main(), not generic name allowances.
EXTRA_CANONICAL_FILENAMES = {
    'moe-top2-routing-token-b.svg': '0 0 640 360',  # origin b818e3217c86c26dde61f83ad8ad43d90045006f
    'brier-expected-risk-motion.svg': '0 0 640 360',  # origin 07ac637904c787a32fe192fdfec01bd80598ea89
    'brier-expected-risk-still.svg': '0 0 640 360',  # origin 07ac637904c787a32fe192fdfec01bd80598ea89
    'log-loss-tail-penalty-motion.svg': '0 0 640 360',  # origin 07ac637904c787a32fe192fdfec01bd80598ea89
    'log-loss-tail-penalty-still.svg': '0 0 640 360',  # origin 07ac637904c787a32fe192fdfec01bd80598ea89
}
# Preserve original source prefix contracts, including their valid named variants.
PREFIX_VIEWBOXES = {
    "ece-binned-calibration": "0 0 720 400",
    "deep-ensemble-spread": "0 0 720 400",
    "cfm-conditional-bridge": "0 0 760 410",
    "rectified-reflow-coupling": "0 0 760 410",
}


def expected_viewbox(path: Path) -> str | None:
    if path.name in EXTRA_CANONICAL_FILENAMES:
        return EXTRA_CANONICAL_FILENAMES[path.name]
    name = path.stem
    stem = re.sub(r"-(?:motion|still)$", "", name)
    if stem in CANONICAL_VIEWBOXES:
        return CANONICAL_VIEWBOXES[stem]
    # A new registered topic cannot inherit a canvas accidentally via a prefix.
    if stem in TOPICS:
        return None
    matches = [(prefix, box) for prefix, box in PREFIX_VIEWBOXES.items()
               if name.startswith(prefix)]
    if not matches:
        return None
    longest = max(len(prefix) for prefix, _ in matches)
    boxes = {box for prefix, box in matches if len(prefix) == longest}
    return next(iter(boxes)) if len(boxes) == 1 else None


# Independently restored original page contracts; never inferred from image URLs.
SOURCE_ALT_CONTRACT_STEMS = {'unigram-viterbi-lattice', 'weak-supervision-vote-fusion', 'expert-cache-miss', 'qk-norm-scale-sweep', 'qlora-frozen-flow', 'ivfpq-probe-pq-lookup', 'graphsage-sample-aggregate', 'gin-multiset-counts', 'minhash-lsh-band-collision', 'sigma-reparam-spectral-gain', 'dora-independent', 'unigram-sampling-alpha', 'hnsw-layer-descent', 'tsne-kl-embedding', 'umap-fuzzy-union', 'cfm-conditional-bridge', 'rectified-reflow-coupling', 'paged-block-mapping'}
STATIC_PREVIEW_LINK_STEMS = {'clr-triangular2-sweep', 'weak-supervision-vote-fusion', 'ivfpq-probe-pq-lookup', 'graphsage-sample-aggregate', 'gin-multiset-counts', 'minhash-lsh-band-collision', 'deep-ensemble-spread', 'ece-binned-calibration', 'hnsw-layer-descent', 'cfm-conditional-bridge', 'rectified-reflow-coupling'}

NAS_STEMS = {"darts-soft-operations", "aging-evolution-queue", "enas-shared-weight-transfer", "mnasnet-latency-tradeoff"}
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
    if not (images[0].get("alt") or "").strip():
        errors.append(f"{page}: marked motion image needs non-whitespace alt text")
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
    expected = expected_viewbox(path)
    if root.tag != NS + "svg" or expected is None or root.get("viewBox") != expected:
        errors.append(f"{path}: invalid SVG root/viewBox (expected {expected!r})")
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
    if set(CANONICAL_VIEWBOXES) != set(TOPICS):
        errors.append("Canvas registry must explicitly match all registered TOPICS")
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
            if stem in SOURCE_ALT_CONTRACT_STEMS:
                images = [img for img in MotionImages(text).images
                          if stem in (img.get("src") or "")]
                if not images or any(not (img.get("alt") or "").strip() for img in images):
                    errors.append(f"{page}: marked motion image needs non-whitespace alt text")
            if stem in STATIC_PREVIEW_LINK_STEMS:
                # An image/fallback attribute is not an independently clickable preview.
                preview_links = re.findall(r"(?<!!)\[[^]]+\]\(([^)]+\.svg)\)", text)
                if static_path.resolve() not in {(page.parent / link).resolve() for link in preview_links}:
                    errors.append(f"{page}: missing independent static preview hyperlink for {stem}")
                if stem == "clr-triangular2-sweep" and animated_path.resolve() not in {(page.parent / link).resolve() for link in preview_links}:
                    errors.append(f"{page}: missing independent full comparison animation hyperlink for {stem}")
            links = re.findall(r"!\[[^]]+\]\(([^)]+\.svg)\)", text)
            linked_images = {(page.parent / link).resolve() for link in links}
            if stem in NAS_STEMS:
                errors.extend(verify_source_pair(page, text, stem))
            elif stem in {"iou-overlap-sweep", "dice-overlap-response"}:
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
            elif stem in {"roc-pr-shift", "roc-youden-cost", "roc-cost-operating-point", "pr-random-ap-expectation", "f1-threshold-topk", "roc-randomized-operating-mix", "roc-tie-half-credit", "pr-ap-tied-threshold", "roc-pairwise-auc", "pr-ap-rectangles", "precision-recall-threshold", "f1-harmonic-gap", "accuracy-prevalence", "fbeta-recall-emphasis", "precision-base-rate", "f1-macro-micro-imbalance", "roc-partial-area", "pr-ap-trapezoid-gap"}:
                errors.extend(verify_source_pair(page, text, stem))
                static_links = re.findall(r"\[[^]]+\]\(([^)]+\.svg)\)", text)
                if static_path.resolve() not in {(page.parent / link).resolve() for link in static_links}:
                    errors.append(f"{page}: missing GitHub static preview link for {stem}")
            elif stem in {"cfm-conditional-bridge", "deep-ensemble-spread", "ece-binned-calibration", "gated-sae-gate-magnitude", "glorot-alternating-width", "glorot-equal-variance-densities", "glorot-fan-tradeoff", "glorot-tanh-saturation", "he-fan-mode-tradeoff", "he-relu-mean-shift", "he-relu-second-moment", "hmm-baum-welch-transition", "hmm-filter-smooth", "hmm-forward-sum-product", "hmm-pairwise-posterior", "hnsw-layer-descent", "ivfpq-probe-pq-lookup", "jumprelu-threshold-jump", "lion-sign-momentum", "muon-spectral-balancing", "mup-adam-sgd", "mup-readout-aggregation", "mup-readout-noise", "mup-transfer-protocol", "mup-transfer-validation", "mup-update-budget", "mup-width-multipliers", "prelu-slope-gain", "qk-norm-scale-sweep", "react-evidence-loop", "rectified-reflow-coupling", "reflexion-memory-feedback", "sigma-reparam-spectral-gain", "tsne-kl-embedding", "umap-fuzzy-union", "unigram-sampling-alpha", "unigram-viterbi-lattice"}:
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
            elif stem in {"paged-block-mapping", "expert-cache-miss"}:
                errors.extend(verify_source_pair(page, text, stem))
                player = (DOCS / "javascripts" / "concept-motion.js").read_text(encoding="utf-8")
                if f"'{stem}-still.svg'" not in player:
                    errors.append(f"{page}: static-first animation not registered in player")
            elif stem in {"adafactor-factored-moments", "adagrad-coordinate-gain", "adam-bias-correction", "adam-epsilon-threshold", "adam-scale-invariance", "adam-sign-reversal", "adamw-epoch-timescale", "ant-colony-pheromone", "asam-neighborhood", "auc-ap-ranking-contrast", "bo-expected-improvement", "bo-gp-conditioning", "boosting-residual-steps", "bpr-gradient-saturation", "bpr-pairwise-ranking", "checkpoint-recompute", "clr-triangular2-sweep", "colbert-maxsim-switch", "cv-fold-rotation", "dora-independent", "dpr-dot-product-sweep", "dropblock-spatial-masking", "dropout-inverted-sampling", "dropout-variance-tradeoff", "effective-number-growth", "eigen-jordan-shear", "eigen-linear-map", "eigen-rotation-no-real", "eigen-zero-eigenvalue", "elo-online-update", "forest-bootstrap-vote", "fp16-loss-scaling", "fp8-scale-range", "gin-multiset-counts", "graphsage-sample-aggregate", "grid-search-x-coverage", "group-norm-statistics", "heavy-ball-overshoot", "ida-bound-reexpansion", "lagrange-dual-gap", "lagrange-kkt-active-set", "lagrange-tangency", "lamb-adam-layer-trust", "lars-layer-trust-scaling", "logit-prior-decision", "lsq-step-size-sweep", "mahalanobis-ellipse-threshold", "map-beta-posterior", "map-precision-at-hits", "mc-dropout-repeated-passes", "mf-als-alternating", "mf-coupled-sgd", "minhash-lsh-band-collision", "mixup-beta-strength", "mixup-cutmix-area", "mixup-loss-decomposition", "mixup-paired-interpolation", "mle-bernoulli-likelihood", "ndcg-position-discount", "newton-armijo-backtracking", "newton-curvature-steps", "newton-indefinite-curvature", "odin-gradient-perturbation", "outlier-mae-rmse", "paired-bootstrap-resampling", "particle-swarm-best", "pr-threshold-sweep", "qat-fake-quant-ste", "qlora-frozen-flow", "r2-mean-baseline", "random-search-x-coverage", "resnet-depth-gradient-factors", "resnet-identity-gradient", "resnet-postrelu-gate", "resnet-projection-shortcut", "resolution-refutation-chain", "rf-bootstrap-oob", "rf-feature-subset", "rmsnorm-shift-response", "roc-rank-transform", "roc-threshold-sweep", "roofline-ridge-sweep", "rotational-norm-balance", "sgd-noise-batch", "shampoo-eigenmode", "sharpness-radius-loss", "sharpness-reparam-curvature", "stochastic-depth-scaling-conventions", "stochastic-depth-survival-samples", "svm-margin-hinge", "weak-supervision-vote-fusion", "wgan-gp-interpolation", "wgan-weight-clip",
                          "svd-unit-circle", "svd-rank-accumulation", "svd-noise-amplification", "svd-ls-orthogonal-residual", "svd-degenerate-bases", "power-iteration-convergence",
                          "kmeans-plusplus-d2", "kmeans-outlier-leverage", "kmeans-feature-scale", "kmeans-elbow-inertia",
                          "ar-score-vs-sample", "ar-likelihood-accumulation", "ar-context-drift", "ar-eos-survival",
                          "3d-unet-depth-kernel", "3d-unet-paired-warp", "3d-unet-sparse-loss", "3d-unet-evaluation-holdout", "3d-unet-skip-concat", "3d-unet-context-tiling", "3d-unet-orthogonal-slices", "3d-unet-sparse-context-gradient"}:
                # GitHub uses the raw static image; the opt-in hook rewrites
                # all three source-relative attributes for each built locale.
                errors.extend(verify_source_pair(page, text, stem))
                if stem in {"adam-bias-correction", "adam-epsilon-threshold", "adam-scale-invariance", "adam-sign-reversal", "ant-colony-pheromone", "bpr-gradient-saturation", "bpr-pairwise-ranking", "eigen-linear-map", "eigen-rotation-no-real", "lagrange-dual-gap", "lagrange-kkt-active-set", "lagrange-tangency", "mf-als-alternating", "mf-coupled-sgd", "newton-armijo-backtracking", "newton-curvature-steps", "newton-indefinite-curvature", "particle-swarm-best", "power-iteration-convergence", "resnet-depth-gradient-factors", "resnet-identity-gradient", "resnet-postrelu-gate", "resnet-projection-shortcut", "svd-degenerate-bases", "svd-ls-orthogonal-residual", "svd-noise-amplification", "svd-rank-accumulation", "svd-unit-circle"}:
                    static_links = re.findall(r"\[[^]]+\]\(([^)]+\.svg)\)", text)
                    if static_path.resolve() not in {
                        (page.parent / link).resolve() for link in static_links
                    }:
                        errors.append(f"{page}: missing GitHub-readable static link")
            elif animated_path.resolve() not in linked_images:
                errors.append(f"{page}: missing or incorrect animated SVG link")
            if stem in {"3d-unet-context-tiling", "3d-unet-depth-kernel", "3d-unet-evaluation-holdout", "3d-unet-orthogonal-slices", "3d-unet-paired-warp", "3d-unet-skip-concat", "3d-unet-sparse-context-gradient", "3d-unet-sparse-loss", "adamw-decoupled-paths", "alpha-beta-cutoff", "astar-frontier", "batch-norm-train-infer", "bpe-ordered-merges", "byol-online-target", "cmaes-distribution-adaptation", "deformable-sampling", "dinov2-dual-objective-ema", "disaggregated-handoff", "dpll-backtrack", "dqn-target-sync", "expert-cache-miss", "forward-ad-jvp", "gat-aggregation", "gcn-aggregation", "gibbs-coordinate-sweeps", "gru-gate-flow", "hmc-leapfrog-trajectory", "hyperband-budget", "kfac-factor-preconditioning", "kmeans-lloyd", "lbfgs-two-loop", "lion-sign-momentum", "mae-visible-patch-reconstruction", "maml-inner-outer-loop", "mcts-search-cycle", "mean-field-coordinate-ascent", "mh-accept-reject", "moco-dictionary-cycle", "moe-top2-routing", "muon-spectral-balancing", "muzero-latent-planning", "nerf-volume-rendering", "nesterov-lookahead", "orca-continuous-batching", "paged-block-mapping", "ppo-clipped-objective", "prioritized-replay-cycle", "qk-norm-scale-sweep", "qmix-monotonic-greedy", "realnvp-affine-coupling", "reverse-ad-vjp", "rmsprop-adaptive-memory", "sam-two-gradient", "sigma-reparam-spectral-gain", "speculative-decoding", "spsa-two-evaluations", "stochastic-depth-paths", "streaming-kv-eviction", "swin-shifted-windows", "td3-delayed-twin-critics", "tree-belief-propagation", "tsne-kl-embedding", "umap-fuzzy-union", "vae-reparameterisation", "viterbi-trellis"}:
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
    # Classification metrics reuse one asset pair across two language-specific pages.
    for suffix in (".md", ".zh-TW.md"):
        recall_page = DOCS / ("theory/evaluation/metrics/classification/recall" + suffix)
        errors.extend(verify_source_pair(recall_page, recall_page.read_text(encoding="utf-8"), "precision-recall-threshold"))
    import subprocess
    semantics = subprocess.run([sys.executable,"scripts/test_classification_motion_semantics.py"],capture_output=True,text=True)
    if semantics.returncode:
        errors.append("Classification motion semantics failed: " + semantics.stdout + semantics.stderr)
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

    # Newer pages keep a GitHub-readable <img src="...-still.svg"> and
    # expose the animated variant to the MkDocs player through data-motion-src.
    # Check both paths rather than accepting the data attribute as the fallback.
    html_motion_topics = {
        "odin-gradient-perturbation": "theory/machine-learning/ood-detection/odin",
        "mahalanobis-ellipse-threshold": "theory/machine-learning/ood-detection/mahalanobis-distance",
    }
    for stem, page_stem in html_motion_topics.items():
        motion = ASSETS / f"{stem}-motion.svg"
        still = ASSETS / f"{stem}-still.svg"
        errors.extend(verify_svg(motion, True))
        errors.extend(verify_svg(still, False))
        for suffix in (".md", ".zh-TW.md"):
            page = DOCS / (page_stem + suffix)
            if not page.exists():
                errors.append(f"{page}: bilingual chapter missing")
                continue
            chapter = page.read_text(encoding="utf-8")
            image_tags = re.findall(r"<img\b[^>]*>", chapter)
            found = False
            for tag in image_tags:
                src = re.search(r'\ssrc="([^"]+)"', tag)
                data = re.search(r'\sdata-motion-src="([^"]+)"', tag)
                if not src or not data:
                    continue
                static_path = (page.parent / src.group(1)).resolve()
                motion_path = (page.parent / data.group(1)).resolve()
                if static_path == still.resolve() and motion_path == motion.resolve():
                    found = True
                    break
            if not found:
                errors.append(f"{page}: no matching real HTML still/motion source pair")
            if "CC BY-SA 4.0" not in chapter:
                errors.append(f"{page}: original visual attribution missing")
        print(f"HTML motion pair {stem}: "
              f"{motion.stat().st_size if motion.exists() else '-'} / "
              f"{still.stat().st_size if still.exists() else '-'} bytes")

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
