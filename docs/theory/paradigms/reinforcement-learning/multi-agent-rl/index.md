---
status: draft
last_reviewed: 2026-10-28
aliases:
  - Multi-agent reinforcement learning
  - MARL
  - 多智能體強化學習
---

# Multi-agent reinforcement learning

Several learning agents act in the same environment, and each agent's experience depends on what the others do.

## Overview

Single-agent reinforcement learning assumes a fixed environment. When other agents are also learning, the environment looks non-stationary to each agent, because the others' policies change during training. The standard model is the Markov game, a generalisation of the Markov decision process with one reward function per agent and joint actions. Busoniu, Babuska and De Schutter (2008) survey the field, grouping tasks into cooperative, competitive and mixed settings.

## Key concepts

- **Non-stationarity.** Each agent's policy changes during training, so the transition dynamics it sees change too. Lowe et al. (2017) name this as the reason experience replay cannot be applied naively.
- **Centralised training, decentralised execution.** Agents can use extra information during training, such as the other agents' actions, and act from their own observations at test time.
- **Credit assignment.** When a team receives one reward, it is hard to tell which agent's action caused it.
- **Communication.** Agents can learn what to send each other when no channel is designed in advance, see [emergent communication](emergent-communication/index.md).

## Training schemes

- **Independent learners** treat the other agents as part of the environment. They are simple to implement, but suffer from non-stationarity.
- **Centralised critics** with decentralised actors, as in [MADDPG](maddpg/index.md), give each agent a value function that sees the other agents' actions.
- **Value factorisation**, as in [QMIX](qmix/index.md), learns per-agent values and combines them so that the joint greedy action is the same as the team's best action.
- **Shared-parameter policy gradients**, as in [MAPPO](mappo/index.md), use one policy network for homogeneous agents, with a centralised value function.

## Population-based training and self-play

Competitive and mixed settings often train agents against a population of past or rival policies, as described in [population-based training](population-based-training/index.md). In OpenAI et al. (2019), the Dota 2 team trains with self-play: rollouts play the latest policy in 80% of games and older policies in 20%. The OpenAI Five team won 99.4% of over 7,000 games in a public arena. Vinyals et al. (2019) report grandmaster-level play in StarCraft II with multi-agent reinforcement learning.

## Applications

- **Games.** StarCraft II and Dota 2 are the best-known testbeds, as in the papers above.
- **Cooperative simulated tasks.** Navigation, communication and predator–prey tasks are standard benchmarks for the centralised-critic methods (Lowe et al., 2017).

## Open questions

- How to keep learning stable as the number of agents grows.
- How agents can learn to communicate and cooperate without hand-designed channels.
- How to evaluate agents when the opponents themselves keep changing.

## Connections

- Parent topic: [Reinforcement Learning](../index.md)
- The single-agent building blocks are [Deep Q-networks](../deep-q-networks/index.md) and [Proximal Policy Optimisation](../proximal-policy-optimisation/index.md).

## References

### Seminal papers

- Lowe et al. (2017), "Multi-agent actor-critic for mixed cooperative-competitive environments", [arXiv:1706.02275](https://arxiv.org/abs/1706.02275) — MADDPG, which introduces centralised critics with decentralised actors.
- Rashid et al. (2018), "QMIX: Monotonic value function factorisation for deep multi-agent reinforcement learning", *Proceedings of ICML 2018*, PMLR 80, [arXiv:1803.11485](https://arxiv.org/abs/1803.11485) — Value factorisation with a monotonic mixing network.
- Yu et al. (2022), "The surprising effectiveness of PPO in cooperative multi-agent games", NeurIPS 2022 Datasets and Benchmarks Track, [arXiv:2103.01955](https://arxiv.org/abs/2103.01955) — MAPPO, a strong PPO baseline for cooperative benchmarks.
- Vinyals et al. (2019), "Grandmaster level in StarCraft II using multi-agent reinforcement learning", *Nature* 575, 350–354. https://doi.org/10.1038/s41586-019-1724-z — Grandmaster-level StarCraft II play with multi-agent training.
- OpenAI et al. (2019), "Dota 2 with large scale deep reinforcement learning", [arXiv:1912.06680](https://arxiv.org/abs/1912.06680) — Self-play with PPO and an LSTM policy, beating the reigning world champions.

### Surveys and textbooks

- Busoniu, Babuska & De Schutter (2008), "A comprehensive survey of multiagent reinforcement learning", *IEEE Transactions on Systems, Man, and Cybernetics, Part C* 38(2), 156–172. https://doi.org/10.1109/tsmcc.2007.913919 — Survey of multi-agent RL settings, learning approaches and open problems.
