---
status: draft
last_reviewed: 2026-10-28
related:
  - applications/robotics/navigation
  - theory/paradigms/imitation
tags:
  - robotics
  - navigation
  - diffusion
  - exploration
aliases:
  - NoMaD
  - Goal Masked Diffusion Policy
  - 目標遮罩擴散策略
---

# NoMaD: Goal-Masked Diffusion Policies

NoMaD, introduced by Sridhar, Shah, Glossop and Levine (2023), is one diffusion policy that does two jobs: it reaches a goal image when the goal is known, and it explores a new environment when it is not. The two behaviours come from one network, switched by a binary mask on the goal input. The parent subtopic is [Navigation with Visual Goals](index.md).

## Overview

Navigation in an unfamiliar place needs two abilities that are usually handled by separate components. Task-oriented navigation reaches a goal that the robot has already located. Task-agnostic exploration searches for a goal in a setting the robot has not seen. Earlier systems used one model for each, or relied on subgoal proposals and planners. NoMaD trains a single policy that can do both, and the authors report that this gives better overall performance in novel environments than approaches that use subgoal proposals from generative models or earlier latent-variable methods (Sridhar et al., 2023).

## Problem

Exploration and goal-reaching pull a policy in different directions. An exploring robot should cover ground and avoid collisions without a destination, while a goal-reaching robot should head for a specific image. Training one model on both requires a way to tell it which mode it is in, and the model must still produce useful actions in both modes.

## Core idea

Give the policy the goal as an input token, and attach a binary mask that controls whether the network may attend to that token. With the mask on, the policy ignores the goal and explores. With the mask off, it conditions on the goal and navigates toward it. During training the mask is sampled at random, so the network learns both behaviours from the same data.

## Equation or algorithm

NoMaD is a conditional denoising diffusion policy:

1. **Encoders.** EfficientNet-B0 encoders turn the past five observations, each 96 by 96 pixels, and the optional goal image into 256-dimensional tokens.
2. **Goal mask.** A binary mask *m* controls attention to the goal token. In training, *m* is drawn from a Bernoulli distribution with *p* = 0.5. At test time, *m* = 1 gives undirected exploration and *m* = 0 gives goal-conditioned navigation.
3. **Transformer and denoiser.** A four-layer Transformer decoder with four heads produces a context for a one-dimensional conditional U-Net, which denoises a sequence of future actions. The paper's figure shows eight future actions.
4. **Training.** The denoising objective is a mean-squared error between the noise added to ground-truth action sequences and the noise the network predicts. A temporal-distance term is added with a small weight.
5. **Sampling.** At test time the policy draws actions by running ten denoising steps. Exploration runs in the undirected mode inside a topological graph built online, with frontier-based subgoal selection following ViKiNG.

The model has about 19 million parameters, as listed in the paper's comparison table.

## Results

The paper reports two kinds of evaluation. Exploration is scored by the share of successful runs and the number of collisions. Table I of the paper gives these values for NoMaD and for comparison methods in indoor and outdoor settings:

| Method | Exploration success | Collisions per run | Navigation success |
|---|---|---|---|
| Masked ViNT | 50% | 1.0 | 30% |
| VIB | 30% | 4.0 | 15% |
| Autoregressive | 90% | 2.0 | 60% |
| Random subgoals | 70% | 2.7 | 90% |
| Subgoal diffusion (335M parameters) | 77% | 1.7 | 90% |
| NoMaD (19M parameters) | 98% | 0.2 | 90% |

Table II of the paper reports the undirected and goal-conditioned success rates of NoMaD at 98% and 92%, against 98% for a plain diffusion policy in undirected mode and 92% for a ViNT policy in goal-conditioned mode. The paper's experiments run on a mobile robot in unseen environments. The text gives different counts of evaluation environments in different places, so the environment list should be read from the paper's own appendix.

## Limitations

- Exploration relies on standard frontier-based planning. The paper proposes smarter region selection, such as semantic or prior-based strategies, as future work.
- Goal images are general but are not always the most natural way for a user to say where to go. Language and spatial coordinates are not supported in this version.
- The authors describe the results as a proof of concept. They report that NoMaD succeeds in all but the hardest environment, and they give little analysis of other failure modes.

## Connections

- [GNM](gnm.md) and [ViNT](vint.md) are goal-conditioned policies that NoMaD is compared against, and ViNT's transformer design is the closest relative of its encoder.
- [Diffusion policies](../../../theory/paradigms/imitation/index.md) are learned by imitation, the same paradigm as most navigation policies on this page.
- [Visual teach-and-repeat](visual-teach-and-repeat.md) is the classical alternative that needs no learned exploration.

## Open questions

- Whether a single diffusion policy can explore as well as a planner that uses a metric map, in very large or changing environments.
- How the goal mask generalises to goal types other than images.

## References

- Sridhar, A., Shah, D., Glossop, C. & Levine, S. (2023). *NoMaD: Goal Masked Diffusion Policies for Navigation and Exploration*. arXiv. https://arxiv.org/abs/2310.07896 — The source of the goal-masked policy, the comparison tables and the exploration results.
- Chi, C. et al. (2023). *Diffusion Policy: Visuomotor Policy Learning via Action Diffusion*. arXiv. https://arxiv.org/abs/2303.04137 — Represents a robot policy as a conditional denoising diffusion process over actions.
- Ho, J., Jain, A. & Abbeel, P. (2020). *Denoising Diffusion Probabilistic Models*. arXiv. https://arxiv.org/abs/2006.11239 — The denoising diffusion model that the policy's sampler is based on.
- Shah, D., Sridhar, A., Dashora, N., Stachowicz, K., Black, K., Hirose, N. & Levine, S. (2023). *ViNT: A Foundation Model for Visual Navigation*. arXiv. https://arxiv.org/abs/2306.14846 — The transformer policy and subgoal-diffusion baseline that NoMaD compares with.
- Shah, D., Sridhar, A., Bhorkar, A., Hirose, N. & Levine, S. (2022). *GNM: A General Navigation Model to Drive Any Robot*. arXiv. https://arxiv.org/abs/2210.03370 — An earlier shared navigation model from the same group, cited as background for goal-conditioned navigation.
