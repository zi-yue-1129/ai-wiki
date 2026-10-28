---
status: complete
last_reviewed: 2026-10-28
related:
  - theory/models/llm
  - theory/paradigms/reinforcement-learning
tags:
  - reasoning
  - verification
aliases:
  - Process reward model
  - PRM
  - Process supervision
  - 過程獎勵模型
  - 過程監督
---

# Process Reward Models

A process reward model (PRM) scores each intermediate step of a solution, rather than only the final answer. It is trained with step-level feedback, and it is used to rank candidate solutions or to guide a search over them. The method is part of the verifier-based line of work on the [reasoning models](index.md) page, and it is the verifier used in the test-time methods of [test-time compute scaling](test-time-scaling.md).

## Overview

A solution to a multi-step problem can reach the right answer through a flawed step, or the wrong answer through a single error. A reward on the final answer alone cannot tell these cases apart. A PRM gives a score to each step, so that a flawed step can be found and a candidate solution can be judged on its reasoning as well as its result.

## Key concepts

- **Outcome supervision**: training or scoring on the final answer only.
- **Process supervision**: training or scoring on the correctness of each intermediate step.
- **Process reward model (PRM)**: a model that outputs a score for each step of a solution.
- **Verifier**: a model that scores candidate solutions, of which a PRM is one kind.

## Problem

Language models make errors in the middle of a multi-step solution, and a final-answer check cannot locate them. The question is whether step-level feedback gives a better signal for training a verifier than outcome feedback, and how the verifier can then be used at inference.

## Core idea

Train a reward model on the correctness of each step, then use it to score candidate solutions step by step. Lightman et al. (2023) compare step-level feedback with outcome feedback on the MATH dataset. Snell et al. (2024) use a PRM at test time, and they train theirs without human step labels.

## How it works

1. Sample one or more candidate solutions from a language model for a question.
2. Score each step of each solution with the PRM.
3. Use the step scores to pick a solution, for example by ranking complete solutions, or to guide a search that extends promising partial solutions.

The aggregation of step scores into a solution score differs between papers. The abstracts reviewed here do not specify one rule, so the choice should be taken from the full paper before it is reused.

## Algorithm

- **Training**: collect step-level correctness labels, either from human annotators or from estimated rollouts, and fit the reward model to them.
- **Inference**: score candidate solutions step by step and select one, as described in How it works.

## Key methods

- **Outcome reward model**: scores only the final answer, and is the baseline in Lightman et al. (2023).
- **Human-labelled PRM**: trained on step labels written by people. Lightman et al. (2023) build one of these on the PRM800K data.
- **Rollout-labelled PRM**: trained on per-step correctness estimated from Monte Carlo rollouts, the approach Snell et al. (2024) use.

## Results

- Lightman et al. (2023) report that process supervision significantly outperforms outcome supervision on the MATH dataset. Their process-supervised model solves 78% of problems from a representative subset of the MATH test set, according to the abstract.
- Snell et al. (2024) train their PRM from estimates of per-step correctness obtained with Monte Carlo rollouts, not from human step labels. They report that the human-labelled PRM800K data was largely ineffective for them.

## Limitations

- Step labels are costly. Human labels give strong signal, but they are expensive to collect at scale.
- Rollout-based labels avoid human annotation, but they depend on the base model's own success rate and cost extra sampling.
- A PRM trained in one domain may not generalise to another. The open questions on the [test-time](test-time-scaling.md) page discuss this.
- The gains reported in these papers are measured on mathematics benchmarks, and the abstracts do not claim they carry over to other tasks.

## Variants and more variants

- **Outcome reward model**: the simpler baseline, scoring only the final answer.
- **Self-consistency**: a verifier-free alternative, which votes over sampled answers instead, see [self-consistency](self-consistency.md).
- **Verifier-guided search**: uses a PRM to guide the search over partial solutions, as in the test-time methods on [test-time compute scaling](test-time-scaling.md).

## Connections

- [Test-time compute scaling](test-time-scaling.md) uses a PRM for its verifier-guided search.
- [Self-consistency](self-consistency.md) is the simplest verifier-free alternative.
- [Reinforcement learning](../../paradigms/reinforcement-learning/index.md) gives the broader framework in which reward models are used to train policies.

## Applications

- Ranking candidate solutions to mathematics problems at inference.
- Locating the first wrong step in a solution, for error analysis or teaching.

## Open questions

- How should step scores be aggregated into a score for the whole solution?
- Can rollout-based labels match human labels at scale, and in domains other than mathematics?

## References

### Seminal papers

- Lightman, H., et al. (2023). *Let's Verify Step by Step*. arXiv. https://arxiv.org/abs/2305.20050 — Compares process supervision with outcome supervision on MATH, and reports that the process-supervised model solves 78% of a representative subset of MATH test problems.
- Snell, C., Lee, J., Xu, K. & Kumar, A. (2024). *Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters*. arXiv. https://arxiv.org/abs/2408.03314 — Uses a PRM trained on Monte Carlo rollout estimates for verifier-guided search at test time.
- Wang, X., et al. (2023). *Self-Consistency Improves Chain of Thought Reasoning in Language Models*. ICLR. https://arxiv.org/abs/2203.11171 — The verifier-free alternative, voting over sampled reasoning paths.
- DeepSeek-AI (2025). *DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning*. Nature, 645, 633–638. https://doi.org/10.1038/s41586-025-09422-z — Uses rule-based rewards rather than a learned PRM, which contrasts with the step-level approach on this page.

### Surveys and textbooks

- Huang, J. & Chang, K. C.-C. (2023). *Towards Reasoning in Large Language Models: A Survey*. arXiv. https://arxiv.org/abs/2212.10403 — Surveys verification-based and search-based reasoning methods.
