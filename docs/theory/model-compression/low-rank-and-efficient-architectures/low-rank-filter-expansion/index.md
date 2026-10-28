---
status: complete
last_reviewed: 2026-10-28
tags:
- model compression
- low-rank factorisation
- convolutional networks
aliases:
  - Low-rank filter expansion
  - Low-rank expansions
  - 低秩濾波器展開
---

# Low-Rank Filter Expansion

Low-rank filter expansion approximates each convolutional filter as a combination of a few separable filters. Jaderberg et al. showed that a standard convolution can be replaced by a sequence of cheaper filters, learned with a low-rank constraint, and reported a possible 2.5 times speed-up with no loss in accuracy on a scene text recognition network. It is a [low-rank factorisation](../index.md) method, and an alternative to the single SVD of [truncated SVD](../truncated-svd/index.md).

## Problem

A standard convolution with a \(k \times k\) filter over many channels is expensive, and most of its filters are highly redundant. Decomposing each filter exactly is not possible in general, so an approximation that keeps the accuracy is needed.

## Core idea

Express the filters of a layer in a low-rank basis of separable filters, that is, filters that factor into a vertical and a horizontal part. The original convolution is then computed as a sequence of cheaper convolutions. The coefficients are chosen to approximate the trained filters, and the network is fine-tuned to recover accuracy.

## Equation or algorithm

A \(k \times k\) filter is approximated by a sum of \(r\) separable filters, each the outer product of a vertical and a horizontal vector. The multiply-add count of the layer falls roughly in proportion to \(r\) divided by \(k\), so a small rank gives a large saving for large kernels. The rank is set per layer, and the approximation is optimised to match the original responses.

## Results

The abstract reports a possible 2.5 times speed-up with no loss in accuracy, and a 4.5 times speed-up with less than a 1% accuracy drop, on a scene text character recognition network. The results on other networks are in the paper.

## Limitations

The approximation is set per layer, and the search over ranks is costly. The gains depend on large kernels, and the separable filters lose some expressive power, which fine-tuning recovers only in part.

## Open issues and related variants

- **Layer choice.** Which layers tolerate a low rank without loss is not known in advance, and it varies between networks.
- **Related:** [truncated SVD](../truncated-svd/index.md) applies a single decomposition to a weight matrix rather than to convolutional filters.
- **Related:** [depthwise-separable convolution](../../../models/cnn/convolution-variants/depthwise-separable-convolution/index.md) is an efficient architecture that builds the same kind of saving into the design.

## Connections

Separable filters are a classical idea in image processing, and the same factorisation appears in the [convolution variants](../../../models/cnn/convolution-variants/index.md) of convolutional networks. Its effect on the speed of real convolutions depends on the hardware, which is discussed under [AI hardware](../../../../engineering/hardware/index.md).

## References

### Seminal papers

- Jaderberg, M., Vedaldi, A., Zisserman, A. (2014). *Speeding up Convolutional Neural Networks with Low Rank Expansions*. arXiv:1405.3866. https://arxiv.org/abs/1405.3866 — Low-rank filter expansions with a possible 2.5 times speed-up and no loss in accuracy on a text recognition network.
- Denton, R., Zaremba, W., Bruna, J., LeCun, Y., Fergus, R. (2014). *Exploiting Linear Structure Within Convolutional Networks for Efficient Evaluation*. arXiv:1404.0736. https://arxiv.org/abs/1404.0736 — Low-rank approximations of convolutional filters, the parallel result from the same year.
- Howard, A. G., et al. (2017). *MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications*. arXiv:1704.04861. https://arxiv.org/abs/1704.04861 — Depthwise-separable convolutions, a design that builds in the same kind of saving.

### Surveys and textbooks

- Hoefler, T., et al. (2021). *Sparsity in Deep Learning: Pruning and Growth for Efficient Inference and Training in Neural Networks*. arXiv:2102.00554. https://arxiv.org/abs/2102.00554 — Surveys efficiency methods, including the factorisation of convolutional layers.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Hu, E. J., et al. (2021). *LoRA: Low-Rank Adaptation of Large Language Models*. arXiv:2106.09685. https://arxiv.org/abs/2106.09685 — A low-rank update used for fine-tuning, a related use of the same structure.
