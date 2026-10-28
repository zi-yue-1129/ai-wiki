---
status: complete
last_reviewed: 2026-10-28
related:
  - engineering/evaluation
  - reference/datasets
  - applications/science
tags:
  - evaluation
  - benchmarks
  - science
aliases:
  - Science benchmarks
  - 科學基準
---

# Science Benchmarks

Science benchmarks test whether a model predicts measured properties of natural systems, such as molecules. Each dataset has its own labels, and each label comes from a particular experiment or calculation, so scores are comparable only when the dataset, the split and the metric are the same.

## Overview

Molecular machine learning long lacked a shared benchmark. Most new methods were tested on different datasets, which made it hard to tell which methods were better. MoleculeNet addressed this by curating several public datasets, defining metrics for evaluation, and providing open-source implementations of featurisation and learning methods in the DeepChem library (Wu et al., 2018). Its authors report that learnable representations are powerful and broadly offer the best performance, with the caveat that they still struggle with complex tasks under data scarcity and with highly imbalanced classification.

The benchmark is an early example of a general pattern in science: a predictive model is only as informative as the split that separates training molecules from test molecules. Random splits put close relatives in both sets, and a scaffold split, which groups molecules by their core structure, tests whether a model generalises to new chemistry.

## Benchmarks compared

| Benchmark | Task | Main metric |
|---|---|---|
| [MoleculeNet](moleculenet.md) | Predicting molecular properties across several datasets | ROC-AUC for classification, error measures for regression |

MoleculeNet is the only benchmark in this family so far, so the comparison is between its tasks rather than between benchmarks. Its datasets cover different properties with different label sources, so an average over tasks hides large differences between them.

## Key concepts

- **Scaffold**: the core ring and linker structure of a molecule, with side groups removed. Scaffold splits keep each scaffold in one set.
- **ROC-AUC**: the area under the receiver operating characteristic curve, a classification score that does not depend on one decision threshold.
- **Featurisation**: the step that turns a molecule into numbers, such as a fingerprint or a graph. Learned featurisation replaces it with a trained network.

## How it works

A model is trained on the training split of a dataset and scored on the held-out test split with the dataset's metric. Classification tasks use ROC-AUC, and regression tasks use error measures. Results are usually averaged over tasks and over several runs. Because the split changes the result, the split must be reported, and comparing a random split with a scaffold split can give very different numbers for the same model.

## Common issues

- **Split choice.** Random splits place near-duplicate molecules in train and test, which overstates generalisation. Scaffold splits test new core structures.
- **Label noise.** Labels come from different assays and sources, so the noise level differs across tasks.
- **Data scarcity and imbalance.** Learned representations can struggle when labels are few or classes are heavily imbalanced (Wu et al., 2018).

## Connections

- [Graph neural networks](../../../models/gnn/index.md) are a common model family for molecules, because a molecule is naturally a graph of atoms and bonds (Gilmer et al., 2017).
- [Metrics](../../metrics/index.md) describes ROC-AUC and the error measures.
- [Science applications](../../../../applications/science/index.md) covers the scientific uses that these benchmarks are meant to support.

## Open questions

- Whether a benchmark of fixed molecular datasets can keep up with the chemistry that new methods are applied to.
- How to report uncertainty so that small gains between methods can be judged against the variation between splits and seeds.

## Related

- [Benchmarks overview](../index.md) lists all families.
- [Protocols](../../protocols/index.md) covers splits and reporting.

## References

### Seminal papers

- Wu, Z. et al. (2018). *MoleculeNet: a benchmark for molecular machine learning*. Chemical Science, 513–530. https://doi.org/10.1039/C7SC02664A — Introduces the curated datasets, metrics and open-source implementations of the benchmark.
- Gilmer, J. et al. (2017). *Neural Message Passing for Quantum Chemistry*. arXiv. https://arxiv.org/abs/1704.01212 — Introduces a message-passing framework for predicting molecular properties from graphs.

### Articles and documentation

- Liang, P. & Bommasani, R. et al. (2022). *Holistic Evaluation of Language Models*. arXiv. https://arxiv.org/abs/2211.09110 — Evaluates models across scenarios and metrics to expose trade-offs, an approach that also applies to scientific benchmarks.
- Recht, B. et al. (2019). *Do ImageNet Classifiers Generalize to ImageNet?* arXiv. https://arxiv.org/abs/1902.10811 — Shows that a re-collected test set can reveal fit to the original collection, a risk for any fixed benchmark.

- Raji, I. D. & Bender, E. M. et al. (2021). *AI and the Everything in the Whole Wide World Benchmark*. arXiv. https://arxiv.org/abs/2111.15366 — Examines construct validity and the limits of broad claims from benchmarks.
