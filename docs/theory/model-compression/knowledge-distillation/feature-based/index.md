---
status: complete
last_reviewed: 2026-10-28
related:
- theory/paradigms/self-supervised
tags:
- model compression
- knowledge distillation
- feature-based distillation
aliases:
  - Feature-based distillation
  - Hint-based distillation
  - 特徵式蒸餾
---

# Feature-Based Distillation

Feature-based distillation trains the student to match the teacher's intermediate representations, not only its outputs. The student learns how the teacher computes its features, which gives a training signal at every depth rather than only at the final layer. It is the second main family of [knowledge distillation](../index.md), alongside matching output distributions.

## Overview

Output-based distillation, as in [response-based distillation](../response-based/index.md), gives the student one target per example: the teacher's softened prediction. A deep teacher, however, builds useful intermediate features, and the final layer carries only part of what it knows. Feature-based methods add a loss that compares hidden activations, usually after a learned projection (a regressor) that maps the student's feature size to the teacher's. When the student is thin and deep, these intermediate hints can make training possible at all.

## Key concepts

- **Hint layer.** A teacher layer whose activations serve as the target for a chosen student layer.
- **Regressor.** A learned projection that maps the student's features to the teacher's dimensions, so the two can be compared.
- **Attention maps.** Spatial summaries of where a network responds, which can be matched instead of full activations.
- **Layer choice.** The teacher and student layers to match are a design decision, and the best choice depends on the architecture.

## Key methods

Both landmark methods below supervise intermediate layers. They differ in how much of the feature they copy.

- [FitNets (Romero et al., 2015)](fitnets/index.md): matches the full hidden activations of a chosen teacher layer, through a learned regressor, in a two-stage schedule.
- [Attention transfer (Zagoruyko & Komodakis, 2016)](attention-transfer/index.md): matches spatial attention maps, which are cheaper summaries of the activations and need no regressor when the resolutions agree.

FitNets transfers more of the feature and needs a compatible feature space. Attention transfer relaxes that constraint, but only applies where the architecture has spatial structure.

## Trade-offs

- **Information versus flexibility.** Feature matching transfers more information than output matching, but it constrains the student to produce compatible features.
- **Cost.** The teacher must run on each input, and the extra losses add hyperparameters to tune.
- **Mismatch.** When student and teacher differ in design, the best hint layer may have no clear counterpart.

## More variants and open issues

- **Variant:** [relation-based distillation](../relation-based/index.md), which matches relations between examples instead of individual features.
- **Variant:** [self-distillation](../self-distillation/index.md), where the hints come from deeper layers of the same network.
- **Open issue:** how to choose hint layers automatically for architectures without an obvious correspondence, such as transformers with different depths.
- **Open issue:** whether matching features transfers the teacher's reasoning, or only its representations.

## Connections

Feature matching is the distillation counterpart of the representation learning discussed in [self-supervised learning](../../../../theory/paradigms/self-supervised/index.md). The idea that a learner absorbs a teacher's internal method, rather than only its answers, has a loose analogue in how people learn from worked examples; see [cognitive science](../../../../brain-mind/cognitive-science/index.md).

## References

### Seminal papers

- Romero, A., Ballas, N., Ebrahimi Kahou, S., Chassang, A., Gatta, C. & Bengio, Y. (2015). *FitNets: Hints for Thin Deep Nets*. ICLR 2015. https://arxiv.org/abs/1412.6550 — Trains a thin, deep student with hint layers from the teacher; the abstract reports a student with almost 10.4 times fewer parameters that outperforms a larger teacher.
- Zagoruyko, S. & Komodakis, N. (2016). *Paying More Attention to Attention: Improving the Performance of Convolutional Neural Networks via Attention Transfer*. arXiv:1612.03928. https://arxiv.org/abs/1612.03928 — Introduces attention transfer, in which the student is trained to match the teacher's attention maps, with gains reported across datasets and CNN architectures.
- Hinton, G., Vinyals, O. & Dean, J. (2015). *Distilling the Knowledge in a Neural Network*. arXiv:1503.02531. https://arxiv.org/abs/1503.02531 — Compresses an ensemble into a single model; the output-level baseline that feature methods extend.

### Surveys and textbooks

- Gou, J., Yu, B., Maybank, S. J. & Tao, D. (2021). *Knowledge Distillation: A Survey*. International Journal of Computer Vision, 129(6). https://doi.org/10.1007/s11263-021-01453-z — Broad review of distillation that classifies the transferred knowledge, including feature-based knowledge. Also free as a preprint at https://arxiv.org/abs/2006.05525.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Sanh, V., Debut, L., Chaumond, J. & Wolf, T. (2019). *DistilBERT, a Distilled Version of BERT: Smaller, Faster, Cheaper and Lighter*. arXiv:1910.01108. https://arxiv.org/abs/1910.01108 — Distils BERT into a model about 40% smaller that keeps 97% of its language understanding, the standard language-model distillation reference.
