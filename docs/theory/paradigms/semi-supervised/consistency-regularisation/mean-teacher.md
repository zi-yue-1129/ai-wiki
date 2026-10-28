---
status: complete
last_reviewed: 2026-10-28
related:
  - theory/paradigms/semi-supervised/consistency-regularisation
  - theory/paradigms/semi-supervised/pseudo-labelling-and-self-training
  - theory/models/computer-vision
tags:
  - semi-supervised learning
  - consistency regularisation
  - exponential moving average
aliases:
  - 平均教師
  - Mean Teacher
  - Mean teachers are better role models
---

# Mean Teacher

Mean Teacher trains a student network to match the predictions of a teacher network, where the teacher's weights are an exponential moving average (EMA) of the student's. The student is trained on labelled data with the usual loss, and on all data with a consistency loss against the teacher. Averaging the weights, rather than the predictions, gives targets that change smoothly and are more accurate than the student alone. The family-level picture is on the [Consistency Regularisation](index.md) page.

## Overview

Tarvainen and Valpola (2017) present Mean Teacher. It builds on Temporal Ensembling, whose targets are averages of predictions from earlier epochs. Mean Teacher averages the weights instead, and updates the teacher after every training step. The abstract reports several results. On SVHN with 250 labels it reaches 4.35% error. On CIFAR-10 with 4000 labels, a ResNet improves the state of the art from 10.55% to 6.28% error. On ImageNet with 10% of the labels, the error falls from 35.24% to 9.11%.

## Key concepts

- **Student**: the model being trained, with weights \(\theta\).
- **Teacher**: a second network whose weights \(\theta'\) are an exponential moving average of the student's.
- **Smoothing coefficient** \(\alpha\): close to 1. The paper uses 0.99 for the ConvNet on SVHN and 0.999 for the ConvNet on CIFAR-10, 0.97 and 0.99 for the ResNet on CIFAR-10 with 1000 and 4000 labels, and 0.9997 for the ResNet on ImageNet.
- **Consistency cost**: a distance between the student's and the teacher's softmax outputs, computed under different noise and augmentation. The teacher is treated as a constant, so no gradient flows into it.
- **Ramp-up**: the weight of the consistency term rises from zero during early training.

## How it works

After each training step, the teacher's weights are updated from the student's:

\[
\theta'_t = \alpha\,\theta'_{t-1} + (1-\alpha)\,\theta_t
\]

The consistency cost is the expected squared distance between the student's and the teacher's outputs over inputs and two independent noise draws, \(\eta\) for the student and \(\eta'\) for the teacher:

\[
J_{\text{cons}}(\theta) = \mathbb E_{x,\eta,\eta'}\Big[\big\|f(x;\theta,\eta) - f(x;\theta',\eta')\big\|^2\Big]
\]

The paper uses mean squared error on the softmax outputs as the consistency cost in most experiments. For ImageNet it uses KL divergence. The total cost is a weighted sum of the classification cost on labelled examples and the consistency cost on all examples. The paper gives no single equation for it. The consistency weight is ramped up over early training. For the ConvNet, Appendix B.1 gives a sigmoid-shaped ramp over 40,000 steps. Section 3 says "the first 80 epochs", which conflicts with the appendix, so this page uses the appendix value.

Each step computes the student's and the teacher's outputs on the same batch with different noise, computes the loss, takes a gradient step on the student only, and then updates the teacher by the EMA.

## Key methods

### Mean teachers are better role models (Tarvainen & Valpola, 2017)

- **Problem:** Temporal Ensembling's targets are averages of predictions from earlier epochs, so they lag behind the current model. The paper asks whether averaging the weights gives better targets.
- **Core idea:** use a teacher built from an EMA of the student's weights, and train the student to match the teacher's predictions under different noise. The EMA smooths the target across many steps without a per-example memory.
- **Equation or algorithm:** the EMA update, the consistency cost and the weighted total cost, as above.
- **Results:**
  - SVHN, error over 10 runs (Table 1): 4.35 ± 0.50% with 250 labels, 4.18 ± 0.27% with 500, 3.95 ± 0.19% with 1000, and 2.50 ± 0.05% with all labels.
  - CIFAR-10, ConvNet, error over 10 runs (Table 2): 21.55 ± 1.48% with 1000 labels, 15.73 ± 0.31% with 2000, 12.31 ± 0.28% with 4000, and 5.94 ± 0.15% with all labels.
  - CIFAR-10 with 4000 labels, ResNet (Table 4): 6.28 ± 0.15%, against 10.55% for the previous best, VAT+EntMin.
  - ImageNet with 10% of the labels, ResNet, on the validation set: 9.11% error, averaged over two runs.
  - With all labels, Mean Teacher and the Π model are almost identical, so the gains come mainly in the low-label regime.
- **Limitations:** the paper reports that VAT beats Mean Teacher in some settings. With the ConvNet, VAT reaches 3.86% against 3.95% on SVHN with 1000 labels, and 10.55% against 12.31% on CIFAR-10 with 4000 labels. Combining Mean Teacher with VAT is "outside the scope of this paper". Good values for \(\alpha\) and the consistency weight span roughly an order of magnitude, and performance "degrades quickly" outside that range. ImageNet results use the validation set, because the test set is not public. The authors say that the reason MSE works better than KL divergence "remains unclear".

## Connections

- The predecessor method, Temporal Ensembling, is part of the [Consistency Regularisation](index.md) family.
- [FixMatch](fixmatch.md) replaces the teacher with thresholded pseudo-labels from weak and strong augmentations.
- Mean Teacher's teacher outputs act as soft pseudo-labels, so it is also a self-training method. See [pseudo-labelling and self-training](../pseudo-labelling-and-self-training/index.md).
- Virtual adversarial training, the adversarial perturbation method that Mean Teacher is compared with, is a related consistency method.
- The general semi-supervised picture is on the [Semi-supervised Learning](../index.md) page.
- The choice of augmentation and noise is central to these methods. See [computer vision](../../../models/computer-vision/index.md).

## Open questions

- Why does MSE work better than KL divergence as the consistency cost? The paper leaves this open.
- How should \(\alpha\) be set for a new dataset or model size, given that the good range is broad but still narrow?
- Would adding adversarial perturbations, as VAT does, improve Mean Teacher? The paper calls this outside its scope.

## References

### Seminal papers

- Tarvainen, A. & Valpola, H. (2017). Mean teachers are better role models: Weight-averaged consistency targets improve semi-supervised deep learning results. arXiv:1703.01780. https://arxiv.org/abs/1703.01780 — Introduces Mean Teacher, with the teacher built from an EMA of the student's weights.
- Laine, S. & Aila, T. (2017). Temporal Ensembling for Semi-Supervised Learning. arXiv:1610.02242. https://arxiv.org/abs/1610.02242 — The predecessor method, which uses averaged predictions from earlier epochs as targets.
- Sohn, K. et al. (2020). FixMatch: Simplifying Semi-Supervised Learning with Consistency and Confidence. arXiv:2001.07685. https://arxiv.org/abs/2001.07685 — Uses confident pseudo-labels from weak augmentations as targets for strong ones.
- Miyato, T., Maeda, S., Koyama, M. & Ishii, S. (2018). Virtual Adversarial Training: A Regularization Method for Supervised and Semi-supervised Learning. arXiv:1704.03976. https://arxiv.org/abs/1704.03976 — Adversarial consistency regularisation, the baseline that Mean Teacher is compared with and beats in some settings.

### Surveys and textbooks

- Oliver, A. et al. (2018). Realistic Evaluation of Deep Semi-Supervised Learning Algorithms. arXiv:1804.09170. https://arxiv.org/abs/1804.09170 — Shows that many reported gains shrink when baselines are tuned fairly.
