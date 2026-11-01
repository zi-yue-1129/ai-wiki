---
related:
  - theory/paradigms/supervised/generalization-theory
  - theory/paradigms/supervised/evaluation-and-validation
  - theory/optimization
tags:
  - generalization
  - implicit regularisation
  - deep learning theory
aliases:
  - Rethinking generalization
  - Zhang et al. 2017
  - 重新思考泛化
last_reviewed: 2026-11-01
---

# Understanding Deep Learning Requires Rethinking Generalization

Zhang et al. (2017) showed that large image classifiers can fit completely random labels, and that they still generalise when the labels are real. The result breaks a common explanation of generalisation, namely that complexity measures and explicit regularisers keep the model simple enough to generalise. The paper is the standard reference for this puzzle, and the family-level picture is on the [Generalisation Theory](index.md) page.

## Overview

Classical learning theory ties generalisation to the complexity of the function class. A model with enough capacity to memorise any labelling should, on that view, fail to generalise. Zhang et al. tested this view on modern networks and found that the capacity is there, and that the usual regularisers are not what makes the networks generalise.

## Problem

The authors ask why large neural networks generalise well in practice, when traditional approaches do not clearly explain it. The experiments separate two questions. Can the network fit the training data when the labels carry no signal? And how much do explicit regularisers contribute to the test accuracy when the labels are real?

## Experiments

- **Random labels.** The networks are trained on CIFAR-10 and ImageNet with true labels and with random labels. The paper's summary is that deep networks easily fit random labels. With random pixels or Gaussian inputs, CIFAR-10 training error also reaches zero.
- **Regularisation ablation.** Data augmentation, weight decay and dropout are switched off, and their effect on test accuracy is measured. Early stopping and batch normalisation are also examined.
- **Finite-sample expressivity.** A construction shows that a two-layer ReLU network can fit any labelling of \(n\) points once its parameters exceed the number of data points.

On CIFAR-10 (Table 1), Inception reaches 100.0% training accuracy on true labels, with 85.75% test accuracy. On random labels it also reaches 100.0% training accuracy, with 9.78% test accuracy, which is near the 10% chance level. On ImageNet (Table 2), Inception v3 reaches 95.20% top-1 training accuracy on random labels, with 0.11% top-1 test accuracy.

## Implicit regularisation

The paper concludes that explicit regularisation is neither necessary nor, by itself, sufficient for controlling the generalisation error. It then looks for implicit regularisation. For linear models, the authors state that stochastic gradient descent from zero converges to a solution with small norm, and in the kernel experiments the interpolating solutions equal the minimum-norm solution. The authors add that minimum norm is only a small part of the story, because the norm rises while test error falls.

## Theory

Theorem 1 states that a two-layer ReLU network with \(2n + d\) weights can represent any function on a sample of \(n\) points in \(d\) dimensions. Corollary 1 gives a construction for depth \(k \ge 2\) with width \(O(n/k)\). The authors compare this with an earlier construction that needed \(O(dn)\) parameters. The result concerns fitting the sample, not generalisation.

## Limitations

- The authors say they have not yet found a precise formal measure under which these large models are simple.
- Rademacher complexity bounds are near one for these models, and uniform stability ignores the labels, so the classical bounds are too weak to explain the results.
- Implicit regularisation does not explain why some architectures generalise better than others.
- The random-label runs used no hyperparameter tuning, so the paper's conclusions about fit are limited to those runs.
- The early-stopping findings are provisional, because they need an isolated test set to be made rigorous.

## Connections

- A stability view of why SGD generalises is given by [Hardt et al. (2015)](https://arxiv.org/abs/1509.01240).
- Norm-based bounds that try to address the puzzle are covered on the [generalisation theory](index.md) page, including [Bartlett et al. (2017)](https://arxiv.org/abs/1706.08498).
- The optimisation side, including the role of SGD, is in the [optimisation](../../../optimization/index.md) chapter.

## Open questions

- Which property of the model and of SGD explains the generalisation that random-label fitting does not?
- Can a measure of complexity be found under which trained networks are simple?
- What separates the architectures that generalise better from those that do not?

## References

### Seminal papers

- Zhang, C., Bengio, S., Hardt, M., Recht, B. & Vinyals, O. (2017). Understanding Deep Learning Requires Rethinking Generalization. ICLR. [arXiv:1611.03530](https://arxiv.org/abs/1611.03530) — The randomisation experiments and the expressivity construction discussed on this page.
- Neyshabur, B., Tomioka, R. & Srebro, N. (2014). In Search of the Real Inductive Bias: On the Role of Implicit Regularization in Deep Learning. [arXiv:1412.6614](https://arxiv.org/abs/1412.6614) — Studies implicit regularisation and the norm of solutions found by gradient methods.
- Hardt, M., Recht, B. & Singer, Y. (2015). Train faster, generalize better: Stability of stochastic gradient descent. [arXiv:1509.01240](https://arxiv.org/abs/1509.01240) — Stability analysis of SGD, which gives a generalisation bound for trained models.
- Bartlett, P., Foster, D. J. & Telgarsky, M. (2017). Spectrally-normalized margin bounds for neural networks. [arXiv:1706.08498](https://arxiv.org/abs/1706.08498) — A norm-based margin bound for neural networks, one of the complexity measures the paper argues is still too weak.

### Surveys and textbooks

- Ioffe, S. & Szegedy, C. (2015). Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift. [arXiv:1502.03167](https://arxiv.org/abs/1502.03167) — The batch normalisation layer whose effect on generalisation the paper measures.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Szegedy, C. et al. (2015). Rethinking the Inception Architecture for Computer Vision. [arXiv:1512.00567](https://arxiv.org/abs/1512.00567) — The Inception v3 architecture used in the ImageNet experiments.
