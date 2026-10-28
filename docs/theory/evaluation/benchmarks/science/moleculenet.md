---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - science
---

# MoleculeNet

MoleculeNet is a benchmark for molecular machine learning. It gathers public datasets for predicting molecular properties and fixes shared splits and metrics, so that new methods are compared on the same data (Wu et al., 2018).

## Task and data

A model takes a molecule, usually as a graph or a fingerprint, and predicts a property. The properties span quantum mechanics, physical chemistry, biophysics and physiology. The datasets differ in size and in the type of label, from binary classes to continuous values.

## Protocol and metric

Classification tasks are scored with ROC-AUC and regression tasks with error measures such as RMSE or MAE, as the benchmark defines for each dataset. The benchmark uses scaffold splits, which place molecules with different core structures in train and test. The test then measures generalisation to new chemistry rather than to near-duplicates (Wu et al., 2018).

## What it shows

It shows whether a learned representation generalises to new molecules, and which featurisation suits which kind of property. The paper reports that learnable representations perform well overall, but struggle with scarce data and highly imbalanced classes. For quantum and biophysical datasets, physics-aware featurisation can matter more than the choice of learning algorithm (Wu et al., 2018).

## Limitations

- **Dataset quality.** Labels come from different sources, so noise differs across tasks.
- **Split choice.** Scores depend on the split, and a random split overstates performance on new chemistry.
- **Overlap.** The same molecules can appear in several public datasets, which can inflate results if they are not removed.

## Related

- [Science overview](index.md) describes the science benchmarks.
- [ROC-AUC](../../metrics/classification/roc-auc.md) is the classification metric used here.
- [RMSE](../../metrics/regression/rmse.md) is an error measure for regression tasks.

## References

### Seminal papers

- Wu, Z. et al. (2018). *MoleculeNet: a benchmark for molecular machine learning*. Chemical Science. https://doi.org/10.1039/C7SC02664A — Introduces the curated datasets, shared splits and metrics.

### Articles and documentation

- Gilmer, J. et al. (2017). *Neural Message Passing for Quantum Chemistry*. arXiv. https://arxiv.org/abs/1704.01212 — Evaluates message-passing networks on molecular property prediction.

### Additional sources

- Raji, I. D. & Bender, E. M. et al. (2021). *AI and the Everything in the Whole Wide World Benchmark*. arXiv. https://arxiv.org/abs/2111.15366 — Examines construct validity and the limits of broad claims from benchmarks.
- Liang, P. & Bommasani, R. et al. (2022). *Holistic Evaluation of Language Models*. arXiv. https://arxiv.org/abs/2211.09110 — Evaluates models across scenarios and metrics to expose trade-offs.
- Recht, B. et al. (2019). *Do ImageNet Classifiers Generalize to ImageNet?* arXiv. https://arxiv.org/abs/1902.10811 — Shows that a re-collected test set can reveal fit to the original collection.
