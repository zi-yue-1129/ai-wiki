---
status: complete
last_reviewed: 2026-10-28
related:
  - theory/deep-learning
  - engineering/training
tags:
  - optimization
  - distributed training
  - natural gradient
aliases:
  - Distributed K-FAC
  - Large-scale K-FAC
  - 分散式 K-FAC
---

# Distributed K-FAC

Distributed K-FAC runs [K-FAC](index.md) across many accelerators, so that the Kronecker factors and their inverses are computed in parallel and shared between processes. Osawa et al. (2019) describe a large-scale version for convolutional networks. They train ResNet-50 on ImageNet with K-FAC on up to 1,024 GPUs, in about 10 minutes. The method targets large mini-batch training, where first-order methods lose accuracy unless their schedules are carefully tuned.

## Problem

Large-batch SGD speeds up training only up to a point. When the mini-batch size grows beyond a certain value, validation accuracy starts to degrade. The standard remedy, from Goyal et al. (2017), scales the learning rate with the mini-batch size and warms it up over the first epochs. Second-order methods such as K-FAC need fewer steps, but their factor computations are expensive, so they must be distributed to be competitive in wall-clock time.

## Core idea

The factor computation and inversion are spread across processes, and the results are combined with collective communication over MPI and NCCL. The design aims to minimise the overhead of computing the Kronecker factors. The paper also examines how stale the factors can be before performance suffers. For batch normalisation layers, the paper does not factorise the Fisher into $A$ and $G$, and it keeps only the diagonal.

## Equation or algorithm

The update applied to each layer is the K-FAC preconditioned gradient, as described on the [K-FAC](index.md) page. The distributed scheme changes how the factors are computed, combined and refreshed. It does not change the form of the update.

## Results

The paper trains ResNet-50 on ImageNet with K-FAC at mini-batch sizes from 4,096 to 32,768. The reported top-1 single-crop validation accuracy is 75.1% to 75.3%, reached in 35 to 45 epochs. The headline result is that ResNet-50 on ImageNet trains in 10 minutes to 74.9% top-1 accuracy on 1,024 Tesla V100 GPUs. The paper's Table 2 places this against published large-batch ImageNet runs.

## Limitations

- The headline results are for ResNet-50 on ImageNet, so the speed claims are specific to that setting.
- The method needs a large GPU cluster with a fast interconnect, and its speed depends on the communication design.
- The factors are stale between refreshes. How much staleness is tolerable depends on the model and the batch size.
- The method inherits the Kronecker approximation's assumptions, and batch normalisation layers use a diagonal rather than a Kronecker factorisation.

## Key methods

- [Large-batch and distributed training](../large-batch-and-distributed.md) covers the first-order large-batch recipes that this method is compared against.
- [K-FAC](index.md) is the single-process method whose factors are computed here in parallel.
- [KFC](kfc.md) is the Kronecker factorisation for convolution layers, the setting of this paper.

## Open issues and related variants

- **Staleness.** How much stale curvature can be tolerated, and how that depends on the model and batch size, needs more study.
- **Fair comparison.** Comparing second-order methods with tuned first-order methods under the same compute budget is an open methodological question.

## Connections

- [Deep learning](../../deep-learning/index.md) describes the back-propagation that supplies the derivatives used in the factors.
- [Training](../../../engineering/training/index.md) covers the systems side of large-scale training.

## References

### Seminal papers

- Osawa, K., Tsuji, Y., Ueno, Y., Naruse, A., Yokota, R. & Matsuoka, S. (2019). *Large-Scale Distributed Second-Order Optimization Using Kronecker-Factored Approximate Curvature for Deep Convolutional Neural Networks*. IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR). https://doi.org/10.1109/cvpr.2019.01264 — Distributes K-FAC across GPUs and trains ResNet-50 on ImageNet in 10 minutes.
- Goyal, P., et al. (2017). *Accurate, Large Minibatch SGD: Training ImageNet in 1 Hour*. arXiv:1706.02677. https://arxiv.org/abs/1706.02677 — The large-batch SGD recipe with learning-rate scaling and warm-up that this work is compared against.
- Grosse, R. & Martens, J. (2016). *A Kronecker-factored approximate Fisher matrix for convolution layers*. ICML, PMLR 48:573–582. https://proceedings.mlr.press/v48/grosse16.html — The Kronecker factorisation for convolution layers used in the convolutional setting.
- Martens, J. & Grosse, R. (2015). *Optimizing Neural Networks with Kronecker-factored Approximate Curvature*. arXiv:1503.05671. https://arxiv.org/abs/1503.05671 — Introduces the K-FAC method that is distributed here.

### Surveys and textbooks

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). *Optimization Methods for Large-Scale Machine Learning*. arXiv:1606.04838. https://arxiv.org/abs/1606.04838 — Survey of large-scale optimisers, including the trade-offs in distributed training.
