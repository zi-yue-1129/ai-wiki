---
status: draft
last_reviewed: 2026-10-28
related:
- engineering/hardware
- brain-mind/neuroscience
tags:
- model compression
- sparsity
- pruning
aliases:
  - Pruning
  - Network Pruning
  - Sparsity
  - 剪枝
  - 網路剪枝
---

# Pruning

Pruning removes parts of a trained network, such as individual weights, neurons, channels or attention heads, that contribute little to its outputs. The remaining network is smaller, and if the removal is structured, it can also be faster. Pruning is one of the three main families of [model compression](../index.md), alongside [quantisation](../quantisation/index.md) and [knowledge distillation](../knowledge-distillation/index.md).

## Overview

A pruned model is described by a **mask**: a binary value for every weight that says whether the weight is kept. Three choices define a pruning method:

- **Granularity.** Unstructured pruning removes single weights, which gives the most freedom but leaves irregular sparsity. Structured pruning removes whole rows, channels, heads or blocks, which leaves a smaller dense matrix that ordinary hardware runs faster.
- **Scoring.** A rule decides which parts are least important. Magnitude is the simplest; others use gradients, Hessian approximations or the activations that a weight multiplies.
- **Schedule.** One-shot pruning removes a fraction in a single step. Iterative pruning alternates removal with retraining, which usually reaches higher sparsity at the same accuracy but costs more compute.

## Key concepts

- **Sparsity**: the fraction of weights removed. A model with 50% sparsity keeps half its weights.
- **Magnitude pruning**: remove the weights with the smallest absolute value. It is cheap and often a strong baseline, as Gale et al. (2019) showed at large scale.
- **N:M sparsity**: a structured pattern that keeps N values in every block of M, such as 2 in every 4. NVIDIA's Ampere GPUs add Sparse Tensor Cores that run the 2:4 pattern. The authors report twice the math throughput of dense matrix units (Mishra et al., 2021).
- **Lottery ticket**: Frankle and Carbin (2018) found that a dense network contains sparse subnetworks which, reset to their original initial weights, train to comparable accuracy in isolation.
- **Global versus layer-wise**: a global threshold lets some layers be pruned more than others, which often gives better accuracy for the same total sparsity.

## How it works

The classic pipeline, from Han et al. (2015), has three steps: train a dense network normally, remove weights whose magnitude is below a threshold, then retrain the remaining weights to recover accuracy. Repeating the prune-and-retrain loop raises sparsity gradually. This pipeline needs a full training run per iteration, so it is expensive for models with billions of parameters.

Large language models changed the problem. Retraining them is costly, so recent methods prune in one shot, using only a small calibration set and a closed-form or local correction for each layer.

## Comparison of families

| Family | Granularity | Schedule | Hardware needs | Page |
| --- | --- | --- | --- | --- |
| Prune and retrain | Individual weights | Iterative | Sparse kernels for speed | [Learning weights and connections](learning-weights-and-connections/index.md) |
| Magnitude pruning | Individual weights | Gradual or one-shot | Sparse kernels for speed | [Magnitude pruning](magnitude-pruning/index.md) |
| Lottery ticket | Individual weights | Iterative with rewinding | Sparse kernels for speed | [Lottery ticket](lottery-ticket/index.md) |
| Structured pruning | Filters, channels, heads | Iterative or after training | Dense hardware, no special kernels | [Structured pruning](structured-pruning/index.md) |
| N:M sparsity | Blocks of M weights | Training or after training | Hardware that supports the pattern | [N:M sparsity](n-m-sparsity/index.md) |
| One-shot LLM pruning | Individual weights | One shot, no retraining | Sparse kernels for speed | [One-shot LLM pruning](one-shot-llm-pruning/index.md) |

Structured pruning and N:M sparsity are the two families that give speed-ups on common hardware without sparse kernels or with few of them. The unstructured families reach higher sparsity at the same accuracy, but they need sparse support to run faster.

## Trade-offs

- **Speed on standard hardware versus sparsity.** Structured pruning gives real speed-ups on dense accelerators, but it removes coarser units and usually reaches lower sparsity at the same accuracy than unstructured pruning.
- **Cost of finding the mask.** Iterative methods need repeated training, one-shot methods need only calibration, and the accuracy gap between them depends on the sparsity target.
- **Hardware lock-in.** A pattern is fast only where the hardware supports it, so the choice depends on the target device.

## Connections

Pruning and sparse computation depend on what chips can skip. The support for N:M patterns and sparse matrix kernels is part of the story in [AI hardware](../../../engineering/hardware/index.md).

For the biological side of pruning, see [neuroscience](../../../brain-mind/neuroscience/index.md).

## Applications

- **Mobile vision models** are pruned to structured sparsity so that they run on small processors.
- **Large language models** are pruned in one shot before quantisation to reduce serving cost.
- **Robotics and embedded control** use pruned networks to fit real-time budgets.

## Open questions

- **Why magnitude works.** Pruning rules are chosen empirically. A theory that predicts which weights can be removed without harm is missing.
- **Hardware for unstructured sparsity.** High unstructured sparsity saves parameters but speeds up little on current accelerators, so structured patterns are often preferred in practice.
- **Pruning during training.** Sparse training could save compute throughout the run, but stability and quality at high sparsity are not fully understood.
- **Reasoning and long context.** The effect of pruning on multi-step reasoning and retrieval is less studied than perplexity.

## References

### Seminal papers

- Han, S., Pool, J., Tran, J., Dally, W. J. (2015). *Learning both Weights and Connections for Efficient Neural Networks*. arXiv:1506.02626. https://arxiv.org/abs/1506.02626 — Shows that pruning and retraining cut AlexNet's parameters by a factor of 9, from 61 million to 6.7 million, with no loss of ImageNet accuracy.
- Frankle, J., Carbin, M. (2018). *The Lottery Ticket Hypothesis: Finding Sparse, Trainable Neural Networks*. arXiv:1803.03635. https://arxiv.org/abs/1803.03635 — Finds sparse "winning tickets" that, trained in isolation from their initial weights, reach accuracy comparable to the original network.
- Frantar, E., Alistarh, D. (2023). *SparseGPT: Massive Language Models Can Be Accurately Pruned in One-Shot*. arXiv:2301.00774. https://arxiv.org/abs/2301.00774 — Prunes GPT-family models to at least 50% sparsity in one shot, without retraining, and reports 60% sparsity with a negligible increase in perplexity.
- Sun, M., et al. (2023). *A Simple and Effective Pruning Approach for Large Language Models*. arXiv:2306.11695. https://arxiv.org/abs/2306.11695 — Wanda, a magnitude-times-activation score that needs no retraining.
- Mishra, A., et al. (2021). *Accelerating Sparse Deep Neural Networks*. arXiv:2104.08378. https://arxiv.org/abs/2104.08378 — Describes NVIDIA Ampere's Sparse Tensor Cores for the 2:4 pattern, which give twice the math throughput of dense matrix units.

### Surveys and textbooks

- Hoefler, T., et al. (2021). *Sparsity in Deep Learning: Pruning and Growth for Efficient Inference and Training in Neural Networks*. arXiv:2102.00554. https://arxiv.org/abs/2102.00554 — A broad survey of sparsity methods across training and inference.
- Gale, T., Elsen, E., Hooker, S. (2019). *The State of Sparsity in Deep Neural Networks*. arXiv:1902.09574. https://arxiv.org/abs/1902.09574 — Benchmarks sparsity methods and finds magnitude pruning a strong baseline.

### Lectures and videos

(none checked for this page)

### Articles and documentation

(none checked for this page)
