---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/llm
tags:
  - reasoning
  - decoding
aliases:
  - Self-consistency
  - Self-consistency decoding
  - 自洽性
  - 自洽解碼
---

# Self-Consistency

Self-consistency replaces the single greedy chain of thought with many sampled chains, then returns the answer that most of them reach. It needs no training and works with any model that can produce chain-of-thought text. The family overview is on the [reasoning models](index.md) page, and the method it extends is [chain of thought](chain-of-thought.md).

## Overview

Chain-of-thought prompting usually decodes one reasoning path, the most likely one at each step. That path can contain an error that the model would not repeat on another attempt. The method rests on an intuition from Wang et al. (2022): a question usually admits several valid reasoning routes to the same answer, while errors tend to scatter across different answers. Sampling diverse paths and voting then favours the consistent answer.

## Problem

Greedy chain-of-thought decoding is brittle. A single wrong step is enough to produce a wrong answer, and the method gives no signal about whether the chain is reliable.

## Core idea

Sample a diverse set of reasoning paths instead of taking only the greedy one. Then marginalise over the paths: group the chains by their final answer and select the answer with the greatest support. The authors describe this as selecting the most consistent answer by marginalising out the sampled reasoning paths.

## Algorithm

1. Prompt the model with chain-of-thought exemplars, as in the [chain-of-thought](chain-of-thought.md) method.
2. Sample \(k\) reasoning paths for the same question, using a sampling temperature above zero so that the paths differ.
3. Extract the final answer from each path.
4. Return the answer \(a^\*\) that appears most often: \(a^\* = \arg\max_a \sum_{i=1}^{k} \mathbf{1}[\,a_i = a\,]\).

The method needs an answer that can be compared across paths. Aggregating free-form text is harder and is not covered by the abstract.

## Results

Wang et al. (2022) report gains over greedy chain-of-thought decoding on arithmetic and commonsense benchmarks. The abstract lists these improvements in accuracy:

- GSM8K: +17.9%
- SVAMP: +11.0%
- AQuA: +12.2%
- StrategyQA: +6.4%
- ARC-challenge: +3.9%

The abstract does not state how many samples \(k\) were drawn, so that setting should be taken from the full paper before it is reused.

## Limitations

- Cost grows with \(k\). Each extra sample is a full generation, so the method trades compute for accuracy directly. This is the same trade-off described on the [test-time compute](test-time-scaling.md) page.
- Voting needs a comparable final answer. For open-ended questions there is no simple majority, and the method needs another way to group answers.
- Majority voting can agree on a wrong answer when the model is systematically wrong. Sampling does not fix a missing skill.
- The paper's gains are reported on benchmarks with short answers. Their size on long-form tasks is not shown.

## Connections

- [Chain of thought](chain-of-thought.md) is the prompting method that self-consistency decodes many times.
- [Test-time compute scaling](test-time-scaling.md) generalises the idea: spend extra samples or search steps, and choose which ones to keep with a verifier rather than a vote.
- [DeepSeek-R1](deepseek-r1.md) uses a related idea when it samples many candidate solutions to create training data.

## Open questions

- How should the number of samples be chosen for each query, given that easy questions need fewer?
- Can answer grouping be learned for free-form outputs, where exact matching fails?

## References

### Seminal papers

- Wang, X., et al. (2022). *Self-Consistency Improves Chain of Thought Reasoning in Language Models*. arXiv. https://arxiv.org/abs/2203.11171 — The original method: sample diverse reasoning paths and keep the most consistent final answer.
- Wei, J., et al. (2022). *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*. arXiv. https://arxiv.org/abs/2201.11903 — The greedy chain-of-thought baseline that self-consistency replaces.
- Snell, C., Lee, J., Xu, K. & Kumar, A. (2024). *Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters*. arXiv. https://arxiv.org/abs/2408.03314 — Studies how spending more inference compute, including sampling, can rival a larger model.
- Lightman, H., et al. (2023). *Let's Verify Step by Step*. arXiv. https://arxiv.org/abs/2305.20050 — Uses a step-level verifier to rank candidate solutions, an alternative to voting.

### Surveys and textbooks

- Huang, J. & Chang, K. C.-C. (2023). *Towards Reasoning in Large Language Models: A Survey*. arXiv. https://arxiv.org/abs/2212.10403 — Surveys decoding and prompting methods for reasoning, including sampling-based voting.
