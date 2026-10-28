---
status: complete
last_reviewed: 2026-10-28
related:
  - theory/models/llm
tags:
  - reasoning
  - prompting
aliases:
  - Zero-shot chain of thought
  - Let's think step by step
  - 零樣本思維鏈
---

# Zero-Shot Chain of Thought

Zero-shot chain of thought asks a language model to reason step by step without any worked examples. It appends a short trigger phrase, "Let's think step by step", to the question, and the model writes its own reasoning before answering. The method is a variant of [chain of thought](chain-of-thought.md), which needs exemplars, and it sits among the other methods on the [reasoning models](index.md) page.

## Overview

Chain-of-thought prompting shows the model how to reason by giving it exemplars with written steps. That requires someone to write those exemplars for each task. Kojima et al. (2022) ask whether the model can be prompted to reason without any exemplars, using only a trigger phrase added to the question.

## Key concepts

- **Zero-shot prompting**: a prompt with no worked examples, only the task.
- **Trigger phrase**: a short instruction that changes how the model responds, here "Let's think step by step".
- **Reasoning chain**: the intermediate steps the model writes before its final answer.

## Problem

Standard chain-of-thought prompting needs a few exemplars whose reasoning steps are written by hand. Their quality affects the result, and writing them for every new task is costly. The question is whether a simple instruction can unlock step-by-step reasoning without exemplars.

## Core idea

Append the trigger phrase to the question. The model then produces a reasoning chain before the answer, in the same way it does when it has exemplars. The method changes only the prompt.

## How it works

The procedure has two steps in the simplest form: prompt the model with the question and the trigger phrase, then read the final answer from the text it writes. No exemplars are included, and no weights change.

## Algorithm

1. Take the question.
2. Append "Let's think step by step" to it.
3. Decode the model's continuation, and read the final answer from the end of the generated reasoning.

## Key methods

Zero-shot chain of thought is a single method, a trigger phrase on top of an unchanged model. Its main comparison is with few-shot chain of thought, which adds exemplars with written steps, and with plain zero-shot prompting, which has no trigger.

## Results

- With InstructGPT (text-davinci-002), the abstract reports accuracy on MultiArith rising from 17.7% to 78.7%, and on GSM8K from 10.4% to 40.7%, when the trigger phrase is used.
- The abstract presents these as zero-shot results, with no exemplars in the prompt.

## Limitations

- The reported gains are for one model family in the abstract, InstructGPT text-davinci-002. The abstract does not establish the same gains for other models.
- The accuracy on hard tasks remains low, so the trigger does not close the gap to stronger methods such as [self-consistency](self-consistency.md).
- As with chain of thought, the written reasoning is an output and not a direct report of the model's internal computation.

## Variants and more variants

- **Few-shot chain of thought**: the exemplar-based method on the [chain-of-thought](chain-of-thought.md) page, which the trigger phrase replaces when no exemplars are available.
- **Self-consistency**: sampling several zero-shot reasoning chains and voting, see [self-consistency](self-consistency.md).

## Connections

- [Chain of thought](chain-of-thought.md) is the exemplar-based method this page simplifies.
- [Self-consistency](self-consistency.md) can be run on top of zero-shot reasoning chains.
- [Large Language Models](../llm/index.md) describes the prompting setting in which the trigger is used.

## Applications

- Quick reasoning prompts for tasks where writing exemplars is not practical.
- Baseline prompts when comparing reasoning methods on a new benchmark.

## Open questions

- Which trigger phrases work best, and do they transfer across models?
- How much of the gain comes from the reasoning itself, and how much from the output format the trigger encourages?

## References

### Seminal papers

- Kojima, T., et al. (2022). *Large Language Models are Zero-Shot Reasoners*. arXiv. https://arxiv.org/abs/2205.11916 — Introduces the trigger phrase "Let's think step by step" and reports the MultiArith and GSM8K results used on this page.
- Wei, J., et al. (2022). *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*. arXiv. https://arxiv.org/abs/2201.11903 — The exemplar-based method that the zero-shot variant is compared with.
- Brown, T. B., et al. (2020). *Language Models are Few-Shot Learners*. arXiv. https://arxiv.org/abs/2005.14165 — The zero-shot and few-shot prompting settings that this method is measured against.

### Surveys and textbooks

- Huang, J. & Chang, K. C.-C. (2023). *Towards Reasoning in Large Language Models: A Survey*. arXiv. https://arxiv.org/abs/2212.10403 — Surveys prompting-based reasoning methods, including zero-shot variants.
