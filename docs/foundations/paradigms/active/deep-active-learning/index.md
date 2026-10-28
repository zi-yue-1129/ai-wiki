---
related:
- foundations/paradigms/self-supervised/index.md
- models/llm/index.md
tags:
  - active learning
  - deep learning
  - loss prediction
---

# Deep Active Learning

Deep active learning applies query strategies to neural networks, which are trained on large amounts of data and produce uncertainty estimates that are harder to trust than those of classical models. Methods address this by estimating uncertainty more reliably, by learning to predict the loss of unlabelled examples, or by choosing representative examples in the network's feature space.

## Overview

Classical strategies were designed for small models. Deep networks need many labels to train, so the initial labelled set is often small and noisy, and retraining at every query is expensive. Deep active learning therefore combines acquisition with efficient training, and it often works with embeddings produced by pre-trained or self-supervised models.

## Main approaches

- **Bayesian approximations**: dropout or ensembles give uncertainty estimates for deep networks, which feed standard acquisition functions.
- **Learning to predict loss**: train a small module to predict the loss of each unlabelled example and query the examples predicted to have high loss.
- **Representation-based selection**: query examples that cover the feature space of the network, which often works well with self-supervised features.
- **Joint acquisition and training**: balance the cost of retraining with the benefit of each query, especially for very large models.

## Connections

Deep active learning uses the uncertainty ideas of [uncertainty sampling](../uncertainty-sampling/index.md) and the batch methods of [batch and diversity](../batch-and-diversity/index.md). Self-supervised embeddings are often the feature space used for selection, see [self-supervised learning](../../self-supervised/index.md). Language models have also been used to choose examples for labelling, see [large language models](../../../../models/llm/index.md).

## Applications

Labelling medical and satellite images, selecting training data for speech and object detection systems, and choosing prompts or examples for human annotation of language data.

## Open questions

Uncertainty from deep networks is often poorly calibrated, and retraining is costly. Results from active learning benchmarks sometimes disappear when strong random baselines or better training recipes are used.

## References

### Seminal papers

- Gal, Islam & Ghahramani (2017), "Deep Bayesian active learning with image data", ICML, arXiv:1703.02910 — Uses dropout-based uncertainty estimates to make active learning work with deep networks on images.
- Yoo & Kweon (2019), "Learning loss for active learning", CVPR, arXiv:1905.03677 — Trains a module to predict the loss of unlabelled examples and queries those with high predicted loss.
- Sener & Savarese (2018), "Active learning for convolutional neural networks: a core-set approach", ICLR, arXiv:1708.00489 — Selects examples that cover the feature space, a strong deep baseline.

### Surveys and textbooks

- Ren et al. (2020), "A survey of deep active learning", arXiv:2009.00236 — Survey of active learning methods for deep networks, with a taxonomy of approaches.
- Settles (2009), "Active learning literature survey", Computer Sciences Technical Report 1648, University of Wisconsin-Madison. https://research.cs.wisc.edu/techreports/2009/TR1648.pdf — Foundational survey that predates deep learning but defines the basic query strategies.

### Lectures and videos

No further entries for this page.

### Articles and documentation

No further entries for this page.

## Further reading

- Kirsch, van Amersfoort & Gal (2019), "BatchBALD: efficient and diverse batch acquisition for deep Bayesian active learning", NeurIPS, arXiv:1906.08158 — Batch acquisition for deep Bayesian active learning.
