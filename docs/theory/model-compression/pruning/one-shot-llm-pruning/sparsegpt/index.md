---
status: complete
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

SparseGPT is a one-shot pruning method for large GPT-family models. It removes weights layer by layer and updates the remaining weights to compensate, using approximate second-order information about the layer's reconstruction error. It reaches high unstructured sparsity without retraining. It is the pruning counterpart of [GPTQ](../../../quantisation/post-training/gptq/index.md), which uses the same framework for rounding.

## Problem

Iterative pruning and retraining are too expensive for models with billions of parameters. Simple magnitude pruning fails at high sparsity in these models, because removing a weight without correcting the others loses too much of the layer's output.

## Core idea

Prune each layer in one shot, choosing which weights to remove and updating the remaining weights so that the layer's output stays close to the original. The choice and the update both come from the reconstruction error, approximated with second-order information from a small calibration set.

## Equation or algorithm

For a layer with weights \(W\) and calibration inputs \(X\), the method seeks a sparse \(\hat{W}\) that keeps the layer output close to the original, approximately minimising

\[
\lVert WX - \hat{W}X \rVert_2^2
\]

over the mask and the updated weights. The solver uses an approximate inverse Hessian of the reconstruction error, computed from the calibration inputs, and the remaining weights are updated to compensate for the removed ones.

## Results

The paper reports that the method can prune large GPT-family models in one shot, without retraining, to at least 50% sparsity. The abstract states that it reaches 60% unstructured sparsity with negligible increase in perplexity. The largest open models it is evaluated on are OPT-175B and BLOOM-176B.

## Limitations

Unstructured sparsity needs sparse kernels to give speed-ups on common hardware. The method needs calibration data and an approximate second-order solver, which adds engineering complexity, and the paper's results are for the GPT family, not for every architecture.

## Open issues and related variants

- **Structured variants.** Extending the reconstruction framework to whole heads or channels is not covered by the original method.
- **Related:** [Wanda](../wanda/index.md) uses a simpler score with no weight update, and reports results competitive with SparseGPT on LLaMA models.

## Connections

SparseGPT and [GPTQ](../../../quantisation/post-training/gptq/index.md) share the same curvature-based framework, one for removal and one for rounding. The unstructured result needs the sparse formats discussed in [AI hardware](../../../../../engineering/hardware/index.md) to run faster.

## References

### Seminal papers

- Frantar, E., Alistarh, D. (2023). *SparseGPT: Massive Language Models Can Be Accurately Pruned in One-Shot*. arXiv:2301.00774. https://arxiv.org/abs/2301.00774 — One-shot pruning with weight reconstruction, reaching 60% unstructured sparsity with negligible perplexity increase on OPT-175B and BLOOM-176B.
- Frantar, E., Ashkboos, S., Hoefler, T., Alistarh, D. (2022). *GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers*. arXiv:2210.17323. https://arxiv.org/abs/2210.17323 — The rounding counterpart that uses the same approximate second-order framework.
- Sun, M., Liu, Z., Bair, A., Kolter, J. Z. (2023). *A Simple and Effective Pruning Approach for Large Language Models*. arXiv:2306.11695. https://arxiv.org/abs/2306.11695 — A simpler one-shot score, without weight correction, for comparison.

### Surveys and textbooks

- Hoefler, T., Alistarh, D., Ben-Nun, T., Dryden, N., Peste, A. (2021). *Sparsity in Deep Learning: Pruning and Growth for Efficient Inference and Training in Neural Networks*. arXiv:2102.00554. https://arxiv.org/abs/2102.00554 — Surveys reconstruction-based and other sparsity methods.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Gale, T., Elsen, E., Hooker, S. (2019). *The State of Sparsity in Deep Neural Networks*. arXiv:1902.09574. https://arxiv.org/abs/1902.09574 — Benchmarks the magnitude baseline that SparseGPT is measured against.
