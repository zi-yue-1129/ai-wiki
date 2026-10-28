---
status: draft
last_reviewed: 2026-10-28
tags:
  - architecture
  - evolution
aliases:
  - Regularized Evolution
  - Aging Evolution
  - AmoebaNet
  - 正則化演化
---

# Regularized Evolution (Real et al., 2018)

Real et al. (2018) showed that a simple evolutionary algorithm can design image classifiers that beat the best hand-designed networks of their time. Their change to standard tournament selection is to remove the oldest model in the population rather than the worst one. The method is one of the landmark strategies of [neural architecture search](../index.md).

## Overview

Evolutionary algorithms had long been applied to network topologies, but the resulting classifiers had remained weaker than human designs. Real et al. evolved an image classifier, AmoebaNet-A, that surpassed hand-designed networks, and compared the method head to head with reinforcement learning and random search on the same code and budget.

## Key concepts

- **Population.** A queue of trained models, each with a validation accuracy that serves as its fitness.
- **Tournament selection.** Each cycle samples \(S\) models from the population at random and picks the most accurate one as the parent. When \(S = 1\), the method reduces to random search, and larger values make selection more greedy.
- **Aging.** Each model is removed by age, not by fitness. The oldest model leaves the population at every cycle, even if it is still among the best. The paper contrasts this with ordinary tournament selection, which removes the worst model in the sample.
- **Mutation.** A child is made from its parent by one of two changes: a hidden-state mutation, which rewires one pairwise combination in a cell, or an operation mutation, which changes the operation applied in one combination. A third option is the identity, which copies the parent.
- **Cell-based search space.** The search explores the NASNet space of stacked normal and reduction cells.

## How it works

The algorithm runs as follows.

1. **Initialise.** Create \(P\) random architectures. Train and evaluate each, and place it in the population.
2. **Select.** Sample \(S\) models uniformly at random from the population, with replacement. Take the most accurate one as the parent.
3. **Mutate and evaluate.** Apply one mutation to the parent to create a child, then train and evaluate the child.
4. **Age.** Add the child to the population and remove the oldest model. Keep the child in the history of all evaluated models.
5. **Repeat.** Return to step 2 until the history contains a fixed number of models, then return the most accurate model in the history.

The main experiments use \(P = 100\) and \(S = 25\). Because removal is by age, even the best model eventually leaves the population, so the population keeps turning over. The authors argue that this favours younger genotypes and keeps the search exploring, instead of being dominated by early models.

## Results

The main comparison uses CIFAR-10. Evolution, RL and random search were each run five times with identical network code and an identical budget of 20,000 evaluated models. The paper reports that evolution produced more accurate models at early stages of the search, which matters when a search has to be stopped early. Given the full 20,000 models, the paper reports that evolution produced models of similar accuracy to the RL baseline. Random search lagged both. The evolved architectures were more accurate than random-search architectures at similar compute, and used fewer FLOPs than RL architectures at similar accuracy.

The selected model, AmoebaNet-A, reached a 3.34% ± 0.06 test error on CIFAR-10 with 3.2M parameters in the configuration with 36 filters (Table 1 in the paper). At full size on ImageNet the paper reports 83.9% top-1 and 96.6% top-5 accuracy, which the abstract describes as surpassing the hand-designed networks for the first time with this method. The large model has 469M parameters.

## Limitations

- **Compute.** Each search was run on 450 K40 GPUs for about seven days to evaluate 20,000 small models. The search cost is large even though the method itself is simple.
- **Uncontrolled baseline.** The CIFAR-10 comparison is controlled, but the paper notes that its comparison with the published NASNet-A result cannot guarantee identical training code or the same number of experiments.
- **Search-space dependence.** The method searches only the space it is given, so the result depends on that space, as with every NAS method.

## Open questions

- **Speed.** Can the population approach be made much cheaper through weight sharing or proxy evaluation? ENAS (Pham et al., 2018) and [DARTS](../darts/index.md) take this route, although the comparison depends on how the cost is counted.
- **Why aging helps.** The paper's argument is empirical. Whether aging beats other ways of keeping a population diverse is open.
- **Fair baselines.** Yang et al. (2019) propose measuring a method's improvement over randomly sampled architectures from the same space, so that gains can be attributed to the method rather than the space.

## References

### Seminal papers

- Real, E., et al. (2018). *Regularized Evolution for Image Classifier Architecture Search*. arXiv:1802.01548. https://arxiv.org/abs/1802.01548 — The paper itself: aging evolution, with a controlled comparison against RL and random search.
- Zoph, B. & Le, Q. V. (2016). *Neural Architecture Search with Reinforcement Learning*. arXiv:1611.01578. https://arxiv.org/abs/1611.01578 — The RL baseline used in the controlled comparison, with an RNN controller that generates architectures.
- Pham, H., et al. (2018). *Efficient Neural Architecture Search via Parameter Sharing*. arXiv:1802.03268. https://arxiv.org/abs/1802.03268 — Weight sharing between child networks, the cheaper alternative to evolving every model from scratch.

### Surveys and textbooks

- Elsken, T., Metzen, J. H. & Hutter, F. (2018). *Neural Architecture Search: A Survey*. arXiv:1808.05377. https://arxiv.org/abs/1808.05377 — Places evolutionary methods within the search-strategy dimension of NAS.

### Articles and documentation

- Li, L. & Talwalkar, A. (2019). *Random Search and Reproducibility for Neural Architecture Search*. arXiv:1902.07638. https://arxiv.org/abs/1902.07638 — Shows that random search is a competitive NAS baseline.
- Yang, A., Esperança, P. M. & Carlucci, F. M. (2019). *NAS evaluation is frustratingly hard*. arXiv:1912.12522. https://arxiv.org/abs/1912.12522 — Benchmarks eight NAS methods on five datasets and argues for measuring gains over random architectures.
