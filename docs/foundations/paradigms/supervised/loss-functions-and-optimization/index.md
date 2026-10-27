---
tags:
  - supervised learning
  - optimization
  - loss functions
---

# Loss Functions, Regularisation and Optimisation

How a supervised learner is told what "wrong" means, how it is kept from memorising, and how its parameters are actually found.

## Loss functions

| Task | Loss | Notes |
|---|---|---|
| Regression | Squared error | Optimal predictor is the conditional mean; sensitive to outliers |
| Regression | Absolute / Huber | Median-like; robust |
| Classification | Cross-entropy $-\log p_\theta(y\mid x)$ | Maximum likelihood; gives probabilities |
| Classification | Hinge | Margin-based, used by SVMs |
| Imbalanced | Focal loss, class weights | Down-weight easy majority examples |
| Ranking | Pairwise / listwise (RankNet, LambdaRank) | Optimise order, not value |
| Segmentation | Dice, IoU losses | Handle region overlap |

A **surrogate loss** replaces the intractable 0–1 loss with a convex bound; classification-calibrated surrogates (Bartlett, Jordan & McAuliffe, 2006) preserve the optimal classifier.

## Regularisation

Anything that restricts the hypothesis to generalise better: weight penalties ($\ell_1$, $\ell_2$), dropout, early stopping, data augmentation, label smoothing, mixup, and limiting model size. Many of these have a Bayesian reading as priors. Large networks trained by SGD also show **implicit regularisation**, where the optimiser itself prefers simpler solutions.

## Optimisation

Training minimises the empirical risk $\hat R(\theta)=\frac1n\sum_i L(f_\theta(x_i),y_i)$.

- **Gradient descent**: $\theta\leftarrow\theta-\eta\nabla\hat R(\theta)$. **Stochastic / mini-batch** versions use a noisy gradient on a subset, which is cheaper and helps escape sharp minima.
- **Momentum, RMSProp, Adam** (Kingma & Ba, 2015, arXiv:1412.6980) adapt step directions and sizes.
- **Learning-rate schedules** (warm-up, cosine decay) matter as much as the choice of optimiser.
- Convex problems (linear models, SVMs) have a single global optimum; deep networks do not, yet SGD works surprisingly well.

## Connections

The same objective underlies [self-supervised](../../self-supervised/index.md) pre-training; only the source of labels changes. See also [Deep Learning](../../../deep-learning/index.md) for backpropagation, and the roadmap entry for a full Optimization page.

## Further reading

- Goodfellow, Bengio & Courville, *Deep Learning*, chapters 7–8.
- Ruder (2016), "An overview of gradient descent optimization algorithms", arXiv:1609.04747.
