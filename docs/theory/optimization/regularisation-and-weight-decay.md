---
status: draft
last_reviewed: 2026-10-28
aliases:
  - 正則化與權重衰減
  - 權重衰減
  - Weight decay
  - Regularisation in optimisation
related:
  - theory/paradigms/supervised/loss-functions-and-optimization
tags:
  - optimization
  - regularisation
  - weight decay
---

# Regularisation and Weight Decay in Optimisation

Regularisation is any change that makes training prefer some solutions over others, usually to improve generalisation. In optimisation it takes three forms: a penalty added to the loss, a shrinkage applied to the parameters at each step, and the implicit bias of the optimiser itself, which comes from the step size, the batch size and the noise in the gradients. The loss-side view is in [Loss Functions and Optimisation](../paradigms/supervised/loss-functions-and-optimization/index.md), and this page covers how the optimiser interacts with it.

## Overview

For plain gradient descent, adding an L2 penalty \(\frac{\lambda}{2}\|\theta\|^2\) to the loss and taking a gradient step is the same as shrinking the parameters by a factor \(1-\eta\lambda\) at each step. The two views coincide under SGD. They separate under adaptive optimisers. The penalty's gradient enters the adaptive denominator, so parameters with large gradients receive less decay. Loshchilov and Hutter (2017) showed this, and [AdamW](adaptive/adamw.md) applies the decay outside the adaptive step.

Beyond explicit penalties, the optimiser itself regularises. Small batches and large step sizes inject gradient noise, and that noise tends to favour broad minima over sharp ones. This implicit bias is discussed on the [sharp minima](sharp-minima.md) and [SGD noise scale](sgd-noise-scale.md) pages.

## Key concepts

- **L2 penalty**: a term \(\frac{\lambda}{2}\|\theta\|^2\) added to the loss. Its gradient is \(\lambda\theta\).
- **Weight decay**: the shrinkage \(\theta \leftarrow (1-\eta\lambda)\theta\) applied at each step, separate from the gradient.
- **Decoupling**: applying weight decay with its own coefficient, independent of the adaptive scaling.
- **Implicit regularisation**: the bias toward particular solutions that comes from the optimiser's dynamics, without any penalty in the loss.
- **Noise injection**: adding random perturbations to gradients or parameters on purpose.

## How it works

Three mechanisms, in order of how explicit they are:

| Mechanism | Where it acts | Typical form |
|---|---|---|
| Penalty in the loss | Gradient, scaled by the optimiser | L2 added to \(L(\theta)\) |
| Decoupled decay | Parameters, outside the gradient | \(\theta \leftarrow \theta - \eta(\nabla \hat L + \lambda\theta)\) |
| Implicit bias | Step size, batch size, gradient noise | Preference for broad minima and small effective learning rate \(\eta/B\) |

Under SGD the first two coincide, so the third is what remains to explain the generalisation gap between batch sizes.

## Key methods

Three entries, each with a page or a link. The first is a link to an existing page, because the method is already covered there.

| Method | Mechanism | What separates it |
|---|---|---|
| [Decoupled weight decay (AdamW)](adaptive/adamw.md) (Loshchilov & Hutter, 2017) | Decoupled decay | Moves the penalty out of the adaptive step, so the decay is not rescaled by the second moment |
| [Sharp minima and large-batch generalisation](sharp-minima.md) (Keskar et al., 2017) | Implicit bias of batch size | Large batches converge to sharper minima, which generalise worse in the authors' experiments |
| [SGD noise scale](sgd-noise-scale.md) (Smith & Le, 2018) | Implicit bias of learning rate and batch size | The noise scale \(\epsilon N/B\) sets the batch size at which generalisation peaks |

## Connections

- [Loss Functions and Optimisation](../paradigms/supervised/loss-functions-and-optimization/index.md) explains the penalty as part of the objective.
- [SGD and momentum](sgd-and-momentum/index.md) is the setting where L2 and weight decay coincide.
- [Adaptive methods](adaptive/index.md) are where the two diverge, and [AdamW](adaptive/adamw.md) is the fix.
- [Learning-rate schedules](learning-rate-schedules.md) interact with the decay, because the effective shrinkage depends on the current rate.
- [Large-batch and distributed training](large-batch-and-distributed.md) is where the implicit-bias results matter most.

## Applications

- Setting the weight-decay coefficient in Transformer and vision training recipes, usually together with AdamW.
- Choosing batch size and learning rate together, using the noise-scale rule as a guide.

## Open questions

- Is the generalisation advantage of small batches due to the noise itself, or to the smaller effective learning rate?
- How should the decay coefficient and the learning rate be tuned jointly when both change over training?
- Do implicit biases from the optimiser survive the addition of explicit regularisers?

## References

### Seminal papers

- Loshchilov, I. & Hutter, F. (2017). *Decoupled Weight Decay Regularization*. ICLR. https://arxiv.org/abs/1711.05101 — Shows that L2 regularisation and weight decay differ under adaptive methods, and proposes AdamW.
- Keskar, N. S., et al. (2017). *On Large-Batch Training for Deep Learning: Generalization Gap and Sharp Minima*. ICLR. https://arxiv.org/abs/1609.04836 — Reports that large-batch training converges to sharp minima that generalise worse.
- Smith, S. L. & Le, Q. V. (2018). *A Bayesian Perspective on Generalization and Stochastic Gradient Descent*. ICLR. https://arxiv.org/abs/1710.06451 — Argues that the optimal batch size scales with the learning rate and the training set size, through the noise scale.
- Goyal, P., et al. (2017). *Accurate, Large Minibatch SGD: Training ImageNet in 1 Hour*. arXiv. https://arxiv.org/abs/1706.02677 — Shows that large batches can match small-batch accuracy with linear scaling and warm-up.

### Surveys and textbooks

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). *Optimization Methods for Large-Scale Machine Learning*. SIAM Review. https://arxiv.org/abs/1606.04838 — Survey of stochastic gradient methods, with discussion of the role of gradient noise and batch size.
