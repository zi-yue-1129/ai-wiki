---
status: draft
last_reviewed: 2026-10-28
---

# Proximal policy optimisation (Schulman et al., 2017)

A policy-gradient method that clips the probability ratio between the new and old policies, so each update stays near the old policy.

## Problem

Plain policy gradients can take steps so large that performance collapses. Trust-region methods are stable but complicated to implement.

## Core idea

Clip the ratio between the new and old action probabilities in the surrogate objective, so the update gains nothing from moving far from the old policy. This allows several epochs of minibatch updates on the same batch of data.

## Equation or algorithm

With the probability ratio \(r_t(\theta) = \pi_\theta(a_t \mid s_t) / \pi_{\theta_{\text{old}}}(a_t \mid s_t)\) and advantage estimate \(\hat{A}_t\):

\[
L^{\text{CLIP}}(\theta) = \mathbb{E}_t\left[\min\left(r_t(\theta)\hat{A}_t,\ \text{clip}\left(r_t(\theta), 1-\epsilon, 1+\epsilon\right)\hat{A}_t\right)\right]
\]

## Results

The paper reports that PPO outperforms other online policy gradient methods on its benchmark tasks, which include simulated robotic locomotion and Atari, with a favourable balance of sample complexity, simplicity and wall-clock time.

## Limitations

The evidence is empirical, and clipping is a heuristic rather than a guarantee of improvement. PPO is also on-policy, so each batch of data supports only a few updates.

## Connections

- Parent topic: [Reinforcement Learning](../index.md)
- Other method on this topic: [Deep Q-Networks](../deep-q-networks/index.md)

## References

### Seminal papers

- Mnih et al. (2015), "Human-level control through deep reinforcement learning", *Nature* 518. https://doi.org/10.1038/nature14236 — The DQN paper, the start of deep reinforcement learning at scale.
- Silver et al. (2016), "Mastering the game of Go with deep neural networks and tree search", *Nature* 529. https://research.google/pubs/mastering-the-game-of-go-with-deep-neural-networks-and-tree-search/ — AlphaGo, combining learned networks with search.
- Christiano et al. (2017), "Deep reinforcement learning from human preferences", NeurIPS, [arXiv:1706.03741](https://arxiv.org/abs/1706.03741) — Learns reward functions from human comparisons, the basis of RLHF.
- Schulman et al. (2017), "Proximal policy optimization algorithms", [arXiv:1707.06347](https://arxiv.org/abs/1707.06347) — PPO, the policy-gradient method most used in practice.

### Surveys and textbooks

- Sutton, R. S. & Barto, A. G. *Reinforcement Learning: An Introduction*, 2nd ed. MIT Press, 2018. http://incompleteideas.net/book/the-book-2nd.html — The standard RL textbook, with a free online draft covering the algorithm families above.
- Levine, S., Kumar, A., Tucker, G. & Fu, J. (2020), "Offline reinforcement learning: tutorial, review, and perspectives on open problems", [arXiv:2005.01643](https://arxiv.org/abs/2005.01643) — Tutorial and review on learning from fixed datasets.
