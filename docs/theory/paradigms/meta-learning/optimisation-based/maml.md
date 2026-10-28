---
status: complete
last_reviewed: 2026-10-28
related:
  - theory/paradigms/meta-learning/optimisation-based
  - theory/paradigms/transfer/fine-tuning-and-adaptation
  - theory/paradigms/continual/regularisation-based
tags:
  - meta-learning
  - few-shot learning
  - bi-level optimisation
aliases:
  - 模型無關元學習
  - MAML
  - Model-agnostic meta-learning
---

# MAML: Model-Agnostic Meta-Learning

MAML learns an initialisation of a network's parameters so that a few gradient steps on a new task give good performance on that task. It is trained over many small tasks, and its objective scores the parameters after adaptation rather than before. It is the reference method for the [optimisation-based meta-learning](index.md) family.

## Overview

Finn, Abbeel and Levine (2017) presented MAML at ICML 2017 (PMLR 70). The method does not depend on a particular architecture: any model trained by gradient descent with a differentiable loss can be used. The paper applies it to few-shot classification on Omniglot and miniImageNet, to regression on sinusoids, and to reinforcement learning. The change from ordinary training is that the outer update differentiates through the inner adaptation step, so the learned starting point is chosen for how well it adapts.

## Key concepts

- **Task** \(\mathcal T_i\): a small learning problem drawn from a task distribution \(p(\mathcal T)\). Each task has a few examples used for adaptation and other examples used to measure the result.
- **Inner update**: one or more gradient steps on a single task, starting from the shared parameters \(\theta\), with step size \(\alpha\).
- **Meta-objective**: the sum over sampled tasks of the loss after adaptation.
- **Meta-gradient**: the gradient of the meta-objective with respect to \(\theta\). It passes through the inner update, so it contains second derivatives. The paper describes it as "a gradient through a gradient".
- **First-order MAML (FOMAML)**: an approximation that drops the second-derivative terms and uses the gradient at the adapted parameters.

## How it works

For a task \(\mathcal T_i\), one inner step gives adapted parameters

\[
\theta_i' = \theta - \alpha\,\nabla_\theta \mathcal L_{\mathcal T_i}(f_\theta)
\]

The meta-objective is the loss of the adapted parameters, summed over tasks,

\[
\min_\theta \sum_{\mathcal T_i \sim p(\mathcal T)} \mathcal L_{\mathcal T_i}\big(f_{\theta_i'}\big)
\]

and the shared parameters move with a meta step size \(\beta\):

\[
\theta \leftarrow \theta - \beta\,\nabla_\theta \sum_{\mathcal T_i \sim p(\mathcal T)} \mathcal L_{\mathcal T_i}\big(f_{\theta_i'}\big)
\]

Algorithm 1 in the paper repeats these steps. It samples a batch of tasks, computes the adapted parameters for each task from a few examples, and then updates \(\theta\) with the summed meta-gradient. The paper's inner step sizes include \(\alpha = 0.01\) with 5 inner steps in training for miniImageNet, and \(\alpha = 0.4\) with 1 inner step in training for 5-way Omniglot. The paper does not state a meta step size \(\beta\) for every experiment.

## Key methods

### Model-Agnostic Meta-Learning for Fast Adaptation of Deep Networks (Finn, Abbeel & Levine, 2017)

- **Problem:** deep networks need many examples to learn a new task, while few-shot learning provides only a handful. The paper asks for an initialisation from which a new task can be learned in a few gradient steps.
- **Core idea:** train the shared initialisation across many tasks, scoring each candidate by its loss after a few gradient steps on each task. The learned initialisation is sensitive to the task, so a small gradient step gives a large improvement.
- **Equation or algorithm:** the inner update, the meta-objective and Algorithm 1, as above. The first-order variant, FOMAML, drops the second derivatives.
- **Results:**
  - Omniglot, convolutional network (Table 1): 5-way accuracy 98.7 ± 0.4% at 1 shot and 99.9 ± 0.1% at 5 shots. 20-way accuracy 95.8 ± 0.3% at 1 shot and 98.9 ± 0.2% at 5 shots.
  - miniImageNet, 5-way (Table 1): 48.70 ± 1.84% at 1 shot and 63.11 ± 0.92% at 5 shots. A fine-tuning baseline reaches 28.86 ± 0.54% and 49.79 ± 0.79%. FOMAML reaches 48.07 ± 1.75% and 63.15 ± 0.91%, which is nearly the same as full MAML.
  - Sinusoid regression, 5 shots (Table 2): the mean squared error is 0.67 after one gradient step and 0.35 after 10 steps. The best baseline in that table, pre-training on all tasks, reaches 2.41 and 2.19.
  - The paper notes that the Omniglot comparisons "may not be strictly comparable" with earlier work, because the earlier data splits were not available.
- **Limitations:** the paper has no dedicated limitations section. In the text, the authors say that "a significant computational expense in MAML comes from the use of second derivatives". On-policy reinforcement learning also needs fresh samples from the current policy at every adaptation step. Results depend on the inner step size and the number of inner steps, which differ between experiments and between training and testing.

## Connections

- The wider family, including Reptile and latent embedding optimisation, is on the [Optimisation-based Meta-learning](index.md) page.
- Metric-based methods, such as matching networks, are compared with MAML on Omniglot. They are on the [Metric-based Meta-learning](../metric-based/index.md) page.
- The inner loop is the same operation as [fine-tuning](../../transfer/fine-tuning-and-adaptation/index.md), but MAML learns the starting point for that operation. The fine-tuning baseline in the miniImageNet table is well behind MAML at 1 shot (28.86% against 48.70%).
- Memory-based meta-learners are on the [Memory and model-based](../memory-and-model-based/index.md) page.
- Continual learning uses similar parameter-space ideas but aims to avoid forgetting. See [regularisation-based continual learning](../../continual/regularisation-based/index.md) and [EWC](../../continual/regularisation-based/ewc.md).

## Open questions

- Second-order gradients are costly. First-order approximations keep most of the accuracy on miniImageNet, but when do they fail?
- The inner step size and number of steps matter. Can they be learned reliably across very different tasks?
- Probabilistic and latent-space extensions, such as probabilistic MAML and latent embedding optimisation, address uncertainty and scale. How do they compare on the same benchmarks?

## References

### Seminal papers

- Finn, C., Abbeel, P. & Levine, S. (2017). Model-Agnostic Meta-Learning for Fast Adaptation of Deep Networks. ICML (PMLR 70). https://arxiv.org/abs/1703.03400 — Introduces MAML and reports the Omniglot and miniImageNet results used on this page.
- Nichol, A., Achiam, J. & Schulman, J. (2018). On First-Order Meta-Learning Algorithms. arXiv:1803.02999. https://arxiv.org/abs/1803.02999 — Analyses first-order MAML and introduces Reptile.
- Rusu, A. A. et al. (2018). Meta-Learning with Latent Embedding Optimization. arXiv:1807.05960. https://arxiv.org/abs/1807.05960 — Performs gradient-based adaptation in a learned low-dimensional latent space instead of the raw parameter space.
- Finn, C., Xu, K. & Levine, S. (2018). Probabilistic Model-Agnostic Meta-Learning. arXiv:1806.02817. https://arxiv.org/abs/1806.02817 — Places a distribution over the initialisation, so that adaptation can sample plausible models for ambiguous tasks.
- Antoniou, A., Edwards, H. & Storkey, A. (2018). How to train your MAML. arXiv:1810.09502. https://arxiv.org/abs/1810.09502 — Lists changes that make MAML training more stable and cheaper.

### Surveys and textbooks

- Hospedales, T. et al. (2020). Meta-Learning in Neural Networks: A Survey. arXiv:2004.05439. https://arxiv.org/abs/2004.05439 — Surveys meta-learning and places gradient-based methods among the other families.
