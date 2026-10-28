---
status: draft
last_reviewed: 2026-10-28
tags:
- model compression
- knowledge distillation
- feature-based distillation
aliases:
  - FitNets
  - Hints for thin deep nets
  - 提示式蒸餾
---

# FitNets

FitNets trains a thin, deep student using hints: intermediate features of a teacher. A hint layer in the teacher is matched by a guided layer in the student through a learned regressor, and the student is trained in two stages, first on the hint and then on the outputs. It is the reference method of [feature-based distillation](../index.md).

## Problem

A deep, thin student trained only on outputs is hard to train, and a large teacher's accuracy does not transfer fully to it. Output matching gives a single target per example, which is too weak a signal for the early layers of a deep network. The paper shows that a deep, thin student trained with hints can match or beat a larger teacher with far fewer parameters.

## Core idea

Use a teacher layer as a hint, and a student layer as the guided layer. Train the student first so that its guided layer predicts the hint, through a learned regressor that maps the student's features to the teacher's size. Then train the whole student on the outputs. The regressor is used only during the first stage and discarded afterwards.

## Equation or algorithm

The hint loss is

$$
\mathcal{L}_{\text{HT}} = \tfrac{1}{2}\, \lVert f_T(x) - r(f_S(x)) \rVert^2
$$

where $f_T$ and $f_S$ are the teacher and student features at the chosen layers, and $r$ is the learned regressor. The first stage minimises this loss with respect to the student layers up to the guided layer and the regressor. The second stage then applies the standard output-distillation objective of [Hinton distillation](../../response-based/hinton-distillation/index.md) to the whole student.

To keep the regressor's parameter count small, the paper uses a convolutional regressor in place of a fully connected one, so that its output has the same spatial size as the hint.

## Results

The abstract reports that on CIFAR-10 a deep student with almost 10.4 times fewer parameters than the teacher outperforms the larger, deeper teacher network. The paper also evaluates on MNIST, CIFAR-100, SVHN and AFLW, and reports that the method matches or outperforms standard distillation on these benchmarks.

## Limitations

- The two-stage schedule adds design choices, and the choice of hint layer matters.
- The regressor is extra training machinery that is discarded after the first stage.
- The reported gains are for convolutional image benchmarks and a fixed family of thin, deep architectures.

## Key methods

- [Attention transfer](../attention-transfer/index.md) matches a spatial summary of the teacher's activations, which is cheaper than FitNets' full-feature hints and needs no regressor.
- [Hinton distillation](../../response-based/hinton-distillation/index.md) is the output-level objective used in FitNets' second stage.

## Open issues and related variants

- **Hint selection.** Choosing hint layers for architectures without an obvious correspondence, such as transformers of different depths, is open.
- **Regressor design.** Whether a simpler mapping than the convolutional regressor loses information about the teacher's features is not settled.

## Connections

FitNets is a distillation counterpart of the layer-wise representation learning in [self-supervised learning](../../../../../theory/paradigms/self-supervised/index.md). The thin, deep student it targets is a common form for [edge hardware](../../../../../engineering/hardware/index.md).

## References

### Seminal papers

- Romero, A., et al. (2014). *FitNets: Hints for Thin Deep Nets*. arXiv:1412.6550. https://arxiv.org/abs/1412.6550 — Trains a thin, deep student on intermediate hints, with about 10.4 times fewer parameters than the teacher on CIFAR-10.
- Hinton, G., Vinyals, O. & Dean, J. (2015). *Distilling the Knowledge in a Neural Network*. arXiv:1503.02531. https://arxiv.org/abs/1503.02531 — The output-level objective used in the second stage.
- Zagoruyko, S. & Komodakis, N. (2016). *Paying More Attention to Attention: Improving the Performance of Convolutional Neural Networks via Attention Transfer*. arXiv:1612.03928. https://arxiv.org/abs/1612.03928 — A cheaper feature target for the same purpose.
- Tung, F. & Mori, G. (2019). *Similarity-Preserving Knowledge Distillation*. arXiv:1907.09682. https://arxiv.org/abs/1907.09682 — Proposes a different intermediate target, for comparison with hints.

### Surveys and textbooks

- Gou, J., et al. (2021). *Knowledge Distillation: A Survey*. International Journal of Computer Vision. https://doi.org/10.1007/s11263-021-01453-z — Surveys feature-based knowledge among other types.
