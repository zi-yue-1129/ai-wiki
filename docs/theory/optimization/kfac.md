---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/math
  - theory/deep-learning
tags:
  - optimization
  - natural gradient
  - curvature
aliases:
  - K-FAC
  - Kronecker-factored approximate curvature
  - Kronecker 分解近似曲率
---

# K-FAC

K-FAC (Kronecker-factored approximate curvature) is a practical approximation to the natural gradient for neural networks. It approximates the Fisher information matrix one layer at a time, writes each block as a Kronecker product of two small matrices, and inverts those small matrices. Martens and Grosse (2015) introduced it. The family overview is [Second-Order and Quasi-Newton Methods](second-order.md).

## Overview

Natural gradient descent preconditions the gradient with the inverse Fisher information matrix. This makes the update invariant to how the parameters are written, and for many models it is a more meaningful direction than the plain gradient. The difficulty is that the Fisher matrix of a network has millions of rows, and inverting it is out of reach. K-FAC makes the inverse affordable by exploiting the structure of a fully connected layer.

## Problem

Natural gradient methods are principled, but for neural networks the Fisher matrix is too large to form or invert. Martens and Grosse ask whether a structured approximation can be inverted cheaply enough to give the progress of the natural gradient at a cost close to that of SGD.

## Core idea

For a fully connected layer with input activations $a$ and output gradients $g$, the gradient of the weight matrix is $\nabla W = g a^\top$. The authors approximate the Fisher block for each layer by a Kronecker product $A \otimes G$, where $A$ is the second moment of the activations and $G$ the second moment of the back-propagated output gradients. The inverse of a Kronecker product is the Kronecker product of the inverses, so only the two small factors need to be inverted.

The paper also approximates the inverse of the whole block-structured matrix as block-diagonal or block-tridiagonal. The authors justify this for the inverse of the Fisher, but not for the Fisher itself, and their experiments confirm that the inverse has this structure only approximately.

## Algorithm

For each layer $\ell$:

1. Accumulate running estimates of the activation covariance $A_\ell$ and the output-gradient covariance $G_\ell$ over a window of mini-batches.
2. Invert the two factors, with a damping term added to each for stability.
3. Precondition the layer's gradient: $\Delta W_\ell = G_\ell^{-1}\,\nabla W_\ell\,A_\ell^{-1}$, with the factors damped as above.
4. Apply the update with a learning rate. Momentum is applied on top of this update, which the paper finds important in practice.

The inverses are updated less often than the gradients. In the paper's experiments the factors are inverted every $T_3 = 20$ iterations, while the gradient is used at every step.

## Results

- The abstract describes K-FAC as "an efficiently invertible approximation" to the Fisher matrix, whose updates can make much faster progress than stochastic gradient descent with momentum. It says each update is "only several times more expensive to compute than the plain stochastic gradient".
- The paper's main experiments train three deep autoencoders from Hinton and Salakhutdinov (2006), on the MNIST, CURVES and FACES data. K-FAC with momentum reaches a lower training error per unit of computation time than a tuned SGD-with-momentum baseline (Figure 10 of the paper).
- The momentum technique is essential to these gains. Without it, K-FAC was not significantly faster than the baseline.

## Limitations

- The Kronecker product and the block-structured inverse are approximations. They ignore correlations between layers.
- The method is designed for fully connected layers. Convolutional and recurrent layers need further approximations, covered in the variants below.
- Each update costs several times an SGD step. The inverse refresh interval, damping schedule and momentum add hyperparameters that SGD does not have.
- The evidence is from autoencoder benchmarks. Speed claims on other tasks need their own experiments.

## Variants

- **K-FAC for convolutional layers.** Grosse and Martens (2016) adapt the Kronecker factorisation to convolution layers, whose weights are shared across spatial positions. [arXiv:1602.01407](https://arxiv.org/abs/1602.01407)
- **EKFAC.** George et al. (2018) keep the Kronecker-factored eigenbasis but re-estimate the scaling in that basis, aiming for a more faithful approximation of the Fisher at similar cost. [arXiv:1806.03884](https://arxiv.org/abs/1806.03884)

## Connections

- [Second-Order and Quasi-Newton Methods](second-order.md) is the overview where K-FAC sits next to L-BFGS and Shampoo.
- [L-BFGS](lbfgs.md) is the deterministic quasi-Newton alternative.
- [Shampoo](shampoo.md) is a related matrix-structured preconditioner, built from gradient statistics rather than the Fisher.
- [Deep learning](../deep-learning/index.md) describes the back-propagation that supplies the output gradients used by the factors.

## Applications

- Training large feed-forward and convolutional networks, where the per-step cost must stay close to SGD. The convolutional variant covers the second case.
- Reinforcement learning with actor-critic methods. Wu et al. (2017) use K-FAC for the natural-gradient updates of both the actor and the critic, inside a trust-region method. [arXiv:1708.05144](https://arxiv.org/abs/1708.05144)

## Open questions

- How much of the gap between the Kronecker approximation and the exact Fisher matters in practice?
- How much of the benefit of K-FAC is due to the curvature estimate and how much to the damping, refresh and momentum schedule?

## References

### Seminal papers

- Martens, J. & Grosse, R. (2015). *Optimizing Neural Networks with Kronecker-factored Approximate Curvature*. ICML. https://arxiv.org/abs/1503.05671 — Introduces K-FAC, a Kronecker-factored approximation to the natural gradient for neural networks.
- Amari, S. (1998). *Natural Gradient Works Efficiently in Learning*. Neural Computation, 10(2), 251–276. https://doi.org/10.1162/089976698300017746 — The natural-gradient method that K-FAC approximates.
- Grosse, R. & Martens, J. (2016). *A Kronecker-factored approximate Fisher matrix for convolution layers*. arXiv. https://arxiv.org/abs/1602.01407 — Extends the Kronecker factorisation to convolution layers.
- George, T., et al. (2018). *Fast Approximate Natural Gradient Descent in a Kronecker-factored Eigenbasis*. arXiv. https://arxiv.org/abs/1806.03884 — Re-estimates the scaling in the Kronecker-factored eigenbasis, a more faithful Fisher approximation.
- Wu, Y., et al. (2017). *Scalable trust-region method for deep reinforcement learning using Kronecker-factored approximation*. arXiv. https://arxiv.org/abs/1708.05144 — Applies K-FAC to actor-critic reinforcement learning with a trust region.
- Gupta, V., Koren, T. & Singer, Y. (2018). *Shampoo: Preconditioned Stochastic Tensor Optimization*. arXiv. https://arxiv.org/abs/1802.09568 — A related matrix-structured preconditioner, for comparison with the Fisher-based approach.
- Liu, D. C. & Nocedal, J. (1989). *On the Limited Memory BFGS Method for Large Scale Optimization*. Mathematical Programming, 45, 503–528. https://doi.org/10.1007/BF01589116 — The deterministic quasi-Newton method that K-FAC is contrasted with.

### Surveys and textbooks

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). *Optimization Methods for Large-Scale Machine Learning*. SIAM Review. https://arxiv.org/abs/1606.04838 — Survey that places natural-gradient and curvature methods alongside first-order methods.
