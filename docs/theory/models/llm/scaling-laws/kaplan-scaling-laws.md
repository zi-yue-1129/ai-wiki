---
status: complete
last_reviewed: 2026-10-28
related:
  - theory/models/llm/scaling-laws
tags:
  - scaling laws
  - power laws
  - language models
aliases:
  - Kaplan scaling laws
  - Scaling laws for neural language models
  - Kaplan 縮放定律
---

# Kaplan scaling laws (Kaplan et al., 2020)

Kaplan et al. measured the held-out cross-entropy loss of Transformer language models across a range of model sizes, dataset sizes and training compute, and found that each follows a power law. The paper also gave a rule for splitting a fixed compute budget between model size and training data. Part of [Scaling laws](index.md).

## Overview

Before this work, the size of language models was often chosen by intuition. Kaplan et al. (2020) trained many models, varied one quantity at a time, and fitted simple equations to the loss. The trends were smooth, and the authors reported that the power laws held across more than seven orders of magnitude of compute.

## Key concepts

- **Non-embedding parameters** \(N\): the parameters outside the token-embedding table, the quantity the paper uses as model size.
- **Dataset size** \(D\): the number of training tokens, counted with the tokeniser used in training.
- **Compute** \(C\): the training operations, which the paper estimates from \(N\) and the number of tokens processed.
- **Critical scales** \(N_c\), \(D_c\), \(C_c\): fitted constants that set the units of each power law.

## Problem

When one of \(N\), \(D\) or \(C\) is not the bottleneck, how does the loss depend on the remaining quantity, and how should a fixed budget be allocated?

## How it works

The loss depends on size and data through a single combined equation,

\[
L(N, D) = \left[\left(\frac{N_c}{N}\right)^{\alpha_N/\alpha_D} + \frac{D_c}{D}\right]^{\alpha_D},
\]

which reduces to a pure power law in \(N\) when data is abundant, and to a pure power law in \(D\) when the model is large. Here \(\alpha_N\) and \(\alpha_D\) are fitted exponents. Each exponent is small, so each large factor in parameters or data buys a modest but predictable drop in loss.

The compute-optimal allocation follows from the same fits. The paper trains each model to a fixed compute budget \(C\), and finds the \(N\) that gives the lowest loss for that budget. The fitted optimum grows faster with \(C\) for \(N\) than for \(D\).

## Key methods

This page covers one method: fitting power laws to held-out loss over a grid of model sizes, data sizes and compute, with a single combined equation for size and data.

- **Training runs**: a grid of Transformer language models trained on WebText2, the paper's text corpus, with learning rates and schedules held in fixed ranges.
- **Fit**: the loss is fitted against each quantity in turn, then against the combined equation above.
- **Allocation**: the compute-optimal model size is read from the fit for each budget.

## Variants

- **Parameter-limited** training, where data is abundant and the loss is fitted against \(N\) alone.
- **Data-limited** training, where a fixed dataset is repeated and the loss is fitted against \(D\) alone. The paper notes overfitting in this regime.
- **Compute-limited** training, where the best run for a budget is trained with the optimal \(N\) and stopped before convergence.

## Results and limits

- Test loss follows power laws in \(N\), \(D\) and \(C\) over the ranges studied, and the paper reports that architectural details such as width and depth have a smaller effect within a wide range (Kaplan et al., 2020).
- The paper concludes that the best use of extra compute favours a larger model trained on a modest amount of data, stopped before convergence. Hoffmann et al. (2022) later found that this allocation trains models on too little data, and proposed a different split.
- The fitted exponents depend on the training setup, including the data and the learning-rate schedule, so they describe this setup as well as language models in general.
- The results are for language modelling loss on one corpus. They do not directly predict downstream task accuracy.

## Applications

- **Planning**: predicting the loss of a large run from smaller runs before the budget is committed.
- **Comparing architectures**: checking whether a change to a model shifts the loss curve or only moves it along the same curve.
- **Motivating the compute-optimal line of work**: the disagreement with the later fits is itself a useful result for choosing a budget.

## Open questions

- Are the exponents universal across corpora, tokenisers and architectures, or only properties of this setup?
- How well does the power-law form hold beyond the range of model sizes the paper measured?

## Connections

- Parent topic: [Scaling laws](index.md)
- Revised split: [Compute-optimal training](../compute-optimal-training/index.md)
- Model family in the same period: [GPT-3 few-shot learning](../gpt-3-few-shot/index.md)

## References

### Seminal papers

- Kaplan, J. et al. (2020). Scaling Laws for Neural Language Models. arXiv:2001.08361. https://arxiv.org/abs/2001.08361 — Fits power laws of loss against model size, data and compute, and gives the allocation rule.
- Hoffmann, J. et al. (2022). Training Compute-Optimal Large Language Models. arXiv:2203.15556. https://arxiv.org/abs/2203.15556 — Revises the allocation by fitting more carefully and training more models on more data.
- Hestness, J. et al. (2017). Deep Learning Scaling is Predictable, Empirically. arXiv:1712.00409. https://arxiv.org/abs/1712.00409 — Earlier evidence of power-law improvement with data across deep-learning tasks.

### Surveys and textbooks

- Henighan, T. et al. (2020). Scaling Laws for Autoregressive Generative Modeling. arXiv:2010.14701. https://arxiv.org/abs/2010.14701 — Applies the same kind of fit to image, video and mathematics models.
- Wei, J. et al. (2022). Emergent Abilities of Large Language Models. *Transactions on Machine Learning Research*. arXiv:2206.07682. https://arxiv.org/abs/2206.07682 — Discusses which abilities appear abruptly with scale, and how the question of scaling relates to them.
- Brown, T. B. et al. (2020). Language Models are Few-Shot Learners. arXiv:2005.14165. https://arxiv.org/abs/2005.14165 — A model family trained at the scale that the fits extrapolate to.
