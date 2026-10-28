---
tags:
  - reinforcement learning
  - offline reinforcement learning
  - batch RL
---

# Offline Reinforcement Learning

Offline reinforcement learning learns a policy from a fixed dataset of past interactions, without new exploration. It matters where online trial and error is costly or unsafe, such as medicine, recommendation and driving, and it poses the distribution shift problem directly.

## Overview

Offline data come from some behaviour policy, and the learned policy may visit actions the data never covered. Standard value learning then overestimates the value of those unseen actions, and the error goes unnoticed because nothing corrects it. Offline methods keep the learned policy close to the data, or make value estimates pessimistic where data are sparse.

## Main approaches

- **Batch-constrained Q-learning** (Fujimoto et al., 2019) restricts actions to those that resemble the data, which avoids bootstrapping from unseen actions.
- **Conservative Q-learning** (Kumar et al., 2020) adds a penalty that lowers Q-values on out-of-distribution actions, so the learned values are pessimistic.
- **Decision transformers** (Chen et al., 2021) treat offline RL as sequence modelling, predicting actions conditioned on desired returns, and avoid explicit value estimation.
- **Behaviour cloning** is the simplest baseline, and is often competitive when data are good, see [imitation learning](../../imitation/index.md).

## Evaluation

Offline policies cannot be evaluated by running them safely, so off-policy evaluation estimates their return from logged data. Estimates depend on coverage and overlap, and they can be badly wrong when the new policy differs from the data.

## Connections

Offline RL is closely tied to [imitation learning](../../imitation/index.md), since the data are often demonstrations, and to [value-based methods](../value-based-methods/index.md). The distribution-shift problem is the same one studied in [transfer learning](../../transfer/index.md). Reasoning about logged data under confounding draws on [probabilistic methods](../../../probabilistic/index.md).

## Applications

Treatment policies from clinical records, recommendation and advertising from logs, robotic control from teleoperated demonstrations, and energy management from historical operation data.

## Open questions

Reliable off-policy evaluation without strong overlap assumptions is unsolved. Combining large offline datasets with a small amount of online fine-tuning is an active area, and it is unclear how much pessimism is the right amount.

## References

### Seminal papers

- Fujimoto, Meger & Precup (2019), "Off-policy deep reinforcement learning without exploration", ICML, arXiv:1812.02900 — Batch-constrained Q-learning, which keeps the policy within the support of the data.
- Kumar, Zhou, Tucker & Levine (2020), "Conservative Q-learning for offline reinforcement learning", NeurIPS, arXiv:2006.04779 — Pessimistic Q-values that prevent overestimating unseen actions.
- Wu, Tucker & Nachum (2019), "Behavior regularized offline reinforcement learning", arXiv:1911.11361 — Regularises the policy toward the behaviour data, a simple and strong offline baseline.
- Chen et al. (2021), "Decision transformer: reinforcement learning via sequence modeling", NeurIPS, arXiv:2106.01345 — Frames offline RL as conditional sequence prediction over returns.

### Surveys and textbooks

(none checked for this page)

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Levine, Kumar, Tucker & Fu (2020), "Offline reinforcement learning: tutorial, review, and perspectives on open problems", arXiv:2005.01643 — Tutorial and review of the field, including its open problems.

## Further reading

- Lange, Gabel & Riedmiller (2012), "Batch reinforcement learning", in *Reinforcement Learning: State of the Art*. No link checked.
