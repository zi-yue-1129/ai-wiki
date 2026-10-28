---
status: draft
last_reviewed: 2026-10-28
tags:
- model compression
- quantisation
- binary neural networks
aliases:
  - Binary neural networks
  - Ternary weight networks
  - 二值化網路
  - 三值化網路
---

# Binary and Ternary Quantisation

Binary and ternary quantisation restrict weights, and sometimes activations, to two values (\(\pm 1\)) or three (\(-1, 0, +1\)). This is the extreme end of [quantisation](../index.md): the storage per weight falls to one or two bits, and multiplications can be replaced by sign flips and additions. Accuracy is harder to keep, so the methods in this family focus on how the scale is handled and how gradients are passed through the discrete values.

## Overview

A binary weight network uses \(W_b = \alpha \cdot \operatorname{sign}(W)\), where \(\alpha\) is a real-valued scale. A ternary network uses values in \(\{-\alpha, 0, +\alpha\}\), so it can drop small weights to zero. Both need the [straight-through estimator](../quantisation-aware-training/index.md) during training, because the sign function has zero gradient almost everywhere.

## Key concepts

- **Scale factor.** A single real scale per layer or per filter keeps the output magnitude close to the full-precision layer. Without it, binary networks lose most of their accuracy.
- **Zero in ternary networks.** The zero value lets a ternary network prune weights as it quantises them, so it sits between binary networks and [pruning](../../pruning/index.md).
- **Binary activations.** Quantising activations as well as weights removes most multiplications, but it discards more information and is harder to train.

## Key methods

### BinaryConnect (Courbariaux et al., 2015)

- **Problem:** Training networks with binary weights during propagation seemed to require binary updates, which do not work with gradient descent.
- **Core idea:** Keep full-precision weights for the parameter updates and binarise them only when computing the forward and backward passes. The binarisation acts as a regulariser.
- **Equation or algorithm:** Forward pass with \(\operatorname{sign}(W)\), gradients computed at the binary weights, updates applied to the real-valued \(W\), and clipping of \(W\) to a bounded range.
- **Results:** The authors report near state-of-the-art results on permutation-invariant MNIST, CIFAR-10 and SVHN, and say binarisation acts as a regulariser.
- **Limitations:** The method was shown on small networks and datasets of its time. It does not include the per-layer scale factor that later methods found important.

### XNOR-Net (Rastegari et al., 2016)

- **Problem:** Binary networks lose much accuracy on ImageNet, because the magnitudes of the weights and activations are discarded.
- **Core idea:** Approximate each real-valued filter by a binary filter times a scale factor computed from the mean absolute value of the filter, so that the output magnitude is preserved. The convolution is then computed with XNOR operations and popcount.
- **Equation or algorithm:** \(W \approx \alpha \cdot B\) with \(B = \operatorname{sign}(W)\) and \(\alpha = \lVert W \rVert_1 / n\), with a similar binarisation of activations in the full XNOR-Net variant.
- **Results:** The abstract reports that the binary-weight version of AlexNet is only 2.9% less accurate than the full-precision AlexNet in top-1 accuracy.
- **Limitations:** The binarised activation version loses more accuracy. The method needs hardware with fast bit operations to realise its speed-up.

### Ternary Weight Networks (Li et al., 2016)

- **Problem:** Binary weights remove too much information. A three-value code keeps a zero, which is cheap and expressive.
- **Core idea:** Quantise each weight to one of three values, with a threshold on the magnitude below which the weight is zero and a scale for the non-zero values.
- **Equation or algorithm:** The threshold and scale are chosen to minimise the expected squared error between the ternary and full-precision weights, approximated per filter.
- **Results:** The abstract reports up to 16 times model compression. The accuracy gap to full precision is given in the paper's tables, and should be read there rather than compared across papers.
- **Limitations:** Ternary arithmetic needs support in hardware. Compression ratios assume the ternary code is stored efficiently.

## Trade-offs

- **Compression versus accuracy.** Going from ternary to binary halves the storage per weight but removes the zero value. The accuracy cost depends on the task and the training recipe, so the papers' tables are the reference.
- **Hardware support.** Binary and ternary networks gain most when the chip implements bitwise operations. On a GPU, the gain is limited.
- **Training difficulty.** Gradient approximations are biased, and results depend on the training schedule.

## More variants and open issues

- **Open issue:** whether binary networks can match full-precision accuracy on large transformers, where most reported gains are on small convolutional networks.
- **Open issue:** how to train binary activations stably at scale.
- **Variant:** learned scale factors per channel, which bring binary networks closer to [mixed-precision](../mixed-precision/index.md) schemes.

## Connections

The extreme low-bit regime connects to the [hardware](../../../../engineering/hardware/index.md) discussion of bit-serial and in-memory computation. The zero value in ternary networks links to [pruning](../../pruning/index.md), and the training of discrete weights links to [neuroscience](../../../../brain-mind/neuroscience/index.md) questions about low-precision synapses.

## References

### Seminal papers

- Courbariaux, M., Bengio, Y., David, J.-P. (2015). *BinaryConnect: Training Deep Neural Networks with Binary Weights during Propagations*. arXiv:1511.00363. https://arxiv.org/abs/1511.00363 — Trains with binary weights in the forward pass while keeping real-valued weights for updates.
- Rastegari, M., Ordonez, V., Redmon, J., Farhadi, A. (2016). *XNOR-Net: ImageNet Classification Using Binary Convolutional Neural Networks*. arXiv:1603.05279. https://arxiv.org/abs/1603.05279 — Binary filters with scale factors that keep AlexNet within 2.9% top-1 accuracy.
- Li, F., Liu, B., Wang, X., Zhang, B., Yan, J. (2016). *Ternary Weight Networks*. arXiv:1605.04711. https://arxiv.org/abs/1605.04711 — Three-value weights with a learned threshold and scale, reaching up to 16 times compression.

### Surveys and textbooks

- Gholami, A., et al. (2021). *A Survey of Quantization Methods for Efficient Neural Network Inference*. arXiv:2103.13630. https://arxiv.org/abs/2103.13630 — Reviews low-bit methods and their trade-offs.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Jacob, B., et al. (2017). *Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference*. arXiv:1712.05877. https://arxiv.org/abs/1712.05877 — Integer-only inference, the 8-bit counterpart to the binary methods above.
