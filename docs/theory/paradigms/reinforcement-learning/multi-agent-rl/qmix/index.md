---
status: complete
last_reviewed: 2026-10-28
aliases:
  - QMIX
  - 單調值函數分解
---

# QMIX: monotonic value function factorisation (Rashid et al., 2018)

Learns a value for each agent and a mixing network that combines them into a team value, with a constraint that makes each agent's greedy choice consistent with the team's best joint action.

## Problem

Independent learners suffer from non-stationarity. A full joint action-value function over all agents grows exponentially with the number of agents, so it is impractical. The question is how to train a team value function that can be used with decentralised, per-agent action selection at execution time.

## Core idea

Each agent has its own action-value function \(Q_a\) over its observations. A mixing network combines these into a team value \(Q_{tot}\), and it is trained end-to-end with a temporal-difference loss on \(Q_{tot}\). The constraint is that \(Q_{tot}\) is monotonic in each agent's value,

\[
\frac{\partial Q_{tot}}{\partial Q_a} \ge 0 \quad \text{for all agents } a.
\]

Rashid et al. enforce this by making the weights of the mixing network non-negative, and generating those weights from state-conditioned hypernetworks followed by an absolute-value activation. Because of the monotonicity, a global argmax over \(Q_{tot}\) gives the same result as each agent taking its own argmax. Execution therefore needs only the per-agent values.

## Equation or algorithm

The team value is \(Q_{tot}(\tau, \mathbf{u}) = f_{\text{mix}}(Q_1(\tau_1, u_1), \ldots, Q_N(\tau_N, u_N); s)\), where \(\tau_a\) is agent \(a\)'s observation history, \(u_a\) its action and \(s\) the global state. The procedure:

1. Each agent computes \(Q_a\) from its own observation history.
2. The mixing network combines these values with weights produced from the global state, and gives \(Q_{tot}\).
3. Train all parts together with a temporal-difference loss on \(Q_{tot}\), with a target network.
4. At execution time, each agent picks the action with the largest \(Q_a\), with no central coordinator.

## Results

The experiments use decentralised unit micromanagement in StarCraft II, on six maps: 3m, 5m, 8m, 2s_3z, 3s_5z and 1c_3s_5z. The baselines are independent Q-learning (IQL) and VDN. Results are test win rates averaged over 20 runs, with 95% confidence intervals. The paper reports that "QMIX is noticeably the strongest performer on all of the maps" (Section 7.1).

## Limitations

- **Representable value functions.** The monotonicity constraint means QMIX cannot represent every team value function. Any function in which one agent's best action depends on the others' actions is outside the class that the mixing network can express.
- **Discrete actions.** The argmax on each agent's values assumes a finite action set.
- **Benchmark scope.** The experiments are on one family of micromanagement maps, and the paper does not test wider settings.

## Connections

- Parent topic: [Multi-agent reinforcement learning](../index.md), and the wider [Reinforcement Learning](../../index.md) overview.
- The single-agent value method it extends is [Deep Q-networks](../../deep-q-networks/index.md), in the [value-based methods](../../value-based-methods/index.md) family.
- The centralised-critic alternative for continuous actions is [MADDPG](../maddpg/index.md), and the on-policy alternative is [MAPPO](../mappo/index.md).

## Applications

- **Team games.** Micromanagement in StarCraft II, where a team of units must coordinate attacks.
- **Coordinated control.** Any cooperative task with discrete actions where a single team reward is available.

## Open questions

- How to extend factorisation to value functions that do not satisfy the monotonicity constraint.
- How to combine factorisation with continuous actions and with communication between agents.

## References

### Seminal papers

- Rashid et al. (2018), "QMIX: Monotonic value function factorisation for deep multi-agent reinforcement learning", *Proceedings of ICML 2018*, PMLR 80, [arXiv:1803.11485](https://arxiv.org/abs/1803.11485) — The QMIX paper, with the monotonic mixing network and the StarCraft II results above.
- Mnih et al. (2015), "Human-level control through deep reinforcement learning", *Nature* 518, 529–533. https://doi.org/10.1038/nature14236 — The deep Q-learning agent whose per-agent value function QMIX builds on.
- Lowe et al. (2017), "Multi-agent actor-critic for mixed cooperative-competitive environments", [arXiv:1706.02275](https://arxiv.org/abs/1706.02275) — MADDPG, the centralised-critic alternative for multi-agent learning.
- Yu et al. (2022), "The surprising effectiveness of PPO in cooperative multi-agent games", [arXiv:2103.01955](https://arxiv.org/abs/2103.01955) — Compares a PPO baseline with QMIX on StarCraft II maps and other benchmarks.

### Surveys and textbooks

- Busoniu, Babuska & De Schutter (2008), "A comprehensive survey of multiagent reinforcement learning", *IEEE Transactions on Systems, Man, and Cybernetics, Part C* 38(2), 156–172. https://doi.org/10.1109/TSMCC.2007.913919 — Survey of multi-agent learning settings and their difficulties.
