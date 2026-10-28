---
status: draft
last_reviewed: 2026-10-28
tags:
  - deep learning
  - optimization
  - initialisation
  - scaling
aliases:
  - Maximal update parametrisation
  - Maximal update parametrization
  - muP
  - μP
  - muTransfer
  - 最大更新參數化
---

# Maximal Update Parametrisation (muP)

The maximal update parametrisation, or muP, is a rule for how the initialisation scale and per-layer learning rates should change with network width, so that every layer learns at a comparable rate as the network grows. Yang and Hu introduced it in 2021 in a study of infinitely wide networks. Its practical use is hyperparameter transfer: a learning rate tuned on a small model can be reused for a much larger one. It is one of the methods compared on the parent [weight initialisation](../index.md) page.

## Overview

Practitioners usually choose an initialisation and a global learning rate from experience with one model size. When the model is made wider, the best learning rate usually moves, so each size needs its own search, which is too expensive for the largest models.

Yang and Hu (2021) asked what happens to training as width tends to infinity. They showed that the standard and neural tangent kernel (NTK) parametrisations have no infinite-width limit in which features learn. In the standard parametrisation, the updates to different layers become unbalanced as width grows. They proposed a modified parametrisation that keeps each layer's update size comparable. Yang et al. (2022), in Tensor Programs V, showed that under it many optimal hyperparameters stay stable as the model grows, so they can be tuned on a small model and transferred to a large one.

## Key concepts

- **Standard parametrisation (SP).** The default in common frameworks: initial variance proportional to the inverse fan-in, and a learning rate that does not depend on width.
- **Feature learning.** Training in which hidden representations change substantially. In the infinite-width limit of the standard and NTK parametrisations, hidden features do not change.
- **muTransfer.** Tuning on small models in muP, then transferring the settings to a larger model.

## How it works

The rule specifies how each parameter's initial variance and learning rate scale with width. For the Adam optimiser, Yang et al. (2022) give the following, with \(\text{fan\_in}\) the number of inputs to the layer:

| Parameter type | Initial variance (muP) | Adam learning rate (muP) |
|---|---|---|
| Input weights and biases | \(1/\text{fan\_in}\) | constant in width |
| Hidden weights | \(1/\text{fan\_in}\) | \(1/\text{fan\_in}\) |
| Output weights | \(1/\text{fan\_in}^2\) | \(1/\text{fan\_in}\) |

Under the standard parametrisation the hidden-layer learning rate is constant in width, which causes the imbalance. The hidden-layer initialisation is the same fan-in scaling as He initialisation, so the main changes are in the output layer and the learning rates. For Transformers the paper also scales attention logits by \(1/d_{\text{head}}\) rather than \(1/\sqrt{d_{\text{head}}}\). Its table gives separate learning-rate rows for SGD and Adam, because the scalings differ.

The muTransfer procedure is:

1. Write the target model in the muP parametrisation.
2. Train several small models of the same architecture at different widths, and tune the learning rate and other hyperparameters on them.
3. Train the large model with the best small-model settings, without tuning it directly.

In Tensor Programs V the optimal settings found this way are stable across widths, whereas under the standard parametrisation the optimum moves.

## Results

The figures below are the paper's own, taken from its abstract. Yang et al. (2022) verified muTransfer on Transformer and ResNet models. Transferring pretraining hyperparameters from a 13-million-parameter model gave results above published numbers for BERT-large (350 million parameters), at a total tuning cost equal to pretraining BERT-large once. Transferring from a 40-million-parameter model exceeded published numbers for the 6.7-billion-parameter GPT-3, with tuning costing about 7% of total pretraining cost.

Yang and Hu (2021) also report that their limits beat NTK baselines and finite-width networks on Word2Vec and few-shot Omniglot learning, tasks that depend on feature learning.

## Limitations

- **The theory concerns width.** Transfer across depth is not covered by the same argument, and the paper's rules do not settle it.
- **The limit is infinite; practice is finite.** The rules are derived as width tends to infinity, and their accuracy at finite width is shown empirically rather than proved.
- **Architecture- and optimiser-specific.** Transformers need the attention change, and the SGD and Adam scalings differ, so a setting derived for one does not carry over to the other.
- **Not every hyperparameter is covered.** The transfer experiments focus on the learning rate, initialisation scale and multipliers; other settings need separate checks.

## Open questions

- Whether a depth analogue of muP exists that transfers settings across depth as well as width.
- Whether the feature-learning advantages of the infinite-width analysis hold for practical models and tasks beyond the paper's examples.
- How muP interacts with normalisation layers, which remove some of the scale dependence that the parametrisation controls.

## References

### Seminal papers

- Yang, G. & Hu, E. J. (2021). *Feature Learning in Infinite-Width Neural Networks*. arXiv. https://arxiv.org/abs/2011.14522 — Shows that the standard and NTK parametrisations have no feature-learning infinite-width limit and proposes the maximal update parametrisation.
- Yang, G., Hu, E. J., Babuschkin, I., Sidor, S., Liu, X., Farhi, D. et al. (2022). *Tensor Programs V: Tuning Large Neural Networks via Zero-Shot Hyperparameter Transfer*. arXiv. https://arxiv.org/abs/2203.03466 — Introduces muTransfer, which tunes hyperparameters on small models and transfers them to large Transformers and ResNets.
- Glorot, X. & Bengio, Y. (2010). *Understanding the difficulty of training deep feedforward neural networks*. AISTATS. https://proceedings.mlr.press/v9/glorot10a.html — The normalised initialisation, a fan-based scaling of the kind the standard parametrisation uses.
- He, K., Zhang, X., Ren, S. & Sun, J. (2015). *Delving Deep into Rectifiers: Surpassing Human-Level Performance on ImageNet Classification*. arXiv. https://arxiv.org/abs/1502.01852 — Derives the fan-in scaled initialisation for rectified networks, the scaling that muP keeps for hidden layers.
- Lee, J., Bahri, Y., Novak, R., Schoenholz, S. S., Pennington, J. & Sohl-Dickstein, J. (2018). *Deep Neural Networks as Gaussian Processes*. arXiv. https://arxiv.org/abs/1711.00165 — Shows that infinitely wide deep networks are equivalent to Gaussian processes, the kernel regime that the standard parametrisation reaches at large width.
