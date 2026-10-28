---
status: draft
last_reviewed: 2026-10-28
aliases:
  - IQL
  - Implicit Q-learning
---

# Implicit Q-learning (Kostrikov et al., 2021)

An offline reinforcement learning method that never evaluates the value of an action outside the dataset. It estimates the value of the best in-dataset actions with an expectile regression, and then extracts a policy by weighted behaviour cloning.

## Problem

Offline methods must improve on the behaviour that produced the data, but they cannot check unseen actions in the environment. Most offline methods therefore either constrain the policy to the data or regularise the values of unseen actions. Kostrikov et al. ask whether a policy can improve over the best behaviour in the data while never querying the value of an action that the data does not contain.

## Core idea

IQL learns three functions: a Q-function, a state-value function \(V\), and a policy. The key step is the value update. Instead of taking the maximum over actions, which requires querying unseen actions, IQL fits \(V\) to an upper expectile of the Q-values of the actions in the dataset. The expectile puts more weight on the best in-data actions, so \(V\) approximates the value of the best actions the data supports. The Q-function is then trained against this \(V\), and the policy is extracted by advantage-weighted behaviour cloning, which favours dataset actions with high advantage.

The method thus improves over the behaviour through generalisation, rather than by querying out-of-distribution actions.

## Equation or algorithm

The value function is fitted by asymmetric least squares, with an expectile \(\tau\) close to one:

\[
L_V(\psi) = \mathbb{E}_{(s,a) \sim \mathcal{D}}\left[ L_2^\tau\big(Q_{\hat\theta}(s,a) - V_\psi(s)\big) \right], \qquad L_2^\tau(u) = |\tau - \mathbb{1}(u < 0)|\, u^2 .
\]

The Q-function is trained with the Bellman target \(r + \gamma V_\psi(s')\), which uses only dataset actions. The policy is then fitted by weighted behaviour cloning, with weights \(\exp(\beta(Q(s,a) - V(s)))\) on dataset transitions.

## Results

The paper reports results on the offline benchmarks of D4RL, including the AntMaze tasks, where several baselines score poorly. Its comparison table includes behaviour cloning, Decision Transformer, AWAC, TD3+BC and conservative Q-learning. The abstract states that the method "never needs to evaluate actions outside of the dataset, but still enables the learned policy to improve substantially over the best behavior in the data through generalization".

## Limitations

- **Expectile and temperature.** Results depend on the expectile \(\tau\) and the advantage temperature \(\beta\), which must be tuned.
- **Dataset quality.** The improvement is bounded by what generalises from the dataset, so the method cannot create good actions the data never contains.
- **Policy extraction.** The weighted behaviour cloning step is only as good as the advantage estimates it uses.

## Connections

- Parent topic: [Offline RL](../index.md).
- Its value update is an alternative to the pessimistic penalty of [CQL](../cql/index.md).
- The policy extraction is advantage-weighted behavioural cloning, a close relative of advantage-weighted regression.
- [Decision Transformer](../decision-transformer/index.md) reaches a related goal, learning from the dataset's returns without value learning.

## Applications

- **Navigation** from logged data, such as the AntMaze tasks in the paper.
- **Learning from demonstrations** when the demonstrations include some suboptimal behaviour.

## Open questions

- How to set the expectile and temperature without online tuning.
- How to extend the method to settings where the dataset is very narrow.

## References

### Seminal papers

- Kostrikov, Nair & Levine (2021), "Offline reinforcement learning with implicit Q-learning", [arXiv:2110.06169](https://arxiv.org/abs/2110.06169) — The IQL paper, with the expectile value update, the advantage-weighted policy extraction and the D4RL results.
- Kumar, Zhou, Tucker & Levine (2020), "Conservative Q-learning for offline reinforcement learning", [arXiv:2006.04779](https://arxiv.org/abs/2006.04779) — The main pessimistic alternative to IQL, for comparison.
- Fujimoto, Meger & Precup (2019), "Off-policy deep reinforcement learning without exploration", [arXiv:1812.02900](https://arxiv.org/abs/1812.02900) — Batch-constrained Q-learning, an offline method that constrains the policy to the data.
- Fu, Kumar, Nachum, Tucker & Levine (2020), "D4RL: Datasets for deep data-driven reinforcement learning", [arXiv:2004.07219](https://arxiv.org/abs/2004.07219) — The offline benchmark suite on which IQL is evaluated.
- Chen et al. (2021), "Decision Transformer: Reinforcement learning via sequence modeling", [arXiv:2106.01345](https://arxiv.org/abs/2106.01345) — An offline method that learns from returns with sequence modelling, for comparison.
