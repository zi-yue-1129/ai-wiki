---
related:
- theory/paradigms/continual/index.md
- engineering/mlops/index.md
tags:
  - online learning
  - data streams
  - concept drift
---

# Streaming and Concept Drift

Data streams arrive continuously and cannot be stored in full, and their distribution can change over time. Learners for streams must process each example once, use bounded memory, and detect or adapt to drift when the relation between inputs and labels changes.

## Overview

Two problems come together. The first is efficiency: algorithms such as Hoeffding trees grow decision trees from a stream with statistical guarantees on how many examples each split needs. The second is drift: the concept may change abruptly, gradually or recurrently, and the learner must notice the change and update or replace its model.

## Main approaches

- **Incremental trees**: grow decision trees from a stream, splitting a node once enough examples support the split.
- **Drift detection**: monitor the error rate or a statistic of the stream and signal drift when it changes significantly.
- **Windowing and forgetting**: train on a recent window of data, or weight recent examples more heavily, so that old concepts fade.
- **Ensembles for drift**: keep several models trained on different periods and combine or replace them as the stream changes.

## Connections

Drift adaptation is closely related to [continual learning](../../continual/index.md), where the goal is to keep old knowledge while learning new tasks. Monitoring and retraining models in production are part of [MLOps](../../../../engineering/mlops/index.md). Stream learners are also online learners in the regret sense, see [online convex optimisation](../online-convex-optimisation/index.md).

## Applications

Fraud and intrusion detection on transaction streams, sensor monitoring in industry, and recommendation models that must track changing user interests.

## Open questions

Distinguishing real drift from noise is difficult, and drift detectors can raise many false alarms. Evaluation is also hard, because the test data is itself a stream whose distribution changes.

## References

### Seminal papers

- Domingos & Hulten (2000), "Mining high-speed data streams", KDD. https://homes.cs.washington.edu/~pedrod/papers/kdd00.pdf — Hoeffding trees, which learn decision trees from high-speed streams with statistical guarantees.
- Bottou (2010), "Large-scale machine learning with stochastic gradient descent", COMPSTAT. https://leon.bottou.org/papers/bottou-2010 — Shows how one-pass stochastic gradient methods handle data too large to store.

### Surveys and textbooks

- Gama, Žliobaitė, Bifet, Pechenizkiy & Bouchachia (2014), "A survey on concept drift adaptation", ACM Computing Surveys. https://doi.org/10.1145/2523813 — Survey of drift types, detection methods and adaptation strategies.
- Hoi, Sahoo, Lu & Zhao (2018), "Online learning: a comprehensive survey", arXiv:1802.02871 — Survey that includes streaming and drift settings within online learning.
- Shalev-Shwartz (2012), "Online learning and online convex optimization", Foundations and Trends in Machine Learning. https://www.cs.huji.ac.il/~shais/papers/OLsurvey.pdf — Survey of the online learning framework that underlies stream learners.

### Lectures and videos

No further entries for this page.

### Articles and documentation

No further entries for this page.

## Further reading

- Bifet & Gavaldà (2007), "Learning from time-changing data with adaptive windowing", *Proceedings of the 2007 SIAM International Conference on Data Mining* (SDM). https://doi.org/10.1137/1.9781611972771.42 — Introduces an adaptive window for detecting changes in streaming data.
