---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/world-models
tags:
  - world models
  - latent actions
  - imitation learning
aliases:
  - LAPO
  - Learning to Act without Actions
  - 無動作標籤的潛在動作學習
---

# LAPO: Learning to Act without Actions

LAPO learns latent actions from video that has no action labels. An inverse dynamics model infers a latent action from consecutive observations, and a forward model predicts the next observation from the current one and that latent action. A vector-quantised bottleneck stops the latent action from simply copying the next observation. The family-level picture is on the [World Models & Embodied AI](index.md) page.

## Overview

Schmidt and Jiang (2024) ask whether the actions behind a video can be recovered from the frames alone. Their abstract says LAPO recovers latent action information purely from video, and that this information supports latent-action policies, world models and inverse dynamics models. The paper appeared at ICLR 2024 as a spotlight. Its experiments use the Procgen benchmark, which has 16 games.

Two neighbouring methods frame the problem differently. [Genie](genie.md) learns a latent action model without action labels in order to generate interactive worlds. [DINO-WM](dino-wm.md) assumes the actions are already known.

## Key concepts

- **Latent action** \(z_t\): a learned code for the transition from observation \(o_t\) to \(o_{t+1}\). It is not labelled and is not a real controller command.
- **Inverse dynamics model (IDM)**: reads the observations, including \(o_{t+1}\), and outputs \(z_t\). In the paper it uses the current observation and the next one (one step of context).
- **Forward dynamics model (FDM)**: predicts \(o_{t+1}\) from past observations and the quantised latent action. It never sees \(o_{t+1}\).
- **Vector quantisation (VQ)**: replaces each latent with an entry from a learned codebook, which limits how much information passes to the forward model.
- **Latent action policy** \(\pi\): maps an observation to a latent action. A small decoder then maps latent actions to real actions.

## How it works

For each transition in action-free video, the IDM and FDM compute

\[
z_t = \mathrm{IDM}(o_t, o_{t+1}), \qquad \hat o_{t+1} = \mathrm{FDM}\big(o_t,\ \mathrm{VQ}(z_t)\big)
\]

The two models are trained jointly by gradient descent to minimise the next-state error \(\lVert \hat o_{t+1} - o_{t+1}\rVert^2\). Gradients pass through the quantiser with a straight-through estimator.

The paper's Table 1 lists the bottleneck settings: 128-dimensional continuous latent actions, quantised with 2 codebooks, 4 discrete latents per codebook, 16-dimensional embeddings and a commitment cost of 0.05.

After the IDM is trained, the pipeline continues in three steps:

1. The latent policy \(\pi(o_t)\) is trained by regression on the IDM's latent labels, with loss \(\lVert \pi(o_t) - z_t\rVert^2\).
2. A decoder \(d\) is trained on a small set of action-labelled transitions to map latent actions to real actions.
3. The composed policy \(d \circ \pi\) is deployed. The paper also has an online fine-tuning stage with PPO.

## Key methods

### Learning to Act without Actions (Schmidt & Jiang, 2024)

- **Problem:** most policies and world models are trained with action labels, but large collections of video have none. The question is whether latent actions recovered from the frames can stand in for them.
- **Core idea:** jointly train an IDM that sees the next observation and an FDM that predicts it, with a vector-quantised bottleneck between them. The bottleneck is there to stop the IDM from copying \(o_{t+1}\) into the latent. The authors write that without it the IDM "would likely result in the IDM learning to simply copy" the next observation.
- **Equation or algorithm:** the IDM/FDM pair above, the regression loss for the latent policy, and the decoder step. The codebook settings are in Table 1.
- **Results:** on Procgen, Section 6.1 reports that LAPO exceeds the expert in 9 of 16 tasks within 4M frames. In the same budget, PPO from scratch reaches only 44% of expert performance. The introduction says about 200 labelled transitions are enough to exceed 4M steps of PPO. Section 6.2 reports that a decoder trained on fewer than 256 labelled transitions matches a policy trained from scratch.
- **Limitations:** the reported experiments are all on Procgen, so transfer to robots or real-world video is not shown. The decoder still needs labelled transitions, and the training objective alone does not determine which latent corresponds to which real action. The bottleneck trades information for shortcut prevention. Too little capacity loses action detail, and the paper's Table 1 gives one chosen setting, not a sweep.

## Connections

- The copying shortcut that LAPO's bottleneck blocks is the central failure mode in [action controllability](action-controllability.md).
- Genie and LAPO both learn actions from unlabelled video, but Genie uses the latent actions to generate worlds, while LAPO uses them to train policies and check them on game tasks.
- DINO-WM assumes labelled actions, so the question LAPO answers does not arise there.
- The latent policy is a behaviour-cloning problem; see [behavioural cloning](../../paradigms/imitation/behavioural-cloning/index.md).

## Open questions

- How many labelled transitions are needed to decode latent actions reliably across games and embodiments.
- Whether the bottleneck choice transfers beyond Procgen-style visual domains.
- Whether the latent actions still depend on the agent's action when the video contains distractors. This is a controllability question; see [action controllability](action-controllability.md).

## References

### Seminal papers

- Schmidt, D. & Jiang, M. (2024). *Learning to Act without Actions*. ICLR 2024 (spotlight). https://arxiv.org/abs/2312.10812 — Introduces LAPO, which recovers latent actions from action-free video and uses a vector-quantised bottleneck to stop the inverse model from copying the next observation.

### Related methods

- Bruce, J. et al. (2024). *Genie: Generative Interactive Environments*. ICML 2024 (PMLR 235). https://proceedings.mlr.press/v235/bruce24a.html — Learns a latent action model without action labels, for generating interactive environments.
- Zhou, G., Pan, H., LeCun, Y. & Pinto, L. (2025). *DINO-WM: World Models on Pre-trained Visual Features enable Zero-shot Planning*. ICML 2025 (PMLR 267). https://proceedings.mlr.press/v267/zhou25t.html — Action-conditioned world model on frozen DINOv2 features, which takes actions as given.
- Rudolph, M., Chuck, C., Black, K., Lvovsky, M., Niekum, S. & Zhang, A. (2024). *Learning Action-based Representations Using Invariance*. Reinforcement Learning Journal, vol. 1 (presented at RLC 2024). https://rlj.cs.umass.edu/2024/papers/Paper39.html — Analyses how inverse dynamics captures controllability over limited horizons and proposes action bisimulation.

### Articles and preprints

- Zhang, Z. et al. (2026). *Delta-JEPA: Learning Action-Sensitive World Models via Latent Difference Decoding*. arXiv preprint 2606.31232. https://arxiv.org/abs/2606.31232 — Decodes actions from the latent displacement between consecutive observations, rather than from concatenated endpoint embeddings. Preprint, not peer reviewed.
- Shi, Y. et al. (2026). *Overcoming Statistical Bias in Action-Controllable World Models*. arXiv preprint 2608.04653. https://arxiv.org/abs/2608.04653 — Proposes CoCo, a counterfactual consistency framework as an alternative remedy. Preprint, not peer reviewed.
