---
status: draft
last_reviewed: 2026-10-28
tags:
  - world models
  - reinforcement learning
  - model-based
aliases:
  - Dreamer
  - 夢想家
  - 想像式強化學習
---

# Dreamer

Dreamer is a family of reinforcement-learning agents. They learn a latent world model from experience, then learn their behaviour by imagining trajectories inside that model rather than by acting in the real environment for every update.

## Overview

A Dreamer agent has three learned parts. A world model encodes observations into a compact latent state and predicts how that state changes with actions, rewards and continuation signals. An actor chooses actions. A critic estimates the value of states. The actor and critic are trained on imagined latent trajectories produced by the world model, so one real experience can support many learning updates. This is the defining idea of [model-based reinforcement learning](../../paradigms/reinforcement-learning/model-based-rl/index.md) in its latent-imagination form.

## Key concepts

- **Latent state**: a compressed representation of the observation that the model predicts forward.
- **Imagined rollout**: a sequence of latent states and predicted rewards produced by the model without touching the environment.
- **Actor-critic on imagination**: the policy is improved by gradients of predicted values, computed through the imagined sequence.

## How it works

1. Store real experience in a replay buffer.
2. Train the world model to reconstruct observations and predict rewards from latent states, so that the latent state carries what matters for control.
3. From sampled real states, roll the policy forward inside the latent model for a fixed horizon.
4. Train the critic on imagined returns and the actor to maximise predicted values, backpropagating through the imagined sequence.

## Key methods

- **DreamerV1 (Hafner et al., 2019)**: learns behaviours by backpropagating value estimates through imagined trajectories in a latent space. [arXiv:1912.01603](https://arxiv.org/abs/1912.01603).
- **DreamerV2 (Hafner et al., 2021)**: uses discrete categorical latent variables in the world model. The abstract describes it as the first agent to reach human-level performance on a benchmark of 55 Atari tasks.
- **DreamerV3 (Hafner et al., 2025)**: uses one fixed configuration across more than 150 tasks in different domains, without per-task tuning, according to the abstract.

What separates the versions is mainly the form of the latent state and the training recipe. The core loop stays the same. Each version's specific training details are in its own paper, which should be read before reusing them.

## Connections

Dreamer sits in the same family as the other [world models](index.md) on this site. Its latent prediction is a form of learned forward modelling. Whether its imagination mechanism corresponds to processes in the brain is an open hypothesis, not something the Dreamer papers establish. The neuroscience-side discussion of planning and simulation is on the [computational neuroscience](../../../brain-mind/computational-neuroscience/index.md) page.

## Applications

Dreamer-style agents have been used for continuous control, for 2D and 3D game environments, and for learning from image observations. The DreamerV3 paper reports results across domains, which is the main evidence for its generality.

## Open questions

- How far the model's errors can grow across a long imagined horizon before the actor learns from misleading values.
- Whether one configuration works equally well for tasks that differ much from those in the benchmark suites.
- How the latent model should handle actions that do not change the observation, which is the controllability problem covered in [Action controllability](action-controllability.md).

## References

### Seminal papers

- Hafner, D., Lillicrap, T., Ba, J. et al. (2019). *Dream to Control: Learning Behaviors by Latent Imagination*. arXiv preprint. https://arxiv.org/abs/1912.01603 — Introduces Dreamer, which learns behaviour by backpropagating through imagined latent trajectories.
- Hafner, D., Lillicrap, T., Norouzi, M. & Ba, J. (2021). *Mastering Atari with Discrete World Models*. ICLR 2021. https://arxiv.org/abs/2010.02193 — DreamerV2, with discrete latent states and results on the Atari benchmark.
- Hafner, D., Pasukonis, J., Ba, J. & Lillicrap, T. (2025). *Mastering diverse control tasks through world models*. Nature 640. https://doi.org/10.1038/s41586-025-08744-2 — Journal version of DreamerV3, one configuration for more than 150 tasks. The arXiv preprint, *Mastering Diverse Domains through World Models*, is at https://arxiv.org/abs/2301.04104.

### Surveys and textbooks

- Moerland, T. M. et al. (2020). *Model-based Reinforcement Learning: A Survey*. arXiv preprint. https://arxiv.org/abs/2006.16712 — Survey of model-based reinforcement learning, covering learned dynamics models and how they are used for planning and policy learning.

### Articles and documentation

- Ha, D. & Schmidhuber, J. (2018). *World Models*. arXiv preprint. https://arxiv.org/abs/1803.10122 — Early latent world model in which a controller is trained inside the model's own simulated rollouts, a precursor to Dreamer.
