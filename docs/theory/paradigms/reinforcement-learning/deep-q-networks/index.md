---
status: draft
last_reviewed: 2026-10-28
---

# Deep Q-networks (Mnih et al., 2015)

A convolutional network approximates the action-value function from raw frames, stabilised by experience replay and a target network.

## Problem

How can one algorithm learn control policies directly from raw pixels across many different games?

## Core idea

A convolutional network approximates the action-value function Q from raw frames. Two changes make training stable: experience replay, which samples random past transitions, and a target network, which is updated only now and then.

## Equation or algorithm

The network is trained to reduce the squared temporal-difference error against the target network:

\[
L(\theta) = \mathbb{E}\left[\left(r + \gamma \max_{a'} Q(s', a'; \theta^-) - Q(s, a; \theta)\right)^2\right]
\]

## Results

One network and one training procedure learned to play a range of Atari 2600 games from raw pixels.

## Limitations

Actions must be discrete, and training needs a great deal of experience. Later work such as Double DQN and Rainbow addresses some of the remaining instability, as the algorithm table above shows.

## Connections

- Parent topic: [Reinforcement Learning](../index.md)
- Other method on this topic: [Proximal Policy Optimisation](../proximal-policy-optimisation/index.md)

## References

### Seminal papers

- Mnih et al. (2015), "Human-level control through deep reinforcement learning", *Nature* 518. https://doi.org/10.1038/nature14236 — The DQN paper, the start of deep reinforcement learning at scale.
- Silver et al. (2016), "Mastering the game of Go with deep neural networks and tree search", *Nature* 529. https://research.google/pubs/mastering-the-game-of-go-with-deep-neural-networks-and-tree-search/ — AlphaGo, combining learned networks with search.
- Christiano et al. (2017), "Deep reinforcement learning from human preferences", NeurIPS, arXiv:1706.03741 — Learns reward functions from human comparisons, the basis of RLHF.
- Schulman et al. (2017), "Proximal policy optimization algorithms", arXiv:1707.06347 — PPO, the policy-gradient method most used in practice.

### Surveys and textbooks

- Sutton, R. S. & Barto, A. G. *Reinforcement Learning: An Introduction*, 2nd ed. MIT Press, 2018. http://incompleteideas.net/book/the-book-2nd.html — The standard RL textbook, with a free online draft covering the algorithm families above.
- Levine, S., Kumar, A., Tucker, G. & Fu, J. (2020), "Offline reinforcement learning: tutorial, review, and perspectives on open problems", arXiv:2005.01643 — Tutorial and review on learning from fixed datasets.
