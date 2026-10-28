---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - neuroscience
---

# Neuroscience Benchmarks

Neuroscience benchmarks test how closely a model's internal responses match measured neural or behavioural data. They ask a different question from accuracy: a model can classify images well and still differ from the brain in how it represents them.

| Benchmark | Task | Main metric |
|---|---|---|
| [Brain-Score](brain-score.md) | Predicting neural and behavioural responses to object images | Predictivity of held-out neural and behavioural data |

## Common issues

- **Mapping choice.** The score depends on how model units are mapped to neural sites, so the regression and the layer must be reported.
- **Limited recordings.** Few sites and images give wide uncertainty, so small differences between models are not reliable.
- **Similarity is not mechanism.** A high score shows that representations are similar on the test, not that the model works the same way as the brain (Yamins et al., 2014).

## Related

- [Benchmarks overview](../index.md) lists all families.
- [Vision](../vision/index.md) covers the image benchmarks that models are trained on.
- [Protocols](../../protocols/index.md) covers splits and reporting.

## References

### Seminal papers

- Schrimpf, M. et al. (2018). *Brain-Score: Which Artificial Neural Network for Object Recognition is most Brain-Like?* bioRxiv. https://doi.org/10.1101/407007 — Introduces the benchmark and its neural and behavioural scores.
- Yamins, D. L. K. et al. (2014). *Performance-optimized hierarchical models predict neural responses in higher visual cortex*. PNAS. https://doi.org/10.1073/pnas.1403112111 — Shows that object-recognition models predict responses in higher visual cortex.

### Articles and documentation

- Raji, I. D. & Bender, E. M. et al. (2021). *AI and the Everything in the Whole Wide World Benchmark*. arXiv. https://arxiv.org/abs/2111.15366 — Examines construct validity and the limits of broad claims from benchmarks.

### Additional sources

- Liang, P. & Bommasani, R. et al. (2022). *Holistic Evaluation of Language Models*. arXiv. https://arxiv.org/abs/2211.09110 — Evaluates models across scenarios and metrics to expose trade-offs.
- Recht, B. et al. (2019). *Do ImageNet Classifiers Generalize to ImageNet?* arXiv. https://arxiv.org/abs/1902.10811 — Shows that a re-collected test set can reveal fit to the original collection.
