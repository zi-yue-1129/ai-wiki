---
tags:
  - reinforcement learning
  - policy gradient
  - actor-critic
---

# Policy Gradient and Actor-Critic Methods

Policy-gradient methods optimise the policy directly by following the gradient of expected return. Actor-critic methods add a learned value function to reduce the variance of that gradient. They handle continuous actions naturally and power most modern RL systems that use neural networks.

## Overview

For a parametrised policy $\pi_\theta$, the policy gradient theorem gives $\nabla_\theta J(\theta) = \mathbb{E}\big[\sum_t \nabla_\theta \log \pi_\theta(a_t\mid s_t)\, A_t\big]$, where $A_t$ is an advantage estimate. REINFORCE uses sampled returns for $A_t$. This is unbiased but noisy, so baselines and critics are used to reduce its variance.

## Key methods

- **REINFORCE** samples full trajectories and weights log-probabilities by the return. It is simple and unbiased, but needs many samples.
- **Actor-critic** methods train a critic to estimate values and use the temporal-difference error as the advantage.
- **A3C** runs several actors in parallel with asynchronous updates, which decorrelates the data without a replay buffer.
- **PPO** limits how far each update can move the policy, using a clipped objective. It is simple to tune and is the default in many applications.

## Trade-offs

Policy methods are on-policy or sample-hungry in their basic forms, and they can converge to poor local optima. Value-based methods are more sample-efficient on discrete actions. Actor-critic and PPO sit between the two, and are the usual choice for continuous control and for fine-tuning large models.

## Connections

The critic is a value function, see [value-based methods](../value-based-methods/index.md). The reward-model and policy-gradient training used for language models is covered in [learning from human feedback](../learning-from-human-feedback/index.md). The same gradient-of-log-likelihood idea appears in [imitation learning](../../imitation/index.md) as an alternative to behaviour cloning.

## Applications

Robot locomotion and manipulation in simulation and on hardware, game-playing agents, fine-tuning language models for helpfulness, and control of industrial processes such as power grids.

## Open questions

Sample efficiency and reproducibility remain serious issues, since results depend strongly on implementation details. Credit assignment over long horizons and reliable exploration in sparse-reward tasks are still open.

## References

### Seminal papers

- Mnih et al. (2016), "Asynchronous methods for deep reinforcement learning", ICML, [arXiv:1602.01783](https://arxiv.org/abs/1602.01783) — A3C, parallel actor-critic training without a replay buffer.
- Schulman, Wolski, Dhariwal, Radford & Klimov (2017), "Proximal policy optimization algorithms", [arXiv:1707.06347](https://arxiv.org/abs/1707.06347) — PPO, a clipped objective that makes policy updates stable and simple.
- Christiano et al. (2017), "Deep reinforcement learning from human preferences", NeurIPS, [arXiv:1706.03741](https://arxiv.org/abs/1706.03741) — Trains a reward model from human comparisons and optimises it with policy gradients.
- Silver et al. (2016), "Mastering the game of Go with deep neural networks and tree search", *Nature* 529. https://research.google/pubs/mastering-the-game-of-go-with-deep-neural-networks-and-tree-search/ — Policy networks trained with policy gradients, combined with search.

### Surveys and textbooks

(none checked for this page)

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Ouyang et al. (2022), "Training language models to follow instructions with human feedback", [arXiv:2203.02155](https://arxiv.org/abs/2203.02155) — InstructGPT, which fine-tunes a language model with PPO against a learned reward model.

## Further reading

- Williams (1992), "Simple statistical gradient-following algorithms for connectionist reinforcement learning", *Machine Learning* 8. https://doi.org/10.1007/BF00992696 — The original REINFORCE paper, the basis of policy gradient methods.
