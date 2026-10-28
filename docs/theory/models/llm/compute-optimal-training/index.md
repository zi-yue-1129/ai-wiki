---
status: draft
last_reviewed: 2026-10-28
---

# Compute-optimal training (Hoffmann et al., 2022)

For a fixed compute budget, the best model size and number of training tokens are found by fitting the trade-off across many training runs.

## Problem

For a fixed compute budget, how should model size and the number of training tokens be balanced?

## Core idea

Train more than 400 language models, from 70 million to over 16 billion parameters, on 5 to 500 billion tokens, then find the best size for each budget. Model size and data should grow together.

## Rule

For every doubling of model size, double the number of training tokens.

## Results

Chinchilla, with 70 billion parameters and four times more data, used the same compute as Gopher (280 billion parameters) and outperformed Gopher, GPT-3 and others on a wide range of downstream tasks. It reached 67.5% average accuracy on MMLU.

## Limitations

The rule was fitted on the range the authors trained. Many later models train well beyond this ratio, because a smaller model is cheaper to serve.

## Connections

- Parent topic: [Large Language Models](../index.md)
- Other method on this topic: [GPT-3 Few-Shot Learning](../gpt-3-few-shot/index.md)
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


### Articles and documentation

- Hugging Face. *LLM Course*. https://huggingface.co/learn/llm-course — Hands-on course on using, fine-tuning and building LLMs with the Hugging Face libraries.
