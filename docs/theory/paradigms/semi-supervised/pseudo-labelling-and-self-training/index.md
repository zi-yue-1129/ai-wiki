---
tags:
  - semi-supervised learning
  - pseudo-labelling
  - self-training
---

# Pseudo-Labelling and Self-Training

Pseudo-labelling trains a model on its own confident predictions for unlabelled data, then retrains on the enlarged set. It is one of the simplest semi-supervised methods, and it is the core of many modern systems.

## Overview

Train a model on the labelled data. Predict labels for unlabelled examples, keep the predictions the model is most confident about, add them to the training set as pseudo-labels, and repeat. The method only works if the confident predictions are mostly right, so the selection rule matters as much as the training loop.

## How it is done

- **Thresholding** keeps predictions above a confidence cut-off, such as 0.95. This limits noisy labels but can ignore hard examples.
- **Soft targets** use the predicted probabilities directly as targets, which preserves uncertainty.
- **Class balancing** adjusts thresholds per class, so common classes do not dominate the pseudo-labels.
- **Iterative self-training** repeats the process, and each round can grow the training set. Errors can also compound across rounds.

Recent methods avoid manual thresholds by combining pseudo-labels with strong augmentation. Unsupervised Data Augmentation (Xie et al., 2020) and FixMatch both train on predictions made from clean inputs and apply the loss to augmented inputs.

## Failure modes

Confirmation bias is the central risk: the model reinforces its own mistakes, and wrong pseudo-labels become more confident over time. Class imbalance and distribution mismatch between labelled and unlabelled data make it worse.

## Connections

Pseudo-labelling is the discrete counterpart of [consistency regularisation](../consistency-regularisation/index.md). It also resembles the self-distillation used in [self-supervised learning](../../self-supervised/index.md), where a teacher supervises a student. Uncertainty estimates from [supervised calibration](../../supervised/evaluation-and-validation/index.md) determine how reliable the confidence threshold is.

## Applications

Speech recognition with unlabelled audio, text classification with few annotated documents, medical image segmentation with few expert masks, and large-scale web data curation.

## Open questions

Choosing thresholds without validation labels, detecting when self-training is making things worse, and keeping pseudo-labelled data balanced across groups are unresolved. Theoretical guarantees exist only under strong assumptions about the data.

## References

### Seminal papers

- Xie et al. (2020), "Unsupervised data augmentation for consistency training", NeurIPS, [arXiv:1904.12848](https://arxiv.org/abs/1904.12848) — Trains on predictions from clean inputs with strong augmented inputs, with large gains on text and image benchmarks.
- Sohn et al. (2020), "FixMatch: simplifying semi-supervised learning with consistency and confidence", NeurIPS, [arXiv:2001.07685](https://arxiv.org/abs/2001.07685) — Uses confident pseudo-labels with a simple threshold, a strong and simple baseline.
- Berthelot et al. (2019), "MixMatch: a holistic approach to semi-supervised learning", NeurIPS, [arXiv:1905.02249](https://arxiv.org/abs/1905.02249) — Sharpens averaged predictions to produce targets for unlabelled data.
- Laine & Aila (2017), "Temporal ensembling for semi-supervised learning", ICLR, [arXiv:1610.02242](https://arxiv.org/abs/1610.02242) — Uses averaged past predictions as smoother targets for unlabelled examples.

### Surveys and textbooks

(none checked for this page)

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Oliver, Odena, Raffel, Cubuk & Goodfellow (2018), "Realistic evaluation of deep semi-supervised learning algorithms", NeurIPS, [arXiv:1804.09170](https://arxiv.org/abs/1804.09170) — Shows how sensitive semi-supervised results are to the evaluation protocol.

## Further reading

- Lee (2013), "Pseudo-label: the simple and efficient semi-supervised learning method for deep neural networks", ICML 2013 Workshop on Challenges in Representation Learning. http://deeplearning.net/wp-content/uploads/2013/03/pseudo_label_final.pdf — Uses the network's own most probable class as the label for unlabelled data.
