---
status: complete
last_reviewed: 2026-10-28
related:
  - theory/deep-learning/nas-automl
tags:
  - neural architecture search
  - evolutionary algorithms
  - aging
aliases:
  - Regularized evolution
  - Aging evolution
  - 正則化演化
---

# Regularized evolution (Real et al., 2019)

Regularized evolution is an evolutionary search over architectures that keeps a population in age order and removes the oldest member each step, instead of the worst. Parents are chosen by tournament, and children are produced by a small mutation of the parent. Part of [Neural architecture search](index.md).

## Overview

Zoph and Le (2017) searched for architectures with reinforcement learning, and the field then assumed that a learned controller was needed to make the search efficient. Real, Aggarwal, Huang and Le (2019) showed that a plain evolutionary search can match or exceed reinforcement learning under the same compute budget, provided that the population is managed in a particular way. The key change is to remove the oldest model rather than the worst one, which keeps the population diverse and stops early lucky models from dominating it.

## Key concepts

- **Population**: a queue of trained architectures, ordered by age.
- **Tournament selection**: a sample of population members is drawn, and the best of the sample becomes the parent.
- **Mutation**: a small random change to the parent, such as changing one operation or one connection.
- **Aging**: removing the oldest architecture from the population at each step, regardless of its score.

## Problem

How can an evolutionary search over architectures find models at least as good as reinforcement-learning search, without a learned controller?

## How it works

The algorithm starts with a population of randomly generated architectures, each trained and scored on the validation set. At each step it does the following.

1. Draw a sample of \(S\) members from the population at random, and choose the best of them as the parent.
2. Mutate the parent to produce a child, and train the child.
3. Add the child to the population.
4. Remove the oldest member of the population.

Because the oldest member is removed rather than the worst, a model that scored well early does not stay in the population forever, and the search keeps exploring.

## Key methods

This page covers one method: aging evolution with tournament selection and single mutations.

- **Initial population**: random architectures, trained to completion.
- **Selection**: tournament of size \(S\) to choose the parent.
- **Mutation**: a small random change to the parent's architecture.
- **Replacement**: the child enters the population and the oldest member leaves.

## Variants

- **Worst-removal evolution** removes the lowest-scoring member instead. Real et al. (2019) show that aging is the better choice in their experiments.
- **Other mutation sets** change the operations and connections allowed, which changes the search space rather than the algorithm.

## Results and limits

- Real et al. (2019) report that regularised evolution matches or exceeds reinforcement-learning search under the same compute budget on their image-classification search space.
- The method trains every child from scratch, so it costs as much per candidate as the original reinforcement-learning search. Weight sharing methods such as [ENAS](efficient-neural-architecture-search.md) reduce that cost.
- The mutations are designed by hand for the search space, so results depend on the choice of mutations.
- Aging removes good models as well as bad ones, which can slow convergence when the population is small.

## Applications

- **Image classifier search** when a reinforcement-learning controller is not wanted.
- **Searches with many workers**, since children can be trained in parallel and the population needs no synchronisation.
- **Baseline** for newer architecture-search methods.

## Open questions

- How should the population size and tournament size be chosen for a new search space?
- Can aging be combined with weight sharing without losing its diversity benefit?

## Connections

- Parent topic: [Neural architecture search](index.md)
- Earlier evolutionary study: [Large-scale evolution of image classifiers](large-scale-evolution.md)
- Reinforcement-learning search it is compared with: Zoph and Le (2017), cited on the [parent page](index.md)

## References

### Seminal papers

- Real, E., Aggarwal, A., Huang, Y. & Le, Q. V. (2019). Regularized Evolution for Image Classifier Architecture Search. In *Proceedings of the AAAI Conference on Artificial Intelligence* 33, 4780–4789. https://doi.org/10.1609/aaai.v33i01.33014780 — Introduces aging evolution, which removes the oldest model each step, and compares it with reinforcement-learning search.
- Real, E., Moore, S., Selle, A., Saxena, S., Suematsu, Y. L., Tan, J., Le, Q. & Kurakin, A. (2017). Large-Scale Evolution of Image Classifiers. In *Proceedings of the 34th ICML*, PMLR 70. https://proceedings.mlr.press/v70/real17a.html — The earlier large-scale evolutionary study that the aging method builds on.
- Zoph, B. & Le, Q. V. (2017). Neural Architecture Search with Reinforcement Learning. In *ICLR 2017*. arXiv:1611.01578. https://arxiv.org/abs/1611.01578 — The reinforcement-learning search that aging evolution is compared with.

### Surveys and textbooks

- Elsken, T., Metzen, J. H. & Hutter, F. (2019). Neural Architecture Search: A Survey. *Journal of Machine Learning Research* 20(55). https://jmlr.org/papers/v20/18-598.html — Survey that places evolutionary search among the search strategies.
- Pham, H. et al. (2018). Efficient Neural Architecture Search via Parameter Sharing. In *Proceedings of the 35th ICML*, PMLR 80. https://proceedings.mlr.press/v80/pham18a.html — Weight-sharing alternative that reduces the cost of training each candidate.
- Liu, H., Simonyan, K. & Yang, Y. (2019). DARTS: Differentiable Architecture Search. In *ICLR 2019*. arXiv:1806.09055. https://arxiv.org/abs/1806.09055 — Gradient-based alternative to the evolutionary search.
