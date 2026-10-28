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
- [Linear algebra for AI](linear-algebra/index.md): vectors, matrices, eigendecomposition, SVD and low-rank approximation, and where each appears in networks, attention, PCA and compression.

## 2. Calculus

**Where it's used:** training = minimising a loss, which needs gradients.

- Partial derivatives and the gradient \( \nabla_\theta L \)
- The chain rule — backpropagation is the chain rule applied systematically
- Jacobians and Hessians
- Taylor expansion (to understand optimisers and curvature)
- [Calculus and optimisation foundations](calculus/index.md): gradients, Hessians, convexity and Lagrange multipliers, with the methods they support.
- [Automatic differentiation](automatic-differentiation/index.md): how software computes exact derivatives of programs by applying the chain rule to each operation

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
- [Probability and statistics for AI](probability-statistics/index.md): random variables, Bayes' rule, MLE versus MAP, estimators and confidence, and the statistical view of a loss function, with the [maximum likelihood](probability-statistics/maximum-likelihood/index.md), [EM](probability-statistics/expectation-maximisation/index.md) and [bootstrap](probability-statistics/bootstrap/index.md) methods.

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

## References

Seminal works for this overview, drawn from the sub-pages linked above, where each is discussed in detail.

- Eckart, C. & Young, G. (1936). The Approximation of One Matrix by Another of Lower Rank. *Psychometrika*. https://doi.org/10.1007/BF02288367 — Shows how the best approximation of a matrix by one of lower rank is found, the basis of the truncated SVD.
- Pearson, K. (1901). LIII. On lines and planes of closest fit to systems of points in space. *Philosophical Magazine*. https://doi.org/10.1080/14786440109462720 — Finds the lines and planes that best fit a cloud of points, the geometric origin of principal component analysis.
- Kuhn, H. W. & Tucker, A. W. (1951). Nonlinear Programming. *Proceedings of the Second Berkeley Symposium on Mathematical Statistics and Probability*. https://doi.org/10.1525/9780520411586-036 — First-order conditions for a constrained optimum, the origin of KKT.
- Cortes, C. & Vapnik, V. (1995). Support-vector networks. *Machine Learning*. https://doi.org/10.1007/BF00994018 — Soft-margin support-vector machine, trained through its Lagrangian dual.
- Bayes, T. (1763). An essay towards solving a problem in the doctrine of chances. *Philosophical Transactions of the Royal Society of London*. https://doi.org/10.1098/rstl.1763.0053 — Posthumous essay on inverse probability, the origin of the rule that bears Bayes' name.
- Fisher, R. A. (1922). On the mathematical foundations of theoretical statistics. *Philosophical Transactions of the Royal Society A*. https://doi.org/10.1098/rsta.1922.0009 — Lays out the foundations of estimation, including maximum likelihood and its properties.
- Rumelhart, D. E., Hinton, G. E. & Williams, R. J. (1986). Learning representations by back-propagating errors. *Nature*. https://doi.org/10.1038/323533a0 — Popularises backpropagation for multilayer networks, the reverse-mode gradient method used to train deep networks.
- Pearlmutter, B. A. (1994). Fast Exact Multiplication by the Hessian. *Neural Computation*. https://doi.org/10.1162/neco.1994.6.1.147 — Shows how to multiply a Hessian by a vector exactly, without forming the matrix, using differentiation.
