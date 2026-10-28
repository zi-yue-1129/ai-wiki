---
related:
- theory/paradigms/semi-supervised/index.md
- engineering/training/index.md
tags:
  - active learning
  - annotation cost
  - human-in-the-loop
---

# Practice and Labelling Cost

In practice, active learning is judged by how much annotation effort it saves, including the cost of the initial labels, the time to retrain and the human work needed to label. This subtopic covers the practical questions that decide whether an active labelling campaign is worth running: the cold-start problem, stopping rules and the cost of different query strategies.

## Overview

Real projects start with no labels, so the first queries are chosen with weak models. Annotators may be slow, inconsistent or expensive, and the cost of a label can depend on the example. Active learning succeeds when the savings in labels outweigh the costs of selection, retraining and waiting for annotation.

## Practical issues

- **Cold start**: with no labels, use diverse or self-supervised representations to pick the first batch, rather than uncertainty from a random model.
- **Stopping rules**: decide when further labelling is no longer improving the model, using a held-out labelled set or a stability criterion.
- **Annotation cost**: weight the selection by the expected cost of each label, or prefer examples that are quick to label.
- **Comparison with random sampling**: always compare against a random baseline, because active strategies can underperform it on some datasets.

## Connections

Cold-start representations come from [self-supervised learning](../../self-supervised/index.md), and combining labelled data with unlabelled data is [semi-supervised learning](../../semi-supervised/index.md). Practical training pipelines are covered in [training and fine-tuning](../../../../engineering/training/index.md).

## Applications

Labelling campaigns for medical images, clinical text and industrial inspection, where each label is expensive and a small improvement in label efficiency has a large effect on cost.

## Open questions

Little is known about how annotator behaviour interacts with query strategies, and benchmarks rarely report the cost of selection or retraining. Reliable stopping rules for deep models remain difficult.

## References

### Seminal papers

- Lewis & Gale (1994), "A sequential algorithm for training text classifiers", SIGIR, https://arxiv.org/abs/cmp-lg/9407020 — Sequential uncertainty sampling for text, where the labelling savings were first shown in practice.
- MacKay (1992), "Information-based objective functions for active data selection", Neural Computation. https://authors.library.caltech.edu/records/efefp-2j353 — Shows how to choose data by expected information gain, a basis for cost-aware selection.
- Kirsch, van Amersfoort & Gal (2019), "BatchBALD: efficient and diverse batch acquisition for deep Bayesian active learning", NeurIPS, arXiv:1906.08158 — Batch selection that avoids redundant labels, which saves annotation effort.

### Surveys and textbooks

- Settles (2009), "Active learning literature survey", Computer Sciences Technical Report 1648, University of Wisconsin-Madison. https://research.cs.wisc.edu/techreports/2009/TR1648.pdf — Survey that discusses practical issues in running active learning projects.
- Ren et al. (2020), "A survey of deep active learning", arXiv:2009.00236 — Survey that compares the practical costs of deep active learning methods.

### Lectures and videos

No further entries for this page.

### Articles and documentation

No further entries for this page.

## Further reading

- Yoo & Kweon (2019), "Learning loss for active learning", CVPR, arXiv:1905.03677 — Loss-prediction approach that avoids retraining for each query.
