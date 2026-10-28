---
status: complete
last_reviewed: 2026-10-28
related:
  - theory/models/llm
  - theory/paradigms/reinforcement-learning
tags:
  - test-time compute
  - scaling
aliases:
  - Test-time scaling
  - Test-time compute scaling
  - 測試時擴展
  - 測試時運算擴展
---

# Test-Time Compute Scaling

Test-time compute scaling asks how to spend a fixed inference budget most effectively. Snell et al. (2024) show that, for a given prompt, allocating compute adaptively can beat simply using a model that is many times larger. The family overview is on the [reasoning models](index.md) page, and the method sits beside [self-consistency](self-consistency.md), which spends test-time compute by voting.

## Overview

Scaling laws describe how language models improve with more parameters, data and training compute. The same logic applies at inference: a model can be given more compute per query, by sampling more candidates, searching over partial solutions or revising its own answer. The open question is which of these is worth the cost, and whether the best choice depends on the query.

## Key concepts

- **Test-time compute**: the work spent on one query at inference, such as generated tokens, sampled answers or search steps.
- **Process reward model (PRM)**: a model that scores each intermediate step of a solution, rather than only the final answer.
- **Best-of-N**: sampling N answers and keeping the one a verifier scores highest. It is the baseline the paper compares against.
- **FLOPs-matched comparison**: a comparison in which each method is given the same number of floating-point operations.

## Problem

Given a fixed amount of inference compute per problem, which test-time strategy gives the best accuracy, and how does that compare with training a larger model? Snell et al. ask this as a compute-matched question, measured in floating-point operations.

## How it works

The paper studies two mechanisms and picks between them for each prompt.

1. **Verifier-guided search:** generate candidate solutions and score their intermediate steps with a PRM, then search over those scores.
2. **Adaptive revision:** fine-tune the model to refine its own answers, so that each attempt is conditioned on its earlier attempts. At test time, it can produce a sequence of revisions, which the paper compares with sampling the same number of answers in parallel.

The compute-optimal choice depends on how hard the prompt is for the base model.

## Key methods

- [Self-consistency](self-consistency.md): voting over samples, with no verifier.
- Verifier-guided search, from Snell et al. (2024): PRM-scored candidates, with the budget allocated per prompt.
- Sequential revision, from Snell et al. (2024): the model refines its own previous attempts.

## Algorithm

For each prompt:

1. Estimate the difficulty of the prompt. The paper bins questions into five quantiles of increasing difficulty, using the base model's pass@1 estimated from 2048 samples. That estimate needs ground-truth answers, so the practical version bins the average verifier score over the same samples instead.
2. Choose a strategy and budget for that difficulty bin. Use search with a verifier, revision, or plain sampling.
3. Run the chosen strategy and return the selected answer.

The paper's comparison baseline is best-of-N: sample N answers and keep the one the verifier scores highest.

## Results

- In a FLOPs-matched evaluation, test-time compute "can be used to outperform a 14x larger model", according to the abstract. The abstract qualifies this as holding on problems where a smaller base model attains somewhat non-trivial success rates.
- The compute-optimal strategy improves efficiency by more than 4x compared with the best-of-N baseline, according to the abstract.
- The PRM in the paper is trained from estimates of per-step correctness obtained with Monte Carlo rollouts, not from human step labels. The authors report that the human-labelled PRM800k data was largely ineffective for them.

## Limitations

- The gain depends on prompt difficulty. For problems the base model almost never solves, extra compute adds little, and for problems it already solves reliably, it is wasted.
- The strategies need a verifier or a revision signal. Training a good process reward model is a separate cost, and the paper's PRM depends on sampled rollouts rather than human labels.
- The results are reported for particular models and benchmarks. The abstract does not claim that the ratios hold across all tasks.

## Variants and more variants

- **Best-of-N with a verifier**: the simplest verifier-based strategy, scoring N samples and keeping the top one.
- **Sequential revision**: the model conditions on its own earlier attempts. It can be compared with parallel sampling at the same budget.
- **Self-consistency**: voting with no verifier, see [self-consistency](self-consistency.md).

## Connections

- [Self-consistency](self-consistency.md) is the simplest test-time strategy, voting over samples with no verifier.
- [Chain of thought](chain-of-thought.md) provides the reasoning text that search and revision operate on.
- [DeepSeek-R1](deepseek-r1.md) moves part of the same compute into training, so the model reasons longer by default.
- [Large Language Models](../llm/index.md) describes the training stages where the reasoning behaviour is shaped.

## Applications

- Hard mathematics and coding problems, where a larger inference budget can change the answer.
- Routing: a cheap difficulty estimate sends easy queries to plain sampling and hard ones to search, saving compute overall.

## Open questions

- How should the difficulty of a prompt be estimated cheaply enough that the estimate does not cost more than it saves?
- Do process verifiers generalise beyond the domain they were trained on?
- How much of the gain carries over to models and benchmarks other than those in the paper?

## References

### Seminal papers

- Snell, C., Lee, J., Xu, K. & Kumar, A. (2024). *Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters*. arXiv. https://arxiv.org/abs/2408.03314 — Compares compute-optimal test-time strategies with a model 14 times larger, under a fixed compute budget.
- Lightman, H., et al. (2023). *Let's Verify Step by Step*. arXiv. https://arxiv.org/abs/2305.20050 — Trains process reward models on step-level human labels and shows that process supervision outperforms outcome supervision on MATH.
- Wang, X., et al. (2023). *Self-Consistency Improves Chain of Thought Reasoning in Language Models*. ICLR. https://arxiv.org/abs/2203.11171 — An early way of spending test-time compute: sample many paths and vote.
- DeepSeek-AI (2025). *DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning*. Nature, 645, 633–638. https://doi.org/10.1038/s41586-025-09422-z — Moves the extra reasoning into training with reinforcement learning on verifiable rewards.

### Surveys and textbooks

- Huang, J. & Chang, K. C.-C. (2023). *Towards Reasoning in Large Language Models: A Survey*. arXiv. https://arxiv.org/abs/2212.10403 — Surveys inference-time methods for reasoning and the evaluation they need.
