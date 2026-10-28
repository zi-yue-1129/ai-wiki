---
status: draft
last_reviewed: 2026-10-28
tags:
- model compression
- sparsity
- lottery ticket hypothesis
aliases:
  - Lottery ticket hypothesis
  - Winning tickets
  - 彩票假說
---

# Lottery Ticket Hypothesis

The lottery ticket hypothesis says that a dense, randomly initialised network contains a small sparse subnetwork that, trained alone from its original initial weights, reaches accuracy comparable to the full network. Such a subnetwork is a **winning ticket**. The idea changed how researchers think about [pruning](../index.md): the valuable part of a large network may be a lucky initialisation as much as the trained weights.

## Overview

The original experiment is simple. Train a dense network, prune its smallest-magnitude weights, reset the surviving weights to their values at the start of training, and train again. If the reset subnetwork trains to the original accuracy, it is a winning ticket. Resetting to random weights instead of the original initialisation destroys the effect, which is why the initialisation matters.

## Key concepts

- **Winning ticket.** A sparse subnetwork plus the initial weights it was reset to, which trains to the accuracy of the dense network.
- **Iterative magnitude pruning (IMP).** The procedure of training, pruning a fraction of weights, rewinding and repeating, which finds sparser tickets than one-shot pruning.
- **Rewinding.** Resetting the surviving weights to an early iteration of training rather than to the very first step. Rewinding to early training is what makes the ticket work on deeper networks.
- **Sparsity achieved.** Winning tickets often reach high sparsity on small networks, but the same procedure struggles on deeper ones without rewinding.

## Comparison of key methods

| Method | Change to the procedure | Page |
| --- | --- | --- |
| Lottery ticket hypothesis | Reset surviving weights to the original initialisation | [The lottery ticket hypothesis](lottery-ticket-hypothesis/index.md) |
| Stabilised tickets | Rewind to an early training point, which works for deeper networks | [Stabilised lottery tickets](stabilised-lottery-ticket/index.md) |

The second method keeps the procedure of the first and changes only where the weights are rewound to. That one change is what allows tickets to be found in deeper networks.

## Trade-offs

- **Insight versus efficiency.** The hypothesis explains why pruned networks train, but finding tickets costs several training runs, which makes it expensive for large models.
- **Initialisation versus training.** Winning tickets depend on the initial weights, so they are sensitive to the random seed and the optimiser.
- **Pruning at initialisation.** Methods that prune before training would save compute, but they have been less reliable at scale than trained-network methods.

## More variants and open issues

- **Open issue:** whether winning tickets exist for large transformers, and how rewinding should work for them.
- **Open issue:** whether the subnetworks found are transferable between datasets and tasks.
- **Variant:** [magnitude pruning](../magnitude-pruning/gradual-pruning/index.md) with gradual schedules, which avoids repeated training runs.

## Connections

The ticket view connects to the broader question of why overparameterised networks train well, covered under [deep learning theory](../../../../theory/deep-learning/index.md). The idea that the brain starts with more connections than it keeps, and that some of them survive a developmental selection, is discussed in [neuroscience](../../../../brain-mind/neuroscience/index.md).

## References

### Seminal papers

- Frankle, J., Carbin, M. (2018). *The Lottery Ticket Hypothesis: Finding Sparse, Trainable Neural Networks*. arXiv:1803.03635. https://arxiv.org/abs/1803.03635 — Sparse subnetworks trained from their original initialisation match the dense network's accuracy.
- Frankle, J., Dziugaite, G. K., Roy, D. M., Carbin, M. (2019). *Stabilizing the Lottery Ticket Hypothesis*. arXiv:1903.01611. https://arxiv.org/abs/1903.01611 — Rewinds to an early training point to find tickets in deeper networks.
- Han, S., Pool, J., Tran, J., Dally, W. J. (2015). *Learning both Weights and Connections for Efficient Neural Networks*. arXiv:1506.02626. https://arxiv.org/abs/1506.02626 — The prune-and-retrain pipeline that the lottery ticket procedure builds on.

### Surveys and textbooks

- Hoefler, T., et al. (2021). *Sparsity in Deep Learning: Pruning and Growth for Efficient Inference and Training in Neural Networks*. arXiv:2102.00554. https://arxiv.org/abs/2102.00554 — Surveys sparse training and inference, including tickets.
- Gale, T., Elsen, E., Hooker, S. (2019). *The State of Sparsity in Deep Neural Networks*. arXiv:1902.09574. https://arxiv.org/abs/1902.09574 — Benchmarks methods and shows that trained sparse networks are hard to train from scratch.

### Lectures and videos

(none checked for this page)

### Articles and documentation

(none checked for this page)
