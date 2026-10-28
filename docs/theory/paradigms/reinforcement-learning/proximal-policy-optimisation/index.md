---
status: draft
last_reviewed: 2026-10-28
aliases:
  - PPO
  - 近端策略最佳化
---

# Proximal policy optimisation (Schulman et al., 2017)

A policy-gradient method that clips the probability ratio between the new and old policies, so each update stays near the old policy.

## Problem

A plain policy-gradient step can be too large, and performance can collapse after a single bad update. Trust-region methods such as TRPO control the step size with a constraint on the average KL divergence between the old and new policies. TRPO is stable, but the constrained optimisation is complicated to implement, and PPO aims for a simpler method with similar reliability.

## Core idea

Let \(r_t(\theta) = \pi_\theta(a_t \mid s_t) / \pi_{\theta_{\text{old}}}(a_t \mid s_t)\) be the probability ratio. The clipped objective keeps \(r_t\) inside \([1-\varepsilon, 1+\varepsilon]\) wherever that would otherwise reward a large move. Taking the minimum of the clipped and unclipped terms means the objective gains nothing from pushing the ratio beyond the band. The paper uses \(\varepsilon = 0.2\) for continuous control. Because the update stays near the old policy, one batch of data can support several epochs of minibatch updates.

## Equation or algorithm

With advantage estimate \(\hat{A}_t\), the clipped surrogate is

\[
L^{\text{CLIP}}(\theta) = \mathbb{E}_t\left[\min\left(r_t(\theta)\hat{A}_t,\ \text{clip}\left(r_t(\theta), 1-\varepsilon, 1+\varepsilon\right)\hat{A}_t\right)\right]
\]

When the policy and value function share parameters, the paper combines the clipped surrogate with a value-function loss and an entropy bonus:

\[
L_t^{\text{CLIP+VF+S}}(\theta) = \mathbb{E}_t\left[L_t^{\text{CLIP}}(\theta) - c_1 L_t^{\text{VF}}(\theta) + c_2 S[\pi_\theta](s_t)\right]
\]

with \(L_t^{\text{VF}} = (V_\theta(s_t) - V_t^{\text{targ}})^2\). The Atari experiments use \(c_1 = 1\) and \(c_2 = 0.01\). The MuJoCo experiments use separate networks for the policy and the value function, so they have no value-loss coefficient and no entropy bonus.

The procedure, in the paper's form:

1. Run the current policy \(\pi_{\theta_{\text{old}}}\) for \(T\) timesteps and collect the trajectories. The Atari setup uses 8 parallel actors with \(T = 128\).
2. Estimate advantages \(\hat{A}_t\) with generalised advantage estimation, using \(\gamma = 0.99\) and \(\lambda = 0.95\) (Schulman et al., 2016).
3. Optimise the surrogate for several epochs over minibatches. The MuJoCo setup uses \(T = 2048\), 10 epochs and minibatches of 64. The Atari setup uses 3 epochs and minibatches of \(32 \times 8\).
4. Set \(\theta_{\text{old}} \leftarrow \theta\) and repeat.

## Results

- **Continuous control.** On seven MuJoCo tasks, the paper reports that PPO outperforms previous methods on almost all environments, with one million timesteps per run. An ablation over 21 runs compares clipping parameters with the normalised score: \(\varepsilon = 0.2\) scores 0.82, \(\varepsilon = 0.1\) scores 0.76, \(\varepsilon = 0.3\) scores 0.70, and no clipping or penalty scores −0.39.
- **Atari.** Across 49 games, PPO is reported to be significantly more sample-efficient than A2C and similar to ACER. Counting which method has the highest average reward over all of training, PPO wins on 30 games, ACER on 18, A2C on 1, with no ties.

## Limitations

- **Heuristic clipping.** Clipping keeps updates close to the old policy in practice, but it does not carry the monotonic-improvement guarantee of TRPO.
- **Implementation sensitivity.** Engstrom et al. (2020) found that code-level details, which the original description leaves out, account for most of PPO's reported advantage over TRPO. Results depend on the implementation.
- **On-policy data.** Each batch supports only a few updates before it must be discarded, which limits sample efficiency compared with replay-based methods.
- **Dated benchmarks.** The evidence comes from the 2017 MuJoCo and Atari setups, and it compares against the baselines available then.

## Connections

- Parent topic: [Reinforcement Learning](../index.md)
- Other method on this topic: [Deep Q-Networks](../deep-q-networks/index.md), which takes the value-based route.
- PPO is used to fine-tune large language models with human feedback. InstructGPT (Ouyang et al., 2022) fine-tunes a model using reinforcement learning from human feedback, covered on [Learning from human feedback](../learning-from-human-feedback/index.md).

## Applications

- **Simulated robot locomotion.** The MuJoCo experiments in the paper are the standard continuous-control benchmark for policy-gradient methods.
- **Language model alignment.** InstructGPT uses reinforcement learning from human feedback to fine-tune its models (Ouyang et al., 2022).

## Open questions

- Which parts of the clipped objective matter most, once implementation details are controlled.
- How PPO compares with newer off-policy methods on sample efficiency.
- Tuning: the clipping range, the number of epochs and the advantage estimator all interact, and good defaults may not transfer across tasks.

## References

### Seminal papers

- Schulman, Wolski, Dhariwal, Radford & Klimov (2017), "Proximal policy optimization algorithms", [arXiv:1707.06347](https://arxiv.org/abs/1707.06347) — The PPO paper, with the clipped objective and the experiments reported above.
- Schulman, Levine, Moritz, Jordan & Abbeel (2015), "Trust region policy optimization", *Proceedings of ICML 2015*, [arXiv:1502.05477](https://arxiv.org/abs/1502.05477) — TRPO, the constrained method that PPO simplifies.
- Schulman, Moritz, Levine, Jordan & Abbeel (2016), "High-dimensional continuous control using generalized advantage estimation", [arXiv:1506.02438](https://arxiv.org/abs/1506.02438) — GAE, the advantage estimator used in the PPO experiments.
- Mnih et al. (2016), "Asynchronous methods for deep reinforcement learning", [arXiv:1602.01783](https://arxiv.org/abs/1602.01783) — A3C, the parallel actor-critic family that the PPO paper's synchronous baseline A2C belongs to.
- Engstrom, Ilyas, Santurkar, Tsipras, Janoos, Rudolph & Madry (2020), "Implementation matters in deep policy gradients: a case study on PPO and TRPO", [arXiv:2005.12729](https://arxiv.org/abs/2005.12729) — Shows that code-level details account for most of PPO's gain over TRPO.

### Surveys and textbooks

- Sutton, R. S. & Barto, A. G. *Reinforcement Learning: An Introduction*, 2nd ed. MIT Press, 2018. http://incompleteideas.net/book/the-book-2nd.html — The standard RL textbook, with a free online draft covering policy-gradient methods.

### Articles and documentation

- Ouyang et al. (2022), "Training language models to follow instructions with human feedback", [arXiv:2203.02155](https://arxiv.org/abs/2203.02155) — InstructGPT, which fine-tunes a language model with reinforcement learning from human feedback.
