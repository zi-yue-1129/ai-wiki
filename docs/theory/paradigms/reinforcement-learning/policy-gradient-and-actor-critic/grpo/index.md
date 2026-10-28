---
status: draft
last_reviewed: 2026-10-28
aliases:
  - GRPO
  - 群組相對策略最佳化
---

# Group relative policy optimisation (Shao et al., 2024)

A PPO-style policy-gradient method for language models that drops the learned critic and computes advantages by normalising rewards within a group of sampled answers to the same question.

## Problem

PPO for language models needs a separate value model, which adds memory and compute cost to training. Shao et al. introduce GRPO in the DeepSeekMath work, asking whether the baseline can come from the rewards of several sampled outputs for the same prompt, with no critic.

## Core idea

For each question \(q\), the policy samples a group of \(G\) outputs \(\{o_i\}\). Each output receives a reward \(r_i\). The advantage is the reward normalised within the group, \(\hat{A}_i = (r_i - \text{mean}(\mathbf{r})) / \text{std}(\mathbf{r})\), and the same value is applied to every token of that output. The mean of the group serves as the baseline that a critic would otherwise learn. The update keeps the clipped probability ratio of PPO and adds a KL penalty to a reference policy, so that the policy does not drift too far.

## Equation or algorithm

The GRPO objective averages, over the group and the tokens of each output, the minimum of the clipped and unclipped ratio terms weighted by the normalised advantage, minus \(\beta\) times a KL divergence to a reference policy. The KL term is added directly to the loss, not to the reward. The paper uses an unbiased estimator of the KL divergence and a coefficient \(\beta = 0.04\) in its DeepSeekMath-RL setup, with 64 sampled outputs per question. The procedure:

1. For each question in a batch, sample \(G\) outputs from the old policy.
2. Score each output with a reward, such as the correctness of a final answer.
3. Normalise the rewards within the group to obtain advantages \(\hat{A}_i\).
4. Update the policy with the clipped objective and the KL penalty, for one or more gradient steps.
5. Set the old policy to the updated policy and repeat.

The paper also describes an outcome-supervision and a process-supervision version. The outcome version assigns one reward per output, as above.

## Results

The paper reports results for a 7B model trained with GRPO, DeepSeekMath-RL, against its instruction-tuned starting point, DeepSeekMath-Instruct 7B, using chain-of-thought prompting:

- **GSM8K:** 82.9% for the instruct model, 88.2% after GRPO.
- **MATH:** 46.8% for the instruct model, 51.7% after GRPO.

These are gains from one training run on mathematical reasoning, not a general comparison across tasks.

## Limitations

- **Depends on the reward.** The advantages are only as good as the reward signal, and for language tasks the reward is often a verifiable answer or a learned model.
- **Group sampling costs.** Sampling 64 outputs per question costs generation time, even though the critic is removed.
- **Narrow evidence.** The reported gains come from mathematical reasoning benchmarks in one model family, and the paper does not establish the method for open-ended tasks.

## Connections

- Parent topic: [Policy gradient and actor-critic](../index.md), and the wider [Reinforcement Learning](../../index.md) overview.
- GRPO is a critic-free variant of [PPO](../../proximal-policy-optimisation/index.md), keeping its clipped objective.
- It inherits the REINFORCE idea of weighting log-probabilities by a return, which is covered on the [REINFORCE](../reinforce/index.md) page.
- Its training signal is related to the human-feedback reward models on the [learning from human feedback](../../learning-from-human-feedback/index.md) page.

## Applications

- **Mathematical reasoning.** The DeepSeekMath-RL model trained with GRPO improves on GSM8K and MATH (Shao et al., 2024).
- **Aligning language models.** The same policy-gradient family is used for preference-based fine-tuning, as in InstructGPT (Ouyang et al., 2022).

## Open questions

- Whether group-normalised advantages hold up when the group rewards are noisy or the answers are open-ended.
- How to choose the group size, which trades compute for variance reduction.

## References

### Seminal papers

- Shao et al. (2024), "DeepSeekMath: Pushing the limits of mathematical reasoning in open language models", [arXiv:2402.03300](https://arxiv.org/abs/2402.03300) — Introduces GRPO, the group-relative baseline, and the GSM8K and MATH results above.
- Schulman et al. (2017), "Proximal policy optimization algorithms", [arXiv:1707.06347](https://arxiv.org/abs/1707.06347) — The clipped objective that GRPO keeps.
- Schulman et al. (2015), "Trust region policy optimization", *Proceedings of ICML 2015*, [arXiv:1502.05477](https://arxiv.org/abs/1502.05477) — The trust-region idea behind the constraint on policy change.
- Ouyang et al. (2022), "Training language models to follow instructions with human feedback", [arXiv:2203.02155](https://arxiv.org/abs/2203.02155) — Policy-gradient fine-tuning of language models with a learned reward model.
- Mnih et al. (2016), "Asynchronous methods for deep reinforcement learning", [arXiv:1602.01783](https://arxiv.org/abs/1602.01783) — Advantage-based actor-critic updates, the family GRPO modifies.

### Surveys and textbooks

- Sutton, R. S. & Barto, A. G. *Reinforcement Learning: An Introduction*, 2nd ed. MIT Press, 2018. http://incompleteideas.net/book/the-book-2nd.html — Background on policy gradients and baselines.
