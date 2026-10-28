---
status: draft
last_reviewed: 2026-10-28
aliases:
  - REINFORCE
  - 策略梯度 REINFORCE
---

# REINFORCE (Williams, 1992)

A Monte Carlo policy-gradient method that raises the log-probability of each sampled action in proportion to the return that followed it.

## Problem

A stochastic policy should be adjusted directly to increase the expected reinforcement it receives, without a model of the environment or a value function. Williams asks which update rule gives this for networks with stochastic output units, and whether it moves the parameters in the direction of the gradient of expected reinforcement.

## Core idea

For a stochastic unit with weight \(w_{ij}\), Williams defines the update \(\Delta w_{ij} = \alpha_{ij}\,(r - b_{ij})\,e_{ij}\). Here \(r\) is the reinforcement, \(b_{ij}\) is a baseline, and \(e_{ij}\) is the eligibility term, which is the derivative of the log-probability of the sampled output with respect to that weight. The paper's Theorem 1 states that the average update vector lies in a direction in which expected reinforcement increases. The baseline does not change that direction, but the paper notes that the choice of baseline affects which local maxima the algorithm may reach.

## Equation or algorithm

In the notation used across this wiki, REINFORCE estimates the gradient of the expected return \(J(\theta)\) from sampled episodes:

\[
\nabla_\theta J(\theta) \approx \sum_t \nabla_\theta \log \pi_\theta(a_t \mid s_t)\,\big(G_t - b\big)
\]

where \(G_t\) is the return from step \(t\) and \(b\) is a baseline. The procedure:

1. Initialise the policy parameters \(\theta\).
2. Sample a complete episode by following \(\pi_\theta\).
3. For each step \(t\), compute the return \(G_t\).
4. Update \(\theta \leftarrow \theta + \alpha \sum_t \nabla_\theta \log \pi_\theta(a_t \mid s_t)\,(G_t - b)\).
5. Repeat from step 2.

## Results

Williams's paper gives a derivation and a theorem rather than a benchmark. Its contribution is the general class of update rules, which underlies the policy-gradient methods that followed.

## Limitations

- **High variance.** Using the full return as the weight gives an unbiased but noisy gradient. Baselines and critics, the basis of [actor-critic methods](../a3c/index.md), reduce the variance.
- **On-policy and episodic.** Each episode is used for one update, which makes the method sample-hungry.
- **Local maxima.** The paper notes that the baseline affects the local maxima the algorithm can reach, and the theorem only guarantees movement along the gradient.

## Connections

- Parent topic: [Policy gradient and actor-critic](../index.md), and the wider [Reinforcement Learning](../../index.md) overview.
- Its advantage-weighted form is the starting point for [A3C](../a3c/index.md), [TRPO](../trpo/index.md) and [Proximal Policy Optimisation](../../proximal-policy-optimisation/index.md).
- [GRPO](../grpo/index.md) keeps the REINFORCE-style update but takes its baseline from the mean reward of a group of sampled outputs.

## Applications

- **Language model fine-tuning.** Policy-gradient updates with a sampled-reward baseline underlie the reinforcement learning used to align language models (Ouyang et al., 2022; Shao et al., 2024).

## Open questions

- Which baselines give low variance without bias in long-horizon tasks.
- How to keep the simplicity of REINFORCE while reusing data, which the later methods pursue.

## References

### Seminal papers

- Williams (1992), "Simple statistical gradient-following algorithms for connectionist reinforcement learning", *Machine Learning* 8(3–4), 229–256. https://doi.org/10.1007/bf00992696 — The paper that introduces the REINFORCE update and proves the gradient-direction theorem.
- Schulman et al. (2016), "High-dimensional continuous control using generalized advantage estimation", [arXiv:1506.02438](https://arxiv.org/abs/1506.02438) — Advantage estimation for reducing the variance of policy-gradient updates.
- Mnih et al. (2016), "Asynchronous methods for deep reinforcement learning", [arXiv:1602.01783](https://arxiv.org/abs/1602.01783) — Actor-critic policy gradients with an advantage baseline.
- Schulman et al. (2017), "Proximal policy optimization algorithms", [arXiv:1707.06347](https://arxiv.org/abs/1707.06347) — A clipped policy-gradient method built on the same log-probability gradient.

### Surveys and textbooks

- Sutton, R. S. & Barto, A. G. *Reinforcement Learning: An Introduction*, 2nd ed. MIT Press, 2018. http://incompleteideas.net/book/the-book-2nd.html — Policy-gradient methods and the role of baselines in the standard textbook.

### Articles and documentation

- Ouyang et al. (2022), "Training language models to follow instructions with human feedback", [arXiv:2203.02155](https://arxiv.org/abs/2203.02155) — InstructGPT, which fine-tunes a language model with reinforcement learning from human feedback.
- Shao et al. (2024), "DeepSeekMath: Pushing the limits of mathematical reasoning in open language models", [arXiv:2402.03300](https://arxiv.org/abs/2402.03300) — Introduces GRPO, which uses a group-mean baseline in place of a learned critic.
