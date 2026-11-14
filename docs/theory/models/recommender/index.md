---
status: draft
last_reviewed: 2026-11-14
related:
  - theory/models/embeddings/index.md
tags:
  - recommender systems
  - collaborative filtering
  - ranking
aliases:
  - Recommender systems
  - 推薦系統
  - 協同過濾
  - collaborative filtering
---

# Recommender Systems

A recommender system predicts which items a user is likely to prefer, and uses those predictions to choose what to show. Films, products, songs, posts and job listings are chosen this way on most large platforms. Unlike classification, the output is a ranking over a very large catalogue, and the data are sparse: a typical user has interacted with a tiny fraction of the items.

## Overview

The basic data are a user–item matrix whose entries record interactions. Some entries are explicit ratings, such as a one- to five-star score. Most are implicit feedback, such as clicks, views or purchases, where a missing entry means either "not interested" or "never seen". This ambiguity shapes both the models and the way they are evaluated.

Three broad approaches are used. **Collaborative filtering** predicts a user's preference from the behaviour of other users or from similar items, without needing item content. **Content-based** methods use item features and the user's history. **Hybrid** systems combine both, which helps when a new user or item has little history, the cold-start problem.

## Key concepts

- **Implicit and explicit feedback**: observed interactions versus stated ratings. Implicit feedback is far more common and gives no direct negatives.
- **Latent factors**: a low-dimensional vector for each user and each item, whose inner product approximates the preference.
- **Top-N ranking**: the usual output. The task is to order a short list correctly, not to predict every rating accurately.
- **Cold start**: the problem of recommending for users or items with no history.
- **Negative sampling**: choosing unobserved items as negative examples when only positives are observed.

## How it works

**Neighbourhood methods.** Sarwar et al. (2001) study item-based collaborative filtering, which predicts a user's preference from the user's own ratings of similar items rather than from similar users. The method is simple and interpretable, and item similarities can be computed ahead of time. Its own page is still to be written.

**Matrix factorisation.** Koren, Bell and Volinsky (2009) describe the factorisation approach that became standard in large rating-prediction problems. Each user and item receives a latent vector, and their inner product predicts the rating. The vectors are fitted to the observed ratings with regularisation, and the same vectors are reused as embeddings, see [Embeddings and Representation Learning](../embeddings/index.md). Details are on the [Matrix Factorization](matrix-factorization.md) page.

**Learning from implicit feedback.** Rendle et al. (2012) note that the most common scenario is implicit feedback, such as clicks and purchases. Their Bayesian Personalised Ranking (BPR) objective trains on pairs: an observed item should be ranked above an unobserved one for the same user. This optimises the ranking directly, rather than fitting a rating. See the [BPR](bpr.md) page.

**Neural collaborative filtering.** He et al. (2017) replace the inner product of matrix factorisation with a neural network, which can learn an interaction function from data. See the [Neural Collaborative Filtering](neural-cf.md) page.

## Key methods

Brief comparison, with a link to each method's own page.

- **[Matrix factorisation (Koren et al., 2009)](matrix-factorization.md)**: latent factors fitted to ratings, with biases. Strong for rating prediction, and its vectors serve as embeddings.
- **[BPR (Rendle et al., 2012)](bpr.md)**: a pairwise ranking loss on implicit feedback, the standard starting point for top-N ranking.
- **[Neural collaborative filtering (He et al., 2017)](neural-cf.md)**: a learned interaction function in place of the inner product. More flexible, with more to tune, and it is evaluated on top-N ranking.

Item-based neighbourhood methods (Sarwar et al., 2001) are a separate family that needs no latent factors. They are mentioned above and are a candidate for a method page of their own.

## Connections

Recommendation shares its representation tools with [Embeddings and Representation Learning](../embeddings/index.md): user and item vectors are embeddings, and approximate nearest-neighbour search retrieves candidates from them. Sequence models such as the [Transformer](../transformer/index.md) are used when the order of a user's interactions matters. The sequential side of recommendation also overlaps with [Reinforcement Learning](../../paradigms/reinforcement-learning/index.md), because a recommendation changes what the user does next.

## Applications

- **Streaming and media.** Ranking films, music and videos for each user.
- **E-commerce.** Showing products a shopper is likely to buy, or pairing items with similar ones.
- **News and social feeds.** Ordering posts by predicted engagement, with questions about what is shown as a result.

## Open questions

- Offline evaluation can disagree with online results, because logged data reflect the previous recommender and not the full set of options.
- Recommendations shape the data that the next model learns from, which can create feedback loops and narrow what users see.
- Cold-start users and items need content or side information, and how to combine these well is unsettled.
- Fairness across providers and user groups is hard to define, and different definitions can conflict.

## References

### Seminal papers

- Sarwar, B., Karypis, G., Konstan, J. & Riedl, J. (2001). Item-based collaborative filtering recommendation algorithms. In *Proceedings of the 10th International World Wide Web Conference (WWW10)*, pp. 285–295. https://doi.org/10.1145/371920.372071 — Introduces item-based neighbourhood methods for collaborative filtering.
- Koren, Y., Bell, R. & Volinsky, C. (2009). Matrix factorization techniques for recommender systems. *Computer*, 42, pp. 30–37. https://doi.org/10.1109/MC.2009.263 — Describes latent-factor models fitted to ratings, the standard matrix factorisation approach.
- Rendle, S., Freudenthaler, C., Gantner, Z. & Schmidt-Thieme, L. (2012). *BPR: Bayesian Personalized Ranking from Implicit Feedback*. arXiv:1205.2618, first published at UAI 2009. https://arxiv.org/abs/1205.2618 — Pairwise ranking objective for implicit feedback, with a Bayesian derivation.
- He, X., Liao, L., Zhang, H., Nie, L., Hu, X. & Chua, T.-S. (2017). Neural collaborative filtering. In *Proceedings of the 26th International Conference on World Wide Web (WWW 2017)*, pp. 173–182. https://doi.org/10.1145/3038912.3052569 — Replaces the inner product in matrix factorisation with a neural network that learns the interaction function.

### Surveys and textbooks

- Ricci, F., Rokach, L. & Shapira, B. (eds.) (2015). *Recommender Systems Handbook*, 2nd ed. Springer. https://doi.org/10.1007/978-1-4899-7637-6 — Reference handbook covering collaborative, content-based and hybrid methods, and evaluation.
