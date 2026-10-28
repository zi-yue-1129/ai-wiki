---
related:
- theory/paradigms/transfer/fine-tuning-and-adaptation/index.md
tags:
  - meta-learning
  - MAML
  - few-shot learning
---

# Optimisation-based Meta-learning

Optimisation-based meta-learning learns an initialisation, or an update rule, that lets a model adapt to a new task in a few gradient steps. The meta-learner is trained across many tasks, and each task is a small training problem. The approach is model-agnostic in the sense that any network trained by gradient descent can be used.

## Overview

The standard formulation is bi-level. An inner loop adapts the parameters to one task using its small support set, and an outer loop updates the shared initialisation so that the adapted parameters perform well on that task's query set. Second-order gradients through the inner loop are expensive, which motivates first-order approximations.

## Main methods

- **MAML**: optimise the initialisation so that a few gradient steps give good performance on each new task.
- **Reptile**: a first-order method that moves the initialisation toward the parameters adapted on each task, avoiding second derivatives.
- **Latent embedding optimisation**: performs the adaptation in a low-dimensional latent space, which scales MAML-style learning to large networks.
- **Probabilistic MAML**: treats the initialisation as a distribution, so that the adapted model can express uncertainty about new tasks.

## Connections

The inner-loop adaptation is the same operation as [fine-tuning](../../transfer/fine-tuning-and-adaptation/index.md), but applied under many tasks so that the starting point is learned for fast adaptation. Metric and memory-based methods, described in the other subtopics, offer alternatives to gradient-based adaptation.

## Applications

Few-shot image classification, personalised models that adapt to a user after a few examples, and robot learning that adapts a policy to a new object or environment in a few trials.

## Open questions

The method is sensitive to hyperparameters, and performance on standard few-shot benchmarks is not always stronger than that of well-tuned simple baselines. Scaling to very large models and tasks with very different structure remains an open problem.

## References

### Seminal papers

- Finn, Abbeel & Levine (2017), "Model-agnostic meta-learning for fast adaptation of deep networks", ICML, arXiv:1703.03400 — MAML, which optimises an initialisation for fast adaptation with a few gradient steps.
- Nichol, Achiam & Schulman (2018), "On first-order meta-learning algorithms", arXiv:1803.02999 — Reptile and a family of first-order methods that avoid second-order gradients.
- Rusu et al. (2019), "Meta-learning with latent embedding optimization", ICLR, arXiv:1807.05960 — Performs adaptation in a learned latent space, which scales gradient-based meta-learning.
- Finn, Xu & Levine (2018), "Probabilistic model-agnostic meta-learning", NeurIPS, arXiv:1806.02817 — Places a distribution over initialisations so that adaptation carries uncertainty.

### Surveys and textbooks

- Hospedales, Antoniou, Micaelli & Storkey (2021), "Meta-learning in neural networks: a survey", IEEE TPAMI, arXiv:2004.05439 — Survey of meta-learning that places gradient-based methods among the other families.

### Lectures and videos

No further entries for this page.

### Articles and documentation

No further entries for this page.

## Further reading

- Antoniou, Edwards & Storkey (2019), "How to train your MAML", ICLR. https://arxiv.org/abs/1810.09502 — Lists the changes that make MAML stable and cheaper to train.
