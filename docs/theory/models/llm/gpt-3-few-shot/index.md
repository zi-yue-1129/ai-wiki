---
status: complete
last_reviewed: 2026-10-28
---

# GPT-3: few-shot learning from the prompt (Brown et al., 2020)

A 175-billion-parameter autoregressive Transformer, tested with zero, one or a few worked examples in the prompt, with no fine-tuning on the task.

## Overview

Earlier systems that learned a new language task usually needed a fine-tuning dataset of that task. The GPT-3 paper asks whether a large enough language model can instead learn the task from a handful of examples written into its prompt, with no weight updates at all. The answer is yes for many tasks, and the paper measures how far that goes.

## Key concepts

- **Autoregressive Transformer**: a model that predicts each next token from the tokens before it.
- **Zero-shot**: the task is described in the prompt, with no examples.
- **One-shot**: one worked example in the prompt before the new input.
- **Few-shot**: a small number of worked examples in the prompt before the new input.
- **In-context learning**: learning the task from the prompt, without a gradient update.

## Problem

Can a language model learn a new task from a few examples in its prompt, without any gradient update?

## Core idea

Scale an autoregressive Transformer to 175 billion parameters and test it with zero, one or a few worked examples in the prompt. The model is not fine-tuned on the task.

## How it works

The prompt holds a task description and a few input–output pairs. The model then continues the text, and its continuation is read as the answer. Nothing in the network changes, so the same model can switch tasks by changing only the prompt.

## Key methods

The paper compares three prompting settings for one model. It sets them against fine-tuning on a task-specific dataset, which the abstract says prior approaches needed. The three settings are zero-shot, one-shot and few-shot, which differ only in how many examples the prompt contains.

## Algorithm

1. Write a task description and a few input–output examples into the prompt.
2. Append the new input.
3. Let the model generate the output token by token. No weights change.

## Results

- The abstract reports strong performance on many NLP datasets, including translation, question answering and cloze tasks.
- It also reports performance on tasks that require on-the-fly reasoning or domain adaptation, such as unscrambling words, using a novel word in a sentence, or performing 3-digit arithmetic.

## Limitations

- The abstract notes datasets where GPT-3's few-shot learning still struggles.
- It also notes datasets where GPT-3 faces methodological issues related to training on large web corpora.
- Prior methods, the abstract says, still need task-specific fine-tuning datasets of thousands or tens of thousands of examples. GPT-3 reduces this need, but does not remove it on every task.

## Variants and more variants

- **Zero-shot**: the task is described but not demonstrated.
- **One-shot**: a single example is shown.
- **Few-shot**: several examples are shown, which the paper uses for its main few-shot results.

## Connections

- Parent topic: [Large Language Models](../index.md)
- Other method on this topic: [Compute-Optimal Training](../compute-optimal-training/index.md)
- Other method on this topic: [InstructGPT and RLHF](../instructgpt-rlhf/index.md)

## Applications

- Prompting a single general-purpose model for translation, question answering and similar tasks without training a new model for each.
- Rapid prototyping of a new task by writing a few examples, before deciding whether fine-tuning is worth the cost.

## Open questions

- Which tasks benefit from in-context examples, and which still need fine-tuning?
- How much of the performance comes from the training data rather than from in-context learning itself?

## References

### Seminal papers

- Brown, T. B., et al. (2020). *Language Models are Few-Shot Learners*. arXiv. https://arxiv.org/abs/2005.14165 — The GPT-3 paper, showing that a 175-billion-parameter model can learn new tasks from a few examples given in the prompt.
- Kaplan, J., et al. (2020). *Scaling Laws for Neural Language Models*. arXiv. https://arxiv.org/abs/2001.08361 — Shows how loss falls predictably as model size, data and compute increase, the trend that motivates scaling up to 175 billion parameters.
- Hoffmann, J., et al. (2022). *Training Compute-Optimal Large Language Models*. arXiv. https://arxiv.org/abs/2203.15556 — The Chinchilla study, arguing that model size and training tokens should grow together for a fixed compute budget.
- Ouyang, L., et al. (2022). *Training language models to follow instructions with human feedback*. arXiv. https://arxiv.org/abs/2203.02155 — InstructGPT, which aligns language models with user intent through fine-tuning on human feedback.
- Wei, J., et al. (2022). *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*. arXiv. https://arxiv.org/abs/2201.11903 — Shows that prompting models to write intermediate reasoning steps improves multi-step problem solving.

### Surveys and textbooks

- Zhao, W. X., et al. (2023). *A Survey of Large Language Models*. arXiv. https://arxiv.org/abs/2303.18223 — A broad survey of pre-training, adaptation and evaluation of LLMs, with a timeline of models.

## Further learning

- Hugging Face. *LLM Course*. https://huggingface.co/learn/llm-course — Hands-on course on using, fine-tuning and building LLMs with the Hugging Face libraries.
- Karpathy, A. (2023). *[1hr Talk] Intro to Large Language Models*. YouTube. https://www.youtube.com/watch?v=zjkBMFhNj_g — A one-hour non-technical overview of how LLMs are trained, what they can do and where they fail.
