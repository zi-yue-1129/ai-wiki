---
status: draft
last_reviewed: 2026-10-28
tags:
- model compression
- structured pruning
- channel pruning
aliases:
  - Filter pruning
  - Pruning filters for efficient ConvNets
  - 濾波器剪枝
---

# Filter Pruning

Filter pruning removes whole convolution filters, and with them the matching input channels of the next layer, so that the network becomes a smaller dense network. Li et al. proposed ranking filters by the magnitude of their weights and pruning the smallest. It is the reference method for [structured pruning](../index.md) of convolutional networks.

## Problem

Pruning individual weights gives sparse layers that standard convolution libraries cannot accelerate. A pruning scheme that gives smaller dense layers was needed.

## Core idea

Rank the filters of each convolution by the magnitude of their weights, remove the smallest, and retrain. The paper also analyses which layers are sensitive to pruning and prunes those less.

## Equation or algorithm

The importance of filter \(j\) is the \(\ell_1\) norm of its weights. Removing filter \(j\) also removes input channel \(j\) of the following layer. The network is retrained after each round of removal, and layers are pruned by different amounts according to their sensitivity.

## Results

The abstract reports that inference cost for VGG-16 is reduced by up to 34% and for ResNet-110 by up to 38% on CIFAR-10.

## Limitations

The reduction is in computation, and the saving in memory is smaller. The importance measure ignores how removing a filter affects later layers, beyond what retraining recovers.

## Open issues and related variants

- **Better scores.** Scores that measure the loss effect of a removal are more accurate than norms, but they cost more to compute.
- **Related:** [network slimming](../network-slimming/index.md) uses the scaling factors of batch normalisation as the score instead.

## Connections

Filter pruning gives the dense matrices that [AI accelerators](../../../../../engineering/hardware/index.md) run well, which is why it is common in deployment. The contrast with unstructured pruning is set out in [learning both weights and connections](../../learning-weights-and-connections/index.md).

## References

### Seminal papers

- Li, H., Kadav, A., Durdanovic, I., Samet, H., Graf, H. P. (2016). *Pruning Filters for Efficient ConvNets*. arXiv:1608.08710. https://arxiv.org/abs/1608.08710 — Filter pruning that reduces VGG-16 inference cost by up to 34% on CIFAR-10.
- Liu, Z., et al. (2017). *Learning Efficient Convolutional Networks through Network Slimming*. arXiv:1708.06519. https://arxiv.org/abs/1708.06519 — Channel selection with an \(\ell_1\) penalty on batch-normalisation scales.
- Han, S., Pool, J., Tran, J., Dally, W. J. (2015). *Learning both Weights and Connections for Efficient Neural Networks*. arXiv:1506.02626. https://arxiv.org/abs/1506.02626 — Unstructured pruning, the contrast that structured methods are measured against.

### Surveys and textbooks

- Hoefler, T., et al. (2021). *Sparsity in Deep Learning: Pruning and Growth for Efficient Inference and Training in Neural Networks*. arXiv:2102.00554. https://arxiv.org/abs/2102.00554 — Compares structured and unstructured sparsity across training and inference.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Gale, T., Elsen, E., Hooker, S. (2019). *The State of Sparsity in Deep Neural Networks*. arXiv:1902.09574. https://arxiv.org/abs/1902.09574 — Benchmarks sparsity methods, including structured ones.
