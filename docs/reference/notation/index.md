---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/math
tags:
  - notation
  - mathematics
  - reference
aliases:
  - 符號
  - 數學符號
  - Notation
---

# Notation and symbols

This page lists the symbols used across the wiki, so that a reader moving between pages can keep the same meanings in view. Where a page uses a different convention for a good reason, it says so. The conventions follow the standard machine learning texts, and they are chosen to be readable rather than to match any single paper.

## Scalars, vectors and matrices

- Lowercase italic letters, such as $x$ or $\alpha$, denote scalars.
- Lowercase bold letters, such as $\mathbf{x}$, denote vectors. A vector is a column by default.
- Uppercase bold letters, such as $\mathbf{W}$, denote matrices. $\mathbf{W} \in \mathbb{R}^{m \times n}$ has $m$ rows and $n$ columns.
- $\mathbf{x}^\top$ is the transpose, $\|\mathbf{x}\|$ is the Euclidean norm, and $\odot$ is the element-wise product.

## Data and models

- $\mathcal{D} = \{(\mathbf{x}_i, y_i)\}_{i=1}^{N}$ is a labelled dataset of $N$ examples.
- $\theta$ denotes the parameters of a model $f_\theta$. For a neural network, $\theta$ collects all weights and biases.
- $\hat{y} = f_\theta(\mathbf{x})$ is the prediction, and $y$ is the target.

## Losses, gradients and optimisation

- $\mathcal{L}(\theta)$ is a loss, usually an empirical average over the dataset: $\mathcal{L}(\theta) = \frac{1}{N}\sum_{i=1}^{N} \ell(f_\theta(\mathbf{x}_i), y_i)$.
- $\nabla_\theta \mathcal{L}$ is the gradient with respect to $\theta$. The gradient is the output of automatic differentiation, covered in [Automatic differentiation](../../theory/math/automatic-differentiation/index.md).
- $\eta$ is a learning rate, and $t$ indexes steps.

## Probability

- $p(x)$ is a density or mass function, and $p(x \mid y)$ is a conditional one.
- $\mathbb{E}_{x \sim p}[f(x)]$ is the expectation of $f$ under $p$.
- $\mathrm{KL}(p \,\|\, q)$ is the Kullback-Leibler divergence.

## Reinforcement learning

- $s$ is a state, $a$ an action, $r$ a reward, and $\gamma \in [0, 1)$ a discount factor.
- $\pi_\theta(a \mid s)$ is a policy, $V^\pi(s)$ a state-value function, and $Q^\pi(s, a)$ an action-value function.
- The agent's return from time $t$ is $G_t = \sum_{k \ge 0} \gamma^k r_{t+k}$.

## Conflicts and exceptions

- Some papers use $x$ for the input and $z$ for a latent code, others the reverse. Pages state the convention they use.
- In Transformers, $d$ often denotes the model width, and $n$ or $T$ the sequence length.

## References

### Seminal papers

- Rumelhart, Hinton and Williams, *Learning representations by back-propagating errors*, Nature (1986). https://doi.org/10.1038/323533a0 — The paper that popularised backpropagation for training multi-layer networks.
- Silver, Huang, Maddison, Guez, Sifre, van den Driessche and colleagues, *Mastering the game of Go with deep neural networks and tree search*, Nature (2016). https://doi.org/10.1038/nature16961 — A reference point for the policy and value notation used in reinforcement learning pages.

### Surveys and textbooks

- Goodfellow, Bengio and Courville, *Deep Learning*, MIT Press (2016). https://www.deeplearningbook.org/ — A textbook whose notation section sets out the conventions for scalars, vectors, matrices and probability.
- Bishop, *Pattern Recognition and Machine Learning*, Springer (2006). https://doi.org/10.1007/978-0-387-45528-0 — A textbook with consistent notation for probabilistic models and Bayesian inference.

### Articles and documentation

- Griewank and Walther, *Evaluating Derivatives: Principles and Techniques of Algorithmic Differentiation*, SIAM (2008). https://doi.org/10.1137/1.9780898717761 — Covers derivative notation and the mechanics behind gradient computation.
