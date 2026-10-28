---
status: draft
last_reviewed: 2026-10-28
tags:
  - deep learning
  - optimization
  - initialisation
aliases:
  - Xavier initialisation
  - Xavier initialization
  - Glorot initialisation
  - Glorot initialization
  - Xavier 初始化
  - Glorot 初始化
---

# Xavier (Glorot) Initialisation

Xavier, or Glorot, initialisation sets the variance of each weight matrix to \(2/(n_{\text{in}}+n_{\text{out}})\), so that forward signals and backward gradients both keep a similar scale through a deep network. Glorot and Bengio proposed it in 2010 while studying why deep networks trained from random starts learned so slowly. It is one of the methods compared on the parent [weight initialisation](../index.md) page.

## Overview

In 2010, deep feedforward networks were hard to train from random weights. Glorot and Bengio asked why standard gradient descent from random initialisation did so poorly. They trained deep networks with several activation functions and monitored the activations and gradients of each layer during training.

Their main observation concerned the logistic sigmoid. Its mean output is positive, which drives the top hidden layer towards saturation early in training, and saturated units learn slowly. Their analysis gave a rule for the scale of the initial weights that keeps the variance of activations and gradients roughly constant across layers. The paper calls it the normalised initialisation; it is now usually called Xavier or Glorot initialisation.

## Key concepts

- **Fan-in and fan-out.** For a dense layer, \(n_{\text{in}}\) is the number of inputs to each unit and \(n_{\text{out}}\) is the number of units it feeds. In the paper these are \(n_i\) and \(n_{i+1}\) for layer \(i\).
- **Linear regime.** The derivation assumes that at initialisation the network is approximately linear, the activation has unit derivative at zero, and inputs and weights are independent.
- **Saturation.** When a sigmoid or tanh unit's input is large, its output is flat and its gradient is near zero.

## How it works

Under the linear assumptions, a layer's pre-activations have variance \(n\,\mathrm{Var}[W]\,\mathrm{Var}[x]\). The forward condition \(n_i\mathrm{Var}[W^i] = 1\) keeps activation variance constant from layer to layer, and the backward condition \(n_{i+1}\mathrm{Var}[W^i] = 1\) keeps gradient variance constant. The two can both hold only when the widths are equal, so the authors average them:

\[
\mathrm{Var}[W^i] = \frac{2}{n_i + n_{i+1}}.
\]

The paper uses the uniform distribution with this variance, since a uniform distribution on \([-a, a]\) has variance \(a^2/3\):

\[
W^i \sim U\left[-\sqrt{\frac{6}{n_i + n_{i+1}}},\; +\sqrt{\frac{6}{n_i + n_{i+1}}}\right].
\]

The procedure is to draw each layer's weights from this distribution, with biases set to zero. The standard scheme the paper compares against, \(U[-1/\sqrt{n}, 1/\sqrt{n}]\), has forward gain one third of the required value in wide layers, so signals shrink with depth.

## Results

The paper's main evidence comes from fully connected networks with five hidden layers, trained on Shapeset-3×2, MNIST, CIFAR-10 and ImageNet. For tanh units, the paper's Table 1 shows test error falling from 27.15 to 15.60 on Shapeset-3×2, from 55.9 to 52.92 on CIFAR-10, and from 70.58 to 68.57 on ImageNet with the normalised initialisation. The paper calls the scheme quite helpful for tanh networks. Softsign networks were more robust to the initialisation, which the authors suggest is due to their gentler nonlinearity. These figures are the paper's own and were not re-run here.

## Limitations

- **The derivation is approximate.** It relies on a linear regime and independence assumptions that hold at initialisation, and the paper does not claim they persist during training.
- **It is tied to the activation.** A rectified unit zeroes half of its inputs and so is not symmetric with unit slope. The forward signal then loses about half its second moment per layer, and the rule is off by a factor of two in variance. [He initialisation](../he-initialisation/index.md) corrects this.
- **Widths differ.** The two conditions hold together only for equal widths, so the compromise is a heuristic otherwise.
- **Residual paths and attention are not covered.** The analysis is for plain feedforward stacks; see the [parent page](../index.md) for residual networks.
- **Hyperparameters do not transfer.** The rule fixes the starting scale at one width and says nothing about how the learning rate should change as the network widens. See [muP](../mup/index.md).

## Open questions

- Whether the forward–backward compromise suits layers of very different shapes, or should be tuned per task.
- How the rule interacts with adaptive optimisers such as Adam, which rescale each parameter's update and may reduce the sensitivity to the starting scale. The paper used plain stochastic gradient descent.
- How well the linear analysis predicts very deep networks that use residual connections and normalisation.

## References

### Seminal papers

- Glorot, X. & Bengio, Y. (2010). *Understanding the difficulty of training deep feedforward neural networks*. AISTATS. https://proceedings.mlr.press/v9/glorot10a.html — Introduces the normalised initialisation with variance \(2/(n_i+n_{i+1})\), based on keeping activation and gradient variances constant.
- He, K., Zhang, X., Ren, S. & Sun, J. (2015). *Delving Deep into Rectifiers: Surpassing Human-Level Performance on ImageNet Classification*. arXiv. https://arxiv.org/abs/1502.01852 — Corrects the Xavier derivation for rectified units and shows that a 30-layer network trains with the new scheme where Xavier stalls.

### Articles and documentation

- Pennington, J., Schoenholz, S. S. & Ganguli, S. (2017). *Resurrecting the sigmoid in deep learning through dynamical isometry: theory and practice*. arXiv. https://arxiv.org/abs/1711.04735 — Extends the analysis to nonlinear networks and shows which activations and initialisations keep all Jacobian singular values near one.
- Mishkin, D. & Matas, J. (2015). *All you need is a good init*. arXiv. https://arxiv.org/abs/1511.06422 — Proposes a data-driven alternative that orthonormally initialises each layer and then normalises the variance of its output.
- Schoenholz, S. S., Gilmer, J., Ganguli, S. & Sohl-Dickstein, J. (2017). *Deep Information Propagation*. arXiv. https://arxiv.org/abs/1611.01232 — Uses mean-field theory to find depth scales that limit how far signals travel through random networks at initialisation.
