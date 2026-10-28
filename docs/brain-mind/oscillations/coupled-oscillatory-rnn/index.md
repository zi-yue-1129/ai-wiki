---
status: draft
last_reviewed: 2026-10-28
tags:
- recurrent networks
- sequence modelling
aliases:
  - 耦合振盪循環神經網路
  - coRNN
  - Coupled Oscillatory RNN
  - Oscillatory Recurrent Neural Network
  - Rusch and Mishra 2021
---

# Coupled Oscillatory Recurrent Neural Network (coRNN)

coRNN is a recurrent neural network whose hidden units are discretised equations of coupled, damped and forced oscillators. Rusch and Mishra (2021) proposed it for learning long sequences. It is an engineering architecture, not a model of the brain, but it is the most direct artificial counterpart of the ideas on [Neural Oscillations and Synchrony](../index.md) in this wiki.

## Overview

In long sequences, gradients propagated back through many recurrent steps tend to vanish or explode. The usual remedy is gating, as in the LSTM (Hochreiter & Schmidhuber, 1997). Rusch and Mishra take a different route. Coupled, forced and damped oscillators can keep their state variables bounded while still producing rich outputs, so they build an RNN from such oscillators and prove bounds on its hidden states and gradients under stated assumptions.

## Key concepts

- **Damping**: friction that removes energy from an oscillator over time. In coRNN it is set by a parameter $\epsilon$.
- **Oscillation frequency**: set by a parameter $\gamma$ and by the diagonal of the recurrent weight matrix $W$.
- **Gradient stability**: the property that gradients neither explode nor vanish over long sequences. The bounds are the paper's main theoretical claim.
- **IMEX discretisation**: a time-stepping scheme that treats some terms implicitly and others explicitly. In coRNN it sets how damping is applied.

## How it works

The starting point is a second-order equation for each hidden unit $y$, with $\sigma = \tanh$ as the activation:

$$\ddot{y} = \sigma\big(W y + \tilde{W}\dot{y} + V u + b\big) - \gamma y - \epsilon \dot{y}.$$

Here $u(t)$ is the input, $W$, $\tilde W$ and $V$ are weight matrices, and $b$ is a bias. The parameter $\gamma$ sets the oscillation frequency and $\epsilon$ sets the damping. The paper associates the diagonal of $W$ with frequency and the diagonal of $\tilde W$ with damping, while off-diagonal entries couple the units. Writing the velocity $z = \dot y$ gives a first-order system. The paper discretises it with a time step $\Delta t$:

$$z_n = z_{n-1} + \Delta t\,\sigma\big(W y_{n-1} + \tilde{W} z_{n-1} + V u_n + b\big) - \Delta t\,\gamma\, y_{n-1} - \Delta t\,\epsilon\, z_{\bar n}, \qquad y_n = y_{n-1} + \Delta t\, z_n,$$

where $\bar n$ is either $n$ (implicit damping) or $n-1$ (explicit damping). The two versions differ only in how the damping term is handled.

The procedure runs as follows.

1. Choose a time step $0 < \Delta t < 1$ and initial states.
2. For each input $u_n$, update the velocity $z_n$, then the state $y_n$ using the new velocity. The paper's main description omits the affine readout.

## Results

The paper's experiments use benchmarks chosen to test long-range dependencies. The figures below are taken from its tables and text.

- **Adding problem.** The network adds two marked numbers in a sequence of length $T$. The paper reports that at $T = 2000$ only coRNN and the expRNN beat the baseline error, and that coRNN converges quickly at $T = 5000$, where the expRNN does not consistently beat the baseline.
- **Sequential MNIST and permuted sequential MNIST.** The paper reports test accuracies of 99.3% (sMNIST) and 96.6% (psMNIST) with 128 hidden units, and 99.4% and 97.3% with 256 units. It is ahead of the listed baselines on sMNIST and near the best on psMNIST.
- **Noise-padded CIFAR-10.** With 128 hidden units, coRNN reaches 59.0%, the highest figure among the models in the paper's table. The best gated anti-symmetric RNN listed reaches 54.7%.

The paper also reports competitive results on IMDB sentiment, human activity recognition and Lorenz 96 forecasting.

## Limitations

- **Comparable, not uniformly better.** The paper claims competitive performance rather than superiority on every task. On the adding problem, the expRNN also beats the baseline at $T = 2000$, and on psMNIST one baseline is slightly higher at 128 units.
- **Loose biological link.** The paper motivates the design from biology but sets aside much neural detail. The resemblance is mathematical, not anatomical.
- **Parameters matter.** The bounds hold under the paper's stated hypotheses. In practice $\gamma$, $\epsilon$ and $\Delta t$ affect behaviour, and the authors tuned them by random search.
- **Narrow task mix.** The benchmarks are mostly classification and forecasting tasks. The paper does not evaluate large-scale language modelling, so its results do not transfer directly to the settings where transformers dominate.

## Open questions

- **Is oscillation the active ingredient?** The anti-symmetric RNN is also a stable ODE-based design (Chang et al., 2019). Ablation studies would show whether the oscillatory form matters beyond stability.
- **Do learned frequencies mean anything?** Whether trained networks learn frequency structure that resembles the bands discussed on the [topic page](../index.md) is an open question.

## References

### Seminal papers

- Rusch, T. K. & Mishra, S. (2021). Coupled Oscillatory Recurrent Neural Network (coRNN): An accurate and (gradient) stable architecture for learning long time dependencies. *ICLR*. https://arxiv.org/abs/2010.00951 — Proposes coRNN and derives bounds on its hidden-state gradients.
- Hochreiter, S. & Schmidhuber, J. (1997). Long Short-Term Memory. *Neural Computation*. https://doi.org/10.1162/neco.1997.9.8.1735 — Introduces the LSTM, the gated baseline for long-range sequence models.

### Surveys and textbooks

- Strogatz, S. H. (2000). From Kuramoto to Crawford: exploring the onset of synchronization in populations of coupled oscillators. *Physica D*. https://doi.org/10.1016/S0167-2789(00)00094-4 — Reviews the Kuramoto model and the onset of synchrony.
- Buzsáki, G. & Draguhn, A. (2004). Neuronal oscillations in cortical networks. *Science*. https://doi.org/10.1126/science.1099745 — Review of cortical network oscillations, the biological background for oscillator models.

### Articles and documentation

- Chang, B., Chen, M., Haber, E. & Chi, E. H. (2019). AntisymmetricRNN: A Dynamical System View on Recurrent Neural Networks. arXiv. https://arxiv.org/abs/1902.09689 — Proposes an anti-symmetric recurrent network based on a stable ODE.
- Erichson, N. B., Azencot, O., Queiruga, A., Hodgkinson, L. & Mahoney, M. W. (2020). Lipschitz Recurrent Neural Networks. arXiv. https://arxiv.org/abs/2006.12070 — Proposes a recurrent unit with stability conditions from dynamical systems theory.
