---
status: draft
last_reviewed: 2026-10-28
---

# GPT-3: few-shot learning from the prompt (Brown et al., 2020)

A 175-billion-parameter autoregressive Transformer, tested with zero, one or a few worked examples in the prompt.

## Problem

Can a language model learn a new task from a few examples in its prompt, without any gradient update?

## Core idea

Scale an autoregressive Transformer to 175 billion parameters and test it with zero, one or a few worked examples in the prompt. The model is not fine-tuned on the task.

## Equation or algorithm


  1. Write a task description and a few input–output examples into the prompt.
  2. Append the new input.
  3. Let the model generate the output token by token. No weights change.

## Results

Strong performance on translation, question answering and cloze tasks, and on 3-digit arithmetic, which the abstract names among its on-the-fly reasoning tasks.

## Limitations

The paper reports that few-shot performance still lags behind models fine-tuned on task-specific data on some tasks.

## Connections

- Parent topic: [Large Language Models](../index.md)
- Other method on this topic: [Compute-Optimal Training](../compute-optimal-training/index.md)
- Other method on this topic: [InstructGPT and RLHF](../instructgpt-rlhf/index.md)

## References

### Seminal papers

- Brown, T. B., et al. (2020). *Language Models are Few-Shot Learners*. arXiv. https://arxiv.org/abs/2005.14165 — The GPT-3 paper, showing that very large models can learn new tasks from a few examples given in the prompt.
- Kaplan, J., et al. (2020). *Scaling Laws for Neural Language Models*. arXiv. https://arxiv.org/abs/2001.08361 — Shows how loss falls predictably as model size, data and compute increase.
- Hoffmann, J., et al. (2022). *Training Compute-Optimal Large Language Models*. arXiv. https://arxiv.org/abs/2203.15556 — The Chinchilla study, arguing that model size and training tokens should grow together for a fixed compute budget.
- Ouyang, L., et al. (2022). *Training language models to follow instructions with human feedback*. arXiv. https://arxiv.org/abs/2203.02155 — InstructGPT, which combines supervised fine-tuning with reinforcement learning from human preferences.
- Wei, J., et al. (2022). *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*. arXiv. https://arxiv.org/abs/2201.11903 — Shows that prompting models to write intermediate reasoning steps improves multi-step problem solving.

### Surveys and textbooks

- Zhao, W. X., et al. (2023). *A Survey of Large Language Models*. arXiv. https://arxiv.org/abs/2303.18223 — A broad survey of pre-training, adaptation and evaluation of LLMs, with a timeline of models.

### Lectures and videos

- Karpathy, A. (2023). *[1hr Talk] Intro to Large Language Models*. YouTube. https://www.youtube.com/watch?v=zjkBMFhNj_g — A one-hour non-technical overview of how LLMs are trained, what they can do and where they fail.

### Articles and documentation

- Hugging Face. *LLM Course*. https://huggingface.co/learn/llm-course — Hands-on course on using, fine-tuning and building LLMs with the Hugging Face libraries.
