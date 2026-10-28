---
status: draft
last_reviewed: 2026-10-28
aliases:
  - Rainbow
  - 彩虹 DQN
---

# Rainbow (Hessel et al., 2018)

An agent that combines six separate improvements to DQN into one learner, and reports state-of-the-art performance on the Atari 2600 benchmark.

## Problem

By 2018 many extensions to DQN each fixed one weakness: overestimation, uniform replay, the form of the value function, one-step targets, the modelling of return distributions and exploration by ε-greedy. Each was usually tested alone. Hessel et al. ask how the improvements combine, and which of them matter when they are used together.

## Core idea

Rainbow takes the DQN agent and integrates six components, one from each family:

- **Double Q-learning** decouples action selection from evaluation to reduce overestimation (van Hasselt et al., 2016).
- **Prioritised replay** samples transitions with high learning potential more often (Schaul et al., 2016).
- **Dueling networks** split the network into a value stream and an advantage stream that share an encoder.
- **Multi-step learning** bootstraps from n-step returns rather than one-step targets.
- **Distributional RL** models the full distribution of returns, using 51 atoms, rather than only its mean.
- **Noisy networks** add learned noise to the linear layers for exploration in place of ε-greedy.

The paper also combines these into a single learning procedure, which is what makes it a single agent rather than a set of separate fixes.

## Equation or algorithm

Rainbow keeps the DQN structure of replay, a target network and minibatch updates, and changes the parts described above. The output is a distribution over returns on 51 atoms, and the multi-step component uses \(n = 3\), which the paper found to perform best after comparing \(n = 1, 3\) and \(5\). The full loss, pseudocode and hyperparameter table are in the paper, which should be read for implementation.

## Results

Across the 57 Atari games evaluated in the paper:

- **Median human-normalised score, no-op starts:** 223% for Rainbow.
- **Median human-normalised score, human starts:** 153% for Rainbow.
- **Best single component:** distributional DQN reaches 164% in the no-op regime, with dueling DDQN at 151% and prioritised DDQN at 140%. In the human-starts regime, prioritised DDQN is the best single component at 128%.

The ablation study finds that prioritised replay and multi-step learning are the two most important components. Distributional learning comes just after them.

## Limitations

- **Complexity.** The combined agent has many interacting parts, which makes results harder to attribute and reproduce.
- **Discrete actions.** The method is designed for the Atari setting with a finite action set.
- **Benchmark scope.** The results are on Atari games, and the paper does not show that the same combination works for continuous control.

## Connections

- Parent topic: [Value-based methods](../index.md), and the wider [Reinforcement Learning](../../index.md) overview.
- It combines [Double DQN](../double-dqn/index.md) with the [Deep Q-networks](../../deep-q-networks/index.md) base agent.
- Prioritised replay is covered on the [Experience replay](../../experience-replay/index.md) page.
- Exploration by noisy networks sits on the [Exploration](../../exploration/index.md) page's theme of driving the agent to try new actions.

## Applications

- **Atari benchmark.** Rainbow is a reference point for value-based agents on the Atari 2600 suite (Hessel et al., 2018).

## Open questions

- Which components remain useful once a sophisticated agent is trained at larger scale.
- How much of the result transfers to continuous control and to domains beyond games.

## References

### Seminal papers

- Hessel et al. (2018), "Rainbow: Combining improvements in deep reinforcement learning", arXiv:1710.02298 — The Rainbow paper, with its six-component ablation and the reported Atari results.
- van Hasselt, Guez & Silver (2016), "Deep reinforcement learning with double Q-learning", arXiv:1509.06461 — The double Q-learning component, which reduces overestimation.
- Schaul, Quan, Antonoglou & Silver (2016), "Prioritized experience replay", arXiv:1511.05952 — The prioritised replay component, reported to beat uniform replay on 41 of 49 games.
- Mnih et al. (2015), "Human-level control through deep reinforcement learning", *Nature* 518, 529–533. https://doi.org/10.1038/nature14236 — The base DQN agent that Rainbow extends.
- Mnih et al. (2013), "Playing Atari with deep reinforcement learning", arXiv:1312.5602 — The early preprint that introduced the Atari setting used throughout.

### Surveys and textbooks

- Sutton, R. S. & Barto, A. G. *Reinforcement Learning: An Introduction*, 2nd ed. MIT Press, 2018. http://incompleteideas.net/book/the-book-2nd.html — Background on multi-step returns and temporal-difference learning.
