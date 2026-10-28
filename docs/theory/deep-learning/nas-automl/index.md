---
status: complete
last_reviewed: 2026-10-28
related:
  - theory/deep-learning
  - theory/optimization/hyperparameter-optimisation
tags:
  - neural architecture search
  - AutoML
  - weight sharing
  - hardware-aware design
aliases:
  - Neural architecture search
  - NAS
  - AutoML
  - 神經架構搜尋
---

# Neural architecture search and AutoML

Neural architecture search (NAS) automates the design of network architectures: a search procedure proposes candidate architectures, estimates how well each would perform, and returns the best one. It is part of the wider field of automated machine learning (AutoML). Part of [Deep Learning](../index.md).

## Overview

Designing a network by hand relies on expert intuition and a long series of trial runs. Zoph and Le (2017) showed that a recurrent controller trained with reinforcement learning could design a convolutional network that rivalled human-designed ones on CIFAR-10. The approach was expensive, because every candidate had to be trained from scratch. Most of the later work aims to make the same search cheaper, by sharing weights between candidates, by searching in a continuous space, or by using cheaper proxies for performance.

## Key concepts

- **Search space**: the set of architectures the search may produce, such as the choice of operations and how they connect.
- **Search strategy**: the rule for proposing candidates, such as reinforcement learning, evolution, gradient descent or random sampling.
- **Performance estimation**: the way a candidate's quality is measured, which can be full training, a short training run, or a shared-weight shortcut.
- **Weight sharing**: a set of parameters reused across many candidate architectures, so each candidate need not be trained from scratch.
- **Hardware-aware objective**: a search goal that includes measured cost on a target device, such as latency, along with accuracy.

## Problem

How can a good architecture be found within a fixed compute budget, without a human writing each candidate, and does the result transfer to the tasks and devices it was not searched on?

## How it works

Elsken, Metzen and Hutter (2019) describe NAS as three parts: a search space, a search strategy and a performance estimation strategy. The search strategy proposes an architecture from the space, the estimator scores it, and the score updates the strategy. The loop repeats until the budget is spent, and the best architecture is then trained fully and evaluated on held-out data.

Methods differ mainly in how they make this loop cheaper. Some keep a reinforcement-learning controller and share weights across candidates. Others relax the discrete choice into a continuous one and optimise it by gradient descent. Evolutionary methods mutate a population of architectures and keep the fittest.

## Key methods

- [DARTS](darts.md): a continuous relaxation of the search space, optimised by gradient descent.
- [Efficient Neural Architecture Search (ENAS)](efficient-neural-architecture-search.md): a controller that samples subgraphs of one shared network.
- [Regularized evolution](regularized-evolution.md): aging evolution, which removes the oldest architecture each step, and matches or exceeds reinforcement-learning search under equal compute.
- [Large-scale evolution](large-scale-evolution.md): simple evolution with novel mutation operators, starting from trivial networks, run at very large scale.
- [MnasNet](mnasnet.md): reinforcement-learning search whose reward combines accuracy with latency measured on a phone.

## Variants

- **Reinforcement-learning search** (Zoph & Le, 2017) trains a controller on the validation accuracy of each sampled candidate.
- **Evolutionary search** keeps a population of architectures and mutates them. Real et al. (2019) show that removing the oldest member of the population, instead of the worst, makes the search more effective.
- **Hardware-aware search** adds the measured latency of a candidate on a target phone to the objective. Tan et al. (2019) use this idea to design mobile image classifiers.

## Results and limits

- Zoph and Le (2017) report a test error of 3.65% on CIFAR-10 for a network found by the search, which they describe as rivalling the best human-invented architecture.
- ENAS reports that it is about 1000 times less expensive than standard NAS, through weight sharing (Pham et al., 2018).
- DARTS reports searches that are orders of magnitude faster than non-differentiable methods (Liu et al., 2019).
- Weight-shared evaluation can rank candidates unreliably. Yu et al. (2020) find that several weight-sharing methods do not reliably beat random sampling of architectures during their search phase.
- Differentiable search can collapse towards parameter-free operations such as skip connections, and this can be fixed with regularisation (Zela et al., 2020).

## Applications

- **Mobile and edge vision models**, where latency on the target device is part of the goal.
- **Sequence models**, such as the recurrent cell found by Zoph and Le (2017) for language modelling.
- **Reusable search pipelines** inside AutoML systems, which combine architecture search with the hyperparameter search described in [Hyperparameter optimisation](../../optimization/hyperparameter-optimisation/index.md).

## Open questions

- Does a searched architecture beat a well-tuned hand-designed baseline when the baseline is also tuned with equal compute?
- How reliable are the cheap estimates of performance, and how often do they rank architectures wrongly?
- Do architectures searched on one dataset transfer to other tasks and to the large-scale models used today?

## Connections

- Parent topic: [Deep Learning](../index.md)
- Hyperparameter search, which tunes a fixed architecture: [Hyperparameter optimisation](../../optimization/hyperparameter-optimisation/index.md)
- Architectures of the kind searched over: [Transformers](../../models/transformer/index.md)

## References

### Seminal papers

- Zoph, B. & Le, Q. V. (2017). Neural Architecture Search with Reinforcement Learning. In *ICLR 2017*. arXiv:1611.01578. https://arxiv.org/abs/1611.01578 — Uses a recurrent controller trained with reinforcement learning to design convolutional and recurrent cells.
- Real, E., Aggarwal, A., Huang, Y. & Le, Q. V. (2019). Regularized Evolution for Image Classifier Architecture Search. In *Proceedings of the AAAI Conference on Artificial Intelligence* 33, 4780–4789. https://doi.org/10.1609/aaai.v33i01.33014780 — Shows that evolutionary search, with the oldest model removed, matches or exceeds reinforcement-learning search under the same compute budget.
- Pham, H., Guan, M., Zoph, B., Le, Q. & Dean, J. (2018). Efficient Neural Architecture Search via Parameter Sharing. In *Proceedings of the 35th ICML*, PMLR 80. https://proceedings.mlr.press/v80/pham18a.html — Introduces weight sharing across candidate architectures, which reduces the cost of the search.
- Liu, H., Simonyan, K. & Yang, Y. (2019). DARTS: Differentiable Architecture Search. In *ICLR 2019*. arXiv:1806.09055. https://arxiv.org/abs/1806.09055 — Relaxes the search space so that it can be optimised by gradient descent.
- Tan, M. et al. (2019). MnasNet: Platform-Aware Neural Architecture Search for Mobile. In *CVPR 2019*. arXiv:1807.11626. https://arxiv.org/abs/1807.11626 — Adds measured latency on a mobile phone to the search objective.

### Surveys and textbooks

- Elsken, T., Metzen, J. H. & Hutter, F. (2019). Neural Architecture Search: A Survey. *Journal of Machine Learning Research* 20(55). https://jmlr.org/papers/v20/18-598.html — Survey that organises NAS into search space, search strategy and performance estimation.
- Yu, K., Sciuto, C., Jaggi, M., Musat, C. & Salzmann, M. (2020). Evaluating the Search Phase of Neural Architecture Search. In *ICLR 2020*. arXiv:1902.08142. https://arxiv.org/abs/1902.08142 — Tests whether the search phase of weight-sharing methods finds good architectures, and finds that it often does not.
- Zela, A., Elsken, T., Saikia, T., Marrakchi, Y., Brox, T. & Hutter, F. (2020). Understanding and Robustifying Differentiable Architecture Search. In *ICLR 2020*. arXiv:1909.09656. https://arxiv.org/abs/1909.09656 — Analyses the collapse of differentiable search and proposes regularisation to avoid it.

## Further learning

- Hutter, F., Kotthoff, L. & Vanschoren, J. (eds.) (2019). *Automated Machine Learning: Methods, Systems, Challenges*. Springer. https://doi.org/10.1007/978-3-030-05318-5 — Book with chapters on NAS and hyperparameter optimisation.
