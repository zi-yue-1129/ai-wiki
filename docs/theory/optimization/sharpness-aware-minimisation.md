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

The paper recommends \(\rho = 0.05\) as a default, a value it calls "a solid default" and uses for all of its ImageNet experiments.

## Key methods

SAM is the base method. The main alternative that keeps its structure is the adaptive variant, which changes the shape of the neighbourhood rather than the update rule.

- [Sharpness-aware minimisation (Foret et al., 2021)](sharpness-aware-minimisation.md): a fixed Euclidean ball of radius \(\rho\) around the weights, one ascent step per iteration.
- [Adaptive sharpness-aware minimisation (Kwon et al., 2021)](asam.md): the same two-gradient step, but the neighbourhood is scaled by the weight magnitudes, which makes the sharpness measure invariant to rescaling of the weights.

## Key results

The paper's headline results are reported as test error, in its Tables 1 and 2:

- **CIFAR-10**, WideResNet-28-10 trained for 1800 epochs with AutoAugment: SAM reaches 1.6% test error, against 2.2% without SAM.
- **ImageNet**, ResNet-152: top-1 error falls from 20.3% to 18.4% with SAM. The 20.3% figure is the 200-epoch baseline; the 400-epoch baseline is 20.9%.

These are single-run numbers from the paper. Later comparisons, including the adaptive variant, report mean and standard deviation over several seeds.

## Limitations

- Each step costs two gradient evaluations, so training is roughly twice as expensive per step as the base optimiser, unless the second pass is made cheaper.
- The radius \(\rho\) is an extra hyperparameter, and its best value depends on the model and the data.
- Sharpness is not an invariant measure: Dinh et al. (2017) show that reparametrisation can change it without changing the function. SAM's benefit is therefore a statement about the chosen parametrisation as well as about the minimum. The adaptive variant addresses this for weight rescaling, which is one specific case.

## Connections

- [Convergence, Loss Landscapes and Sharpness](theory-and-landscapes.md) is the overview where SAM sits beside convergence theory and the landscape literature.
- [Sharp minima](sharp-minima.md) gives the flatness-and-generalisation hypothesis that SAM is built to test.
- [SGD noise scale](sgd-noise-scale.md) explains why large batches tend to find sharper minima.
- [Regularisation and weight decay](regularisation-and-weight-decay.md) changes the loss landscape directly, as a penalty, rather than through a worst-case neighbourhood.

## Applications

- Training image classifiers on CIFAR and ImageNet, where the paper reports improved test error.

## Open questions

- Is a worst-case neighbourhood the right notion of flatness, or does it mostly act as a regulariser on the gradient?
- How should \(\rho\) be scaled with model size or batch size, and can it be set without a search?

## References

### Seminal papers

- Foret, P., Kleiner, A., Mobahi, H. & Neyshabur, B. (2021). *Sharpness-Aware Minimization for Efficiently Improving Generalization*. ICLR 2021. https://arxiv.org/abs/2010.01412 — Proposes SAM, a min-max objective over a neighbourhood of the parameters, and reports better generalisation on image benchmarks. Checked: arXiv metadata matches; ICLR 2021 poster page at https://iclr.cc/virtual/2021/poster/2782 lists the same title.
- Kwon, J., Kim, J., Park, H. & Choi, I. K. (2021). *ASAM: Adaptive Sharpness-Aware Minimization for Scale-Invariant Learning of Deep Neural Networks*. ICML 2021, PMLR 139. https://arxiv.org/abs/2102.11600 — Introduces a scale-invariant sharpness measure and the adaptive neighbourhood used by ASAM. Checked: arXiv metadata matches; the paper header gives PMLR 139.
- Keskar, N. S., et al. (2017). *On Large-Batch Training for Deep Learning: Generalization Gap and Sharp Minima*. ICLR 2017. https://arxiv.org/abs/1609.04836 — The sharp-minima hypothesis that SAM is designed to act on. Checked: the ICLR 2017 entry at https://mlanthology.org/iclr/2017/keskar2017iclr-large lists the same title.
- Dinh, L., Pascanu, R., Bengio, S. & Bengio, Y. (2017). *Sharp Minima Can Generalize For Deep Nets*. ICML 2017, PMLR 70. https://proceedings.mlr.press/v70/dinh17b.html — Shows that sharpness can be changed by reparametrisation without changing the function, which limits what sharpness measures can explain.
- Dauphin, Y., et al. (2014). *Identifying and attacking the saddle point problem in high-dimensional non-convex optimization*. arXiv. https://arxiv.org/abs/1406.2572 — The high-dimensional landscape context in which flat and sharp regions matter.

### Surveys and textbooks

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). *Optimization Methods for Large-Scale Machine Learning*. SIAM Review. https://arxiv.org/abs/1606.04838 — Survey of stochastic gradient methods, the base optimisers that SAM wraps.
