---
status: draft
last_reviewed: 2026-10-28
related:
  - society/interpretability
tags:
  - interpretability
  - attribution
aliases:
  - 積分梯度
  - Integrated gradients
---

# Integrated gradients

!!! info "Part of Feature attribution"
    This method page belongs to [Feature attribution](feature-attribution.md). It explains the method in detail; the overview compares it with the other methods.

Integrated gradients attributes a prediction to input features by accumulating the model's gradients along a straight path from a baseline input to the actual input. Sundararajan, Taly and Yan (2017) derived it from two axioms that they argue any attribution method should satisfy.

## Problem

Plain gradients, as used in saliency maps, can be unreliable: in saturated regions of a network the gradient can be near zero even when a feature matters a great deal. The problem is to find an attribution method that does not depend on where the gradient happens to be flat, and that is principled enough to justify.

## Core idea

Choose a baseline \(x'\) that carries no information, such as a black image or a zero vector. Move from the baseline to the input along a straight line and add up the gradients along the way. The total is the attribution for each feature, measured relative to the baseline.

## Equation

For input \(x\), baseline \(x'\), and model \(F\), the attribution to feature \(i\) is

\[
\mathrm{IG}_i(x) = (x_i - x'_i) \int_0^1 \frac{\partial F\bigl(x' + \alpha (x - x')\bigr)}{\partial x_i}\, d\alpha.
\]

In practice the integral is approximated by a sum over a finite number of steps.

## Results

The paper uses the axioms of sensitivity (a feature that changes the output gets a non-zero attribution) and implementation invariance (functionally equivalent networks get identical attributions) to design the method. It reports that most known attribution methods fail these axioms. The authors apply the method to two image models, two text models and a chemistry model, and show that it can help debug networks.

## Limitations

- **Baseline dependence.** The result depends on the baseline, and the choice of a neutral baseline is itself a judgement.
- **Approximation.** The integral is estimated numerically, so the attributions carry approximation error that must be checked.
- **Model, not world.** Attributions describe the model's sensitivity along the path, not causal effects in the world.
- **Sanity.** As with other gradient methods, a plausible-looking attribution does not by itself show that the model relies on the feature (Adebayo et al., 2018).

## References

### Seminal papers

- Sundararajan, M., Taly, A. & Yan, Q. (2017). Axiomatic Attribution for Deep Networks. *Proceedings of ICML 2017*. https://arxiv.org/abs/1703.01365 — Introduces integrated gradients and the sensitivity and implementation-invariance axioms.
- Simonyan, K., Vedaldi, A. & Zisserman, A. (2014). Deep Inside Convolutional Networks: Visualising Image Classification Models and Saliency Maps. *ICLR 2014 Workshop*. https://arxiv.org/abs/1312.6034 — The gradient-based saliency maps that integrated gradients refines.
- Lundberg, S. M. & Lee, S.-I. (2017). A Unified Approach to Interpreting Model Predictions. *Advances in Neural Information Processing Systems 30*. https://arxiv.org/abs/1705.07874 — Presents SHAP, which compares attributions against Shapley values rather than gradients.

### Surveys and textbooks

- Adebayo, J. et al. (2018). Sanity Checks for Saliency Maps. *Advances in Neural Information Processing Systems 31*. https://arxiv.org/abs/1810.03292 — Shows that some gradient-based maps are independent of the model and the data.
- Molnar, C. *Interpretable Machine Learning: A Guide for Making Black Box Models Explainable*, 3rd edition. https://christophm.github.io/interpretable-ml-book/ — Free online book covering attribution methods with worked examples.
