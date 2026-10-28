---
status: draft
last_reviewed: 2026-10-28
aliases:
  - MAPPO
  - 多智能體 PPO
---

# Multi-agent PPO (Yu et al., 2022)

Shows that PPO with a shared policy and a centralised value function is a strong baseline for cooperative multi-agent games, competitive with QMIX and MADDPG on several benchmarks.

## Problem

Off-policy and value-factorisation methods such as QMIX and MADDPG dominated cooperative multi-agent benchmarks. PPO is simple and widely used, but was assumed to be weaker in multi-agent settings. Yu et al. ask whether PPO, adapted in a few principled ways, performs well on these tasks.

## Core idea

The paper compares independent PPO (IPPO), where each agent has its own critic on local observations, with MAPPO, where agents share one policy network and a centralised value function takes the global state as input. Parameter sharing is used in settings where the agents are homogeneous, and the paper reports that parameter sharing "outperforms MAPPO without parameter sharing by a clear margin" in its appendix. The value function can take both agent-specific features and global features as input.

## Equation or algorithm

MAPPO is the PPO algorithm of [Proximal Policy Optimisation](../../proximal-policy-optimisation/index.md), with three changes: a shared actor across agents, a centralised value function \(V(s)\) over the global state, and advantage estimates computed from that value. The paper recommends the following practices:

- **Value normalisation** to stabilise value learning.
- **Value input** with both local, agent-specific features and global features, where these are available.
- **Limited epochs.** Up to 10 training epochs on difficult environments and 15 on easy ones.
- **Clipping** with a ratio below 0.2 for the best performance.
- **Large batch sizes** for the best task performance.

The paper also finds that performance degrades when samples are reused too often in multi-agent domains.

## Results

- **SMAC.** IPPO and MAPPO perform strongly on the vast majority of maps. MAPPO performs at least as well as QMIX on most maps with the same number of samples. On 6h_vs_8z, MAPPO with feature pruning reaches a median win rate of 88.3%, against 9.4% for QMIX.
- **MPE.** MAPPO performs comparably to the off-policy baselines, and very similarly to QMIX on all tasks.
- **Google Research Football.** MAPPO clearly outperforms QMIX in each scenario. On 3v1, it reaches 88.03 against 8.12 for QMIX.
- **Hanabi.** MAPPO produces results comparable or superior to the best and average returns reported for the benchmark.

## Limitations

- **Sample reuse.** Performance degrades when training data is reused too often, which limits the sample efficiency of an on-policy method.
- **Homogeneous agents.** Parameter sharing fits homogeneous agents most naturally. The paper's strongest claims are for settings of that kind.
- **Hyperparameter sensitivity.** Several of the recommended factors interact, so the results depend on careful tuning.

## Connections

- Parent topic: [Multi-agent reinforcement learning](../index.md), and the wider [Reinforcement Learning](../../index.md) overview.
- The single-agent algorithm it adapts is [Proximal Policy Optimisation](../../proximal-policy-optimisation/index.md).
- The main alternatives are [QMIX](../qmix/index.md), a value-factorisation method, and [MADDPG](../maddpg/index.md), a centralised-critic actor-critic method.

## Applications

- **Cooperative benchmarks.** StarCraft Multi-Agent Challenge, Google Research Football and Hanabi, as used in the paper.
- **Team coordination in simulation.** Multi-agent navigation and communication tasks with a shared reward.

## Open questions

- How well the recommended practices carry over to heterogeneous teams and to larger numbers of agents.
- How to combine on-policy stability with the sample efficiency of replay-based methods.

## References

### Seminal papers

- Yu et al. (2022), "The surprising effectiveness of PPO in cooperative multi-agent games", NeurIPS 2022 Datasets and Benchmarks Track, arXiv:2103.01955 — The MAPPO paper, with the benchmark results and recommended practices above.
- Schulman et al. (2017), "Proximal policy optimization algorithms", arXiv:1707.06347 — The single-agent PPO algorithm that MAPPO adapts.
- Rashid et al. (2018), "QMIX: Monotonic value function factorisation for deep multi-agent reinforcement learning", *Proceedings of ICML 2018*, PMLR 80, arXiv:1803.11485 — The value-factorisation baseline that MAPPO is compared against.
- Lowe et al. (2017), "Multi-agent actor-critic for mixed cooperative-competitive environments", arXiv:1706.02275 — MADDPG, the centralised-critic baseline in the paper's comparisons.
- Engstrom et al. (2020), "Implementation matters in deep policy gradients: a case study on PPO and TRPO", arXiv:2005.12729 — Shows that implementation details, which the MAPPO recommendations also depend on, can change PPO's results.
