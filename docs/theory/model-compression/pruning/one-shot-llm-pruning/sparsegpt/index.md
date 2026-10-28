---
status: draft
last_reviewed: 2026-10-28
tags:
- model compression
- sparsity
- large language models
aliases:
  - SparseGPT
  - 稀疏 GPT
---

# SparseGPT

SparseGPT is a one-shot pruning method for large GPT-family models. It removes weights layer by layer and updates the remaining weights to compensate, using an approximate inverse Hessian of the layer's reconstruction error. It reaches high unstructured sparsity without retraining. It is the pruning counterpart of [GPTQ](../../../quantisation/post-training/gptq/index.md), which uses the same framework for rounding.

## Problem

Iterative pruning and retraining are too expensive for models with billions of parameters. Simple magnitude pruning fails at high sparsity in these models, because removing a weight without correcting the others loses too much of the layer's output.

## Core idea

Prune each layer in one shot, choosing which weights to remove and updating the remaining weights so that the layer's output stays close to the original. The choice and the update both come from the reconstruction error, approximated with second-order information.

## Equation or algorithm

For a layer with inputs \(X\), the method minimises \(\lVert WX - \hat{W}X \rVert^2\) over the mask and the updated weights \(\hat{W}\). It works column by column with a blockwise update, using an approximate inverse Hessian computed from the calibration inputs. The solver runs on a small calibration set.

## Results

The abstract reports that the method can reach 60% unstructured sparsity in large GPT-family models with negligible increase in perplexity.

## Limitations

Unstructured sparsity needs sparse kernels to give speed-ups. The method needs calibration data and an approximate second-order solver, which adds engineering complexity.

## Open issues and related variants

- **Structured variants.** Extending the reconstruction framework to whole heads or channels is not covered by the original method.
- **Related:** [Wanda](../wanda/index.md) uses a simpler score with no weight update.

## Connections

SparseGPT and [GPTQ](../../../quantisation/post-training/gptq/index.md) share the same curvature-based framework, one for removal and one for rounding. The unstructured result needs the sparse formats discussed in [AI hardware](../../../../../engineering/hardware/index.md) to run faster.

## References

### Seminal papers

- Frantar, E., Alistarh, D. (2023). *SparseGPT: Massive Language Models Can Be Accurately Pruned in One-Shot*. arXiv:2301.00774. https://arxiv.org/abs/2301.00774 — One-shot pruning with weight reconstruction, reaching 60% sparsity with little perplexity increase.
- Frantar, E., et al. (2022). *GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers*. arXiv:2210.17323. https://arxiv.org/abs/2210.17323 — The rounding counterpart that uses the same second-order framework.
- Sun, M., et al. (2023). *A Simple and Effective Pruning Approach for Large Language Models*. arXiv:2306.11695. https://arxiv.org/abs/2306.11695 — A simpler one-shot score for comparison, without weight correction.

### Surveys and textbooks

- Hoefler, T., et al. (2021). *Sparsity in Deep Learning: Pruning and Growth for Efficient Inference and Training in Neural Networks*. arXiv:2102.00554. https://arxiv.org/abs/2102.00554 — Surveys reconstruction-based and other sparsity methods.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Gale, T., Elsen, E., Hooker, S. (2019). *The State of Sparsity in Deep Neural Networks*. arXiv:1902.09574. https://arxiv.org/abs/1902.09574 — Benchmarks the magnitude baseline that SparseGPT is measured against.
