---
status: draft
last_reviewed: 2026-10-28
related:
- theory/models/cnn
- theory/models/transformer
- engineering/training
tags:
- model compression
- low-rank factorisation
- efficient architectures
aliases:
  - Low-rank factorisation
  - Efficient architectures
  - 低秩分解與高效架構
---

# Low-Rank Factorisation and Efficient Architectures

This family reduces the parameters or computation of a model without changing numerical precision and without unstructured sparsity. It has two parts: factorising large weight matrices into products of thinner ones, and choosing architectures that are small by design. Low-rank adaptation (LoRA) is covered here too, because it uses the same mathematics but does not compress the model it adapts.

## Overview

Low-rank factorisation rewrites a large weight matrix as a product of two thinner matrices, usually after training. Efficient architectures make the opposite choice: the model is designed to be small before training. The two differ in when the decision is made. Factorisation shrinks an existing model, and an efficient architecture is a different model that is trained from the start.

## Comparison of methods

| Method | When it is applied | What is reduced | Typical trade-off | Page |
| --- | --- | --- | --- | --- |
| Truncated SVD | After training | Parameters and multiply-adds of dense and convolutional layers | Error grows when the layer has high effective rank | [Truncated SVD](truncated-svd/index.md) |
| Low-rank filter expansion | After training, usually with fine-tuning | Multiply-adds of convolutional layers | Accuracy loss grows with compression, and each layer needs its own rank | [Low-rank filter expansion](low-rank-filter-expansion/index.md) |
| LoRA | During fine-tuning | Trainable parameters, not the size of the base model | Adds an update term at inference unless merged | [LoRA](lora/index.md) |
| Efficient architectures | Before training | Parameters and computation, by design | The model is fixed by its design, and accuracy depends on the design | See below |

The first two methods compress a trained model, so their results depend on how close each layer is to low rank. LoRA leaves the base model at its original size and learns only a small update. Efficient architectures avoid the question altogether by training a small model.

## Efficient architectures

Efficient architectures are covered on the Models pages, which describe how they work. This page links to them rather than repeating the material.

- **Depthwise-separable convolutions**, used by MobileNet, replace a standard convolution with a per-channel filter and a \(1 \times 1\) mixing step. See [depthwise-separable convolution](../../models/cnn/convolution-variants/depthwise-separable-convolution/index.md).
- **Shared keys and values**, in multi-query and grouped-query attention, reduce the key–value cache during decoding. See [attention variants](../../models/transformer/attention-variants/index.md) and [the KV cache](../../models/transformer/kv-cache/index.md). Grouped-query attention has its own method page in [inference optimisation](../../../engineering/inference-optimization/grouped-query-attention.md).
- **Mixture of experts** keeps the total number of parameters large while activating only a few experts for each token. See the [Mixture of experts](../../models/mixture-of-experts/index.md) page for the layer and its routing, and the [Transformer](../../models/transformer/index.md) page for where it sits.

## Trade-offs

- **Compress or design.** Compressing a trained model keeps its accuracy as a starting point but cannot make it much smaller without loss. Designing a small model can reach a better frontier, but it must be trained again.
- **Parameters versus speed.** A lower rank or a smaller architecture saves parameters, but the speed-up depends on whether the hardware runs the smaller operations efficiently.
- **Adapters versus compression.** LoRA reduces what must be trained and stored per task, not what must be served. Confusing the two leads to wrong estimates of memory use at inference.

## More variants and open issues

- **Rank selection.** Choosing the rank of each layer is usually done by search or by measuring the spectrum of the weights. A general rule is not established.
- **Factorisation with fine-tuning.** Whether a factorised model recovers accuracy better after fine-tuning than after one-shot factorisation depends on the layers, and the best recipe is empirical.
- **Efficient attention.** Whether shared keys and values hold up for very long contexts is a live question; see the open issues on the attention-variants page.

## Connections

Factorising a matrix is a way of finding its essential directions, which connects to [linear algebra](../../math/index.md) and to the spectral view of learned representations. The brain's efficiency is sometimes attributed to sparse, low-dimensional codes; see [neuroscience](../../../brain-mind/neuroscience/index.md) for the comparison.

## References

### Seminal papers

- Denton, R., Zaremba, W., Bruna, J., LeCun, Y., Fergus, R. (2014). *Exploiting Linear Structure Within Convolutional Networks for Efficient Evaluation*. arXiv:1404.0736. https://arxiv.org/abs/1404.0736 — Low-rank approximations of convolutional filters, with speed-ups of about 2 times with accuracy kept within 1%.
- Jaderberg, M., Vedaldi, A., Zisserman, A. (2014). *Speeding up Convolutional Neural Networks with Low Rank Expansions*. arXiv:1405.3866. https://arxiv.org/abs/1405.3866 — Low-rank filter expansions for convolutional layers, with up to 4.5 times speed-up on a text recognition network.
- Hu, E. J., et al. (2021). *LoRA: Low-Rank Adaptation of Large Language Models*. arXiv:2106.09685. https://arxiv.org/abs/2106.09685 — Trains low-rank updates on frozen weights, reducing trainable parameters by up to 10,000 times for GPT-3 175B.
- Howard, A. G., et al. (2017). *MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications*. arXiv:1704.04861. https://arxiv.org/abs/1704.04861 — Depthwise-separable convolutions for small, fast vision models, with a width and resolution multiplier to trade latency for accuracy.
- Shazeer, N., et al. (2017). *Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer*. arXiv:1701.06538. https://arxiv.org/abs/1701.06538 — Sparsely gated experts that raise capacity by more than 1000 times at small efficiency cost.

### Surveys and textbooks

- Hoefler, T., et al. (2021). *Sparsity in Deep Learning: Pruning and Growth for Efficient Inference and Training in Neural Networks*. arXiv:2102.00554. https://arxiv.org/abs/2102.00554 — A broad survey of efficient architectures and sparsity methods across training and inference.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Ainslie, J., et al. (2023). *GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints*. arXiv:2305.13245. https://arxiv.org/abs/2305.13245 — Grouped-query attention, with quality close to multi-head attention at the speed of multi-query attention.
