---
status: draft
last_reviewed: 2026-10-28
aliases:
  - MADDPG
  - 多智能體深度確定性策略梯度
---

# Multi-agent deep deterministic policy gradient (Lowe et al., 2017)

A centralised-critic method: during training each agent's critic sees every agent's observations and actions, while each actor uses only its own observations at execution time.

## Problem

Independent learners see a non-stationary environment, since the other agents keep changing. Experience replay becomes unreliable for the same reason. Lowe et al. ask whether agents in mixed cooperative and competitive settings can learn coordinated behaviour when they are trained with extra information that is not available at test time.

## Core idea

The paper adopts centralised training with decentralised execution. Each agent \(i\) has an actor \(\mu_i\) that maps its local observation \(o_i\) to an action, and a critic \(Q_i\) that takes the state information \(x\) and the actions of all agents. In the simplest case \(x = (o_1, \ldots, o_N)\). Because the critic knows what the other agents do, the environment is stationary from its point of view, even though the other policies are changing. The actor is trained with the deterministic policy gradient through its own critic, as in [DDPG](../../policy-gradient-and-actor-critic/ddpg/index.md).

The paper also proposes two extensions. Policy ensembles train \(K\) sub-policies per agent and select one at random for each episode. Policy inference learns approximate models of the other agents' policies from observations, for settings where they are not known.

## Equation or algorithm

For agent \(i\), the actor update is the deterministic policy gradient through the centralised critic:

\[
\nabla_{\theta_i} J(\mu_i) = \mathbb{E}_{x, \mathcal{D}}\left[\nabla_{\theta_i}\mu_i(o_i)\, \nabla_{a_i} Q_i^{\mu}(x, a_1, \ldots, a_N)\big|_{a_i = \mu_i(o_i)}\right]
\]

The critic is trained with a temporal-difference target built from the target actors, as in DDPG. The procedure:

1. Run the current actors, each on its own observation, and store the joint transition.
2. Sample a minibatch of joint transitions from the replay buffer.
3. Update each critic \(Q_i\) with its centralised target.
4. Update each actor \(\mu_i\) with the gradient through its critic.
5. Update target networks slowly and repeat.

## Results

The paper evaluates on six multi-agent environments: cooperative communication, cooperative navigation, keep-away, physical deception, predator–prey, and covert communication. It reports that "in all cases, MADDPG outperforms DDPG when directly pitted against it". In cooperative communication, agents reach the target in 84.0% of episodes with MADDPG against 32.0% with DDPG. The authors also report that agents with policy ensembles are stronger than those with a single policy.

## Limitations

- **Centralised information.** Training needs the other agents' actions and observations, which may not be available in all deployments.
- **Scaling.** The critic's input grows with the number of agents, so the joint action space grows as well.
- **Inferred policies.** Where the other policies are not known, the approximate policy inference is an extra source of error.
- **Continuous actions.** The method inherits the continuous-action setting of DDPG, and its deterministic actors need exploration noise.

## Connections

- Parent topic: [Multi-agent reinforcement learning](../index.md), and the wider [Reinforcement Learning](../../index.md) overview.
- It builds on [DDPG](../../policy-gradient-and-actor-critic/ddpg/index.md) for each agent's actor and critic.
- The discrete-action, value-based alternative is [QMIX](../qmix/index.md), and the shared-parameter PPO alternative is [MAPPO](../mappo/index.md).

## Applications

- **Cooperative simulated tasks.** Navigation and communication tasks, which the paper uses to test coordination.
- **Mixed settings.** Predator–prey and keep-away tasks, where teams and adversaries learn at the same time.

## Open questions

- How to scale centralised critics to large numbers of agents.
- How to infer the policies of other agents reliably when they cannot be observed.

## References

### Seminal papers

- Lowe et al. (2017), "Multi-agent actor-critic for mixed cooperative-competitive environments", [arXiv:1706.02275](https://arxiv.org/abs/1706.02275) — The MADDPG paper, with the centralised critic, the ensemble extension and the results above.
- Lillicrap et al. (2016), "Continuous control with deep reinforcement learning", ICLR, [arXiv:1509.02971](https://arxiv.org/abs/1509.02971) — DDPG, the single-agent method that each MADDPG agent uses.
- Rashid et al. (2018), "QMIX: Monotonic value function factorisation for deep multi-agent reinforcement learning", *Proceedings of ICML 2018*, PMLR 80, [arXiv:1803.11485](https://arxiv.org/abs/1803.11485) — A value-based alternative for cooperative teams.
- Yu et al. (2022), "The surprising effectiveness of PPO in cooperative multi-agent games", NeurIPS 2022 Datasets and Benchmarks Track, [arXiv:2103.01955](https://arxiv.org/abs/2103.01955) — A strong on-policy baseline with a centralised value function.
- Busoniu, Babuska & De Schutter (2008), "A comprehensive survey of multiagent reinforcement learning", *IEEE Transactions on Systems, Man, and Cybernetics, Part C* 38(2), 156–172. https://doi.org/10.1109/tsmcc.2007.913919 — Survey of multi-agent learning settings and their difficulties.
