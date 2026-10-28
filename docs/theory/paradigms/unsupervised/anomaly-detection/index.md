---
tags:
  - unsupervised learning
  - anomaly detection
---

# Anomaly Detection

Anomaly detection finds rare inputs that differ from the normal data, often without any labelled anomalies. It matters for fraud, equipment faults, network intrusions and quality control.

## Overview

Most data are normal and anomalies are rare, so supervised classifiers have too few examples to learn from. Anomaly detectors instead model what normal looks like and score how far each new point departs from it. The threshold is a business decision, and a score is only useful if its false-alarm rate is acceptable.

## Main approaches

| Approach | Idea | Examples |
|---|---|---|
| Density-based | Low estimated density means anomalous | Gaussian models, normalising flows |
| Distance-based | Anomalies are far from their neighbours | kNN distance, LOF |
| Isolation-based | Anomalies are isolated by few random splits | Isolation Forest |
| Boundary-based | Learn a region that contains normal data | One-class SVM |
| Reconstruction-based | Anomalies reconstruct poorly | Autoencoders, PCA residuals |

## How the main methods work

**Isolation Forest** builds random trees that split on random features and thresholds. Anomalous points are separated after few splits, so their average path length is short. It scales well and needs little tuning.

**Local outlier factor (LOF)** compares the local density around each point with the density of its neighbours. A point in a sparse area next to dense neighbours gets a high score.

**One-class SVM** finds a boundary, in a kernel feature space, that encloses most of the training data and leaves few points outside. The parameter $\nu$ bounds the fraction of training points treated as outliers.

**Reconstruction error** uses an autoencoder or PCA trained on normal data. Inputs with high error lie outside the learned normal subspace.

## Evaluation

Anomalies are rare, so accuracy is misleading. Precision-recall curves, precision at a fixed alert budget, and time-aware validation (train on the past, test on the future) are more useful. Labels, when available, usually come from investigators and may be incomplete.

## Connections

Density models give anomaly scores directly, see [density estimation](../density-and-generative-models/index.md). Reconstruction-based detection uses [autoencoders](../autoencoders-and-representations/index.md). Under distribution shift, what counts as normal changes over time, a topic linked to [continual learning](../../continual/index.md).

## Applications

Credit-card fraud, industrial sensor monitoring, network intrusion detection, medical signal monitoring, and flagging unusual transactions for review. In cybersecurity it is closely linked to [threat detection](../../../../applications/cybersecurity/index.md).

## Open questions

Defining normal for data that drift, separating harmful anomalies from merely rare ones, and explaining to analysts why a point was flagged are open practical problems.

## References

### Seminal papers

- Liu, F. T., Ting, K. M. & Zhou, Z.-H. (2008). Isolation forest. *ICDM*. https://doi.org/10.1109/ICDM.2008.17 — Introduces Isolation Forest, which isolates anomalies with random splits.
- Breunig, Kriegel, Ng & Sander (2000), "LOF: identifying density-based local outliers", SIGMOD. https://cs.fit.edu/~pkc/ml/related/breunig00sigmod.pdf — Defines the local outlier factor, a score based on relative local density.
- Schölkopf, Platt, Shawe-Taylor, Smola & Williamson (2001), "Estimating the support of a high-dimensional distribution", *Neural Computation* 13(7). https://doi.org/10.1162/089976601750264965 — Introduces the one-class SVM for novelty detection.

### Surveys and textbooks

- Chandola, Banerjee & Kumar (2009), "Anomaly detection: a survey", *ACM Computing Surveys* 41(3). https://doi.org/10.1145/1541880.1541882 — Classic survey organising anomaly detection methods by the kind of data and anomaly.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Pang, Shen, Cao & van den Hengel (2021), "Deep learning for anomaly detection: a review", [arXiv:2007.02500](https://arxiv.org/abs/2007.02500) — Reviews deep anomaly detection methods and their assumptions.

## Further reading

- Aggarwal, *Outlier Analysis*, 2nd ed., Springer (2017). https://doi.org/10.1007/978-3-319-47578-3 — Textbook on outlier detection methods across data types.
