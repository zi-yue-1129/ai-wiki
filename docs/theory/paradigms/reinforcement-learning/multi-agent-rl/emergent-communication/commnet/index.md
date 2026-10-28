---
status: draft
last_reviewed: 2026-10-28
aliases:
  - CommNet
  - Communication neural network
---

# CommNet (Sukhbaatar et al., 2016)

A fully cooperative model in which agents communicate by sending continuous vectors over a shared broadcast channel. The channel and the policy are learned together by back-propagation.

## Problem

Many cooperative tasks involve agents that see only part of the environment. In most earlier work the communication protocol was fixed by the designer. Sukhbaatar et al. ask whether agents can learn what to transmit, and whether the learned communication helps them perform better than agents that do not communicate.

## Core idea

The model treats all \(J\) agents as parts of one large feed-forward controller. Each agent occupies a subset of units, and the connectivity between layers is a broadcast channel. At each step, agent \(j\) produces a hidden state \(h_j\) from its input. Each agent then receives the sum of the other agents' transmitted vectors, and its next hidden state is computed from its own state and that sum. Because the channel is continuous, the whole system can be trained with ordinary back-propagation, and it can be combined with standard single-agent reinforcement learning or supervised learning.

The model is simple, so it can be applied to a wide range of tasks with partial visibility. It also allows the number of agents to change at run time, which the authors note matters for applications such as communication between moving cars.

## Equation or algorithm

With agent \(j\) transmitting a vector \(c_j\) derived from its hidden state, the input to agent \(i\) at the next layer is

\[
\text{input}_i = \sum_{j \ne i} c_j ,
\]

so the communication vector for each agent is the sum of the transmissions of the others. The policy for each agent is then produced from the combined hidden state, and the reward is shared by all agents.

## Results

The paper evaluates CommNet on several cooperative tasks, including a lever-pulling task, a traffic junction in which cars must pass through without colliding, and a combat task. The abstract reports that agents "learn to communicate amongst themselves, yielding improved performance over non-communicative agents and baselines". In some cases, the learned language can be interpreted, revealing simple strategies for solving the task.

## Limitations

- **Full cooperation is assumed.** Every agent receives the same reward, so the model does not address competitive settings.
- **Sum-based communication.** Summing transmissions treats all other agents alike, so the model cannot easily focus on particular agents.
- **Interpretability.** Some learned messages can be interpreted, but this depends on the task.

## Connections

- DIAL, described in [RIAL and DIAL](../rial-dial/index.md), also trains communication end to end, but uses discrete messages at execution time.
- CommNet is one of the emergent-communication methods covered in the [overview](../index.md).
- [MADDPG](../../maddpg/index.md) coordinates agents without a learned channel. Its centralised critics see the other agents' actions during training, instead of messages.

## Applications

- **Traffic control.** Cars communicate about the junction, as in the traffic junction task.
- **Multi-robot coordination**, where robots have partial views and must share information.

## Open questions

- How to handle communication among a large or changing number of agents.
- How to make learned messages easier to interpret.

## References

### Seminal papers

- Sukhbaatar, Szlam & Fergus (2016), "Learning multiagent communication with backpropagation", *Advances in Neural Information Processing Systems 29 (NIPS 2016)*, [arXiv:1605.07736](https://arxiv.org/abs/1605.07736) — The CommNet paper, with the broadcast channel, the back-propagation training and the traffic junction and combat tasks.
- Foerster et al. (2016), "Learning to communicate with deep multi-agent reinforcement learning", [arXiv:1605.06676](https://arxiv.org/abs/1605.06676) — RIAL and DIAL, which learn discrete and differentiable messages for comparison.
- Lazaridou, Peysakhovich & Baroni (2017), "Multi-agent cooperation and the emergence of (natural) language", [arXiv:1612.07182](https://arxiv.org/abs/1612.07182) — Studies emergent symbols in referential games and how they can be grounded in human language.
- Lowe et al. (2017), "Multi-agent actor-critic for mixed cooperative-competitive environments", [arXiv:1706.02275](https://arxiv.org/abs/1706.02275) — Centralised critics for comparison with communication-based coordination.

### Surveys and textbooks

- Busoniu, Babuska & De Schutter (2008), "A comprehensive survey of multiagent reinforcement learning", *IEEE Transactions on Systems, Man, and Cybernetics, Part C* 38(2), 156–172. https://doi.org/10.1109/tsmcc.2007.913919 — Survey of multi-agent learning settings, including communication as a coordination tool.
