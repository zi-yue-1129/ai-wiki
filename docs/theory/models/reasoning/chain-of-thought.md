---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/llm
tags:
  - reasoning
  - prompting
aliases:
  - Chain of thought
  - Chain-of-thought prompting
  - 思維鏈
  - 思維鏈提示
---

# Chain of Thought

Chain-of-thought prompting asks a language model to write its intermediate reasoning steps before the final answer, usually by showing it a few worked examples in which the steps are spelled out. The method needs no training. It is the first step in the [reasoning models](index.md) line of work, and the parent page compares it with the other landmark methods.

## Overview

A plain prompt such as "question, answer" asks the model to jump straight to the result. For a multi-step problem, the model must then carry every intermediate calculation implicitly. Chain-of-thought prompting makes the intermediate steps part of the output. Each exemplar in the prompt shows a question, a sequence of reasoning steps and an answer, and the model imitates that pattern on a new question.

## Problem

Standard few-shot prompting, in which the examples show only inputs and answers, performs poorly on arithmetic and commonsense problems that need several inferential steps. Wei et al. (2022) asked whether writing the steps in the prompt would change this.

## Core idea

Include a few exemplars whose answers are preceded by a natural-language chain of reasoning steps. The model then produces a chain for the new question before its answer. The authors argue that reasoning ability of this kind appears only in sufficiently large language models.

## Algorithm

1. Write a small set of exemplars. Each has a question, a chain of intermediate steps and a final answer.
2. Append the new question after the exemplars.
3. Decode the model's continuation. Read the final answer from the end of the generated chain.

No weights change. The same procedure can be run with any model that accepts a text prompt.

## Results

- Wei et al. (2022) report that prompting a 540-billion-parameter model with just eight chain-of-thought exemplars reaches state-of-the-art accuracy on the GSM8K benchmark of math word problems. The abstract also says the approach outperforms a fine-tuned GPT-3 model paired with a verifier on that benchmark.
- Kojima et al. (2022) show a zero-shot variant: appending the phrase "Let's think step by step" to the question, with no exemplars. With InstructGPT (text-davinci-002), the abstract reports accuracy rising from 17.7% to 78.7% on MultiArith and from 10.4% to 40.7% on GSM8K. Because this variant is described here rather than on its own page, it is a candidate for a separate page later.

## Limitations

- The gains appear mainly in large models. The abstract ties the reasoning ability to "sufficiently large" models, so small models gain little.
- The exemplars have to be written by hand for each task, and their quality affects the result.
- A fluent chain can still contain a wrong step, and the final answer can be wrong even when the chain looks convincing. Sampling several chains and voting on the answers, see [self-consistency](self-consistency.md), addresses part of this.
- The written chain is an output, not a direct report of the model's internal computation. Whether the two match is an open question on the [parent page](index.md).

## Connections

- [Large Language Models](../llm/index.md) lists chain-of-thought as one of the capabilities that emerge with scale.
- [Self-consistency](self-consistency.md) builds directly on this method.
- [DeepSeek-R1](deepseek-r1.md) trains the step-by-step behaviour into the model instead of prompting for it.

## Open questions

- Which tasks benefit from explicit steps, and which are hurt by them?
- How much of the gain is due to the steps themselves, and how much to the format of the exemplars?

## References

### Seminal papers

- Wei, J., et al. (2022). *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*. arXiv. https://arxiv.org/abs/2201.11903 — The original method, with exemplars that contain intermediate reasoning steps.
- Kojima, T., et al. (2022). *Large Language Models are Zero-Shot Reasoners*. NeurIPS. https://arxiv.org/abs/2205.11916 — Shows that the phrase "Let's think step by step" elicits reasoning without exemplars.
- Brown, T. B., et al. (2020). *Language Models are Few-Shot Learners*. arXiv. https://arxiv.org/abs/2005.14165 — The few-shot prompting setting that chain-of-thought extends with written steps.
- Wang, X., et al. (2022). *Self-Consistency Improves Chain of Thought Reasoning in Language Models*. arXiv. https://arxiv.org/abs/2203.11171 — Replaces greedy decoding of a single chain with a vote over sampled chains.

### Surveys and textbooks

- Huang, J. & Chang, K. C.-C. (2023). *Towards Reasoning in Large Language Models: A Survey*. arXiv. https://arxiv.org/abs/2212.10403 — Places chain-of-thought within the wider literature on eliciting and evaluating reasoning.
