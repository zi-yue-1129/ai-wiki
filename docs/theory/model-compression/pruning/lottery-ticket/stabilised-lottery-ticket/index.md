---
status: draft
last_reviewed: 2026-10-28
tags:
- model compression
- sparsity
- lottery ticket hypothesis
aliases:
  - Stabilised lottery ticket
  - Stabilizing the lottery ticket hypothesis
  - 穩定的彩票假說
---

# Stabilised Lottery Tickets

The stabilised lottery ticket work extends the [lottery ticket hypothesis](../lottery-ticket-hypothesis/index.md) to deeper networks. Frankle and colleagues found that resetting the surviving weights to their initialisation fails for larger models, and that rewinding them to an early point in training, after the first unstable steps, recovers winning tickets.

## Problem

For deeper networks, resetting to the initialisation does not produce winning tickets. The hypothesis then appeared to fail beyond small models.

## Core idea

Rewind the surviving weights to an early iteration of training, rather than to the initialisation. The early point is chosen after the initial instability of training, so that the rewound weights are stable. The authors also search for subnetworks that can be identified early in training.

## Equation or algorithm

The iterative procedure is modified so that the mask is taken from training at an early iteration \(k\) and the surviving weights are rewound to the weights at iteration \(k\). Training then continues from there, with pruning repeated in the same way.

## Results

The abstract describes the modified procedure as finding subnetworks that could have been obtained by pruning early in training, and it extends the tickets to deeper networks.

## Limitations

Finding tickets still needs a full dense training run to the rewind point, so the approach does not save training compute on its own.

## Open issues and related variants

- **Rewind point.** The right point to rewind to depends on the network and the dataset, and it is found by experiment.
- **Related:** [gradual pruning](../../magnitude-pruning/gradual-pruning/index.md) removes the need for repeated training runs by pruning during a single run.

## Connections

The stabilised procedure is the version that scales the ticket idea to the networks used in [training](../../../../../engineering/training/index.md) practice. The question of which sparse subnetworks train well is also a question of [deep learning theory](../../../../../theory/deep-learning/index.md).

## References

### Seminal papers

- Frankle, J., Dziugaite, G. K., Roy, D. M., Carbin, M. (2019). *Stabilizing the Lottery Ticket Hypothesis*. arXiv:1903.01611. https://arxiv.org/abs/1903.01611 — Rewinds to an early training point to find winning tickets in deeper networks.
- Frankle, J., Carbin, M. (2018). *The Lottery Ticket Hypothesis: Finding Sparse, Trainable Neural Networks*. arXiv:1803.03635. https://arxiv.org/abs/1803.03635 — The original reset-to-initialisation procedure that this work modifies.
- Han, S., Pool, J., Tran, J., Dally, W. J. (2015). *Learning both Weights and Connections for Efficient Neural Networks*. arXiv:1506.02626. https://arxiv.org/abs/1506.02626 — The iterative prune-and-retrain pipeline that the ticket procedure extends.

### Surveys and textbooks

- Hoefler, T., et al. (2021). *Sparsity in Deep Learning: Pruning and Growth for Efficient Inference and Training in Neural Networks*. arXiv:2102.00554. https://arxiv.org/abs/2102.00554 — Surveys sparse training, including tickets found by rewinding.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Gale, T., Elsen, E., Hooker, S. (2019). *The State of Sparsity in Deep Neural Networks*. arXiv:1902.09574. https://arxiv.org/abs/1902.09574 — Benchmarks the sparse networks that tickets produce against other methods.
