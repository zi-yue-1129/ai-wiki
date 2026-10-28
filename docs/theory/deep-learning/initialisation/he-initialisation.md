---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/deep-learning/initialisation
  - theory/models/cnn
tags:
  - He initialisation
  - ReLU
  - initialisation
aliases:
  - He 初始化
  - Kaiming 初始化
  - He initialization
---

# He (Kaiming) initialisation

He initialisation sets the variance of a layer's weights to twice the value that the Glorot rule gives for the fan-in alone, which keeps signals stable through rectified linear activations. It made it possible to train very deep rectifier networks from scratch.

## Overview

The [chapter](index.md) covers the general picture. This page covers He initialisation, the rule for networks that use ReLU and its relatives. The paper that introduced it also introduced PReLU, a learned variant of the rectifier.

## Problem

A rectifier sets every negative input to zero, so about half of the signal is removed at each layer. With the Glorot scale, the variance of the signal shrinks by roughly half per layer, and a deep network loses its signal before training can begin.

## Core idea

Scale the weights so that the variance lost to the rectifier is recovered. For a layer with fan-in $n_{\text{in}}$ and a ReLU activation, the forward variance is preserved when the weight variance is $2/n_{\text{in}}$. He and colleagues derive this rule and also a version for the backward pass [(He et al., 2015)](https://arxiv.org/abs/1502.01852).

## Equation

For a normal initialisation of a rectifier layer,

$$W \sim \mathcal{N}\left(0,\; \frac{2}{n_{\text{in}}}\right)$$

For a parametric rectifier $\mathrm{PReLU}$ with slope $a$, the variance is scaled by $2/(1+a^2)$, which recovers the ReLU case at $a = 0$.

## Results

The paper reports a PReLU network that surpasses the reported human-level top-5 error on ImageNet 2012 classification, with the figure given in the abstract: 4.94% top-5 test error. It also reports that the initialisation makes very deep networks trainable where the previous scale did not.

## Limitations

- The rule assumes the activation is a rectifier and that inputs are independent, which holds only approximately in trained networks.
- Residual connections change the variance across blocks, so the rule has to be combined with careful placement of normalisation or scaled residual branches.

## Connections

He initialisation is derived by correcting the [Glorot rule](glorot-initialisation.md) for rectifiers. The architectures that use it most, residual networks, are covered in [CNNs](../../models/cnn/index.md). The regularisers that interact with activation scale are in [Dropout](../dropout/index.md).

## Applications

Default for convolutional and dense layers with ReLU or its variants, and in most image classification backbones.

## Open questions

- How should the rule change for activations with non-zero means, such as GELU or SwiGLU?
- Do residual scaling rules capture the best behaviour at great depth?

## References

### Seminal papers

- He, Zhang, Ren and Sun, *Delving Deep into Rectifiers: Surpassing Human-Level Performance on ImageNet Classification* (2015). https://arxiv.org/abs/1502.01852 — Introduces He initialisation and PReLU, and reports the top-5 error figure.
- Glorot and Bengio, *Understanding the difficulty of training deep feedforward neural networks*, Proceedings of the 13th International Conference on Artificial Intelligence and Statistics (2010). https://proceedings.mlr.press/v9/glorot10a.html — The rule that He initialisation corrects for rectifiers.
- He, Zhang, Ren and Sun, *Deep Residual Learning for Image Recognition*, IEEE Conference on Computer Vision and Pattern Recognition (2016). https://doi.org/10.1109/CVPR.2016.90 — Residual networks, which use this initialisation in their deepest form.
- Krizhevsky, Sutskever and Hinton, *ImageNet Classification with Deep Convolutional Neural Networks*, NeurIPS (2012). https://papers.nips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html — A deep rectifier network trained on ImageNet, the setting that motivated the rule.
- Schoenholz, Gilmer, Ganguli and Sohl-Dickstein, *Deep Information Propagation* (2016). https://arxiv.org/abs/1611.01232 — Mean-field analysis of signal propagation in rectifier and other deep networks.
