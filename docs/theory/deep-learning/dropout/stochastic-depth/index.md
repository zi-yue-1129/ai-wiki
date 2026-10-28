---
status: draft
last_reviewed: 2026-10-28
tags:
  - regularisation
  - residual connections
  - deep learning
aliases:
  - Stochastic Depth
  - DropPath
  - 隨機深度
---

# Stochastic Depth

Stochastic depth trains a residual network by randomly skipping whole residual blocks in each mini-batch, so that a skipped block passes its input straight through. Huang et al. (2016) introduced it as a way to train very deep networks. It is one of the methods on the parent [dropout and stochastic regularisation](../index.md) page.

## Overview

Residual networks made it possible to train networks with hundreds of layers. Each block adds a learned function to its input through an identity shortcut (see [ResNet](../../../models/cnn/backbones-and-scaling/resnet/index.md)). Huang et al. observed that very deep residual networks still have costs. Gradients can vanish, the forward signal can weaken, and training is slow. Their proposal was to train with a short effective network while using the full depth at test time.

Stochastic depth does this by dropping blocks at random during training. It is dropout applied to whole layers rather than to individual units. Because the shortcut stays in place, a dropped block does not break the signal path. The network simply runs without that block for one step.

## Key concepts

- **Residual block.** A learned transform \(f\) with an identity shortcut, so that the output is the input plus \(f(\text{input})\).
- **Survival probability.** The chance that a given block is kept in a mini-batch. In the paper it decreases linearly with depth, so early blocks are kept more often than late ones.
- **Identity shortcut.** The path that carries the input unchanged. It is what makes skipping a block safe.
- **Effective depth.** The number of blocks actually used on one training step. It is smaller than the full depth and changes from step to step.

## How it works

For block \(l\), let \(b_l\) be a Bernoulli variable that equals 1 with survival probability \(p_l\). During training, the output of the block is

\[
H_l = \mathrm{ReLU}\big(b_l\, f_l(H_{l-1}) + H_{l-1}\big).
\]

At test time every block is used, and the residual branch is scaled by its survival probability:

\[
H_l = \mathrm{ReLU}\big(p_l\, f_l(H_{l-1}) + H_{l-1}\big).
\]

The training procedure is:

1. Choose a survival probability for each block, decreasing with depth.
2. For each mini-batch, sample \(b_l\) independently for every block.
3. Skip the blocks with \(b_l = 0\), so that their input passes through the shortcut.
4. Compute the loss and update the weights. A skipped block receives no gradient from that mini-batch.
5. At test time, use all blocks and scale each residual branch by its survival probability.

The scaling at test time plays the same role as the rescaling in dropout. It keeps the expected output of each block close to what the network saw during training.

## Results

The abstract of Huang et al. (2016) reports that stochastic depth reduces training time substantially and improves test error significantly on almost all of the datasets used for evaluation. It also reports that the method allows residual networks to be made deeper than 1200 layers while still giving meaningful improvements, with 4.91% test error on CIFAR-10.[^1] The comparisons are with ordinary residual networks trained without the method.

## Limitations

- **It needs residual structure.** The method relies on identity shortcuts. Skipping a block in a plain network without them would remove part of the signal.
- **It adds a schedule.** The survival probabilities are a design choice. The linear decay rule is a heuristic that the paper motivates but does not derive.
- **Test-time network is not a sampled one.** Every test-time pass uses the full depth, so the scaled network is an average over depths and not one of the networks seen in training. This is the same approximation that dropout makes.
- **Explanations are partial.** Huang et al. explain the benefit through shorter effective depth during training. Veit et al. (2016) argue that residual networks are ensembles of paths, and that most of the gradient in a 110-layer network comes from paths only 10 to 34 layers long. The two accounts are compatible, but neither settles why the method works.

## Open questions

- **Which account is right?** Is the benefit a shorter effective depth during training, an implicit ensemble of paths, or both?
- **Which schedule?** The best survival probabilities, and whether they should vary with architecture or dataset size, are not known in general.
- **Beyond residual networks.** Transformer blocks also have residual connections, so the same idea can be applied to them. How well the benefit carries over to other architectures is an empirical question.

## Connections

Stochastic depth is the block-level counterpart of [dropout](../index.md), which works on units. Both are regularisers that rely on redundancy in the network, so that no single part is indispensable. The residual structure it depends on is described in the [ResNet](../../../models/cnn/backbones-and-scaling/resnet/index.md) page, and the same idea is relevant to [Transformer](../../../models/transformer/index.md) blocks. For the brain, there is no established analogue of skipping whole processing stages, although parallel and bypass pathways exist in the cortex. See [NeuroAI](../../../../brain-mind/neuroai/index.md).

## Applications

- **Very deep image classifiers.** Stochastic depth was developed to train residual networks with hundreds or more than a thousand layers.
- **Shorter training time.** The paper reports that the method reduces the time needed to train deep residual networks.
- **Other residual architectures.** The idea of dropping residual branches can be used in any architecture built from residual blocks.

[^1]: Figures quoted from the abstract of Huang et al. (2016). The benchmark tables are in the paper.

## References

### Seminal papers

- Huang, G. et al. (2016). *Deep Networks with Stochastic Depth*. arXiv. https://arxiv.org/abs/1603.09382 — The paper itself: randomly drops residual blocks during training and uses the full network at test time, scaled by survival probability.
- He, K. et al. (2015). *Deep Residual Learning for Image Recognition*. arXiv. https://arxiv.org/abs/1512.03385 — Introduces residual learning with identity shortcuts, the architecture that stochastic depth modifies.
- Hinton, G. E. et al. (2012). *Improving neural networks by preventing co-adaptation of feature detectors*. arXiv. https://arxiv.org/abs/1207.0580 — The preprint that introduced dropout, the unit-level form of the same idea.

### Articles and documentation

- He, K. et al. (2016). *Identity Mappings in Deep Residual Networks*. arXiv. https://arxiv.org/abs/1603.05027 — Analyses identity skip connections and proposes a residual unit that eases the training of very deep networks.
- Veit, A., Wilber, M. & Belongie, S. (2016). *Residual Networks Behave Like Ensembles of Relatively Shallow Networks*. arXiv. https://arxiv.org/abs/1605.06431 — Describes residual networks as collections of paths of different lengths, most of which are short.
