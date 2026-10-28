---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/math
  - theory/deep-learning
tags:
  - optimization
  - adaptive methods
aliases:
  - 自適應最佳化
  - 自適應方法
  - Adaptive optimisers
  - Adaptive gradient methods
---

# Adaptive Methods

Adaptive methods give each parameter its own step size. Parameters that receive large or frequent gradients take smaller steps, and rarely updated parameters take larger ones. Most optimisers used to train large neural networks today belong to this family. This page covers the common idea and its best-known members. The [overview](../index.md) explains where these methods sit among the other optimisation families.

## Overview

Plain SGD uses one learning rate \(\eta\) for all parameters. Real networks mix very different scales: embedding rows that appear once per batch, normalisation gains, and attention weights may see gradients that differ by orders of magnitude. A single \(\eta\) must then be small enough for the largest gradients, which makes progress on the rest slow.

Adaptive methods keep running statistics of the gradients and divide each update by a per-parameter scale. The scale is usually the root mean square of recent gradients, so the update has roughly unit size in each coordinate.

## Key concepts

- **Second-moment estimate**: a running average \(v_t\) of squared gradients, which measures how large each parameter's gradients have been.
- **First-moment estimate**: a running average \(m_t\) of gradients, which acts as momentum.
- **Bias correction**: the averages start at zero, so early estimates are too small. Dividing by \(1-\beta^t\) corrects this.
- **Epsilon \(\epsilon\)**: a small constant that prevents division by zero. Its value affects behaviour when gradients are tiny.
- **Decoupled weight decay**: applying the decay directly to the parameters, outside the adaptive step (see below).

## How it works

Adam combines a momentum term with a per-parameter scale:

\[
\begin{aligned}
m_t &= \beta_1 m_{t-1} + (1-\beta_1)\, g_t \\
v_t &= \beta_2 v_{t-1} + (1-\beta_2)\, g_t^2 \\
\theta_t &= \theta_{t-1} - \eta\, \frac{\hat m_t}{\sqrt{\hat v_t}+\epsilon}
\end{aligned}
\]

Here \(\hat m_t = m_t/(1-\beta_1^t)\) and \(\hat v_t = v_t/(1-\beta_2^t)\). Typical values are \(\beta_1 \approx 0.9\) and \(\beta_2 \approx 0.999\).

Because every coordinate is scaled, the update size is bounded by roughly \(\eta\) in each direction. This makes Adam less sensitive to the scale of the gradients, but it also means the effective learning rate changes over time as \(v_t\) moves, which is one reason learning-rate schedules matter.

## Variants

| Method | Idea | Status |
|---|---|---|
| AdaGrad | Accumulate all past squared gradients; suits sparse features | Planned |
| RMSProp | Exponential average of squared gradients instead of a sum | Planned |
| Adam | Momentum plus adaptive scale, with bias correction | This page |
| AdamW | Adam with decoupled weight decay | This page |
| LARS, LAMB | Layer-wise scaling of the step by the weight norm, for very large batches | Planned |
| Adafactor | Factorised second-moment estimate to save memory | Planned |
| Lion | Sign-based update from momentum; less memory than Adam | Planned |
| Shampoo, SOAP | Preconditioners built from matrix statistics of the gradient | Planned, see [Second-order methods](../second-order.md) |
| Muon | Orthogonalised momentum updates for matrix parameters | Planned |

## Key methods

### Adam (Kingma & Ba, 2014/2015)

- **Problem:** stochastic gradients are noisy and sparse, and first-order methods need careful, problem-specific learning rates.
- **Core idea:** adapt a separate step size for each parameter using running estimates of the first and second moments of its gradient, with bias correction for early steps.
- **Equation or algorithm:** the update above, with \(\beta_1 \approx 0.9\), \(\beta_2 \approx 0.999\) and \(\epsilon\) a small constant.
- **Results:** the abstract describes the method as working well in practice and comparing favourably with other stochastic optimisers. It gives no benchmark numbers in the abstract; the experimental results are in the paper's body.
- **Limitations:** the paper's convergence analysis is in the online convex optimisation framework, not for deep networks. Adam can generalise worse than SGD with momentum on some image tasks, and its per-parameter scaling interacts badly with L2 regularisation (see AdamW).

### AdamW (Loshchilov & Hutter, 2017/2019)

- **Problem:** for adaptive methods, adding an L2 penalty to the loss is not the same as weight decay. The penalty is rescaled by the adaptive denominator, so regularisation weakens for parameters with large gradients.
- **Core idea:** apply weight decay directly to the parameters, outside the adaptive step, so the decay factor is decoupled from the gradient scaling.
- **Equation or algorithm:** \(\theta_t = \theta_{t-1} - \eta\big(\frac{\hat m_t}{\sqrt{\hat v_t}+\epsilon} + \lambda\,\theta_{t-1}\big)\).
- **Results:** the abstract reports that decoupled decay substantially improves Adam's generalisation and lets it compete with SGD with momentum on image classification. It gives no specific numbers in the abstract.
- **Limitations:** the decay coefficient and learning rate still interact, and the benefit has been reported mainly for image classification. AdamW is now common for Transformer models, but its advantage on other tasks depends on tuning.

## Connections

- [SGD and momentum](../sgd-and-momentum.md) is the non-adaptive baseline that these methods are compared with.
- [Loss functions and optimisation](../../paradigms/supervised/loss-functions-and-optimization/index.md) covers weight decay as a regulariser.
- [Mathematics](../../math/index.md) gives the moment and convexity background.

## Applications

- AdamW and Adam are common for training Transformers and other large networks.
- Adafactor and similar memory-light variants are used where optimiser state is too large to store in full.

## Open questions

- Why do adaptive methods sometimes generalise worse than SGD with momentum, and when does tuning close the gap?
- Which per-parameter scaling rules work best at very large batch sizes?

## References

### Seminal papers

- Kingma, D. P. & Ba, J. (2015). Adam: A Method for Stochastic Optimization. ICLR. https://arxiv.org/abs/1412.6980 — Proposes Adam, an adaptive method that uses bias-corrected moment estimates of the gradient.
- Loshchilov, I. & Hutter, F. (2019). Decoupled Weight Decay Regularization. ICLR. https://arxiv.org/abs/1711.05101 — Shows that L2 regularisation and weight decay differ for Adam and proposes AdamW.
- Duchi, J., Hazan, E. & Singer, Y. (2011). Adaptive Subgradient Methods for Online Learning and Stochastic Optimization. *JMLR*. https://jmlr.org/papers/v12/duchi11a.html — Introduces AdaGrad, which scales each coordinate by its accumulated squared gradients.

### Surveys and textbooks

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). Optimization Methods for Large-Scale Machine Learning. *SIAM Review*. https://arxiv.org/abs/1606.04838 — Survey of stochastic gradient methods, including adaptive variants, and their trade-offs for large datasets.

### Articles and documentation

- PyTorch documentation, *torch.optim*. https://pytorch.org/docs/stable/optim.html — Reference implementations of Adam, AdamW and related optimisers with their exact update rules.
