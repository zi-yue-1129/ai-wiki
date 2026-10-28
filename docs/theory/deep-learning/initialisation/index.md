---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/optimization
  - theory/models/transformer
  - brain-mind/computational-neuroscience
tags:
  - deep learning
  - optimization
  - initialisation
  - residual connections
aliases:
  - Weight initialisation
  - Weight initialization
  - Parameter initialisation
  - 權重初始化
  - 初始化
---

# Weight Initialisation and Signal Propagation

Weight initialisation sets the starting values of a network's parameters before training begins. Because a deep network multiplies its signals through many layers, the scale of those starting values decides whether activations and gradients shrink towards zero, grow without bound, or keep a usable size. The study of how signals travel through a network at its starting point is called signal propagation.

## Overview

Training begins from random numbers. In the first steps, the behaviour of the network is set almost entirely by them, and the gradients the optimiser uses are computed from them. If the weights are too small, activations shrink layer by layer and the signal fades before it reaches the output. If they are too large, activations grow and units saturate. In both cases the backward gradients are badly scaled, and learning slows or stops. Glorot and Bengio (2010) showed this for deep sigmoid and tanh networks trained from naive random starts, and that the choice of scale changed how fast they converged.

Initialisation matters beyond the first steps. The starting scale helps decide how deep a plain network can be and still train, and whether a setting that works for a small model also works for a large one. The second concern led to hyperparameter transfer methods, discussed under muP below.

Later designs, such as residual connections and normalisation layers, reduced the sensitivity to the starting scale without removing it.

## Key concepts

- **Fan-in and fan-out.** The number of inputs \(n_{\text{in}}\) and outputs \(n_{\text{out}}\) of a layer. Most initialisation rules set the weight variance from one of these.
- **Variance propagation.** The variance of activations, and of gradients, is multiplied by a roughly fixed factor at each layer.
- **Gain.** The factor by which a layer and its nonlinearity multiply the variance of a signal. A gain of one preserves the scale.
- **Saturation.** When a unit's input is so large that its activation is nearly flat and its gradient is close to zero. Sigmoid and tanh units saturate; rectified units do not saturate for positive inputs.
- **Edge of chaos.** The boundary between an ordered regime, in which different inputs become more alike with depth, and a chaotic regime, in which nearby inputs are pushed apart. Trainability is usually best near this boundary.
- **Dynamical isometry.** The condition that all singular values of the network's input–output Jacobian are close to one.

## How it works

For one linear layer with \(n\) inputs whose activations have variance \(\mathrm{Var}[x]\), and weights that are independent, zero-mean and have variance \(\mathrm{Var}[w]\), the output \(y = \sum_j w_j x_j\) has

\[
\mathrm{Var}[y] = n\,\mathrm{Var}[w]\,\mathrm{Var}[x].
\]

The factor \(n\,\mathrm{Var}[w]\) is the forward gain. Through \(L\) layers of roughly linear behaviour, the activation variance is multiplied by the product of these gains. The same argument for gradients uses the number of outputs instead of inputs. Depending on the per-layer gain, the signal either shrinks exponentially with depth, grows exponentially, or stays about the same size.

Glorot and Bengio (2010) could satisfy the forward and backward conditions together only when all layers have the same width, so they chose \(\mathrm{Var}[w] = 2/(n_{\text{in}} + n_{\text{out}})\). He et al. (2015) noticed that a rectified unit zeroes its negative inputs and so removes about half of the second moment. The forward gain of a rectified layer is then \(\tfrac{1}{2} n\,\mathrm{Var}[w]\), and the matching choice is \(\mathrm{Var}[w] = 2/n_{\text{in}}\). The [Xavier/Glorot](glorot-xavier/index.md) and [He](he-initialisation/index.md) pages give the details.

### Depth, chaos and the edge of chaos

The per-layer gain is a linear argument. For nonlinear networks with random weights, mean-field theory tracks how the similarity between two inputs changes with depth. In the ordered phase, different inputs become more alike; in the chaotic phase, nearby inputs are pushed apart. Poole et al. (2016) describe this as an order-to-chaos expressivity transition, in which the curvature of the functions computed by chaotic networks grows exponentially with depth. Schoenholz et al. (2017) defined depth scales that limit how far a signal can travel, and argued that a network can be trained only when information can travel through it. Near the edge of chaos one depth scale diverges, so very deep networks can be trained if they are set close to that boundary.

Pennington et al. (2017) found that rectified networks cannot reach dynamical isometry, while sigmoidal networks can, but only with orthogonal weights.

### Why residual connections and normalisation help

A residual block computes \(x + F(x)\). Its identity path carries the signal without multiplication, so the block's gain stays near one even when \(F\) contributes little. He et al. (2016) showed that with identity skip connections, forward and backward signals can pass directly from any block to any other.

Normalisation works differently. De and Smith (2020) showed that at initialisation batch normalisation scales each residual branch down, relative to the skip path, by about the square root of the depth, so early in training each block is close to the identity. Zhang et al. (2019) reached a similar effect without normalisation by rescaling the initialisation (Fixup), and trained residual networks with 10,000 layers as stably as normalised ones. Brock et al. (2021) used signal propagation tools with weight standardisation to build normalisation-free residual networks competitive with EfficientNets on ImageNet. The [normalisation layers](../normalisation/index.md) page covers the normalisers themselves.

## Key methods

Each method has its own page. The comparison here is brief.

| Method | Year | Core idea | Page |
|---|---|---|---|
| Xavier (Glorot) initialisation | 2010 | Variance \(2/(n_{\text{in}}+n_{\text{out}})\), keeping forward and backward signals similar in near-linear layers | [Xavier/Glorot](glorot-xavier/index.md) |
| He initialisation | 2015 | Variance \(2/n_{\text{in}}\), compensating for the half of the signal that rectifiers remove | [He initialisation](he-initialisation/index.md) |
| Maximal update parametrisation (muP) | 2021 | Scales initialisation and learning rates with width so features learn at a comparable rate and settings transfer | [muP](mup/index.md) |

Xavier and He are rules for one network at its starting point. muP says how the starting scale and learning rates should change as the network is made wider.

## Connections

Initialisation is tied to the rest of training. The learning-rate warm-up described on the [gradual warm-up](../../optimization/gradual-warm-up.md) page is often explained as protection against the unreliable early gradients a poor start produces. The [residual networks](../../models/cnn/backbones-and-scaling/resnet/index.md) and [Transformer](../../models/transformer/index.md) pages show where the identity path and normalisation placement are used.

The brain-and-mind angle concerns dynamics rather than training. Van Vreeswijk and Sompolinsky (1996) showed that networks of excitatory and inhibitory neurons whose inputs nearly balance produce strongly chaotic activity even under constant input, in the same family of random-network analysis as the earlier work of Sompolinsky, Crisanti and Sommers (1988). This shows that neural circuits can sit in a chaotic regime without blowing up. It does not show that the cortex is tuned to the edge of chaos, and biological circuits are not drawn from independent random numbers: their initial wiring is shaped by development, as the [developmental cognition](../../../brain-mind/developmental-cognition/index.md) page describes.

## Applications

- **Training deep networks.** Glorot and He schemes are standard options, and He initialisation is the usual choice for rectified networks.
- **Normalisation-free networks.** Fixup and the designs of Brock et al. (2021) show that careful initialisation can replace normalisation layers in residual networks.
- **Tuning very large models.** muP lets a sweep run on a small model and the best settings be reused for a much larger one. The [muP](mup/index.md) page reports the evidence.

## Open questions

- **Does the starting analysis predict trained networks?** Most of the theory describes the network at initialisation, and training moves the weights far from that point. How far the edge-of-chaos and isometry conditions survive training is not settled.
- **Do infinite-width limits describe real networks?** The muP rules and the kernel limit of very wide networks are derived as width tends to infinity. Yang and Hu (2021) note that the standard and NTK parametrisations do not admit a limit in which features learn. How well the limits describe practical networks is an active question.
- **What makes normalisation help?** The identity-at-initialisation account of De and Smith (2020) explains part of the benefit of batch normalisation in residual networks. Whether it explains the rest is still debated.
- **Biology.** Whether neural systems tune their gain towards a critical regime by an analogous mechanism is unknown.

## References

### Seminal papers

- Glorot, X. & Bengio, Y. (2010). *Understanding the difficulty of training deep feedforward neural networks*. AISTATS. https://proceedings.mlr.press/v9/glorot10a.html — Introduces the normalised initialisation with variance \(2/(n_i+n_{i+1})\), based on keeping activation and gradient variances constant.
- He, K., Zhang, X., Ren, S. & Sun, J. (2015). *Delving Deep into Rectifiers: Surpassing Human-Level Performance on ImageNet Classification*. arXiv. https://arxiv.org/abs/1502.01852 — Corrects the Xavier derivation for rectified units and shows that a 30-layer network trains with the new scheme where Xavier stalls.
- Sompolinsky, H., Crisanti, A. & Sommers, H. J. (1988). *Chaos in Random Neural Networks*. Physical Review Letters. https://doi.org/10.1103/PhysRevLett.61.259 — Early analysis of random recurrent networks, which identifies the transition between ordered and chaotic dynamics.
- Poole, B., Lahiri, S., Raghu, M., Sohl-Dickstein, J. & Ganguli, S. (2016). *Exponential expressivity in deep neural networks through transient chaos*. arXiv. https://arxiv.org/abs/1606.05340 — Mean-field analysis of random deep networks that identifies an order-to-chaos expressivity transition.
- Schoenholz, S. S., Gilmer, J., Ganguli, S. & Sohl-Dickstein, J. (2017). *Deep Information Propagation*. arXiv. https://arxiv.org/abs/1611.01232 — Defines depth scales that limit the trainability of random networks and argues that trainability is best near the edge of chaos.
- van Vreeswijk, C. & Sompolinsky, H. (1996). *Chaos in Neuronal Networks with Balanced Excitatory and Inhibitory Activity*. Science. https://doi.org/10.1126/science.274.5293.1724 — Shows that balanced excitation and inhibition in neuronal network models produce strongly chaotic activity.
- Yang, G. & Hu, E. J. (2021). *Feature Learning in Infinite-Width Neural Networks*. arXiv. https://arxiv.org/abs/2011.14522 — Shows that the standard and NTK parametrisations have no feature-learning infinite-width limit and proposes the maximal update parametrisation.
- Yang, G., Hu, E. J., Babuschkin, I., Sidor, S., Liu, X., Farhi, D. et al. (2022). *Tensor Programs V: Tuning Large Neural Networks via Zero-Shot Hyperparameter Transfer*. arXiv. https://arxiv.org/abs/2203.03466 — Introduces muTransfer, which tunes hyperparameters on small models and transfers them to large Transformers and ResNets.

### Articles and documentation

- Pennington, J., Schoenholz, S. S. & Ganguli, S. (2017). *Resurrecting the sigmoid in deep learning through dynamical isometry: theory and practice*. arXiv. https://arxiv.org/abs/1711.04735 — Computes the Jacobian singular value distribution and shows which activations and initialisations reach dynamical isometry.
- He, K., Zhang, X., Ren, S. & Sun, J. (2016). *Identity Mappings in Deep Residual Networks*. arXiv. https://arxiv.org/abs/1603.05027 — Analyses how identity skip connections let forward and backward signals reach any block, and proposes a residual unit that eases training.
- De, S. & Smith, S. L. (2020). *Batch Normalization Biases Residual Blocks Towards the Identity Function in Deep Networks*. arXiv. https://arxiv.org/abs/2002.10444 — Shows that batch normalisation downscales residual branches at initialisation, making deep residual blocks close to the identity.
- Zhang, H., Dauphin, Y. N. & Ma, T. (2019). *Fixup Initialization: Residual Learning Without Normalization*. arXiv. https://arxiv.org/abs/1901.09321 — Rescales a standard initialisation so that residual networks train without normalisation layers, including networks with 10,000 layers.
- Brock, A., De, S. & Smith, S. L. (2021). *Characterizing signal propagation to close the performance gap in unnormalized ResNets*. arXiv. https://arxiv.org/abs/2101.08692 — Uses signal propagation tools with weight standardisation to design normalisation-free ResNets competitive with EfficientNets.
