---
status: draft
last_reviewed: 2026-10-28
aliases:
  - SAC
  - 軟演員–評論家
---

# Soft actor-critic (Haarnoja et al., 2018)

An off-policy actor-critic method for continuous control that maximises reward plus policy entropy, using a stochastic actor and two Q-functions.

## Problem

Off-policy deterministic methods such as DDPG are brittle, and on-policy methods such as PPO need many samples. Haarnoja et al. ask whether an off-policy actor-critic can be stable and sample-efficient, and whether maximising entropy alongside reward makes exploration and robustness easier.

## Core idea

The objective adds the policy's entropy to the expected reward at each step, with a temperature \(\alpha\) that sets the trade-off. The resulting soft value function \(V(s) = \mathbb{E}_{a}[Q(s,a) - \log \pi(a \mid s)]\) pushes the policy to stay as random as the reward allows. The actor is stochastic and is trained through the reparameterisation trick, which makes its sampled actions differentiable. Two Q-functions are trained and their minimum is used for the value and policy gradients, which limits overestimation, as in TD3.

## Equation or algorithm

The maximum-entropy objective is

\[
J(\pi) = \sum_t \mathbb{E}\left[r(s_t, a_t) + \alpha\, \mathcal{H}\big(\pi(\cdot \mid s_t)\big)\right]
\]

The soft Q target is \(\hat{Q}(s_t, a_t) = r(s_t, a_t) + \gamma\, \mathbb{E}\big[V_{\bar{\psi}}(s_{t+1})\big]\), where \(\bar{\psi}\) are the target value-network weights. The policy is updated by minimising a KL divergence, which with the reparameterised action \(a_t = f_\phi(\epsilon; s_t)\) becomes \(\mathbb{E}\big[\log \pi_\phi(f_\phi(\epsilon; s_t) \mid s_t) - Q_\theta(s_t, f_\phi(\epsilon; s_t))\big]\). The target value network is updated with a soft rate \(\tau\). The procedure:

1. Collect transitions with the stochastic policy and store them in a replay buffer.
2. Sample a minibatch, compute the soft Q target with the target value network, and update both Q-functions.
3. Update the value network and the policy using the minimum of the two Q-functions.
4. Update the target value network with rate \(\tau\), and repeat.

In the version studied by the paper, the temperature \(\alpha\) is fixed, and the reward scale is the one hyperparameter that needs tuning.

## Results

The paper reports that SAC "exceeds the performance of prior state-of-the-art off-policy deep RL methods by a wide margin" and shows "a substantial improvement in both performance and sample efficiency over both off-policy and on-policy prior methods". On the harder Gym MuJoCo tasks (Hopper, Walker2d, HalfCheetah, Ant and Humanoid), it outperforms DDPG, PPO, soft Q-learning and TD3 by a large margin, and DDPG fails to make progress on Ant and Humanoid. Results are averaged over five random seeds, and the authors report very similar performance across seeds.

## Limitations

- **Temperature sensitivity.** Performance depends on the reward scale, which sets the effective entropy weight in this version. Later work learns \(\alpha\) automatically; this paper does not include that step.
- **Two critics and a stochastic actor.** The method has more networks than DDPG, which adds computation per update.
- **Continuous actions.** The method is designed for continuous control, and the paper's results are on simulated locomotion tasks.

## Connections

- Parent topic: [Policy gradient and actor-critic](../index.md), and the wider [Reinforcement Learning](../../index.md) overview.
- Its deterministic predecessor is [DDPG](../ddpg/index.md), and its overestimation fix shares ideas with [TD3](../td3/index.md).
- It is an off-policy method, in contrast with the on-policy [PPO](../../proximal-policy-optimisation/index.md).

## Applications

- **Simulated robot locomotion.** The MuJoCo tasks in the paper are the reported applications, and the method is a standard baseline for continuous control.

## Open questions

- How to tune or learn the temperature automatically across tasks with different reward scales.
- How the method behaves on real robots, where the paper does not test.

## References

### Seminal papers

- Haarnoja, Zhou, Abbeel & Levine (2018), "Soft actor-critic: Off-policy maximum entropy deep reinforcement learning with a stochastic actor", [arXiv:1801.01290](https://arxiv.org/abs/1801.01290) — The SAC paper, with the maximum-entropy objective and the MuJoCo results above.
- Fujimoto, van Hoof & Meger (2018), "Addressing function approximation error in actor-critic methods", [arXiv:1802.09477](https://arxiv.org/abs/1802.09477) — TD3, which uses the same two-critic minimum against overestimation.
- Lillicrap et al. (2016), "Continuous control with deep reinforcement learning", ICLR, [arXiv:1509.02971](https://arxiv.org/abs/1509.02971) — DDPG, the deterministic off-policy baseline that SAC outperforms.
- Schulman et al. (2017), "Proximal policy optimization algorithms", [arXiv:1707.06347](https://arxiv.org/abs/1707.06347) — The on-policy baseline in the SAC comparison.

### Surveys and textbooks

- Sutton, R. S. & Barto, A. G. *Reinforcement Learning: An Introduction*, 2nd ed. MIT Press, 2018. http://incompleteideas.net/book/the-book-2nd.html — Background on actor-critic methods and the value functions used by SAC.
