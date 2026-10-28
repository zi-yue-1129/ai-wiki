---
tags:
  - reinforcement learning
  - value functions
  - Q-learning
---

# Value-Based Methods

Value-based reinforcement learning estimates how good each action is in each state, then acts greedily with respect to those estimates. Q-learning and its deep variants are the classic examples, and they remain central to offline and model-based approaches.

## Overview

The action-value function $Q^\pi(s,a)$ is the expected discounted return from taking action $a$ in state $s$ and then following policy $\pi$. Its optimal version satisfies the Bellman equation $Q^*(s,a)=\mathbb{E}[r + \gamma \max_{a'} Q^*(s',a')]$. Value-based methods repeatedly move the current estimate toward the right-hand side, using sampled transitions.

## Key methods

- **Tabular Q-learning** updates a table of values from sampled transitions, and converges to $Q^*$ under suitable conditions when every state–action pair is visited.
- **Deep Q-networks (DQN)** use a neural network for $Q$, a replay buffer to break correlations between samples, and a target network that is updated slowly. DQN reached human-level play on many Atari games from raw pixels.
- **Double and dueling variants** reduce the overestimation of maxima and separate the value of states from the advantage of actions.
- **Distributional methods** learn the full distribution of returns rather than only their mean.

## Components and variants

Two parts of the value-based loop have many variants of their own. [Experience replay](../experience-replay/index.md) decides which stored transitions the network learns from, from uniform sampling to priorities and hindsight relabelling. [Exploration](../exploration/index.md) decides which actions are tried, from count bonuses to ensembles of value heads. Target-network and overestimation fixes, such as the double and dueling variants above, are the third component, and each has open questions of its own.

## Limits

Value-based methods work best with discrete actions, because the maximum over actions must be computed. They can be unstable with function approximation and off-policy data, which is why target networks and replay are needed. The overestimation bias of the maximum is a persistent source of error.

## Connections

Value learning underlies [model-based planning](../model-based-rl/index.md), where a learned value guides search, and [offline RL](../offline-rl/index.md), where pessimistic value estimates keep the policy close to the data. Deep Q-networks use the same function-approximation tools as [deep learning](../../../deep-learning/index.md). The temporal-difference error is a form of the prediction-error signal discussed in [Reinforcement Learning](../index.md) and [neuroscience](../../../../brain-mind/neuroscience/index.md).

## Applications

Playing Atari and board games, control of data-centre cooling, recommendation with discrete item sets, and resource allocation problems where actions are a small set of options.

## Open questions

Stable value learning with function approximation and off-policy data is not fully understood. Extending value methods to very large or continuous action spaces, without giving up the maximisation, remains difficult.

## References

### Seminal papers

- Mnih et al. (2015), "Human-level control through deep reinforcement learning", *Nature* 518. https://klab.tch.harvard.edu/academia/classes/Neuro230/ReadingAssignments/MnihEtAlHassibis15NatureControlDeepRL.pdf — The DQN paper, which combined replay and target networks to learn Atari play from pixels.
- Silver et al. (2016), "Mastering the game of Go with deep neural networks and tree search", *Nature* 529. https://research.google/pubs/mastering-the-game-of-go-with-deep-neural-networks-and-tree-search/ — AlphaGo, which combines learned values and policies with tree search.
- van Hasselt, Guez & Silver (2016), "Deep reinforcement learning with double Q-learning", AAAI, arXiv:1509.06461 — Removes the overestimation bias of DQN by separating action selection from evaluation.
- Schrittwieser et al. (2020), "Mastering Atari, Go, Chess and Shogi by planning with a learned model", *Nature*, arXiv:1911.08265 — MuZero, which learns values and a model together for planning.

### Surveys and textbooks

(none checked for this page)

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Kumar, Zhou, Tucker & Levine (2020), "Conservative Q-learning for offline reinforcement learning", NeurIPS, arXiv:2006.04779 — Penalises Q-values on actions unsupported by the data, a value method for offline learning.

## Further reading

- Sutton & Barto, *Reinforcement Learning: An Introduction*, 2nd ed., MIT Press (2018). http://incompleteideas.net/book/the-book-2nd.html
