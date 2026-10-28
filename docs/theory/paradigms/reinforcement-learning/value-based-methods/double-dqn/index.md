---
status: draft
last_reviewed: 2026-10-28
aliases:
  - Double DQN
  - 雙重深度 Q 網路
---

# Double DQN (van Hasselt et al., 2016)

A change to the DQN target in which the online network chooses the action and the target network evaluates it, which reduces the overestimation that the maximum introduces.

## Problem

DQN's target takes the maximum of the same network's estimates, both to pick the action and to score it. When the estimates are noisy, the maximum is biased upward. van Hasselt, Guez and Silver show that DQN overestimates action values in every one of the 49 Atari games they tested, and that the overestimation can hurt performance.

## Core idea

The DQN target already contains a second network, the slowly updated target network. Double DQN uses it differently. The online network picks the greedy next action, and the target network scores that action. Separating selection from evaluation makes the maximum less prone to pick up positive noise. The paper notes that this needs no extra networks or parameters, and adds only minimal computation.

## Equation or algorithm

The DQN target is

\[
Y_t^{\text{DQN}} = R_{t+1} + \gamma \max_a Q(S_{t+1}, a; \theta^-_t)
\]

and the Double DQN target is

\[
Y_t^{\text{DoubleDQN}} = R_{t+1} + \gamma\, Q\big(S_{t+1}, \arg\max_a Q(S_{t+1}, a; \theta_t); \theta^-_t\big)
\]

Here \(\theta\) are the online parameters and \(\theta^-\) the target parameters. Everything else in the DQN training procedure, including replay and the squared loss, stays the same. Only the target changes.

## Results

The paper reports results on 49 Atari games, using the same evaluation as DQN:

- **Median human-normalised score, no-op starts:** 93.5% for DQN and 114.7% for Double DQN.
- **Mean, no-op starts:** 241.1% for DQN and 330.3% for Double DQN.
- **Median, human starts:** 47.5% for DQN and 88.4% for Double DQN.

The paper also measures value estimates over evaluation phases of 125,000 steps and reports that Double DQN's estimates are much closer to the values obtained from the learned policies.

## Limitations

- **Overestimation is reduced, not removed.** The decoupled target lowers the bias, but the learned values can still be inaccurate, and the paper offers no general guarantee.
- **Same replay and bootstrapping.** Double DQN still uses one-step targets and uniform replay. Prioritised replay (Schaul et al., 2016) and multi-step returns are separate improvements, combined later in Rainbow.
- **Discrete actions.** The argmax over actions still requires a finite action set.

## Connections

- Parent topic: [Value-based methods](../index.md), and the wider [Reinforcement Learning](../../index.md) overview.
- It modifies the target of [Deep Q-networks](../../deep-q-networks/index.md), and the tabular overestimation problem it addresses is discussed in [Q-learning](../q-learning/index.md).
- It is one of the six components combined in [Rainbow](../rainbow/index.md).

## Applications

- **Atari benchmark agents.** The method is evaluated on the Atari 2600 suite, which became the standard test bed for value-based agents (van Hasselt et al., 2016; Hessel et al., 2018).

## Open questions

- How much bias remains in the double estimator, and when it is harmful.
- Whether separating selection from evaluation helps with continuous action spaces, where the argmax itself is hard.

## References

### Seminal papers

- van Hasselt, Guez & Silver (2016), "Deep reinforcement learning with double Q-learning", [arXiv:1509.06461](https://arxiv.org/abs/1509.06461) — The Double DQN paper, showing DQN's overestimation and the decoupled target.
- Mnih et al. (2015), "Human-level control through deep reinforcement learning", *Nature* 518, 529–533. https://doi.org/10.1038/nature14236 — The DQN paper whose target Double DQN modifies.
- Schaul, Quan, Antonoglou & Silver (2016), "Prioritized experience replay", [arXiv:1511.05952](https://arxiv.org/abs/1511.05952) — A separate DQN improvement that replays transitions by their learning potential.
- Hessel et al. (2018), "Rainbow: Combining improvements in deep reinforcement learning", [arXiv:1710.02298](https://arxiv.org/abs/1710.02298) — Combines Double DQN with five other DQN extensions.

### Surveys and textbooks

- Sutton, R. S. & Barto, A. G. *Reinforcement Learning: An Introduction*, 2nd ed. MIT Press, 2018. http://incompleteideas.net/book/the-book-2nd.html — Background on temporal-difference targets and maximisation bias in value learning.
