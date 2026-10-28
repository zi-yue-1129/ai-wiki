---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/math
  - theory/deep-learning
  - theory/paradigms/supervised/loss-functions-and-optimization
  - brain-mind/neuroai
tags:
  - optimization
  - gradient descent
aliases:
  - 最佳化
  - 優化
  - Optimisation
  - Optimization
  - 梯度下降
  - Gradient descent
---

# Optimisation

Training a model means choosing its parameters so that a loss function is small. Optimisation is the set of algorithms that do this search. Almost every method in this wiki, from linear regression to large language models, ends in an optimiser.

## Overview

Write the model as \(f_\theta\) with parameters \(\theta\), and the training loss as an average over data, \(L(\theta)=\frac{1}{N}\sum_i \ell(f_\theta(x_i), y_i)\). Learning is the search for \(\theta^\* = \arg\min_\theta L(\theta)\). Because the search is over millions or billions of numbers, we rely on the gradient \(\nabla_\theta L\), which points uphill, and move the other way. How well this works depends on the shape of the loss surface: whether it is convex, how curved it is, and how noisy our estimate of the gradient is.

The mathematics of this search sits in [Mathematics](../math/index.md), and the training pipeline that uses it is in [Deep Learning](../deep-learning/index.md). The supervised-learning view of losses and regularisation is in [Loss Functions & Optimisation](../paradigms/supervised/loss-functions-and-optimization/index.md). This page covers the algorithms themselves.

## Key concepts

- **Gradient descent**: repeatedly update \(\theta \leftarrow \theta - \eta \nabla L(\theta)\), where \(\eta\) is the learning rate.
- **Stochastic gradient descent (SGD)**: estimate the gradient from a random mini-batch rather than the whole dataset. Each step is cheap and noisy.
- **Learning rate**: the step size \(\eta\). Too large diverges; too small crawls. Schedules change it over training.
- **Momentum**: average past gradients so that the update keeps moving along consistent directions and damps oscillation.
- **Convexity**: a convex function has no spurious local minima, so any local minimum is global. Neural-network losses are non-convex.
- **Smoothness (Lipschitz gradient)**: a bound \(L\) on how fast the gradient can change. It fixes the largest safe step size, \(\eta \le 1/L\).
- **Conditioning**: when curvature differs widely across directions, plain gradient descent zig-zags. Per-parameter scaling helps.
- **Loss landscape**: the high-dimensional surface of \(L(\theta)\). It contains saddle points, flat regions and wide or narrow minima.

## How it works

### Gradient descent and its noise

For a convex, \(L\)-smooth loss, gradient descent with \(\eta = 1/L\) reduces the loss at rate \(O(1/T)\) after \(T\) steps. For strongly convex losses the rate is linear (geometric). Stochastic gradients give an unbiased estimate \(g_t\) of \(\nabla L\), so the expected update matches the full gradient but adds variance. With a decreasing step size the noise averages out, and the classic Robbins–Monro conditions \(\sum \eta_t = \infty\) and \(\sum \eta_t^2 < \infty\) guarantee convergence.

The noise is not only a nuisance. It helps the optimiser escape sharp saddle points and tends to prefer flatter minima, which many studies link to better generalisation, although this link is debated.

### Momentum

Heavy-ball momentum (Polyak, 1964) keeps a velocity \(v_t = \beta v_{t-1} + g_t\) and updates \(\theta \leftarrow \theta - \eta v_t\). Nesterov's variant evaluates the gradient at a look-ahead point instead of the current one. Momentum is widely used when training convolutional networks with SGD.

### Adaptive methods

Adaptive methods keep a per-parameter scale. Parameters that receive large gradients take smaller steps, and rarely updated parameters take larger ones. Adam keeps running averages of the gradient and its square:

\[
\begin{aligned}
m_t &= \beta_1 m_{t-1} + (1-\beta_1)\, g_t \\
v_t &= \beta_2 v_{t-1} + (1-\beta_2)\, g_t^2 \\
\theta_t &= \theta_{t-1} - \eta\, \frac{\hat m_t}{\sqrt{\hat v_t}+\epsilon}
\end{aligned}
\]

where \(\hat m_t\) and \(\hat v_t\) are bias-corrected versions of \(m_t\) and \(v_t\). Adam and its relatives are common in training Transformers, and they often need less learning-rate tuning than SGD. The key methods below explain why its weight-decay implementation matters.

### Second-order and quasi-Newton methods

Newton's method uses the Hessian \(H\) to take step \(-H^{-1}\nabla L\), which corrects for curvature. Exact Hessians have \(d^2\) entries for \(d\) parameters, so practical methods approximate them. Shampoo and K-FAC are examples used in large-scale training. They are less common than Adam but appear in research on very large models.

## Key methods

### Adam (Kingma & Ba, 2014/2015)

- **Problem:** stochastic gradients are noisy and sparse, and first-order methods need careful, problem-specific learning rates.
- **Core idea:** adapt a separate step size for each parameter using running estimates of the first and second moments of its gradient, with bias correction for early steps.
- **Equation or algorithm:** the update above, with \(\beta_1 \approx 0.9\), \(\beta_2 \approx 0.999\) and \(\epsilon\) a small constant. The paper's default values are those in the algorithm box.
- **Results:** the abstract describes the method as working well in practice and comparing favourably with other stochastic optimisers. It gives no benchmark numbers in the abstract; the experimental results are in the paper's body.
- **Limitations:** the paper's convergence analysis is in the online convex optimisation framework, not for deep networks. Adam can generalise worse than SGD with momentum on some image tasks, and its per-parameter scaling interacts badly with L2 regularisation (see AdamW).

### AdamW (Loshchilov & Hutter, 2017/2019)

- **Problem:** for adaptive methods, adding an L2 penalty to the loss is not the same as weight decay. The penalty is rescaled by the adaptive denominator, so regularisation weakens for parameters with large gradients.
- **Core idea:** apply weight decay directly to the parameters, outside the adaptive step, so the decay factor is decoupled from the gradient scaling.
- **Equation or algorithm:** \(\theta_t = \theta_{t-1} - \eta\big(\frac{\hat m_t}{\sqrt{\hat v_t}+\epsilon} + \lambda\,\theta_{t-1}\big)\).
- **Results:** the abstract reports that decoupled decay substantially improves Adam's generalisation and lets it compete with SGD with momentum on image classification. It gives no specific numbers in the abstract.
- **Limitations:** the decay coefficient and learning rate still interact, and the benefit has been reported mainly for image classification. AdamW is now the default for many Transformer models, but its advantage on other tasks depends on tuning.

## Connections

- **Mathematics:** convexity, Taylor expansion and the Hessian are the tools that explain why a method works. See [Mathematics](../math/index.md).
- **Deep learning:** backpropagation computes \(\nabla L\), and the optimiser decides how to use it. See [Deep Learning](../deep-learning/index.md).
- **Regularisation:** weight decay, early stopping and noise injection act on the same objective and can be seen as implicit changes to the optimisation. See [Loss Functions & Optimisation](../paradigms/supervised/loss-functions-and-optimization/index.md).
- **Brain and mind:** exact backpropagation needs symmetric feedback weights that biological circuits do not obviously have, so the search for local, plausible learning rules is a major theme in [NeuroAI](../../brain-mind/neuroai/index.md).

## Applications

- Training image classifiers with SGD and momentum, and transformers with AdamW.
- Hyperparameter search and learning-rate schedules in large-scale language-model training.
- Convex optimisation in SVMs, logistic regression and control, where the convergence rates above give guarantees.

## Open questions

- Why do stochastic and adaptive methods find solutions that generalise, when the loss surface has many minima?
- How do learning-rate warm-up and schedules interact with very large batch sizes?
- Can second-order information be used at the scale of billion-parameter models at acceptable cost?
- What are the optimisation analogues in biological learning, and which rules can be implemented locally?

## References

### Seminal papers

- Robbins, H. & Monro, S. (1951). A stochastic approximation method. *Annals of Mathematical Statistics*. doi:10.1214/aoms/1177729586 — Introduces stochastic approximation with decreasing step sizes, the foundation of stochastic gradient descent.
- Polyak, B. T. (1964). Some methods of speeding up the convergence of iteration methods. *USSR Computational Mathematics and Mathematical Physics*. doi:10.1016/0041-5553(64)90137-5 — Introduces heavy-ball momentum and analyses its acceleration on quadratic problems.
- Kingma, D. P. & Ba, J. (2015). Adam: A Method for Stochastic Optimization. ICLR. https://arxiv.org/abs/1412.6980 — Proposes Adam, an adaptive method that uses bias-corrected moment estimates of the gradient.
- Loshchilov, I. & Hutter, F. (2019). Decoupled Weight Decay Regularization. ICLR. https://arxiv.org/abs/1711.05101 — Shows that L2 regularisation and weight decay differ for Adam and proposes AdamW.

### Surveys and textbooks

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). Optimization Methods for Large-Scale Machine Learning. *SIAM Review*. https://arxiv.org/abs/1606.04838 — Survey of stochastic gradient methods and their trade-offs for large datasets, with convergence analysis.
- Boyd, S. & Vandenberghe, L. (2004). *Convex Optimization*. Cambridge University Press. https://web.stanford.edu/~boyd/cvxbook/ — Standard textbook on convex analysis and algorithms, with a free PDF from the authors.

### Lectures and videos

- Li, H., Xu, Z., Taylor, G., Studer, C. & Goldstein, T. (2018). Visualizing the Loss Landscape of Neural Nets. NeurIPS. https://arxiv.org/abs/1712.09913 — Visualisation method for loss surfaces that shows how network design changes landscape geometry.

### Articles and documentation

- Stanford CS231n, *Optimization* lecture notes. https://cs231n.github.io/optimization-1/ — Clear, illustrated notes on gradient descent, learning rates and momentum for students new to the topic.
