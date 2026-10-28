---
status: draft
last_reviewed: 2026-10-28
tags:
  - deep learning
  - optimization
  - initialisation
aliases:
  - He initialisation
  - He initialization
  - Kaiming initialisation
  - Kaiming initialization
  - He 初始化
  - Kaiming 初始化
---

# He Initialisation

He, or Kaiming, initialisation sets the variance of each weight to \(2/n_{\text{in}}\) in networks built from rectified linear units. He et al. derived it in 2015 by correcting the [Xavier (Glorot) rule](../glorot-xavier/index.md) for the fact that a rectifier removes the negative half of its input. In the paper's experiments it trained a plain 30-layer network from random weights where the Xavier scheme stalled. It is one of the methods compared on the parent [weight initialisation](../index.md) page.

## Overview

Glorot and Bengio's rule was derived for activations that are symmetric with unit slope at zero, such as tanh. The rectified linear unit, \(\max(0, x)\), is neither, yet it became the standard activation for deep convolutional networks. He et al. (2015) asked what scale suits rectified networks, and found that it differs from the Xavier rule by a factor of two in variance.

The paper also derived the rule for the parametric rectifier (PReLU), which has a learned negative slope and covers the ordinary rectifier and the linear case.

## Key concepts

- **Rectifier.** A unit that outputs its input when positive and zero otherwise. For a symmetric input distribution it keeps about half of the input's second moment.
- **Negative slope \(a\).** In PReLU, negative inputs are multiplied by \(a\). \(a = 0\) gives the ordinary rectifier and \(a = 1\) a linear unit.
- **Backward condition.** The gradient through a layer is a sum over the units it feeds, so the backward condition uses the number of outputs. When widths are similar, the two choices give nearly the same scale.

## How it works

Let layer \(l\) have \(n_l\) inputs, which are the outputs of a rectifier in the previous layer. The variance of the pre-activation is \(\mathrm{Var}[y_l] = n_l \mathrm{Var}[w_l]\,\mathrm{E}[x_l^2]\), and for a rectifier \(\mathrm{E}[x_l^2] = \tfrac{1}{2}\mathrm{Var}[y_{l-1}]\). Over \(L\) layers,

\[
\mathrm{Var}[y_L] = \mathrm{Var}[y_1] \prod_{l=2}^{L} \tfrac{1}{2} n_l \mathrm{Var}[w_l].
\]

Each factor must equal one, so \(\tfrac{1}{2} n_l \mathrm{Var}[w_l] = 1\), which gives

\[
w_l \sim \mathcal{N}\left(0, \frac{2}{n_l}\right),
\]

a zero-mean Gaussian with standard deviation \(\sqrt{2/n_l}\). Biases are set to zero. For PReLU with slope \(a\) the condition becomes \(\tfrac{1}{2}(1 + a^2)\,n_l \mathrm{Var}[w_l] = 1\), which recovers the rectifier at \(a = 0\) and the linear case at \(a = 1\).

For the backward pass the same argument gives \(\tfrac{1}{2}\hat{n}_l\mathrm{Var}[w_l] = 1\), where \(\hat{n}_l\) is the number of outputs times the square of the kernel size. The paper notes that either condition alone suffices for convergence in its networks. The procedure is: for each layer, compute \(n_l\) (inputs times kernel area), draw weights from \(\mathcal{N}(0, 2/n_l)\), and set biases to zero.

## Results

He et al. compared the scheme with Xavier on the ImageNet 2012 classification benchmark.

- **Moderately deep models.** On a 22-layer model both schemes converged, and the new scheme began reducing error earlier. For a 14-layer model the paper reports top-1 and top-5 error of 33.82% and 13.34% with the new scheme, against 33.90% and 13.44% with Xavier, and no clear accuracy difference between them.
- **Extremely deep models.** In the comparison of models of up to 30 layers (27 convolutional and 3 fully connected), the new scheme made the 30-layer model converge, while the Xavier scheme stalled with diminishing gradients.
- **Final system.** A PReLU network reached 4.94% top-5 error on ImageNet 2012, which the authors report as a 26% relative improvement over GoogLeNet's 6.66%.

The paper also reports that its 30-layer ImageNet model reached 38.56% top-1 and 16.59% top-5 error, clearly worse than the 14-layer model. In these experiments, depth alone did not improve accuracy.

## Limitations

- **Scale, not accuracy.** The scheme keeps signals at a sensible size at the start; it does not show that the trained network generalises better.
- **Depth has diminishing returns.** The deeper ImageNet model did worse, and the paper cites other studies where deeper networks saturated. Initialisation makes deep networks trainable but does not guarantee that depth helps.
- **The derivation is for rectifiers.** GELU, SiLU and other activations are not covered by the factor of one half and need their own gain.
- **Width changes.** The rule fixes the scale at one width; [muP](../mup/index.md) addresses how the learning rate should change as the network widens.

## Open questions

- What gain suits the gated feed-forward blocks common in modern Transformers.
- Whether the advantage persists at great depth with residual connections and normalisation, which the paper's plain networks did not test.

## References

### Seminal papers

- He, K., Zhang, X., Ren, S. & Sun, J. (2015). *Delving Deep into Rectifiers: Surpassing Human-Level Performance on ImageNet Classification*. arXiv. https://arxiv.org/abs/1502.01852 — Derives the \(2/n_l\) initialisation for rectifiers and PReLU, and shows that a 30-layer network converges with it.
- Glorot, X. & Bengio, Y. (2010). *Understanding the difficulty of training deep feedforward neural networks*. AISTATS. https://proceedings.mlr.press/v9/glorot10a.html — The Xavier or normalised initialisation, which He et al. adapt for rectified units.

### Articles and documentation

- Schoenholz, S. S., Gilmer, J., Ganguli, S. & Sohl-Dickstein, J. (2017). *Deep Information Propagation*. arXiv. https://arxiv.org/abs/1611.01232 — Uses mean-field theory to show how depth limits the trainability of random networks.
- Pennington, J., Schoenholz, S. S. & Ganguli, S. (2017). *Resurrecting the sigmoid in deep learning through dynamical isometry: theory and practice*. arXiv. https://arxiv.org/abs/1711.04735 — Shows that ReLU networks cannot reach dynamical isometry; sigmoidal networks can.
- He, K., Zhang, X., Ren, S. & Sun, J. (2016). *Identity Mappings in Deep Residual Networks*. arXiv. https://arxiv.org/abs/1603.05027 — Shows how identity skip connections interact with rectified residual blocks.
