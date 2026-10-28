---
status: draft
last_reviewed: 2026-10-28
tags:
- model compression
- sparsity
- large language models
aliases:
  - One-shot pruning
  - LLM pruning
  - 大型語言模型一次剪枝
---

# One-Shot Pruning of Large Language Models

One-shot pruning removes a large fraction of the weights of a trained language model in a single pass per layer, with no retraining. Iterative pruning with retraining is too expensive for models with billions of parameters, so one-shot methods choose the weights to remove from a small calibration set and adjust the remaining weights, or not, in a single step. The two main methods are [SparseGPT](sparsegpt/index.md), which updates the remaining weights, and [Wanda](wanda/index.md), which does not.

## Overview

Both methods work layer by layer. For each linear layer, they score or select weights using calibration inputs, remove the chosen fraction, and move on. The difference is whether the surviving weights are corrected to compensate for the removal. SparseGPT corrects them with an approximate second-order solver. Wanda uses a score that is cheap to compute and corrects nothing.

## Comparison of methods

| Method | Removes weights by | Corrects remaining weights | Cost | Page |
| --- | --- | --- | --- | --- |
| SparseGPT | Second-order reconstruction error | Yes, blockwise update | Higher, one solver per layer | [SparseGPT](sparsegpt/index.md) |
| Wanda | Weight magnitude times input activation norm | No | Low, one pass over calibration inputs | [Wanda](wanda/index.md) |

Wanda is the simpler choice when calibration time or engineering effort matters most. SparseGPT is the choice when accuracy at high sparsity matters, because the correction keeps more of the output.

## Key concepts

- **Calibration set.** A small sample of inputs, used to measure the activations that each weight multiplies.
- **Unstructured sparsity.** Individual weights are removed, so the speed-up needs sparse kernels; see [N:M sparsity](../n-m-sparsity/index.md) for a pattern that hardware can skip.
- **Layer-wise objective.** The error in a layer's output, \(\lVert WX - \hat{W}X \rVert^2\), rather than the error in the weights.

## Trade-offs

- **Accuracy versus cost.** SparseGPT is more accurate at high sparsity and costs more calibration time.
- **Hardware support.** Unstructured sparsity needs sparse kernels to be fast; without them, the saving is only in storage.
- **Combination with quantisation.** The same second-order framework is used by [GPTQ](../../quantisation/post-training/gptq/index.md) for rounding, so the two can share code.

## Open issues

- **Reasoning and long context.** The effect of one-shot pruning on multi-step reasoning is less studied than perplexity.
- **Beyond perplexity.** Evaluation of pruned models on instruction following and safety is still limited.
- **Structured one-shot methods.** Removing whole heads or channels in one shot at comparable accuracy remains an open engineering problem.

## Connections

One-shot pruning sits between the iterative methods in [learning both weights and connections](../learning-weights-and-connections/index.md) and the post-training quantisation in [quantisation](../../quantisation/index.md). The sparse formats it produces depend on the [AI hardware](../../../../engineering/hardware/index.md) that will run them.

## References

### Seminal papers

- Frantar, E., Alistarh, D. (2023). *SparseGPT: Massive Language Models Can Be Accurately Pruned in One-Shot*. arXiv:2301.00774. https://arxiv.org/abs/2301.00774 — One-shot pruning with weight reconstruction, reaching 60% sparsity with little perplexity increase.
- Sun, M., et al. (2023). *A Simple and Effective Pruning Approach for Large Language Models*. arXiv:2306.11695. https://arxiv.org/abs/2306.11695 — Wanda, a magnitude-times-activation score that needs no retraining or weight update.
- Han, S., Pool, J., Tran, J., Dally, W. J. (2015). *Learning both Weights and Connections for Efficient Neural Networks*. arXiv:1506.02626. https://arxiv.org/abs/1506.02626 — The iterative pruning that one-shot methods replace for large models.

### Surveys and textbooks

- Hoefler, T., et al. (2021). *Sparsity in Deep Learning: Pruning and Growth for Efficient Inference and Training in Neural Networks*. arXiv:2102.00554. https://arxiv.org/abs/2102.00554 — Surveys sparsity methods, including their cost and hardware trade-offs.
- Gale, T., Elsen, E., Hooker, S. (2019). *The State of Sparsity in Deep Neural Networks*. arXiv:1902.09574. https://arxiv.org/abs/1902.09574 — Benchmarks magnitude pruning, which one-shot LLM methods are compared against.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Frantar, E., et al. (2022). *GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers*. arXiv:2210.17323. https://arxiv.org/abs/2210.17323 — The quantisation method that shares the second-order framework of SparseGPT.
