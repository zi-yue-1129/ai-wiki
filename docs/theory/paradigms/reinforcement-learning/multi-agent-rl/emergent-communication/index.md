---
status: draft
last_reviewed: 2026-10-28
aliases:
  - Emergent communication
  - 湧現式通訊
---

# Emergent communication

Emergent communication studies agents that learn what to say to each other. The message channel is not designed in advance. Agents learn both a protocol, which says what each message means, and a policy that acts on it. The question is whether useful symbols, and possibly something like language, arise from the need to cooperate.

## Problem

In a partially observable task, one agent may hold information that another needs. If the channel is fixed by hand, the learning problem is reduced to choosing actions. If the channel is learned, the agents must solve two problems at once: they must decide what to send, and they must learn what the messages mean to the receiver. The learning signal for the message is also indirect, because it comes only through the team's reward.

## Main approaches

- **[RIAL and DIAL](rial-dial/index.md)** (Foerster et al., 2016) learn communication with deep Q-learning. RIAL treats messages as discrete actions. DIAL passes error gradients through a noisy channel during training.
- **[CommNet](commnet/index.md)** (Sukhbaatar et al., 2016) uses continuous messages. Each agent receives the sum of the other agents' transmitted vectors, and the policy and the communication are trained together by back-propagation.
- **Referential games** (Lazaridou et al., 2017) give a speaker and a listener an image and ask the listener to pick the same image from a set. The agents coordinate on symbols, and the study examines whether those symbols can be grounded in human language.

## Comparison

| Method | Message type | Training signal | Main question |
|---|---|---|---|
| RIAL | Discrete symbols | Deep Q-learning on the message action | Can messages be learned at all? |
| DIAL | Continuous values in training, discretised at execution | Gradients through the channel | Can credit flow between agents? |
| CommNet | Continuous vectors | Reward through the policy | Does communication help cooperative tasks? |
| Referential game | Discrete symbols | Reward for matching the image | Do the symbols carry meaning? |

## Connections

- Communication is a special case of a [Markov game](../index.md) with partial observability and a shared reward.
- Multi-agent methods that do not communicate, such as [MADDPG](../maddpg/index.md) and [QMIX](../qmix/index.md), usually fix the coordination channel to the critic during training.
- The grounding problem in referential games is close to the study of [language models](../../../../models/llm/index.md), which learn language from text rather than from interaction.

## Open issues and further variants

- Emergent protocols often fail to transfer to new partners or new tasks.
- Learned symbols may not be understood by humans, which limits interpretability.
- Simple reward signals may not produce compositional language, so the training setup matters as much as the model.

## References

### Seminal papers

- Foerster et al. (2016), "Learning to communicate with deep multi-agent reinforcement learning", [arXiv:1605.06676](https://arxiv.org/abs/1605.06676) — Introduces RIAL and DIAL, and the switch riddle and other communication tasks.
- Sukhbaatar, Szlam & Fergus (2016), "Learning multiagent communication with backpropagation", [arXiv:1605.07736](https://arxiv.org/abs/1605.07736) — Introduces CommNet, a continuous communication model trained jointly with the policy.
- Lazaridou, Peysakhovich & Baroni (2017), "Multi-agent cooperation and the emergence of (natural) language", [arXiv:1612.07182](https://arxiv.org/abs/1612.07182) — Studies emergent symbols in referential games and how they can be grounded in human language.
- Lowe et al. (2017), "Multi-agent actor-critic for mixed cooperative-competitive environments", [arXiv:1706.02275](https://arxiv.org/abs/1706.02275) — Centralised critics, which many emergent-communication studies use as a baseline.

### Surveys and textbooks

- Busoniu, Babuska & De Schutter (2008), "A comprehensive survey of multiagent reinforcement learning", *IEEE Transactions on Systems, Man, and Cybernetics, Part C* 38(2), 156–172. https://doi.org/10.1109/tsmcc.2007.913919 — Survey of multi-agent learning settings, including communication as a coordination tool.
