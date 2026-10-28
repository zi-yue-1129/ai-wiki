---
status: complete
last_reviewed: 2026-10-28
aliases:
  - DDPG
  - 深度確定性策略梯度
---

# Deep deterministic policy gradient (Lillicrap et al., 2016)

An off-policy actor-critic method for continuous actions that trains a deterministic actor with a deep Q-function critic, using DQN-style replay and slowly updated target networks.

## Problem

DQN takes a maximum over a discrete set of actions, which is not available when actions are continuous. Policy gradients handle continuous actions but need many on-policy samples. Lillicrap et al. ask whether the ideas that let DQN learn from raw pixels can be combined with a deterministic policy gradient for continuous control.

## Core idea

The actor \(\mu(s \mid \theta^\mu)\) outputs an action directly, with no sampling. The critic \(Q(s, a \mid \theta^Q)\) estimates the value of state–action pairs. The actor is trained by following the gradient of the critic with respect to the action, which is the deterministic policy gradient. The critic is trained with a temporal-difference target computed by a target actor and a target critic, and both target networks follow the learned networks with a small soft update. Transitions are stored in a replay buffer and sampled in minibatches, as in DQN.

## Equation or algorithm

The actor update, with the deterministic policy gradient, is

\[
\nabla_{\theta^\mu} J \approx \mathbb{E}_{s}\left[\nabla_a Q(s, a \mid \theta^Q)\big|_{a = \mu(s)}\, \nabla_{\theta^\mu} \mu(s \mid \theta^\mu)\right]
\]

The critic minimises the squared loss \(L = \frac{1}{N}\sum_i (y_i - Q(s_i, a_i \mid \theta^Q))^2\), where

\[
y_i = r_i + \gamma\, Q'\big(s_{i+1}, \mu'(s_{i+1} \mid \theta^{\mu'}) \mid \theta^{Q'}\big)
\]

and the target networks are updated as \(\theta' \leftarrow \tau\theta + (1 - \tau)\theta'\), with \(\tau = 0.001\) in the paper. The replay buffer holds \(10^6\) transitions, and the minibatch size is 64 for low-dimensional states and 16 when learning from pixels. The discount is \(\gamma = 0.99\).

## Results

The abstract reports that the algorithm "robustly solves more than 20 simulated physics tasks" with one learning algorithm, one architecture and one set of hyperparameters. The paper also reports that for many of the tasks the method can learn policies end-to-end, directly from raw pixel inputs.

## Limitations

- **Critic overestimation.** The critic uses a single Q-function, which can overestimate values in the way that DQN does. [TD3](../td3/index.md) addresses this directly.
- **Brittle training.** Learning depends on the target-network rate, the replay design and the exploration noise added to actions, and the method is sensitive to these settings.
- **Deterministic policy.** The actor outputs one action per state, so exploration must be added externally, and the policy does not represent uncertainty by itself. [SAC](../sac/index.md) uses a stochastic actor instead.

## Connections

- Parent topic: [Policy gradient and actor-critic](../index.md), and the wider [Reinforcement Learning](../../index.md) overview.
- DDPG is the continuous-action analogue of [Deep Q-networks](../../deep-q-networks/index.md), using the same replay and target-network ideas.
- Its successors are [TD3](../td3/index.md), which fixes its overestimation, and [SAC](../sac/index.md), which uses a stochastic actor with entropy regularisation.

## Applications

- **Simulated robot control.** The paper's physics tasks are simulated robot and locomotion problems, the standard setting for continuous-control methods.
- **Learning from pixels.** The reported end-to-end results from raw images show the method outside state-based control.

## Open questions

- How to make deterministic actor–critic methods stable without careful hand-tuning of noise and target rates.
- How to represent uncertainty in continuous control when the actor is deterministic.

## References

### Seminal papers

- Lillicrap et al. (2016), "Continuous control with deep reinforcement learning", ICLR, [arXiv:1509.02971](https://arxiv.org/abs/1509.02971) — The DDPG paper, with the deterministic actor, the target networks and the physics results above.
- Mnih et al. (2015), "Human-level control through deep reinforcement learning", *Nature* 518, 529–533. https://doi.org/10.1038/nature14236 — The replay and target-network design that DDPG adapts to continuous actions.
- Silver et al. (2014), "Deterministic policy gradient algorithms", *Proceedings of ICML 2014*, PMLR 32, 387–395. https://proceedings.mlr.press/v32/silver14.html — The deterministic policy gradient theorem on which DDPG's actor update rests.
- Fujimoto, van Hoof & Meger (2018), "Addressing function approximation error in actor-critic methods", [arXiv:1802.09477](https://arxiv.org/abs/1802.09477) — TD3, a later method that corrects DDPG's overestimation.
- Haarnoja et al. (2018), "Soft actor-critic: Off-policy maximum entropy deep reinforcement learning with a stochastic actor", [arXiv:1801.01290](https://arxiv.org/abs/1801.01290) — A stochastic successor to DDPG for continuous control.

### Surveys and textbooks

- Sutton, R. S. & Barto, A. G. *Reinforcement Learning: An Introduction*, 2nd ed. MIT Press, 2018. http://incompleteideas.net/book/the-book-2nd.html — Background on policy gradients and actor-critic methods.
