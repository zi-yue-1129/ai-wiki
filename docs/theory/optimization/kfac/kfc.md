---
status: complete
last_reviewed: 2026-10-28
related:
  - theory/models/cnn
  - theory/deep-learning
tags:
  - optimization
  - natural gradient
  - convolutional networks
aliases:
  - KFC
  - Kronecker factors for convolution
  - 卷積的 Kronecker 因子
---

# K-FAC for Convolutions (KFC)

KFC (Kronecker Factors for Convolution) extends [K-FAC](index.md) to convolutional networks. It approximates the Fisher block of each convolution layer as a Kronecker product of two small matrices, so the natural-gradient update can be computed with the same cheap inversion that K-FAC uses for fully connected layers. Grosse and Martens (2016) introduced it.

## Problem

K-FAC's Kronecker factorisation was derived for fully connected layers, where each weight multiplies one input activation. In a convolution layer the same filter weights are shared across every spatial position, and each output depends on a patch of the input. The factorisation does not apply directly, so convolutional networks could not use K-FAC's natural-gradient updates.

## Core idea

KFC builds a structured probabilistic model of the backpropagated derivatives. It assumes that the activations are independent of the derivatives, that both are spatially homogeneous (their statistics are the same at every location), and that the derivatives are spatially uncorrelated. Under these assumptions, the Fisher block of each convolution layer decomposes as a Kronecker product. One factor is built from the input patches seen by the filters, averaged over spatial locations. The other is built from the output derivatives, accumulated across locations. The inverse then needs only the two small factors, as in K-FAC.

## Equation or algorithm

The KFC approximation has the form

$$
\mathcal{F}_\ell \approx \Omega_\ell \otimes \Gamma_\ell
$$

where $\Omega_\ell$ is the second moment of the layer's input patches and $\Gamma_\ell$ is the second moment of the backpropagated derivatives. The update is then the K-FAC preconditioned step, with damping added to both factors and the inverses refreshed less often than the gradients. The paper also shows that the resulting updates are invariant to commonly used reparameterisations, such as centring the activations.

## Results

The abstract reports that approximate natural gradient descent with KFC trains convolutional networks several times faster than carefully tuned SGD with momentum, and that it trains them in 10 to 20 times fewer iterations. The experiments use CIFAR-10 and Street View House Numbers (SVHN). The paper's stated aim is to evaluate the optimiser on previously published architectures, not to reach state-of-the-art accuracy. The paper also checks its modelling assumptions on trained networks, and finds the derivatives only weakly correlated, both spatially and across feature maps.

## Limitations

- The three probabilistic assumptions are approximations. The paper's measurements support them on its own networks, but they are not guaranteed for every architecture.
- Convolution needs more bookkeeping than the fully connected case, because the input patches must be extracted and accumulated for each layer.
- The experiments use two image benchmarks and older architectures, so the speed claims do not transfer directly to modern networks.
- As in K-FAC, the method needs damping and an inverse-refresh schedule, which are extra hyperparameters.

## Key methods

- [K-FAC](index.md) is the fully connected method whose Kronecker factorisation KFC extends.
- [EKFAC](ekfac.md) keeps the Kronecker-factored eigenbasis and tracks a diagonal variance in it. The authors report that it improves optimisation over K-FAC on several architectures.
- [Distributed K-FAC](distributed-kfac.md) runs the same kind of convolutional curvature across many GPUs for large-scale training.

## Open issues and related variants

- **Approximation quality.** How closely the KFC factors match the exact Fisher in deep convolutional networks is not settled.
- **Cost of patch statistics.** Accumulating patch statistics for large images and many channels is a practical bottleneck, and cheaper estimates are an open question.

## Connections

- [Convolutional networks](../../models/cnn/index.md) are the architecture family that KFC targets.
- [Second-order and quasi-Newton methods](../second-order.md) is the overview that places K-FAC next to L-BFGS and Shampoo.

## References

### Seminal papers

- Grosse, R. & Martens, J. (2016). *A Kronecker-factored approximate Fisher matrix for convolution layers*. ICML, PMLR 48:573–582. https://proceedings.mlr.press/v48/grosse16.html — Introduces KFC, the Kronecker factorisation of the Fisher block for convolution layers.
- Martens, J. & Grosse, R. (2015). *Optimizing Neural Networks with Kronecker-factored Approximate Curvature*. arXiv:1503.05671. https://arxiv.org/abs/1503.05671 — Introduces K-FAC for fully connected layers, which KFC extends.
- George, T., et al. (2018). *Fast Approximate Natural Gradient Descent in a Kronecker-factored Eigenbasis*. arXiv:1806.03884. https://arxiv.org/abs/1806.03884 — A later variant that keeps the Kronecker-factored eigenbasis, for comparison.
- Amari, S. (1998). *Natural Gradient Works Efficiently in Learning*. Neural Computation, 10(2), 251–276. https://doi.org/10.1162/089976698300017746 — The natural-gradient method that KFC approximates.

### Surveys and textbooks

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). *Optimization Methods for Large-Scale Machine Learning*. arXiv:1606.04838. https://arxiv.org/abs/1606.04838 — Survey placing natural-gradient and curvature methods among large-scale optimisers.
