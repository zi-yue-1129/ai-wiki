---
tags:
  - semi-supervised learning
  - theory
---

# Theory and Assumptions

Unlabelled data help only under certain assumptions about how inputs and labels relate. This page covers the main assumptions, why unlabelled data can also hurt, and how to tell which regime a problem is in.

## Overview

A semi-supervised learner has to assume something about the unlabelled data. Without that, unlabelled examples carry no information about labels. The standard assumptions are the smoothness assumption, the cluster assumption, and the manifold assumption. Each suggests a different kind of method.

## Core assumptions

- **Smoothness:** if two points are close, their labels are likely the same. This justifies consistency regularisation and kernel smoothing.
- **Cluster:** points in the same cluster share a label, and decision boundaries pass through low-density regions. This justifies self-training and transductive SVMs.
- **Manifold:** the data lie on a low-dimensional manifold, and smoothness is measured along it. This justifies graph methods and manifold regularisation.

## When unlabelled data hurt

Singh, Nowak & Zhu (2008) showed that unlabelled data can improve or worsen accuracy depending on whether the assumptions match the data. If the true decision boundary cuts through dense regions, cluster-based methods push the boundary into the wrong place. Models that assume the wrong structure can be worse than supervised baselines.

## Practical checks

Compare against a strong supervised baseline with the same labelled data, use the same budget and tuning for each method, and report results across several label-set sizes. Evaluation protocols that tune on the full labelled set can hide failure, as Oliver et al. (2018) found for many methods.

## Connections

The assumptions correspond to the methods in [consistency regularisation](../consistency-regularisation/index.md), [graph-based methods](../graph-based-methods/index.md) and [pseudo-labelling](../pseudo-labelling-and-self-training/index.md). The bias–variance reasoning from [generalisation theory](../../supervised/generalization-theory/index.md) applies: unlabelled data reduce variance only if the assumed structure is correct.

## Applications

Choosing between semi-supervised and supervised approaches for a new dataset, deciding how many labels to collect before relying on unlabelled data, and diagnosing when a semi-supervised model underperforms.

## Open questions

Formal conditions under which unlabelled data provably help are still limited, and most results are for simple models. Connecting these assumptions to the structure of modern deep networks is an active area.

## References

### Seminal papers

- Singh, Nowak & Zhu (2008), "Unlabeled data: now it helps, now it doesn't", NeurIPS. https://proceedings.neurips.cc/paper/2008/hash/07871915a8107172b3b5dc15a6574ad3-Abstract.html — Gives conditions under which unlabelled data help and when they hurt.
- Belkin, Niyogi & Sindhwani (2006), "Manifold regularization: a geometric framework for learning from labeled and unlabeled examples", *JMLR* 7. https://www.jmlr.org/papers/v7/belkin06a.html — Formalises the manifold assumption as a regulariser.
- Zhou, Bousquet, Lal, Weston & Schölkopf (2004), "Learning with local and global consistency", NeurIPS. https://papers.nips.cc/paper/2506-learning-with-local-and-global-consistency — Formalises the smoothness trade-off between labelled fit and graph consistency.
- Zhu, Ghahramani & Lafferty (2003), "Semi-supervised learning using Gaussian fields and harmonic functions", ICML. https://mlanthology.org/icml/2003/zhu2003icml-semi/ — Shows how graph smoothness turns unlabelled data into labels.

### Surveys and textbooks

(none checked for this page)

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Oliver, Odena, Raffel, Cubuk & Goodfellow (2018), "Realistic evaluation of deep semi-supervised learning algorithms", NeurIPS, arXiv:1804.09170 — Shows how the gains from many methods depend on the evaluation protocol.

## Further reading

- Chapelle, Schölkopf & Zien (eds.), *Semi-Supervised Learning*, MIT Press (2006). No free link checked.
