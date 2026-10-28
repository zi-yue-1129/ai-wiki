---
status: complete
last_reviewed: 2026-10-28
aliases:
  - PBT
  - Population Based Training
---

# Population-based training (Jaderberg et al., 2017)

An asynchronous optimisation method that trains a population of models and tunes their hyperparameters during training. Members that fall behind copy the weights and hyperparameters of better members, and then explore new hyperparameter values.

## Problem

Hyperparameters such as learning rates, exploration settings and loss weights strongly affect how neural networks train. A single fixed setting is usually a compromise over the whole run. Search methods that train many configurations separately spend most of their budget on poor settings, and they still return one fixed setting. Jaderberg et al. ask whether a single training run, with a population of models, can find a schedule of hyperparameters and select models at the same time.

## Core idea

PBT keeps a population of workers, each training its own model in parallel. Each worker alternates between two phases:

- **Step.** The worker trains with gradient descent for a number of steps, and it records its performance (the evaluation score).
- **Exploit and explore.** When a worker is ready, it can exploit the rest of the population. Exploit selects another member to copy the weights and hyperparameters from. Explore then creates new hyperparameters for the next steps by either perturbing the copied values or resampling them from the original prior.

Because the copying and perturbation happen during training, the population produces a schedule of hyperparameter values rather than one fixed setting. The method needs only a small change to a standard distributed training framework.

## Equation or algorithm

Each worker repeats the following loop:

1. Train for \(T\) gradient steps with the current weights \(\theta\) and hyperparameters \(h\).
2. Evaluate the model with the performance measure \(p\), such as the mean episodic return or the validation score.
3. If the worker is under-performing the rest of the population, copy the weights and hyperparameters of a better member, \(h, \theta \leftarrow \text{exploit}(h, \theta, p, P)\).
4. Perturb or resample the copied hyperparameters, \(h \leftarrow \text{explore}(h)\), and continue training.

The paper uses \(\text{exploit}\) to select a member with higher recorded performance, and \(\text{explore}\) to perturb hyperparameters or resample them from the prior. In the experiments, truncation selection copies a member of the top 20% into a bottom-20% worker, and reinforcement-learning runs use a t-test on recent rewards. Each hyperparameter is perturbed by a factor of 1.2 or 0.8 in most experiments, and the GAN experiments use factors of 2.0 or 0.5.

## Results

The paper applies PBT to deep reinforcement learning, supervised learning for machine translation, and generative adversarial networks. For reinforcement learning, it tunes UNREAL on DeepMind Lab levels, Feudal Networks on Atari games, and A3C agents on StarCraft II. The Introduction states that PBT "can match and even outperform heavily tuned hyperparameter schedules". The abstract reports faster wall-clock convergence and higher final performance. The reinforcement-learning comparisons are made at the same number of steps, so the paper does not measure wall-clock speed for them. For translation, the paper reports BLEU gains from 23.71 to 24.23 on validation and from 22.30 to 22.65 on test.

## Limitations

- **Population cost.** The method uses many models at once, so it needs enough parallel compute.
- **Greedy copying.** The paper calls PBT a greedy algorithm that "can get stuck in local optima". A population of 10 or fewer may not keep enough diversity for exploration.
- **Choice of rules.** The exploit and explore rules and their settings depend on the application.

## Connections

- PBT is a population-based form of [hyperparameter optimisation](../../../../../../theory/optimization/index.md), and its schedules are an alternative to a fixed learning-rate schedule.
- Like evolutionary methods, it selects and mutates members of a population, but the inner loop is gradient-based training.
- It is the training method behind the population in [FTW](../ftw/index.md) and sits within the [population-based training](../index.md) overview.

## Applications

- **Reinforcement learning.** Tuning exploration and learning-rate settings of deep agents.
- **Supervised learning.** Maximising a metric such as BLEU for translation directly.
- **Generative models.** Tuning training of GANs against an evaluation score.

## Open questions

- How to choose exploit and explore rules when the evaluation score is noisy.
- How to keep the population diverse when copying favours a few members.

## References

### Seminal papers

- Jaderberg et al. (2017), "Population based training of neural networks", [arXiv:1711.09846](https://arxiv.org/abs/1711.09846) — The PBT paper, with the exploit and explore steps and the experiments on reinforcement learning, translation and GANs.
- Snoek, Larochelle & Adams (2012), "Practical Bayesian optimization of machine learning algorithms", [arXiv:1206.2944](https://arxiv.org/abs/1206.2944) — Bayesian optimisation of hyperparameters, a search-based baseline for PBT's schedules.
- Jaderberg et al. (2016), "Reinforcement learning with unsupervised auxiliary tasks", [arXiv:1611.05397](https://arxiv.org/abs/1611.05397) — UNREAL, one of the agents that PBT tunes in the paper.
- Jaderberg et al. (2019), "Human-level performance in 3D multiplayer games with population-based reinforcement learning", *Science* 364, 859–865. https://discovery.ucl.ac.uk/id/eprint/10076318 — Applies population-based training to Capture the Flag. The link is the author-institution repository record.
- Mnih et al. (2015), "Human-level control through deep reinforcement learning", *Nature* 518, 529–533. https://doi.org/10.1038/nature14236 — A deep reinforcement learning method whose hyperparameters are the kind that PBT tunes.
