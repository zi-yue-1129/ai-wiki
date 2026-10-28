---
status: draft
last_reviewed: 2026-10-28
tags:
  - world models
  - latent actions
  - imitation learning
aliases:
  - LAPO
  - Learning to Act without Actions
  - 無動作標籤的潛在動作學習
---

# LAPO (Learning to Act without Actions)

LAPO is a method for learning latent actions from video that has no action labels. It trains an inverse dynamics model that infers a latent action from consecutive frames, and a forward model that predicts the next frame from the current frame and that latent action. A quantised bottleneck keeps the latent action from simply copying the next frame.

## Problem

Robot and game data with action labels are expensive to collect, while video of agents doing things is abundant. LAPO asks whether the actions behind a video can be recovered from the frames themselves, and whether those recovered actions are good enough to train a policy, a world model or an inverse dynamics model.

## Core idea

Train two models together. The inverse model sees the whole sequence of observations and predicts a latent action for each transition. The forward model predicts the next observation from the current one and that latent action. Because the inverse model can see the next frame, it has a shortcut: encode the next frame directly. The authors prevent this by applying vector quantisation to the latent action before it reaches the forward model. Schmidt and Jiang (2024) state that without quantisation the inverse model "would likely result in the IDM learning to simply copy" the next observation.

## How it works

1. Observe consecutive frames from action-free video.
2. The inverse dynamics model reads the full observation sequence and outputs a latent action for each transition.
3. The latent action is vector-quantised, which limits its information content.
4. The forward dynamics model predicts the next observation from the current observation and the quantised latent action.
5. Train both models end to end on the prediction loss. Afterwards, a small decoder can map a few labelled transitions to real actions, which is how the latent action policy is used.

The abstract states that the learned latent actions enable latent-action policies, world models and inverse dynamics models. The exact losses and the decoding step are in the paper.

## Key methods

- Versus [Genie](genie.md), which uses the same kind of latent action to generate an interactive world, LAPO is aimed at training policies and models from video.
- Versus [DINO-WM](dino-wm.md), which assumes actions are known, LAPO recovers them from video, which is why its bottleneck matters.

## Results

The abstract reports that LAPO recovers latent action information from video alone and that this information supports the downstream models named above. Benchmark results should be copied from the paper.

## Limitations

- The quantised bottleneck is a design choice that trades information for shortcut prevention. Too little capacity loses action detail, and too much re-enables the copying shortcut.
- A latent action learned this way is not guaranteed to match the meaning of a real robot command. A small labelled set is needed to map it to real actions.
- Whether the latent action still depends on the action when the environment has distractors is a controllability question; see [action controllability](action-controllability.md).

## Connections

LAPO is the reference method for the copying shortcut described in [action controllability](action-controllability.md). It also connects to imitation learning, where the latent actions serve as a policy's output space; see [imitation learning](../../paradigms/imitation/index.md). The parent overview is at [world models & embodied AI](index.md).

## Applications

Training latent action policies from unlabelled gameplay or robot video, and bootstrapping a world model from video before a few labelled actions are added.

## Open questions

- How much labelled data is enough to map latent actions to real actions reliably.
- Whether the bottleneck choice transfers across embodiments and visual domains.

## References

### Seminal papers

- Schmidt, D. & Jiang, M. (2024). *Learning to Act without Actions*. ICLR 2024 (spotlight). https://arxiv.org/abs/2312.10812 — Introduces LAPO, which learns latent actions from action-free video and uses vector quantisation to prevent the inverse model from copying the next observation.

### Articles and preprints

- Bruce, J. et al. (2024). *Genie: Generative Interactive Environments*. ICML 2024. https://proceedings.mlr.press/v235/bruce24a.html — Uses a latent action model learned from unlabelled video in a generative setting, a related approach.
- Rudolph, M. et al. (2024). *Learning Action-based Representations Using Invariance*. Reinforcement Learning Conference 2024. https://arxiv.org/abs/2403.16369 — Analyses the single-step inverse dynamics shortcut that LAPO's bottleneck is designed to block.
- Zhang, Z. et al. (2026). *Delta-JEPA: Learning Action-Sensitive World Models via Latent Difference Decoding*. arXiv preprint. https://arxiv.org/abs/2606.31232 — Newer work on the same leakage problem, decoding actions from latent differences. Preprint, not peer reviewed.
- Shi, Y. et al. (2026). *Overcoming Statistical Bias in Action-Controllable World Models*. arXiv preprint. https://arxiv.org/abs/2608.04653 — Counterfactual consistency regularisation as an alternative remedy. Preprint, not peer reviewed.
