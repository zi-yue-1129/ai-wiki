---
status: draft
last_reviewed: 2026-10-28
tags:
  - reinforcement learning
  - agents
aliases:
  - QMIX
  - 單調值函數分解
  - Monotonic value function factorisation
---

# QMIX (Rashid et al., 2018)

QMIX is a value-based method for cooperative [multi-agent reinforcement learning](../index.md). It learns a value for each agent and combines them into a joint value for the team, with a constraint that makes each agent's own greedy choice consistent with the best joint action. Teams are trained with the joint value and then act from their individual values alone.

## Overview

In a cooperative team every agent shares one reward. The natural quantity is a joint action value $Q_{\text{tot}}(\boldsymbol{\tau}, \mathbf{a})$, but the joint action space grows exponentially with the number of agents, and a decentralised team needs each agent to choose its action from something it can compute alone. Value decomposition offers a route. Sunehag et al. (2017) proposed VDN, which sums per-agent values. The sum is simple but limits the joint values that can be represented. QMIX keeps the decomposition but replaces the sum with a learned nonlinear mixture, and the constraint that the mixture is monotonic in each agent's value keeps decentralised execution correct. The method extends [deep Q-networks](../../deep-q-networks/index.md) to the multi-agent case.

## Key concepts

- **Per-agent utility** $Q_a(\tau_a, a_a)$: the value that agent $a$ assigns to its own action, given its local history of observations and actions.
- **Mixing network**: combines the per-agent utilities into $Q_{\text{tot}}$. It is used only during training.
- **Hypernetwork**: a small network that reads the global state and outputs the weights of the mixing network, so the mixture can depend on information that no single agent sees.
- **Monotonicity**: the joint value never falls when one agent's value rises. This is what allows each agent to act greedily on its own value.

## How it works

QMIX factorises the joint value as

$$
Q_{\text{tot}}(\boldsymbol{\tau}, \mathbf{a}; \theta) = f_{\text{mix}}\big(Q_1(\tau_1, a_1), \dots, Q_n(\tau_n, a_n); s\big), \qquad \frac{\partial Q_{\text{tot}}}{\partial Q_a} \ge 0 \;\; \text{for every agent } a,
$$

where $s$ is the global state. The monotonicity condition implies that the joint greedy action is the combination of each agent's greedy action, which is the consistency property that makes decentralised execution valid. In the paper's architecture, the mixing weights are kept non-negative by taking absolute values of the hypernetwork outputs, a sufficient condition for monotonicity; the biases are unconstrained.

Training uses the usual deep Q-learning loss on the joint value, with a target network and a replay buffer:

$$
L(\theta) = \mathbb{E}\Big[\big(r + \gamma \max_{\mathbf{a}'} Q_{\text{tot}}^{-}(\boldsymbol{\tau}', \mathbf{a}'; \theta^{-}) - Q_{\text{tot}}(\boldsymbol{\tau}, \mathbf{a}; \theta)\big)^2\Big].
$$

The algorithm proceeds as follows:

1. Each agent's utility network computes $Q_a$ from its own observation history.
2. The hypernetworks read the global state and produce the mixing weights.
3. The mixing network combines the utilities into $Q_{\text{tot}}$.
4. The loss is minimised on a batch of stored transitions, and the target network is updated periodically.
5. At execution time each agent takes the argmax of its own $Q_a$. The mixer is not used.

## Results

The paper's main evidence comes from the StarCraft Multi-Agent Challenge (SMAC), a set of micromanagement scenarios in which a team of units must defeat a built-in opponent. The paper reports that QMIX outperforms VDN and the policy-gradient method COMA on these maps, with the gap largest on the scenarios that demand the most coordination. The exact win rates are in the paper and should be read there.

## Limitations

- **Restricted representation.** Monotonicity limits the joint values that can be expressed. Son et al. (2019) show that some factorisable tasks cannot be represented this way and propose QTRAN to address the gap.
- **Shared reward only.** QMIX assumes a team reward. Competitive or mixed-motive settings need different methods, such as [MADDPG](../maddpg/index.md).
- **Global state in training.** The hypernetworks use the global state, which must be available during training.
- **Discrete actions.** The value-based design does not directly handle continuous action spaces.

## Open questions

Does a richer factorisation, one that is not monotonic, generalise better or only fit the training team? Papoudakis et al. (2020) compare value decomposition with other families on common tasks, which makes it possible to ask how much the mixing network adds in practice. A further question is how QMIX-style value decomposition combines with on-policy methods such as the PPO variant studied by Yu et al. (2021).

## References

### Seminal papers

- Rashid, T. et al. (2018). *QMIX: Monotonic Value Function Factorisation for Deep Multi-Agent Reinforcement Learning*. arXiv:1803.11485. https://arxiv.org/abs/1803.11485 — The QMIX paper, which mixes per-agent values with a monotonic network conditioned on the global state.
- Sunehag, P. et al. (2017). *Value-Decomposition Networks For Cooperative Multi-Agent Learning*. arXiv:1706.05296. https://arxiv.org/abs/1706.05296 — VDN, which decomposes the team value into a sum of agent-wise values and identifies the lazy-agent problem.
- Son, K. et al. (2019). *QTRAN: Learning to Factorize with Transformation for Cooperative Multi-Agent Reinforcement Learning*. arXiv:1905.05408. https://arxiv.org/abs/1905.05408 — Shows that VDN and QMIX cover only part of the factorisable tasks and proposes a factorisation that avoids their structural constraints.
- Foerster, J. et al. (2017). *Counterfactual Multi-Agent Policy Gradients*. arXiv:1705.08926. https://arxiv.org/abs/1705.08926 — COMA, a centralised critic with decentralised actors, used here as a comparison method on SMAC.

### Articles and documentation

- Yu, C. et al. (2021). *The Surprising Effectiveness of PPO in Cooperative, Multi-Agent Games*. arXiv:2103.01955. https://arxiv.org/abs/2103.01955 — Shows that PPO-based multi-agent methods perform strongly on cooperative benchmarks, including StarCraft tasks.
- Papoudakis, G. et al. (2020). *Benchmarking Multi-Agent Deep Reinforcement Learning Algorithms in Cooperative Tasks*. arXiv:2006.07869. https://arxiv.org/abs/2006.07869 — Compares independent learning, centralised policy gradients and value decomposition methods such as QMIX on common cooperative tasks.
