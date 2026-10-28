---
status: draft
last_reviewed: 2026-10-28
tags:
  - world models
  - controllability
aliases:
  - 動作可控性
  - action controllability
---

# Action Controllability in World Models

A world model is useful for planning only if its predictions change when the agent's action changes. Many learned models fail this test. They predict plausible next frames while using the action input very little. This page describes that failure, the shortcuts behind it, and the remedies proposed in the literature.

## Overview

An action-conditioned world model takes the current state and an action, and predicts the next state. Training on logged data rewards getting the next frame right. In video and robot data the next frame is usually close to the current one, so a model can reach low prediction error by copying the present state and ignoring the action. Its predictions then barely respond to what the agent does, and a planner that searches over actions gets little useful signal.

## Key concepts

- **Action-ignoring model**: a model whose predicted future changes little when the action changes.
- **Inverse dynamics**: predicting the action that caused a transition between two observations. It is often added as an auxiliary task so that the latent representation keeps action information.
- **Shortcut**: a route to low training loss that bypasses the intended signal, for example copying the answer into the latent code.
- **Controllability**: how much the predicted future depends on the chosen action.

## How it works

The literature describes three mechanisms that let a model ignore actions.

1. **Copying through an inverse-dynamics head.** If the inverse model sees both the current and the next observation, it can encode the next observation itself into the "latent action". Schmidt and Jiang (2024) state that without a bottleneck the inverse model "would likely result in the IDM learning to simply copy" the next observation. Their remedy is vector quantisation of the latent action, which limits how much information reaches the forward model. See [LAPO](lapo.md).
2. **Leakage through concatenation.** If the decoder that predicts the action reads a concatenated pair of current and next latent states, the next state can carry action-correlated cues that the forward predictor has already used. Zhang et al. (2026, preprint) report that decoding the action from the latent difference between the two states, rather than from the concatenation, is more effective. Their ablations state that "displacement-based action decoding is consistently more effective than endpoint concatenation."
3. **Myopic controllability.** Rudolph et al. (2024) observe that single-step inverse dynamics captures controllability only over a limited horizon. They propose action bisimulation, a recursive invariance constraint, to capture control relevance over longer horizons.

A different family of remedies adds training targets rather than changing the architecture. Shi et al. (2026, preprint) argue that supplying actions as inputs is not enough. They regularise predictions to stay consistent under hypothetical changes to the action and the scene, so the model cannot rely on statistical regularities that hold without any action effect.

## Key methods

- [LAPO (Schmidt & Jiang, 2024)](lapo.md): restricts the latent action with a quantised bottleneck, so that it encodes the change between frames rather than the next frame.
- [DINO-WM (Zhou et al., 2025)](dino-wm.md): conditions the predictor on actions through an embedding added to every patch of frozen visual features. It does not add a controllability objective.
- Delta-JEPA (Zhang et al., 2026) and CoCo (Shi et al., 2026) are recent preprints. They change which signal the action decoder reads, or add counterfactual consistency terms. Their claims have not yet passed peer review.

## Connections

Planning with a learned model is covered in [model-based reinforcement learning](../../paradigms/reinforcement-learning/model-based-rl/index.md). A controllability failure there shows up as a planner that cannot tell apart actions with different consequences.

The distinction between a forward model that predicts the sensory consequences of one's own movement and a model that ignores those movements is a familiar idea in motor control. For the neuroscience background, see [World models & embodied AI](index.md).

## Applications

Controllable world models are needed wherever an agent plans with a learned simulator, for example robot manipulation and navigation from video or logged trajectories.

## Open questions

- Do controllability tests that swap actions measure what planning actually needs?
- Do the leakage fixes, such as decoding from differences, change the quality of predicted frames?
- How much multi-step consistency training costs compared with its gain in planning success?

## References

### Seminal papers

- Schmidt, D. & Jiang, M. (2024). *Learning to Act without Actions*. ICLR 2024 (spotlight). https://arxiv.org/abs/2312.10812 — Introduces LAPO, which recovers latent actions from action-free video and uses a vector-quantised bottleneck to stop the inverse model from copying the next frame.
- Rudolph, M. et al. (2024). *Learning Action-based Representations Using Invariance*. Reinforcement Learning Conference 2024. https://arxiv.org/abs/2403.16369 — Analyses how single-step inverse dynamics captures controllability and proposes action bisimulation for longer horizons.
- Zhou, G., Pan, H., LeCun, Y. & Pinto, L. (2025). *DINO-WM: World Models on Pre-trained Visual Features enable Zero-shot Planning*. ICML 2025. https://proceedings.mlr.press/v267/zhou25t.html — Action-conditioned predictor on frozen DINOv2 patch features, used for planning.

### Articles and preprints

- Zhang, Z. et al. (2026). *Delta-JEPA: Learning Action-Sensitive World Models via Latent Difference Decoding*. arXiv preprint. https://arxiv.org/abs/2606.31232 — Decodes actions from latent differences rather than endpoint concatenation. Preprint, not peer reviewed.
- Shi, Y. et al. (2026). *Overcoming Statistical Bias in Action-Controllable World Models*. arXiv preprint. https://arxiv.org/abs/2608.04653 — Proposes counterfactual consistency regularisation for action-controllable world models. Preprint, not peer reviewed.
