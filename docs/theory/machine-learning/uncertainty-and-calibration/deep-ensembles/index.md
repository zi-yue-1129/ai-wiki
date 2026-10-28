---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/supervised/trees-and-ensembles
tags:
  - uncertainty
  - deep learning
  - ensembles
aliases:
  - 深度集成
  - Deep Ensembles
---

# Deep Ensembles

A deep ensemble trains several copies of the same neural network from different random starting points, then averages their predictions. The spread among the copies is a practical estimate of epistemic uncertainty. Lakshminarayanan, Pritzel and Blundell (2017) proposed the method as a simple alternative to [Bayesian neural networks](../index.md).

## Overview

Deep networks are powerful predictors, but a single network gives no reliable sense of how much to trust a given output. Bayesian neural networks offer a principled answer, but they require changes to the training procedure and are expensive. Lakshminarayanan et al. (2017) offered a different route. Their abstract describes a method that is simple to implement, readily parallelisable, needs little hyperparameter tuning, and yields high-quality predictive uncertainty. The idea is ensembling, a classic way to reduce variance, applied to networks that also report their own noise.

## Key concepts

- **Ensemble member.** One network, with its own random initialisation and, usually, its own ordering of the training data.
- **Proper scoring rule.** Each member is trained with a loss, such as negative log-likelihood, that rewards honest probabilities.
- **Diversity.** Ensembles help only when the members disagree on inputs they are unsure about. Members that make the same mistakes add little.

## How it works

For classification, each member \(m\) outputs a probability \(p_m(y \mid x)\). The ensemble predicts the average:

\[
p(y \mid x) = \frac{1}{M}\sum_{m=1}^{M} p_m(y \mid x).
\]

For regression, each member outputs a mean \(\mu_m(x)\) and a variance \(\sigma^2_m(x)\). Treating the members as an equally weighted mixture of Gaussians, the ensemble mean and variance are

\[
\mu_*(x) = \frac{1}{M}\sum_{m=1}^{M}\mu_m(x), \qquad
\sigma^2_*(x) = \frac{1}{M}\sum_{m=1}^{M}\big(\sigma^2_m(x) + \mu_m(x)^2\big) - \mu_*(x)^2.
\]

Each member minimises the negative log-likelihood, which for a Gaussian output is, up to a constant, \(\frac{(y-\mu)^2}{2\sigma^2} + \tfrac{1}{2}\log \sigma^2\).

The procedure is as follows.

1. Choose one architecture and a proper scoring rule for the output.
2. Train \(M\) copies independently, each from a different random initialisation and data order.
3. For a new input, run all \(M\) members and combine their outputs with the formulas above.
4. Use the spread, not only the average, as the uncertainty.

## Results

The abstract reports that the method produces well-calibrated uncertainty estimates on classification and regression benchmarks, and that these are as good as or better than those of approximate Bayesian neural networks. On test examples from unseen distributions, the method expresses higher uncertainty, which is the behaviour one wants when the model is out of its depth. The authors also report that the approach scales to ImageNet. The exact numbers are in the paper and were not re-run for this page.

## Limitations

- **Cost.** Training and running \(M\) networks multiplies the compute and memory needed, although the copies can run in parallel.
- **Limited diversity.** Members that differ only in their random seed may end up in similar solutions, which reduces the benefit of averaging.
- **Not an exact posterior.** The ensemble is an approximation to Bayesian averaging. Wilson and Izmailov (2020) argue that it is effective, but it is not the same as integrating over a posterior.
- **Shift is not solved.** Ovadia et al. (2019) found that methods which marginalise over models gave surprisingly strong results under dataset shift, but accuracy and calibration still degrade as inputs move away from the training data.

## Open questions

- How can diversity be increased cheaply, through different architectures, data subsets or training objectives?
- Can an ensemble be compressed into a single network without losing its calibration, for example through [knowledge distillation](../../../model-compression/knowledge-distillation/index.md)?
- Which members should be trusted when the ensemble is large but its members systematically agree on the wrong answer?

## Connections

The method extends a familiar idea from classical learning. [Trees and ensembles](../../../paradigms/supervised/trees-and-ensembles/index.md) combine many weak models to reduce variance, and deep ensembles apply the same averaging to networks whose outputs also carry uncertainty. The [probabilistic methods](../../../probabilistic/index.md) page describes the Bayesian view that the ensemble approximates, and [MC dropout](../mc-dropout/index.md) is the cheaper approximation that uses a single network. The brain-mind link is only an analogy: people weight several noisy cues by reliability (Ernst and Banks, 2002), but that does not show the brain runs an ensemble.

## References

### Seminal papers

- Lakshminarayanan, B., Pritzel, A. & Blundell, C. (2017). Simple and scalable predictive uncertainty estimation using deep ensembles. NeurIPS. https://arxiv.org/abs/1612.01474 — Proposes training an ensemble of networks with a proper scoring rule as a simple, scalable alternative to Bayesian neural networks.
- Ernst, M. O. & Banks, M. S. (2002). Humans integrate visual and haptic information in a statistically optimal fashion. *Nature*. https://doi.org/10.1038/415429a — Shows that people weight sensory cues by their reliability, the analogy used in the connections section.

### Surveys and textbooks

- Wilson, A. G. & Izmailov, P. (2020). Bayesian deep learning and a probabilistic perspective of generalization. NeurIPS. https://arxiv.org/abs/2002.08791 — Argues that deep ensembles provide an effective approximation to Bayesian marginalisation.
- Gawlikowski, J. et al. (2021). A survey of uncertainty in deep neural networks. arXiv. https://arxiv.org/abs/2107.03342 — Surveys uncertainty sources and estimation methods for deep networks.
- Hüllermeier, E. & Waegeman, W. (2021). Aleatoric and epistemic uncertainty in machine learning: an introduction to concepts and methods. *Machine Learning*. https://arxiv.org/abs/1910.09457 — Introduces the aleatoric and epistemic distinction that ensemble spread is used to address.

### Articles and documentation

- Ovadia, Y. et al. (2019). Can you trust your model's uncertainty? Evaluating predictive uncertainty under dataset shift. NeurIPS. https://arxiv.org/abs/1906.02530 — Benchmark in which methods that marginalise over models give strong results under dataset shift.
