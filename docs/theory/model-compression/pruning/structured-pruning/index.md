---
status: draft
last_reviewed: 2026-10-28
tags:
- model compression
- structured pruning
- channel pruning
aliases:
  - Structured pruning
  - Channel pruning
  - Filter pruning
  - 結構化剪枝
  - 通道剪枝
---

# Structured and Channel Pruning

Structured pruning removes whole units, such as filters, channels, neurons, attention heads or blocks, rather than individual weights. The result is a smaller dense network, which ordinary hardware runs faster without special sparse kernels. This is why structured pruning is the usual choice when speed on standard accelerators matters more than the highest sparsity.

## Overview

A convolutional layer with \(C\) output channels can lose a channel together with its filter and the matching input channel of the next layer. A transformer can lose attention heads or feed-forward neurons in the same way. The method has two parts: a score that ranks the units by importance, and a rule for removing the lowest-ranked units while keeping the network consistent.

## Key concepts

- **Filter and channel pruning.** Removing a convolution's output channel, which also removes the corresponding input channel of the next layer.
- **Importance scores.** Common choices are the norm of a filter, the scaling factor of batch normalisation, or the change in loss from removing the unit.
- **Speed-up versus compression.** Removing channels reduces both parameters and computation, but the fraction of each depends on where the channels are removed.
- **Consistency.** The network must still be well defined after removal, which constrains which channels can be dropped together, such as residual connections.

## Key methods

### Pruning Filters for Efficient ConvNets (Li et al., 2016)

- **Problem:** Pruning individual weights gives sparse layers that standard convolution libraries cannot accelerate. A pruning scheme that gives smaller dense layers was needed.
- **Core idea:** Rank the filters of each convolution by the magnitude of their weights, remove the smallest, and retrain. The paper analyses which layers are sensitive and prunes them less.
- **Equation or algorithm:** Filter importance is the \(\ell_1\) norm of the filter weights. Removing filter \(j\) also removes the input channel \(j\) of the following layer, and the network is retrained after each round of removal.
- **Results:** The abstract reports that inference cost for VGG-16 is reduced by up to 34% and for ResNet-110 by up to 38% on CIFAR-10.
- **Limitations:** The reduction is in computation, and the saving in memory is smaller. The importance measure ignores how removing a filter affects the layers after it, beyond the retraining.

### Learning Efficient Convolutional Networks through Network Slimming (Liu et al., 2017)

- **Problem:** Choosing which channels to remove needs a score that is cheap to compute and reflects how much each channel matters after training.
- **Core idea:** Add an \(\ell_1\) penalty on the scaling factors of batch normalisation during training, so that many factors become small, then remove the channels with small factors and fine-tune.
- **Equation or algorithm:** The training loss includes a penalty \(\lambda \sum_\gamma |\gamma|\) on batch-normalisation scale parameters \(\gamma\). Channels with small \(\gamma\) are removed and the remaining network is fine-tuned.
- **Results:** For VGGNet, the abstract reports a 20 times reduction in model size and a 5 times reduction in computing operations with the multi-pass version of the method.
- **Limitations:** The penalty is set by hand, and the method depends on batch normalisation being present in the architecture.

## Trade-offs

- **Speed on standard hardware versus sparsity.** Structured pruning gives real speed-ups on dense accelerators, but it removes coarser units and usually reaches lower sparsity at the same accuracy than unstructured pruning.
- **Scoring cost.** Cheap scores such as norms are less accurate than scores that measure the loss effect.
- **Architecture dependence.** Residual connections and attention heads need rules that keep the network valid, so the method differs across architectures.

## More variants and open issues

- **Variant:** [N:M sparsity](../n-m-sparsity/index.md), a fine-grained pattern that sits between unstructured and structured pruning.
- **Open issue:** how to prune attention heads and feed-forward neurons in large transformers without retraining at full cost.
- **Open issue:** whether scores such as batch-normalisation factors remain meaningful for architectures without batch normalisation.

## Connections

Structured pruning is the form of pruning that matches the dense matrix units of [AI accelerators](../../../../engineering/hardware/index.md), which is why it is common in deployment. Its link to the biological case, where whole pathways are eliminated during development, is discussed in [neuroscience](../../../../brain-mind/neuroscience/index.md).

## References

### Seminal papers

- Li, H., Kadav, A., Durdanovic, I., Samet, H., Graf, H. P. (2016). *Pruning Filters for Efficient ConvNets*. arXiv:1608.08710. https://arxiv.org/abs/1608.08710 — Filter pruning that reduces VGG-16 inference cost by up to 34% on CIFAR-10.
- Liu, Z., et al. (2017). *Learning Efficient Convolutional Networks through Network Slimming*. arXiv:1708.06519. https://arxiv.org/abs/1708.06519 — Batch-normalisation scale factors with an \(\ell_1\) penalty to choose channels to remove.
- Han, S., Pool, J., Tran, J., Dally, W. J. (2015). *Learning both Weights and Connections for Efficient Neural Networks*. arXiv:1506.02626. https://arxiv.org/abs/1506.02626 — Unstructured pruning, the contrast that structured methods are measured against.

### Surveys and textbooks

- Hoefler, T., et al. (2021). *Sparsity in Deep Learning: Pruning and Growth for Efficient Inference and Training in Neural Networks*. arXiv:2102.00554. https://arxiv.org/abs/2102.00554 — Compares structured and unstructured sparsity across training and inference.
- Gale, T., Elsen, E., Hooker, S. (2019). *The State of Sparsity in Deep Neural Networks*. arXiv:1902.09574. https://arxiv.org/abs/1902.09574 — Benchmarks sparsity methods, including structured ones.

### Lectures and videos

(none checked for this page)

### Articles and documentation

(none checked for this page)
