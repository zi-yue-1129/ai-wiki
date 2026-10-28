---
related:
- theory/paradigms/active/uncertainty-sampling/index.md
tags:
  - active learning
  - batch acquisition
  - diversity
---

# Batch and Diversity-based Active Learning

Selecting one example at a time is slow when labelling happens in batches, as it does in practice. Choosing the top-k uncertain examples often selects near-duplicates, so batch methods balance how informative each example is with how different the examples are from one another.

## Overview

Batch acquisition asks for a set of examples that is jointly informative. Diversity methods spread the batch over the input space, while Bayesian batch methods score a whole batch by the information it provides about the model parameters. Gradient-based methods use the direction in which each example would move the model, and they choose examples that point in different directions.

## Main methods

- **Core-set selection**: choose a batch that covers the unlabelled pool well, so that every region of the input space is close to a labelled example.
- **Gradient-embedding methods**: represent each example by the gradient it would induce and choose a batch that is both large in magnitude and diverse in direction.
- **BatchBALD**: score batches by their joint mutual information, which avoids selecting redundant examples that carry the same information.

## Connections

Batch selection builds on [uncertainty sampling](../uncertainty-sampling/index.md), and diversity is the input-space counterpart of the coverage ideas in [clustering](../../unsupervised/clustering/index.md). The labelled batches are then used in ordinary [supervised learning](../../supervised/index.md).

## Applications

Labelling large pools of images for an object detector in a fixed annotation budget, selecting text for legal review, and choosing experiments in scientific settings where each batch is run together.

## Open questions

Computing joint informativeness is expensive for large models and large batches. The best trade-off between uncertainty and diversity depends on the data, and gains over random sampling are not always large.

## References

### Seminal papers

- Sener & Savarese (2018), "Active learning for convolutional neural networks: a core-set approach", ICLR, arXiv:1708.00489 — Selects a batch that covers the unlabelled pool, which gives a strong diversity baseline for deep networks.
- Ash, Zhang, Krishnamurthy, Langford & Agarwal (2020), "Deep batch active learning by diverse, uncertain gradient lower bounds", ICLR, arXiv:1906.03671 — BADGE, which picks a batch of gradient embeddings that is both uncertain and diverse.
- Kirsch, van Amersfoort & Gal (2019), "BatchBALD: efficient and diverse batch acquisition for deep Bayesian active learning", NeurIPS, arXiv:1906.08158 — Scores batches by their joint mutual information, which discourages redundant examples.

### Surveys and textbooks

- Settles (2009), "Active learning literature survey", Computer Sciences Technical Report 1648, University of Wisconsin-Madison. https://research.cs.wisc.edu/techreports/2009/TR1648.pdf — Survey covering batch and diversity-based query strategies.
- Ren et al. (2020), "A survey of deep active learning", arXiv:2009.00236 — Survey that discusses batch and diversity strategies for deep networks.

### Lectures and videos

No further entries for this page.

### Articles and documentation

No further entries for this page.

## Further reading

- Hoi, Jin, Zhu & Lyu (2006), "Batch mode active learning and its application to medical image classification", ICML. No link checked.
