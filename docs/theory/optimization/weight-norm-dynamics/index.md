---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/transformer
tags:
  - optimization
  - weight decay
  - normalisation
  - training stability
aliases:
  - Weight-norm dynamics
  - Weight norm growth
  - 權重範數動態
---

# Weight-Norm Dynamics

When a layer is followed by normalisation, its output does not change if its weights are rescaled. The weight norm then drifts in a direction set by the optimiser and the learning rate, not by the loss. This subtopic covers how the norm grows, how weight decay sets an equilibrium, and what that means for training stability. The general treatment of decay is in [Regularisation and Weight Decay](../regularisation-and-weight-decay.md), and the decoupled form is on the [AdamW](../adaptive/adamw.md) page.

## Overview

Consider a layer whose output is normalised, so that scaling its weights by a constant leaves the output unchanged. The gradient is then orthogonal to the weight vector, and each gradient step increases the norm. The effective learning rate, which is the step size relative to the weight norm, therefore shrinks over training. Weight decay counteracts this growth, and the two effects balance at an equilibrium norm.

Two questions follow. How quickly does the equilibrium arrive relative to the length of training? And what happens to layers that are not scale-invariant, such as the attention output or a classifier head, where the same balance does not hold?

## Key methods

Each method has its own page. The overview and comparison here are brief.

| Method | Mechanism | What it shows |
|---|---|---|
| [Rotational equilibrium](rotational-equilibrium.md) (Kosson et al., 2023) | Weight decay balances the rotation of each neuron's weights | An equilibrium norm and a timescale of about \(1/(\eta\lambda)\) steps, with neurons rotating at different rates |
| [Weight decay scaling for AdamW](adamw-weight-decay-scaling.md) (Wang & Aitchison, 2024) | Sets \(\lambda\) so that the averaging timescale is fixed in epochs | Optimal decay depends on model and dataset size, and it changes with the learning rate |
| Spherical motion dynamics (Wan et al., 2020) | Analyses the dynamics of normalised networks trained with SGD and decay | Norm converges to an equilibrium with decay, and grows without it, shrinking the effective step |
| Exponential learning-rate view (Li & Arora, 2019) | Shows that decay and normalisation together act like an exponentially growing step | Only the product \(\eta\lambda\) matters for scale-invariant layers |

The attention-specific side of this problem is on the [QK-normalisation](../../models/transformer/qk-norm.md) and [σReparam](../../models/transformer/sigma-reparam.md) pages. Bounding a norm alone does not guarantee stable attention, because collapse can happen in rank or entropy.

## Connections

- [AdamW](../adaptive/adamw.md) separates weight decay from the adaptive step, which is the setting in which the equilibrium analysis applies.
- [Learning-rate schedules](../learning-rate-schedules.md) interact with decay, since the equilibrium depends on the product of the learning rate and the decay.
- [Sharp minima](../sharp-minima.md) covers the other route by which the optimiser and the regulariser affect the solution.

## Open questions

- How well the equilibrium picture predicts non-scale-invariant layers, such as heads and projections that are not followed by normalisation.
- Whether the timescale rule holds across architectures other than the convolutional and vision models used in the cited work.

## References

- Kosson, A., Messmer, B., & Jaggi, M. (2023). *Rotational Equilibrium: How Weight Decay Balances Learning Across Neural Networks*. arXiv:2305.17212. https://arxiv.org/abs/2305.17212 — analyses the equilibrium of each neuron's weights under AdamW and SGD.
- Loshchilov, I., & Hutter, F. (2019). *Decoupled Weight Decay Regularization*. ICLR 2019. https://arxiv.org/abs/1711.05101 — separates weight decay from the adaptive gradient step.
- Wan, R., Zhu, Z., Zhang, X., & Sun, J. (2020). *Spherical Motion Dynamics: Learning Dynamics of Neural Network with Normalization, Weight Decay, and SGD*. arXiv:2006.08419. https://arxiv.org/abs/2006.08419 — derives the norm dynamics of normalised layers trained with SGD and weight decay.
- Li, Z., & Arora, S. (2019). *An Exponential Learning Rate Schedule for Deep Learning*. ICLR 2020. https://arxiv.org/abs/1910.07454 — shows that weight decay with normalisation acts like an exponentially growing learning rate.
- Wang, X., & Aitchison, L. (2024). *How to Set AdamW's Weight Decay as You Scale Model and Dataset Size*. arXiv:2405.13698. https://arxiv.org/abs/2405.13698 — proposes how to set the decay as model and dataset size change.
- Wortsman, M., Liu, P. J., Xiao, L., et al. (2023). *Small-scale proxies for large-scale Transformer training instabilities*. arXiv:2309.14322. https://arxiv.org/abs/2309.14322 — reproduces attention and output-logit instabilities at small scale, and tests remedies.
