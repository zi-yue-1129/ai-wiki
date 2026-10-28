---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/math
  - theory/deep-learning
  - theory/paradigms/supervised/loss-functions-and-optimization
  - brain-mind/neuroai
tags:
  - optimization
  - gradient descent
aliases:
  - 最佳化
  - 優化
  - Optimisation
  - Optimization
  - 梯度下降
  - Gradient descent
---

# Optimisation

Training a model means choosing its parameters so that a loss function is small. Optimisation is the set of algorithms that do this search. Almost every method in this wiki, from linear regression to large language models, ends in an optimiser.

## Overview

Write the model as \(f_\theta\) with parameters \(\theta\), and the training loss as an average over data, \(L(\theta)=\frac{1}{N}\sum_i \ell(f_\theta(x_i), y_i)\). Learning is the search for \(\theta^\* = \arg\min_\theta L(\theta)\). Because the search is over millions or billions of numbers, we rely on the gradient \(\nabla_\theta L\), which points uphill, and move the other way. How well this works depends on the shape of the loss surface: whether it is convex, how curved it is, and how noisy our estimate of the gradient is.

The mathematics of this search is in [Mathematics](../math/index.md), and the training pipeline that uses it is in [Deep Learning](../deep-learning/index.md). The supervised-learning view of losses and regularisation is in [Loss Functions & Optimisation](../paradigms/supervised/loss-functions-and-optimization/index.md). This folder covers the optimisers themselves.

## Key concepts

- **Gradient descent**: repeatedly update \(\theta \leftarrow \theta - \eta \nabla L(\theta)\), where \(\eta\) is the learning rate.
- **Stochastic gradient descent (SGD)**: estimate the gradient from a random mini-batch rather than the whole dataset. Each step is cheap and noisy.
- **Convexity**: a convex function has no spurious local minima, so any local minimum is global. Neural-network losses are non-convex.
- **Smoothness**: a bound \(L\) on how fast the gradient can change. It fixes the largest safe step size, \(\eta \le 1/L\).
- **Conditioning**: when curvature differs widely across directions, plain gradient descent zig-zags. Per-parameter scaling helps.
- **Loss landscape**: the high-dimensional surface of \(L(\theta)\), with saddle points, flat regions and wide or narrow minima.

## Families

The optimisers below are grouped by what information they use. Each subpage gives the mechanism, the variants, and the key papers.

| Family | Uses | Subpage | Status |
|---|---|---|---|
| First-order, SGD family | Gradient and momentum | [SGD and momentum](sgd-and-momentum/index.md) | Draft |
| Adaptive methods | Per-parameter scale from squared gradients | [Adaptive methods](adaptive/index.md) | Draft (Adam and AdamW have their own pages) |
| Second-order and quasi-Newton | Curvature (Hessian or its approximation) | [Second-order methods](second-order.md), with pages on [L-BFGS](lbfgs.md), [K-FAC](kfac.md) and [Shampoo](shampoo.md) | Draft |
| Learning-rate schedules and warm-up | How \(\eta\) changes over time | [Learning-rate schedules](learning-rate-schedules.md), with pages on [gradual warm-up](gradual-warm-up.md), [cosine annealing with warm restarts](cosine-annealing-warm-restarts.md) and [cyclical learning rates](cyclical-learning-rates.md) | Draft |
| Regularisation and weight decay | Penalties that the optimiser must respect | [Regularisation and weight decay](regularisation-and-weight-decay.md), with pages on [sharp minima](sharp-minima.md) and the [SGD noise scale](sgd-noise-scale.md); decoupled decay is on the [AdamW](adaptive/adamw.md) page | Draft |
| Gradient clipping and normalisation | Limits on gradient size | [Gradient clipping and normalisation](gradient-clipping-and-normalisation.md), with pages on [norm clipping](norm-clipping.md), [LARS](lars.md) and [LAMB](lamb.md) | Draft |
| Large-batch and distributed | Training across many devices | [Large-batch and distributed](large-batch-and-distributed.md) | Draft |
| Zeroth-order and evolutionary | No gradient at all | [Zeroth-order and evolutionary](zeroth-order-and-evolutionary.md), with pages on [SPSA](spsa.md), [evolution strategies](evolution-strategies.md) and [CMA-ES](cma-es.md) | Draft |
| Theory | Convergence, landscapes, sharpness | [Theory and landscapes](theory-and-landscapes.md) | Planned |

## How it works

Gradient descent on a convex, \(L\)-smooth loss with step \(\eta = 1/L\) reduces the loss at rate \(O(1/T)\) after \(T\) steps, and linearly if the loss is strongly convex. Stochastic gradients add noise, and the classic Robbins–Monro conditions on the step sizes guarantee convergence. Each family above changes one part of this picture: the direction (momentum), the scale (adaptive methods), the curvature used (second-order), the schedule of steps, or the regularity assumed.

## Connections

- **Mathematics:** convexity, Taylor expansion and the Hessian explain why a method works. See [Mathematics](../math/index.md).
- **Deep learning:** backpropagation computes \(\nabla L\), and the optimiser decides how to use it. See [Deep Learning](../deep-learning/index.md).
- **Regularisation:** weight decay and early stopping act on the same objective and can be seen as implicit changes to the optimisation.
- **Brain and mind:** biological learning cannot follow an exact gradient, because exact backpropagation needs symmetric feedback weights that biological circuits do not obviously have. The search for local, plausible learning rules is a major theme in [NeuroAI](../../brain-mind/neuroai/index.md).

## Open questions

- Why do stochastic and adaptive methods find solutions that generalise, when the loss surface has many minima?
- How do learning-rate warm-up and schedules interact with very large batch sizes?
- Can second-order information be used at the scale of billion-parameter models at acceptable cost?
- Which local learning rules in biological systems approximate these optimisers?

## References

### Seminal papers

- Robbins, H. & Monro, S. (1951). A stochastic approximation method. *Annals of Mathematical Statistics*. doi:10.1214/aoms/1177729586 — Introduces stochastic approximation with decreasing step sizes, the foundation of stochastic gradient descent.
- Polyak, B. T. (1964). Some methods of speeding up the convergence of iteration methods. *USSR Computational Mathematics and Mathematical Physics*. doi:10.1016/0041-5553(64)90137-5 — Introduces heavy-ball momentum and analyses its acceleration on quadratic problems.
- Kingma, D. P. & Ba, J. (2015). Adam: A Method for Stochastic Optimization. ICLR. https://arxiv.org/abs/1412.6980 — Proposes Adam, an adaptive method with bias-corrected moment estimates of the gradient.

### Surveys and textbooks

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). Optimization Methods for Large-Scale Machine Learning. *SIAM Review*. https://arxiv.org/abs/1606.04838 — Survey of stochastic gradient methods and their trade-offs for large datasets, with convergence analysis.
- Boyd, S. & Vandenberghe, L. (2004). *Convex Optimization*. Cambridge University Press. https://web.stanford.edu/~boyd/cvxbook/ — Standard textbook on convex analysis and algorithms, with a free PDF from the authors.

### Lectures and videos

- Li, H., Xu, Z., Taylor, G., Studer, C. & Goldstein, T. (2018). Visualizing the Loss Landscape of Neural Nets. NeurIPS. https://arxiv.org/abs/1712.09913 — Visualisation method for loss surfaces that shows how network design changes landscape geometry.

### Articles and documentation

- Stanford CS231n, *Optimization* lecture notes. https://cs231n.github.io/optimization-1/ — Clear, illustrated notes on gradient descent, learning rates and momentum for students new to the topic.
