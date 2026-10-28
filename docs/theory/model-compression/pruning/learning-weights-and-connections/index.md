---
status: draft
last_reviewed: 2026-10-28
tags:
- model compression
- sparsity
- pruning
aliases:
  - Learning both weights and connections
  - Han et al. 2015
  - 學習權重與連接
---

# Learning Both Weights and Connections

Learning both weights and connections is the 2015 pruning method that showed a large network could lose most of its parameters after training, then regain its accuracy with retraining. It is the origin of the prune-and-retrain pipeline used across the [pruning](../index.md) family, and it sets the baseline that later methods such as [magnitude pruning](../magnitude-pruning/index.md) and [N:M sparsity](../n-m-sparsity/index.md) are compared against.

## Problem

Large networks, such as AlexNet for image classification, contain far more parameters than they need. Storing them is expensive on mobile systems, where memory and bandwidth are limited.

## Core idea

Train the network to learn which connections matter, prune the weak ones, and retrain. The pruned network keeps its accuracy while having far fewer connections.

## Equation or algorithm

Weights whose magnitude is below a threshold are set to zero and held there with a mask. The network is then retrained on the remaining weights. The threshold is raised over several rounds, with retraining between them, until the target sparsity is reached.

## Results

The abstract reports that the method reduced the number of parameters of AlexNet by a factor of 9, from 61 million to 6.7 million, without loss of accuracy.

## Limitations

Retraining costs about as much as training. The unstructured result needs sparse software or hardware to run faster. The method was developed for convolutional networks, before large transformers.

## Open issues and related variants

- **Iterative cost.** Repeated pruning and retraining is expensive, which is why one-shot and gradual methods were developed; see [gradual pruning](../magnitude-pruning/gradual-pruning/index.md).
- **Related:** the Deep Compression pipeline (Han et al., 2016) adds quantisation and coding after this pruning step; see [quantisation](../../quantisation/index.md).

## Connections

The unstructured masks this method produces are a poor fit for dense hardware, which is why [N:M sparsity](../n-m-sparsity/index.md) was introduced. The memory savings matter most for [mobile and edge deployment](../../../../engineering/hardware/index.md).

## References

### Seminal papers

- Han, S., Pool, J., Tran, J., Dally, W. J. (2015). *Learning both Weights and Connections for Efficient Neural Networks*. arXiv:1506.02626. https://arxiv.org/abs/1506.02626 — Shows that prune-and-retrain cuts AlexNet's parameters from 61 million to 6.7 million.
- Han, S., Mao, H., Dally, W. J. (2016). *Deep Compression: Compressing Deep Neural Networks with Pruning, Trained Quantization and Huffman Coding*. ICLR. https://arxiv.org/abs/1510.00149 — Adds quantisation and coding to pruning, for a combined reduction of 35 to 49 times.
- Frankle, J., Carbin, M. (2018). *The Lottery Ticket Hypothesis: Finding Sparse, Trainable Neural Networks*. arXiv:1803.03635. https://arxiv.org/abs/1803.03635 — Shows that the pruned subnetworks can be trained from their original initial weights.
- Zhu, M., Gupta, S. (2017). *To prune, or not to prune: exploring the efficacy of pruning for model compression*. arXiv:1710.01878. https://arxiv.org/abs/1710.01878 — Compares pruned large networks with small dense networks at equal parameter counts.

### Surveys and textbooks

- Hoefler, T., et al. (2021). *Sparsity in Deep Learning: Pruning and Growth for Efficient Inference and Training in Neural Networks*. arXiv:2102.00554. https://arxiv.org/abs/2102.00554 — A broad survey of sparsity methods across training and inference.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Gale, T., Elsen, E., Hooker, S. (2019). *The State of Sparsity in Deep Neural Networks*. arXiv:1902.09574. https://arxiv.org/abs/1902.09574 — Benchmarks sparsity methods and finds simple magnitude pruning a strong baseline.
