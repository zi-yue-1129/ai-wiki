---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - science
---

# Science Benchmarks

Science benchmarks test whether a model predicts measured properties of natural systems, such as molecules. Because each dataset has its own labels, scores are comparable only when the dataset, the split and the metric are the same.

| Benchmark | Task | Main metric |
|---|---|---|
| [MoleculeNet](moleculenet.md) | Predicting molecular properties across several datasets | ROC-AUC for classification, error measures for regression |

## Common issues

- **Split choice.** Random splits place near-duplicate molecules in train and test, which overstates generalisation. Scaffold splits test new core structures.
- **Label noise.** Labels come from different assays and sources, so the noise level differs across tasks (Wu et al., 2018).
- **Data scarcity.** Learned representations can struggle when labels are few or classes are heavily imbalanced (Wu et al., 2018).

## Related

- [Benchmarks overview](../index.md) lists all families.
- [Metrics](../../metrics/index.md) describes ROC-AUC and the error measures.
- [Protocols](../../protocols/index.md) covers splits and reporting.

## References

### Seminal papers

- Wu, Z. et al. (2018). *MoleculeNet: a benchmark for molecular machine learning*. Chemical Science. https://doi.org/10.1039/C7SC02664A — Introduces the curated datasets, shared splits and metrics.

### Articles and documentation

- Gilmer, J. et al. (2017). *Neural Message Passing for Quantum Chemistry*. arXiv. https://arxiv.org/abs/1704.01212 — Evaluates message-passing networks on molecular property prediction.

### Additional sources

- Raji, I. D. & Bender, E. M. et al. (2021). *AI and the Everything in the Whole Wide World Benchmark*. arXiv. https://arxiv.org/abs/2111.15366 — Examines construct validity and the limits of broad claims from benchmarks.
- Liang, P. & Bommasani, R. et al. (2022). *Holistic Evaluation of Language Models*. arXiv. https://arxiv.org/abs/2211.09110 — Evaluates models across scenarios and metrics to expose trade-offs.
- Recht, B. et al. (2019). *Do ImageNet Classifiers Generalize to ImageNet?* arXiv. https://arxiv.org/abs/1902.10811 — Shows that a re-collected test set can reveal fit to the original collection.
