---
status: complete
last_reviewed: 2026-10-28
---

# Compute-optimal training (Hoffmann et al., 2022)

For a fixed compute budget, the best model size and number of training tokens are found by fitting the trade-off across many training runs. The paper, known as Chinchilla, argues that model size and training tokens should be scaled together.

## Overview

Training a large language model costs compute, and the budget can be spent on a bigger model, on more data, or on both. Hoffmann et al. ask which split of a fixed budget gives the best final model, and answer it with an empirical fit across many training runs.

## Key concepts

- **Compute budget**: the total training compute, which grows with the number of parameters times the number of training tokens.
- **Training tokens**: the amount of text the model sees during training.
- **Scaling law**: a fitted relation between model size, data and loss, used to choose the split of a budget.
- **Compute-optimal**: the model size and token count that reach the lowest loss for a given budget.

## Problem

For a fixed compute budget, how should model size and the number of training tokens be balanced?

## How it works

The authors train a family of models across a grid of sizes and token counts. For each budget, they find the size and token count that give the lowest loss, then fit how the optimum scales. Model size and training tokens should be scaled together, so that neither is held back as the budget grows.

## Key methods

This page covers one method: a fitted, compute-matched sweep over model sizes and token counts. The scaling-law background that motivates the fit is in Kaplan et al. (2020), and the model family whose scale this question concerns is [GPT-3](../gpt-3-few-shot/index.md).

## Algorithm

1. Train more than 400 language models, from 70 million to over 16 billion parameters, on 5 to 500 billion tokens.
2. For each compute budget, find the model size and token count with the lowest loss.
3. Fit how the best size and the best token count change with the budget.
4. Apply the fitted rule: model size and training tokens should grow together, so that doubling the size means doubling the data.

## Results

- Chinchilla, with 70 billion parameters and four times more data, used the same compute as Gopher (280 billion parameters). It outperformed Gopher on a broad range of downstream evaluation tasks, with a greater than 7% improvement on MMLU over Gopher.
- Chinchilla reaches a state-of-the-art average accuracy of 67.5% on the MMLU benchmark, according to the abstract.

## Limitations

- The fit covers the range the authors trained, from 70 million to over 16 billion parameters and up to 500 billion tokens. Extending it to much larger budgets is an extrapolation.
- The result is a compute-optimal choice for training only. It does not account for the cost of serving a model after training, so a smaller model trained on more data can be preferred in practice for other reasons.
- The paper's comparisons are against specific models, Gopher and others, trained on particular data.

## Variants and more variants

- **Compute-optimal fit**: the method described here, which picks the split for a fixed budget.

## Connections

- Parent topic: [Large Language Models](../index.md)
- Other method on this topic: [GPT-3 Few-Shot Learning](../gpt-3-few-shot/index.md)
- Other method on this topic: [InstructGPT and RLHF](../instructgpt-rlhf/index.md)

## Applications

- Planning pre-training runs, where a fixed compute budget must be split between model size and data.
- Comparing published models by their token counts, to see whether a model was trained compute-optimally.

## Open questions

- How well does the fitted rule hold for model sizes and data sizes beyond the paper's range?
- How should the choice change when the cost of serving the model is included in the budget?

## References

### Seminal papers

- Hoffmann, J., et al. (2022). *Training Compute-Optimal Large Language Models*. arXiv. https://arxiv.org/abs/2203.15556 — The Chinchilla study, arguing that model size and training tokens should grow together for a fixed compute budget, with the 400-model sweep and the 67.5% MMLU result.
- Kaplan, J., et al. (2020). *Scaling Laws for Neural Language Models*. arXiv. https://arxiv.org/abs/2001.08361 — Shows that loss scales as a power law with model size, dataset size and compute, the background for fitting a compute-optimal split.
- Brown, T. B., et al. (2020). *Language Models are Few-Shot Learners*. arXiv. https://arxiv.org/abs/2005.14165 — The GPT-3 paper, the 175-billion-parameter model family that this page's scale question concerns.
- Ouyang, L., et al. (2022). *Training language models to follow instructions with human feedback*. arXiv. https://arxiv.org/abs/2203.02155 — InstructGPT, which aligns language models with user intent through fine-tuning on human feedback.

### Surveys and textbooks

- Zhao, W. X., et al. (2023). *A Survey of Large Language Models*. arXiv. https://arxiv.org/abs/2303.18223 — A broad survey of pre-training, adaptation and evaluation of LLMs, with a timeline of models.

## Further learning

- Hugging Face. *LLM Course*. https://huggingface.co/learn/llm-course — Hands-on course on using, fine-tuning and building LLMs with the Hugging Face libraries.
- Karpathy, A. (2023). *[1hr Talk] Intro to Large Language Models*. YouTube. https://www.youtube.com/watch?v=zjkBMFhNj_g — A one-hour non-technical overview of how LLMs are trained, what they can do and where they fail.
