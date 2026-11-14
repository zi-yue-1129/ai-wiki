---
related:
  - theory/model-compression/pruning
  - engineering/hardware/co-design
tags:
  - model compression
  - sparsity
  - pruning
last_reviewed: 2026-11-01
aliases:
  - Sparsity in Deep Learning
  - Hoefler sparsity survey
  - 深度學習中的稀疏性
---

# Sparsity in Deep Learning (Hoefler et al., 2021)

Hoefler, Alistarh and Ben-Nun (2021) survey the methods for making neural networks sparse, meaning that many weights or activations are set to zero. The survey is a tutorial as well as a review: it treats sparsification for both inference and training, and it asks when a sparse network is worth its extra cost on real hardware (Hoefler et al., 2021).

## Overview

The survey starts from the cost of deep learning. Large networks need energy, memory and training time, and sparsity is one way to reduce all three. The abstract states that sparse networks can generalise as well as, or better than, the dense networks they came from, and that sparsity can shrink a model enough to fit a mobile device (Hoefler et al., 2021).

The survey does not claim that every sparse network is cheap. Its central theme is the gap between a reduction in parameter count and a reduction in run time, and most of its discussion is about closing that gap.

## Key concepts

- **Unstructured sparsity**: any individual weight may be zero. It gives the highest freedom in choosing which weights to remove, but it needs an index for each surviving value.
- **Structured sparsity**: whole filters, channels, heads or blocks are removed. The survey says it has the lowest storage overhead and the highest performance, but it may lead to worse models (Hoefler et al., 2021, Section 3.1).
- **Overhead of indices**: removing random elements requires storing the positions of the remaining non-zero values (Section 2.2). Arbitrary sparsity therefore runs less efficiently than dense computation on hardware built for dense operations (Section 2.3).
- **Occam's hill**: accuracy first rises as sparsity removes learned noise, then falls. At high sparsity the quality of the network degrades quickly (Section 2.1).

## How it works

The survey organises sparsification into three phases: choosing what to remove, changing the network, and recovering accuracy. It covers magnitude-based removal, methods that add connections during training, and methods that decide the sparsity pattern before training starts (Hoefler et al., 2021).

The survey says that its discussion applies to both inference and training (Section 2). For training, the interesting question is whether a sparse network can be trained from scratch. Liu et al., cited in the survey, conclude that this works well when the architecture and hyperparameters are chosen carefully. They also report that unstructured pruning from scratch fails on large ImageNet models, where fine-tuning still helps (Section 2.4.3).

Pruning at initialisation is a separate family. SNIP identifies connections to remove in a data-driven way before training, using connection sensitivity (Lee et al., 2018). The survey reports that a random initialisation is a strong baseline for these methods (Section 2.4.3).

## Key methods

Compare the families briefly, and read each method's own page for the detail:

- [Learning weights and connections](learning-weights-and-connections/index.md): prune and retrain, the classic iterative method (Han et al., 2015).
- [Magnitude pruning](magnitude-pruning/index.md): remove the smallest weights, gradually or in one shot.
- [Lottery ticket](lottery-ticket/index.md): a sparse subnetwork that trains well from its original initialisation.
- [Structured pruning](structured-pruning/index.md): remove whole channels or filters, which runs on dense hardware.

## Evidence and results

The survey reports that some current methods can reduce model size by about 10 to 100 times, with no significant loss of accuracy (Section 1.1). Dense-sparse-dense training, cited in the survey, reports significantly higher generalisation than the dense baseline (Section 2.4.2; Han et al., 2016).

The gains depend strongly on the target. A reduction in parameters does not translate into a proportional speed-up unless the sparsity pattern matches the hardware, which is why the survey separates unstructured from structured methods so carefully.

## Limitations

- **Hardware gap.** Unstructured sparsity saves storage but often not time, unless kernels or hardware support the pattern.
- **Extreme sparsity.** The survey notes that it is unclear whether very high sparsity is achievable for deep models, and whether the accuracy trade-off holds at those levels (Sections 2.2 and 2.4.3).
- **Tuning.** Methods that change structure during training add hyperparameters, and the survey notes that few studies show how to tune them (Section 2.4.6).

## Connections

- [Hardware co-design](../../../engineering/hardware/co-design/index.md) covers the other side of the gap: what hardware needs to run a sparse network efficiently.
- [Quantisation survey](../quantisation/quantisation-survey.md) covers the other common compression route, which reduces the precision of each value rather than removing values.

## Applications

Sparse networks are used where memory and energy are the binding limits, such as mobile devices, and for training very large networks with fewer operations (Hoefler et al., 2021).

## Open questions

- Whether sparsity improves interpretability, which the survey leaves open (Section 1).
- How to obtain real speed-ups from unstructured sparsity on general-purpose hardware.

## References

### Seminal papers

- Hoefler, T., Alistarh, D. & Ben-Nun, T. (2021). *Sparsity in Deep Learning: Pruning and Growth for Efficient Inference and Training in Neural Networks*. arXiv. https://arxiv.org/abs/2102.00554 — A survey and tutorial on sparsification for inference and training, with the hardware trade-offs discussed on this page.
- Han, S., Pool, J., Tran, J. & Dally, W. J. (2015). *Learning both Weights and Connections for Efficient Neural Networks*. arXiv. https://arxiv.org/abs/1506.02626 — Prune-and-retrain, the classic iterative pruning method.
- Han, S. et al. (2016). *DSD: Dense-Sparse-Dense Training for Deep Neural Networks*. arXiv. https://arxiv.org/abs/1607.04381 — Dense-sparse-dense training, cited in the survey as improving generalisation.
- Lee, N., Ajanthan, T. & Torr, P. H. S. (2018). *SNIP: Single-shot Network Pruning based on Connection Sensitivity*. arXiv. https://arxiv.org/abs/1810.02340 — Pruning at initialisation using connection sensitivity, before any training.

### Surveys and benchmarks

- Gale, T., Elsen, E. & Hooker, S. (2019). *The State of Sparsity in Deep Neural Networks*. arXiv. https://arxiv.org/abs/1902.09574 — A comparison of sparsification methods, cited here for the state of the field at the time.
- Frankle, J. & Carbin, M. (2018). *The Lottery Ticket Hypothesis: Finding Sparse, Trainable Neural Networks*. arXiv. https://arxiv.org/abs/1803.03635 — The sparse-subnetwork hypothesis that the survey discusses in connection with pruning and rewinding.
