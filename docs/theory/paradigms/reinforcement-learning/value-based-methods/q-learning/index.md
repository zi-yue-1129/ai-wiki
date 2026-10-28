---
status: draft
last_reviewed: 2026-10-28
aliases:
  - Q-learning
  - Q 學習
---

# Q-learning (Watkins & Dayan, 1992)

An off-policy temporal-difference method that learns the optimal action values from sampled transitions, without a model of the environment.

## Problem

An agent that does not know the transition probabilities needs to learn which action is best in each state from experience alone. Dynamic programming needs the model, and Monte Carlo methods must wait for complete episodes. The problem is to learn optimal action values from sampled experience, updating after every step.

## Core idea

Keep a table \(Q(x, a)\) of action values. After each step, with state \(x\), action \(a\), reward \(r\) and next state \(y\), move \(Q(x, a)\) toward \(r + \gamma \max_b Q(y, b)\). The target takes the greedy maximum at the next state, whatever action the agent actually takes next. The learned values therefore describe the optimal policy even while the agent explores with a different policy.

## Equation or algorithm

Watkins and Dayan write the update with a learning factor \(\alpha_n\) that depends on the number of visits to the pair:

\[
Q_n(x,a) = (1 - \alpha_n)\, Q_{n-1}(x,a) + \alpha_n \left[ r_n + \gamma \max_b Q_{n-1}(y_n, b) \right]
\]

for the pair \((x, a)\) visited at step \(n\), and no change for other pairs. The procedure:

1. Initialise \(Q(s, a)\) for all pairs.
2. Start an episode in state \(s\).
3. Choose \(a\) from \(s\) with an exploration rule, such as ε-greedy on \(Q\).
4. Take \(a\), observe \(r\) and the next state \(s'\).
5. Update \(Q(s, a) \leftarrow Q(s, a) + \alpha \left[ r + \gamma \max_{b} Q(s', b) - Q(s, a) \right]\).
6. Set \(s \leftarrow s'\) and repeat until the episode ends.

**Convergence.** Watkins and Dayan show that \(Q_n\) converges to \(Q^*\) with probability one, provided every state–action pair is visited infinitely often, rewards are bounded, \(0 \le \alpha_n < 1\) with \(\sum_n \alpha_n = \infty\) and \(\sum_n \alpha_n^2 < \infty\) for each pair, and \(0 < \gamma < 1\). Tsitsiklis (1994) proves the same convergence through asynchronous stochastic approximation.

## Results

Watkins and Dayan's contribution is a convergence theorem, not an empirical benchmark. Its practical reach came through function approximation. Deep Q-networks use the same max-target with a neural network, and reach human-level play on many Atari games (Mnih et al., 2015).

## Limitations

- **Tabular form.** A table entry for each state–action pair is impractical for large or continuous spaces.
- **Maximisation bias.** The max over noisy estimates tends to overestimate values. The Double DQN paper reports overestimation for DQN in all 49 tested Atari games (van Hasselt et al., 2016).
- **Convergence conditions.** The guarantee needs infinite visits to every pair and a learning-rate schedule. Both assumptions can fail in practice, and with function approximation the guarantee no longer holds.

## Connections

- Parent topic: [Value-based methods](../index.md), and the wider [Reinforcement Learning](../../index.md) overview.
- The deep version is [Deep Q-networks](../../deep-q-networks/index.md). The fix for overestimation is [Double DQN](../double-dqn/index.md).
- The on-policy counterpart is [SARSA](../sarsa/index.md), which learns the values of the policy being followed.
- The temporal-difference error used in the update is the signal discussed on the parent page for its link to dopamine.

## Applications

- **Teaching and small discrete problems**, such as grid worlds, where the table is small enough to store. Gridworlds are common teaching examples for tabular methods (Sutton & Barto, 2018).

## Open questions

- Stable off-policy learning with function approximation, where the convergence guarantee does not carry over.
- Reliable value estimates under noise, without the overestimation bias.

## References

### Seminal papers

- Watkins & Dayan (1992), "Q-learning", *Machine Learning* 8(3–4), 279–292. https://doi.org/10.1007/bf00992698 — The paper that defines Q-learning and proves its convergence to optimal action values.
- Tsitsiklis (1994), "Asynchronous stochastic approximation and Q-learning", *Machine Learning* 16(3), 185–202. https://doi.org/10.1007/bf00993306 — Proves convergence of Q-learning through asynchronous stochastic approximation.
- Mnih et al. (2015), "Human-level control through deep reinforcement learning", *Nature* 518, 529–533. https://doi.org/10.1038/nature14236 — The deep version of Q-learning, with replay and a target network.
- van Hasselt, Guez & Silver (2016), "Deep reinforcement learning with double Q-learning", [arXiv:1509.06461](https://arxiv.org/abs/1509.06461) — Shows that DQN overestimates action values and reduces the bias.
- Mnih et al. (2013), "Playing Atari with deep reinforcement learning", [arXiv:1312.5602](https://arxiv.org/abs/1312.5602) — Early preprint that applied a Q-learning-based network to raw Atari frames.

### Surveys and textbooks

- Sutton, R. S. & Barto, A. G. *Reinforcement Learning: An Introduction*, 2nd ed. MIT Press, 2018. http://incompleteideas.net/book/the-book-2nd.html — Covers tabular Q-learning in its temporal-difference chapter, with the convergence context.
