---
status: complete
last_reviewed: 2026-10-28
tags:
- model compression
- knowledge distillation
- feature-based distillation
aliases:
  - Attention transfer
  - Attention maps distillation
  - 注意力轉移
---

# Attention Transfer

Attention transfer trains a student convolutional network to match the teacher's spatial attention maps, which summarise where the network responds, instead of matching the full feature tensors. Zagoruyko and Komodakis (2016) showed that this cheaper target improves a student CNN across several datasets and architectures. It is a [feature-based](../index.md) method that trades some information for a simpler target.

## Problem

Matching full activations forces the student to copy every channel of the teacher's features, including features the student may not have the capacity to represent. A cheaper target that still carries the teacher's structure is needed.

## Core idea

Match the teacher's attention maps. An attention map is a spatial summary of a layer's activations, so the student learns where to respond without copying every channel. The paper defines two kinds of map: activation-based maps, computed from the activations, and gradient-based maps, computed from the gradients of the output with respect to the activations. The activation-based form is the one reported to work better than matching full activations.

## Equation or algorithm

For a layer with activation tensor $A$ of $C$ channels, the activation-based mapping sums the absolute activations raised to a power $p > 1$ over channels, giving one spatial map per example:

$$
F^{p}_{\text{sum}}(A) = \sum_{i=1}^{C} |A_i|^{p}
$$

The student's loss adds a penalty to the usual task loss. For each matched pair of layers $j$, the student and teacher maps are first flattened and $\ell_2$-normalised, and then compared:

$$
\mathcal{L}_{AT} = \mathcal{L}(W_S, x) + \frac{\beta}{2} \sum_{j \in \mathcal{I}} \left\| \frac{Q_S^{j}}{\lVert Q_S^{j} \rVert_2} - \frac{Q_T^{j}}{\lVert Q_T^{j} \rVert_2} \right\|_p
$$

Here $Q^j$ is the vectorised attention map for layer $j$, $\mathcal{I}$ the set of matched layers, $\beta$ the weight of the penalty, and $p$ the norm type, which the paper sets to 2. Normalising the maps makes the comparison insensitive to their overall scale.

## Results

On CIFAR-10, Table 1 of the paper reports median test error over five runs. Attention transfer lowers the error of every student-teacher pair in the table, including pairs where the teacher is deeper than the student. Three of the pairs are shown below.

| Student (teacher) | Student alone (%) | With attention transfer (%) | Teacher (%) |
|---|---|---|---|
| WRN-16-1 (WRN-16-2) | 8.77 | 7.93 | 6.31 |
| WRN-16-1 (WRN-40-1) | 8.77 | 8.25 | 6.58 |
| WRN-16-2 (WRN-40-2) | 6.31 | 5.85 | 5.23 |

The paper also reports that activation-based transfer beats matching full activations in every pair, and that combining it with the standard distillation loss gives further gains.

On ImageNet, a ResNet-18 student trained with attention transfer from a ResNet-34 teacher reaches 29.3% top-1 validation error, against 30.4% without transfer. The teacher reaches 26.1%. In transfer learning, Table 4 of the paper reports that attention transfer lowers the error of an ImageNet-pretrained ResNet-18 from 28.5% to 27.0% on CUB birds, and from 28.2% to 27.1% on MIT Scenes. On Scenes it does about as well as knowledge distillation, while on CUB it does better. The paper notes that its ImageNet attention losses were applied to only two groups of residual blocks, and that the hyperparameters were not tuned.

## Limitations

- Attention maps exist only where the architecture has spatial structure, so the method was developed for convolutional networks.
- The summary discards channel information that full feature matching would keep.
- The penalty weight $\beta$ and the choice of matched layers are extra settings that the student's performance depends on.

## Key methods

- [FitNets](../fitnets/index.md) matches the full intermediate features through a learned regressor. It carries more information than attention transfer, at a higher cost.
- [Hinton distillation](../../response-based/hinton-distillation/index.md) is the output-level objective that attention transfer adds its penalty to.

## Open issues and related variants

- **Transformers.** Attention maps are a natural target for transformers, but how well the transfer works there needs study.
- **Other intermediate targets.** Similarity-preserving distillation (Tung and Mori, 2019) matches a different intermediate summary, and comparing it with attention maps on the same tasks is open.

## Connections

Attention maps are a spatial summary of where a network looks, which links the method to the attention mechanisms in [transformers](../../../../../theory/models/transformer/index.md). The focus on where a system responds has a counterpart in [neuroscience](../../../../../brain-mind/neuroscience/index.md), though the method is an engineering device and makes no neural claim.

## References

### Seminal papers

- Zagoruyko, S. & Komodakis, N. (2016). *Paying More Attention to Attention: Improving the Performance of Convolutional Neural Networks via Attention Transfer*. arXiv:1612.03928. https://arxiv.org/abs/1612.03928 — Matches activation-based spatial attention maps between teacher and student to improve a smaller CNN.
- Romero, A., et al. (2014). *FitNets: Hints for Thin Deep Nets*. arXiv:1412.6550. https://arxiv.org/abs/1412.6550 — Full-feature hints, the alternative that attention transfer simplifies.
- Hinton, G., Vinyals, O. & Dean, J. (2015). *Distilling the Knowledge in a Neural Network*. arXiv:1503.02531. https://arxiv.org/abs/1503.02531 — The output loss that attention transfer is added to.
- Tung, F. & Mori, G. (2019). *Similarity-Preserving Knowledge Distillation*. arXiv:1907.09682. https://arxiv.org/abs/1907.09682 — Proposes a different intermediate target, for comparison with attention maps.

### Surveys and textbooks

- Gou, J., et al. (2021). *Knowledge Distillation: A Survey*. International Journal of Computer Vision. https://doi.org/10.1007/s11263-021-01453-z — Surveys distillation methods, including feature-based targets.
