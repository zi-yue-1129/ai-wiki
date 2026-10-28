---
status: draft
last_reviewed: 2026-10-28
tags:
- model compression
- knowledge distillation
- feature-based distillation
aliases:
  - Feature-based distillation
  - FitNets
  - Attention transfer
  - 特徵式蒸餾
---

# Feature-Based Distillation

Feature-based distillation trains the student to match the teacher's intermediate representations, not only its outputs. The student learns how the teacher computes its features, which gives a training signal at every depth rather than only at the final layer. It is the second main family of [knowledge distillation](../index.md), alongside matching output distributions.

## Overview

Output-based distillation, as in [Hinton et al.](../index.md), gives the student one target per example: the teacher's softened prediction. A deep teacher, however, builds useful intermediate features, and the final layer carries only part of what it knows. Feature-based methods add a loss that compares hidden activations, usually after a learned projection that maps the student's feature size to the teacher's. Where the student is thin and deep, these intermediate hints are what make training possible.

## Key concepts

- **Hint layer.** A teacher layer whose activations serve as the target for a chosen student layer.
- **Regressor.** A learned projection that maps the student's features to the teacher's dimensions, so that the two can be compared.
- **Attention maps.** Spatial summaries of where a network responds, which can be matched instead of full activations.
- **Layer choice.** The teacher and student layers to match are a design decision, and the best choice depends on the architecture.

## Key methods

### FitNets (Romero et al., 2014)

- **Problem:** A deep, thin student trained only on outputs is hard to train, and a large teacher's accuracy does not transfer fully to it.
- **Core idea:** Use a hint layer from the teacher and a guided layer in the student. Train the student first to match the hint through a regressor, then train it on the outputs.
- **Equation or algorithm:** A hint loss \(\lVert f_T(x) - r(f_S(x)) \rVert^2\), where \(r\) is a learned regressor, followed by the standard output-distillation loss.
- **Results:** The abstract reports that on CIFAR-10 a deep student with almost 10.4 times fewer parameters outperforms a larger teacher network.
- **Limitations:** The two-stage training schedule adds design choices, and the choice of hint layer matters.

### Attention transfer (Zagoruyko and Komodakis, 2016)

- **Problem:** Matching full activations forces the student to copy features it may not have capacity for. A cheaper target that still carries the teacher's structure is needed.
- **Core idea:** Match the teacher's attention maps, which summarise where the network responds, instead of the full feature tensors.
- **Equation or algorithm:** An attention map is computed from the squared activations summed over channels. The student is trained to make its attention maps close to the teacher's, added to the usual loss.
- **Results:** The authors argue that a smaller student CNN gains accuracy by mimicking the attention maps of a stronger teacher.
- **Limitations:** Attention maps exist only where the architecture has spatial structure, so the method was developed for convolutional networks.

## Trade-offs

- **Information versus flexibility.** Feature matching transfers more information than output matching, but it constrains the student's architecture to produce compatible features.
- **Cost.** The teacher must be run on each input, and the extra losses add tuning.
- **Mismatch.** When student and teacher differ in design, the best hint layer may not have a clear counterpart.

## More variants and open issues

- **Variant:** [relation-based distillation](../relation-based/index.md), which matches relations between examples instead of individual features.
- **Open issue:** how to choose hint layers automatically for architectures that do not have an obvious correspondence, such as transformers with different depths.
- **Open issue:** whether matching features transfers the teacher's reasoning, or only its representations.

## Connections

Feature matching is the distillation counterpart of the representation learning discussed in [self-supervised learning](../../../../theory/paradigms/self-supervised/index.md). The idea that a student learns from the internal state of a teacher, rather than from its answers, has an analogy in how learners absorb a teacher's methods; see [cognitive science](../../../../brain-mind/cognitive-science/index.md).

## References

### Seminal papers

- Romero, A., et al. (2014). *FitNets: Hints for Thin Deep Nets*. arXiv:1412.6550. https://arxiv.org/abs/1412.6550 — Trains a thin, deep student on intermediate hints from a teacher, with about 10.4 times fewer parameters than the teacher on CIFAR-10.
- Zagoruyko, S., Komodakis, N. (2016). *Paying More Attention to Attention: Improving the Performance of Convolutional Neural Networks via Attention Transfer*. arXiv:1612.03928. https://arxiv.org/abs/1612.03928 — Matches attention maps between teacher and student, improving a smaller CNN.
- Hinton, G., Vinyals, O., Dean, J. (2015). *Distilling the Knowledge in a Neural Network*. arXiv:1503.02531. https://arxiv.org/abs/1503.02531 — Output-level distillation, the baseline that feature methods extend.

### Surveys and textbooks

- Gou, J., et al. (2021). *Knowledge Distillation: A Survey*. International Journal of Computer Vision. https://doi.org/10.1007/s11263-021-01453-z — Surveys distillation by knowledge type, including feature-based knowledge.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Sanh, V., et al. (2019). *DistilBERT, a Distilled Version of BERT: Smaller, Faster, Cheaper and Lighter*. arXiv:1910.01108. https://arxiv.org/abs/1910.01108 — Distills BERT with hidden-state alignment as well as output matching.
