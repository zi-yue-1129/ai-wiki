---
related:
- theory/paradigms/probabilistic
- theory/machine-learning
---

# Mathematics for AI

Five areas of mathematics carry most of AI. This page explains where each is used and the minimum you need.

## 1. Linear algebra

**Where it's used:** data are vectors and matrices; each neural-network layer is a matrix multiply plus a nonlinearity; embeddings are points in vector space; attention is built from dot products.

**Minimum to know:**

- Vectors, matrices, tensors; shape rules for matrix multiplication
- Dot product and cosine similarity \( \cos\theta = \frac{\mathbf{a}\cdot\mathbf{b}}{\|\mathbf{a}\|\|\mathbf{b}\|} \) — the basis of semantic search
- Linear maps, rank, bases
- Eigendecomposition and singular value decomposition (SVD): PCA, and the low-rank idea behind LoRA
- Norms (L1, L2): regularisation

## 2. Calculus

**Where it's used:** training = minimising a loss, which needs gradients.

- Partial derivatives and the gradient \( \nabla_\theta L \)
- The chain rule — backpropagation is the chain rule applied systematically
- Jacobians and Hessians
- Taylor expansion (to understand optimisers and curvature)

\[
\frac{\partial L}{\partial w} = \frac{\partial L}{\partial y}\cdot\frac{\partial y}{\partial z}\cdot\frac{\partial z}{\partial w}
\]

## 3. Probability and statistics

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

## Resources

- [Mathematics for Machine Learning](https://mml-book.github.io/) (free PDF)
- 3Blue1Brown, *Essence of Linear Algebra*, *Essence of Calculus*, *Neural Networks*
- [d2l appendix: Mathematics for Deep Learning](https://d2l.ai/chapter_appendix-mathematics-for-deep-learning/index.html)
- MIT 18.06 Linear Algebra (Gilbert Strang)
