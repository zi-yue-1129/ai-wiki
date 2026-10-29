---
status: complete
last_reviewed: 2026-10-28
aliases:
  - TD3
  - 雙延遲深度確定性策略梯度
---

# Twin delayed deep deterministic policy gradient (Fujimoto et al., 2018)

A DDPG variant that fixes overestimation in the critic with two Q-functions, updates the actor less often than the critics, and smooths the target action with noise.

## Problem

Fujimoto, van Hoof and Meger show that DDPG's critic overestimates action values, and that the errors in the actor's policy updates compound, because the actor follows the critic's current, inaccurate estimates. Their question is how to reduce this function-approximation error in actor-critic methods without giving up the deterministic actor of DDPG.

## Core idea

TD3 changes DDPG in three ways:

1. **Clipped double Q-learning.** Two critics are trained, and the target uses the smaller of their two estimates, which limits overestimation.
2. **Delayed policy updates.** The actor and the target networks are updated less often than the critics, here once for every two critic updates, so the policy chases a more accurate value.
3. **Target policy smoothing.** Clipped noise is added to the target action, so that the value target is averaged over a small region of actions and cannot exploit a sharp peak in the critic.

## Equation or algorithm

The TD3 target is

\[
y = r + \gamma \min_{i=1,2} Q_{\theta'_i}\big(s', \pi_{\phi'}(s') + \epsilon\big), \qquad \epsilon \sim \text{clip}\big(\mathcal{N}(0, \sigma), -c, c\big)
\]

The paper uses policy delay \(d = 2\), target-noise standard deviation \(\sigma = 0.2\), noise clip \(c = 0.5\), and a soft target-update rate of \(\tau = 0.005\). The procedure for each step:

1. Sample a minibatch from the replay buffer.
2. Compute the smoothed target action from the target actor, and form the clipped double-Q target \(y\).
3. Update both critics towards \(y\).
4. Every \(d\) steps, update the actor with the gradient through the first critic, then update the target networks.

![Four-stage TD3 process: smoothed target action, clipped twin target Q values, critic updates each step, and delayed actor and target updates](../../../../../assets/concept-animations/td3-delayed-twin-critics-motion.svg)

*Original animated teaching schematic (CC BY-SA 4.0).* The upper path adds clipped noise to the **target actor's action**, evaluates it with **both target critics**, and uses their **minimum** to form the bootstrap target. The lower path distinguishes **both online critics updating every step** from **the actor and target networks updating only every second critic step** (the paper's example delay (d=2)). The target networks receive a **soft update**, not a hard copy; the actor's policy gradient uses the first online critic. The timeline is **illustrative, not measured training dynamics**. Use the MkDocs Play/Pause control, or view the [GitHub-readable static overview](../../../../../assets/concept-animations/td3-delayed-twin-critics-still.svg). See [Fujimoto et al. (2018)](https://arxiv.org/abs/1802.09477).

## Results

The paper evaluates on seven OpenAI Gym MuJoCo tasks, with results averaged over 10 trials of one million time steps. The abstract states that the method outperforms the state of the art in every environment tested. Table 1 gives maximum average return for TD3, DDPG and PPO:

| Environment | TD3 | DDPG | PPO |
|---|---|---|---|
| HalfCheetah | 9636.95 | 3305.60 | 1795.43 |
| Hopper | 3564.07 | 2020.46 | 2164.70 |
| Walker2d | 4682.82 | 1843.85 | 3317.69 |
| Ant | 4372.44 | 1005.30 | 1083.20 |
| Reacher | −3.60 | −6.51 | −6.18 |
| InvertedPendulum | 1000.00 | 1000.00 | 1000.00 |
| InvertedDoublePendulum | 9337.47 | 9355.52 | 8977.94 |

The table is the paper's own. On InvertedDoublePendulum, DDPG's value is slightly higher than TD3's, so the "every environment" claim does not hold on that one task.

## Limitations

- **Evaluation scope.** The main results are on continuous MuJoCo control, with a fixed set of seven tasks, and the paper does not test discrete actions or pixel inputs.
- **Deterministic exploration.** The actor is deterministic, so exploration depends on the noise added to actions, as in DDPG.
- **Extra hyperparameters.** The policy delay, target noise and noise clip are new settings that the paper chooses, and the results depend on them.

## Connections

- Parent topic: [Policy gradient and actor-critic](../index.md), and the wider [Reinforcement Learning](../../index.md) overview.
- TD3 builds on [DDPG](../ddpg/index.md), and its double-Q idea echoes the [Double DQN](../../value-based-methods/double-dqn/index.md) fix for overestimation in discrete actions.
- The stochastic alternative that also handles overestimation is [SAC](../sac/index.md).

## Applications

- **Simulated locomotion.** The MuJoCo benchmark tasks, such as Hopper, Walker2d and Ant, are the paper's main applications.

## Open questions

- Whether the three fixes remain the right ones for stochastic or very high-dimensional actions.
- How the stability gains transfer from simulated locomotion to real robots.

## References

### Seminal papers

- Fujimoto, van Hoof & Meger (2018), "Addressing function approximation error in actor-critic methods", *Proceedings of ICML 2018*, [arXiv:1802.09477](https://arxiv.org/abs/1802.09477) — The TD3 paper, with the three changes and the MuJoCo comparison above.
- Lillicrap et al. (2016), "Continuous control with deep reinforcement learning", ICLR, [arXiv:1509.02971](https://arxiv.org/abs/1509.02971) — DDPG, the deterministic method that TD3 modifies.
- Haarnoja et al. (2018), "Soft actor-critic: Off-policy maximum entropy deep reinforcement learning with a stochastic actor", [arXiv:1801.01290](https://arxiv.org/abs/1801.01290) — A stochastic actor-critic method that is compared against the same family.
- Schulman et al. (2017), "Proximal policy optimization algorithms", [arXiv:1707.06347](https://arxiv.org/abs/1707.06347) — The on-policy baseline in the TD3 MuJoCo comparison.
- van Hasselt, Guez & Silver (2015), "Deep reinforcement learning with double Q-learning", [arXiv:1509.06461](https://arxiv.org/abs/1509.06461) — Double Q-learning with function approximation, the estimator that clipped double Q-learning builds on.

### Surveys and textbooks

- Sutton, R. S. & Barto, A. G. *Reinforcement Learning: An Introduction*, 2nd ed. MIT Press, 2018. http://incompleteideas.net/book/the-book-2nd.html — Background on actor-critic methods and overestimation in value learning.
