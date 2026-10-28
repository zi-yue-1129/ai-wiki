---
status: draft
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

## Problem

Given a fixed amount of inference compute per problem, which test-time strategy gives the best accuracy, and how does that compare with training a larger model? Snell et al. ask this as a compute-matched question, measured in floating-point operations.

## Core idea

The paper studies two mechanisms and picks between them for each prompt:

1. **Verifier-guided search:** generate candidate solutions and score their intermediate steps with a process reward model, then search over those scores. The verifier is trained on step-level labels, following [Lightman et al. (2023)](https://arxiv.org/abs/2305.20050).
2. **Adaptive revision:** update the model's output distribution for each prompt at test time, so that later attempts improve on earlier ones.

The compute-optimal choice depends on how hard the prompt is for the base model.

## Procedure in outline

For each prompt:

1. Estimate the difficulty of the prompt, for example from the base model's success rate on a small sample.
2. Choose a strategy and budget for that difficulty. Use search with a verifier, or revision, or plain sampling.
3. Run the chosen strategy and return the selected answer.

The paper's comparison baseline is best-of-\(N\): sample \(N\) answers and keep the one the verifier scores highest.

## Results

- In a FLOPs-matched evaluation, test-time compute "can be used to outperform a 14x larger model", according to the abstract. This holds only on problems where the smaller base model reaches a somewhat non-trivial success rate.
- The compute-optimal strategy improves efficiency by more than 4x compared with the best-of-\(N\) baseline, according to the abstract.

## Limitations

- The gain depends on prompt difficulty. For problems the base model almost never solves, extra compute adds little, and for problems it already solves reliably, it is wasted.
- The strategies need a verifier or a revision signal, and training a good process reward model is a separate cost.
- The results are reported for particular models and benchmarks. The abstract does not claim that the ratios hold across all tasks.

## Connections

- [Self-consistency](self-consistency.md) is the simplest test-time strategy, voting over samples with no verifier.
- [Chain of thought](chain-of-thought.md) provides the reasoning text that search and revision operate on.
- [DeepSeek-R1](deepseek-r1.md) moves part of the same compute into training, so the model reasons longer by default.
- [Large Language Models](../llm/index.md) describes the training stages where the reasoning behaviour is shaped.

## Open questions

- How should the difficulty of a prompt be estimated cheaply enough that the estimate does not cost more than it saves?
- Do process verifiers generalise beyond the domain they were trained on?

## References

### Seminal papers

- Snell, C., Lee, J., Xu, K. & Kumar, A. (2024). *Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters*. arXiv. https://arxiv.org/abs/2408.03314 — Compares compute-optimal test-time strategies with a model 14 times larger, under a fixed compute budget.
- Lightman, H., et al. (2023). *Let's Verify Step by Step*. arXiv. https://arxiv.org/abs/2305.20050 — Trains process reward models on step-level labels and shows they beat outcome supervision on MATH.
- Wang, X., et al. (2022). *Self-Consistency Improves Chain of Thought Reasoning in Language Models*. arXiv. https://arxiv.org/abs/2203.11171 — An early way of spending test-time compute: sample many paths and vote.
- DeepSeek-AI (2025). *DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning*. arXiv. https://arxiv.org/abs/2501.12948 — Moves the extra reasoning into training with reinforcement learning on verifiable rewards.

### Surveys and textbooks

- Huang, J. & Chang, K. C.-C. (2023). *Towards Reasoning in Large Language Models: A Survey*. arXiv. https://arxiv.org/abs/2212.10403 — Surveys inference-time methods for reasoning and the evaluation they need.
