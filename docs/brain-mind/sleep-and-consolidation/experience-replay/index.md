---
status: draft
last_reviewed: 2026-10-28
tags:
- reinforcement learning
- memory
- sleep
aliases:
  - Experience Replay
  - Replay Buffer
  - 經驗回放
  - 經驗重播
  - 回放緩衝區
  - DQN Replay
---

# Experience replay (Lin, 1992; Mnih et al., 2015)

Experience replay stores an agent's past transitions in a buffer and reuses them for later learning updates. Lin introduced the idea in 1992 for reinforcement-learning agents with neural-network learners. Mnih et al. (2015) made it central to the deep Q-network, which learned to play Atari games from pixels. It is the clearest case of a replay idea from neuroscience becoming a routine engineering tool.

This page is part of [Sleep, Replay and Memory Consolidation](../index.md). It covers the origin of the method and its brain comparison. The full set of variants, such as prioritised and hindsight replay, is on the [theory page on experience replay](../../../theory/paradigms/reinforcement-learning/experience-replay/index.md).

## Overview

A learner that uses each new transition once, in the order it occurs, learns slowly and sees strongly correlated data. Consecutive steps are similar, so updates from them are strongly correlated. Experience replay solves this by keeping transitions in a buffer and drawing training samples from it. The same experience can then inform many updates, and samples from different times can be mixed together.

## Problem

Early reinforcement-learning methods, such as Q-learning, learned value functions from each transition as it arrived. When the value function was a neural network, this was slow and could be unstable. Lin (1992) asked whether an agent could learn more from the same experience, and whether the order in which it reused that experience mattered.

## Core idea

Each transition is stored as a tuple of state, action, reward and next state. The learner repeatedly presents stored transitions as if the agent had experienced them again. Lin's version replayed the most recent experiences, and noted that backward temporal order can be more effective for propagating credit along a trajectory. He also argued that replaying the same experience too many times is harmful, so the replay has to be limited.

Mnih et al. (2015) kept a replay memory of the one million most recent frames. At each update they sampled a mini-batch uniformly at random from this memory. Random sampling breaks the correlation between consecutive frames, and the authors say it reduces the variance of updates and avoids oscillations or divergence in the parameters.

## Equation or algorithm

The deep Q-network procedure is:

1. Act in the environment with the current policy, using a small amount of random exploration, and store the transition (s, a, r, s') in the replay memory D. When the memory is full, the oldest transition is removed.
2. Sample a mini-batch of transitions uniformly from D.
3. For each sampled transition, compute the target r + γ max over a' of Q(s', a'; θ⁻), where θ⁻ are the parameters of a separate target network.
4. Update the online parameters θ by gradient descent on the squared error between the target and Q(s, a; θ).

In equation form the loss is

\(L(\theta) = \mathbb{E}_{(s,a,r,s') \sim D}\left[\left(r + \gamma \max_{a'} Q(s', a'; \theta^-) - Q(s, a; \theta)\right)^2\right]\)

where \(\gamma\) is the discount factor, and the expectation is taken over the replay memory rather than over the current trajectory.

## Results

- Lin (1992) reported that replay significantly improved learning speed in a simulated survival task, compared with the same learners without replay.
- Mnih et al. (2015) reported a deep Q-network that learned from pixels and the game score. It was tested on 49 games and outperformed the best existing reinforcement-learning methods on 43 of them.

The DQN results combine replay with other components of the agent, so they do not measure replay's contribution alone.

## Limitations

- **Memory cost.** Storing raw frames, especially images, is expensive. The buffer size becomes a design constraint.
- **Uniform sampling spends updates evenly.** Transitions the agent already predicts well receive as many updates as rare or surprising ones. Prioritised methods change this, and the theory page covers them.
- **Off-policy bias.** Stored transitions come from older policies, so updates made from them differ from updates on-policy. Correction methods exist but add complexity.
- **Narrow evidence.** The DQN results come from a fixed benchmark of Atari games. Generalisation to other domains needs separate evidence.
- **The brain analogy is suggestive.** The similarity with replay in the hippocampus is a point of comparison, not evidence that the brain uses this algorithm.

## Connections

- **Brain.** Replay in the hippocampus, described on [Hippocampal replay](../hippocampal-replay/index.md), also reuses recent sequences, and Lin's backward ordering resembles the reverse replay Foster and Wilson (2006) reported. The conceptual link to memory systems is the complementary learning systems account on [Complementary Learning Systems](../../memory-learning/complementary-learning-systems/index.md).
- **Reinforcement learning.** The full algorithm is on [Deep Q-networks](../../../theory/paradigms/reinforcement-learning/deep-q-networks/index.md), and the general framework is on [Reinforcement Learning](../../../theory/paradigms/reinforcement-learning/index.md).
- **Continual learning.** Replay of old data to prevent forgetting uses the same buffer idea, as described on [Replay and memory in continual learning](../../../theory/paradigms/continual/replay-and-memory/index.md).

## Applications

- **Game-playing and control agents.** Deep Q-network style agents, including the Atari agent of Mnih et al. (2015), use replay buffers to learn from pixel input.
- **Continual learning.** Rehearsal of old data, interleaved with new data, is a common baseline against catastrophic forgetting.

## Open questions

- **Does backward ordering help deep networks?** Lin's result came from a simulated grid-world task, and the benefit of backward replay in large networks is not established.
- **Which experiences should be kept?** A first-in, first-out buffer forgets, while selection rules add cost. The best retention rule depends on the task.
- **Does the brain analogy predict new algorithms?** Whether the utility rule of Mattar and Daw (2018) would work as a selection rule for deep networks is an open question.

## References

### Seminal papers

- Lin, L.-J. (1992). Self-improving reactive agents based on reinforcement learning, planning and teaching. *Machine Learning* 8, 293–321. https://doi.org/10.1007/BF00992699 — Introduces experience replay for reinforcement-learning agents with neural-network learners, and tests it in a simulated survival task.
- Mnih, V. et al. (2015). Human-level control through deep reinforcement learning. *Nature* 518, 529–533. https://doi.org/10.1038/nature14236 — The deep Q-network, which samples uniformly from a replay memory of recent frames and learns Atari games from pixels.
- Foster, D. J. & Wilson, M. A. (2006). Reverse replay of behavioural sequences in hippocampal place cells during the awake state. *Nature* 440, 680–683. https://doi.org/10.1038/nature04587 — The biological counterpart: reverse replay of place-cell sequences in awake rats.

### Surveys and textbooks

- Wittkuhn, L. et al. (2021). Replay in minds and machines. *Neuroscience & Biobehavioral Reviews* 129, 367–388. https://doi.org/10.1016/j.neubiorev.2021.08.002 — Reviews the computational functions of replay in neuroscience and machine learning, and how the two fields relate.
