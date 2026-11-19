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
    'alibi-content-recency': 'theory/models/transformer/positional-encodings/index',
    'alibi-distance-softmax': 'theory/models/transformer/positional-encodings/index',
    'alibi-head-prefix': 'theory/models/transformer/positional-encodings/index',
    'rope-axial-2d': 'theory/models/transformer/positional-encodings/index',
    'rope-cache-reindex': 'theory/models/transformer/positional-encodings/index',
    'rope-frequency-bands': 'theory/models/transformer/positional-encodings/index',
    'rope-interpolation-angle': 'theory/models/transformer/positional-encodings/index',
    'shaw-relative-clipping': 'theory/models/transformer/positional-encodings/index',
    'shaw-relative-value': 'theory/models/transformer/positional-encodings/index',
    'sinusoidal-multiscale': 'theory/models/transformer/positional-encodings/index',
    'yarn-attention-temperature': 'theory/models/transformer/positional-encodings/index',
    'yarn-frequency-ramp': 'theory/models/transformer/positional-encodings/index',

    'ucb1-optimism-switch': 'theory/paradigms/online/stochastic-bandits/index',
    'ucb1-bonus-sensitivity': 'theory/paradigms/online/stochastic-bandits/index',
    'thompson-beta-posterior-draws': 'theory/paradigms/online/stochastic-bandits/index',
    'thompson-evidence-concentration': 'theory/paradigms/online/stochastic-bandits/index',

    "s4d-diagonal-modes": "theory/models/ssm/structured-state-spaces/s4d/index",
    "mamba2-ssd-causal-map": "theory/models/ssm/selective-state-spaces/mamba-2/index",
    "rainbow-c51-projection": "theory/paradigms/reinforcement-learning/value-based-methods/rainbow/index",
    "rainbow-dueling-head": "theory/paradigms/reinforcement-learning/value-based-methods/rainbow/index",
    "rainbow-nstep-returns": "theory/paradigms/reinforcement-learning/value-based-methods/rainbow/index",
    "rainbow-noisynet-samples": "theory/paradigms/reinforcement-learning/value-based-methods/rainbow/index",

    "dt-return-budget": "theory/paradigms/reinforcement-learning/offline-rl/decision-transformer/index",
    "dt-causal-prefix": "theory/paradigms/reinforcement-learning/offline-rl/decision-transformer/index",
    "q-sarsa-backup": "theory/paradigms/reinforcement-learning/value-based-methods/q-learning/index",
    "q-sarsa-noisy-backups": "theory/paradigms/reinforcement-learning/value-based-methods/q-learning/index",
    "q-sarsa-epsilon": "theory/paradigms/reinforcement-learning/value-based-methods/q-learning/index",
    "double-dqn-selector": "theory/paradigms/reinforcement-learning/value-based-methods/double-dqn/index",
    "td-terminal-truncation": "theory/paradigms/reinforcement-learning/value-based-methods/q-learning/index",
    "cliff-walking": "theory/paradigms/reinforcement-learning/value-based-methods/q-learning/index",
    "eligibility-trace-cut": "theory/paradigms/reinforcement-learning/value-based-methods/q-learning/index",
    "nstep-lambda-forward": "theory/paradigms/reinforcement-learning/value-based-methods/q-learning/index",
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
    "reinforce-reward-to-go": "theory/paradigms/reinforcement-learning/policy-gradient-and-actor-critic/reinforce/index",
    "reinforce-return-credit": "theory/paradigms/reinforcement-learning/policy-gradient-and-actor-critic/reinforce/index",
    "grpo-group-advantages": "theory/paradigms/reinforcement-learning/policy-gradient-and-actor-critic/grpo/index",
    "self-instruct-filter-loop": "engineering/synthetic-data/self-instruct",
    "recursive-tail-loss": "engineering/synthetic-data/model-collapse",
    "awq-salient-scaling": "theory/model-compression/quantisation/post-training/awq/index",
    "gptq-error-compensation": "theory/model-compression/quantisation/post-training/gptq/index",
    "saliency-local-gradient": "society/interpretability/saliency-maps",
    "integrated-gradients-path": "society/interpretability/integrated-gradients",
    "power-iteration-projection-contraction": "theory/math/linear-algebra/eigendecomposition",
    "large-batch-warmup-ramp": "theory/optimization/gradual-warm-up",
    "theta-gamma-phase-amplitude": "brain-mind/oscillations/theta-gamma-coupling/index",
    "coherence-phase-gating": "brain-mind/oscillations/communication-through-coherence/index",
    "strips-state-effects": "theory/paradigms/symbolic-ai/planning/strips",
    "graphplan-layer-extraction": "theory/paradigms/symbolic-ai/planning/graphplan",
    "genetic-crossover-mutation": "theory/paradigms/evolutionary/genetic-algorithms",
    "map-elites-archive": "theory/paradigms/evolutionary/map-elites",
    "place-cell-firing": "brain-mind/navigation-cognitive-maps/place-cells/index",
    "successor-occupancy": "brain-mind/navigation-cognitive-maps/successor-representation/index",
    "causal-lamp-intervention": "theory/paradigms/imitation/behavioural-cloning/causal-confusion",
    "copycat-action-lag": "theory/paradigms/imitation/behavioural-cloning/causal-confusion",
    "prompt-injection-boundary": "engineering/llm-security/indirect-prompt-injection",
    "watermark-greenlist-score": "engineering/llm-security/watermarking",
    "ia3-channel-gates": "theory/paradigms/transfer/fine-tuning-and-adaptation/ia3",
    "prefix-kv-attention": "theory/paradigms/transfer/fine-tuning-and-adaptation/prefix-tuning",
    "forward-prediction-correction": "brain-mind/motor-control/internal-forward-models/index",
    "ofc-selective-feedback": "brain-mind/motor-control/optimal-feedback-control/index",
    "vqvae-codebook-snap": "theory/paradigms/unsupervised/density-and-generative-models/vae/vq-vae",
    "gaussian-splat-alpha-composite": "theory/models/computer-vision/3d-and-neural-rendering/gaussian-splatting",
    "fixmatch-confidence-gate": "theory/paradigms/semi-supervised/consistency-regularisation/fixmatch",
    "mean-teacher-ema-tracking": "theory/paradigms/semi-supervised/consistency-regularisation/mean-teacher",
    "simclr-temperature-competition": "theory/paradigms/self-supervised/contrastive-learning/simclr",
    "bahdanau-alignment-context": "theory/models/transformer/bahdanau-attention/index",
    "svi-minibatch-global": "theory/paradigms/probabilistic/variational-inference/stochastic-variational-inference",
    "soap-eigenbasis-adam": "theory/optimization/adaptive/soap",
    "t5-span-corruption": "theory/models/transformer/architecture-families/t5/index",
    "deit-dual-head-distillation": "theory/models/transformer/vision-transformer/deit/index",
    "score-sde-flow": "theory/paradigms/unsupervised/density-and-generative-models/diffusion/score-sde",
    "consistency-trajectory-map": "theory/paradigms/unsupervised/density-and-generative-models/diffusion/consistency-models",
    "ewc-fisher-springs": "theory/paradigms/continual/regularisation-based/ewc",
    "neat-add-node-innovation": "theory/paradigms/evolutionary/neat",
    "pbwm-gate": "brain-mind/working-memory-executive-function/pbwm/index",
    "activity-silent-trace": "brain-mind/working-memory-executive-function/activity-silent-working-memory/index",
    "sac-entropy-temperature": "theory/paradigms/reinforcement-learning/policy-gradient-and-actor-critic/sac/index",
    "dpo-preference-margin": "theory/paradigms/reinforcement-learning/learning-from-human-feedback/dpo/index",
    "roi-align-sampling": "theory/models/computer-vision/segmentation/mask-r-cnn",
    "sam-prompt-ambiguity": "theory/models/computer-vision/segmentation/segment-anything",
    "vivit-factorised-attention": "theory/models/computer-vision/video/vivit",
    "i3d-filter-inflation": "theory/models/computer-vision/video/i3d",
    "video-joint-denoising": "theory/models/computer-vision/video/video-diffusion",
    "latent-space-denoise": "theory/paradigms/unsupervised/density-and-generative-models/diffusion/latent-diffusion",
    "layernorm-feature-shift": "theory/models/mlp/layer-normalisation/index",
    "seq2seq-context-handoff": "theory/models/rnn/sequence-modes/sequence-to-sequence/index",
    "lime-local-surrogate": "society/interpretability/lime",
    "shap-coalition-marginals": "society/interpretability/shap",
    "backdoor-standardisation": "theory/causal-inference/index",
    "collider-selection": "theory/causal-inference/index",
    "gqa-head-sharing": "engineering/inference-optimization/grouped-query-attention",
    "gqa-uptraining-pooling": "engineering/inference-optimization/grouped-query-attention",
    'gradient-clipping-comparison': 'theory/optimization/gradient-clipping-and-normalisation',
    'gradient-accumulation-clipping-order': 'theory/optimization/gradient-clipping-and-normalisation',
    'gradient-global-layer-budget': 'theory/optimization/gradient-clipping-and-normalisation',
    'gradient-amp-unscale-order': 'theory/optimization/gradient-clipping-and-normalisation',
    'gradient-agc-relative-cap': 'theory/optimization/gradient-clipping-and-normalisation',
    'gradient-decoupled-decay': 'theory/optimization/gradient-clipping-and-normalisation',
    'kivi-quantization-axis': 'engineering/inference-optimization/kivi',
    'h2o-heavy-hitter-selection': 'engineering/inference-optimization/h2o',

    "conformal-subgroup-coverage": "theory/paradigms/probabilistic/uncertainty-calibration/conformal-prediction",
    "conformal-shift-coverage": "theory/paradigms/probabilistic/uncertainty-calibration/conformal-prediction",
    "conformal-cqr-expansion": "theory/paradigms/probabilistic/uncertainty-calibration/conformal-prediction",
    "conformal-weighted-quantile": "theory/paradigms/probabilistic/uncertainty-calibration/conformal-prediction",
    "conformal-aps-cumulative": "theory/paradigms/probabilistic/uncertainty-calibration/conformal-prediction",
    "conformal-alpha-staircase": "theory/paradigms/probabilistic/uncertainty-calibration/conformal-prediction",
    "conformal-mondrian-groups": "theory/paradigms/probabilistic/uncertainty-calibration/conformal-prediction",
    "conformal-raps-penalty": "theory/paradigms/probabilistic/uncertainty-calibration/conformal-prediction",
    "fedavg-weighted-round": "theory/paradigms/federated/federated-averaging/index",
    "secagg-mask-cancellation": "theory/paradigms/federated/privacy-and-secure-aggregation/index",
    "dagger-dataset-aggregation": "theory/paradigms/imitation/interactive-imitation/dagger",
    "dart-noisy-expert-recovery": "theory/paradigms/imitation/interactive-imitation/dart",
    "openvla-dual-encoder-fusion": "applications/robotics/openvla/index",
    "openvla-percentile-action-bins": "applications/robotics/openvla/index",
    "vint-goal-waypoint-flow": "applications/robotics/navigation/vint",
    "nomad-goal-mask-routing": "applications/robotics/navigation/nomad",
    "gnm-speed-normalization": "applications/robotics/navigation/gnm",
    "ving-learned-graph-routing": "applications/robotics/navigation/ving",

    "saycan-skill-grounding": "applications/robotics/saycan/index",
    "rt2-action-token-decoding": "applications/robotics/rt-2/index",
    "diffusion-policy-noise-training": "applications/robotics/diffusion-policy/index",
    "diffusion-policy-multimodal-actions": "applications/robotics/diffusion-policy/index",
    "diffusion-policy-denoising": "applications/robotics/diffusion-policy/index",
    "diffusion-policy-receding-horizon": "applications/robotics/diffusion-policy/index",
    'act-temporal-ensemble': 'applications/robotics/aloha/index',
    'act-cvae-train-deploy': 'applications/robotics/aloha/index',

    "stdp-spike-timing": "brain-mind/snn-neuromorphic/stdp/index",
    "eprop-local-credit": "brain-mind/snn-neuromorphic/eprop/index",
    "pbt-exploit-explore": "theory/paradigms/reinforcement-learning/multi-agent-rl/population-based-training/pbt/index",
    "ftw-two-level-learning": "theory/paradigms/reinforcement-learning/multi-agent-rl/population-based-training/ftw/index",
    "kd-soft-target-alignment": "theory/model-compression/knowledge-distillation/response-based/hinton-distillation/index",
    "fitnets-hint-then-output": "theory/model-compression/knowledge-distillation/feature-based/fitnets/index",
    "offline-iql-expectile": "theory/paradigms/reinforcement-learning/offline-rl/iql/index",
    "offline-cql-conservative": "theory/paradigms/reinforcement-learning/offline-rl/cql/index",
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
    "roc-fpr-batch": "theory/evaluation/metrics/classification/roc-auc",
    "roc-fpr-zero-alarms": "theory/evaluation/metrics/classification/roc-auc",
    "roc-fpr-budget-mix": "theory/evaluation/metrics/classification/roc-auc",
    "roc-pr-shift": "theory/evaluation/metrics/classification/roc-auc",
    "roc-prior-policy": "theory/evaluation/metrics/classification/roc-auc",
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
    "flashattention-online-rescale": "theory/models/transformer/attention-variants/flash-attention/index",
    "flashattention-exact-merge": "theory/models/transformer/attention-variants/flash-attention/index",
    "flashattention-causal-tiles": "theory/models/transformer/attention-variants/flash-attention/index",
    "flashattention-backward-remat": "theory/models/transformer/attention-variants/flash-attention/index",
    "flashattention2-query-parallel": "theory/models/transformer/attention-variants/flash-attention/index",
    "flashattention3-load-compute-pipeline": "theory/models/transformer/attention-variants/flash-attention/index",
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
    "kalman-gain-fusion": "theory/paradigms/probabilistic/graphical-models/kalman-filter",
    "particle-weight-resampling": "theory/paradigms/probabilistic/graphical-models/particle-filter",
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
    "rlhf-dpo-margin": "theory/paradigms/reinforcement-learning/learning-from-human-feedback/dpo/index",
    "rlhf-reward-sums": "theory/paradigms/reinforcement-learning/learning-from-human-feedback/reward-modelling/index",
    "mcts-search-cycle": "theory/paradigms/reinforcement-learning/mcts-and-self-play/index",
    "alphazero-policy-target": "theory/paradigms/reinforcement-learning/alphazero/index",
    "alphazero-selfplay-labels": "theory/paradigms/reinforcement-learning/alphazero/index",
    "alphazero-puct-select": "theory/paradigms/reinforcement-learning/alphazero/index",
    "alphazero-value-backup": "theory/paradigms/reinforcement-learning/alphazero/index",
    "rnd-prediction-error": "theory/paradigms/reinforcement-learning/exploration/rnd/index",
    "rnd-state-novelty": "theory/paradigms/reinforcement-learning/exploration/rnd/index",
    "icm-forward-inverse": "theory/paradigms/reinforcement-learning/exploration/icm/index",
    "icm-predictable-stochastic": "theory/paradigms/reinforcement-learning/exploration/icm/index",
    "dqn-target-sync": "theory/paradigms/reinforcement-learning/deep-q-networks/index",
    "adamw-decoupled-paths": "theory/optimization/adaptive/adamw",
    "adam-bias-correction": "theory/optimization/adaptive/adam",
    "adam-scale-invariance": "theory/optimization/adaptive/adam",
    "adam-sign-reversal": "theory/optimization/adaptive/adam",
    "adam-epsilon-threshold": "theory/optimization/adaptive/adam",
    "ddpg-actor-gradient": "theory/paradigms/reinforcement-learning/policy-gradient-and-actor-critic/ddpg/index",
    "ddpg-replay-bootstrap": "theory/paradigms/reinforcement-learning/policy-gradient-and-actor-critic/ddpg/index",
    "ddpg-ou-noise": "theory/paradigms/reinforcement-learning/policy-gradient-and-actor-critic/ddpg/index",
    "ddpg-polyak-target": "theory/paradigms/reinforcement-learning/policy-gradient-and-actor-critic/ddpg/index",
    "a3c-nstep-return": "theory/paradigms/reinforcement-learning/policy-gradient-and-actor-critic/a3c/index",
    "trpo-ratio-surrogate": "theory/paradigms/reinforcement-learning/policy-gradient-and-actor-critic/trpo/index",
    "a3c-async-gradient": "theory/paradigms/reinforcement-learning/policy-gradient-and-actor-critic/a3c/index",
    "trpo-kl-backtracking": "theory/paradigms/reinforcement-learning/policy-gradient-and-actor-critic/trpo/index",
    "sac-soft-target": "theory/paradigms/reinforcement-learning/policy-gradient-and-actor-critic/sac/index",
    "sac-temperature-feedback": "theory/paradigms/reinforcement-learning/policy-gradient-and-actor-critic/sac/index",
    "td3-delayed-twin-critics": "theory/paradigms/reinforcement-learning/policy-gradient-and-actor-critic/td3/index",
    "ppo-clipped-objective": "theory/paradigms/reinforcement-learning/proximal-policy-optimisation/index",
    "prioritized-replay-cycle": "theory/paradigms/reinforcement-learning/experience-replay/index",
    "sam-two-gradient": "theory/optimization/sharpness-aware-minimisation",
    "fgsm-sign-step": "theory/machine-learning/adversarial-robustness/fgsm",
    "pgd-projection-path": "theory/machine-learning/adversarial-robustness/pgd-adversarial-training",
    "lbfgs-two-loop": "theory/optimization/lbfgs",
    "nesterov-lookahead": "theory/optimization/sgd-and-momentum/nesterov",
    "hyperband-budget": "theory/optimization/hyperparameter-optimisation/hyperband",
    "bo-gp-conditioning": "theory/optimization/hyperparameter-optimisation/bayesian-optimisation",
    "bo-expected-improvement": "theory/optimization/hyperparameter-optimisation/bayesian-optimisation",
    "qmix-monotonic-greedy": "theory/paradigms/reinforcement-learning/multi-agent-rl/qmix/index",
    "maddpg-joint-bootstrap": "theory/paradigms/reinforcement-learning/multi-agent-rl/maddpg/index",
    "maddpg-actor-gradient": "theory/paradigms/reinforcement-learning/multi-agent-rl/maddpg/index",
    "mappo-backward-gae": "theory/paradigms/reinforcement-learning/multi-agent-rl/mappo/index",
    "mappo-shared-advantage": "theory/paradigms/reinforcement-learning/multi-agent-rl/mappo/index",
    "rial-dial-credit-path": "theory/paradigms/reinforcement-learning/multi-agent-rl/emergent-communication/rial-dial/index",
    "commnet-leave-one-out": "theory/paradigms/reinforcement-learning/multi-agent-rl/emergent-communication/commnet/index",
    "dial-dru-train-execute": "theory/paradigms/reinforcement-learning/multi-agent-rl/emergent-communication/rial-dial/index",
    "commnet-layer-iterations": "theory/paradigms/reinforcement-learning/multi-agent-rl/emergent-communication/commnet/index",
    "muzero-latent-planning": "theory/paradigms/reinforcement-learning/model-based-rl/muzero/index",
    "pets-ensemble-particles": "theory/paradigms/reinforcement-learning/model-based-rl/pets/index",
    "mbpo-short-branches": "theory/paradigms/reinforcement-learning/model-based-rl/mbpo/index",
    "pets-cem-refit": "theory/paradigms/reinforcement-learning/model-based-rl/pets/index",
    "mbpo-horizon-error": "theory/paradigms/reinforcement-learning/model-based-rl/mbpo/index",
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
    "forward-ad-directional-jvp": "theory/math/automatic-differentiation/forward-mode",
    "forward-ad-jacobian-columns": "theory/math/automatic-differentiation/forward-mode",
    "forward-ad-dual-chain": "theory/math/automatic-differentiation/forward-mode",
    "forward-ad-branch-kink": "theory/math/automatic-differentiation/forward-mode",
    "forward-ad-loop-tangent": "theory/math/automatic-differentiation/forward-mode",
    "forward-ad-hessian-vector": "theory/math/automatic-differentiation/forward-mode",
    "forward-ad-linear-solve": "theory/math/automatic-differentiation/forward-mode",
    "forward-ad-sparse-packing": "theory/math/automatic-differentiation/forward-mode",
    "forward-ad-softmax-tangent": "theory/math/automatic-differentiation/forward-mode",
    "forward-ad-matmul-tangent": "theory/math/automatic-differentiation/forward-mode",
    "forward-ad-finite-difference": "theory/math/automatic-differentiation/forward-mode",
    "forward-ad-normalization-jvp": "theory/math/automatic-differentiation/forward-mode",
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
    "ddm-first-passage": "brain-mind/decision-reward/diffusion-model/index",
    "mbmf-revaluation": "brain-mind/decision-reward/model-based-vs-model-free/index",
    "dreamer-posterior-prior": "theory/models/world-models/dreamer",
    "dreamer-lambda-bootstrap": "theory/models/world-models/dreamer",
    "mle-bernoulli-likelihood": "theory/math/probability-statistics/maximum-likelihood",
    "map-beta-posterior": "theory/math/probability-statistics/maximum-a-posteriori",
    "nerf-volume-rendering": "theory/models/computer-vision/3d-and-neural-rendering/nerf",
    "rao-ballard-residual": "brain-mind/predictive-coding/rao-ballard-1999/index",
    "predictive-local-settling": "brain-mind/predictive-coding/whittington-bogacz-2017/index",
    "iou-overlap-sweep": "theory/evaluation/metrics/segmentation/iou",
    "dice-overlap-response": "theory/evaluation/metrics/segmentation/dice",
    "ddpm-progressive-noising": "theory/paradigms/unsupervised/density-and-generative-models/diffusion/ddpm",
    "ddim-strided-sampling": "theory/paradigms/unsupervised/density-and-generative-models/diffusion/ddim",
    "ddim-eta-coefficients": "theory/paradigms/unsupervised/density-and-generative-models/diffusion/ddim",
}
# Canvas contracts are review-time literals, never inferred from the SVG under test.
# Every new TOPICS entry must explicitly declare its reviewed geometry here.
CANONICAL_VIEWBOXES = {'3d-unet-context-tiling': '0 0 800 420',
 '3d-unet-depth-kernel': '0 0 800 420',
 '3d-unet-evaluation-holdout': '0 0 800 420',
 '3d-unet-orthogonal-slices': '0 0 640 360',
 '3d-unet-paired-warp': '0 0 800 420',
 '3d-unet-skip-concat': '0 0 800 420',
 '3d-unet-sparse-context-gradient': '0 0 640 360',
 '3d-unet-sparse-loss': '0 0 800 420',
 'a3c-async-gradient': '0 0 640 360',
 'a3c-nstep-return': '0 0 640 360',
 'accuracy-prevalence': '0 0 640 360',
 'act-cvae-train-deploy': '0 0 640 360',
 'act-temporal-ensemble': '0 0 640 360',
 'activity-silent-trace': '0 0 640 360',
 'adafactor-factored-moments': '0 0 720 460',
 'adagrad-coordinate-gain': '0 0 720 460',
 'adam-bias-correction': '0 0 800 420',
 'adam-epsilon-threshold': '0 0 800 420',
 'adam-scale-invariance': '0 0 800 420',
 'adam-sign-reversal': '0 0 800 420',
 'adamw-decoupled-paths': '0 0 640 360',
 'adamw-epoch-timescale': '0 0 640 360',
 'aging-evolution-queue': '0 0 640 360',
 'alibi-content-recency': '0 0 640 360',
 'alibi-distance-softmax': '0 0 640 360',
 'alibi-head-prefix': '0 0 640 360',
 'alpha-beta-cutoff': '0 0 640 360',
 'alphazero-policy-target': '0 0 640 360',
 'alphazero-puct-select': '0 0 640 360',
 'alphazero-selfplay-labels': '0 0 640 360',
 'alphazero-value-backup': '0 0 640 360',
 'ant-colony-pheromone': '0 0 640 360',
 'ar-context-drift': '0 0 800 420',
 'ar-eos-survival': '0 0 800 420',
 'ar-likelihood-accumulation': '0 0 800 420',
 'ar-score-vs-sample': '0 0 800 420',
 'asam-neighborhood': '0 0 640 360',
 'astar-frontier': '0 0 640 360',
 'auc-ap-ranking-contrast': '0 0 640 360',
 'awq-salient-scaling': '0 0 640 360',
 'backdoor-standardisation': '0 0 800 430',
 'bahdanau-alignment-context': '0 0 640 360',
 'batch-norm-train-infer': '0 0 640 360',
 'bo-expected-improvement': '0 0 640 360',
 'bo-gp-conditioning': '0 0 640 360',
 'boosting-residual-steps': '0 0 640 360',
 'bpe-ordered-merges': '0 0 640 360',
 'bpr-gradient-saturation': '0 0 800 420',
 'bpr-pairwise-ranking': '0 0 800 420',
 'byol-online-target': '0 0 640 360',
 'causal-lamp-intervention': '0 0 640 360',
 'cfg-extrapolation': '0 0 640 360',
 'cfm-conditional-bridge': '0 0 760 410',
 'checkpoint-recompute': '0 0 640 360',
 'cliff-walking': '0 0 440 548',
 'clr-triangular2-sweep': '0 0 640 360',
 'cmaes-distribution-adaptation': '0 0 640 360',
 'coherence-phase-gating': '0 0 640 360',
 'colbert-maxsim-switch': '0 0 640 360',
 'collider-selection': '0 0 800 430',
 'commnet-layer-iterations': '0 0 640 360',
 'commnet-leave-one-out': '0 0 640 360',
 'conformal-alpha-staircase': '0 0 640 360',
 'conformal-aps-cumulative': '0 0 640 360',
 'conformal-cqr-expansion': '0 0 640 360',
 'conformal-mondrian-groups': '0 0 640 360',
 'conformal-raps-penalty': '0 0 640 360',
 'conformal-shift-coverage': '0 0 640 360',
 'conformal-subgroup-coverage': '0 0 640 360',
 'conformal-weighted-quantile': '0 0 640 360',
 'consistency-trajectory-map': '0 0 800 420',
 'copycat-action-lag': '0 0 640 360',
 'cv-fold-rotation': '0 0 640 360',
 'dagger-dataset-aggregation': '0 0 640 360',
 'dart-noisy-expert-recovery': '0 0 640 360',
 'darts-soft-operations': '0 0 640 360',
 'ddim-eta-coefficients': '0 0 800 420',
 'ddim-strided-sampling': '0 0 640 360',
 'ddm-first-passage': '0 0 640 360',
 'ddpg-actor-gradient': '0 0 640 360',
 'ddpg-ou-noise': '0 0 640 360',
 'ddpg-polyak-target': '0 0 640 360',
 'ddpg-replay-bootstrap': '0 0 640 360',
 'ddpm-progressive-noising': '0 0 640 360',
 'deep-ensemble-spread': '0 0 720 400',
 'deformable-sampling': '0 0 640 360',
 'deit-dual-head-distillation': '0 0 640 360',
 'dial-dru-train-execute': '0 0 640 360',
 'dice-overlap-response': '0 0 640 360',
 'diffusion-policy-denoising': '0 0 640 360',
 'diffusion-policy-multimodal-actions': '0 0 640 360',
 'diffusion-policy-noise-training': '0 0 640 360',
 'diffusion-policy-receding-horizon': '0 0 640 360',
 'dinov2-dual-objective-ema': '0 0 640 360',
 'disaggregated-handoff': '0 0 640 360',
 'dora-independent': '0 0 640 360',
 'double-dqn-selector': '0 0 440 634',
 'dpll-backtrack': '0 0 640 360',
 'dpo-preference-margin': '0 0 760 420',
 'dpr-dot-product-sweep': '0 0 640 360',
 'dqn-target-sync': '0 0 640 360',
 'dreamer-lambda-bootstrap': '0 0 640 360',
 'dreamer-posterior-prior': '0 0 640 360',
 'dropblock-spatial-masking': '0 0 640 360',
 'dropout-inverted-sampling': '0 0 640 360',
 'dropout-variance-tradeoff': '0 0 640 360',
 'dt-causal-prefix': '0 0 640 360',
 'dt-return-budget': '0 0 640 360',
 'ece-binned-calibration': '0 0 720 400',
 'effective-number-growth': '0 0 640 360',
 'eigen-jordan-shear': '0 0 800 420',
 'eigen-linear-map': '0 0 800 420',
 'eigen-rotation-no-real': '0 0 800 420',
 'eigen-zero-eigenvalue': '0 0 800 420',
 'eligibility-trace-cut': '0 0 440 598',
 'elo-online-update': '0 0 640 360',
 'enas-shared-weight-transfer': '0 0 800 420',
 'eprop-local-credit': '0 0 640 360',
 'ewc-fisher-springs': '0 0 640 360',
 'expert-cache-miss': '0 0 640 360',
 'f1-harmonic-gap': '0 0 640 360',
 'f1-macro-micro-imbalance': '0 0 640 360',
 'f1-threshold-topk': '0 0 640 360',
 'fbeta-recall-emphasis': '0 0 640 360',
 'fedavg-weighted-round': '0 0 640 360',
 'fgsm-sign-step': '0 0 640 360',
 'fitnets-hint-then-output': '0 0 720 400',
 'fixmatch-confidence-gate': '0 0 640 360',
 'flashattention-backward-remat': '0 0 640 360',
 'flashattention-causal-tiles': '0 0 640 360',
 'flashattention-exact-merge': '0 0 640 322',
 'flashattention-online-rescale': '0 0 640 322',
 'flashattention2-query-parallel': '0 0 640 360',
 'flashattention3-load-compute-pipeline': '0 0 640 360',
 'forest-bootstrap-vote': '0 0 640 360',
 'forward-ad-branch-kink': '0 0 800 420',
 'forward-ad-directional-jvp': '0 0 800 420',
 'forward-ad-dual-chain': '0 0 800 420',
 'forward-ad-finite-difference': '0 0 800 420',
 'forward-ad-hessian-vector': '0 0 800 420',
 'forward-ad-jacobian-columns': '0 0 800 420',
 'forward-ad-jvp': '0 0 640 360',
 'forward-ad-linear-solve': '0 0 800 420',
 'forward-ad-loop-tangent': '0 0 800 420',
 'forward-ad-matmul-tangent': '0 0 800 420',
 'forward-ad-normalization-jvp': '0 0 800 420',
 'forward-ad-softmax-tangent': '0 0 800 420',
 'forward-ad-sparse-packing': '0 0 800 420',
 'forward-prediction-correction': '0 0 640 360',
 'fp16-loss-scaling': '0 0 640 360',
 'fp8-scale-range': '0 0 640 360',
 'ftw-two-level-learning': '0 0 640 360',
 'gat-aggregation': '0 0 640 360',
 'gated-sae-gate-magnitude': '0 0 640 360',
 'gaussian-splat-alpha-composite': '0 0 640 360',
 'gcn-aggregation': '0 0 640 360',
 'genetic-crossover-mutation': '0 0 640 360',
 'gibbs-coordinate-sweeps': '0 0 640 360',
 'gin-multiset-counts': '0 0 640 360',
 'glorot-alternating-width': '0 0 640 360',
 'glorot-equal-variance-densities': '0 0 640 360',
 'glorot-fan-tradeoff': '0 0 640 360',
 'glorot-tanh-saturation': '0 0 640 360',
 'gnm-speed-normalization': '0 0 640 360',
 'gptq-error-compensation': '0 0 640 360',
 'gqa-head-sharing': '0 0 640 360',
 'gqa-uptraining-pooling': '0 0 640 360',
 'gradient-accumulation-clipping-order': '0 0 800 420',
 'gradient-agc-relative-cap': '0 0 800 420',
 'gradient-amp-unscale-order': '0 0 800 420',
 'gradient-clipping-comparison': '0 0 800 420',
 'gradient-decoupled-decay': '0 0 800 420',
 'gradient-global-layer-budget': '0 0 800 420',
 'gradient-norm-clipping': '0 0 640 360',
 'graphplan-layer-extraction': '0 0 640 360',
 'graphsage-sample-aggregate': '0 0 640 360',
 'grid-search-x-coverage': '0 0 640 360',
 'group-norm-statistics': '0 0 640 360',
 'grpo-group-advantages': '0 0 760 400',
 'gru-gate-flow': '0 0 640 360',
 'h2o-heavy-hitter-selection': '0 0 640 360',
 'he-fan-mode-tradeoff': '0 0 640 360',
 'he-relu-mean-shift': '0 0 640 360',
 'he-relu-second-moment': '0 0 640 360',
 'heavy-ball-overshoot': '0 0 640 360',
 'hmc-leapfrog-trajectory': '0 0 640 360',
 'hmm-baum-welch-transition': '0 0 800 420',
 'hmm-filter-smooth': '0 0 800 420',
 'hmm-forward-sum-product': '0 0 800 420',
 'hmm-pairwise-posterior': '0 0 800 420',
 'hnsw-layer-descent': '0 0 640 360',
 'hyperband-budget': '0 0 640 360',
 'i3d-filter-inflation': '0 0 800 440',
 'ia3-channel-gates': '0 0 640 360',
 'icm-forward-inverse': '0 0 680 370',
 'icm-predictable-stochastic': '0 0 760 390',
 'ida-bound-reexpansion': '0 0 640 360',
 'integrated-gradients-path': '0 0 640 360',
 'iou-overlap-sweep': '0 0 640 360',
 'itemcf-weighted-neighbors': '0 0 800 420',
 'ivfpq-probe-pq-lookup': '0 0 640 360',
 'jumprelu-threshold-jump': '0 0 640 360',
 'kalman-gain-fusion': '0 0 640 360',
 'kd-soft-target-alignment': '0 0 720 400',
 'kfac-factor-preconditioning': '0 0 640 360',
 'kivi-quantization-axis': '0 0 640 360',
 'kmeans-elbow-inertia': '0 0 800 420',
 'kmeans-feature-scale': '0 0 800 420',
 'kmeans-lloyd': '0 0 640 360',
 'kmeans-outlier-leverage': '0 0 800 420',
 'kmeans-plusplus-d2': '0 0 800 420',
 'lagrange-dual-gap': '0 0 640 360',
 'lagrange-kkt-active-set': '0 0 640 360',
 'lagrange-tangency': '0 0 640 360',
 'lamb-adam-layer-trust': '0 0 640 360',
 'large-batch-warmup-ramp': '0 0 640 360',
 'lars-layer-trust-scaling': '0 0 640 360',
 'latent-space-denoise': '0 0 800 436',
 'layernorm-feature-shift': '0 0 860 440',
 'lbfgs-two-loop': '0 0 640 360',
 'lime-local-surrogate': '0 0 640 360',
 'lion-sign-momentum': '0 0 640 360',
 'logit-prior-decision': '0 0 640 360',
 'lsq-step-size-sweep': '0 0 640 360',
 'maddpg-actor-gradient': '0 0 640 360',
 'maddpg-joint-bootstrap': '0 0 640 360',
 'mae-visible-patch-reconstruction': '0 0 640 360',
 'mahalanobis-ellipse-threshold': '0 0 640 360',
 'mamba2-ssd-causal-map': '0 0 860 440',
 'maml-inner-outer-loop': '0 0 640 360',
 'map-beta-posterior': '0 0 640 360',
 'map-elites-archive': '0 0 640 360',
 'map-precision-at-hits': '0 0 640 360',
 'mappo-backward-gae': '0 0 640 360',
 'mappo-shared-advantage': '0 0 640 360',
 'mbmf-revaluation': '0 0 640 360',
 'mbpo-horizon-error': '0 0 640 360',
 'mbpo-short-branches': '0 0 640 360',
 'mc-dropout-repeated-passes': '0 0 640 360',
 'mcts-search-cycle': '0 0 640 360',
 'mean-field-coordinate-ascent': '0 0 640 360',
 'mean-teacher-ema-tracking': '0 0 640 360',
 'mf-als-alternating': '0 0 800 420',
 'mf-coupled-sgd': '0 0 800 420',
 'mh-accept-reject': '0 0 640 360',
 'minhash-lsh-band-collision': '0 0 640 360',
 'mixup-beta-strength': '0 0 640 360',
 'mixup-cutmix-area': '0 0 640 360',
 'mixup-loss-decomposition': '0 0 640 360',
 'mixup-paired-interpolation': '0 0 640 360',
 'mle-bernoulli-likelihood': '0 0 640 360',
 'mnasnet-latency-tradeoff': '0 0 800 420',
 'moco-dictionary-cycle': '0 0 640 360',
 'moe-top2-routing': '0 0 640 360',
 'muon-spectral-balancing': '0 0 640 360',
 'mup-adam-sgd': '0 0 640 360',
 'mup-readout-aggregation': '0 0 640 360',
 'mup-readout-noise': '0 0 640 360',
 'mup-transfer-protocol': '0 0 640 360',
 'mup-transfer-validation': '0 0 640 360',
 'mup-update-budget': '0 0 640 360',
 'mup-width-multipliers': '0 0 640 360',
 'muzero-latent-planning': '0 0 640 360',
 'ndcg-position-discount': '0 0 640 360',
 'neat-add-node-innovation': '0 0 640 360',
 'nerf-volume-rendering': '0 0 640 360',
 'nesterov-lookahead': '0 0 640 360',
 'neumf-dual-path': '0 0 800 420',
 'newton-armijo-backtracking': '0 0 640 360',
 'newton-curvature-steps': '0 0 640 360',
 'newton-indefinite-curvature': '0 0 640 360',
 'nomad-goal-mask-routing': '0 0 640 360',
 'nstep-lambda-forward': '0 0 520 626',
 'odin-gradient-perturbation': '0 0 640 360',
 'ofc-selective-feedback': '0 0 640 360',
 'offline-cql-conservative': '0 0 440 548',
 'offline-iql-expectile': '0 0 440 548',
 'openvla-dual-encoder-fusion': '0 0 640 360',
 'openvla-percentile-action-bins': '0 0 640 360',
 'orca-continuous-batching': '0 0 640 360',
 'outlier-mae-rmse': '0 0 640 360',
 'paged-block-mapping': '0 0 640 360',
 'paired-bootstrap-resampling': '0 0 640 360',
 'particle-swarm-best': '0 0 640 360',
 'particle-weight-resampling': '0 0 640 360',
 'pbt-exploit-explore': '0 0 640 360',
 'pbwm-gate': '0 0 640 360',
 'pca-rank1-reconstruction': '0 0 640 360',
 'pca-variance-axis': '0 0 640 360',
 'pets-cem-refit': '0 0 640 360',
 'pets-ensemble-particles': '0 0 640 360',
 'pgd-projection-path': '0 0 640 360',
 'place-cell-firing': '0 0 640 360',
 'power-iteration-convergence': '0 0 640 360',
 'power-iteration-projection-contraction': '0 0 640 360',
 'ppo-clipped-objective': '0 0 640 360',
 'pr-ap-rectangles': '0 0 640 360',
 'pr-ap-tied-threshold': '0 0 640 360',
 'pr-ap-trapezoid-gap': '0 0 640 360',
 'pr-random-ap-expectation': '0 0 640 360',
 'pr-threshold-sweep': '0 0 640 360',
 'precision-base-rate': '0 0 640 360',
 'precision-recall-threshold': '0 0 640 360',
 'predictive-local-settling': '0 0 640 360',
 'prefix-kv-attention': '0 0 640 360',
 'prelu-slope-gain': '0 0 640 360',
 'prioritized-replay-cycle': '0 0 640 360',
 'prompt-injection-boundary': '0 0 640 360',
 'q-sarsa-backup': '0 0 640 360',
 'q-sarsa-epsilon': '0 0 440 630',
 'q-sarsa-noisy-backups': '0 0 440 644',
 'qat-fake-quant-ste': '0 0 640 360',
 'qk-norm-scale-sweep': '0 0 640 360',
 'qlora-frozen-flow': '0 0 640 360',
 'qmix-monotonic-greedy': '0 0 640 360',
 'r2-mean-baseline': '0 0 640 360',
 'rainbow-c51-projection': '0 0 440 548',
 'rainbow-dueling-head': '0 0 440 548',
 'rainbow-noisynet-samples': '0 0 440 548',
 'rainbow-nstep-returns': '0 0 440 548',
 'random-search-x-coverage': '0 0 640 360',
 'rao-ballard-residual': '0 0 640 360',
 'react-evidence-loop': '0 0 640 360',
 'realnvp-affine-coupling': '0 0 640 360',
 'rectified-reflow-coupling': '0 0 760 410',
 'recursive-tail-loss': '0 0 640 360',
 'reflexion-memory-feedback': '0 0 640 360',
 'reinforce-return-credit': '0 0 760 400',
 'reinforce-reward-to-go': '0 0 640 360',
 'resnet-depth-gradient-factors': '0 0 800 420',
 'resnet-identity-gradient': '0 0 800 420',
 'resnet-postrelu-gate': '0 0 800 420',
 'resnet-projection-shortcut': '0 0 800 420',
 'resolution-refutation-chain': '0 0 640 360',
 'reverse-ad-vjp': '0 0 640 360',
 'rf-bootstrap-oob': '0 0 800 420',
 'rf-feature-subset': '0 0 800 420',
 'rial-dial-credit-path': '0 0 640 360',
 'rlhf-dpo-margin': '0 0 640 360',
 'rlhf-reward-sums': '0 0 640 360',
 'rmsnorm-shift-response': '0 0 640 360',
 'rmsprop-adaptive-memory': '0 0 640 360',
 'rnd-prediction-error': '0 0 680 370',
 'rnd-state-novelty': '0 0 680 370',
 'roc-fpr-batch': '0 0 640 360',
 'roc-fpr-zero-alarms': '0 0 640 360',
 'roc-fpr-budget-mix': '0 0 640 360',
 'roc-pr-shift': '0 0 640 360',
 'roc-prior-policy': '0 0 640 360',
 'roc-youden-cost': '0 0 640 360',
 'roc-cost-operating-point': '0 0 640 360',
 'roc-pairwise-auc': '0 0 640 360',
 'roc-partial-area': '0 0 640 360',
 'roc-randomized-operating-mix': '0 0 640 360',
 'roc-rank-transform': '0 0 640 360',
 'roc-threshold-sweep': '0 0 640 360',
 'roc-tie-half-credit': '0 0 640 360',
 'roi-align-sampling': '0 0 800 460',
 'roofline-ridge-sweep': '0 0 640 360',
 'rope-axial-2d': '0 0 640 360',
 'rope-cache-reindex': '0 0 640 360',
 'rope-frequency-bands': '0 0 640 360',
 'rope-interpolation-angle': '0 0 640 360',
 'rotational-norm-balance': '0 0 640 360',
 'rt2-action-token-decoding': '0 0 640 360',
 's4d-diagonal-modes': '0 0 860 440',
 'sac-entropy-temperature': '0 0 760 420',
 'sac-soft-target': '0 0 640 360',
 'sac-temperature-feedback': '0 0 640 360',
 'saliency-local-gradient': '0 0 640 360',
 'sam-prompt-ambiguity': '0 0 800 460',
 'sam-two-gradient': '0 0 640 360',
 'saycan-skill-grounding': '0 0 640 360',
 'score-sde-flow': '0 0 800 420',
 'secagg-mask-cancellation': '0 0 640 360',
 'self-instruct-filter-loop': '0 0 640 360',
 'seq2seq-context-handoff': '0 0 860 440',
 'sgd-noise-batch': '0 0 640 360',
 'shampoo-eigenmode': '0 0 640 360',
 'shap-coalition-marginals': '0 0 640 360',
 'sharpness-radius-loss': '0 0 640 360',
 'sharpness-reparam-curvature': '0 0 640 360',
 'shaw-relative-clipping': '0 0 640 360',
 'shaw-relative-value': '0 0 640 360',
 'sigma-reparam-spectral-gain': '0 0 640 360',
 'simclr-temperature-competition': '0 0 640 360',
 'sinusoidal-multiscale': '0 0 640 360',
 'soap-eigenbasis-adam': '0 0 640 360',
 'speculative-decoding': '0 0 640 360',
 'spsa-two-evaluations': '0 0 640 360',
 'stdp-spike-timing': '0 0 640 360',
 'stochastic-depth-paths': '0 0 640 360',
 'stochastic-depth-scaling-conventions': '0 0 640 360',
 'stochastic-depth-survival-samples': '0 0 640 360',
 'streaming-kv-eviction': '0 0 640 360',
 'strips-state-effects': '0 0 640 360',
 'successor-occupancy': '0 0 640 360',
 'svd-degenerate-bases': '0 0 800 420',
 'svd-ls-orthogonal-residual': '0 0 800 420',
 'svd-noise-amplification': '0 0 800 420',
 'svd-rank-accumulation': '0 0 800 420',
 'svd-unit-circle': '0 0 640 360',
 'svi-minibatch-global': '0 0 640 360',
 'svm-margin-hinge': '0 0 640 360',
 'swin-shifted-windows': '0 0 640 360',
 't5-span-corruption': '0 0 640 360',
 'td-terminal-truncation': '0 0 440 602',
 'td3-delayed-twin-critics': '0 0 640 360',
 'theta-gamma-phase-amplitude': '0 0 640 360',
 'thompson-beta-posterior-draws': '0 0 860 464',
 'thompson-evidence-concentration': '0 0 860 464',
 'tree-belief-propagation': '0 0 640 360',
 'trpo-kl-backtracking': '0 0 640 360',
 'trpo-ratio-surrogate': '0 0 640 360',
 'tsne-kl-embedding': '0 0 640 360',
 'ucb1-bonus-sensitivity': '0 0 860 464',
 'ucb1-optimism-switch': '0 0 860 464',
 'umap-fuzzy-union': '0 0 640 360',
 'unigram-sampling-alpha': '0 0 640 360',
 'unigram-viterbi-lattice': '0 0 640 360',
 'vae-reparameterisation': '0 0 640 360',
 'video-joint-denoising': '0 0 800 436',
 'ving-learned-graph-routing': '0 0 640 360',
 'vint-goal-waypoint-flow': '0 0 640 360',
 'viterbi-trellis': '0 0 640 360',
 'vivit-factorised-attention': '0 0 800 440',
 'vqvae-codebook-snap': '0 0 640 360',
 'watermark-greenlist-score': '0 0 640 360',
 'weak-supervision-vote-fusion': '0 0 640 360',
 'wgan-gp-interpolation': '0 0 640 360',
 'wgan-weight-clip': '0 0 640 360',
 'yarn-attention-temperature': '0 0 640 360',
 'yarn-frequency-ramp': '0 0 640 360'}
# Explicit non-TOPICS assets validated by main(), not generic name allowances.
EXTRA_CANONICAL_FILENAMES = {'brier-expected-risk-motion.svg': '0 0 640 360',
 'brier-expected-risk-still.svg': '0 0 640 360',
 'icm-predictable-stochastic-mobile-motion.svg': '0 0 380 770',
 'icm-predictable-stochastic-mobile-still.svg': '0 0 380 770',
 'log-loss-tail-penalty-motion.svg': '0 0 640 360',
 'log-loss-tail-penalty-still.svg': '0 0 640 360',
 'moe-top2-routing-token-b.svg': '0 0 640 360',
 'rnd-state-novelty-mobile-motion.svg': '0 0 380 660',
 'rnd-state-novelty-mobile-still.svg': '0 0 380 660'}
# Preserve original source prefix contracts, including their valid named variants.
PREFIX_VIEWBOXES = {'backdoor-standardisation-': '0 0 800 430',
 'cfm-conditional-bridge': '0 0 760 410',
 'collider-selection-': '0 0 800 430',
 'deep-ensemble-spread': '0 0 720 400',
 'dpo-preference-margin-': '0 0 760 420',
 'ece-binned-calibration': '0 0 720 400',
 'fitnets-hint-then-output-': '0 0 720 400',
 'flashattention-exact-merge-': '0 0 640 322',
 'flashattention-online-rescale-': '0 0 640 322',
 'forward-ad-': '0 0 800 420',
 'i3d-filter-inflation-': '0 0 800 440',
 'icm-forward-inverse-': '0 0 680 370',
 'icm-predictable-stochastic-': '0 0 760 390',
 'icm-predictable-stochastic-mobile-': '0 0 380 770',
 'kd-soft-target-alignment-': '0 0 720 400',
 'mamba2-ssd-causal-map-': '0 0 860 440',
 'rainbow-': '0 0 440 548',
 'rectified-reflow-coupling': '0 0 760 410',
 'rnd-prediction-error-': '0 0 680 370',
 'rnd-state-novelty-': '0 0 680 370',
 'rnd-state-novelty-mobile-': '0 0 380 660',
 's4d-diagonal-modes-': '0 0 860 440',
 'sac-entropy-temperature-': '0 0 760 420',
 'thompson-beta-posterior-draws-': '0 0 860 464',
 'thompson-evidence-concentration-': '0 0 860 464',
 'ucb1-bonus-sensitivity-': '0 0 860 464',
 'ucb1-optimism-switch-': '0 0 860 464',
 'vivit-factorised-attention-': '0 0 800 440'}


PREFIX_EXCLUSIONS = {'forward-ad-': ('forward-ad-jvp-',)}

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
               if name.startswith(prefix) and not any(name.startswith(excluded) for excluded in PREFIX_EXCLUSIONS.get(prefix, ()))]
    if not matches:
        return None
    longest = max(len(prefix) for prefix, _ in matches)
    boxes = {box for prefix, box in matches if len(prefix) == longest}
    return next(iter(boxes)) if len(boxes) == 1 else None


# Independently restored original page contracts; never inferred from image URLs.
SOURCE_ALT_CONTRACT_STEMS = {'a3c-async-gradient',
 'a3c-nstep-return',
 'act-cvae-train-deploy',
 'act-temporal-ensemble',
 'alphazero-policy-target',
 'alphazero-puct-select',
 'alphazero-selfplay-labels',
 'alphazero-value-backup',
 'cfm-conditional-bridge',
 'commnet-layer-iterations',
 'commnet-leave-one-out',
 'dagger-dataset-aggregation',
 'dart-noisy-expert-recovery',
 'ddim-eta-coefficients',
 'ddim-strided-sampling',
 'ddpg-actor-gradient',
 'ddpg-ou-noise',
 'ddpg-polyak-target',
 'ddpg-replay-bootstrap',
 'ddpm-progressive-noising',
 'dial-dru-train-execute',
 'diffusion-policy-denoising',
 'diffusion-policy-multimodal-actions',
 'diffusion-policy-noise-training',
 'diffusion-policy-receding-horizon',
 'dora-independent',
 'dreamer-lambda-bootstrap',
 'dreamer-posterior-prior',
 'eprop-local-credit',
 'expert-cache-miss',
 'fedavg-weighted-round',
 'flashattention-backward-remat',
 'flashattention-causal-tiles',
 'flashattention-exact-merge',
 'flashattention-online-rescale',
 'flashattention2-query-parallel',
 'flashattention3-load-compute-pipeline',
 'forward-prediction-correction',
 'ftw-two-level-learning',
 'gin-multiset-counts',
 'gnm-speed-normalization',
 'gqa-head-sharing',
 'gqa-uptraining-pooling',
 'graphsage-sample-aggregate',
 'grpo-group-advantages',
 'h2o-heavy-hitter-selection',
 'hnsw-layer-descent',
 'ia3-channel-gates',
 'ivfpq-probe-pq-lookup',
 'kivi-quantization-axis',
 'maddpg-actor-gradient',
 'maddpg-joint-bootstrap',
 'mappo-backward-gae',
 'mappo-shared-advantage',
 'mbpo-horizon-error',
 'mbpo-short-branches',
 'minhash-lsh-band-collision',
 'nomad-goal-mask-routing',
 'ofc-selective-feedback',
 'openvla-dual-encoder-fusion',
 'openvla-percentile-action-bins',
 'paged-block-mapping',
 'pbt-exploit-explore',
 'pets-cem-refit',
 'pets-ensemble-particles',
 'prefix-kv-attention',
 'prompt-injection-boundary',
 'qk-norm-scale-sweep',
 'qlora-frozen-flow',
 'rectified-reflow-coupling',
 'reinforce-reward-to-go',
 'rial-dial-credit-path',
 'rlhf-dpo-margin',
 'rlhf-reward-sums',
 'rt2-action-token-decoding',
 'sac-soft-target',
 'sac-temperature-feedback',
 'saycan-skill-grounding',
 'secagg-mask-cancellation',
 'sigma-reparam-spectral-gain',
 'stdp-spike-timing',
 'trpo-kl-backtracking',
 'trpo-ratio-surrogate',
 'tsne-kl-embedding',
 'umap-fuzzy-union',
 'unigram-sampling-alpha',
 'unigram-viterbi-lattice',
 'ving-learned-graph-routing',
 'vint-goal-waypoint-flow',
 'watermark-greenlist-score',
 'weak-supervision-vote-fusion'}
STATIC_PREVIEW_LINK_STEMS = {'a3c-async-gradient',
 'a3c-nstep-return',
 'act-cvae-train-deploy',
 'act-temporal-ensemble',
 'alphazero-policy-target',
 'alphazero-puct-select',
 'alphazero-selfplay-labels',
 'alphazero-value-backup',
 'awq-salient-scaling',
 'cfm-conditional-bridge',
 'clr-triangular2-sweep',
 'coherence-phase-gating',
 'commnet-layer-iterations',
 'commnet-leave-one-out',
 'conformal-alpha-staircase',
 'conformal-aps-cumulative',
 'conformal-cqr-expansion',
 'conformal-mondrian-groups',
 'conformal-raps-penalty',
 'conformal-shift-coverage',
 'conformal-subgroup-coverage',
 'conformal-weighted-quantile',
 'dagger-dataset-aggregation',
 'dart-noisy-expert-recovery',
 'ddpg-actor-gradient',
 'ddpg-ou-noise',
 'ddpg-polyak-target',
 'ddpg-replay-bootstrap',
 'deep-ensemble-spread',
 'deit-dual-head-distillation',
 'dial-dru-train-execute',
 'diffusion-policy-denoising',
 'diffusion-policy-multimodal-actions',
 'diffusion-policy-noise-training',
 'diffusion-policy-receding-horizon',
 'dreamer-lambda-bootstrap',
 'dreamer-posterior-prior',
 'ece-binned-calibration',
 'eprop-local-credit',
 'fedavg-weighted-round',
 'fgsm-sign-step',
 'fixmatch-confidence-gate',
 'forward-ad-branch-kink',
 'forward-ad-directional-jvp',
 'forward-ad-dual-chain',
 'forward-ad-finite-difference',
 'forward-ad-hessian-vector',
 'forward-ad-jacobian-columns',
 'forward-ad-linear-solve',
 'forward-ad-loop-tangent',
 'forward-ad-matmul-tangent',
 'forward-ad-normalization-jvp',
 'forward-ad-softmax-tangent',
 'forward-ad-sparse-packing',
 'ftw-two-level-learning',
 'gaussian-splat-alpha-composite',
 'gin-multiset-counts',
 'gnm-speed-normalization',
 'gptq-error-compensation',
 'gqa-head-sharing',
 'gqa-uptraining-pooling',
 'gradient-accumulation-clipping-order',
 'gradient-agc-relative-cap',
 'gradient-amp-unscale-order',
 'gradient-clipping-comparison',
 'gradient-decoupled-decay',
 'gradient-global-layer-budget',
 'graphplan-layer-extraction',
 'graphsage-sample-aggregate',
 'grpo-group-advantages',
 'h2o-heavy-hitter-selection',
 'hnsw-layer-descent',
 'ia3-channel-gates',
 'icm-forward-inverse',
 'icm-predictable-stochastic',
 'integrated-gradients-path',
 'ivfpq-probe-pq-lookup',
 'kalman-gain-fusion',
 'kivi-quantization-axis',
 'maddpg-actor-gradient',
 'maddpg-joint-bootstrap',
 'mappo-backward-gae',
 'mappo-shared-advantage',
 'mbpo-horizon-error',
 'mbpo-short-branches',
 'mean-teacher-ema-tracking',
 'minhash-lsh-band-collision',
 'nomad-goal-mask-routing',
 'openvla-dual-encoder-fusion',
 'openvla-percentile-action-bins',
 'particle-weight-resampling',
 'pbt-exploit-explore',
 'pets-cem-refit',
 'pets-ensemble-particles',
 'pgd-projection-path',
 'place-cell-firing',
 'predictive-local-settling',
 'prefix-kv-attention',
 'prompt-injection-boundary',
 'rao-ballard-residual',
 'rectified-reflow-coupling',
 'reinforce-reward-to-go',
 'rial-dial-credit-path',
 'rlhf-dpo-margin',
 'rlhf-reward-sums',
 'rnd-prediction-error',
 'rnd-state-novelty',
 'rt2-action-token-decoding',
 'sac-soft-target',
 'sac-temperature-feedback',
 'saliency-local-gradient',
 'saycan-skill-grounding',
 'secagg-mask-cancellation',
 'stdp-spike-timing',
 'strips-state-effects',
 'successor-occupancy',
 't5-span-corruption',
 'theta-gamma-phase-amplitude',
 'trpo-kl-backtracking',
 'trpo-ratio-surrogate',
 'ving-learned-graph-routing',
 'vint-goal-waypoint-flow',
 'vqvae-codebook-snap',
 'watermark-greenlist-score',
 'weak-supervision-vote-fusion'}

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
            if value.strip().lower() in {"nan", "+nan", "-nan", "inf", "+inf", "-inf", "infinity", "+infinity", "-infinity"}:
                errors.append(f"{path}: non-finite numeric SVG attribute {local_key}={value!r}")
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
        if stem == "rnd-state-novelty":
            # A mobile-first stacked diagram; require both motion and fallback.
            errors.extend(verify_svg(ASSETS / f"{stem}-mobile-motion.svg", True))
            errors.extend(verify_svg(ASSETS / f"{stem}-mobile-still.svg", False))
        if stem == "icm-predictable-stochastic":
            # The MkDocs player selects this legible stacked layout on narrow
            # screens. Both variants must be valid, self-contained and accessible.
            errors.extend(verify_svg(ASSETS / f"{stem}-mobile-motion.svg", True))
            errors.extend(verify_svg(ASSETS / f"{stem}-mobile-still.svg", False))
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
            # The site enhances GitHub-readable <img> fallbacks via data-motion-src.
            links.extend(re.findall(r'data-motion-src="([^"]+\.svg)"', text))
            linked_images = {(page.parent / link).resolve() for link in links}
            if ((stem in NAS_STEMS | {"ddim-eta-coefficients", "ddim-strided-sampling", "ddpm-progressive-noising", "gqa-head-sharing", "gqa-uptraining-pooling"}) or (stem.startswith("ddpg-"))) or (stem in NAS_STEMS or stem.startswith("rainbow-")) or stem.startswith(("rnd-", "icm-")):
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
            elif stem in {'a3c-async-gradient', 'a3c-nstep-return', 'alibi-content-recency', 'alibi-distance-softmax', 'alibi-head-prefix', 'cfm-conditional-bridge', 'deep-ensemble-spread', 'dreamer-lambda-bootstrap', 'dreamer-posterior-prior', 'ece-binned-calibration', 'fitnets-hint-then-output', 'hmm-baum-welch-transition', 'hmm-filter-smooth', 'hmm-forward-sum-product', 'hmm-pairwise-posterior', 'kd-soft-target-alignment', 'lion-sign-momentum', 'mbpo-horizon-error', 'mbpo-short-branches', 'muon-spectral-balancing', 'pets-cem-refit', 'pets-ensemble-particles', 'qk-norm-scale-sweep', 'rectified-reflow-coupling', 'rlhf-dpo-margin', 'rlhf-reward-sums', 'rope-axial-2d', 'rope-cache-reindex', 'rope-frequency-bands', 'rope-interpolation-angle', 'shaw-relative-clipping', 'shaw-relative-value', 'sigma-reparam-spectral-gain', 'sinusoidal-multiscale', 'trpo-kl-backtracking', 'trpo-ratio-surrogate', 'tsne-kl-embedding', 'umap-fuzzy-union', 'yarn-attention-temperature', 'yarn-frequency-ramp'}:
                errors.extend(verify_source_pair(page, text, stem))
            elif stem in {"roc-cost-operating-point", "pr-random-ap-expectation", "f1-threshold-topk", "roc-randomized-operating-mix", "roc-tie-half-credit", "pr-ap-tied-threshold", "roc-pairwise-auc", "pr-ap-rectangles", "precision-recall-threshold", "f1-harmonic-gap", "accuracy-prevalence", "fbeta-recall-emphasis", "precision-base-rate", "f1-macro-micro-imbalance", "roc-partial-area", "pr-ap-trapezoid-gap"}:
                errors.extend(verify_source_pair(page, text, stem))
                static_links = re.findall(r"\[[^]]+\]\(([^)]+\.svg)\)", text)
                if static_path.resolve() not in {(page.parent / link).resolve() for link in static_links}:
                    errors.append(f"{page}: missing GitHub static preview link for {stem}")
            elif stem in {"activity-silent-trace", "cfm-conditional-bridge", "consistency-trajectory-map", "deep-ensemble-spread", "ece-binned-calibration", "gated-sae-gate-magnitude", "glorot-alternating-width", "glorot-equal-variance-densities", "glorot-fan-tradeoff", "glorot-tanh-saturation", "he-fan-mode-tradeoff", "he-relu-mean-shift", "he-relu-second-moment", "hmm-baum-welch-transition", "hmm-filter-smooth", "hmm-forward-sum-product", "hmm-pairwise-posterior", "hnsw-layer-descent", "ivfpq-probe-pq-lookup", "jumprelu-threshold-jump", "latent-space-denoise", "lion-sign-momentum", "muon-spectral-balancing", "mup-adam-sgd", "mup-readout-aggregation", "mup-readout-noise", "mup-transfer-protocol", "mup-transfer-validation", "mup-update-budget", "mup-width-multipliers", "pbwm-gate", "prelu-slope-gain", "prompt-injection-boundary", "qk-norm-scale-sweep", "react-evidence-loop", "rectified-reflow-coupling", "reflexion-memory-feedback", "roi-align-sampling", "sam-prompt-ambiguity", "score-sde-flow", "sigma-reparam-spectral-gain", "tsne-kl-embedding", "umap-fuzzy-union", "unigram-sampling-alpha", "unigram-viterbi-lattice", "video-joint-denoising", "watermark-greenlist-score"}:
                errors.extend(verify_source_pair(page, text, stem))
            elif stem in {'alphazero-policy-target', 'alphazero-puct-select', 'alphazero-selfplay-labels', 'alphazero-value-backup', 'conformal-alpha-staircase', 'conformal-aps-cumulative', 'conformal-cqr-expansion', 'conformal-mondrian-groups', 'conformal-raps-penalty', 'conformal-shift-coverage', 'conformal-subgroup-coverage', 'conformal-weighted-quantile', 'itemcf-weighted-neighbors', 'neumf-dual-path'}:
                errors.extend(verify_source_pair(page, text, stem))
                static_links = re.findall(r"\[[^]]+\]\(([^)]+\.svg)\)", text)
                if static_path.resolve() not in {
                    (page.parent / link).resolve() for link in static_links
                }:
                    errors.append(f"{page}: missing GitHub-readable fallback link for {stem}")
            elif stem in {"reinforce-reward-to-go", "reinforce-return-credit", "grpo-group-advantages", "itemcf-weighted-neighbors", "neumf-dual-path"}:
                errors.extend(verify_source_pair(page, text, stem))
                static_links = re.findall(r"\[[^]]+\]\(([^)]+\.svg)\)", text)
                if static_path.resolve() not in {
                    (page.parent / link).resolve() for link in static_links
                }:
                    errors.append(f"{page}: missing GitHub-readable fallback link for {stem}")
            elif stem in {'cliff-walking', 'commnet-layer-iterations', 'commnet-leave-one-out', 'dial-dru-train-execute', 'double-dqn-selector', 'eligibility-trace-cut', 'fedavg-weighted-round', 'ftw-two-level-learning', 'gradient-accumulation-clipping-order', 'gradient-agc-relative-cap', 'gradient-amp-unscale-order', 'gradient-clipping-comparison', 'gradient-decoupled-decay', 'gradient-global-layer-budget', 'maddpg-actor-gradient', 'maddpg-joint-bootstrap', 'mappo-backward-gae', 'mappo-shared-advantage', 'nstep-lambda-forward', 'offline-cql-conservative', 'offline-iql-expectile', 'openvla-dual-encoder-fusion', 'openvla-percentile-action-bins', 'pbt-exploit-explore', 'q-sarsa-backup', 'q-sarsa-epsilon', 'q-sarsa-noisy-backups', 'rial-dial-credit-path', 'rt2-action-token-decoding', 'saycan-skill-grounding', 'secagg-mask-cancellation', 'td-terminal-truncation'}:
                errors.extend(verify_source_pair(page, text, stem))
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
            elif stem in {"t5-span-corruption", "deit-dual-head-distillation"}:
                # GitHub displays the static img; the MkDocs player reads data-motion-src.
                images = [attrs for attrs in MotionImages(text).images
                          if stem in (attrs.get("src") or "")]
                if len(images) != 1:
                    errors.append(f"{page}: expected exactly one static-first motion image")
                else:
                    for attribute, expected in (("src", static_path),
                                                ("data-motion-src", animated_path),
                                                ("data-still-src", static_path)):
                        value = images[0].get(attribute)
                        if not value or (page.parent / value).resolve() != expected.resolve():
                            errors.append(f"{page}: invalid {attribute} asset link")
                static_links = re.findall(r"\[[^]]+\]\(([^)]+\.svg)\)", text)
                linked = {(page.parent / link).resolve() for link in static_links}
                if static_path.resolve() not in linked:
                    errors.append(f"{page}: missing GitHub-readable static SVG link")
            elif stem in {'3d-unet-context-tiling', '3d-unet-depth-kernel', '3d-unet-evaluation-holdout', '3d-unet-orthogonal-slices', '3d-unet-paired-warp', '3d-unet-skip-concat', '3d-unet-sparse-context-gradient', '3d-unet-sparse-loss', 'act-cvae-train-deploy', 'act-temporal-ensemble', 'adafactor-factored-moments', 'adagrad-coordinate-gain', 'adam-bias-correction', 'adam-epsilon-threshold', 'adam-scale-invariance', 'adam-sign-reversal', 'adamw-epoch-timescale', 'ant-colony-pheromone', 'ar-context-drift', 'ar-eos-survival', 'ar-likelihood-accumulation', 'ar-score-vs-sample', 'asam-neighborhood', 'auc-ap-ranking-contrast', 'awq-salient-scaling', 'backdoor-standardisation', 'bahdanau-alignment-context', 'bo-expected-improvement', 'bo-gp-conditioning', 'boosting-residual-steps', 'bpr-gradient-saturation', 'bpr-pairwise-ranking', 'causal-lamp-intervention', 'checkpoint-recompute', 'clr-triangular2-sweep', 'coherence-phase-gating', 'colbert-maxsim-switch', 'collider-selection', 'copycat-action-lag', 'cv-fold-rotation', 'dagger-dataset-aggregation', 'dart-noisy-expert-recovery', 'dora-independent', 'dpo-preference-margin', 'dpr-dot-product-sweep', 'dropblock-spatial-masking', 'dropout-inverted-sampling', 'dropout-variance-tradeoff', 'dt-causal-prefix', 'dt-return-budget', 'effective-number-growth', 'eigen-jordan-shear', 'eigen-linear-map', 'eigen-rotation-no-real', 'eigen-zero-eigenvalue', 'elo-online-update', 'eprop-local-credit', 'ewc-fisher-springs', 'fixmatch-confidence-gate', 'forest-bootstrap-vote', 'forward-ad-branch-kink', 'forward-ad-directional-jvp', 'forward-ad-dual-chain', 'forward-ad-finite-difference', 'forward-ad-hessian-vector', 'forward-ad-jacobian-columns', 'forward-ad-linear-solve', 'forward-ad-loop-tangent', 'forward-ad-matmul-tangent', 'forward-ad-normalization-jvp', 'forward-ad-softmax-tangent', 'forward-ad-sparse-packing', 'forward-prediction-correction', 'fp16-loss-scaling', 'fp8-scale-range', 'gaussian-splat-alpha-composite', 'genetic-crossover-mutation', 'gin-multiset-counts', 'gnm-speed-normalization', 'gptq-error-compensation', 'graphplan-layer-extraction', 'graphsage-sample-aggregate', 'grid-search-x-coverage', 'group-norm-statistics', 'h2o-heavy-hitter-selection', 'heavy-ball-overshoot', 'i3d-filter-inflation', 'ia3-channel-gates', 'ida-bound-reexpansion', 'integrated-gradients-path', 'kalman-gain-fusion', 'kivi-quantization-axis', 'kmeans-elbow-inertia', 'kmeans-feature-scale', 'kmeans-outlier-leverage', 'kmeans-plusplus-d2', 'lagrange-dual-gap', 'lagrange-kkt-active-set', 'lagrange-tangency', 'lamb-adam-layer-trust', 'large-batch-warmup-ramp', 'lars-layer-trust-scaling', 'lime-local-surrogate', 'logit-prior-decision', 'lsq-step-size-sweep', 'mahalanobis-ellipse-threshold', 'mamba2-ssd-causal-map', 'map-beta-posterior', 'map-elites-archive', 'map-precision-at-hits', 'mc-dropout-repeated-passes', 'mean-teacher-ema-tracking', 'mf-als-alternating', 'mf-coupled-sgd', 'minhash-lsh-band-collision', 'mixup-beta-strength', 'mixup-cutmix-area', 'mixup-loss-decomposition', 'mixup-paired-interpolation', 'mle-bernoulli-likelihood', 'ndcg-position-discount', 'neat-add-node-innovation', 'newton-armijo-backtracking', 'newton-curvature-steps', 'newton-indefinite-curvature', 'nomad-goal-mask-routing', 'odin-gradient-perturbation', 'ofc-selective-feedback', 'outlier-mae-rmse', 'paired-bootstrap-resampling', 'particle-swarm-best', 'particle-weight-resampling', 'place-cell-firing', 'power-iteration-convergence', 'power-iteration-projection-contraction', 'pr-threshold-sweep', 'predictive-local-settling', 'prefix-kv-attention', 'prompt-injection-boundary', 'qat-fake-quant-ste', 'qlora-frozen-flow', 'r2-mean-baseline', 'random-search-x-coverage', 'rao-ballard-residual', 'recursive-tail-loss', 'resnet-depth-gradient-factors', 'resnet-identity-gradient', 'resnet-postrelu-gate', 'resnet-projection-shortcut', 'resolution-refutation-chain', 'rf-bootstrap-oob', 'rf-feature-subset', 'rmsnorm-shift-response', 'roc-rank-transform', 'roc-threshold-sweep', 'roofline-ridge-sweep', 'rotational-norm-balance', 's4d-diagonal-modes', 'sac-entropy-temperature', 'sac-soft-target', 'sac-temperature-feedback', 'saliency-local-gradient', 'self-instruct-filter-loop', 'sgd-noise-batch', 'shampoo-eigenmode', 'shap-coalition-marginals', 'sharpness-radius-loss', 'sharpness-reparam-curvature', 'simclr-temperature-competition', 'soap-eigenbasis-adam', 'stdp-spike-timing', 'stochastic-depth-scaling-conventions', 'stochastic-depth-survival-samples', 'strips-state-effects', 'successor-occupancy', 'svd-degenerate-bases', 'svd-ls-orthogonal-residual', 'svd-noise-amplification', 'svd-rank-accumulation', 'svd-unit-circle', 'svi-minibatch-global', 'svm-margin-hinge', 'theta-gamma-phase-amplitude', 'thompson-beta-posterior-draws', 'thompson-evidence-concentration', 'ucb1-bonus-sensitivity', 'ucb1-optimism-switch', 'ving-learned-graph-routing', 'vint-goal-waypoint-flow', 'vivit-factorised-attention', 'vqvae-codebook-snap', 'watermark-greenlist-score', 'weak-supervision-vote-fusion', 'wgan-gp-interpolation', 'wgan-weight-clip'}:
                # GitHub uses the raw static image; the opt-in hook rewrites
                # all three source-relative attributes for each built locale.
                errors.extend(verify_source_pair(page, text, stem))
                if stem in {"adam-bias-correction", "adam-epsilon-threshold", "adam-scale-invariance", "adam-sign-reversal", "ant-colony-pheromone", "bpr-gradient-saturation", "bpr-pairwise-ranking", "eigen-linear-map", "eigen-rotation-no-real", "lagrange-dual-gap", "lagrange-kkt-active-set", "lagrange-tangency", "mf-als-alternating", "mf-coupled-sgd", "newton-armijo-backtracking", "newton-curvature-steps", "newton-indefinite-curvature", "particle-swarm-best", "power-iteration-convergence", "resnet-depth-gradient-factors", "resnet-identity-gradient", "resnet-postrelu-gate", "resnet-projection-shortcut", "svd-degenerate-bases", "svd-ls-orthogonal-residual", "svd-noise-amplification", "svd-rank-accumulation", "svd-unit-circle"}:
                    static_links = re.findall(r"\[[^]]+\]\(([^)]+\.svg)\)", text)
                    if static_path.resolve() not in {
                        (page.parent / link).resolve() for link in static_links
                    }:
                        errors.append(f"{page}: missing GitHub-readable static link")
            elif stem in {"layernorm-feature-shift", "seq2seq-context-handoff", "flashattention-online-rescale", "flashattention-exact-merge", "flashattention-causal-tiles", "flashattention-backward-remat", "flashattention2-query-parallel", "flashattention3-load-compute-pipeline"}:

                errors.extend(verify_source_pair(page, text, stem))
            elif stem.startswith("diffusion-policy-"):
                errors.extend(verify_source_pair(page, text, stem))
            elif animated_path.resolve() not in linked_images:
                # Paired HTML is intentional for GitHub: <img src> is a
                # readable still, while data-motion-src enables playback on
                # MkDocs. Accept it only when *both* resolved paths match.
                paired = False
                if stem in {
                    "rnd-prediction-error", "rnd-state-novelty",
                    "icm-forward-inverse", "icm-predictable-stochastic"
                }:
                    for tag in re.findall(r"<img\b[^>]*>", text):
                        attrs = dict(re.findall(
                            r'(?:^|\s)(src|data-motion-src|data-still-src)="([^"]+)"',
                            tag,
                        ))
                        if all(name in attrs for name in (
                            "src", "data-motion-src", "data-still-src"
                        )):
                            paired = (
                                (page.parent / attrs["src"]).resolve() == static_path.resolve()
                                and (page.parent / attrs["data-still-src"]).resolve() == static_path.resolve()
                                and (page.parent / attrs["data-motion-src"]).resolve() == animated_path.resolve()
                            )
                            if paired:
                                break
                if not paired:
                    errors.append(f"{page}: missing or incorrect animated SVG link")
            if stem in {'muon-spectral-balancing', 'adamw-decoupled-paths', 'sac-temperature-feedback', 'ddm-first-passage', 'paged-block-mapping', 'td3-delayed-twin-critics', 'watermark-greenlist-score', 'gru-gate-flow', 'diffusion-policy-noise-training', 'forward-ad-finite-difference', 'mbmf-revaluation', 'a3c-nstep-return', 'gat-aggregation', 'mappo-backward-gae', 'ddpg-replay-bootstrap', 'lbfgs-two-loop', 'batch-norm-train-infer', 'tree-belief-propagation', 'byol-online-target', 'commnet-leave-one-out', 'dqn-target-sync', 'forward-ad-matmul-tangent', 'expert-cache-miss', 'forward-ad-sparse-packing', '3d-unet-orthogonal-slices', 'ddpg-polyak-target', 'deformable-sampling', 'nesterov-lookahead', 'sigma-reparam-spectral-gain', 'rt2-action-token-decoding', '3d-unet-context-tiling', 'streaming-kv-eviction', 'dinov2-dual-objective-ema', 'dreamer-lambda-bootstrap', 'speculative-decoding', 'eprop-local-credit', 'cmaes-distribution-adaptation', 'kmeans-lloyd', 'gqa-uptraining-pooling', 'ftw-two-level-learning', 'mbpo-horizon-error', 'bpe-ordered-merges', 'umap-fuzzy-union', 'ddpg-ou-noise', 'prioritized-replay-cycle', 'gcn-aggregation', 'rlhf-reward-sums', 'gqa-head-sharing', 'alphazero-puct-select', 'pets-cem-refit', 'forward-ad-linear-solve', 'muzero-latent-planning', 'fedavg-weighted-round', 'hmc-leapfrog-trajectory', 'forward-ad-hessian-vector', 'sam-two-gradient', 'astar-frontier', 'realnvp-affine-coupling', '3d-unet-skip-concat', 'rial-dial-credit-path', 'pbt-exploit-explore', 'mean-field-coordinate-ascent', 'icm-forward-inverse', 'stochastic-depth-paths', 'qk-norm-scale-sweep', 'dreamer-posterior-prior', '3d-unet-paired-warp', 'swin-shifted-windows', 'ddpg-actor-gradient', 'trpo-kl-backtracking', 'kfac-factor-preconditioning', 'vae-reparameterisation', 'diffusion-policy-denoising', 'alphazero-policy-target', 'fgsm-sign-step', 'openvla-dual-encoder-fusion', 'openvla-percentile-action-bins', 'alphazero-value-backup', 'rlhf-dpo-margin', 'diffusion-policy-multimodal-actions', 'mh-accept-reject', 'mappo-shared-advantage', 'nomad-goal-mask-routing', 'viterbi-trellis', '3d-unet-evaluation-holdout', 'forward-ad-normalization-jvp', 'mbpo-short-branches', 'forward-ad-softmax-tangent', 'pgd-projection-path', 'diffusion-policy-receding-horizon', 'rnd-prediction-error', 'qmix-monotonic-greedy', 'forward-ad-dual-chain', 'pets-ensemble-particles', 'stdp-spike-timing', 'forward-ad-jvp', '3d-unet-depth-kernel', 'trpo-ratio-surrogate', 'forward-ad-loop-tangent', 'prompt-injection-boundary', 'mae-visible-patch-reconstruction', 'hyperband-budget', 'maml-inner-outer-loop', 'tsne-kl-embedding', 'a3c-async-gradient', 'maddpg-actor-gradient', 'nerf-volume-rendering', 'ppo-clipped-objective', 'disaggregated-handoff', 'moco-dictionary-cycle', 'alpha-beta-cutoff', 'dpll-backtrack', 'rnd-state-novelty', 'orca-continuous-batching', '3d-unet-sparse-context-gradient', 'reverse-ad-vjp', 'alphazero-selfplay-labels', 'moe-top2-routing', 'ving-learned-graph-routing', 'icm-predictable-stochastic', 'rmsprop-adaptive-memory', 'sac-soft-target', 'spsa-two-evaluations', 'dagger-dataset-aggregation', 'gnm-speed-normalization', 'gibbs-coordinate-sweeps', 'saycan-skill-grounding', 'maddpg-joint-bootstrap', 'lion-sign-momentum', 'vint-goal-waypoint-flow', 'secagg-mask-cancellation', 'forward-ad-jacobian-columns', 'dial-dru-train-execute', '3d-unet-sparse-loss', 'commnet-layer-iterations', 'dart-noisy-expert-recovery', 'forward-ad-directional-jvp', 'mcts-search-cycle', 'forward-ad-branch-kink'}:
                static_links = re.findall(r"\[[^]]+\]\(([^)]+\.svg)\)", text)
                static_links += re.findall(r'<img[^>]*\s+src="([^"]+\.svg)"', text)
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
