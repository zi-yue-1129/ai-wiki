---
status: complete
last_reviewed: 2026-10-28
related:
  - theory/models/transformer
tags:
  - optimization
  - weight decay
  - normalisation
aliases:
  - Rotational equilibrium
  - 旋轉平衡
---

# Rotational Equilibrium

Kosson, Messmer and Jaggi (2023) study how weight decay affects the update behaviour of individual neurons. Their main claim is that, under AdamW, the weights of each neuron reach an equilibrium in which the decay and the gradient updates balance. The equilibrium is reached on a timescale set by the product of the learning rate and the decay, and neurons with different gradient statistics settle at different rotation rates. The parent subtopic is [Weight-Norm Dynamics](index.md).

## Overview

A scale-invariant neuron is one whose output does not change when its weights are multiplied by a constant. The gradient of such a neuron is orthogonal to its weight vector. Each update therefore rotates the weights and increases their norm, and the decay pulls the norm back down. The rotation the weights make per step is the quantity the paper follows.

## Problem

Training curves often show weight norms that keep growing when weight decay is small, and the effective learning rate shrinks as a result. Practitioners set the decay by convention, and it is not clear whether a given value is too small to matter within the training budget. The paper asks how weight decay sets the norm and the rotation of each neuron, and how long the system takes to reach that state.

## Core idea

The paper follows each neuron's weights \(\omega \in \mathbb{R}^C\) under AdamW with learning rate \(\eta\) and decay \(\lambda\), where \(C\) is the dimension of the weight vector. The equilibrium norm is

\[
\|\omega\| = \sqrt{\frac{\eta C}{2\lambda - \eta\lambda^2}} \approx \sqrt{\frac{\eta C}{2\lambda}},
\]

and the expected rotation per step in equilibrium is approximately \(\sqrt{2\eta\lambda(1-\beta_1)/(1+\beta_1)}\), where \(\beta_1\) is the momentum coefficient. The squared norm contracts towards this equilibrium by a factor of \((1-\eta\lambda)^2\) per step, so the timescale is about \(1/(\eta\lambda)\) steps. The paper presents the contraction as an approximation.

Under this account, a decay that is too small gives a timescale much longer than the training run. The weights then may not reach equilibrium, and the norm keeps growing. A larger decay shortens the timescale, and the rotation reaches its steady value within the run.

## How it works

1. Choose the learning rate \(\eta\) and decay \(\lambda\), and compute the timescale \(1/(\eta\lambda)\) in steps.
2. Compare the timescale with the number of training steps. If it is much longer, decay has little effect within the run.
3. Monitor the norm and rotation of each neuron, not only the layer as a whole. Neurons with imbalanced radial gradients rotate at different rates.
4. Equalise the rotation rates, for example with Weight Standardisation, which the paper reports balances the rotation across neurons.

## Results

The paper combines the derivation with experiments that compare the predicted equilibrium with trained networks. It reports that Weight Standardisation makes each neuron scale-invariant, and that this balances the rotation across neurons (Figure 7 of the paper). It also compares AdamW with Adam plus an L2 penalty, and finds that AdamW performs better. The paper attributes the gap mainly to the balanced rotation under AdamW, and analyses it in its appendix. The exact figures should be checked in the paper before reuse.

## Limitations

- The equilibrium result is derived for scale-invariant neurons. Layers that are not followed by normalisation, such as classifier heads, are outside the derivation, so their behaviour needs separate evidence.
- The expected rotation is an approximation that holds for small relative updates and a small radial component, and the paper checks it empirically. The constants are not exact for every architecture.
- The timescale rule is about steps. It becomes a rule about epochs only when the number of steps per epoch is fixed, which is the point developed in [AdamW weight-decay scaling](adamw-weight-decay-scaling.md).

## Connections

- [Weight-Norm Dynamics](index.md) places this result among the other accounts of norm growth.
- [AdamW](../adaptive/adamw.md) is the optimiser for which the equilibrium was derived.
- [Regularisation and weight decay](../regularisation-and-weight-decay.md) gives the general view of decay.
- The attention-logit side of norm growth is discussed on the [QK-normalisation](../../models/transformer/qk-norm.md) page.

## Open questions

- Whether the equilibrium picture holds for non-scale-invariant layers, where decay acts directly on the output scale.
- How the rotation imbalance across neurons interacts with the per-parameter scaling of adaptive optimisers in very large models.

## References

- Kosson, A., Messmer, B., & Jaggi, M. (2023). *Rotational Equilibrium: How Weight Decay Balances Learning Across Neural Networks*. arXiv:2305.17212. https://arxiv.org/abs/2305.17212 — the source of the equilibrium norm, rotation and timescale results.
- Loshchilov, I., & Hutter, F. (2019). *Decoupled Weight Decay Regularization*. ICLR 2019. https://arxiv.org/abs/1711.05101 — introduces the decoupled decay used in the analysis.
- Wan, R., Zhu, Z., Zhang, X., & Sun, J. (2020). *Spherical Motion Dynamics: Learning Dynamics of Neural Network with Normalization, Weight Decay, and SGD*. arXiv:2006.08419. https://arxiv.org/abs/2006.08419 — an earlier analysis of norm dynamics for SGD with decay, under stated assumptions.
- Li, Z., & Arora, S. (2019). *An Exponential Learning Rate Schedule for Deep Learning*. ICLR 2020. https://arxiv.org/abs/1910.07454 — shows that weight decay with normalisation is equivalent to SGD under an exponentially increasing learning rate.
- Wang, X., & Aitchison, L. (2024). *How to Set AdamW's Weight Decay as You Scale Model and Dataset Size*. arXiv:2405.13698. https://arxiv.org/abs/2405.13698 — uses the same timescale view to choose the decay for different scales.
