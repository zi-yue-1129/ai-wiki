---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/math
tags:
  - optimization
  - large batch
  - layer-wise adaptation
aliases:
  - LARS
  - Layer-wise adaptive rate scaling
  - 逐層自適應學習率縮放
---

# LARS

LARS (Layer-wise Adaptive Rate Scaling) gives each layer its own learning rate, scaled by the ratio of the layer's weight norm to its gradient norm. You, Gitman and Ginsburg (2017) introduced it so that convolutional networks could be trained with batch sizes of 8K and 32K without losing accuracy. The parent overview is [Gradient Clipping and Normalised Updates](gradient-clipping-and-normalisation.md).

## Overview

Linear learning-rate scaling with warm-up, as in Goyal et al. (2017), works up to a point. Beyond it, a global learning rate that is safe for early layers can diverge in others, because different layers have different ratios of gradient to weight. LARS addresses this by making the step of each layer proportional to the size of that layer's weights. A layer whose weights are small receives a small step, whatever the size of its gradient.

## Problem

The abstract states that the usual large-batch recipe, linear learning-rate scaling with warm-up, is not general enough, and that training can diverge. The authors ask whether a per-layer rule can keep large-batch training stable for AlexNet and ResNet-50.

## Core idea

Compute, for each layer, a local learning rate equal to the global rate times a trust ratio. The trust ratio is the layer's weight norm divided by its gradient norm, with a small weight-decay term included, and it is scaled by a trust coefficient \(\eta\). Each layer then takes a step whose size is set by its own weights.

## Algorithm

For layer \(\ell\) with weights \(w_\ell\) and gradient \(\nabla L(w_\ell)\), with global learning rate \(\gamma\), weight decay \(\beta\) and trust coefficient \(\eta < 1\):

1. Compute the trust ratio \(\lambda_\ell = \eta\, \dfrac{\|w_\ell\|}{\|\nabla L(w_\ell)\| + \beta\|w_\ell\|}\).
2. Update the momentum \(v_\ell \leftarrow m\, v_\ell + \gamma\, \lambda_\ell\, (\nabla L(w_\ell) + \beta w_\ell)\), then set \(w_\ell \leftarrow w_\ell - v_\ell\).

The trust ratio is defined in Equation 6 of the paper, and the momentum and weight updates follow its Algorithm 1. Both were checked against the full text.

## Results

- The abstract reports that the authors scale AlexNet to a batch size of 8K and ResNet-50 to a batch size of 32K, both "without loss in accuracy".
- The abstract gives no other accuracy or speed figures, so none are quoted here.

## Limitations

- The method is designed for SGD-type updates with momentum. Its extension to adaptive optimisers is the subject of [LAMB](lamb.md).
- The paper notes that the weight-to-gradient norm ratio varies significantly between weights and biases, and it does not say how the trust ratio treats biases.
- The benefit is reported for large batches. At small batches it may not improve on plain SGD.

## Connections

- [Gradient Clipping and Normalised Updates](gradient-clipping-and-normalisation.md) is the overview where LARS sits beside norm clipping and LAMB.
- [Gradual warm-up and linear scaling](gradual-warm-up.md) is the global-rate recipe that LARS extends.
- [LAMB](lamb.md) applies the same trust-ratio idea to Adam.
- [Large-batch and distributed training](large-batch-and-distributed.md) is the setting where the method is used.

## Open questions

- How should the trust ratio treat layers whose weights are near zero, or are normalised by a batch statistic?
- Does the benefit persist when the batch is small enough that the global rate is already stable?

## References

### Seminal papers

- You, Y., Gitman, I. & Ginsburg, B. (2017). *Large Batch Training of Convolutional Networks*. arXiv. https://arxiv.org/abs/1708.03888 — Introduces LARS and reports AlexNet at batch size 8K and ResNet-50 at 32K without loss in accuracy.
- You, Y., et al. (2019). *Large Batch Optimization for Deep Learning: Training BERT in 76 Minutes*. ICLR. https://arxiv.org/abs/1904.00962 — Extends the layer-wise trust-ratio idea to Adam through LAMB.
- Goyal, P., et al. (2017). *Accurate, Large Minibatch SGD: Training ImageNet in 1 Hour*. arXiv. https://arxiv.org/abs/1706.02677 — The linear scaling and warm-up recipe that LARS was proposed to go beyond.
- Pascanu, R., Mikolov, T. & Bengio, Y. (2013). *On the Difficulty of Training Recurrent Neural Networks*. ICML. https://arxiv.org/abs/1211.5063 — Norm clipping, a different way to limit the step when gradients are large.

### Surveys and textbooks

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). *Optimization Methods for Large-Scale Machine Learning*. SIAM Review. https://arxiv.org/abs/1606.04838 — Survey of stochastic gradient methods, with discussion of step-size choices for large batches.
