---
status: complete
last_reviewed: 2026-11-11
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

He initialisation chooses the scale of random weights to compensate for rectifier nonlinearities. For a ReLU layer, the fan-in rule uses weight variance $2/n_{\mathrm{in}}$ to keep the expected squared activation stable under the initialisation assumptions.[^he]

## Overview

The chapter on weight initialisation describes signal propagation through deep networks. He initialisation uses the rectifier's effect on squared activations to set a layer's weight scale. The original paper also introduces PReLU, whose negative slope is learned during training. [Weight initialisation](index.md).[^he]

## Problem

Repeated multiplication by a scale factor below or above one can make signals shrink or grow exponentially with depth. Glorot initialisation balances forward and backward propagation using the two layer widths. He initialisation includes a rectifier-dependent gain in that calculation. [Glorot initialisation](glorot-initialisation.md).[^glorot][^he]

## Core idea

Write a preactivation as $z=\sum_{i=1}^{n_{\mathrm{in}}} w_i x_i$ with zero bias. Suppose the weights are independent, zero-mean, independent of the inputs, and have common variance $v$. Suppose also that the inputs have common second moment $m_2=\mathbb{E}[x_i^2]$. Then $\mathbb{E}[z]=0$ and $\mathbb{E}[z^2]=n_{\mathrm{in}}v m_2$. For a distribution of $z$ symmetric about zero, ReLU retains half of this second moment.[^he]

$$
\mathbb{E}[\operatorname{ReLU}(z)^2]
=\frac12\mathbb{E}[z^2]
=\frac{n_{\mathrm{in}}v}{2}m_2.
$$

Choosing $v=2/n_{\mathrm{in}}$ makes the multiplier one. The second moment and centred variance are related by $\operatorname{Var}(x)=\mathbb{E}[x^2]-\mathbb{E}[x]^2$. ReLU outputs generally have positive mean. For example, if $z\sim\mathcal{N}(0,q)$, direct integration gives $\mathbb{E}[\operatorname{ReLU}(z)^2]=q/2$ and $\operatorname{Var}(\operatorname{ReLU}(z))=q(1/2-1/(2\pi))$.[^he]

## Equation

### Normal and uniform forms

For a rectifier with negative slope $a$, the gain is $g=\sqrt{2/(1+a^2)}$. The forward rule uses the following distributions, with $a=0$ for ReLU. For PReLU, use the slope's value at initialisation.[^he][^pytorch]

$$
w_{ij}\sim\mathcal{N}\!\left(0,\frac{g^2}{n_{\mathrm{in}}}\right),
\qquad
w_{ij}\sim\mathcal{U}(-u,u),
\qquad
u=g\sqrt{\frac{3}{n_{\mathrm{in}}}}.
$$

These choices have the same weight variance, since a uniform distribution on $[-u,u]$ has variance $u^2/3$. The normal distribution's standard deviation is $g/\sqrt{n_{\mathrm{in}}}$.

### Fan-in, fan-out and tensor layout

The fan-in rule targets forward propagation. The analogous backward rule uses variance $g^2/n_{\mathrm{out}}$ under the gradient independence approximation. For a dense layer, the two fans count input and output features. For an ordinary ungrouped convolution with kernel size $k_h\times k_w$, they are $n_{\mathrm{in}}=C_{\mathrm{in}}k_hk_w$ and $n_{\mathrm{out}}=C_{\mathrm{out}}k_hk_w$.[^he][^pytorch]

PyTorch's `kaiming_normal_` and `kaiming_uniform_` use `mode="fan_in"` or `mode="fan_out"`. Their fan calculation assumes a dense weight tensor shaped `[out_features, in_features]` for the operation `x @ w.T`. For a custom matrix stored as `[in_features, out_features]` and used as `x @ w`, initialise `w.T`. Set `nonlinearity="relu"` for ReLU, or `nonlinearity="leaky_relu"` with the actual negative slope passed as `a`.[^pytorch]

### Worked convolution example

An ungrouped $3\times3$ convolution mapping 16 input channels to 32 output channels has weight shape $[32,16,3,3]$. Its fan-in is 144 and fan-out is 288. With ReLU and fan-in scaling, the weight variance is $1/72$, the normal standard deviation is about $0.11785$, and the uniform bound is about $0.20412$.

The forward second-moment multiplier is $144(1/72)/2=1$. With fan-out scaling the variance becomes $1/144$ and this forward multiplier becomes $1/2$, illustrating the role of the selected fan.

## Results

The original paper's Figure 3 compares initialisations on a 30-layer ReLU network. He initialisation allows that model to converge, while the Xavier-initialised run stalls. Its ImageNet classification results also depend on the architecture, activation and evaluation procedure. The best single model reaches 5.71% top-5 validation error with multi-scale and multi-view evaluation. A six-model combination reaches 4.94% top-5 test error.[^he]

## Limitations

- The calculation describes random weights at initialisation. Training changes the weights and their dependence on activations and gradients. Mean-field analyses study additional quantities, including how correlations between different inputs propagate through the network.[^propagation]
- Adding a residual branch changes the propagation calculation. Fixup studies architecture-dependent rescaling of residual branches for training deep networks without normalisation. [Normalisation](../normalisation/index.md).[^fixup]

## Connections

Glorot initialisation uses variance $2/(n_{\mathrm{in}}+n_{\mathrm{out}})$ at unit gain. For equal fans $n$, this becomes $1/n$, compared with the ReLU He variance $2/n$. Convolutional architectures supply the channel counts and kernel shapes that determine these fans. [Glorot initialisation](glorot-initialisation.md), [CNNs](../../models/cnn/index.md).[^glorot][^pytorch]

## Applications

The rule supplies a weight scale for dense and convolutional layers followed by ReLU or leaky ReLU. Choosing the gain and fan mode ties the implementation to the activation and propagation direction being modelled. [PyTorch initialisation documentation](https://docs.pytorch.org/docs/2.15/nn.init.html).[^pytorch]

## Open questions

- How should signal propagation determine gains for non-rectifier nonlinearities and gated layers?
- How should per-layer gains interact with depth-dependent residual scaling?

[^he]: He et al., [*Delving Deep into Rectifiers*](https://arxiv.org/html/1502.01852), §2.2, Equations 7–15, Figure 3 and Tables 6–7.
[^glorot]: Glorot and Bengio, [*Understanding the Difficulty of Training Deep Feedforward Neural Networks*](https://proceedings.mlr.press/v9/glorot10a.html), §4.2.
[^pytorch]: PyTorch 2.15, [*torch.nn.init*](https://docs.pytorch.org/docs/2.15/nn.init.html), the gain table and Kaiming normal/uniform documentation.
[^propagation]: Schoenholz et al., [*Deep Information Propagation*](https://arxiv.org/abs/1611.01232), abstract and §2.
[^fixup]: Zhang, Dauphin and Ma, [*Fixup Initialization*](https://arxiv.org/abs/1901.09321), §§2–3.

## References

### Seminal papers

- He, K., Zhang, X., Ren, S. & Sun, J. (2015). *Delving Deep into Rectifiers: Surpassing Human-Level Performance on ImageNet Classification*. https://arxiv.org/abs/1502.01852 — Derives rectifier-aware initialisation, introduces PReLU and reports the ImageNet experiments.
- Glorot, X. & Bengio, Y. (2010). *Understanding the Difficulty of Training Deep Feedforward Neural Networks*. AISTATS. https://proceedings.mlr.press/v9/glorot10a.html — Derives an initialisation that balances forward and backward signal scales.
- Schoenholz, S. S., Gilmer, J., Ganguli, S. & Sohl-Dickstein, J. (2017). *Deep Information Propagation*. ICLR. https://arxiv.org/abs/1611.01232 — Studies variance and correlation propagation in randomly initialised deep networks.
- Zhang, H., Dauphin, Y. N. & Ma, T. (2019). *Fixup Initialization: Residual Learning Without Normalization*. ICLR. https://arxiv.org/abs/1901.09321 — Develops residual-branch initialisation using network depth and update-scale analysis.

### Articles and documentation

- PyTorch 2.15. *torch.nn.init*. https://docs.pytorch.org/docs/2.15/nn.init.html — Specifies activation gains, fan modes and tensor-layout assumptions for Kaiming initialisation.
