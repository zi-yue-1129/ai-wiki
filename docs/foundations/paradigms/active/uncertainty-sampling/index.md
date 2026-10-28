---
related:
- foundations/paradigms/supervised/evaluation-and-validation/index.md
tags:
  - active learning
  - uncertainty sampling
  - query strategies
---

# Uncertainty Sampling and Query Strategies

Uncertainty sampling asks the model which unlabelled example it is least sure about, and sends that example to the annotator. It is the simplest and most widely used query strategy. Related strategies choose examples that a committee of models disagrees on, or examples that would change the model most if labelled.

## Overview

A query strategy scores each unlabelled example and selects the highest scorers for labelling. Least-confidence, margin and entropy are common uncertainty scores for classifiers. Query-by-committee measures disagreement between several models, and expected-model-change or information-based scores estimate how much a label would update the model.

## Main strategies

- **Least confidence, margin and entropy**: pick the example whose top predicted probabilities are closest, or whose predictive distribution has the highest entropy.
- **Query by committee**: train several models on the labelled data and query the example they disagree on most.
- **Information gain**: choose the example that maximises the expected reduction in uncertainty about model parameters, which can be computed in closed form for some Bayesian models.
- **Bayesian uncertainty for deep networks**: estimate uncertainty with dropout or ensembles so that the same strategies apply to neural networks.

## Connections

Uncertainty sampling depends on well-calibrated probabilities, which connects to [evaluation and validation](../../supervised/evaluation-and-validation/index.md) in supervised learning. Choosing informative examples is closely related to [semi-supervised learning](../../semi-supervised/index.md), where unlabelled data is used without labels, and to the interactive labelling of [imitation learning](../../imitation/interactive-imitation/index.md).

## Applications

Labelling medical images where expert time is scarce, building text classifiers from a small seed set, and selecting sensor readings to label in scientific experiments.

## Open questions

Uncertainty estimates are often poorly calibrated for deep networks, which makes the selected examples less useful. Uncertainty sampling can also select outliers or repeatedly sample from a narrow region of the input space.

## References

### Seminal papers

- Lewis & Gale (1994), "A sequential algorithm for training text classifiers", SIGIR, https://arxiv.org/abs/cmp-lg/9407020 — Introduces uncertainty sampling for text classification, labelling the examples the classifier is least sure about.
- MacKay (1992), "Information-based objective functions for active data selection", Neural Computation. https://authors.library.caltech.edu/records/efefp-2j353 — Chooses data by expected information gain under a Bayesian model.
- Gal, Islam & Ghahramani (2017), "Deep Bayesian active learning with image data", ICML, arXiv:1703.02910 — Estimates uncertainty for deep networks with dropout, so that standard acquisition functions work on image data.

### Surveys and textbooks

- Settles (2009), "Active learning literature survey", Computer Sciences Technical Report 1648, University of Wisconsin-Madison. https://research.cs.wisc.edu/techreports/2009/TR1648.pdf — Broad survey of query strategies, the scenarios they apply to and their practical behaviour.
- Ren et al. (2020), "A survey of deep active learning", arXiv:2009.00236 — Survey of active learning methods for deep networks, with a taxonomy of query strategies.

### Lectures and videos

No further entries for this page.

### Articles and documentation

No further entries for this page.

## Further reading

- Seung, Opper & Sompolinsky (1992), "Query by committee", COLT. No link checked.
