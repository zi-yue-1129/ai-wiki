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

Experience replay stores an agent's past transitions in a buffer and reuses them for later learning updates. It is a standard engineering tool, and it is the closest counterpart to hippocampal replay in this chapter.

This page is part of [Sleep, Replay and Memory Consolidation](../index.md). It compares the method with hippocampal replay. The algorithm itself, its variants and their trade-offs are covered on the [theory page on experience replay](../../../theory/paradigms/reinforcement-learning/experience-replay/index.md), which is not repeated here.

## Overview

A learner that uses each new transition once, in the order it occurs, sees strongly correlated data, because consecutive steps are similar. Keeping transitions in a buffer and drawing samples from it lets one experience inform several updates, and lets samples from different times be mixed together.

## Problem

The question for this chapter is whether the brain reuses recent experience in a similar way. Hippocampal replay reactivates recent sequences during rest and sleep, sometimes in reverse (see [Hippocampal replay](../hippocampal-replay/index.md)).

## Core idea

Each transition is stored as a tuple of state, action, reward and next state. Lin (1992) presented experience replay as one of three extensions for speeding up reinforcement learning, alongside learning action models for planning and teaching. The extensions were evaluated in a dynamic, nondeterministic environment. Mnih et al. (2015) kept a replay memory of recent experience in the deep Q-network and sampled from it at random. Random sampling breaks the correlation between consecutive steps.

The brain comparison lies in the structure. Both systems reuse recent experience out of the order in which it occurred. Hippocampal replay is compressed in time and tied to network events (see [Sharp-wave ripples](../sharp-wave-ripples/index.md)), while the artificial buffer is a plain store sampled at random. The match is in the principle, not in the mechanism.

## Equation or algorithm

In outline, the agent stores each transition, samples a mini-batch from the buffer, and updates its value estimates from the sampled transitions. The exact update rule is given on the [theory page on experience replay](../../../theory/paradigms/reinforcement-learning/experience-replay/index.md) and on the [deep Q-networks page](../../../theory/paradigms/reinforcement-learning/deep-q-networks/index.md).

## Results

- Lin (1992) evaluated the three extensions empirically in a dynamic, nondeterministic environment. Experience replay was one of them.
- Mnih et al. (2015) reported human-level control on a set of games with a deep Q-network that uses replay.

The DQN results combine replay with other components of the agent, so they do not isolate replay's contribution.

## Limitations

- **Memory cost.** Storing raw frames, especially images, is expensive, so the buffer size becomes a design constraint.
- **Uniform sampling spends updates evenly.** Transitions the agent already predicts well receive as many updates as rare or surprising ones. Prioritised methods change this, as the theory page describes.
- **Off-policy bias.** Stored transitions come from older policies, so updates from them differ from updates on the current policy.
- **Narrow evidence.** The DQN results come from one family of games. Generalisation to other domains needs separate evidence.
- **The brain analogy is suggestive.** The similarity with hippocampal replay is a point of comparison, not evidence that the brain uses this algorithm.

## Connections

- **Brain.** Replay in the hippocampus, described on [Hippocampal replay](../hippocampal-replay/index.md), reuses recent sequences, and reverse replay links outcomes back to earlier actions (Mattar and Daw, 2018). The memory-systems account is on [Complementary Learning Systems](../../memory-learning/complementary-learning-systems/index.md).
- **Reinforcement learning.** The algorithm is on [Deep Q-networks](../../../theory/paradigms/reinforcement-learning/deep-q-networks/index.md), and the general framework is on [Reinforcement Learning](../../../theory/paradigms/reinforcement-learning/index.md).
- **Continual learning.** Replay of old data to prevent forgetting uses the same buffer idea, as described on [Replay and memory in continual learning](../../../theory/paradigms/continual/replay-and-memory/index.md).

## Applications

- **Game-playing and control agents.** Deep Q-network style agents use replay buffers to learn from stored experience.
- **Continual learning.** Rehearsal of old data, interleaved with new data, is a common baseline against catastrophic forgetting.

## Open questions

- **Does reversing the order of replay help deep networks?** Reverse replay is a brain-inspired idea, and its benefit for large networks is not established.
- **Does the utility rule transfer?** Mattar and Daw's utility account (2018) is a candidate rule for choosing which experiences to replay. Whether it helps deep networks is an open question.

## References

### Seminal papers

- Lin, L.-J. (1992). Self-improving reactive agents based on reinforcement learning, planning and teaching. *Machine Learning* 8, 293–321. https://doi.org/10.1007/BF00992699 — Presents experience replay as one of three extensions for speeding up reinforcement learning (with learning action models for planning and teaching), evaluated in a dynamic, nondeterministic environment.
- Mnih, V. et al. (2015). Human-level control through deep reinforcement learning. *Nature* 518, 529–533. https://doi.org/10.1038/nature14236 — The deep Q-network, which learns from a replay memory of recent experience sampled at random.
- Foster, D. J. & Wilson, M. A. (2006). Reverse replay of behavioural sequences in hippocampal place cells during the awake state. *Nature* 440, 680–683. https://doi.org/10.1038/nature04587 — The biological counterpart: reverse replay of place-cell sequences during waking rest after running in rats.
- Mattar, M. G. & Daw, N. D. (2018). Prioritized memory access explains planning and hippocampal replay. *Nature Neuroscience* 21, 1609–1617. https://doi.org/10.1038/s41593-018-0232-z — Proposes that replay is ordered by utility, the extra reward an update would earn, and reproduces forward and reverse replay.

### Surveys and textbooks

- Wittkuhn, L. et al. (2021). Replay in minds and machines. *Neuroscience & Biobehavioral Reviews* 129, 367–388. https://doi.org/10.1016/j.neubiorev.2021.08.002 — Reviews replay in brains and in machine learning, comparing the two fields.
