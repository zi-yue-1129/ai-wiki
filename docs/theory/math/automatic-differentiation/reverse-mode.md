---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/math/automatic-differentiation
  - theory/deep-learning
tags:
  - reverse-mode differentiation
  - backpropagation
  - adjoint
aliases:
  - 反向模式自動微分
  - Reverse-mode automatic differentiation
  - Reverse mode
---

# Reverse-mode differentiation

Reverse-mode differentiation computes the gradient of a scalar output with respect to all inputs in one backward sweep over a program, after one forward sweep that records the intermediate values. When the output is a scalar and the inputs are many, as with the loss of a neural network and its parameters, this is far cheaper than computing one directional derivative per input. Backpropagation is this method applied to a neural network.

## Overview

The [automatic differentiation chapter](index.md) describes the two modes. This page covers reverse mode, which is the one that trains large models. It is best understood as the chain rule applied from the output towards the inputs, carrying a sensitivity for each intermediate value.

## Problem

Suppose a function $f: \mathbb{R}^n \to \mathbb{R}$ maps millions of parameters to a loss. The gradient has $n$ components. Forward mode produces one component per pass, so a full gradient costs about $n$ passes. Training a model would then take a time proportional to its number of parameters for every update, which is impractical.

## Core idea

Reverse mode works in two phases. The forward phase runs the program and stores each intermediate value $v_i$ in a computational graph. The reverse phase starts with the adjoint of the output, $\bar{y} = 1$, and walks the graph backwards. At each node it uses the local derivatives of the operation to pass the adjoint to its inputs, adding contributions where a value is used more than once:

$$\bar{v}_j = \sum_{i \in \text{children}(j)} \bar{v}_i \,\frac{\partial v_i}{\partial v_j}$$

Each adjoint is a vector-Jacobian product. The point is that the gradient with respect to all inputs is produced by one backward sweep whose cost is a small constant multiple of evaluating the function, a result known as the cheap gradient principle [(Griewank and Walther, 2008)](https://doi.org/10.1137/1.9780898717761).

## Equation

For a vector-valued operation $y = g(x)$ with Jacobian $J$, the adjoint rule maps the output sensitivity $\bar{y}$ to an input sensitivity without forming $J$:

$$\bar{x} = J^{\top} \bar{y}$$

For a layer $y = Wx + b$ with a loss $L$, this gives $\bar{W} = \bar{y}\, x^{\top}$ and $\bar{x} = W^{\top} \bar{y}$. Chaining these rules through the graph is exactly backpropagation [(Rumelhart et al., 1986)](https://doi.org/10.1038/323533a0).

## Results

The reverse-mode gradient is exact up to floating-point rounding, unlike finite differences, which trade truncation error against rounding error. The survey by Baydin and colleagues reviews how reverse mode is used across machine learning and compares it with forward mode and with symbolic differentiation [(Baydin et al., 2018)](https://arxiv.org/abs/1502.05767). Specific runtime comparisons are in that survey and in the frameworks it covers.

## Limitations

- Reverse mode must store the intermediate values of the forward pass, so memory grows with the length of the computation. For long sequences or deep models this can dominate the cost.
- Checkpointing trades memory for recomputation: some intermediate values are discarded and recomputed during the reverse sweep. The schedule that minimises the extra work is a known optimisation problem [(Griewank and Walther, 2008)](https://doi.org/10.1137/1.9780898717761).
- Control flow with data-dependent branches is differentiated along the path that was executed. The gradient is correct for that path, but the function may be non-differentiable at the branch boundaries.

## Connections

Reverse mode is the mechanism behind [backpropagation](../../deep-learning/index.md), and the gradients it produces drive the optimisers used in training. Its dual, forward mode, is covered in [Forward-mode differentiation](forward-mode.md). The sensitivity notation is in [Notation and symbols](../../../reference/notation/index.md).

## Applications

Training neural networks of any architecture, gradient-based optimisation of simulators, and sensitivity analysis in scientific computing where the output is a scalar objective.

## Open questions

- How should reverse mode be organised for very long sequences, where storing the forward pass is infeasible?
- Can the graph be built and differentiated efficiently for programs with dynamic structure and discrete choices?

## References

### Seminal papers

- Rumelhart, Hinton and Williams, *Learning representations by back-propagating errors*, Nature (1986). https://doi.org/10.1038/323533a0 — Popularises backpropagation, which is reverse mode applied to layered networks.
- Pearlmutter and Siskind, *Reverse-mode AD in a functional framework: Lambda the ultimate backpropagator*, ACM Transactions on Programming Languages and Systems (2008). https://doi.org/10.1145/1330017.1330018 — Reverse mode as a program transformation in a functional setting.

### Surveys and textbooks

- Baydin, Pearlmutter, Radul and Siskind, *Automatic differentiation in machine learning: a survey*, Journal of Machine Learning Research (2018). https://arxiv.org/abs/1502.05767 — Survey of both modes and their use in machine learning.
- Griewank and Walther, *Evaluating Derivatives: Principles and Techniques of Algorithmic Differentiation*, SIAM (2008). https://doi.org/10.1137/1.9780898717761 — Standard textbook covering the cheap gradient principle and checkpointing.
- Goodfellow, Bengio and Courville, *Deep Learning*, MIT Press (2016). https://www.deeplearningbook.org/ — Explains backpropagation in the context of training neural networks.

### Articles and documentation

- Paszke et al., *PyTorch: An Imperative Style, High-Performance Deep Learning Library* (2019). https://arxiv.org/abs/1912.01703 — Describes a framework that records the graph during the forward pass and replays it in reverse.
