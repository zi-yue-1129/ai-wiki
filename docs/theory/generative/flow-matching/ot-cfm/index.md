---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/unsupervised/density-and-generative-models
tags:
  - generative models
  - optimal transport
aliases:
  - OT-CFM
  - 最佳傳輸條件流匹配
  - 最佳輸運條件流匹配
  - Optimal transport conditional flow matching
  - Minibatch optimal transport
---

# OT-CFM: Optimal-Transport Conditional Flow Matching

OT-CFM is a variant of [conditional flow matching](../conditional-flow-matching/index.md) introduced by Tong et al. (2023). Instead of pairing each noise sample with a data sample at random, it pairs them by a minibatch optimal-transport plan. The resulting paths are simpler, and training is more stable and sampling is faster, according to the authors. It is one of the three landmark methods of the [Flow Matching and Rectified Flow](../index.md) topic.

## Overview

In conditional flow matching, each training pair consists of a noise sample and a data sample. Independent pairing is simple, but it gives paths that cross one another and bend. Crossing paths tend to make the velocity field harder to learn. Tong et al. (2023) observe that the choice of pairing is free, and that a pairing with low total transport cost gives simpler flows.

The method draws on optimal transport, the study of the cheapest way to move one distribution onto another (Villani, 2009). Exact plans between full distributions are impractical, so OT-CFM works within each minibatch. The paper also shows that, when the true optimal plan is available, its objective approximates dynamic optimal transport.

## Key concepts

- **Transport cost**: the total cost of moving mass from one distribution to another, here taken as squared Euclidean distance between a noise sample and a data sample.
- **Coupling**: a joint distribution over pairs. A plan is a coupling whose marginals are the two distributions.
- **Minibatch optimal transport**: computing the optimal plan between a batch of noise samples and a batch of data samples, rather than between the full distributions.
- **Dynamic optimal transport**: the formulation of optimal transport in terms of a path of densities and a velocity field (Villani, 2009). The paper's flows approximate it when the true plan is known.

## How it works

Draw a minibatch of \(m\) noise samples \(x_0^{i}\) and \(m\) data samples \(x_1^{j}\). Compute the optimal plan between them for the squared-distance cost:

\[
\pi^\star = \arg\min_{\pi \in \Pi_m} \sum_{i,j} \pi_{ij}\,\big\|x_0^{i} - x_1^{j}\big\|^2
\]

Here \(\Pi_m\) is the set of couplings of the two batches. The minibatch then supplies pairs \((x_0, x_1)\) drawn from \(\pi^\star\), and training proceeds as in conditional flow matching. With straight conditional paths, the regression target is \(x_1 - x_0\), and the loss is

\[
\mathcal{L}_{\text{OT-CFM}} = \mathbb{E}_{(x_0, x_1) \sim \pi^\star}\,\mathbb{E}_{t}\big\|v_\theta\big((1-t)\,x_0 + t\,x_1,\; t\big) - (x_1 - x_0)\big\|^2
\]

The paper states its objective for general Gaussian conditional paths. The straight-path form above is the limit of those paths as the terminal standard deviation goes to zero, so it is the case used for illustration here.

The algorithm is:

1. Sample a minibatch of noise and a minibatch of data.
2. Solve the assignment, or an entropic approximation such as Sinkhorn's algorithm (Peyré & Cuturi, 2018), to get a plan \(\pi^\star\) between them.
3. Sample pairs from the plan, sample \(t\), and take a regression step on the loss above.
4. Sample by solving the learned ODE as in other flow-matching models.

## Results

The paper's experiments cover single-cell dynamics, unsupervised image translation and Schrödinger bridge inference. According to its abstract, OT-CFM creates simpler flows that are more stable to train and lead to faster inference than the independent-coupling version. The abstract also states that, when the true optimal plan is available, OT-CFM approximates dynamic optimal transport. The abstract gives no numerical scores, so none are quoted here.

## Limitations

- **Minibatch plans are approximate.** The plan is optimal only within a batch, so it matches the full optimal transport only roughly. The paper's approximation claim covers the case where the true plan is known.
- **Cost of the plan.** Exact assignment solvers scale poorly with batch size, and entropic solvers add a tuning parameter.
- **Choice of cost.** Squared distance between pixel vectors may not match perceptual similarity, so the cheapest pairing in that metric is not guaranteed to give the most useful paths.
- **Scale.** The experiments cover biological data, image translation and bridge problems. Whether minibatch pairing helps at the scale of large text-to-image models is not shown by them.

## Open questions

- Which transport cost, other than squared Euclidean distance, gives pairings that help generation in high-dimensional data?
- How large must the minibatch be before its plan is close to the full optimal transport?
- How does pairing interact with reflow, which also changes the coupling, in [rectified flow](../rectified-flow/index.md)?

## References

### Seminal papers

- Tong, A. et al. (2023). *Improving and generalizing flow-based generative models with minibatch optimal transport*. arXiv. https://arxiv.org/abs/2302.00482 — The paper itself: the generalised conditional flow matching family, OT-CFM and the experiments described here.
- Lipman, Y., Chen, R. T. Q., Ben-Hamu, H., Nickel, M. & Le, M. (2022). *Flow Matching for Generative Modeling*. arXiv. https://arxiv.org/abs/2210.02747 — The conditional flow matching objective that OT-CFM generalises, with the optimal-transport paths as a special case.
- Albergo, M. S., Boffi, N. M. & Vanden-Eijnden, E. (2023). *Stochastic Interpolants: A Unifying Framework for Flows and Diffusions*. arXiv. https://arxiv.org/abs/2303.08797 — A framework in which the interpolant between two densities can be optimised, and which recovers the Schrödinger bridge in that case.

### Surveys and textbooks

- Peyré, G. & Cuturi, M. (2018). *Computational Optimal Transport*. arXiv. https://arxiv.org/abs/1803.00567 — A short book on optimal transport with a focus on numerical methods, including the entropic approximations used for minibatch plans.
- Villani, C. (2009). *Optimal Transport*. Springer. https://doi.org/10.1007/978-3-540-71050-9 — The standard mathematical reference on the theory of optimal transport and its dynamic formulation.
