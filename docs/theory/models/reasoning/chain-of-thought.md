---
status: complete
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

## Key concepts

- **Exemplar**: a worked example in the prompt, containing a question, its reasoning chain and its answer.
- **Reasoning chain**: the sequence of natural-language intermediate steps the model writes before its answer.
- **Few-shot prompting**: a setting in which the model is given a handful of examples in the prompt and no weight updates. The method extends it by adding the steps to each example.
- **Zero-shot variant**: a prompt with no exemplars, in which a trigger phrase asks the model to reason first.

## Problem

Standard few-shot prompting, in which the examples show only inputs and answers, performs poorly on arithmetic and commonsense problems that need several inferential steps. Wei et al. (2022) asked whether writing the steps in the prompt would change this.

## Core idea

Include a few exemplars whose answers are preceded by a natural-language chain of reasoning steps. The model then produces a chain for the new question before its answer. The authors argue that reasoning ability of this kind appears only in sufficiently large language models, and that the gains they measure come from the model imitating the reasoning steps, not from any change in its weights.

## How it works

Given the prompt below, the model continues the text with a chain of steps and then a final answer. The first exemplar shows the pattern to imitate. This is an illustrative prompt written for this page, not one taken from the paper.

```text
Q: A shop has 12 pens. It sells 5 and then receives 4 more.
   How many pens does it have?
A: The shop starts with 12 pens. After selling 5, it has 12 - 5 = 7.
   After receiving 4, it has 7 + 4 = 11. The answer is 11.

Q: A library has 30 books. It lends 8 and then gets 6 returned.
   How many books does it have?
A:
```

The model writes its own steps after the final `A:` and ends with an answer, here 30 − 8 + 6 = 28.

## Algorithm

1. Write a small set of exemplars. Each has a question, a chain of intermediate steps and a final answer.
2. Append the new question after the exemplars.
3. Decode the model's continuation. Read the final answer from the end of the generated chain.

No weights change. The same procedure can be run with any model that accepts a text prompt.

## Key methods

Two entries on this page, each with the detail it needs:

- **Few-shot chain of thought** (Wei et al., 2022): exemplars with written steps, the method described above.
- **Zero-shot chain of thought** (Kojima et al., 2022): no exemplars. The trigger phrase "Let's think step by step" is appended to the question. It is covered here because the trigger changes only the prompt, not the method.

## Results

- Wei et al. (2022) report that prompting a 540-billion-parameter model with just eight chain-of-thought exemplars reaches state-of-the-art accuracy on the GSM8K benchmark of math word problems. The abstract also says this result surpasses a fine-tuned GPT-3 model that uses a verifier.
- Kojima et al. (2022) show the zero-shot variant. The abstract reports that, with InstructGPT (text-davinci-002), accuracy on MultiArith rises from 17.7% to 78.7%, and on GSM8K from 10.4% to 40.7%.
- The Wei et al. abstract ties these gains to model size. Smaller models were not reported to gain in the same way.

## Limitations

- The gains appear mainly in large models. The abstract ties the reasoning ability to "sufficiently large" models, so small models gain little.
- The exemplars have to be written by hand for each task, and their quality affects the result.
- A fluent chain can still contain a wrong step, and the final answer can be wrong even when the chain looks convincing. Sampling several chains and voting on the answers, see [self-consistency](self-consistency.md), addresses part of this.
- The written chain is an output, not a direct report of the model's internal computation. Whether the two match is an open question on the [parent page](index.md).

## Variants and more variants

- **Zero-shot chain of thought**: the trigger phrase replaces exemplars, at the cost of lower accuracy on hard tasks.
- **Self-consistency**: samples several chains and votes, see [self-consistency](self-consistency.md).
- **Trained reasoning**: [DeepSeek-R1](deepseek-r1.md) learns the step-by-step behaviour from reward signals, so the prompt no longer has to request it.

## Connections

- [Large Language Models](../llm/index.md) lists chain-of-thought as one of the capabilities that emerge with scale.
- [Self-consistency](self-consistency.md) builds directly on this method.
- [DeepSeek-R1](deepseek-r1.md) trains the step-by-step behaviour into the model instead of prompting for it.

## Applications

- Arithmetic and word-problem solving, the benchmarks on which the method was first shown to work.
- Multi-step question answering, where an intermediate justification helps a reader check the answer.
- Prompt design for tutoring and coding assistants, which often ask the model to explain its steps.

## Open questions

- Which tasks benefit from explicit steps, and which are hurt by them?
- How much of the gain is due to the steps themselves, and how much to the format of the exemplars?
- Do written chains describe the computation that produced the answer, or are they a plausible story written after the fact?

## References

### Seminal papers

- Wei, J., et al. (2022). *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*. arXiv. https://arxiv.org/abs/2201.11903 — The original method, with exemplars that contain intermediate reasoning steps, and the 540B-parameter GSM8K result.
- Kojima, T., et al. (2022). *Large Language Models are Zero-Shot Reasoners*. arXiv. https://arxiv.org/abs/2205.11916 — Shows that the phrase "Let's think step by step" elicits reasoning without exemplars, with the MultiArith and GSM8K numbers used above.
- Brown, T. B., et al. (2020). *Language Models are Few-Shot Learners*. arXiv. https://arxiv.org/abs/2005.14165 — The few-shot prompting setting that chain-of-thought extends with written steps, for a 175-billion-parameter model.
- Wang, X., et al. (2023). *Self-Consistency Improves Chain of Thought Reasoning in Language Models*. ICLR. https://arxiv.org/abs/2203.11171 — Replaces greedy decoding of a single chain with a vote over sampled chains.

### Surveys and textbooks

- Huang, J. & Chang, K. C.-C. (2023). *Towards Reasoning in Large Language Models: A Survey*. arXiv. https://arxiv.org/abs/2212.10403 — Places chain-of-thought within the wider literature on eliciting and evaluating reasoning.
