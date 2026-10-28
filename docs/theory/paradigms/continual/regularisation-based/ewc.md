---
status: complete
last_reviewed: 2026-10-28
related:
  - theory/paradigms/continual/regularisation-based
  - theory/paradigms/continual/replay-and-memory
  - theory/paradigms/transfer/fine-tuning-and-adaptation
tags:
  - continual learning
  - catastrophic forgetting
  - Fisher information
aliases:
  - 彈性權重鞏固
  - EWC
  - Elastic weight consolidation
---

# EWC: Elastic Weight Consolidation

EWC is a regularisation method for continual learning. When a network learns a new task, it adds a penalty that pulls each weight back toward its value after the old task. The stiffness of each penalty is set by how much that weight mattered for the old task. The family-level picture is on the [Regularisation-based Continual Learning](index.md) page.

## Overview

Kirkpatrick et al. (2017) start from catastrophic forgetting: a network trained on tasks one after another loses its performance on the earlier ones. Their remedy is to slow down learning on the weights that matter for the old tasks, and let the other weights move freely. The name follows the idea of synaptic consolidation in neuroscience. The paper tests the method on sequences of permuted MNIST tasks and on sequential learning of several Atari 2600 games. It claims that a single network can keep expertise on tasks it has not seen for a long time. The arXiv preprint dates from December 2016. The published version appeared in PNAS in 2017.

## Key concepts

- **Catastrophic forgetting**: gradient descent on a new task overwrites the weights that encoded an old one.
- **Anchor** \(\theta^*_{A}\): the parameter values learned on the old task A.
- **Fisher information** \(F_i\): for each parameter \(i\), a value that measures how sensitive the old task's likelihood is to changes in that weight. The paper uses only the diagonal. It notes that this equals the second derivative of the loss near a minimum, can be computed from first-order derivatives alone, and is positive semi-definite.
- **Strength** \(\lambda\): sets how strongly the old task is protected relative to the new one.
- **Laplace-style approximation**: the paper treats the posterior over old-task parameters as a Gaussian centred on \(\theta^*_A\), with precision given by the diagonal Fisher. The authors list the point estimate as a limitation (see below).

## How it works

Learning task B starts from the parameters found on task A. The loss for task B is augmented with a quadratic penalty:

\[
L(\theta) = L_B(\theta) + \sum_i \frac{\lambda}{2}\,F_i\,(\theta_i - \theta^*_{A,i})^2
\]

Each weight behaves like a spring attached to its old value, with stiffness \(\lambda F_i\). Weights with a small Fisher value are free to move, and weights with a large value stay close to where task A left them. After task A, the diagonal Fisher is computed and stored together with the anchor values. For a third task, a penalty for each earlier task is added and the penalties are summed.

For the Atari experiments, the paper recomputes the Fisher diagonal at each task switch, using 100 mini-batches from the replay buffer. The main text does not say whether the Fisher is estimated from sampled model predictions or from empirical gradients.

## Key methods

### Overcoming catastrophic forgetting in neural networks (Kirkpatrick et al., 2017)

- **Problem:** gradient-based training on a sequence of tasks overwrites the weights that earlier tasks depended on, so the network forgets. The paper frames learning tasks in sequence as crucial for artificial intelligence, and treats forgetting as the obstacle.
- **Core idea:** penalise changes to each weight in proportion to its estimated importance for the old task, using the Fisher information as the importance measure. Important weights stay close to their old values, and unimportant weights adapt to the new task.
- **Equation or algorithm:** the penalised loss above, with a diagonal Fisher computed after each task. One penalty term per old task extends the method to several tasks.
- **Results:** on the MNIST permutation tasks, the results appear only as figures, and the text gives no accuracy values. On sequential Atari 2600 games, the paper plots total human-normalised scores, capped at 10. The per-game scores appear only as plots, so this page does not quote them. The paper's settings include ten games per sequence, drawn at random from those that DQN plays at human level or above, and an EWC penalty scaling factor of 400 in the appendix. The paper reports that EWC does not reach the score of ten separate DQNs.
- **Limitations:** the paper's diagonal, point-estimate treatment of the weights is an approximation. It reports that EWC lets "a large number of tasks to be learned in sequence, with only modest growth in the error rates", but its figures show only a few task sequences, so the scaling claim is qualitative.

## Connections

- Other penalty and distillation methods in the same family, such as synaptic intelligence and learning without forgetting, are listed on the [Regularisation-based Continual Learning](index.md) page. They estimate importance online or distil old outputs instead of using the Fisher.
- The main alternative that keeps old data is [replay and memory](../replay-and-memory/index.md).
- Starting from a pre-trained model, as in [fine-tuning and adaptation](../../transfer/fine-tuning-and-adaptation/index.md), is a simpler way to reduce forgetting in many practical settings.
- A method that learns starting points for fast adaptation, rather than protecting old tasks, is [MAML](../../meta-learning/optimisation-based/maml.md).

## Open questions

- Would a fuller posterior, or a Bayesian treatment of the weights, fix the underestimated uncertainty at an acceptable cost? The paper suggests this but does not test it.
- How much does the choice of Fisher estimator, sampled or empirical, change the result?
- How well does a diagonal importance estimate hold up over many tasks?

## References

### Seminal papers

- Kirkpatrick, J. et al. (2017). Overcoming catastrophic forgetting in neural networks. *PNAS* 114(13), 3521–3526. https://pmc.ncbi.nlm.nih.gov/articles/PMC5380101 — Introduces EWC. The arXiv preprint is [arXiv:1612.00796](https://arxiv.org/abs/1612.00796).
- Zenke, F., Poole, B. & Ganguli, S. (2017). Continual Learning Through Synaptic Intelligence. arXiv:1703.04200. https://arxiv.org/abs/1703.04200 — Each connection tracks how useful it has been for earlier tasks during training, an alternative to a Fisher-based penalty.
- Li, Z. & Hoiem, D. (2016). Learning without Forgetting. arXiv:1606.09282. https://arxiv.org/abs/1606.09282 — Keeps earlier behaviour by distilling the old model's outputs on new data, so the old training data is not needed.

### Surveys and textbooks

- De Lange, M. et al. (2021). A continual learning survey: Defying forgetting in classification tasks. IEEE TPAMI. https://doi.org/10.1109/TPAMI.2021.3057446 (arXiv:1909.08383, https://arxiv.org/abs/1909.08383) — Compares regularisation, replay and architecture methods on common benchmarks.
- Parisi, G. I. et al. (2019). Continual Lifelong Learning with Neural Networks: A Review. arXiv:1802.07569. https://arxiv.org/abs/1802.07569 — Reviews continual learning methods for reducing catastrophic forgetting and their links to biological learning.
