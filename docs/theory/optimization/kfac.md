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

K-FAC (Kronecker-factored approximate curvature) is a practical approximation to the natural gradient for neural networks. It approximates the Fisher information matrix layer by layer, writes each block as a Kronecker product of two small matrices, and inverts those small matrices. Martens and Grosse (2015) introduced it. The family overview is [Second-Order and Quasi-Newton Methods](second-order.md).

## Overview

Natural gradient descent preconditions the gradient with the inverse Fisher information matrix. This makes the update invariant to how the parameters are written, and for many models it is a more meaningful direction than the plain gradient. The difficulty is that the Fisher matrix of a network has millions of rows, and inverting it is out of reach. K-FAC makes the inverse affordable by exploiting the structure of a fully connected layer.

## Problem

Natural gradient methods are principled, but for neural networks the Fisher matrix is too large to form or invert. Martens and Grosse ask whether a structured approximation can be inverted cheaply enough to give the progress of the natural gradient at a cost close to that of SGD.

## Core idea

For a fully connected layer with input activations \(a\) and output gradients \(g\), the gradient of the weight matrix is \(\nabla W = g a^\top\). The authors approximate the Fisher block for each layer by a Kronecker product \(A \otimes G\), where \(A\) is the second moment of the activations and \(G\) the second moment of the back-propagated output gradients. The inverse of a Kronecker product is the Kronecker product of the inverses, so only the two small factors need to be inverted.

## Algorithm

For each layer \(\ell\):

1. Accumulate running estimates of the activation covariance \(A_\ell\) and the output-gradient covariance \(G_\ell\).
2. Invert the two factors, typically with a damping term added to each for stability.
3. Precondition the layer's gradient: \(\Delta W_\ell = G_\ell^{-1}\,\nabla W_\ell\,A_\ell^{-1}\), with the factors damped as above.
4. Apply the update with a learning rate, and refresh the factors and their inverses at fixed intervals to save computation.

The inverses are updated less often than the gradients. In the paper's experiments the factors are inverted every \(T_3 = 20\) iterations, while the gradient is used at every step.

## Results

- The abstract states that K-FAC is "an efficiently invertible approximation" to the Fisher matrix, and that its updates can make much faster progress than stochastic gradient descent with momentum.
- It is described as "only several times more expensive to compute than the plain stochastic gradient". The abstract gives no numeric speed-up, so the size of the gain should be taken from the paper's experiments.

## Limitations

- The Kronecker product is an approximation. The abstract notes that it is neither diagonal nor low-rank, but it still ignores correlations between layers.
- It is designed for fully connected layers, and extending it to convolutional and recurrent layers requires further approximations.
- The factors must be refreshed and inverted at intervals, and damping must be tuned, so the method has more hyperparameters than SGD.

## Connections

- [Second-Order and Quasi-Newton Methods](second-order.md) is the overview where K-FAC sits next to L-BFGS and Shampoo.
- [L-BFGS](lbfgs.md) is the deterministic quasi-Newton alternative.
- [Shampoo](shampoo.md) is a related matrix-structured preconditioner, built from gradient statistics rather than the Fisher.
- [Deep learning](../deep-learning/index.md) describes the back-propagation that supplies the output gradients used by the factors.

## Applications

- Training large feed-forward and convolutional networks, where the per-step cost must stay close to SGD.
- Reinforcement learning with policy networks, where the natural gradient is a natural choice for the update.

## Open questions

- How should the approximation be extended to convolutional and attention layers without losing the speed advantage?
- How much of the benefit of K-FAC is due to the curvature estimate and how much to the damping and refresh schedule?

## References

### Seminal papers

- Martens, J. & Grosse, R. (2015). *Optimizing Neural Networks with Kronecker-factored Approximate Curvature*. ICML. https://arxiv.org/abs/1503.05671 — Introduces K-FAC, a Kronecker-factored approximation to the natural gradient for neural networks.
- Amari, S. (1998). *Natural Gradient Works Efficiently in Learning*. Neural Computation, 10(2), 251–276. https://doi.org/10.1162/089976698300017746 — The natural-gradient method that K-FAC approximates.
- Gupta, V., Koren, T. & Singer, Y. (2018). *Shampoo: Preconditioned Stochastic Tensor Optimization*. ICML. https://arxiv.org/abs/1802.09568 — A related matrix-structured preconditioner, for comparison with the Fisher-based approach.
- Liu, D. C. & Nocedal, J. (1989). *On the Limited Memory BFGS Method for Large Scale Optimization*. Mathematical Programming, 45, 503–528. https://doi.org/10.1007/BF01589116 — The deterministic quasi-Newton method that K-FAC is contrasted with.

### Surveys and textbooks

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). *Optimization Methods for Large-Scale Machine Learning*. SIAM Review. https://arxiv.org/abs/1606.04838 — Survey that places natural-gradient and curvature methods alongside first-order methods.
