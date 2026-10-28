---
status: draft
last_reviewed: 2026-10-28
aliases:
  - DPO
  - 直接偏好最佳化
---

# Direct preference optimisation (Rafailov et al., 2023)

Fits a language model to preference pairs with a classification loss, so that no separate reward model and no reinforcement learning loop is needed.

## Problem

Reinforcement learning from human feedback first trains a reward model on comparisons and then runs a policy-gradient method against it. This is more complicated to implement and tune than fitting a model directly to the comparisons. Rafailov et al. ask whether the KL-constrained reward-maximisation objective can be solved directly on preference data.

## Core idea

The KL-constrained objective has a known optimal policy. For a reference policy \(\pi_{\text{ref}}\), a coefficient \(\beta\) and a reward \(r\), the optimum is \(\pi_r(y \mid x) \propto \pi_{\text{ref}}(y \mid x)\exp(r(x, y)/\beta)\). Rearranging this gives the reward in terms of the policy, \(r(x, y) = \beta \log(\pi_r(y \mid x)/\pi_{\text{ref}}(y \mid x)) + \beta \log Z(x)\). Substituting this into the Bradley–Terry preference model makes the partition term cancel, and the reward model disappears. What remains is a loss on the policy and the reference model alone.

## Equation or algorithm

The DPO loss over preference triples \((x, y_w, y_l)\) is

\[
\mathcal{L}_{\text{DPO}}(\pi_\theta; \pi_{\text{ref}}) = -\mathbb{E}_{(x, y_w, y_l)} \left[\log \sigma\left(\beta \log \frac{\pi_\theta(y_w \mid x)}{\pi_{\text{ref}}(y_w \mid x)} - \beta \log \frac{\pi_\theta(y_l \mid x)}{\pi_{\text{ref}}(y_l \mid x)}\right)\right]
\]

where \(y_w\) is the preferred completion, \(y_l\) the dispreferred one, and \(\beta\) controls the strength of the KL constraint. The procedure:

1. Take a batch of prompts with preferred and dispreferred completions.
2. Compute the log-probability of each completion under the policy and under the frozen reference model.
3. Take a gradient step on the loss above.
4. Repeat until the policy converges. No sampling from the policy during training is needed.

## Results

The paper compares DPO with PPO-based RLHF on several tasks:

- **Sentiment control.** DPO "produces by far the most efficient frontier, achieving the highest reward while still achieving low KL", and exceeds PPO-based RLHF in controlling the sentiment of generations.
- **Summarisation.** DPO has a win rate of about 61% against the reference at temperature 0.0, compared with 57% for PPO at its best sampling temperature. The authors note that they did not meaningfully tune \(\beta\), so these results may underestimate DPO.
- **Human study.** DPO samples at temperature 0.25 were preferred 58% of the time over PPO samples at temperature 0.
- **Dialogue.** The paper reports that DPO is the only computationally efficient method that improves over the preferred completions in the Anthropic HH dataset.

## Limitations

- **Scale.** The models were evaluated up to 6B parameters, and the paper calls scaling DPO to much larger models future work.
- **Generalisation.** The paper asks how the DPO policy generalises out of distribution, compared with learning from an explicit reward function, and leaves this open.
- **Over-optimisation.** The paper asks how reward over-optimisation appears in the direct setting, which is not settled.
- **Automatic judgements.** The win rates computed by GPT-4 depend on the prompt, so the evaluation itself is open to question.

## Connections

- Parent topic: [Learning from Human Feedback](../index.md), and the wider [Reinforcement Learning](../../index.md) overview.
- DPO removes the explicit reward model of [Reward modelling](../reward-modelling/index.md) and uses the same Bradley–Terry comparison model.
- It replaces the policy-optimisation step of [InstructGPT](../../../models/llm/instructgpt-rlhf/index.md), which uses [Proximal Policy Optimisation](../../proximal-policy-optimisation/index.md).

## Applications

- **Preference fine-tuning of language models.** The paper fine-tunes summarisation and dialogue models on preference data.
- **Controlled generation.** Steering the sentiment of generated text toward preferred outputs.

## Open questions

- Whether a policy trained without an explicit reward model still generalises as well as one trained with it.
- How to tune \(\beta\) and the reference model for best results at larger scale.

## References

### Seminal papers

- Rafailov et al. (2023), "Direct preference optimization: your language model is secretly a reward model", NeurIPS 2023, arXiv:2305.18290 — The DPO paper, with the loss, the closed-form derivation and the results above.
- Ouyang et al. (2022), "Training language models to follow instructions with human feedback", arXiv:2203.02155 — InstructGPT, the RLHF pipeline that DPO simplifies.
- Christiano et al. (2017), "Deep reinforcement learning from human preferences", arXiv:1706.03741 — Learns reward functions from human comparisons, the basis of the reward model that DPO avoids.
- Stiennon et al. (2020), "Learning to summarize from human feedback", NeurIPS 2020, arXiv:2009.01325 — Summarisation with a reward model and PPO, one of the baselines DPO is compared against.
- Bradley & Terry (1952), "Rank analysis of incomplete block designs: I. The method of paired comparisons", *Biometrika* 39(3/4), 324. https://doi.org/10.2307/2334029 — The paired-comparison model used to derive the DPO loss.
