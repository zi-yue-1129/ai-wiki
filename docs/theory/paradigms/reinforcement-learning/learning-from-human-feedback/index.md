---
tags:
  - reinforcement learning
  - human feedback
  - alignment
---

# Learning from Human Feedback

Learning from human feedback trains an agent using preferences or ratings from people instead of, or in addition to, a hand-written reward. Reinforcement learning from human feedback (RLHF) is the method behind the alignment of most large language models.

## Overview

People are often better at comparing two outputs than at writing a numerical reward. A typical pipeline collects pairwise comparisons, trains a reward model to predict which output people prefer, and then optimises the policy against that reward model, usually with a constraint to stay close to a reference model.

## The RLHF pipeline

1. **Collect comparisons.** Annotators rank pairs of outputs for the same prompt.
2. **Train a reward model.** A network learns to score outputs so that preferred ones score higher, using a Bradley–Terry style likelihood.
3. **Optimise the policy.** A reinforcement learning algorithm, usually PPO, maximises the learned reward, with a penalty for drifting from the supervised model.

## Methods

- [Reward modelling](reward-modelling/index.md): learns a reward from pairwise comparisons with the Bradley–Terry model. It is the first step of RLHF.
- [Direct preference optimisation](dpo/index.md): fits the policy to comparisons with a classification loss, with no explicit reward model and no reinforcement learning loop.
- [InstructGPT](../../../models/llm/instructgpt-rlhf/index.md): the RLHF pipeline applied to GPT-3, combining a reward model with PPO.

## Known problems

- **Reward hacking:** the policy finds outputs that score well on the reward model but are not actually preferred.
- **Annotator disagreement and bias:** preferences reflect particular people and contexts, and they may not generalise.
- **Cost:** collecting comparisons and running online optimisation is expensive.
- **Alternatives:** [direct preference optimisation](dpo/index.md) and similar methods fit the policy to comparisons without an explicit reward model, which simplifies the pipeline.

## Connections

The optimisation step uses the [policy-gradient methods](../policy-gradient-and-actor-critic/index.md). Reward models are supervised classifiers over comparisons, see [supervised learning](../../supervised/index.md). Large language model alignment is covered in [Large Language Models](../../../models/llm/index.md). The distinction between preferences and rewards connects to decision-making research in [neuroscience and psychology](../../../../brain-mind/psychology/index.md).

## Applications

Aligning chat assistants for helpfulness and harmlessness, summarisation tuned to human judgement, and robot tasks specified by comparisons rather than reward functions.

## Open questions

Whose preferences should count, how to detect reward hacking, and how to keep preference-trained models honest when they are more capable than the people rating them are open problems. The long-run effect of optimising against learned preferences is not yet established.

## References

### Seminal papers

- Christiano et al. (2017), "Deep reinforcement learning from human preferences", NeurIPS, [[arXiv:1706.03741](https://arxiv.org/abs/1706.03741)](https://arxiv.org/abs/1706.03741) — The original method for learning reward functions from human comparisons.
- Stiennon et al. (2020), "Learning to summarize from human feedback", NeurIPS, [[arXiv:2009.01325](https://arxiv.org/abs/2009.01325)](https://arxiv.org/abs/2009.01325) — Applies the full pipeline to summarisation and shows that human preference models outperform reference-based metrics.
- Ouyang et al. (2022), "Training language models to follow instructions with human feedback", [[arXiv:2203.02155](https://arxiv.org/abs/2203.02155)](https://arxiv.org/abs/2203.02155) — InstructGPT, the template for RLHF in large language models.

### Surveys and textbooks

(none checked for this page)

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Rafailov et al. (2023), "Direct preference optimization: your language model is secretly a reward model", NeurIPS, [[arXiv:2305.18290](https://arxiv.org/abs/2305.18290)](https://arxiv.org/abs/2305.18290) — Fits the policy to preference pairs directly, without a separate reward model.
- Schulman et al. (2017), "Proximal policy optimization algorithms", [[arXiv:1707.06347](https://arxiv.org/abs/1707.06347)](https://arxiv.org/abs/1707.06347) — The PPO algorithm used in most RLHF pipelines.

## Further reading

- Bradley & Terry (1952), "Rank analysis of incomplete block designs", *Biometrika* 39. https://doi.org/10.2307/2334029 — Introduces the paired-comparison model behind pairwise preference learning.
