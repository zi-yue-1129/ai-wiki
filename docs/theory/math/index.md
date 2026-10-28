---
related:
- theory/paradigms/probabilistic
- theory/machine-learning
---

# Mathematics for AI

Five areas of mathematics carry most of AI. This page explains where each is used and the minimum you need.

## 1. Linear algebra

> Detailed page: [Linear algebra for AI](linear-algebra/index.md), with [singular value decomposition](linear-algebra/svd.md) and [eigendecomposition](linear-algebra/eigendecomposition.md).


**Where it's used:** data are vectors and matrices; each neural-network layer is a matrix multiply plus a nonlinearity; embeddings are points in vector space; attention is built from dot products.

**Minimum to know:**

- Vectors, matrices, tensors; shape rules for matrix multiplication
- Dot product and cosine similarity \( \cos\theta = \frac{\mathbf{a}\cdot\mathbf{b}}{\|\mathbf{a}\|\|\mathbf{b}\|} \) — the basis of semantic search
- Linear maps, rank, bases
- Eigendecomposition and singular value decomposition (SVD): PCA, and the low-rank idea behind LoRA
- Norms (L1, L2): regularisation

## 2. Calculus

> Detailed page: [Calculus and optimisation foundations](calculus/index.md), with [Newton's method](calculus/newtons-method.md) and [Lagrange multipliers](calculus/lagrange-multipliers.md).


**Where it's used:** training = minimising a loss, which needs gradients.

- Partial derivatives and the gradient \( \nabla_\theta L \)
- The chain rule — backpropagation is the chain rule applied systematically
- Jacobians and Hessians
- Taylor expansion (to understand optimisers and curvature)

\[
\frac{\partial L}{\partial w} = \frac{\partial L}{\partial y}\cdot\frac{\partial y}{\partial z}\cdot\frac{\partial z}{\partial w}
\]

## 3. Probability and statistics

> Detailed page: [Probability and statistics for AI](probability-statistics/index.md), with [maximum likelihood](probability-statistics/maximum-likelihood.md) and [maximum a posteriori estimation](probability-statistics/maximum-a-posteriori.md).


**Where it's used:** models output probability distributions; a language model *is* \( p(x_t \mid x_{<t}) \); uncertainty estimation; confidence intervals and significance tests in evaluation.

- Conditional probability and Bayes' rule \( p(\theta\mid D) = \frac{p(D\mid\theta)p(\theta)}{p(D)} \)
- Common distributions: Bernoulli, categorical, Gaussian, Poisson
- Expectation, variance, covariance
- Maximum likelihood (MLE) and maximum a posteriori (MAP) estimation
- Sampling and Monte Carlo methods
- Hypothesis testing and the bootstrap (is model A really better than B?)

## 4. Information theory

**Where it's used:** cross-entropy loss; KL divergence (VAEs, the KL penalty in RLHF, distillation); perplexity; mutual information (representation learning, neural coding).

| Quantity | Definition | Intuition |
|---|---|---|
| Entropy | \( H(p) = -\sum p(x)\log p(x) \) | Average surprise |
| Cross-entropy | \( H(p,q) = -\sum p(x)\log q(x) \) | Cost of coding p with q; the classification loss |
| KL divergence | \( D_{KL}(p\|q) = \sum p\log\frac{p}{q} \) | Gap between distributions (asymmetric) |
| Mutual information | \( I(X;Y) = H(X) - H(X\mid Y) \) | How much knowing Y reduces uncertainty about X |
| Perplexity | \( \exp(H) \) | How many options a language model is effectively choosing between |

Information theory is also central in neuroscience: the **efficient coding hypothesis** (Barlow, 1961) proposes that sensory neurons maximise information transmission and reduce redundancy — closely related to sparse coding and self-supervised objectives.

## 5. Optimisation

**Where it's used:** all training is optimisation.

- Gradient descent \( \theta \leftarrow \theta - \eta\nabla_\theta L \)
- Stochastic gradient descent and mini-batches
- Momentum, Adam, AdamW (the current default)
- Learning-rate schedules: warmup, cosine decay
- Convex vs non-convex: deep-network losses are non-convex, yet SGD finds solutions that generalise
- Constrained optimisation and Lagrange multipliers (SVMs, KL-constrained RLHF)

## 6. Other useful tools

- **Graph theory**: knowledge graphs, GNNs, connectomes
- **Dynamical systems**: RNNs, neuron models, ODE/SDE views of diffusion models
- **Game theory**: GANs, multi-agent systems, mechanism design
- **Numerics**: floating-point formats (FP32/BF16/FP8), numerical stability (log-sum-exp)

## References

- Deisenroth, M. P., Faisal, A. A. & Ong, C. S. (2020). *Mathematics for Machine Learning*. Cambridge University Press. https://mml-book.github.io/ — Textbook linking linear algebra, analytic geometry, matrix decompositions, vector calculus, probability and optimisation to machine learning.
- Cover, T. M. & Thomas, J. A. (2006). *Elements of Information Theory* (2nd ed.). Wiley. https://doi.org/10.1002/047174882X — Standard reference for entropy, mutual information and channel-coding results used in the information-theory section.
- Boyd, S. & Vandenberghe, L. (2004). *Convex Optimization*. Cambridge University Press. https://doi.org/10.1017/CBO9780511804441 — Textbook on convex sets, duality and the algorithms behind the optimisation section.
- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning*. MIT Press. https://www.deeplearningbook.org/ — Chapters 2 to 4 cover the linear algebra, probability and information theory this page introduces.
- Hastie, T., Tibshirani, R. & Friedman, J. (2009). *The Elements of Statistical Learning* (2nd ed.). Springer. https://doi.org/10.1007/978-0-387-84858-7 — Statistical foundations for probability, regression and model selection in machine learning.

## Further learning

- [d2l appendix: Mathematics for Deep Learning](https://d2l.ai/chapter_appendix-mathematics-for-deep-learning/index.html) — free interactive appendix with code.
