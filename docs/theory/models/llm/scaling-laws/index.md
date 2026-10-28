---
status: complete
last_reviewed: 2026-10-28
related:
  - theory/models/llm
  - theory/deep-learning
tags:
  - scaling laws
  - power laws
  - emergent abilities
  - compute
aliases:
  - Scaling laws
  - Neural scaling laws
  - 縮放定律
  - Emergent abilities
---

# Scaling laws

Neural scaling laws are empirical power-law relations between a model's loss and its size, its training data and the compute spent on training. They let a team predict the loss of a larger run from smaller ones, and they set the question of how a fixed budget should be split. Part of [Large Language Models](../index.md).

## Overview

Hestness et al. (2017) showed that the generalisation error of several deep networks falls as a power law in the amount of training data. Kaplan et al. (2020) fitted the same kind of law for Transformer language models over model size, data and compute, with trends that held across many orders of magnitude. Henighan et al. (2020) found similar behaviour in other domains, such as images, video and mathematics. These results turned scale from a rule of thumb into a quantity that can be planned around. Later work revised how the budget should be split (see [Compute-optimal training](../compute-optimal-training/index.md)).

A second line of work asks about abilities rather than loss. Wei et al. (2022) listed tasks on which small models score near chance and larger models score well, and called these abilities emergent. Schaeffer et al. (2023) argue that the apparent sharpness depends on the choice of metric.

## Key concepts

- **Power law**: a relation of the form \(y \propto x^{-\alpha}\), which is a straight line on a log–log plot.
- **Loss**: the cross-entropy the model achieves on held-out text, which the scaling laws describe.
- **Compute**: the total training operations, roughly proportional to the parameter count times the number of training tokens.
- **Irreducible loss**: a floor that the loss approaches as size and data grow, due to the entropy of the data itself.
- **Emergent ability**: a capability that is absent in smaller models and present in larger ones, as observed on a chosen metric.

## Problem

How does the loss depend on the number of parameters \(N\), the number of training tokens \(D\) and the compute \(C\), and how should a fixed budget be divided between \(N\) and \(D\)?

## How it works

The usual form fits the held-out loss as a sum of a floor and two power-law terms:

\[
\hat L(N, D) = E + \frac{A}{N^{\alpha}} + \frac{B}{D^{\beta}},
\]

where \(E\), \(A\), \(B\), \(\alpha\) and \(\beta\) are fitted from many training runs. The fit is then used to predict larger runs, and to choose \(N\) and \(D\) for a compute budget \(C \approx 6ND\).

The budget question can be answered in two ways. Kaplan et al. (2020) found that the best use of extra compute favoured a larger model trained on a modest amount of data. Hoffmann et al. (2022) redid the fit with more careful training runs and found that model size and data should grow in roughly equal proportion. The two answers differ, and the disagreement is the main point of the compute-optimal line of work.

## Key methods

- [Kaplan scaling laws](kaplan-scaling-laws.md): the first detailed fit of power laws for Transformer language models, and the source of the question about how to split a budget.
- [Compute-optimal training](../compute-optimal-training/index.md): the revised split, which ties model size to the number of training tokens.

## Variants

- **Loss scaling** fits the held-out loss as the main quantity, as in Kaplan et al. (2020).
- **Downstream scaling** fits the score on a particular task, which can show abrupt changes that the loss does not.
- **Cross-domain scaling** fits the same laws for images, video or other modalities (Henighan et al., 2020).

## Results and limits

- Loss falls smoothly as a power law in parameters, data and compute over a wide range (Kaplan et al., 2020). Hestness et al. (2017) found similar power laws for other deep networks.
- Emergent abilities appear as sharp jumps when the score is a threshold-like metric, and the sharpness is reduced or removed with a smoother metric (Schaeffer et al., 2023). Wei et al. (2022) document the jumps on the metrics they used.
- Extrapolating a fit beyond the range it was measured on is uncertain. The fitted exponents and constants depend on the data, the architecture and the training schedule.
- Scaling laws describe averages over many models. They say little about any single capability, which may appear at a different scale.

## Applications

- **Planning training runs**: predicting the loss of a large run from cheaper experiments before committing the budget.
- **Choosing model size and data**: applying the compute-optimal rule to a fixed budget.
- **Evaluating claims about emergence**: checking whether a sudden change depends on the chosen metric.

## Open questions

- Do scaling laws hold for downstream tasks and for reasoning, or only for the held-out loss?
- Which abilities are truly emergent, and which become sharp only because of the metric?
- How should scaling laws change when inference cost and data quality, rather than only training compute, limit a project?

## Connections

- Parent topic: [Large Language Models](../index.md)
- Related: [Deep Learning](../../../deep-learning/index.md), where the power laws of deep networks are discussed as a general pattern
- Other method on this topic: [Compute-optimal training](../compute-optimal-training/index.md)

## References

### Seminal papers

- Kaplan, J. et al. (2020). Scaling Laws for Neural Language Models. arXiv:2001.08361. https://arxiv.org/abs/2001.08361 — Fits power laws of loss against model size, data and compute for Transformer language models.
- Hoffmann, J. et al. (2022). Training Compute-Optimal Large Language Models. arXiv:2203.15556. https://arxiv.org/abs/2203.15556 — Redoes the fit and argues that model size and training tokens should grow together for a fixed budget.
- Hestness, J. et al. (2017). Deep Learning Scaling is Predictable, Empirically. arXiv:1712.00409. https://arxiv.org/abs/1712.00409 — Shows power-law improvement of generalisation error with data across several deep-learning tasks.
- Henighan, T. et al. (2020). Scaling Laws for Autoregressive Generative Modeling. arXiv:2010.14701. https://arxiv.org/abs/2010.14701 — Extends the power-law fits to image, video and mathematics models.
- Brown, T. B. et al. (2020). Language Models are Few-Shot Learners. arXiv:2005.14165. https://arxiv.org/abs/2005.14165 — The GPT-3 study, whose large models display the abilities discussed in the emergence debate.

### Surveys and textbooks

- Wei, J. et al. (2022). Emergent Abilities of Large Language Models. *Transactions on Machine Learning Research*. arXiv:2206.07682. https://arxiv.org/abs/2206.07682 — Defines emergent abilities as those absent in small models and present in large ones, and lists examples.
- Schaeffer, R., Miranda, B. & Koyejo, S. (2023). Are Emergent Abilities of Large Language Models a Mirage? In *NeurIPS 2023*. arXiv:2304.15004. https://arxiv.org/abs/2304.15004 — Argues that apparent emergence depends on nonlinear or discontinuous metrics.
