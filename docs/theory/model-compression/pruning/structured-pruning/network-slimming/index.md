---
status: complete
last_reviewed: 2026-10-28
tags:
- model compression
- structured pruning
- channel pruning
aliases:
  - Network slimming
  - 網路瘦身
---

# Network Slimming

Network slimming chooses which channels to remove by using the scaling factors of batch normalisation as the importance score. A sparsity penalty is added during training, so that many scaling factors shrink towards zero. The channels with small factors are then removed and the network is fine-tuned. It is a [structured pruning](../index.md) method that needs no separate scoring pass.

## Problem

Choosing which channels to remove needs a score that is cheap to compute and reflects how much each channel matters after training. Filter norms do not always track this.

## Core idea

Add an \(\ell_1\) penalty on the batch-normalisation scaling factors during training. Many factors become small, which marks their channels as unimportant. Remove those channels globally, using one threshold across the whole network, and fine-tune the rest.

## Equation or algorithm

The training objective adds a sparsity penalty on the scale parameters \(\gamma\) of the batch-normalisation layers:

\[
\mathcal{L} = \sum_{(x,y)} \ell\big(f(x, W), y\big) + \lambda \sum_{\gamma \in \Gamma} |\gamma|
\]

Here \(\lambda\) balances the two terms. The paper chooses it by grid search over \(10^{-3}\), \(10^{-4}\) and \(10^{-5}\) on a validation set. It uses \(10^{-4}\) for VGGNet and \(10^{-5}\) for ResNet and DenseNet. The \(\ell_1\) term is not smooth, so the paper trains with subgradient descent. After training, channels are pruned by a global threshold, a percentile of all the scaling factors. In the multi-pass VGGNet experiments on CIFAR, at most half of the channels in any layer may be pruned, so that no layer is removed entirely. The remaining network is then fine-tuned.

## Results

The abstract reports that a multi-pass version of network slimming gives a 20 times reduction in VGGNet's model size and a 5 times reduction in its computing operations.

## Limitations

The penalty weight \(\lambda\) has to be chosen by search, and the global threshold can remove a whole layer unless a per-layer cap is added. The method depends on batch normalisation being present in the architecture, which limits it for models that do not use it.

## Open issues and related variants

- **Architectures without batch normalisation.** Whether the scaling factors remain meaningful when no batch normalisation is present is an open question.
- **Related:** [filter pruning](../filter-pruning/index.md) uses filter norms as the score instead.

## Connections

Network slimming removes whole channels, so the result runs on the dense hardware discussed in [AI hardware](../../../../../engineering/hardware/index.md). Its link to the biological case, where whole pathways are eliminated during development, is discussed in [neuroscience](../../../../../brain-mind/neuroscience/index.md).

## References

### Seminal papers

- Liu, Z., Li, J., Shen, Z., Huang, G., Yan, S., Zhang, C. (2017). *Learning Efficient Convolutional Networks through Network Slimming*. arXiv:1708.06519. https://arxiv.org/abs/1708.06519 — Uses an \(\ell_1\) penalty on batch-normalisation scales to choose channels; a 20 times smaller VGGNet with the multi-pass version.
- Li, H., Kadav, A., Durdanovic, I., Samet, H., Graf, H. P. (2016). *Pruning Filters for Efficient ConvNets*. arXiv:1608.08710. https://arxiv.org/abs/1608.08710 — The filter-norm alternative to the batch-normalisation score.
- Han, S., Pool, J., Tran, J., Dally, W. J. (2015). *Learning both Weights and Connections for Efficient Neural Networks*. arXiv:1506.02626. https://arxiv.org/abs/1506.02626 — The unstructured baseline that channel removal is compared against.

### Surveys and textbooks

- Hoefler, T., Alistarh, D., Ben-Nun, T., Dryden, N., Peste, A. (2021). *Sparsity in Deep Learning: Pruning and Growth for Efficient Inference and Training in Neural Networks*. arXiv:2102.00554. https://arxiv.org/abs/2102.00554 — Compares channel-level and weight-level sparsity across training and inference.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Gale, T., Elsen, E., Hooker, S. (2019). *The State of Sparsity in Deep Neural Networks*. arXiv:1902.09574. https://arxiv.org/abs/1902.09574 — Benchmarks structured and unstructured sparsity under one protocol.
