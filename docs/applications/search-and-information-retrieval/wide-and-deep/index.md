---
status: draft
last_reviewed: 2026-10-28
tags:
  - recommendation
  - supervised learning
aliases:
  - Wide & Deep
  - 寬且深學習
---

# Wide & Deep (Cheng et al. 2016)

Wide & Deep is a recommendation model that trains a linear "wide" component and a deep neural "deep" component together, so that it both memorises specific feature combinations and generalises to new ones. Cheng and colleagues built it for app recommendations on Google Play. It is one of the landmark methods for [ads and recommendation ranking](../index.md), covered in the parent page [Search Engines and Information Retrieval](../index.md).

## Overview

Recommendation data are sparse. Most users have used only a few of the apps in the store, and most features, such as a particular installed app or a country, are rare. A linear model with hand-built cross features, such as "installed app X and viewing app Y", memorises which combinations lead to installs, but it cannot score combinations it has never seen. A deep network with embeddings generalises to unseen combinations, but it can over-generalise and recommend loosely related items when user–item interactions are sparse.

## Key concepts

- **Memorisation**: learning that a specific feature combination predicts a click or install. Cross-product features make this explicit.
- **Generalisation**: transferring what is known about related items to combinations that were never observed, through learned embeddings.
- **Embedding**: a dense, low-dimensional vector for a categorical value such as an app ID. Embeddings are learned during training.
- **Joint training**: the two parts are trained together on one loss, unlike an ensemble, where each part is trained separately and their predictions are averaged.

## How it works

The wide part is a linear model over the raw features $x$ and their cross-product transformations $\phi(x)$. The deep part is a feed-forward network whose final activation is $a^{(l_f)}$. The model predicts

$$
P(Y=1 \mid x) = \sigma\left(w_{\text{wide}}^{\top}[x, \phi(x)] + w_{\text{deep}}^{\top} a^{(l_f)} + b\right)
$$

where $\sigma$ is the sigmoid and $b$ is a bias. Both parts feed one logistic output and are trained with one logistic loss.

The procedure in the paper is:

1. Generate training data from logged impressions, with categorical values mapped to integer IDs and continuous values normalised.
2. Form the wide input from raw features and the cross-product features that the engineers have chosen.
3. Map each categorical feature to an embedding, concatenate the embeddings with the continuous features, and pass them through hidden layers to obtain $a^{(l_f)}$.
4. Compute the joint prediction and minimise the logistic loss, using FTRL with L1 regularisation for the wide weights and AdaGrad for the deep weights.
5. Serve the model: for each request, score a candidate list in batches and sort the apps by predicted score.

## Results

The paper reports offline and online results on Google Play. The offline AUC was 0.726 for the wide-only control, 0.722 for the deep-only model and 0.728 for Wide & Deep. In a live A/B test that ran for three weeks, with 1% of users in each group, Wide & Deep increased app acquisitions on the main landing page by 3.9% relative to the wide-only control, and by about 1% relative to the deep-only model.

## Limitations

- **Manual cross features.** The wide part depends on cross-product features chosen by engineers, which the paper acknowledges as a burden. The deep part reduces that work but does not remove it.
- **One platform.** The evidence comes from one commercial app store, and the online gains were measured against specific baselines.
- **Small offline gap.** The offline AUC differences are small while the online differences are larger, so offline metrics alone were not enough to predict the online effect.

## Open questions

- Whether automatic feature interaction, learned by the network itself, can replace hand-chosen cross features without losing the memorisation benefit. [DeepFM](https://arxiv.org/abs/1703.04247) (Guo et al., 2017) combines a factorisation machine with a deep network that shares the same embeddings.
- How to model a user's history in a way that depends on the candidate item. The Deep Interest Network (Zhou et al., 2017) uses attention over past behaviour for this purpose.

## Connections

- The wide part is a regularised linear model, see [Linear models](../../../theory/paradigms/supervised/linear-models/index.md), and the deep part is a [multilayer perceptron](../../../theory/models/mlp/index.md).
- The model is trained as a supervised classifier, using the logistic loss covered in [Loss functions and optimisation](../../../theory/paradigms/supervised/loss-functions-and-optimization/index.md).
- Recommendation is also a sequential decision problem, which the [contextual bandits](../../../theory/paradigms/online/contextual-bandits/index.md) page treats with exploration in mind.

## Applications

Wide & Deep-style models score candidate apps, videos, products and ads in production recommendation and advertising systems. Click-through prediction for ads is the best-known use: the model estimates the probability of a click, which is then combined with a bid to rank ads.

## References

### Seminal papers

- Cheng, H.-T. et al. (2016). Wide & Deep learning for recommender systems. https://arxiv.org/abs/1606.07792 — Jointly trains a linear model over cross-product features and a deep network, and reports an online gain in app acquisitions on Google Play.
- Guo, H. et al. (2017). DeepFM: A factorization-machine based neural network for CTR prediction. https://arxiv.org/abs/1703.04247 — Combines a factorisation machine and a deep network over shared embeddings, removing the need for hand-built cross features.
- Zhou, G. et al. (2017). Deep interest network for click-through rate prediction. https://arxiv.org/abs/1706.06978 — Uses attention over a user's past behaviour to build an interest vector for each candidate ad, deployed in Alibaba display advertising.
- Covington, P., Adams, J. & Sargin, E. (2016). Deep neural networks for YouTube recommendations. RecSys. https://doi.org/10.1145/2959100.2959190 — Describes two-stage candidate-generation and ranking networks for video recommendation at scale.
- Richardson, M., Dominowska, E. & Ragno, R. (2007). Predicting clicks. WWW. https://doi.org/10.1145/1242572.1242643 — Estimates click-through rates for new sponsored-search ads, where little click history exists yet.
