---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/model-compression
  - engineering/training/peft-lora.md
tags:
  - efficient inference
  - representation learning
aliases:
  - 截斷奇異值分解
  - 低秩近似
  - Eckart–Young theorem
  - Truncated SVD
  - Low-rank approximation
---

# Truncated SVD and the Eckart–Young Theorem

The truncated singular value decomposition keeps the $k$ largest singular values of a matrix and discards the rest. The result is the closest matrix of rank $k$ to the original, which makes it the standard tool for low-rank compression. It is one of the three key methods of [linear algebra for AI](../index.md).

## Overview

Many AI matrices are close to low rank: a weight matrix may act mainly along a few directions, and a data matrix may vary mainly along a few axes. Replacing such a matrix by a simpler one that keeps most of its action saves storage and computation.

The question is what "closest" means. Eckart and Young (1936) answered it for the Frobenius norm, the square root of the sum of squared entries: keep the leading singular values and their vectors, and drop the rest.

## Key concepts

- **Singular value and singular vectors**: every real matrix $A \in \mathbb{R}^{m\times n}$ factors as $A = U\Sigma V^\top$. The columns $u_i$ and $v_i$ are orthonormal, and $\sigma_i$ are the singular values in decreasing order.
- **Rank-$k$ truncation**: the matrix $A_k$ built from the first $k$ terms of the SVD.
- **Frobenius norm**: $\lVert M\rVert_F = \sqrt{\sum_{ij} M_{ij}^2}$.

## How it works

The Eckart–Young theorem states that, among all matrices $B$ of rank at most $k$,

$$
\lVert A - A_k \rVert_F = \min_{\operatorname{rank}(B)\le k} \lVert A - B \rVert_F,
\qquad
\lVert A - A_k \rVert_F^2 = \sum_{i>k} \sigma_i^2 .
$$

The error is therefore the energy in the discarded singular values. As a small example, take $A = \begin{pmatrix} 3 & 0 \\ 0 & 1 \end{pmatrix}$. Its singular values are 3 and 1, and the best rank-1 approximation keeps the entry 3. The error is 1 in both the Frobenius and the spectral norm.

The method runs in four steps:

1. Compute the SVD $A = U\Sigma V^\top$. The classical algorithm (Golub & Kahan, 1965) is numerically stable.
2. Choose $k$ from a target error or a target size.
3. Keep the first $k$ columns of $U$ and $V$, and the first $k$ singular values.
4. Store the factors $U_k$, $\Sigma_k$ and $V_k$ instead of $A$. Applying the approximation to a vector $x$ costs $U_k(\Sigma_k(V_k^\top x))$, which needs about $k(m+n)$ numbers of storage instead of $mn$.

For a network, the same steps apply to a weight matrix $W$, which the two thinner factors replace in [model compression](../../../model-compression/index.md).

## Results

The theorem is exact and has no benchmark. Its practical value depends on how well reconstruction error predicts the loss of a trained network, and three kinds of evidence bear on this.

- **Redundancy in weights.** Denil and colleagues (2013) show that trained networks have large parameter redundancy. In the best case, more than 95% of the weights could be predicted from a small learned subset without a drop in accuracy, according to their abstract. It is not a truncated SVD, but it supports the premise that weights can be compressed.
- **Learned low-rank updates.** LoRA (Hu et al., 2021) is a related but different method. It trains low-rank updates on frozen weights rather than truncating them. On GPT-3 175B, the abstract reports 10,000 times fewer trainable parameters and 3 times less GPU memory than full fine-tuning with Adam, with quality on par with or better than fine-tuning on RoBERTa, DeBERTa, GPT-2 and GPT-3.

## Limitations

- **Reconstruction is not accuracy.** The theorem minimises matrix error, not model loss. A small reconstruction error can still hurt accuracy if it falls on directions the network relies on.
- **Slow decay.** Many trained weight matrices have slowly decaying singular values, so a small error needs a large $k$ and the saving disappears.
- **Cost of the full SVD.** The exact SVD of a dense $m\times n$ matrix costs on the order of $mn\min(m,n)$ operations, which motivates the [randomized SVD](../randomized-svd/index.md).
- **Linear only.** Nonlinear activations between layers mean that an error in one layer propagates through the rest of the network.
- **Retraining is often needed.** Without fine-tuning after truncation, accuracy can drop sharply.

## Open questions

- How should the rank be chosen for each layer, given their differing spectra?
- Does a small reconstruction error in weights translate into a small change in what the network computes?
- How does the rank that LoRA needs compare with the rank that truncation needs for the same accuracy?

## References

### Seminal papers

- Eckart, C. & Young, G. (1936). The Approximation of One Matrix by Another of Lower Rank. *Psychometrika*. https://doi.org/10.1007/BF02288367 — The original result that the best approximation of a matrix by one of lower rank is given by its truncated SVD.
- Golub, G. & Kahan, W. (1965). Calculating the Singular Values and Pseudo-Inverse of a Matrix. *Journal of the Society for Industrial and Applied Mathematics Series B Numerical Analysis*. https://doi.org/10.1137/0702016 — Gives a stable algorithm for computing the SVD, by bidiagonalisation followed by diagonalisation.
- Denil, M. et al. (2013). Predicting Parameters in Deep Learning. https://arxiv.org/abs/1306.0543 — Shows that many weights of several deep networks are redundant and can be predicted from a small learned subset.
- Hu, E. J. et al. (2021). LoRA: Low-Rank Adaptation of Large Language Models. https://arxiv.org/abs/2106.09685 — Trains low-rank update matrices on top of frozen pretrained weights for efficient fine-tuning.

### Surveys and textbooks

- Kolda, T. G. & Bader, B. W. (2009). Tensor Decompositions and Applications. *SIAM Review*. https://doi.org/10.1137/07070111X — Surveys higher-order tensor decompositions and their relation to the matrix SVD.
- Halko, N., Martinsson, P. G. & Tropp, J. A. (2011). Finding Structure with Randomness: Probabilistic Algorithms for Constructing Approximate Matrix Decompositions. *SIAM Review*. https://doi.org/10.1137/090771806 — Surveys randomized algorithms that approximate the truncated SVD faster than the exact method on large matrices.
