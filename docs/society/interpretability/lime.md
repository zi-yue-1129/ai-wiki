---
status: draft
last_reviewed: 2026-10-28
related:
  - society/interpretability
tags:
  - interpretability
  - explainable AI
  - surrogate models
aliases:
  - 局部可解釋模型
  - LIME
  - Local interpretable model-agnostic explanations
---

# LIME

!!! info "Part of Feature attribution"
    This method page belongs to [Feature attribution](feature-attribution.md). It explains the method in detail; the overview compares it with the other methods.

LIME (Local Interpretable Model-agnostic Explanations) explains one prediction of any classifier by fitting a simple, interpretable model to the classifier's behaviour in the neighbourhood of that input. Ribeiro, Singh and Guestrin (2016) introduced it, and the method works without access to the model's internals.

## Problem

A complex classifier may be accurate, but a user who must act on one prediction needs to know why it was made. The problem is to explain a single decision, using only the model's inputs and outputs, in terms a person can read.

## Core idea

Perturb the input to create many nearby samples, record the classifier's output for each, and weight the samples by how close they are to the original. Fit a sparse linear model to these weighted samples. The coefficients of that model are the explanation, and they are faithful only near the original input.

## Equation

LIME chooses the explanation \(\xi(x)\) as the interpretable model \(g\) that balances local fidelity and simplicity:

\[
\xi(x) = \operatorname*{argmin}_{g \in G} \; \mathcal{L}(f, g, \pi_x) + \Omega(g),
\]

where \(f\) is the classifier, \(\pi_x\) is the proximity weighting around \(x\), \(\mathcal{L}\) measures how poorly \(g\) matches \(f\) near \(x\), and \(\Omega(g)\) penalises complexity.

## Results

The paper reports simulated experiments and experiments with human subjects. The human-subject studies ask whether explanations help people decide whether to trust a prediction, and whether they help choose between models. The results support the usefulness of the explanations for these decisions, not their accuracy as descriptions of the model.

## Limitations

- **Local only.** The explanation describes the model near one input and may not hold for others.
- **Instability.** Because the perturbations are random, repeated runs can give different explanations unless the sampling is controlled.
- **Representation choice.** The interpretable features (for example, words or superpixels) are chosen by the designer and shape the explanation.
- **Fidelity.** A low-complexity surrogate can look convincing while misrepresenting the model; this must be measured.

## References

### Seminal papers

- Ribeiro, M. T., Singh, S. & Guestrin, C. (2016). "Why Should I Trust You?": Explaining the Predictions of Any Classifier. *Proceedings of KDD 2016*. https://arxiv.org/abs/1602.04938 — Introduces LIME and reports both simulated and human-subject experiments.
- Lundberg, S. M. & Lee, S.-I. (2017). A Unified Approach to Interpreting Model Predictions. *Advances in Neural Information Processing Systems 30*. https://arxiv.org/abs/1705.07874 — Presents SHAP, a related additive method that unifies six existing explanation methods.
- Štrumbelj, E. & Kononenko, I. (2014). Explaining prediction models and individual predictions with feature contributions. *Knowledge and Information Systems*, 41(3), 647–665. https://doi.org/10.1007/s10115-013-0679-x — Explains individual predictions of general models with feature contributions based on Shapley values.

### Surveys and textbooks

- Sundararajan, M., Taly, A. & Yan, Q. (2017). Axiomatic Attribution for Deep Networks. *Proceedings of ICML 2017*. https://arxiv.org/abs/1703.01365 — A gradient-based alternative for neural networks, for comparison.
- Molnar, C. *Interpretable Machine Learning: A Guide for Making Black Box Models Explainable*, 3rd edition. https://christophm.github.io/interpretable-ml-book/ — Free online book with a chapter on local surrogate models, including LIME.
