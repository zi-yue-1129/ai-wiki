---
status: complete
last_reviewed: 2026-10-28
related:
  - theory/deep-learning/nas-automl
tags:
  - neural architecture search
  - differentiable search
  - bilevel optimisation
aliases:
  - DARTS
  - Differentiable Architecture Search
  - 可微分架構搜尋
---

# DARTS: Differentiable Architecture Search (Liu et al., 2019)

DARTS relaxes the discrete choice of operations in a cell into a weighted sum, so that the architecture weights can be optimised by gradient descent alongside the network weights. After the search, the architecture is discretised by keeping the strongest choices. Part of [Neural architecture search](index.md).

## Overview

Earlier NAS methods searched over discrete choices and needed a controller or an evolutionary loop to propose each candidate. Liu, Simonyan and Yang (2019) observed that the choice among operations can be made soft. Every edge of a cell then carries a weighted mixture of candidate operations, and the mixing weights are learned on a validation set.

## Key concepts

- **Cell**: a small directed acyclic graph of nodes, whose edges carry operations. A full network stacks copies of a searched cell.
- **Mixed operation**: the weighted sum of all candidate operations on an edge.
- **Architecture weights** \(\alpha\): the logits that set the mixing weights, learned by gradient descent on the validation loss.
- **Network weights** \(w\): the ordinary parameters of the operations, learned on the training loss.
- **Discretisation**: the final step that replaces each mixed operation by its strongest choice.

## Problem

How can the choice of operations in a cell be searched by gradient descent, without training each discrete candidate, and how should the soft choice be turned back into a fixed architecture?

## How it works

On each edge \((i,j)\), the mixed operation is

\[
\bar o^{(i,j)}(x) = \sum_{o\in\mathcal O} \frac{\exp\bigl(\alpha_o^{(i,j)}\bigr)}{\sum_{o'\in\mathcal O}\exp\bigl(\alpha_{o'}^{(i,j)}\bigr)}\, o(x),
\]

where \(\mathcal O\) is the set of candidate operations. The search is a bilevel problem: the architecture weights minimise the validation loss, given network weights that minimise the training loss,

\[
\min_{\alpha} \; \mathcal L_{\text{val}}\bigl(w^\ast(\alpha), \alpha\bigr) \quad \text{s.t.} \quad w^\ast(\alpha) = \arg\min_w \mathcal L_{\text{train}}(w, \alpha).
\]

The inner problem is approximated by one gradient step, \(w' = w - \xi \nabla_w \mathcal L_{\text{train}}(w,\alpha)\), which gives a first-order or second-order update to \(\alpha\). After the search, each edge keeps the operation with the largest \(\alpha\), and each node keeps its two strongest incoming edges.

## Key methods

This page covers one method: a bilevel gradient search over a relaxed cell, with discretisation at the end.

1. Build a supernet: stack cells in which every edge is a mixed operation.
2. Alternate gradient steps on the network weights (training split) and the architecture weights (validation split).
3. Discretise the learned \(\alpha\) into a fixed cell by keeping the strongest operations and edges.
4. Train the discrete architecture from scratch and evaluate it on held-out data.

## Variants

- **First-order DARTS** sets \(\xi = 0\), which removes the second derivative and is cheaper.
- **Second-order DARTS** keeps the unrolled step, which is more accurate but needs more memory and compute.
- **Cell-based search** searches one cell and stacks it, and the cell found on CIFAR-10 can be transferred to ImageNet.

## Results and limits

- Liu et al. (2019) report that the method discovers high-performance convolutional cells on CIFAR-10 and ImageNet, and recurrent cells on language-modelling benchmarks, and that it is orders of magnitude faster than non-differentiable methods.
- The supernet holds every candidate operation in memory at once, which limits the size of the search space that fits on one device.
- The search can collapse towards parameter-free operations, such as skip connections, which look good early in the search. Zela et al. (2020) analyse this collapse and propose regularisation that prevents it.
- The bilevel gradient is an approximation. Its quality depends on the learning rates of both levels, and on how well the supernet ranks candidates (Yu et al., 2020).

## Applications

- **Designing image-classification cells** for a fixed compute budget, as a cheaper alternative to reinforcement-learning search.
- **Sequence-model cells**, searched on language modelling with the same relaxation.
- **Baselines** for later search methods.

## Open questions

- How can the collapse towards skip connections be prevented without hand-tuned regularisation?
- Does the supernet ranking used during search predict the accuracy of the discrete architecture after full training?

## Connections

- Parent topic: [Neural architecture search](index.md)
- Other method on this topic: [Efficient Neural Architecture Search (ENAS)](efficient-neural-architecture-search.md), which also shares weights between candidates but samples them with a controller
- Related optimisation idea: [Hyperparameter optimisation](../../optimization/hyperparameter-optimisation/index.md), which tunes the outer settings of a fixed architecture

## References

### Seminal papers

- Liu, H., Simonyan, K. & Yang, Y. (2019). DARTS: Differentiable Architecture Search. In *ICLR 2019*. arXiv:1806.09055. https://arxiv.org/abs/1806.09055 — Introduces the continuous relaxation of the cell search space and the bilevel gradient search.
- Pham, H. et al. (2018). Efficient Neural Architecture Search via Parameter Sharing. In *Proceedings of the 35th ICML*, PMLR 80. https://proceedings.mlr.press/v80/pham18a.html — Shows that weight sharing across candidates makes the search far cheaper.
- Zoph, B. & Le, Q. V. (2017). Neural Architecture Search with Reinforcement Learning. In *ICLR 2017*. arXiv:1611.01578. https://arxiv.org/abs/1611.01578 — The reinforcement-learning search that DARTS replaces with gradient descent.

### Surveys and textbooks

- Zela, A. et al. (2020). Understanding and Robustifying Differentiable Architecture Search. In *ICLR 2020*. arXiv:1909.09656. https://arxiv.org/abs/1909.09656 — Explains why differentiable search collapses towards skip connections, and how to regularise it.
- Yu, K. et al. (2020). Evaluating the Search Phase of Neural Architecture Search. In *ICLR 2020*. arXiv:1902.08142. https://arxiv.org/abs/1902.08142 — Tests how well the search phase of weight-sharing methods ranks architectures.
- Elsken, T., Metzen, J. H. & Hutter, F. (2019). Neural Architecture Search: A Survey. *Journal of Machine Learning Research* 20(55). https://jmlr.org/papers/v20/18-598.html — Survey that places DARTS among the search strategies.
