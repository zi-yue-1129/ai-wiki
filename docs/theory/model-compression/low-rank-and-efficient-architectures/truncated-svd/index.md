---
status: draft
last_reviewed: 2026-10-28
tags:
- model compression
- low-rank factorisation
- singular value decomposition
aliases:
  - Truncated SVD
  - Low-rank matrix approximation
  - 截斷奇異值分解
---

# Truncated SVD

Truncated SVD compresses a trained weight matrix by keeping only its largest singular values. It replaces a large matrix with the product of two thinner ones, which needs fewer parameters and fewer multiply-adds when the kept rank is small. Denton et al. applied the idea to the filters of convolutional layers and reported speed-ups of about 2 times on CPU and GPU with accuracy kept within 1%. It is a [low-rank factorisation](../index.md) method that works after training.

## Problem

A dense layer with an \(m \times n\) weight matrix costs \(mn\) parameters, and large layers dominate the size and the compute of many models. If the matrix is close to low rank, most of that cost is spent on directions that carry little signal.

## Core idea

Decompose the matrix by singular value decomposition, \(W = U \Sigma V^\top\), and keep only the \(r\) largest singular values. The truncated product \(U_r \Sigma_r V_r^\top\) is the best rank-\(r\) approximation of \(W\) in the Frobenius norm. Writing it as two layers, \(W \approx AB\) with \(A = U_r \Sigma_r\) and \(B = V_r^\top\), turns one layer into two thinner ones.

## Equation or algorithm

The parameter count falls from \(mn\) to \(r(m+n)\), so the saving is positive whenever \(r < \frac{mn}{m+n}\). The approximation error is given by the discarded singular values, \(\lVert W - W_r \rVert_F^2 = \sum_{i > r} \sigma_i^2\), which provides a direct way to choose \(r\) for a given error budget. In practice the rank is chosen layer by layer, and the factorised model is usually fine-tuned afterwards to recover accuracy.

### Rank budget and discarded energy

Take the illustrative matrix $W=\operatorname{diag}(6,3,1,0.5)$ and $x=(1,1,1,1)^\top$. Here $U=V=I$, so $W_rx$ retains the first $r$ components directly. The animation builds the two factors and their intermediate activation, reveals output components, and compares the storage of ordinary dense factors $A\in\mathbb R^{4\times r}$ and $B\in\mathbb R^{r\times4}$.

| Rank $r$ | $W_rx$ | Factor entries / original entries | $\|W-W_r\|_F^2$ |
|---:|---|---:|---:|
| 1 | $(6,0,0,0)$ | 8 / 16 | 10.25 |
| 2 | $(6,3,0,0)$ | 16 / 16 | 1.25 |
| 3 | $(6,3,1,0)$ | 24 / 16 | 0.25 |

Increasing rank reduces matrix approximation error but need not compress storage. The count assumes dense storage and excludes bias, alignment and intermediate buffers; a diagonal matrix itself admits other structured storage formats. For general inputs, output error depends on projections onto right singular vectors and is not the Frobenius error. All values are constructed examples, not model measurements or latency results.

The upper panel now follows the actual two-factor computation: $h=Bx$ and $y_r=Ah$. The active rows of $B$ are the first $r$ rows of the identity; the active columns of $A$ contain the corresponding scaled identity columns. Increasing $r$ by one adds a row of four entries to $B$, a column of four entries to $A$, and one intermediate activation. Dashed slots are absent from the current factors, while solid zero-valued cells are counted under the dense-storage assumption. The vertical marker on each storage bar marks the original 16 entries. The static preview shows the rank-three factors with all three budget comparisons. No full weight matrix needs to be reconstructed to evaluate $Ah$.

For a general SVD, the output error on a particular input is

$$
\| (W-W_r)x\|_2^2=\sum_{i>r}\sigma_i^2(v_i^\top x)^2.
$$

For example, at rank one, the squared error on $x=(1,0,0,0)^\top$ is zero, while on $x=(0,1,0,0)^\top$ it is 9; the matrix approximation error remains 10.25. This illustrates why rank selection using weight energy alone is not equivalent to minimizing errors on an input distribution.

<div style="max-width:100%;overflow-x:auto" role="group" tabindex="0" aria-label="Successive rows of B and columns of A compute Bx then ABx; factor storage and discarded squared error are compared for ranks one through three.">
<div style="width:640px">
<img data-source-asset-urls src="../../../../assets/concept-animations/svd-factor-rank-budget-still.svg" data-motion-src="../../../../assets/concept-animations/svd-factor-rank-budget-motion.svg" data-still-src="../../../../assets/concept-animations/svd-factor-rank-budget-still.svg" alt="Successive rows of B and columns of A compute Bx then ABx; factor storage and discarded squared error are compared for ranks one through three." width="640" height="360">
</div>
</div>

*Original 12-second teaching animation (CC BY-SA 4.0).* Use Play/Pause on MkDocs; the focusable container scrolls horizontally on narrow screens. GitHub displays the [static preview](../../../../assets/concept-animations/svd-factor-rank-budget-still.svg); the [full animation](../../../../assets/concept-animations/svd-factor-rank-budget-motion.svg) is also linked.

### Input-weighted rank-one approximation

For an input second-moment matrix $M_x=\mathbb E[xx^\top]$, the expected squared output error of any approximation $\widetilde W$ is

$$
\mathbb E\|(W-\widetilde W)x\|_2^2=\operatorname{tr}\big((W-\widetilde W)M_x(W-\widetilde W)^\top\big).
$$

Take the same diagonal matrix and suppose the input is the first basis vector with probability $p$ and the second with probability $1-p$. The ordinary rank-one SVD keeps the first mode, with expected output error $9(1-p)$. A different rank-one approximation retaining only the second mode, $\widetilde W=\operatorname{diag}(0,3,0,0)$, has expected error $36p$. It has larger squared Frobenius error (37.25 instead of 10.25), yet gives smaller expected output error when $p<0.2$. Both use the same dense-factor entry count. At $p=0.2$ they tie.

This example compares fixed linear approximations without fine-tuning and is not a measured neural-network result.

The weighted objective is a Frobenius norm after scaling the inputs: $\mathbb E\|(W-\widetilde W)x\|_2^2=\|(W-\widetilde W)M_x^{1/2}\|_F^2$. If $M_x$ is positive definite, truncate $WM_x^{1/2}$ to rank $r$ and multiply the result on the right by $M_x^{-1/2}$. In the present example $M_x=\operatorname{diag}(p,1-p,0,0)$ is singular. Only the first two columns affect the objective; setting the unsupported columns to zero attains the optimum. The two squared singular values of $WM_x^{1/2}$ are $36p$ and $9(1-p)$, with additional zeros. Keeping the larger weighted mode therefore gives the globally minimal rank-at-most-one error $\min(36p,9(1-p))$. At the tie $p=0.2$, both illustrated choices attain 7.2; other rank-one solutions can also attain the optimum.

For positive semidefinite $M_x$ including singular cases, write $C=M_x^{1/2}$, let $C^+$ be its Moore–Penrose pseudoinverse, and let $Y_r=(WC)_r$ be a truncated SVD. One minimizer is $\widetilde W_r=Y_rC^+$. Indeed, $P=C^+C$ projects onto the support of $C$, and $Y_rP=Y_r$ because its nonzero right singular vectors lie in that support. Hence $\widetilde W_r C=Y_r$, with rank at most $r$, attaining the unconstrained Frobenius lower bound. Components on the null space of $C$ do not affect the objective; any alternative completion must still respect the rank constraint. At $p=0$ or $p=1$ in the toy example, only one input direction has support.

The animation sweeps $p$ from 0.1 to 0.9 and back, holding at the crossing. The left bars show retained-mode candidates' weighted energies on the same 0–36 scale; the right curves show the **discarded** energy for each choice, so keeping the larger left bar corresponds to the lower curve. The two colored markers coincide at the tie. The still preview uses $p=0.1$. All values are illustrative, not model measurements.

<div style="max-width:100%;overflow-x:auto" role="group" tabindex="0" aria-label="Input mixture changes the two weighted mode energies and the expected output errors of retaining either mode.">
<div style="width:640px">
<img data-source-asset-urls src="../../../../assets/concept-animations/svd-input-weighted-rank-one-still.svg" data-motion-src="../../../../assets/concept-animations/svd-input-weighted-rank-one-motion.svg" data-still-src="../../../../assets/concept-animations/svd-input-weighted-rank-one-still.svg" alt="Input mixture changes the two weighted mode energies and the expected output errors of retaining either mode." width="640" height="360">
</div>
</div>

*Original 12-second teaching animation (CC BY-SA 4.0).* Use Play/Pause on MkDocs; the focusable container scrolls horizontally on narrow screens. GitHub displays the [static preview](../../../../assets/concept-animations/svd-input-weighted-rank-one-still.svg); the [full animation](../../../../assets/concept-animations/svd-input-weighted-rank-one-motion.svg) is also linked.

## Results

Denton et al. report, for convolutional layers, speed-ups of about 2 times on both CPU and GPU, with accuracy kept within 1% of the original model. The exact figures for each network are in the paper.

## Limitations

The method works only when the layer is close to low rank. Errors can grow quickly in the layers that matter most, so the gains are uneven across a network. A factorised layer also needs two matrix multiplications instead of one, which can offset the saving on hardware that favours a single large operation.

## Open issues and related variants

- **Rank selection.** Choosing \(r\) per layer is usually done by searching against validation accuracy, and an automatic rule is not established.
- **Related:** [low-rank filter expansion](../low-rank-filter-expansion/index.md) factorises convolutional filters into a basis of separable filters instead of a single SVD.
- **Related:** [LoRA](../lora/index.md) applies the same low-rank structure during fine-tuning, without compressing the base model.

## Connections

The singular value decomposition is a basic tool of [linear algebra](../../../math/index.md), and the best low-rank approximation is a standard result in numerical analysis. The dense layers it compresses are the same ones described on the [multilayer perceptron](../../../models/mlp/index.md) page.

## References

### Seminal papers

- Denton, R., Zaremba, W., Bruna, J., LeCun, Y., Fergus, R. (2014). *Exploiting Linear Structure Within Convolutional Networks for Efficient Evaluation*. arXiv:1404.0736. https://arxiv.org/abs/1404.0736 — Applies low-rank approximations to convolutional filters, with speed-ups of about 2 times and accuracy kept within 1%.
- Jaderberg, M., Vedaldi, A., Zisserman, A. (2014). *Speeding up Convolutional Neural Networks with Low Rank Expansions*. arXiv:1405.3866. https://arxiv.org/abs/1405.3866 — Low-rank expansions of convolutional filters, an alternative to a single SVD per layer.
- Hu, E. J., et al. (2021). *LoRA: Low-Rank Adaptation of Large Language Models*. arXiv:2106.09685. https://arxiv.org/abs/2106.09685 — The same low-rank structure used as a fine-tuning update rather than a compression step.

### Surveys and textbooks

- Hoefler, T., et al. (2021). *Sparsity in Deep Learning: Pruning and Growth for Efficient Inference and Training in Neural Networks*. arXiv:2102.00554. https://arxiv.org/abs/2102.00554 — Surveys efficiency methods, including the factorisation of weight matrices.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Gholami, A., et al. (2021). *A Survey of Quantization Methods for Efficient Neural Network Inference*. arXiv:2103.13630. https://arxiv.org/abs/2103.13630 — Compares low-bit precision with other compression methods such as factorisation.
