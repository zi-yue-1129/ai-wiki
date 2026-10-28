---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/deep-learning
  - theory/math
tags:
  - automatic differentiation
  - backpropagation
  - gradients
aliases:
  - 自動微分
  - 反向傳播
  - Automatic differentiation
  - Autodiff
---

# Automatic differentiation

Automatic differentiation computes exact derivatives of a program by applying the chain rule to each elementary operation the program performs. It is the mechanism behind backpropagation, and it is what lets modern frameworks compute gradients of arbitrary models without anyone deriving them by hand.

## Overview

A program is a sequence of elementary operations: additions, multiplications, calls to functions with known derivatives. Automatic differentiation records these operations and applies the chain rule to them in a systematic order. It differs from numerical differentiation, which approximates derivatives with finite differences and suffers from rounding error, and from symbolic differentiation, which builds a single large expression and can blow up in size.

## Key concepts

- **Computational graph**: a directed graph whose nodes are intermediate values and whose edges are the operations that produce them.
- **Chain rule**: the rule that derivatives of composed functions multiply along the paths of the graph.
- **Jacobian-vector product (JVP)**: the directional derivative of a function along a given input direction.
- **Vector-Jacobian product (VJP)**: the gradient of a scalar output with respect to inputs, applied to a given output sensitivity. Reverse mode computes VJPs.
- **Higher-order derivatives**: derivatives of derivatives, such as Hessians, computed by differentiating the gradient computation.

## How it works

Automatic differentiation has two modes. **Forward mode** propagates derivatives from inputs to outputs, one input direction at a time, so its cost grows with the number of inputs. **Reverse mode** propagates sensitivities from the output back to the inputs, so one pass gives the gradient with respect to all inputs. For a scalar loss and millions of parameters, reverse mode is far cheaper, and it is the mode that implements backpropagation [(Baydin et al., 2018)](https://arxiv.org/abs/1502.05767).

Rumelhart, Hinton and Williams popularised backpropagation for training multi-layer networks, which is reverse-mode differentiation applied to a layered network [(Rumelhart et al., 1986)](https://doi.org/10.1038/323533a0).

## Key methods

- [Reverse-mode differentiation](reverse-mode.md): one backward pass for the gradient of a scalar output. This is backpropagation.
- [Forward-mode differentiation](forward-mode.md): one forward pass per input direction, efficient when inputs are few.

## Implementations

Frameworks record a graph during the forward computation and replay it in reverse to compute gradients. PyTorch's imperative design records operations as they run, and it is described with its performance goals in [Paszke et al. (2019)](https://arxiv.org/abs/1912.01703). Functional frameworks such as JAX expose forward and reverse modes as transformations of functions, which makes higher-order derivatives straightforward to compose.

## Connections

Gradient-based training, covered in [Deep learning](../../deep-learning/index.md), depends on reverse-mode differentiation. The notation for gradients is in [Notation and symbols](../../../reference/notation/index.md). Derivative computation in general is treated by Griewank and Walther [(Griewank and Walther, 2008)](https://doi.org/10.1137/1.9780898717761). The calculus that the chain rule builds on is in [Calculus](../index.md).

## Applications

Training every modern neural network, computing physical simulation sensitivities, sensitivity analysis in engineering, and computing Hessian information for optimisation and uncertainty.

## Open questions

- How should automatic differentiation handle programs with discrete choices, control flow and random sampling?
- What is the best memory trade-off for reverse mode on very long computations?

## References

### Seminal papers

- Baydin, Pearlmutter, Radul and Siskind, *Automatic differentiation in machine learning: a survey*, Journal of Machine Learning Research (2018). https://arxiv.org/abs/1502.05767 — A survey of automatic differentiation for machine learning, covering both modes.
- Rumelhart, Hinton and Williams, *Learning representations by back-propagating errors*, Nature (1986). https://doi.org/10.1038/323533a0 — Popularises backpropagation for multi-layer networks.
- Pearlmutter and Siskind, *Reverse-mode AD in a functional framework: Lambda the ultimate backpropagator*, ACM Transactions on Programming Languages and Systems (2008). https://doi.org/10.1145/1330017.1330018 — Reverse mode as a functional transformation.

### Surveys and textbooks

- Griewank and Walther, *Evaluating Derivatives: Principles and Techniques of Algorithmic Differentiation*, SIAM (2008). https://doi.org/10.1137/1.9780898717761 — The standard textbook on algorithmic differentiation.
- Goodfellow, Bengio and Courville, *Deep Learning*, MIT Press (2016). https://www.deeplearningbook.org/ — Explains backpropagation within the wider training setting.

### Articles and documentation

- Paszke et al., *PyTorch: An Imperative Style, High-Performance Deep Learning Library* (2019). https://arxiv.org/abs/1912.01703 — Describes how a widely used framework records and runs operations.
