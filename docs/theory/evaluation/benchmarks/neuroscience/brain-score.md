---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - neuroscience
---

# Brain-Score

Brain-Score is a benchmark that scores artificial neural networks by how well their internal responses predict neural recordings from primate visual cortex and behavioural data on object recognition (Schrimpf et al., 2018). It asks how closely a model's representation matches measured responses, not only whether it classifies images correctly.

## Task and data

The model is shown the same images that were shown to an animal. Its internal responses are mapped to the recorded neural responses, and the score measures how well that mapping predicts responses to held-out images (Schrimpf et al., 2018).

## Protocol and metric

Predictivity is the correlation between predicted and measured responses on held-out images, summarised across recording sites. The choice of layer, the regression method and the neural dataset all affect the score, so each must be reported.

## What it shows

It shows how well a model's representation matches measured neural and behavioural responses for object recognition. Higher predictivity is evidence of similarity to the brain, not proof of a shared mechanism. Earlier work found that models optimised for recognition predict responses in higher visual cortex (Yamins et al., 2014).

## Limitations

- **Flexible mapping.** A flexible regression can fit noise, so the mapping must be constrained and validated.
- **Limited data.** Recordings cover few sites and images, so scores carry wide uncertainty.
- **Single task.** Object recognition on still images does not capture the full range of brain function.

## Related

- [Neuroscience overview](index.md) describes the neuroscience benchmarks.
- [ImageNet](../vision/imagenet.md) is the classification benchmark that many of the scored models are trained on.

## References

### Seminal papers

- Schrimpf, M. et al. (2018). *Brain-Score: Which Artificial Neural Network for Object Recognition is most Brain-Like?* bioRxiv. https://doi.org/10.1101/407007 — Introduces the benchmark and its neural and behavioural scores.
- Yamins, D. L. K. et al. (2014). *Performance-optimized hierarchical models predict neural responses in higher visual cortex*. PNAS. https://doi.org/10.1073/pnas.1403112111 — Shows that object-recognition models predict responses in higher visual cortex.

### Articles and documentation

- Raji, I. D. & Bender, E. M. et al. (2021). *AI and the Everything in the Whole Wide World Benchmark*. arXiv. https://arxiv.org/abs/2111.15366 — Examines construct validity and the limits of broad claims from benchmarks.

### Additional sources

- Liang, P. & Bommasani, R. et al. (2022). *Holistic Evaluation of Language Models*. arXiv. https://arxiv.org/abs/2211.09110 — Evaluates models across scenarios and metrics to expose trade-offs.
- Recht, B. et al. (2019). *Do ImageNet Classifiers Generalize to ImageNet?* arXiv. https://arxiv.org/abs/1902.10811 — Shows that a re-collected test set can reveal fit to the original collection.
