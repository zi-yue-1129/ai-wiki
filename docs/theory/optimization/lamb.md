---
status: complete
last_reviewed: 2026-10-28
related:
  - theory/math
tags:
  - optimization
  - large batch
  - layer-wise adaptation
aliases:
  - LAMB
  - Layer-wise adaptive moments
  - 逐層自適應動量
---

# LAMB

LAMB (Layer-wise Adaptive Moments for Batch training) applies the layer-wise trust ratio of LARS to an Adam-style update. You et al. (2019) used it to train BERT with very large batches, reducing training time from three days to 76 minutes on a TPU Pod. The parent overview is [Gradient Clipping and Normalised Updates](gradient-clipping-and-normalisation.md), and the per-coordinate method it extends is [Adam](adaptive/adam.md).

## Overview

LARS scales each layer's step by its trust ratio, but it works with SGD-type updates. Transformers are usually trained with Adam, whose per-coordinate normalisation is important for them. LAMB keeps the Adam update, which contains the bias-corrected first and second moments, and then rescales the whole layer update by the trust ratio. The result is an adaptive optimiser in which the size of each layer's change is proportional to the layer's weight norm, clipped by a function \(\phi\).

## Problem

The abstract states the aim as large-batch training without degradation in performance. For BERT, the authors want to use batch sizes large enough to cut training time sharply, and they ask whether an Adam-based method can do this without losing accuracy.

## Core idea

Compute the Adam direction for each layer, then multiply it by a trust ratio equal to the layer's weight norm, clipped by \(\phi\), divided by the norm of the update. This makes each layer's change proportional to its own weights, as in LARS, while keeping Adam's per-coordinate behaviour.

## Algorithm

For layer \(\ell\) with weights \(x_t\), let \(r_t = \dfrac{\hat m_t}{\sqrt{\hat v_t}+\epsilon}\) be the bias-corrected Adam direction, without weight decay, and let \(\lambda\) be the weight-decay coefficient. Let \(\phi(z) = \min\{\max\{z, \gamma_l\}, \gamma_u\}\) be a clipping function with bounds \(\gamma_l\) and \(\gamma_u\), where \(\phi(z) = z\) is a special case.

1. Compute the trust ratio \(\dfrac{\phi(\|x_t\|)}{\|r_t + \lambda x_t\|}\).
2. Update \(x_{t+1} = x_t - \eta_t\, \dfrac{\phi(\|x_t\|)}{\|r_t + \lambda x_t\|}\,(r_t + \lambda x_t)\).

The update is taken from the method description in the paper and was checked against the full text.

## Results

- The abstract reports training with very large batch sizes of 32,868 "without any degradation of performance".
- It reports that BERT training time can be reduced "from 3 days to just 76 minutes", with the shorter time coming from raising the batch size to the memory limit of a TPUv3 Pod.
- The abstract names BERT and ResNet-50 as training tasks, and it states a convergence analysis of LAMB and LARS.

## Limitations

- The reported speed-up depends on a large hardware setup, and it is not a like-for-like comparison of algorithms on one machine.
- The clipping function \(\phi\) adds bounds \(\gamma_l\) and \(\gamma_u\), which are further settings to choose.
- The convergence analysis is a general result, and it does not replace an empirical check on the target model.

## Connections

- [LARS](lars.md) is the SGD-based method whose trust ratio LAMB adopts.
- [Adam](adaptive/adam.md) provides the update that LAMB rescales.
- [AdamW](adaptive/adamw.md) separates weight decay from the adaptive step, which LAMB's update also needs to handle.
- [Gradual warm-up and linear scaling](gradual-warm-up.md) is the schedule recipe used alongside it in large-batch pre-training.
- [Large-batch and distributed training](large-batch-and-distributed.md) is where the method is used in practice.

## Open questions

- Does the trust ratio help across Transformer sizes, or only at the batch sizes studied?
- How does LAMB compare with adaptive methods that have no layer-wise scaling, when both are tuned?

## References

### Seminal papers

- You, Y., et al. (2019). *Large Batch Optimization for Deep Learning: Training BERT in 76 Minutes*. ICLR. https://arxiv.org/abs/1904.00962 — Introduces LAMB, an Adam-based layer-wise optimiser, for BERT pre-training with very large batches.
- You, Y., Gitman, I. & Ginsburg, B. (2017). *Large Batch Training of Convolutional Networks*. arXiv. https://arxiv.org/abs/1708.03888 — The trust-ratio idea for SGD that LAMB extends to Adam.
- Kingma, D. P. & Ba, J. (2015). *Adam: A Method for Stochastic Optimization*. ICLR. https://arxiv.org/abs/1412.6980 — The per-coordinate update that LAMB rescales layer by layer.
- Loshchilov, I. & Hutter, F. (2017). *Decoupled Weight Decay Regularization*. arXiv:1711.05101 (ICLR 2019). https://arxiv.org/abs/1711.05101 — Decoupled weight decay, which the adaptive update uses alongside the trust ratio.

### Surveys and textbooks

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). *Optimization Methods for Large-Scale Machine Learning*. SIAM Review. https://arxiv.org/abs/1606.04838 — Survey of adaptive stochastic methods and their trade-offs in large-scale training.
