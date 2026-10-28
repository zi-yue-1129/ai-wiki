---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/model-compression
  - theory/models/transformer
  - theory/paradigms/unsupervised
  - brain-mind/neuroai
tags:
  - representation learning
  - efficient inference
  - dimensionality reduction
aliases:
  - 線性代數
  - 奇異值分解
  - 特徵分解
  - 低秩近似
  - Linear algebra
  - SVD
---

# Linear Algebra for AI

Linear algebra studies vectors, matrices and the linear maps between them. It is the language in which AI systems store their data, their weights and their intermediate activations, and most of the arithmetic a model performs is matrix arithmetic.

## Overview

At its core, a neural network is a long chain of matrix multiplications interleaved with simple nonlinear functions. A fully connected layer maps an input vector $x$ to $h = \sigma(Wx + b)$, where $W$ is a matrix of learned weights and $\sigma$ is an elementwise nonlinearity. Images, sentences and sensor recordings are all arrays of numbers, and comparing two of them usually means a dot product or a distance. A small set of ideas recurs across the field. Dot products measure similarity, matrices represent linear maps, and matrix factorisations reveal the directions in which data or a model varies most.

Linear algebra is also where AI meets classical numerical computing. Accelerators are built to multiply large matrices quickly, so the cost of a model is largely the cost of its matrix products. This page expands the largest part of the [Mathematics for AI](../index.md) overview.

## Key concepts

- **Vector**: an ordered list of numbers, $x \in \mathbb{R}^d$. It can be a feature vector, a word embedding or the activity of a population of neurons at one instant.
- **Matrix and tensor**: a two-dimensional array of numbers, and its higher-dimensional generalisation. Shapes must agree for a product: $A \in \mathbb{R}^{m\times n}$ times $B \in \mathbb{R}^{n\times p}$ gives an $m\times p$ matrix.
- **Dot product and cosine similarity**: $a^\top b$ measures how well two vectors align. The cosine $\cos\theta = \frac{a^\top b}{\lVert a\rVert\,\lVert b\rVert}$ removes the effect of length.
- **Norm**: a function that measures the size of a vector. The Euclidean ($\ell_2$) norm $\lVert x\rVert_2 = \sqrt{\sum_i x_i^2}$ and the $\ell_1$ norm $\sum_i |x_i|$ are the common choices. Norms also define the penalties in [ridge and lasso regression](../../paradigms/supervised/linear-models/index.md).
- **Rank**: the number of linearly independent columns of a matrix, which is also the dimension of its output space. A rank-$r$ matrix can be written as a product of two thinner matrices whose inner dimension is $r$. Strang (1993) gives an accessible account of how rank organises the four fundamental subspaces of a matrix.
- **Eigenvector and eigenvalue**: a nonzero vector $v$ and a scalar $\lambda$ with $Av = \lambda v$. A symmetric matrix has real eigenvalues and an orthonormal set of eigenvectors.
- **Singular value decomposition (SVD)**: every real matrix factors as $A = U\Sigma V^\top$, where the columns of $U$ and $V$ are orthonormal and the diagonal of $\Sigma$ holds nonnegative singular values $\sigma_1 \ge \sigma_2 \ge \cdots$. Golub and Kahan (1965) gave a stable algorithm for computing it.
- **Projection**: a linear map $P$ with $P^2 = P$ that sends vectors onto a subspace. If $Q$ has orthonormal columns, $QQ^\top$ projects orthogonally onto their span.

## How it works

**Layers as matrix products.** If a layer takes $n$ inputs and has $m$ units, its weight matrix has shape $m \times n$. When a batch of inputs is stacked as the rows of a matrix, the whole layer is one matrix product. This is why training consists largely of large matrix multiplications.

**Similarity as dot products.** Embedding models place items in a vector space so that related items have a large cosine similarity. Word vectors learned from text have this property, which was shown at scale by Mikolov and colleagues (2013). The [Transformer](../../models/transformer/index.md) builds its attention from the same operation. Each query is compared with every key by a dot product, the scores are scaled and normalised by a softmax, and the result weights a sum of values (Vaswani et al., 2017).

**Eigendecomposition of the covariance matrix.** For centred data $X \in \mathbb{R}^{n\times d}$, the covariance matrix is $C = \frac{1}{n}X^\top X$. It is symmetric and positive semidefinite, so it has an orthonormal eigenbasis. The eigenvector with the largest eigenvalue points along the direction of greatest variance. [Principal component analysis](pca/index.md) is built on this fact.

**Truncated SVD and the best low-rank approximation.** Keeping only the $k$ largest singular values gives

$$
A_k = \sum_{i=1}^{k} \sigma_i\, u_i v_i^\top .
$$

The Eckart–Young theorem says that $A_k$ is the closest matrix of rank at most $k$ to $A$, measured in the Frobenius norm. Its squared error is $\lVert A - A_k\rVert_F^2 = \sum_{i>k}\sigma_i^2$, the sum of the discarded squared singular values (Eckart & Young, 1936). This is the basis of the [truncated SVD](truncated-svd/index.md) method.

```mermaid
flowchart LR
  W["Weight matrix W (m × n)"] --> S["SVD: W = U Σ Vᵀ"]
  S --> T["Keep k largest σᵢ"]
  T --> F["Factors U_k, Σ_k, V_kᵀ"]
  F --> C["About k(m + n) numbers instead of mn"]
```

## Key methods

Three landmark methods cover most of the subject in practice. Each has its own page.

| Method | What it computes | Where it appears |
|---|---|---|
| [Truncated SVD (Eckart–Young)](truncated-svd/index.md) | The best rank-$k$ approximation of a matrix | Compressing weights, low-rank factorisation, the idea behind LoRA |
| [Principal component analysis](pca/index.md) | Orthogonal directions of greatest variance, from the eigenvectors of the covariance matrix or the SVD of the data | Dimensionality reduction, visualisation, eigenfaces, neural population analysis |
| [Randomized SVD](randomized-svd/index.md) | An approximate truncated SVD, computed by projecting onto a random subspace | Very large matrices, where an exact SVD is too costly |

## Connections

- **Neural networks.** Each layer is a matrix product, and backpropagation through it multiplies the gradient by the transposed weight matrix. The chain rule that drives [automatic differentiation](../automatic-differentiation/index.md) therefore runs on linear algebra. The [deep learning](../../deep-learning/index.md) page shows how these layers are stacked.
- **Attention.** Attention scores are dot products between queries and keys, so the geometry of the query and key spaces determines what a model attends to. See the [attention is all you need](../../models/transformer/attention-is-all-you-need/index.md) page for the architecture.
- **Dimensionality reduction and representations.** PCA is the linear member of a family that includes nonlinear methods, and [autoencoders](../../paradigms/unsupervised/autoencoders-and-representations/index.md) learn a nonlinear generalisation of the same idea. The [dimensionality reduction](../../paradigms/unsupervised/dimensionality-reduction/index.md) page compares them.
- **Compression.** A weight matrix that is nearly low-rank can be replaced by two thinner factors, which is one of the [model compression](../../model-compression/index.md) strategies. [LoRA and QLoRA](../../../engineering/training/peft-lora.md) apply a low-rank update to a frozen model during fine-tuning, and [vector databases](../../../engineering/vector-databases/index.md) use inner products and approximate nearest-neighbour search to retrieve embeddings at scale.
- **Brain and mind.** Recorded population activity is a matrix, with neurons as one axis and time or conditions as the other. Studies of motor cortex describe such activity with a few principal components (Churchland et al., 2012; Gallego et al., 2017). Representational similarity analysis compares brain and model representations through matrices of pairwise dissimilarities (Kriegeskorte, 2008). See [sparse coding](../../../brain-mind/computational-neuroscience/sparse-coding/index.md) and [NeuroAI](../../../brain-mind/neuroai/index.md).

## Applications

- **Semantic search and retrieval.** Documents and queries are embedded as vectors and ranked by cosine similarity or inner product. Libraries such as FAISS perform this at large scale.
- **Model compression and fine-tuning.** Low-rank factorisation shrinks a layer's parameters, and low-rank updates make fine-tuning cheap. Hu and colleagues (2021) report that LoRA cuts the trainable parameters of GPT-3 175B by a factor of 10,000 relative to full fine-tuning with Adam, per their abstract.
- **Visualisation and preprocessing.** Projecting data onto two or three principal components is a common first look at a dataset. Sirovich and Kirby (1987) and Turk and Pentland (1991) used the same projection to represent faces.

## Open questions

- **Are weights and activations low-rank for the right reasons?** Trained networks often have singular values that decay quickly, but how much of that structure is needed for a given accuracy depends on the layer and the task.
- **Why does low-rank adaptation work?** LoRA restricts weight updates to a low-rank subspace and still matches full fine-tuning on several benchmarks (Hu et al., 2021). A full explanation of which directions must change is still missing.
- **Linear coordinates versus nonlinear features.** PCA and SVD assume that useful structure is linear. Nonlinear representations, such as those found by deep autoencoders (Hinton & Salakhutdinov, 2006), can be more compact, but they are harder to analyse.
- **Does neural population structure reflect the brain or the method?** The answer depends on preprocessing and on the dimensionality-reduction method used.

## References

### Seminal papers

- Eckart, C. & Young, G. (1936). The Approximation of One Matrix by Another of Lower Rank. *Psychometrika*. https://doi.org/10.1007/BF02288367 — Shows how the best approximation of a matrix by one of lower rank is found, the basis of the truncated SVD.
- Pearson, K. (1901). LIII. On lines and planes of closest fit to systems of points in space. *Philosophical Magazine*. https://doi.org/10.1080/14786440109462720 — Finds the lines and planes that best fit a cloud of points, the geometric origin of principal component analysis.
- Hotelling, H. (1933). Analysis of a complex of statistical variables into principal components. *Journal of Educational Psychology*. https://doi.org/10.1037/h0071325 — Introduces principal components as successive uncorrelated combinations of variables with the largest variance.
- Golub, G. & Kahan, W. (1965). Calculating the Singular Values and Pseudo-Inverse of a Matrix. *Journal of the Society for Industrial and Applied Mathematics Series B Numerical Analysis*. https://doi.org/10.1137/0702016 — Gives a numerically stable algorithm that reduces a matrix to bidiagonal form and then diagonalises it.
- Vaswani, A. et al. (2017). Attention Is All You Need. NeurIPS. https://arxiv.org/abs/1706.03762 — Introduces the Transformer, whose attention layers are built from dot products between queries and keys.
- Mikolov, T. et al. (2013). Efficient Estimation of Word Representations in Vector Space. https://arxiv.org/abs/1301.3781 — Learns continuous word vectors from large corpora, where similarity in the vector space tracks word similarity.
- Hinton, G. E. & Salakhutdinov, R. R. (2006). Reducing the Dimensionality of Data with Neural Networks. *Science*. https://doi.org/10.1126/science.1127647 — Trains deep autoencoders whose low-dimensional codes work better than principal component analysis, according to the abstract.
- Hu, E. J. et al. (2021). LoRA: Low-Rank Adaptation of Large Language Models. https://arxiv.org/abs/2106.09685 — Freezes pretrained weights and trains low-rank update matrices, which cuts the cost of fine-tuning.
- Turk, M. & Pentland, A. (1991). Eigenfaces for Recognition. *Journal of Cognitive Neuroscience*. https://doi.org/10.1162/jocn.1991.3.1.71 — Recognises faces by projecting images onto principal components, which the authors call eigenfaces.
- Churchland, M. M. et al. (2012). Neural population dynamics during reaching. *Nature*. https://doi.org/10.1038/nature11129 — Analyses population recordings from motor cortex during reaching using low-dimensional projections of the activity.
- Gallego, J. A. et al. (2017). Neural Manifolds for the Control of Movement. *Neuron*. https://doi.org/10.1016/j.neuron.2017.05.025 — Argues that movement-related population activity can be described on low-dimensional neural manifolds.
- Kriegeskorte, N. (2008). Representational similarity analysis – connecting the branches of systems neuroscience. *Frontiers in Systems Neuroscience*. https://doi.org/10.3389/neuro.06.004.2008 — Compares brain and model representations through matrices of pairwise dissimilarities.

### Surveys and textbooks

- Kolda, T. G. & Bader, B. W. (2009). Tensor Decompositions and Applications. *SIAM Review*. https://doi.org/10.1137/07070111X — Surveys higher-order tensor decompositions, presented as extensions of the matrix SVD and of PCA.
- Strang, G. (1993). The Fundamental Theorem of Linear Algebra. *The American Mathematical Monthly*. https://doi.org/10.2307/2324660 — Expository article on the four fundamental subspaces of a matrix and how they relate.
- Martinsson, P.-G. & Tropp, J. A. (2020). Randomized numerical linear algebra: Foundations and algorithms. *Acta Numerica*. https://doi.org/10.1017/S0962492920000021 — Survey of probabilistic algorithms for low-rank approximation, subspace iteration and related tasks.
