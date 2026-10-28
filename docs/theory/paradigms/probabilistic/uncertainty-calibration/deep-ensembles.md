---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/probabilistic/uncertainty-calibration
tags:
  - uncertainty quantification
  - ensembles
  - neural networks
aliases:
  - 深度集成
  - Deep ensembles
  - Neural network ensembles
---

# Deep Ensembles

A deep ensemble trains several neural networks independently, each from a different random initialisation and data order, and averages their predictive distributions. The spread of the members' predictions gives an estimate of uncertainty. Part of [Uncertainty quantification and calibration](index.md).

## Overview

Averaging several models often improves accuracy, a fact known from the early neural-network ensemble work (Hansen & Salamon, 1990). Lakshminarayanan et al. (2017) showed that ensembles of networks, each trained with a proper scoring rule, also give well-calibrated uncertainty, including on inputs far from the training data. The method needs no change to the architecture and is simple to implement.

## Key concepts

- **Ensemble member**: a network with its own random initialisation and training order.
- **Mixture prediction**: the average of the members' predictive distributions, \(p(y\mid x)=\frac{1}{M}\sum_m p_m(y\mid x)\).
- **Disagreement**: the variation between members, which is larger where the data are unfamiliar.
- **Proper scoring rule**: the negative log-likelihood, which trains each member to report calibrated probabilities.

## How it works

Train \(M\) networks on the same data, each with different random seeds. For a new input, average the predicted distributions. The average is the ensemble's prediction, and its entropy or the disagreement between members serves as an uncertainty measure. Lakshminarayanan et al. (2017) also add adversarial training to encourage smoothness, and they train each member to output both a mean and a variance for regression.

Fort, Hu and Lakshminarayanan (2019) argue that the diversity of ensemble members comes from their different basins in the loss landscape, which explains why independently trained networks disagree more than networks from a single run.

## Variants

- **Snapshot ensembles** collect models from different points along one training run, which costs less but gives less diversity.
- **Randomised ensembles** change the data order, augmentations or architecture across members.
- **Bayesian-style ensembles** combine the averaging with a prior or with approximate posterior samples, linking the method to Bayesian inference (Gal & Ghahramani, 2016).

## Results and limits

- Ensembles improve both accuracy and calibration and are robust across tasks, which is why they are a strong baseline.
- The cost grows linearly with the number of members, both at training and at inference time.
- Members can be too similar, so the diversity that gives the uncertainty estimate may be smaller than expected.
- An ensemble is not a true posterior over parameters. Its uncertainty is an empirical estimate and has no general guarantee.

## Applications

- **Image classification and regression**: strong baselines for accuracy and calibrated confidence (Lakshminarayanan et al., 2017).
- **Out-of-distribution detection**: flagging inputs on which members disagree.
- **Safety-critical prediction**: using disagreement to decide when to defer to a person.

## Open questions

- How many members, and how much diversity, are needed for good uncertainty at a fixed compute budget.
- Whether ensembles provide reliable uncertainty for very large models, where training each member is expensive.

## References

### Seminal papers

- Lakshminarayanan, B., Pritzel, A. & Blundell, C. (2017). Simple and scalable predictive uncertainty estimation using deep ensembles. In *Advances in Neural Information Processing Systems* 30. https://proceedings.neurips.cc/paper/2017/hash/9ef2ed4b7fd2c810847ffa5fa85bce38-Abstract.html — Introduces deep ensembles for predictive uncertainty.
- Hansen, L. K. & Salamon, P. (1990). Neural network ensembles. *IEEE Transactions on Pattern Analysis and Machine Intelligence* 12(10), 993–1001. https://doi.org/10.1109/34.58871 — Early analysis showing that averaging neural networks improves generalisation.
- Gal, Y. & Ghahramani, Z. (2016). Dropout as a Bayesian approximation: representing model uncertainty in deep learning. In *Proceedings of the 33rd International Conference on Machine Learning*, PMLR 48. https://proceedings.mlr.press/v48/gal16.html — Relates ensembles of dropout-trained networks to approximate Bayesian inference.

### Surveys and textbooks

- Fort, S., Hu, H. & Lakshminarayanan, B. (2019). Deep ensembles: a loss landscape perspective. arXiv:1912.02757. https://arxiv.org/abs/1912.02757 — Explains why independently trained members diverge and how that affects uncertainty.
- Guo, C., Pleiss, G., Sun, Y. & Weinberger, K. Q. (2017). On calibration of modern neural networks. In *Proceedings of the 34th International Conference on Machine Learning*, PMLR 70. https://proceedings.mlr.press/v70/guo17a.html — Compares deep ensembles with post-hoc calibration methods for neural networks.
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. https://github.com/probml/pml-book — Free textbook; covers ensembles and Bayesian model averaging.
