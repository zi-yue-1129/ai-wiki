---
status: draft
last_reviewed: 2026-10-28
tags:
  - architecture
  - gradient descent
  - search
aliases:
  - Differentiable Architecture Search
  - DARTS
  - 可微分架構搜尋
---

# DARTS: Differentiable Architecture Search (Liu et al., 2018)

DARTS replaces the discrete choice of architecture with a continuous one. Each candidate operation receives a learned weight, and these weights are optimised by gradient descent alongside the network's own parameters. Compared with the earlier reinforcement-learning and evolutionary methods, it cut the cost of [neural architecture search](../index.md) by about three orders of magnitude.

## Overview

Earlier methods, including the [RL controller](../nas-rl/index.md) and [regularized evolution](../regularized-evolution/index.md), treat each candidate as a black box that returns one score, so the search needs many trained candidates. Liu, Simonyan and Yang (2018) asked whether the architecture could be made continuous, so that gradients could guide the search.

## Key concepts

- **Cell.** The searched block is a small directed acyclic graph. A normal cell keeps the image size, and a reduction cell halves it.
- **Mixed operation.** On each edge, all candidate operations are applied and their outputs are summed with softmax weights, including a zero operation that means no connection.
- **Architecture weights \(\alpha\).** The learnable logits that set the mixing weights. All normal cells share one set, and all reduction cells share another.
- **First-order and second-order updates.** A first-order update ignores how the weights would change after an architecture step. A second-order update accounts for it with a one-step look-ahead, at extra cost.

## How it works

The search alternates two gradient steps (Algorithm 1).

1. **Architecture step.** Update \(\alpha\) by descending \(\nabla_\alpha \mathcal{L}_{\mathrm{val}}(w - \xi \nabla_w \mathcal{L}_{\mathrm{train}}(w, \alpha), \alpha)\). The step size \(\xi\) is zero for the first-order method.
2. **Weight step.** Update the network weights \(w\) by descending \(\nabla_w \mathcal{L}_{\mathrm{train}}(w, \alpha)\) on training data.

The relaxation replaces the choice of operation on each edge with a softmax mixture,

\[
\bar{o}^{(i,j)}(x) = \sum_{o \in \mathcal{O}} \frac{\exp\big(\alpha_o^{(i,j)}\big)}{\sum_{o' \in \mathcal{O}} \exp\big(\alpha_{o'}^{(i,j)}\big)}\, o(x),
\]

where \(\mathcal{O}\) is the set of candidate operations. At the end of the search, each node keeps its \(k\) strongest operations from distinct predecessor nodes, with the zero operation excluded. The paper keeps the top two predecessors per node, and only at the very end.

The outer objective is a bilevel problem: choose \(\alpha\) to minimise the validation loss at the \(w\) that minimises the training loss for that \(\alpha\). The one-step approximation avoids solving the inner problem. All candidates share one over-parameterised network and its operation weights, which makes a single search feasible, but it also biases the ranking, because each candidate's weights are trained among many others.

## Results

On CIFAR-10, the second-order DARTS cell reached a 2.76% ± 0.09 test error with 3.3M parameters, at a search cost of 4 GPU days. The first-order variant reached 3.00% ± 0.14 at 1.5 GPU days. Random sampling in the same space gave 3.29% ± 0.15. The paper compares these costs with 2000 GPU days for NASNet (Zoph et al., 2017) and 3150 GPU days for AmoebaNet (Real et al., 2018).

The cell transferred to ImageNet in the mobile setting with 26.7% top-1 error. On Penn Treebank, the recurrent cell reached a test perplexity of 55.7, with about one GPU day for four runs.

Two ablations test the bilevel formulation. Optimising \(\alpha\) on the union of training and validation data gave 4.16% ± 0.16 error with coordinate descent, and 3.56% ± 0.10 with SGD. The authors suspect that \(\alpha\) then overfits the training data.

## Limitations

- **Continuous-to-discrete gap.** The search trains with soft mixtures, but the final architecture keeps only a few operations. The paper names this discrepancy and suggests annealing the softmax temperature.
- **Memory.** Keeping every operation makes the supernet larger than any candidate, so the search runs on eight cells and the cell is then evaluated in a network of twenty.
- **Restricted space.** The evidence covers convolutional and recurrent cells in one template.

## Open questions

- **Discretisation.** Can the gap between the relaxed network and the discrete architecture close while keeping gradient efficiency?
- **Robustness.** How much of the advantage survives a common protocol? Yang et al. (2019) argue for measuring gains against random architectures.
- **Random search.** Li and Talwalkar (2019) find that random search with weight sharing beats random search with early stopping on PTB and is highly competitive on CIFAR-10. Part of the gain may lie in the sharing scheme and the space, not only in gradients.

## References

### Seminal papers

- Liu, H., Simonyan, K. & Yang, Y. (2018). *DARTS: Differentiable Architecture Search*. arXiv:1806.09055. https://arxiv.org/abs/1806.09055 — The paper itself: a continuous relaxation of the architecture choice, trained by gradient descent.
- Zoph, B., et al. (2017). *Learning Transferable Architectures for Scalable Image Recognition*. arXiv:1707.07012. https://arxiv.org/abs/1707.07012 — NASNet, the searched cell whose cost of about 2000 GPU days DARTS compares against.
- Pham, H., et al. (2018). *Efficient Neural Architecture Search via Parameter Sharing*. arXiv:1802.03268. https://arxiv.org/abs/1802.03268 — ENAS, a cheap weight-sharing baseline that DARTS compares against.
- Real, E., et al. (2018). *Regularized Evolution for Image Classifier Architecture Search*. arXiv:1802.01548. https://arxiv.org/abs/1802.01548 — The AmoebaNet search whose cost of about 3150 GPU days DARTS compares against.

### Surveys and textbooks

- Elsken, T., Metzen, J. H. & Hutter, F. (2018). *Neural Architecture Search: A Survey*. arXiv:1808.05377. https://arxiv.org/abs/1808.05377 — Organises NAS by search space, search strategy and performance estimation.

### Articles and documentation

- Li, L. & Talwalkar, A. (2019). *Random Search and Reproducibility for Neural Architecture Search*. arXiv:1902.07638. https://arxiv.org/abs/1902.07638 — Random search with weight sharing, which beats random search with early stopping on PTB.
- Yang, A., Esperança, P. M. & Carlucci, F. M. (2019). *NAS evaluation is frustratingly hard*. arXiv:1912.12522. https://arxiv.org/abs/1912.12522 — Argues for comparing NAS methods under a shared protocol and against random architectures.
