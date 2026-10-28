---
status: draft
last_reviewed: 2026-10-28
aliases:
  - Population-based training
  - 基於種群的訓練
---

# Population-based training

Population-based training (PBT) trains many agents at once and lets them learn from each other. Good members copy the weights and hyperparameters of better members, and then explore new settings. The result is a schedule of hyperparameters that changes during training, rather than one fixed setting. In multi-agent reinforcement learning, a population also provides opponents, so the methods here are used to train agents for competitive and mixed games.

## Problem

A fixed hyperparameter setting is rarely best for a whole training run. Learning rates and exploration settings that help early can hurt later. Searching over settings with separate runs costs a lot of compute, and the best setting found by search is still fixed. In competitive games there is an additional problem: an agent trained only against one opponent can fail against others, so the training population must be diverse.

## Main approaches

- **[Population-based training (PBT)](pbt/index.md)** (Jaderberg et al., 2017) runs a population asynchronously. A worker that under-performs copies the weights and hyperparameters of a better worker, then perturbs the copied hyperparameters. The result is a schedule of hyperparameter values.
- **[Capture the Flag agents (FTW)](ftw/index.md)** (Jaderberg et al., 2019) trains a population of independent agents by playing teams together and against each other in randomly generated maps. Each agent learns its own internal reward, and the authors report human-level play in the first-person game Quake III Arena.
- **Self-play against older policies**, as in the OpenAI Five training described in the [overview](../index.md), plays the latest policy in most games and older policies in the rest, so that training does not overfit to the latest policy.

## Comparison

| Method | Population role | Schedule | Target |
|---|---|---|---|
| PBT | Copy and perturb members | Hyperparameters change during training | Single-agent training, supervised and generative models |
| FTW | Teammates and opponents | Internal rewards and policies | Team competition in 3D games |
| Self-play with older policies | Past policies as opponents | Opponent sampling | Competitive games |

## Connections

- The population is a form of [evolutionary computation](../../../../../theory/paradigms/evolutionary/index.md) with gradient-based inner loops.
- The competitive setting relates to [self-play](../../../../../applications/games/index.md) for board games such as [AlphaZero](../../alphazero/index.md).
- Hyperparameter schedules are part of the [optimisation](../../../../../theory/optimization/index.md) methods that train neural networks.

## Applications

- **Hyperparameter tuning** for reinforcement learning, supervised learning and generative models.
- **Competitive games**, such as first-person team games and real-time strategy.

## Open questions

- How large a population is needed, and how to set the exploit and explore rules for a new application.
- How to keep a population diverse enough to avoid collapse to a single strategy.

## References

### Seminal papers

- Jaderberg et al. (2017), "Population based training of neural networks", [arXiv:1711.09846](https://arxiv.org/abs/1711.09846) — Introduces PBT, with the exploit and explore steps and the hyperparameter schedules it finds.
- Jaderberg et al. (2019), "Human-level performance in 3D multiplayer games with population-based reinforcement learning", *Science* 364, 859–865. https://doi.org/10.1126/science.aau6249 — Trains a population of agents to play Capture the Flag at human level.
- Vinyals et al. (2019), "Grandmaster level in StarCraft II using multi-agent reinforcement learning", *Nature* 575, 350–354. https://doi.org/10.1038/s41586-019-1724-z — Multi-agent training that reaches grandmaster level in StarCraft II, a competitive setting that this page compares with.
- Snoek, Larochelle & Adams (2012), "Practical Bayesian optimization of machine learning algorithms", [arXiv:1206.2944](https://arxiv.org/abs/1206.2944) — Bayesian optimisation of hyperparameters, the search-based alternative that PBT's schedules are compared with.
- Jaderberg et al. (2016), "Reinforcement learning with unsupervised auxiliary tasks", [arXiv:1611.05397](https://arxiv.org/abs/1611.05397) — UNREAL, one of the agents that PBT tunes in the original paper.

### Surveys and textbooks

- Busoniu, Babuska & De Schutter (2008), "A comprehensive survey of multiagent reinforcement learning", *IEEE Transactions on Systems, Man, and Cybernetics, Part C* 38(2), 156–172. https://doi.org/10.1109/tsmcc.2007.913919 — Survey of multi-agent learning settings, including the competitive settings that populations address.
