---
status: complete
last_reviewed: 2026-10-28
related:
  - theory/deep-learning/nas-automl
tags:
  - neural architecture search
  - parameter sharing
  - reinforcement learning
aliases:
  - ENAS
  - Efficient Neural Architecture Search
  - 高效神經架構搜尋
---

# Efficient Neural Architecture Search (Pham et al., 2018)

ENAS makes architecture search far cheaper than the original reinforcement-learning search by having all candidate architectures share one set of weights. A recurrent controller samples a subgraph of a large graph of operations, and the controller is trained with policy gradients on the validation reward. Part of [Neural architecture search](index.md).

## Overview

The search of Zoph and Le (2017) trained every sampled architecture from scratch, which made it very expensive. Pham, Guan, Zoph, Le and Dean (2018) observed that the candidate architectures are all subgraphs of one large graph, so their operations can share parameters. Training one candidate then updates the parameters that other candidates also use, and the cost of evaluating a candidate falls sharply.

## Key concepts

- **Supergraph**: a directed acyclic graph that contains all candidate architectures as subgraphs.
- **Controller** \(\pi(m;\theta)\): a recurrent network that samples an architecture \(m\) with parameters \(\theta\).
- **Shared weights** \(w\): one set of operation parameters reused by every sampled subgraph.
- **Validation reward** \(R(m,w)\): the accuracy of a sampled architecture \(m\) with shared weights \(w\) on a validation set.

## Problem

How can the controller-based search of Zoph and Le (2017) be made cheap enough to run on modest hardware, without training each sampled architecture from scratch?

## How it works

The search alternates two updates.

1. **Shared weights.** Sample an architecture \(m\) from the controller and train the shared weights \(w\) on the training set, minimising the cross-entropy loss of the subgraph \(m\).
2. **Controller.** Sample several architectures, evaluate their reward on the validation set, and update \(\theta\) to maximise the expected reward \(J(\theta) = \mathbb E_{m\sim\pi(m;\theta)}[R(m,w)]\).

The controller gradient uses the REINFORCE estimator with a baseline \(b\),

\[
\nabla_\theta J(\theta) \approx \frac{1}{M}\sum_{k=1}^{M} \bigl(R(m_k, w) - b\bigr)\,\nabla_\theta \log \pi(m_k;\theta),
\]

where \(M\) is the number of sampled architectures and \(b\) is typically an exponential moving average of past rewards. After the search, the best sampled architecture is trained from scratch.

## Key methods

This page covers one method: a controller that samples subgraphs of a supergraph with shared weights, trained by policy gradients on validation reward.

- **Supergraph design**: a set of operations and connections big enough to contain good architectures.
- **Alternating updates**: the shared weights and the controller are trained in turns on separate data splits.
- **Final training**: the architecture the controller prefers is retrained from scratch, because the shared weights are only an estimate.

## Variants

- **Recurrent cell search** applies ENAS to language modelling, where the output is a recurrent cell.
- **Convolutional cell search** applies it to image classification, where the output is a convolutional cell that is stacked to form the network.
- **Other sampling rules** replace the controller with a different distribution over subgraphs, which changes how the search explores the space.

## Results and limits

- Pham et al. (2018) report that ENAS delivers strong results using much fewer GPU-hours than earlier automatic model design, and about 1000 times less compute than standard NAS.
- On Penn Treebank, the authors report a test perplexity of 55.8 for an architecture found by ENAS. On CIFAR-10, they report a test error of 2.89%, close to NASNet at 2.65% (Pham et al., 2018).
- Parameter sharing can make the rankings of subgraphs unreliable, so the architecture that scores best during search may not be the best one after training. Yu et al. (2020) study this effect for weight-sharing methods.
- The controller's reward depends on shared weights that are still changing, so the reward is noisy and the policy gradient is high-variance.

## Applications

- **Low-budget architecture search**, where reinforcement-learning search would cost too much.
- **Recurrent cell discovery** for sequence modelling, following the language-modelling results.
- **Baselines** for newer weight-sharing methods, such as [DARTS](darts.md), which uses the same idea with a different search strategy.

## Open questions

- How much of the cost saving survives when the search space is much larger or the target is a large modern model?
- Can the reliability of the shared-weight ranking be checked cheaply during the search?

## Connections

- Parent topic: [Neural architecture search](index.md)
- Other method on this topic: [DARTS](darts.md), which relaxes the search space instead of sampling it
- Search that this method makes cheaper: Zoph and Le (2017), described on the [parent page](index.md)

## References

### Seminal papers

- Pham, H., Guan, M., Zoph, B., Le, Q. & Dean, J. (2018). Efficient Neural Architecture Search via Parameter Sharing. In *Proceedings of the 35th ICML*, PMLR 80. https://proceedings.mlr.press/v80/pham18a.html — Introduces ENAS: a controller samples subgraphs of a supergraph that share weights, trained with policy gradients on validation reward.
- Zoph, B. & Le, Q. V. (2017). Neural Architecture Search with Reinforcement Learning. In *ICLR 2017*. arXiv:1611.01578. https://arxiv.org/abs/1611.01578 — The reinforcement-learning search, where each candidate is trained from scratch, that ENAS makes cheaper.
- Liu, H., Simonyan, K. & Yang, Y. (2019). DARTS: Differentiable Architecture Search. In *ICLR 2019*. arXiv:1806.09055. https://arxiv.org/abs/1806.09055 — Another weight-sharing search, which optimises architecture choices by gradient descent.

### Surveys and textbooks

- Yu, K. et al. (2020). Evaluating the Search Phase of Neural Architecture Search. In *ICLR 2020*. arXiv:1902.08142. https://arxiv.org/abs/1902.08142 — Tests whether the shared-weight ranking used during search predicts the final accuracy.
- Zela, A. et al. (2020). Understanding and Robustifying Differentiable Architecture Search. In *ICLR 2020*. arXiv:1909.09656. https://arxiv.org/abs/1909.09656 — Analyses the failure modes of weight-sharing search in the differentiable setting.
- Elsken, T., Metzen, J. H. & Hutter, F. (2019). Neural Architecture Search: A Survey. *Journal of Machine Learning Research* 20(55). https://jmlr.org/papers/v20/18-598.html — Survey that places weight sharing among the performance-estimation strategies.
