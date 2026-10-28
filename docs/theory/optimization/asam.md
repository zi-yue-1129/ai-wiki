---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/math
  - theory/deep-learning
tags:
  - optimization
  - sharpness
  - scale invariance
aliases:
  - ASAM
  - Adaptive sharpness-aware minimisation
  - 自適應銳度感知最小化
---

# Adaptive Sharpness-Aware Minimisation (ASAM)

ASAM is a variant of [SAM](sharpness-aware-minimisation.md) whose neighbourhood is scaled by the size of each weight. Because of that scaling, its sharpness measure does not change when the weights of a network are rescaled without changing the function it computes. Kwon et al. (2021) introduced it at ICML 2021.

## Overview

Like SAM, ASAM wraps a base optimiser and takes two gradient evaluations per step. The change is in the shape of the neighbourhood the perturbation may reach, not in the outer training loop.

## Problem

SAM uses a ball of fixed radius \(\rho\) in weight space. Many networks have layers, such as ReLU networks followed by batch normalisation, that let the weights be rescaled while the function stays the same. Under such a rescaling the fixed-radius sharpness changes, so a measured sharpness can be a poor guide to generalisation. The paper notes that the appropriate \(\rho\) for SAM depends on the scale of the weights along the training trajectory.

## Core idea

Define the neighbourhood relative to the weights: a perturbation may be large where the weights are large and small where they are small. Sharpness is then measured in a scale-invariant way, and the training objective follows from the same neighbourhood.

## Algorithm

ASAM defines adaptive sharpness with a normalisation operator \(T_w\). The paper's element-wise choice is \(T_w = \mathrm{diag}(|w_1|, \ldots, |w_k|)\), and the adaptive sharpness is

\[
\max_{\|T_w^{-1}\varepsilon\|_p \le \rho} L_S(w + \varepsilon) - L_S(w),
\]

where \(1 \le p \le \infty\). Its first-order approximation for \(p = 2\) gives the perturbation

\[
\hat\varepsilon(w) = \rho\,\frac{T_w^2 \nabla_w L_S(w)}{\|T_w \nabla_w L_S(w)\|_2}.
\]

The training step then uses the gradient at the perturbed point, \(g = \nabla_w L_B\big(w + \hat\varepsilon(w)\big)\), exactly as in SAM. The paper also gives a filter-wise choice of \(T_w\) for convolutional layers, in which the diagonal entries for a filter use that filter's \(\ell_2\) norm and the remaining weights use absolute values.

## Key results

The paper reports mean and standard deviation over several runs, for maximum test accuracy:

- **CIFAR-10, DenseNet-121**: SAM 92.00 ± 0.17; ASAM 93.33 ± 0.04 (5 runs).
- **CIFAR-10, WideResNet-28-10**: SAM 96.98 ± 0.04; ASAM 97.28 ± 0.07 (5 runs).
- **ImageNet, ResNet-50**, top-1 accuracy: SAM 76.39 ± 0.03; ASAM 76.63 ± 0.18 (3 runs).

The paper states that ASAM "generally surpasses SGD and SAM". The gains over SAM in these tables are small, mostly a fraction of a percentage point.

## Limitations

- The gains over SAM are small in the paper's own tables. On ImageNet the difference is within a few standard deviations of the runs.
- The choice of \(T_w\) is a design decision. The element-wise and filter-wise versions define different neighbourhoods, and the paper does not claim that either is optimal.
- The paper says the appropriate \(\rho\) for ASAM does not depend on the weight scale in the way SAM's does, but it does not give a shared default. Values of \(\rho\) are therefore not directly comparable between SAM and ASAM.
- The paper gives no explicit per-step cost for ASAM. Since the update has the same two-gradient structure as SAM's, the inferred cost is the same as SAM's, plus the cost of applying \(T_w\).

## Connections

- [SAM](sharpness-aware-minimisation.md) is the fixed-radius method that ASAM modifies. Read it first.
- [Convergence, Loss Landscapes and Sharpness](theory-and-landscapes.md) is the overview that places both methods among the landscape results.
- [Sharp minima](sharp-minima.md) is the flatness hypothesis that the scale-invariance argument refines.
- [Adaptive methods](adaptive/index.md) also rescale updates by weight-dependent quantities, though Adam and its relatives do it with gradient statistics rather than with the weights.

## Applications

- Training convolutional image classifiers on CIFAR-10 and ImageNet, the benchmarks the paper reports.

## Open questions

- Does scale invariance explain the generalisation gains, or does the gain come from the change in effective neighbourhood size?
- How should \(T_w\) be chosen for architectures beyond the ones the paper tests?

## References

### Seminal papers

- Kwon, J., Kim, J., Park, H. & Choi, I. K. (2021). *ASAM: Adaptive Sharpness-Aware Minimization for Scale-Invariant Learning of Deep Neural Networks*. ICML 2021, PMLR 139. https://arxiv.org/abs/2102.11600 — Defines scale-invariant adaptive sharpness and the ASAM objective, and reports small gains over SAM on CIFAR-10 and ImageNet. Checked: arXiv metadata and the PMLR 139 header in the paper.
- Foret, P., Kleiner, A., Mobahi, H. & Neyshabur, B. (2021). *Sharpness-Aware Minimization for Efficiently Improving Generalization*. ICLR 2021. https://arxiv.org/abs/2010.01412 — The fixed-radius method that ASAM modifies. Checked: ICLR 2021 poster page https://iclr.cc/virtual/2021/poster/2782 lists the same title.
- Keskar, N. S., et al. (2017). *On Large-Batch Training for Deep Learning: Generalization Gap and Sharp Minima*. ICLR 2017. https://arxiv.org/abs/1609.04836 — The sharp-minima hypothesis that the adaptive measure is meant to test. Checked: ICLR 2017 entry at https://mlanthology.org/iclr/2017/keskar2017iclr-large lists the same title.
- Dinh, L., Pascanu, R., Bengio, S. & Bengio, Y. (2017). *Sharp Minima Can Generalize For Deep Nets*. ICML 2017, PMLR 70. https://proceedings.mlr.press/v70/dinh17b.html — Shows that reparametrisation changes sharpness without changing the function, which is the problem ASAM addresses.

### Surveys and textbooks

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). *Optimization Methods for Large-Scale Machine Learning*. SIAM Review. https://arxiv.org/abs/1606.04838 — Survey of the stochastic gradient methods that both SAM and ASAM wrap.
