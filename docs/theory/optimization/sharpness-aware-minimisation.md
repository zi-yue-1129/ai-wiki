---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/math
  - theory/deep-learning
tags:
  - optimization
  - sharpness
  - generalisation
aliases:
  - SAM
  - Sharpness-aware minimisation
  - 銳度感知最小化
---

# Sharpness-Aware Minimisation (SAM)

SAM trains a model towards parameters whose whole neighbourhood has low loss, not only low loss at the single point the optimiser visits. Foret et al. (2021) introduced it and reported better generalisation on image benchmarks. The parent overview is [Convergence, Loss Landscapes and Sharpness](theory-and-landscapes.md).

## Overview

SAM is a wrapper around a base optimiser such as SGD. It changes the gradient the base optimiser uses, at the cost of one extra forward and backward pass per step.

## Problem

Two parameter settings can have the same training loss and very different sharpness, meaning how fast the loss rises nearby. Sharp minima are sensitive to small perturbations of the weights, and the training loss does not show the difference. The aim is to find minima that stay low under perturbation, which is expected to generalise better.

## Core idea

Replace the training loss by the worst loss within a ball of radius \(\rho\) around the parameters. This turns training into a min-max problem: find parameters that minimise the loss after the worst small perturbation has been applied.

## Algorithm

The SAM objective is

\[
\min_w \max_{\|\varepsilon\|_2 \le \rho} L_S(w + \varepsilon),
\]

where \(L_S\) is the training loss. The inner maximisation is approximated by a first-order Taylor expansion of \(L_S\) around \(w\). For the Euclidean norm, the approximate worst-case perturbation is

\[
\hat\varepsilon(w) = \rho\,\frac{\nabla_w L_S(w)}{\|\nabla_w L_S(w)\|_2}.
\]

That is, a step of length \(\rho\) in the direction of steepest ascent. The gradient used for the update is then evaluated at the perturbed point:

\[
g = \nabla_w L_B\big(w + \hat\varepsilon(w)\big).
\]

With SGD as the base optimiser, the update is \(w_{t+1} = w_t - \eta\, g\), where \(g\) is computed on the mini-batch \(B\). Each step therefore needs two gradient evaluations, one at \(w\) and one at \(w + \hat\varepsilon(w)\).

The paper recommends \(\rho = 0.05\) as a default, and uses it for its main experiments without further tuning.

## Key results

The abstract reports that SAM improves generalisation across benchmark datasets, including CIFAR-10, CIFAR-100 and ImageNet, and on fine-tuning tasks, with state-of-the-art results in several settings. The abstract gives no accuracy figures, so this page does not quote any.

## Limitations

- Each step costs two gradient evaluations, so training is roughly twice as expensive per step as the base optimiser, unless the second pass is made cheaper.
- The radius \(\rho\) is an extra hyperparameter, and its best value depends on the model and the data.
- Sharpness is not an invariant measure: Dinh et al. (2017) show that reparametrisation can change it without changing the function. SAM's benefit is therefore a statement about the chosen parametrisation as well as about the minimum.

## Connections

- [Convergence, Loss Landscapes and Sharpness](theory-and-landscapes.md) is the overview where SAM sits beside convergence theory and the landscape literature.
- [Sharp minima](sharp-minima.md) gives the flatness-and-generalisation hypothesis that SAM is built to test.
- [SGD noise scale](sgd-noise-scale.md) explains why large batches tend to find sharper minima.
- [Regularisation and weight decay](regularisation-and-weight-decay.md) changes the loss landscape directly, as a penalty, rather than through a worst-case neighbourhood.

## Applications

- Training image classifiers on CIFAR and ImageNet, where the paper reports improved generalisation.
- Fine-tuning pre-trained models, where the paper also reports improvements.

## Open questions

- Is a worst-case neighbourhood the right notion of flatness, or does it mostly act as a regulariser on the gradient?
- How should \(\rho\) be scaled with model size or batch size, and can it be set without a search?

## References

### Seminal papers

- Foret, P., Kleiner, A., Mobahi, H. & Neyshabur, B. (2021). *Sharpness-Aware Minimization for Efficiently Improving Generalization*. arXiv. https://arxiv.org/abs/2010.01412 — Proposes SAM, a min-max objective over a neighbourhood of the parameters, and reports better generalisation on image benchmarks.
- Keskar, N. S., et al. (2017). *On Large-Batch Training for Deep Learning: Generalization Gap and Sharp Minima*. ICLR. https://arxiv.org/abs/1609.04836 — The sharp-minima hypothesis that SAM is designed to act on.
- Dinh, L., Pascanu, R., Bengio, S. & Bengio, Y. (2017). *Sharp Minima Can Generalize For Deep Nets*. arXiv. https://arxiv.org/abs/1703.04933 — Shows that sharpness can be changed by reparametrisation without changing the function, which limits what sharpness measures can explain.
- Dauphin, Y., et al. (2014). *Identifying and attacking the saddle point problem in high-dimensional non-convex optimization*. arXiv. https://arxiv.org/abs/1406.2572 — The high-dimensional landscape context in which flat and sharp regions matter.

### Surveys and textbooks

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). *Optimization Methods for Large-Scale Machine Learning*. SIAM Review. https://arxiv.org/abs/1606.04838 — Survey of stochastic gradient methods, the base optimisers that SAM wraps.
